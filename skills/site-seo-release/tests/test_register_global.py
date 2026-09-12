from __future__ import annotations

import codecs
import importlib.util
import io
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
SCRIPT_PATH = REPOSITORY_ROOT / "skills/site-seo-release/scripts/register_global.py"
SPEC = importlib.util.spec_from_file_location("register_global", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
register_global = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = register_global
SPEC.loader.exec_module(register_global)


TEST_WORK_ROOT = REPOSITORY_ROOT / ".test-work"


def workspace_temporary_directory() -> tempfile.TemporaryDirectory[str]:
    TEST_WORK_ROOT.mkdir(exist_ok=True)
    mkdir = os.mkdir
    with mock.patch.object(
        tempfile._os,
        "mkdir",
        side_effect=lambda path, _mode=0o777: mkdir(path),
    ):
        return tempfile.TemporaryDirectory(dir=TEST_WORK_ROOT)


class RegisterGlobalTests(unittest.TestCase):
    def make_skill(self, root: Path) -> Path:
        skill = root / "skill" / "SKILL.md"
        skill.parent.mkdir()
        skill.write_text("---\nname: site-seo-release\n---\n", encoding="utf-8")
        return skill

    def run_main(self, arguments: list[str]) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with mock.patch("sys.stdout", stdout), mock.patch("sys.stderr", stderr):
            code = register_global.main(arguments)
        return code, stdout.getvalue(), stderr.getvalue()

    def test_dry_run_prints_only_path_status_and_new_block_and_writes_nothing(self) -> None:
        with workspace_temporary_directory() as temporary:
            root = Path(temporary)
            skill = self.make_skill(root)
            target = root / "config" / "AGENTS.md"
            secret = "EXISTING-GLOBAL-CONTENT-MUST-NOT-PRINT"
            target.parent.mkdir()
            target.write_text(secret, encoding="utf-8")
            before = target.read_bytes()

            code, stdout, stderr = self.run_main(
                ["--target", str(target), "--skill", str(skill)]
            )

            self.assertEqual(code, 0, stderr)
            self.assertEqual(target.read_bytes(), before)
            self.assertIn(f"PATH: {target.resolve()}", stdout)
            self.assertIn("STATUS: insert", stdout)
            self.assertIn(register_global.START_MARKER, stdout)
            self.assertIn(str(skill.resolve()), stdout)
            self.assertNotIn(secret, stdout)
            self.assertEqual(list(target.parent.glob(".site-seo-release.*")), [])

    def test_apply_supports_missing_parent_after_plan(self) -> None:
        with workspace_temporary_directory() as temporary:
            root = Path(temporary)
            skill = self.make_skill(root)
            target = root / "missing" / "nested" / "GEMINI.md"
            plan = register_global.plan_registration(target, skill)
            self.assertEqual(plan.status, "create")
            self.assertFalse(target.parent.exists())

            result = register_global.apply_registration(plan)

            self.assertEqual(result.status, "create")
            self.assertIsNone(result.backup)
            self.assertTrue(target.is_file())
            self.assertEqual(list(target.parent.glob(".site-seo-release.*.bak")), [])

    def test_second_apply_is_idempotent_and_creates_no_second_backup(self) -> None:
        with workspace_temporary_directory() as temporary:
            root = Path(temporary)
            skill = self.make_skill(root)
            target = root / "CLAUDE.md"

            first = register_global.plan_registration(target, skill)
            register_global.apply_registration(first)
            first_bytes = target.read_bytes()
            backup_count = len(list(root.glob(".site-seo-release.*.bak")))

            second = register_global.plan_registration(target, skill)
            result = register_global.apply_registration(second)

            self.assertEqual(second.status, "unchanged")
            self.assertEqual(result.status, "unchanged")
            self.assertIsNone(result.backup)
            self.assertEqual(target.read_bytes(), first_bytes)
            self.assertEqual(target.read_bytes().count(register_global.START_BYTES), 1)
            self.assertEqual(
                len(list(root.glob(".site-seo-release.*.bak"))), backup_count
            )

    def test_update_preserves_bom_crlf_and_every_byte_outside_block(self) -> None:
        with workspace_temporary_directory() as temporary:
            root = Path(temporary)
            skill = self.make_skill(root)
            target = root / "AGENTS.md"
            prefix = codecs.BOM_UTF8 + "Cabeçalho\r\n\r\n".encode("utf-8")
            stale = (
                register_global.START_MARKER
                + "\r\nold registry\r\n"
                + register_global.END_MARKER
            ).encode("utf-8")
            suffix = "\r\n\r\nConteúdo final\r\n".encode("utf-8")
            original = prefix + stale + suffix
            target.write_bytes(original)

            plan = register_global.plan_registration(target, skill)
            self.assertEqual(plan.status, "update")
            register_global.apply_registration(plan)
            updated = target.read_bytes()

            self.assertTrue(updated.startswith(prefix))
            self.assertTrue(updated.endswith(suffix))
            self.assertTrue(updated.startswith(codecs.BOM_UTF8))
            managed = updated[len(prefix) : len(updated) - len(suffix)]
            self.assertNotIn(b"\n", managed.replace(b"\r\n", b""))
            backups = list(root.glob(".site-seo-release.*.bak"))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_bytes(), original)

    def test_invalid_and_duplicate_markers_are_rejected_without_writes(self) -> None:
        cases = {
            "start only": register_global.START_MARKER,
            "end only": register_global.END_MARKER,
            "duplicate": (
                f"{register_global.START_MARKER}\n{register_global.END_MARKER}\n"
                f"{register_global.START_MARKER}\n{register_global.END_MARKER}"
            ),
            "reversed": (
                f"{register_global.END_MARKER}\n{register_global.START_MARKER}"
            ),
        }
        for name, content in cases.items():
            with self.subTest(name=name), workspace_temporary_directory() as temporary:
                root = Path(temporary)
                skill = self.make_skill(root)
                target = root / "AGENTS.md"
                target.write_text(content, encoding="utf-8")
                before = target.read_bytes()

                code, _stdout, stderr = self.run_main(
                    ["--target", str(target), "--skill", str(skill), "--apply"]
                )

                self.assertEqual(code, 2)
                self.assertIn("marker", stderr.lower())
                self.assertEqual(target.read_bytes(), before)
                self.assertEqual(list(root.glob(".site-seo-release.*")), [])

    def test_target_directory_is_rejected(self) -> None:
        with workspace_temporary_directory() as temporary:
            root = Path(temporary)
            skill = self.make_skill(root)
            target = root / "directory-target"
            target.mkdir()

            code, _stdout, stderr = self.run_main(
                ["--target", str(target), "--skill", str(skill)]
            )

            self.assertEqual(code, 2)
            self.assertIn("directory", stderr.lower())

    def test_symlink_ancestor_is_rejected_when_supported(self) -> None:
        with workspace_temporary_directory() as temporary:
            root = Path(temporary)
            skill = self.make_skill(root)
            real = root / "real"
            real.mkdir()
            linked = root / "linked"
            try:
                linked.symlink_to(real, target_is_directory=True)
            except (NotImplementedError, OSError) as exc:
                self.skipTest(f"Directory symlinks unavailable: {exc}")

            code, _stdout, stderr = self.run_main(
                ["--target", str(linked / "AGENTS.md"), "--skill", str(skill)]
            )

            self.assertEqual(code, 2)
            self.assertIn("symlink or junction", stderr.lower())
            self.assertEqual(list(real.iterdir()), [])

    def test_dangling_target_symlink_is_rejected(self) -> None:
        with workspace_temporary_directory() as temporary:
            root = Path(temporary)
            skill = self.make_skill(root)
            target = root / "AGENTS.md"
            try:
                target.symlink_to(root / "missing-global.md")
            except (NotImplementedError, OSError) as exc:
                self.skipTest(f"File symlinks unavailable: {exc}")
            self.assertTrue(target.is_symlink())
            self.assertFalse(target.exists())

            code, _stdout, stderr = self.run_main(
                ["--target", str(target), "--skill", str(skill), "--apply"]
            )

            self.assertEqual(code, 2)
            self.assertIn("symlink or junction", stderr.lower())
            self.assertTrue(target.is_symlink())
            self.assertFalse((root / "missing-global.md").exists())
            self.assertEqual(list(root.glob(".site-seo-release.*")), [])

    def test_skill_source_requires_expected_file_and_frontmatter(self) -> None:
        cases = (
            ("OTHER.md", b"---\nname: site-seo-release\n---\n", "named SKILL.md"),
            ("SKILL.md", b"---\nname: unrelated\n---\n", "frontmatter"),
            ("SKILL.md", b"not frontmatter\n", "frontmatter"),
            ("SKILL.md", b"---\nname: site-seo-release\n---\n\xff", "UTF-8"),
        )
        for file_name, content, expected in cases:
            with self.subTest(file_name=file_name, expected=expected), workspace_temporary_directory() as temporary:
                root = Path(temporary)
                skill = root / "skill" / file_name
                skill.parent.mkdir()
                skill.write_bytes(content)
                target = root / "AGENTS.md"

                code, _stdout, stderr = self.run_main(
                    ["--target", str(target), "--skill", str(skill), "--apply"]
                )

                self.assertEqual(code, 2)
                self.assertIn(expected.lower(), stderr.lower())
                self.assertFalse(target.exists())
                self.assertEqual(list(root.glob(".site-seo-release.*")), [])

    def test_non_utf8_target_is_rejected_without_writes(self) -> None:
        with workspace_temporary_directory() as temporary:
            root = Path(temporary)
            skill = self.make_skill(root)
            target = root / "AGENTS.md"
            original = "Conteúdo global".encode("utf-16")
            target.write_bytes(original)

            code, _stdout, stderr = self.run_main(
                ["--target", str(target), "--skill", str(skill), "--apply"]
            )

            self.assertEqual(code, 2)
            self.assertIn("utf-8", stderr.lower())
            self.assertEqual(target.read_bytes(), original)
            self.assertEqual(list(root.glob(".site-seo-release.*")), [])

    def test_apply_prints_backup_path_on_insert(self) -> None:
        with workspace_temporary_directory() as temporary:
            root = Path(temporary)
            skill = self.make_skill(root)
            target = root / "AGENTS.md"
            target.write_bytes(b"existing\n")

            code, stdout, stderr = self.run_main(
                ["--target", str(target), "--skill", str(skill), "--apply"]
            )

            self.assertEqual(code, 0, stderr)
            backups = list(root.glob(".site-seo-release.*.bak"))
            self.assertEqual(len(backups), 1)
            self.assertIn(f"BACKUP: {backups[0].resolve()}", stdout)
            self.assertEqual(backups[0].read_bytes(), b"existing\n")

    def test_apply_reports_missing_permissions_before_backup(self) -> None:
        with workspace_temporary_directory() as temporary:
            root = Path(temporary)
            skill = self.make_skill(root)
            target = root / "AGENTS.md"
            target.write_text("existing", encoding="utf-8")
            plan = register_global.plan_registration(target, skill)

            with mock.patch.object(register_global.os, "access", return_value=False):
                with self.assertRaisesRegex(register_global.RegistrationError, "permission"):
                    register_global.apply_registration(plan)

            self.assertEqual(target.read_text(encoding="utf-8"), "existing")
            self.assertEqual(list(root.glob(".site-seo-release.*")), [])

    def test_default_skill_path_is_the_feature_skill(self) -> None:
        expected = REPOSITORY_ROOT / "skills/site-seo-release/SKILL.md"
        self.assertEqual(register_global._default_skill_path().resolve(), expected.resolve())


if __name__ == "__main__":
    unittest.main()
