"""Method-section narrative checks for the Typst paper skill."""

import importlib.util
import sys
from pathlib import Path

from tests.support.paths import SCRIPT_DIR_TYPST


def _load_typst_logic():
    saved_path = list(sys.path)
    saved_modules = {name: sys.modules.pop(name, None) for name in ("parsers",)}
    try:
        sys.path.insert(0, str(SCRIPT_DIR_TYPST))
        spec = importlib.util.spec_from_file_location(
            "typst_method_analyze_logic", SCRIPT_DIR_TYPST / "analyze_logic.py"
        )
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = saved_path
        for name, module in saved_modules.items():
            if module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module


analyze_logic = _load_typst_logic()


def _run(tmp_path: Path, content: str, section: str | None = "methods") -> str:
    typ = tmp_path / "main.typ"
    typ.write_text(content, encoding="utf-8")
    return "\n".join(analyze_logic.analyze(typ, section))


_METHOD_CASE = """= Proposed Method
== Encoder
Next, we introduce the encoder module.
*Input stage.* This module is used to normalize the samples.
The samples retain their timestamps during normalization.
*Fusion stage.*
The component aims to fuse the aligned features.
*Output stage.* The stage emits the fused representation.
$
z = f(x)
$ <eq:encoder>
The score is computed from the fused representation.
It is normalized across the feature axis.
The result enters the decoder.
== Decoder
Because the fused representation remains ambiguous, the decoder resolves it.
"""


_COMPLIANT_METHOD = """= Methods
== Encoder
Because the raw samples remain noisy, the encoder first aligns their timestamps.
*Input representation.* The upstream samples retain their measured units.
*Alignment operator.* A masked projection aligns valid observations.
*Output contract.* The encoder emits an aligned feature tensor.
$
z = f(x)
$ <eq:encoder>
where $z$ denotes the aligned representation passed to the decoder.
== Decoder
Since the aligned tensor still contains ambiguity, the decoder estimates the target.
"""


def test_typst_method_narrative_reports_three_candidates_and_edge_table(
    tmp_path: Path,
) -> None:
    report = _run(tmp_path, _METHOD_CASE)

    assert report.count("M-HEADING") == 1
    assert report.count("M-SEQWORD") == 1
    assert report.count("M-EQUATION") == 1
    assert "M-EDGETABLE" in report
    assert "Encoder -> Decoder" in report
    assert report.count("Meaning-Check: NEEDS-LLM") == 3


def test_typst_method_narrative_accepts_closed_method_section(tmp_path: Path) -> None:
    report = _run(tmp_path, _COMPLIANT_METHOD)

    assert "M-HEADING" not in report
    assert "M-SEQWORD" not in report
    assert "M-EQUATION" not in report
    assert "M-EDGETABLE" in report


def test_typst_method_equation_ignores_unlabeled_block(tmp_path: Path) -> None:
    report = _run(
        tmp_path,
        """= Methods
== Encoder
Because the input remains noisy, the encoder aligns it.
$
z = f(x)
$
The score is computed from the representation.
It is normalized across the feature axis.
The result enters the decoder.
== Decoder
Because ambiguity remains, the decoder estimates the target.
""",
    )

    assert "M-EQUATION" not in report


def test_typst_method_equation_detects_labeled_multiline_block(tmp_path: Path) -> None:
    report = _run(
        tmp_path,
        """= Methods
== Encoder
Because the input remains noisy, the encoder aligns it.
$ z &= f(x) \\
  &= g(x) $ <eq:encoder>
The score is computed from the representation.
It is normalized across the feature axis.
The result enters the decoder.
== Decoder
Because ambiguity remains, the decoder estimates the target.
""",
    )

    assert report.count("M-EQUATION") == 1
    assert "<eq:encoder>" in report


def test_typst_method_equations_share_one_following_gloss(tmp_path: Path) -> None:
    report = _run(
        tmp_path,
        """= Methods
== Encoder
Because the input remains noisy, the encoder aligns it.
$
z_1 = f(x)
$ <eq:aligned>
$
z_2 = g(z_1)
$ <eq:fused>
where $z_1$ is the aligned feature and $z_2$ enters the decoder.
== Decoder
Because ambiguity remains, the decoder estimates the target.
""",
    )

    assert "M-EQUATION" not in report


def test_typst_method_narrative_respects_comments_and_protected_tokens(tmp_path: Path) -> None:
    report = _run(
        tmp_path,
        """= Methods
== Boundary handling
Next, this section introduces the boundary module. // because a constraint remains
*Comment heading.* // This module is used to announce a false hit.
The paragraph only states the input boundary.
*Real announcement.* This module is used to normalize the samples.
*Protected announcement.* $ "This module is used to" $
$ x = 1 $ <eq:boundary>
The output object is defined. // where appears only in a comment
See @eq:where; the reference key is not a symbol gloss.
$ where $ appears only inside protected math.
== Decoder
Because ambiguity remains, the decoder estimates the target.
""",
    )

    assert "M-HEADING" not in report
    assert "M-SEQWORD" in report
    assert "M-EQUATION" in report


def test_typst_method_narrative_ignores_block_comments(tmp_path: Path) -> None:
    report = _run(
        tmp_path,
        """= Methods
== Encoder
Because the input remains noisy, the encoder aligns it.
/*
*Input stage.* This module is used to normalize the samples.
*Fusion stage.* The component aims to fuse the features.
*Output stage.* The stage emits the representation.
$
z = f(x)
$ <eq:disabled>
*/
== Decoder
Because ambiguity remains, the decoder estimates the target.
""",
    )

    assert "M-HEADING" not in report
    assert "M-EQUATION" not in report


def test_typst_method_narrative_is_off_without_section_gate(tmp_path: Path) -> None:
    report = _run(tmp_path, _METHOD_CASE, section=None)

    assert "M-HEADING" not in report
    assert "M-SEQWORD" not in report
    assert "M-EQUATION" not in report
    assert "M-EDGETABLE" not in report


def test_typst_experiment_lead_ins_do_not_enter_method_scope(tmp_path: Path) -> None:
    report = _run(
        tmp_path,
        """= Methods
== Pipeline
Because the input remains noisy, the pipeline aligns it before prediction.
= Experiments
*Accuracy by dataset.* The score reaches 91.2 percent.
*Latency by batch.* The median is 12 milliseconds.
*Memory by model.* The peak is 4.2 gigabytes.
""",
    )

    assert "M-HEADING" not in report
    assert "M-SEQWORD" not in report
    assert "M-EQUATION" not in report


def test_typst_sequence_transitions_have_one_runtime_source() -> None:
    assert analyze_logic.TRANSITIONS["sequence"] == {
        "next",
        "then",
        "subsequently",
        "after that",
        "after this",
    }
