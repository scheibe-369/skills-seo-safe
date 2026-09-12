#!/usr/bin/env python3
"""Install site-seo-release into a project's local agent directories."""

from __future__ import annotations

import argparse
import codecs
import os
import shutil
import stat
import sys
import uuid
from dataclasses import dataclass
from pathlib import Path


SKILL_NAME = "site-seo-release"
START_MARKER = f"<!-- {SKILL_NAME}:start -->"
END_MARKER = f"<!-- {SKILL_NAME}:end -->"
TEXT_SUFFIXES = {"", ".md", ".yaml", ".yml", ".py", ".json", ".txt"}


class InstallError(RuntimeError):
    """Raised when installation cannot proceed without risking user data."""


@dataclass(frozen=True)
class Host:
    name: str
    skill_relative_path: Path
    instructions_file: str

    @property
    def managed_block(self) -> str:
        skill_path = self.skill_relative_path.as_posix() + "/SKILL.md"
        return (
            f"{START_MARKER}\n"
            f"## Site SEO Release\n\n"
            f"Leia `{skill_path}` ao criar, reformular, alterar de forma relevante ou "
            "finalizar site público ou landing page, inclusive o fechamento de página "
            "privada ou noindex. Crie ou atualize `SEO-SPEC.md` e, "
            "na revisão final, `tasks/site-release.md` e `tasks/site-release.json` com "
            "evidências e pendências. Reutilize a skill já carregada enquanto o contexto "
            "estiver atual.\n"
            f"{END_MARKER}"
        )


HOSTS = {
    "codex": Host(
        name="Codex",
        skill_relative_path=Path(".agents/skills") / SKILL_NAME,
        instructions_file="AGENTS.md",
    ),
    "claude": Host(
        name="Claude",
        skill_relative_path=Path(".claude/skills") / SKILL_NAME,
        instructions_file="CLAUDE.md",
    ),
}


def _is_ignored(path: Path) -> bool:
    return path.name == "__pycache__" or path.suffix == ".pyc"


def _normalize_text(data: bytes) -> bytes:
    # Git checkouts with core.autocrlf rewrite line endings; compare content, not EOL.
    if data.startswith(codecs.BOM_UTF8):
        data = data[len(codecs.BOM_UTF8):]
    return data.replace(b"\r\n", b"\n")


def _newline_for(data: bytes) -> bytes:
    return b"\r\n" if b"\r\n" in data else b"\n"


def _write_atomic(path: Path, data: bytes) -> None:
    temporary = path.parent / f".{SKILL_NAME}.{uuid.uuid4()}.tmp"
    try:
        with open(temporary, "xb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        if path.exists():
            shutil.copymode(path, temporary)
        os.replace(temporary, path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def _lexical_absolute(path: Path) -> Path:
    return Path(os.path.abspath(os.fspath(path)))


def _is_link(path: Path) -> bool:
    try:
        if path.is_symlink():
            return True
        is_junction = getattr(os.path, "isjunction", None)
        if is_junction is not None and is_junction(path):
            return True
        if os.name == "nt":
            attributes = getattr(path.lstat(), "st_file_attributes", 0)
            reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
            return bool(attributes & reparse_flag)
    except FileNotFoundError:
        return False
    except OSError as exc:
        raise InstallError(f"Cannot inspect path component: {path}") from exc
    return False


def _reject_symlink_chain(path: Path, label: str) -> None:
    current = _lexical_absolute(path)
    chain = list(reversed(current.parents)) + [current]
    for component in chain:
        if _is_link(component):
            raise InstallError(
                f"Refusing {label}: symlink, junction or reparse point in path: {component}"
            )


def _reject_tree_symlinks(root: Path, label: str) -> None:
    if _is_link(root):
        raise InstallError(f"Refusing {label}: symlink: {root}")
    if not root.exists():
        return
    if not root.is_dir():
        raise InstallError(f"Refusing {label}: expected a directory: {root}")

    for directory, dirnames, filenames in os.walk(root, followlinks=False):
        directory_path = Path(directory)
        for name in [*dirnames, *filenames]:
            candidate = directory_path / name
            if _is_link(candidate):
                raise InstallError(f"Refusing {label}: symlink: {candidate}")


def _tree_manifest(root: Path) -> dict[str, bytes | None]:
    manifest: dict[str, bytes | None] = {".": None}
    for directory, dirnames, filenames in os.walk(root, followlinks=False):
        directory_path = Path(directory)
        dirnames[:] = sorted(name for name in dirnames if name != "__pycache__")
        relative_directory = directory_path.relative_to(root)

        for name in dirnames:
            relative = relative_directory / name
            manifest[relative.as_posix()] = None
        for name in sorted(filenames):
            candidate = directory_path / name
            if _is_ignored(candidate):
                continue
            relative = relative_directory / name
            content = candidate.read_bytes()
            if candidate.suffix in TEXT_SUFFIXES:
                content = _normalize_text(content)
            manifest[relative.as_posix()] = content
    return manifest


def _validate_instruction_file(path: Path, expected_block: str) -> bool:
    """Return True when the managed block must be appended."""
    if _is_link(path):
        raise InstallError(f"Refusing instructions update through symlink: {path}")
    if not path.exists():
        return True
    if not path.is_file():
        raise InstallError(f"Instructions path is not a file: {path}")

    try:
        text = path.read_bytes().decode("utf-8")
    except UnicodeDecodeError as exc:
        raise InstallError(f"Instructions file is not valid UTF-8: {path}") from exc

    starts = text.count(START_MARKER)
    ends = text.count(END_MARKER)
    if starts != ends or starts > 1:
        raise InstallError(f"Unbalanced or duplicate managed markers in {path}")
    if starts == 0:
        return True

    start = text.index(START_MARKER)
    end_start = text.index(END_MARKER)
    if end_start < start:
        raise InstallError(f"Unbalanced managed markers in {path}")
    end = end_start + len(END_MARKER)
    if text[start:end].replace("\r\n", "\n") != expected_block:
        raise InstallError(f"Existing managed block differs in {path}; refusing overwrite")
    return False


def _append_managed_block(path: Path, block: str) -> None:
    existing = path.read_bytes() if path.exists() else b""
    newline = _newline_for(existing)
    encoded = block.encode("utf-8").replace(b"\n", newline)
    if not existing:
        separator = b""
    elif existing.endswith((b"\n", b"\r")):
        separator = newline
    else:
        separator = newline + newline
    path.parent.mkdir(parents=True, exist_ok=True)
    _write_atomic(path, existing + separator + encoded + newline)


def _copy_skill(source: Path, destination: Path) -> None:
    def ignore(_directory: str, names: list[str]) -> set[str]:
        return {name for name in names if name == "__pycache__" or name.endswith(".pyc")}

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination, ignore=ignore)


def _selected_hosts(platform: str) -> list[Host]:
    if platform == "both":
        return [HOSTS["codex"], HOSTS["claude"]]
    return [HOSTS[platform]]


def install(project_arg: Path, platform: str, dry_run: bool) -> list[str]:
    raw_source = Path(__file__).absolute().parents[1]
    _reject_symlink_chain(raw_source, "source")
    source = Path(__file__).resolve().parents[1]
    _reject_tree_symlinks(source, "source")
    source_manifest = _tree_manifest(source)

    project = _lexical_absolute(project_arg)
    _reject_symlink_chain(project, "project")
    if not project.exists() or not project.is_dir():
        raise InstallError(f"Project must be an existing directory: {project}")

    plans: list[tuple[Host, Path, Path, bool, bool]] = []
    actions: list[str] = []

    for host in _selected_hosts(platform):
        destination = project / host.skill_relative_path
        instructions = project / host.instructions_file
        _reject_symlink_chain(destination, f"{host.name} destination")
        _reject_tree_symlinks(destination, f"{host.name} destination")
        _reject_symlink_chain(instructions, f"{host.name} instructions")

        destination_exists = destination.exists()
        if destination_exists and source_manifest != _tree_manifest(destination):
            raise InstallError(
                f"Existing {host.name} skill differs from source: {destination}; "
                "refusing overwrite"
            )

        append_instructions = _validate_instruction_file(instructions, host.managed_block)
        plans.append(
            (host, destination, instructions, destination_exists, append_instructions)
        )
        actions.append(
            f"{host.name}: "
            + (f"keep identical skill at {destination}" if destination_exists else f"copy skill to {destination}")
        )
        actions.append(
            f"{host.name}: "
            + (
                f"append managed block to {instructions}"
                if append_instructions
                else f"keep identical managed block in {instructions}"
            )
        )

    if dry_run:
        return ["DRY RUN: no files written", *actions]

    for host, destination, instructions, destination_exists, append_instructions in plans:
        if not destination_exists:
            _copy_skill(source, destination)
        if append_instructions:
            _append_managed_block(instructions, host.managed_block)

    return actions


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install site-seo-release locally in a project for Codex, Claude, or both."
    )
    parser.add_argument("--project", required=True, type=Path, help="Existing project directory")
    parser.add_argument(
        "--platform",
        choices=("codex", "claude", "both"),
        default="both",
        help="Target host, default: both",
    )
    parser.add_argument("--dry-run", action="store_true", help="Validate and print without writing")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    try:
        actions = install(args.project, args.platform, args.dry_run)
    except (InstallError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    for action in actions:
        print(action)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
