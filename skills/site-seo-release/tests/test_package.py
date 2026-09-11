from __future__ import annotations

import importlib.util
from pathlib import Path
import shutil
import sys
import unittest

from test_install_skill import workspace_temporary_directory


SKILL_ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("skill_package_validator", SKILL_ROOT / "scripts/validate_skill.py")
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


class PackageTests(unittest.TestCase):
    def copy_skill(self, root: str) -> Path:
        destination = Path(root) / SKILL_ROOT.name
        shutil.copytree(SKILL_ROOT, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        return destination

    def test_current_package_has_no_broken_references(self):
        self.assertEqual(validator.validate(SKILL_ROOT), [])

    def test_removed_reference_is_detected(self):
        with workspace_temporary_directory() as root:
            skill = self.copy_skill(root)
            (skill / "references/report-contract.md").unlink()
            self.assertTrue(any("Broken reference" in error for error in validator.validate(skill)))

    def test_reference_cannot_escape_installed_package(self):
        with workspace_temporary_directory() as root:
            skill = self.copy_skill(root)
            entry = skill / "SKILL.md"
            entry.write_text(entry.read_text(encoding="utf-8") + "\n[external](../outside.md)\n", encoding="utf-8")
            self.assertTrue(any("escapes skill" in error for error in validator.validate(skill)))

    def test_explicit_only_metadata_is_rejected(self):
        with workspace_temporary_directory() as root:
            skill = self.copy_skill(root)
            metadata = skill / "agents/openai.yaml"
            metadata.write_text(metadata.read_text(encoding="utf-8").replace("allow_implicit_invocation: true", "allow_implicit_invocation: false"), encoding="utf-8")
            self.assertTrue(any("Implicit invocation" in error for error in validator.validate(skill)))


if __name__ == "__main__":
    unittest.main()
