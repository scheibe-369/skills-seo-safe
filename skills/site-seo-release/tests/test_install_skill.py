from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
INSTALLER = REPOSITORY_ROOT / "skills/site-seo-release/scripts/install_skill.py"
TEST_WORK_ROOT = REPOSITORY_ROOT / ".test-work"
START_MARKER = "<!-- site-seo-release:start -->"
END_MARKER = "<!-- site-seo-release:end -->"


def workspace_temporary_directory() -> tempfile.TemporaryDirectory[str]:
    TEST_WORK_ROOT.mkdir(exist_ok=True)
    # Python 3.12 creates temporary directories with mode 0o700. In this
    # Windows sandbox that mode is translated into an ACL which denies the
    # test process itself, so create the same TemporaryDirectory with the
    # platform default directory ACL.
    mkdir = os.mkdir
    with mock.patch.object(tempfile._os, "mkdir", side_effect=lambda path, _mode=0o777: mkdir(path)):
        return tempfile.TemporaryDirectory(dir=TEST_WORK_ROOT)


def load_installer_module():
    spec = importlib.util.spec_from_file_location("site_seo_release_installer", INSTALLER)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load installer module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class InstallSkillTests(unittest.TestCase):
    def run_installer(
        self, project: Path, platform: str = "both", dry_run: bool = False, installer: Path = INSTALLER
    ) -> subprocess.CompletedProcess[str]:
        command = [sys.executable, str(installer), "--project", str(project), "--platform", platform]
        if dry_run:
            command.append("--dry-run")
        return subprocess.run(command, capture_output=True, text=True, check=False)

    def assert_clean_copy(self, destination: Path) -> None:
        self.assertTrue((destination / "scripts/install_skill.py").is_file())
        self.assertFalse(any(path.name == "__pycache__" for path in destination.rglob("*")))
        self.assertFalse(any(path.suffix == ".pyc" for path in destination.rglob("*")))

    def test_platform_selection(self) -> None:
        cases = {
            "codex": (True, False),
            "claude": (False, True),
            "both": (True, True),
        }
        for platform, (has_codex, has_claude) in cases.items():
            with self.subTest(platform=platform), workspace_temporary_directory() as temporary:
                project = Path(temporary)
                result = self.run_installer(project, platform)
                self.assertEqual(result.returncode, 0, result.stderr)

                codex_destination = project / ".agents/skills/site-seo-release"
                claude_destination = project / ".claude/skills/site-seo-release"
                self.assertEqual(codex_destination.exists(), has_codex)
                self.assertEqual(claude_destination.exists(), has_claude)
                self.assertEqual((project / "AGENTS.md").exists(), has_codex)
                self.assertEqual((project / "CLAUDE.md").exists(), has_claude)
                if has_codex:
                    self.assert_clean_copy(codex_destination)
                    self.assertIn(
                        ".agents/skills/site-seo-release/SKILL.md",
                        (project / "AGENTS.md").read_text(encoding="utf-8"),
                    )
                    agents_text = (project / "AGENTS.md").read_text(encoding="utf-8")
                    self.assertIn("tasks/site-release.json", agents_text)
                    self.assertIn("Reutilize a skill já carregada", agents_text)
                if has_claude:
                    self.assert_clean_copy(claude_destination)
                    self.assertIn(
                        ".claude/skills/site-seo-release/SKILL.md",
                        (project / "CLAUDE.md").read_text(encoding="utf-8"),
                    )

    def test_detects_windows_reparse_point_without_path_is_junction(self) -> None:
        module = load_installer_module()

        class ReparsePath:
            def is_symlink(self) -> bool:
                return False

            def lstat(self) -> SimpleNamespace:
                return SimpleNamespace(st_file_attributes=0x400)

        with mock.patch.object(module.os, "name", "nt"):
            with mock.patch.object(module.os.path, "isjunction", return_value=False, create=True):
                self.assertTrue(module._is_link(ReparsePath()))

    def test_second_install_is_idempotent(self) -> None:
        with workspace_temporary_directory() as temporary:
            project = Path(temporary)
            first = self.run_installer(project)
            self.assertEqual(first.returncode, 0, first.stderr)
            agents_before = (project / "AGENTS.md").read_bytes()
            claude_before = (project / "CLAUDE.md").read_bytes()

            second = self.run_installer(project)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual((project / "AGENTS.md").read_bytes(), agents_before)
            self.assertEqual((project / "CLAUDE.md").read_bytes(), claude_before)
            self.assertEqual(agents_before.count(START_MARKER.encode()), 1)
            self.assertEqual(agents_before.count(END_MARKER.encode()), 1)

    def test_missing_destination_is_not_a_link(self) -> None:
        module = load_installer_module()
        with workspace_temporary_directory() as temporary:
            self.assertFalse(module._is_link(Path(temporary) / "not-created-yet"))

    def test_preserves_existing_instruction_text(self) -> None:
        with workspace_temporary_directory() as temporary:
            project = Path(temporary)
            original = b"# Existing rules\r\n\r\nKeep this byte-for-byte.\r\n"
            (project / "AGENTS.md").write_bytes(original)

            result = self.run_installer(project, "codex")
            self.assertEqual(result.returncode, 0, result.stderr)
            updated = (project / "AGENTS.md").read_bytes()
            self.assertTrue(updated.startswith(original))
            self.assertEqual(updated.count(START_MARKER.encode()), 1)
            self.assertEqual(updated.count(END_MARKER.encode()), 1)

    def test_conflicting_destination_causes_zero_mutation(self) -> None:
        with workspace_temporary_directory() as temporary:
            project = Path(temporary)
            conflict = project / ".agents/skills/site-seo-release"
            conflict.mkdir(parents=True)
            (conflict / "foreign.txt").write_text("user content", encoding="utf-8")
            (project / "AGENTS.md").write_text("existing\n", encoding="utf-8")
            before = {
                path.relative_to(project).as_posix(): path.read_bytes()
                for path in project.rglob("*")
                if path.is_file()
            }

            result = self.run_installer(project, "both")
            self.assertNotEqual(result.returncode, 0)
            after = {
                path.relative_to(project).as_posix(): path.read_bytes()
                for path in project.rglob("*")
                if path.is_file()
            }
            self.assertEqual(after, before)
            self.assertFalse((project / ".claude").exists())

    def test_different_managed_block_causes_zero_mutation(self) -> None:
        with workspace_temporary_directory() as temporary:
            project = Path(temporary)
            content = f"before\n{START_MARKER}\nchanged by user\n{END_MARKER}\nafter\n"
            (project / "AGENTS.md").write_text(content, encoding="utf-8")

            result = self.run_installer(project, "codex")
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual((project / "AGENTS.md").read_text(encoding="utf-8"), content)
            self.assertFalse((project / ".agents").exists())

    def test_dry_run_writes_nothing(self) -> None:
        with workspace_temporary_directory() as temporary:
            project = Path(temporary)
            result = self.run_installer(project, dry_run=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("DRY RUN", result.stdout)
            self.assertEqual(list(project.iterdir()), [])

    def test_rejects_project_ancestor_symlink_when_supported(self) -> None:
        with workspace_temporary_directory() as temporary:
            root = Path(temporary)
            real_project = root / "real-project"
            real_project.mkdir()
            linked_project = root / "linked-project"
            try:
                linked_project.symlink_to(real_project, target_is_directory=True)
            except (NotImplementedError, OSError) as exc:
                self.skipTest(f"Directory symlinks unavailable: {exc}")

            result = self.run_installer(linked_project, "codex")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("symlink", result.stderr.lower())
            self.assertEqual(list(real_project.iterdir()), [])

    def test_rejects_symlink_inside_source_when_supported(self) -> None:
        with workspace_temporary_directory() as temporary:
            root = Path(temporary)
            fixture = root / "site-seo-release"
            fixture_installer = fixture / "scripts/install_skill.py"
            fixture_installer.parent.mkdir(parents=True)
            shutil.copy2(INSTALLER, fixture_installer)
            target = root / "outside.txt"
            target.write_text("outside", encoding="utf-8")
            try:
                (fixture / "escape.txt").symlink_to(target)
            except (NotImplementedError, OSError) as exc:
                self.skipTest(f"File symlinks unavailable: {exc}")
            project = root / "project"
            project.mkdir()

            result = self.run_installer(project, "codex", installer=fixture_installer)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("symlink", result.stderr.lower())
            self.assertEqual(list(project.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
