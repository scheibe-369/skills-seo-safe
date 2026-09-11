#!/usr/bin/env python3
"""Register a short site-seo-release discovery block in a global instructions file.

The default mode is a read-only plan. Pass ``--apply`` to create an exclusive
backup beside the target and then update only the managed block.
"""

from __future__ import annotations

import argparse
import codecs
from dataclasses import dataclass
import os
from pathlib import Path
import re
import stat
import sys
import uuid


SKILL_NAME = "site-seo-release"
REGISTRY_VERSION = 1
START_MARKER = f"<!-- {SKILL_NAME}:global:start -->"
END_MARKER = f"<!-- {SKILL_NAME}:global:end -->"
START_BYTES = START_MARKER.encode("ascii")
END_BYTES = END_MARKER.encode("ascii")


class RegistrationError(RuntimeError):
    """Raised when registration cannot proceed without risking user data."""


@dataclass(frozen=True)
class RegistrationPlan:
    target: Path
    skill: Path
    status: str
    block: str
    original: bytes
    updated: bytes


def _absolute(path: Path) -> Path:
    return Path(os.path.abspath(os.fspath(path)))


def _is_link_or_junction(path: Path) -> bool:
    try:
        if path.is_symlink():
            return True
        isjunction = getattr(os.path, "isjunction", None)
        if isjunction is not None and isjunction(path):
            return True
        try:
            path_stat = path.lstat()
        except FileNotFoundError:
            return False
        if os.name == "nt":
            attributes = getattr(path_stat, "st_file_attributes", 0)
            reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
            return bool(attributes & reparse_flag)
    except OSError as exc:
        raise RegistrationError(f"Cannot inspect path component: {path}") from exc
    return False


def _reject_link_chain(path: Path, label: str) -> None:
    absolute = _absolute(path)
    for component in [*reversed(absolute.parents), absolute]:
        if _is_link_or_junction(component):
            raise RegistrationError(
                f"Refusing {label}: symlink or junction in path: {component}"
            )


def _validate_skill(path: Path) -> Path:
    skill = _absolute(path)
    _reject_link_chain(skill, "skill path")
    if not skill.exists():
        raise RegistrationError(f"Skill file does not exist: {skill}")
    if not skill.is_file():
        raise RegistrationError(f"Skill path is not a file: {skill}")
    if skill.name != "SKILL.md":
        raise RegistrationError(f"Skill source must be named SKILL.md: {skill}")
    if "\r" in str(skill) or "\n" in str(skill):
        raise RegistrationError("Skill path contains a line break")
    try:
        text = skill.read_bytes().decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise RegistrationError(f"Skill source is not valid UTF-8: {skill}") from exc
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise RegistrationError(f"Skill source lacks YAML frontmatter: {skill}")
    try:
        closing = next(
            index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"
        )
    except StopIteration as exc:
        raise RegistrationError(f"Skill source has unclosed YAML frontmatter: {skill}") from exc
    names = [
        match.group(1)
        for line in lines[1:closing]
        if (match := re.fullmatch(r"\s*name:\s*['\"]?([^'\"\s]+)['\"]?\s*", line))
    ]
    if names != [SKILL_NAME]:
        raise RegistrationError(
            f"Skill frontmatter must contain exactly name: {SKILL_NAME}: {skill}"
        )
    return skill


def _validate_target(path: Path) -> Path:
    target = _absolute(path)
    _reject_link_chain(target, "target path")
    if target.exists() and target.is_dir():
        raise RegistrationError(f"Target path is a directory: {target}")
    if target.exists() and not target.is_file():
        raise RegistrationError(f"Target path is not a regular file: {target}")
    return target


def render_block(skill: Path) -> str:
    return (
        f"{START_MARKER}\n"
        "## Registro Site SEO Release\n\n"
        f"Versão do registro: {REGISTRY_VERSION}\n"
        f"Caminho da skill: {skill}\n\n"
        "Ative ao criar, reformular, alterar de forma relevante ou finalizar sites "
        "públicos e landing pages. No início, crie ou atualize `SEO-SPEC.md`. No "
        "fechamento, atualize `tasks/site-release.md` e `tasks/site-release.json` "
        "com pendências e evidências.\n\n"
        "Leia a skill inteira somente na primeira ativação, em uma nova fase ou após "
        "mudança material. Reutilize o contexto já carregado, sem reler a cada "
        "mensagem, e carregue referências apenas sob demanda. Fora desse escopo, não "
        "carregue a skill.\n"
        f"{END_MARKER}"
    )


def _newline_for(data: bytes) -> bytes:
    if b"\r\n" in data:
        return b"\r\n"
    return b"\n"


def _encode_block(block: str, newline: bytes) -> bytes:
    encoded = block.encode("utf-8")
    if newline == b"\r\n":
        encoded = encoded.replace(b"\n", b"\r\n")
    return encoded


def _validate_markers(data: bytes, target: Path) -> tuple[int, int] | None:
    starts = data.count(START_BYTES)
    ends = data.count(END_BYTES)
    if starts == 0 and ends == 0:
        return None
    if starts != 1 or ends != 1:
        raise RegistrationError(
            f"Invalid or duplicate site-seo-release global markers in {target}"
        )
    start = data.index(START_BYTES)
    end_start = data.index(END_BYTES)
    if end_start < start:
        raise RegistrationError(
            f"Invalid site-seo-release global marker order in {target}"
        )
    return start, end_start + len(END_BYTES)


def _insert_block(data: bytes, block: bytes, newline: bytes) -> bytes:
    if not data:
        return block + newline
    separator = newline if data.endswith((b"\n", b"\r")) else newline + newline
    return data + separator + block + newline


def plan_registration(target_arg: Path, skill_arg: Path) -> RegistrationPlan:
    skill = _validate_skill(skill_arg)
    target = _validate_target(target_arg)
    try:
        original = target.read_bytes() if target.exists() else b""
    except OSError as exc:
        raise RegistrationError(f"Cannot read target: {target}") from exc

    newline = _newline_for(original)
    block = render_block(skill)
    encoded_block = _encode_block(block, newline)
    marker_range = _validate_markers(original, target)

    if marker_range is None:
        updated = _insert_block(original, encoded_block, newline)
        status = "create" if not target.exists() else "insert"
    else:
        start, end = marker_range
        updated = original[:start] + encoded_block + original[end:]
        status = "unchanged" if updated == original else "update"

    return RegistrationPlan(target, skill, status, block, original, updated)


def _ensure_apply_permissions(target: Path) -> None:
    parent = target.parent
    if not os.access(parent, os.W_OK):
        raise RegistrationError(f"No write permission for target directory: {parent}")
    if target.exists() and not os.access(target, os.W_OK):
        raise RegistrationError(f"No write permission for target file: {target}")


def _write_exclusive(path: Path, data: bytes, mode: int | None = None) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        if mode is not None:
            os.chmod(path, mode)
    except BaseException:
        try:
            path.unlink(missing_ok=True)
        finally:
            raise


def apply_registration(plan: RegistrationPlan) -> str:
    if plan.status == "unchanged":
        return "unchanged"

    try:
        plan.target.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise RegistrationError(
            f"Cannot create target directory: {plan.target.parent}"
        ) from exc

    _reject_link_chain(plan.target, "target path")
    _ensure_apply_permissions(plan.target)
    current = plan.target.read_bytes() if plan.target.exists() else b""
    if current != plan.original:
        raise RegistrationError("Target changed after planning; refusing update")

    mode = stat.S_IMODE(plan.target.stat().st_mode) if plan.target.exists() else None
    backup = plan.target.parent / f".site-seo-release.{uuid.uuid4()}.bak"
    temporary = plan.target.parent / f".site-seo-release.{uuid.uuid4()}.tmp"
    try:
        _write_exclusive(backup, plan.original, mode)
    except OSError as exc:
        raise RegistrationError(
            f"Cannot create exclusive backup beside target: {plan.target}"
        ) from exc

    try:
        _write_exclusive(temporary, plan.updated, mode)
        os.replace(temporary, plan.target)
    except OSError as exc:
        temporary.unlink(missing_ok=True)
        raise RegistrationError(f"Cannot update target: {plan.target}") from exc
    return plan.status


def _default_skill_path() -> Path:
    return Path(__file__).absolute().parents[1] / "SKILL.md"


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Register site-seo-release discovery in a global instructions file."
    )
    parser.add_argument("--target", required=True, type=Path, help="Global MD file to update")
    parser.add_argument(
        "--skill",
        type=Path,
        default=_default_skill_path(),
        help="Source SKILL.md path, default: this skill's SKILL.md",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Create an exclusive backup and apply the planned managed block",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    try:
        plan = plan_registration(args.target, args.skill)
        status = apply_registration(plan) if args.apply else plan.status
    except (RegistrationError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print(f"PATH: {plan.target}")
    print(f"STATUS: {status}")
    if not args.apply:
        print("BLOCK:")
        print(plan.block)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
