#!/usr/bin/env python3
"""Validate an offline site SEO release report and derive its gate decision.

The decision reflects only the scope and environment declared by the report.
It does not certify that evidence is true or that the project was published.
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime
import json
from pathlib import Path
import sys
from typing import Any


SCHEMA_VERSION = 1
ENVIRONMENTS = {"local", "preview", "production"}
STATUSES = {"pass", "fail", "pending", "blocked", "na"}
SEVERITIES = {"critical", "high", "medium", "low"}
OPEN_STATUSES = {"fail", "pending", "blocked"}
REASON_STATUSES = {"pending", "blocked", "na"}
ACTION_STATUSES = OPEN_STATUSES

REQUIRED_CHECK_IDS = (
    "context",
    "page-intent",
    "titles",
    "descriptions",
    "headings-content",
    "canonical-indexing",
    "robots",
    "sitemap",
    "llms",
    "social",
    "favicon",
    "images",
    "performance",
    "navigation-mobile",
    "forms-ui",
    "forms-delivery",
    "privacy",
    "cookies",
    "not-found",
    "email-spf",
    "email-dkim",
    "email-dmarc",
    "security",
    "credit",
    "build",
    "production-verification",
)


class SchemaError(ValueError):
    """Raised when a report does not satisfy the release report contract."""


def _is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_audited_at(value: Any) -> None:
    if not _is_nonempty_string(value):
        raise SchemaError("audited_at must be a non-empty ISO 8601 string")

    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise SchemaError("audited_at must be a valid ISO 8601 datetime") from exc

    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise SchemaError("audited_at must include a timezone")


def _validate_string_list(value: Any, field: str, *, nonempty: bool = False) -> None:
    if not isinstance(value, list):
        raise SchemaError(f"{field} must be a list")
    if nonempty and not value:
        raise SchemaError(f"{field} must not be empty")
    if any(not _is_nonempty_string(item) for item in value):
        raise SchemaError(f"{field} must contain only non-empty strings")


def validate_report(report: Any) -> dict[str, Any]:
    """Validate *report* and return a normalized gate result.

    Evidence is checked only for shape and presence. Its factual accuracy is not
    evaluated by this offline validator.
    """

    if not isinstance(report, dict):
        raise SchemaError("report must be a JSON object")

    version = report.get("schema_version")
    if type(version) is not int or version != SCHEMA_VERSION:
        raise SchemaError(f"schema_version must be {SCHEMA_VERSION}")

    if not _is_nonempty_string(report.get("project")):
        raise SchemaError("project must be a non-empty string")

    environment = report.get("environment")
    if not isinstance(environment, str) or environment not in ENVIRONMENTS:
        allowed = ", ".join(sorted(ENVIRONMENTS))
        raise SchemaError(f"environment must be one of: {allowed}")

    _validate_audited_at(report.get("audited_at"))
    _validate_string_list(report.get("scope"), "scope", nonempty=True)

    checks = report.get("checks")
    if not isinstance(checks, list):
        raise SchemaError("checks must be a list")

    seen_ids: set[str] = set()
    normalized_checks: list[dict[str, Any]] = []

    for index, check in enumerate(checks):
        prefix = f"checks[{index}]"
        if not isinstance(check, dict):
            raise SchemaError(f"{prefix} must be an object")

        check_id = check.get("id")
        if not _is_nonempty_string(check_id):
            raise SchemaError(f"{prefix}.id must be a non-empty string")
        if check_id in seen_ids:
            raise SchemaError(f"duplicate check id: {check_id}")
        seen_ids.add(check_id)

        status = check.get("status")
        if not isinstance(status, str) or status not in STATUSES:
            allowed = ", ".join(sorted(STATUSES))
            raise SchemaError(f"{prefix}.status must be one of: {allowed}")

        severity = check.get("severity")
        if not isinstance(severity, str) or severity not in SEVERITIES:
            allowed = ", ".join(sorted(SEVERITIES))
            raise SchemaError(f"{prefix}.severity must be one of: {allowed}")

        required = check.get("required")
        if type(required) is not bool:
            raise SchemaError(f"{prefix}.required must be a boolean")

        evidence = check.get("evidence")
        _validate_string_list(
            evidence,
            f"{prefix}.evidence",
            nonempty=status == "pass",
        )

        if status in REASON_STATUSES and not _is_nonempty_string(check.get("reason")):
            raise SchemaError(f"{prefix}.reason is required for status {status}")

        if status in ACTION_STATUSES and not _is_nonempty_string(check.get("action")):
            raise SchemaError(f"{prefix}.action is required for status {status}")

        normalized_checks.append(check)

    missing = [check_id for check_id in REQUIRED_CHECK_IDS if check_id not in seen_ids]
    if missing:
        raise SchemaError("missing required check ids: " + ", ".join(missing))

    open_checks = [check for check in normalized_checks if check["status"] in OPEN_STATUSES]
    blocking_checks = [
        check
        for check in open_checks
        if check["required"] or check["severity"] in {"critical", "high"}
    ]

    if blocking_checks:
        decision = "NOT_READY"
    elif open_checks:
        decision = "READY_WITH_RESERVATIONS"
    else:
        decision = "READY"

    status_counts = Counter(check["status"] for check in normalized_checks)
    severity_counts = Counter(check["severity"] for check in open_checks)
    return {
        "schema_version": SCHEMA_VERSION,
        "project": report["project"],
        "environment": environment,
        "audited_at": report["audited_at"],
        "scope": report["scope"],
        "decision": decision,
        "counts": {
            "total": len(normalized_checks),
            "open": len(open_checks),
            "blocking": len(blocking_checks),
            "by_status": {status: status_counts.get(status, 0) for status in sorted(STATUSES)},
            "open_by_severity": {
                severity: severity_counts.get(severity, 0)
                for severity in ("critical", "high", "medium", "low")
            },
        },
        "open_checks": [
            {
                "id": check["id"],
                "status": check["status"],
                "severity": check["severity"],
                "required": check["required"],
                "action": check["action"],
            }
            for check in open_checks
        ],
        "notice": (
            "This decision evaluates only the declared report scope and environment. "
            "It does not certify publication or the truth of supplied evidence."
        ),
    }


def render_markdown(result: dict[str, Any]) -> str:
    """Render a validated gate result as concise Markdown."""

    counts = result["counts"]
    lines = [
        f"# Release gate: {result['decision']}",
        "",
        f"Project: {result['project']}",
        f"Environment: {result['environment']}",
        f"Audited at: {result['audited_at']}",
        "Scope: " + ", ".join(result["scope"]),
        f"Checks: {counts['total']} total, {counts['open']} open, {counts['blocking']} blocking",
        "",
        result["notice"],
    ]

    if result["open_checks"]:
        lines.extend(
            [
                "",
                "## Open checks",
                "",
                "| Check | Status | Severity | Required | Action |",
                "|---|---|---|---|---|",
            ]
        )
        for check in result["open_checks"]:
            check_id = _markdown_cell(check["id"])
            action = _markdown_cell(check["action"])
            lines.append(
                f"| {check_id} | {check['status']} | {check['severity']} | "
                f"{'yes' if check['required'] else 'no'} | {action} |"
            )
    else:
        lines.extend(["", "No open checks were declared."])

    return "\n".join(lines)


def _markdown_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise SchemaError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def _load_report(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle, object_pairs_hook=_reject_duplicate_keys)
    except OSError as exc:
        raise SchemaError(f"cannot read report: {exc}") from exc
    except UnicodeDecodeError as exc:
        raise SchemaError("report must be valid UTF-8") from exc
    except json.JSONDecodeError as exc:
        raise SchemaError(f"invalid JSON: {exc.msg}") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate an offline SEO release report and derive its decision."
    )
    parser.add_argument("path", type=Path, help="Path to the JSON release report")
    parser.add_argument(
        "--markdown",
        action="store_true",
        help="Print the decision as Markdown instead of JSON",
    )
    args = parser.parse_args(argv)

    try:
        result = validate_report(_load_report(args.path))
    except SchemaError as exc:
        print(json.dumps({"error": "schema_error", "message": str(exc)}), file=sys.stderr)
        return 2

    if args.markdown:
        print(render_markdown(result))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))

    return 1 if result["decision"] == "NOT_READY" else 0


if __name__ == "__main__":
    raise SystemExit(main())
