import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_profiles_are_isolated_and_traceable() -> None:
    profiles = [
        json.loads((ROOT / "profiles" / name).read_text(encoding="utf-8"))
        for name in ("nature.json", "ieee.json", "elsevier.json")
    ]
    assert {item["profile"] for item in profiles} == {"nature", "ieee", "elsevier"}
    assert all(item["source_path"] and item["provenance"] for item in profiles)
    assert all(item["load_order"] and item["forbidden_cross_profile_rules"] for item in profiles)
    assert all(item["evidence_gate"] for item in profiles)
