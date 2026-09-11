import sys
from pathlib import Path

SCRIPTS_ROOT = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from core import canonical_section, render_result, select_profile  # noqa: E402


def test_precedence_and_conflict():
    result = select_profile(venue="nature", journal="Applied Energy", domain="control_ieee")
    assert result.venue == "nature"
    assert len(result.conflicts) == 2


def test_journal_then_domain_then_unspecified():
    assert select_profile(journal="Applied Energy").venue == "elsevier"
    assert select_profile(domain="control_ieee").venue == "ieee"
    result = select_profile(domain="quantum")
    assert result.venue == "unspecified" and result.missing_evidence


def test_aliases_and_tokens_are_traceable():
    assert canonical_section("experiments").canonical == "results"
    result = render_result(
        "Value [1] is 42%.",
        input_text="Value [1] is 42%.",
        selection=select_profile(),
        target="method",
    )
    assert result.summary["section"] == "methods"
    assert "[1]" in result.summary["protected_tokens"]
