from __future__ import annotations

from copy import deepcopy
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "release_gate.py"
SPEC = importlib.util.spec_from_file_location("release_gate", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
release_gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(release_gate)


def valid_report() -> dict:
    return {
        "schema_version": 1,
        "project": "Example site",
        "environment": "preview",
        "audited_at": "2026-09-11T16:30:00-03:00",
        "scope": ["https://example.test/"],
        "checks": [
            {
                "id": check_id,
                "status": "pass",
                "severity": "medium",
                "required": True,
                "evidence": [f"Verified {check_id}"],
            }
            for check_id in release_gate.REQUIRED_CHECK_IDS
        ],
    }


class ReleaseGateSchemaTests(unittest.TestCase):
    def assert_schema_error(self, report: dict, text: str) -> None:
        with self.assertRaisesRegex(release_gate.SchemaError, text):
            release_gate.validate_report(report)

    def test_pass_requires_evidence(self) -> None:
        report = valid_report()
        report["checks"][0]["evidence"] = []
        self.assert_schema_error(report, "evidence must not be empty")

    def test_all_catalog_check_ids_are_required(self) -> None:
        report = valid_report()
        removed = report["checks"].pop()["id"]
        self.assert_schema_error(report, f"missing required check ids: {removed}")

    def test_duplicate_ids_are_rejected(self) -> None:
        report = valid_report()
        report["checks"].append(deepcopy(report["checks"][0]))
        self.assert_schema_error(report, "duplicate check id")

    def test_required_pending_check_is_not_ready(self) -> None:
        report = valid_report()
        check = report["checks"][0]
        check.update(
            status="pending",
            evidence=[],
            reason="Preview is not reachable yet",
            action="Deploy a preview and rerun the check",
        )
        result = release_gate.validate_report(report)
        self.assertEqual(result["decision"], "NOT_READY")
        self.assertEqual(result["counts"]["blocking"], 1)

    def test_na_requires_reason_and_can_be_required(self) -> None:
        report = valid_report()
        check = report["checks"][0]
        check.update(status="na", evidence=[])
        self.assert_schema_error(report, "reason is required for status na")

        check["reason"] = "Not applicable to this project scope"
        result = release_gate.validate_report(report)
        self.assertEqual(result["decision"], "READY")

    def test_unknown_enums_are_rejected(self) -> None:
        cases = (
            ("environment", "staging", "environment must be one of"),
            ("status", "done", "status must be one of"),
            ("severity", "urgent", "severity must be one of"),
        )
        for field, value, expected in cases:
            with self.subTest(field=field):
                report = valid_report()
                if field == "environment":
                    report[field] = value
                else:
                    report["checks"][0][field] = value
                self.assert_schema_error(report, expected)

    def test_non_string_enums_are_schema_errors(self) -> None:
        cases = (
            ("environment", ["preview"], "environment must be one of"),
            ("status", ["pass"], "status must be one of"),
            ("severity", {"high": True}, "severity must be one of"),
        )
        for field, value, expected in cases:
            with self.subTest(field=field):
                report = valid_report()
                if field == "environment":
                    report[field] = value
                else:
                    report["checks"][0][field] = value
                self.assert_schema_error(report, expected)

    def test_schema_version_requires_exact_integer(self) -> None:
        for value in (1.0, True, "1", None):
            with self.subTest(value=value):
                report = valid_report()
                report["schema_version"] = value
                self.assert_schema_error(report, "schema_version must be 1")

    def test_required_must_be_a_json_boolean(self) -> None:
        for value in (1, 0, "true", None):
            with self.subTest(value=value):
                report = valid_report()
                report["checks"][0]["required"] = value
                self.assert_schema_error(report, "required must be a boolean")

    def test_open_optional_medium_check_has_reservations(self) -> None:
        report = valid_report()
        check = report["checks"][0]
        check.update(
            status="fail",
            severity="medium",
            required=False,
            evidence=[],
            action="Improve the optional check",
        )
        result = release_gate.validate_report(report)
        self.assertEqual(result["decision"], "READY_WITH_RESERVATIONS")

    def test_open_optional_high_check_is_not_ready(self) -> None:
        report = valid_report()
        check = report["checks"][0]
        check.update(
            status="blocked",
            severity="high",
            required=False,
            evidence=[],
            reason="External dependency unavailable",
            action="Restore the dependency and verify",
        )
        result = release_gate.validate_report(report)
        self.assertEqual(result["decision"], "NOT_READY")

    def test_extra_unique_check_is_allowed(self) -> None:
        report = valid_report()
        report["checks"].append(
            {
                "id": "custom-accessibility",
                "status": "pass",
                "severity": "low",
                "required": False,
                "evidence": ["Keyboard navigation verified"],
            }
        )
        result = release_gate.validate_report(report)
        self.assertEqual(result["counts"]["total"], len(release_gate.REQUIRED_CHECK_IDS) + 1)


class ReleaseGateCliTests(unittest.TestCase):
    def write_report(self, report: dict) -> Path:
        temp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8")
        self.addCleanup(Path(temp.name).unlink, missing_ok=True)
        with temp:
            json.dump(report, temp)
        return Path(temp.name)

    def write_bytes(self, content: bytes) -> Path:
        temp = tempfile.NamedTemporaryFile(mode="wb", suffix=".json", delete=False)
        self.addCleanup(Path(temp.name).unlink, missing_ok=True)
        with temp:
            temp.write(content)
        return Path(temp.name)

    def test_schema_error_returns_exit_2(self) -> None:
        path = self.write_report({"schema_version": 1})
        stderr = io.StringIO()
        with patch("sys.stderr", stderr):
            code = release_gate.main([str(path)])
        self.assertEqual(code, 2)
        self.assertIn('"error": "schema_error"', stderr.getvalue())

    def test_invalid_utf8_returns_exit_2_without_traceback(self) -> None:
        path = self.write_bytes(b'{"project":"bad-utf8-\xff"}')
        stderr = io.StringIO()
        with patch("sys.stderr", stderr):
            code = release_gate.main([str(path)])
        self.assertEqual(code, 2)
        self.assertIn("report must be valid UTF-8", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())

    def test_duplicate_json_key_returns_exit_2(self) -> None:
        report = valid_report()
        serialized_checks = json.dumps(report["checks"])
        duplicate_key_json = (
            "{"
            '"schema_version":1,'
            '"project":"Example","project":"Hidden override",'
            '"environment":"preview",'
            '"audited_at":"2026-09-11T16:30:00-03:00",'
            '"scope":["https://example.test/"],'
            f'"checks":{serialized_checks}'
            "}"
        )
        path = self.write_bytes(duplicate_key_json.encode("utf-8"))
        stderr = io.StringIO()
        with patch("sys.stderr", stderr):
            code = release_gate.main([str(path)])
        self.assertEqual(code, 2)
        self.assertIn("duplicate JSON object key: project", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())

    def test_not_ready_returns_exit_1(self) -> None:
        report = valid_report()
        report["checks"][0].update(
            status="fail",
            evidence=[],
            action="Fix the required release check",
        )
        path = self.write_report(report)
        with patch("sys.stdout", io.StringIO()):
            code = release_gate.main([str(path)])
        self.assertEqual(code, 1)

    def test_ready_markdown_returns_exit_0(self) -> None:
        path = self.write_report(valid_report())
        stdout = io.StringIO()
        with patch("sys.stdout", stdout):
            code = release_gate.main([str(path), "--markdown"])
        self.assertEqual(code, 0)
        self.assertIn("# Release gate: READY", stdout.getvalue())
        self.assertIn("Audited at: 2026-09-11T16:30:00-03:00", stdout.getvalue())
        self.assertIn("Scope: https://example.test/", stdout.getvalue())
        self.assertIn("does not certify publication", stdout.getvalue())

    def test_markdown_escapes_extra_check_id_and_action(self) -> None:
        report = valid_report()
        report["checks"].append(
            {
                "id": "custom|check\nsecond-line",
                "status": "fail",
                "severity": "low",
                "required": False,
                "evidence": [],
                "action": "Fix|this\nnow",
            }
        )
        result = release_gate.validate_report(report)
        markdown = release_gate.render_markdown(result)
        self.assertIn("custom\\|check second-line", markdown)
        self.assertIn("Fix\\|this now", markdown)


if __name__ == "__main__":
    unittest.main()
