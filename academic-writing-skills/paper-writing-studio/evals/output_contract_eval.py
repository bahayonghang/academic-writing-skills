"""Run recorded output-contract fixtures against the pure routing core.

This is a local contract check. It does not call a language model or prove
provider-backed quality, real-paper fidelity, installation, or human review.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from core import canonical_section, render_result, select_profile  # noqa: E402


def _assert_equal(actual: Any, expected: Any, label: str) -> None:
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, got {actual!r}")


def _selection_kwargs(data: dict[str, Any]) -> dict[str, str | None]:
    return {key: data.get(key) for key in ("venue", "journal", "domain")}


def _run_selection(case: dict[str, Any]) -> None:
    source = case.get("input", {})
    selection = select_profile(**_selection_kwargs(source))
    expected = case["expected"]
    _assert_equal(selection.venue, expected["venue"], "venue")
    if "selection_source" in expected:
        _assert_equal(selection.source, expected["selection_source"], "selection_source")
    if "conflict_count" in expected:
        _assert_equal(len(selection.conflicts), expected["conflict_count"], "conflict_count")
    if "missing_evidence" in expected:
        _assert_equal(
            list(selection.missing_evidence), expected["missing_evidence"], "missing_evidence"
        )
    if "section" in expected:
        _assert_equal(canonical_section(source["target"]).canonical, expected["section"], "section")


def _run_render(case: dict[str, Any]) -> None:
    source = case.get("input", {})
    selection = select_profile(**_selection_kwargs(source))
    render = case.get("render", {})
    result = render_result(
        render.get("text", source.get("input_text", "")),
        input_text=source.get("input_text", ""),
        selection=selection,
        target=source["target"],
        profile_version="fixture",
        ai_tells_avoided=render.get("ai_tells_avoided", []),
        untraceable_tokens=render.get("untraceable_tokens", []),
        degraded=bool(render.get("degraded", False)),
    )
    expected = case["expected"]
    summary = result.summary
    for key in ("venue", "section", "degraded", "ai_tells_avoided", "untraceable_tokens"):
        if key in expected:
            actual = summary.get(key)
            if key == "section":
                actual = summary.get("section")
            _assert_equal(actual, expected[key], f"summary.{key}")
    if "selection_source" in expected:
        _assert_equal(
            summary.get("selection_source"), expected["selection_source"], "selection_source"
        )
    if "missing_evidence" in expected:
        _assert_equal(
            summary.get("missing_evidence"), expected["missing_evidence"], "missing_evidence"
        )
    if "protected_tokens" in expected:
        _assert_equal(
            summary.get("protected_tokens"), expected["protected_tokens"], "protected_tokens"
        )
    if expected.get("compact_shorter") and not (len(result.text_compact) < len(result.text)):
        raise AssertionError("text_compact must be materially shorter than text")


def _run_profile_gate(case: dict[str, Any]) -> None:
    profiles = case.get("profiles", [])
    manifests = []
    for name in profiles:
        path = ROOT / "profiles" / f"{name}.json"
        manifests.append(json.loads(path.read_text(encoding="utf-8")))
    expected = case["expected"]
    for manifest in manifests:
        gate = manifest["evidence_gate"]
        required = expected["candidate_policy_required"]
        if required not in gate["candidate_policy"]:
            raise AssertionError(f"{manifest['profile']}.candidate_policy omits {required!r}")
    if expected.get("each_profile_isolated"):
        source_paths = {manifest["source_path"] for manifest in manifests}
        provenance = {manifest["provenance"] for manifest in manifests}
        if len(source_paths) != len(manifests) or len(provenance) != len(manifests):
            raise AssertionError("profiles must keep distinct source_path and provenance")
        for manifest in manifests:
            forbidden = set(manifest["forbidden_cross_profile_rules"])
            if "shared_tsv_merge" not in forbidden:
                raise AssertionError(f"{manifest['profile']} permits shared TSV merging")


def run() -> dict[str, Any]:
    cases_path = Path(__file__).with_name("output_contract_cases.json")
    cases = json.loads(cases_path.read_text(encoding="utf-8"))
    failures: list[dict[str, str]] = []
    for case in cases.get("cases", []):
        try:
            kind = case.get("kind")
            if kind == "selection":
                _run_selection(case)
            elif kind == "selection_and_render":
                _run_selection(case)
                _run_render(case)
            elif kind == "render":
                _run_render(case)
            elif kind == "profile_gate":
                _run_profile_gate(case)
            else:
                raise AssertionError(f"unsupported fixture kind: {kind!r}")
        except (AssertionError, KeyError, OSError, json.JSONDecodeError) as exc:
            failures.append({"id": str(case.get("id", "<unknown>")), "error": str(exc)})
    total = len(cases.get("cases", []))
    return {
        "ok": not failures,
        "summary": {"total": total, "passed": total - len(failures), "failed": len(failures)},
        "failures": failures,
        "evidence": "recorded_fixture + pure local core",
        "missing_evidence": [
            "provider-backed output",
            "real-paper style quality",
            "clean installation",
            "human editorial or blind review",
        ],
    }


if __name__ == "__main__":
    report = run()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["ok"] else 1)
