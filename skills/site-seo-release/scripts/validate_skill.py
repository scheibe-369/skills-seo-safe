"""Validate this package's portable metadata and local reference graph offline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


def validate(skill: Path) -> list[str]:
    errors: list[str] = []
    entry = skill / "SKILL.md"
    try:
        content = entry.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"Cannot read SKILL.md: {exc}"]
    match = re.match(r"\A---\n(.*?)\n---\n", content, re.S)
    if not match:
        return ["Expected UTF-8 frontmatter with opening/closing delimiters"]
    fields = {}
    for line in match[1].splitlines():
        key, separator, value = line.partition(":")
        if not separator or key in fields:
            errors.append("Malformed or duplicate frontmatter field")
        fields[key] = value.strip()
    if set(fields) != {"name", "description"}:
        errors.append("Portable core must contain only name and description")
    name = fields.get("name", "")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        errors.append("Invalid portable skill name")
    if name != skill.name:
        errors.append("Skill name must match directory name")
    try:
        description = json.loads(fields.get("description", ""))
        if not isinstance(description, str) or not 1 <= len(description) <= 1024:
            errors.append("Description must be a non-empty string up to 1024 characters")
    except (ValueError, TypeError):
        errors.append("Use a JSON-compatible quoted YAML string for description")

    required = (
        "LICENSE", "agents/openai.yaml", "assets/seo-spec.md",
        "scripts/release_gate.py", "scripts/install_skill.py", "scripts/register_global.py",
    )
    for relative in required:
        if not (skill / relative).is_file():
            errors.append(f"Missing package resource: {relative}")

    metadata_file = skill / "agents/openai.yaml"
    if metadata_file.is_file():
        metadata = metadata_file.read_text(encoding="utf-8")
        parsed = {}
        for line in metadata.splitlines():
            if line.startswith("  "):
                key, _, value = line.strip().partition(":")
                parsed[key] = value.strip()
        for field in ("display_name", "short_description", "default_prompt"):
            try:
                parsed[field] = json.loads(parsed.get(field, ""))
            except ValueError:
                errors.append(f"Invalid quoted interface field: {field}")
                parsed[field] = ""
        short = parsed.get("short_description", "")
        if not isinstance(short, str) or not 25 <= len(short) <= 64:
            errors.append("short_description must have 25 to 64 characters")
        prompt = parsed.get("default_prompt", "")
        if not isinstance(prompt, str) or f"${name}" not in prompt:
            errors.append("default_prompt must name the skill explicitly")
        if parsed.get("allow_implicit_invocation") != "true":
            errors.append("Implicit invocation must remain enabled")

    for path in skill.rglob("*"):
        if path.suffix not in {".md", ".yaml", ".py", ".json"} or "__pycache__" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            errors.append(f"Resource is not readable UTF-8: {path.relative_to(skill)}")
            continue
        if any(char in text for char in ("\u2013", "\u2014")):
            errors.append(f"Long dash in active copy: {path.relative_to(skill)}")
        if path.suffix != ".md":
            continue
        for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            target = link.strip("<>")
            if urlsplit(target).scheme or target.startswith("#"):
                continue
            relative = unquote(target.split("#", 1)[0])
            resolved = (path.parent / relative).resolve()
            if not resolved.is_relative_to(skill.resolve()):
                errors.append(f"Package reference escapes skill: {path.name}: {target}")
            elif not resolved.exists():
                errors.append(f"Broken reference: {path.name}: {target}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    try:
        errors = validate(args.path)
    except (OSError, UnicodeError) as exc:
        errors = [f"Cannot inspect package: {exc}"]
    print(json.dumps({"valid": not errors, "errors": errors}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
