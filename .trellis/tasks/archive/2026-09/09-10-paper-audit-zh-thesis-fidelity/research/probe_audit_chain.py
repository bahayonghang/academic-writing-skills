"""Read-only product probes; all synthetic workspace writes stay in one temp directory."""

from __future__ import annotations

import contextlib
import dataclasses
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
AUDIT = ROOT / "academic-writing-skills" / "paper-audit"
ZH = ROOT / "academic-writing-skills" / "latex-thesis-zh"
sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["PYTHONIOENCODING"] = "utf-8"
sys.path.insert(0, str(AUDIT / "scripts"))

import audit  # noqa: E402
from consolidate_review_findings import consolidate_findings, load_comment_files  # noqa: E402
from paths import WorkspaceLayout  # noqa: E402
from prepare_review_workspace import prepare_workspace  # noqa: E402
from report_generator import (  # noqa: E402
    AuditIssue, AuditResult, calculate_scores, render_json_report,
    render_self_check_report, render_deep_review_report, render_gate_report,
)
from scholar_eval import evaluate_from_audit  # noqa: E402


def command(args: list[str]) -> dict:
    result = subprocess.run(
        [sys.executable, "-B", *args],
        capture_output=True,
        encoding="utf-8",
        cwd=ROOT,
        env=dict(os.environ),
        timeout=60,
        check=False,
    )
    return {
        "command": [sys.executable, "-B", *args],
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def main() -> None:
    result: dict = {
        "date": "2026-09-10",
        "boundary": "Synthetic local CLI/API probes; no LLM reviewer, network, TeX compiler, or real thesis run.",
        "source_hashes": {
            str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in (
                AUDIT / "scripts/audit.py",
                AUDIT / "scripts/zh_check_adapters.py",
                AUDIT / "scripts/prepare_review_workspace.py",
                AUDIT / "scripts/consolidate_review_findings.py",
                ZH / "scripts/check_consistency.py",
            )
        },
        "cases": {},
    }
    info_issue = AuditIssue("CONSISTENCY", None, "Info", "P3", "[Script] NEEDS-LLM 合成观察")
    info_result = AuditResult(
        file_path="synthetic.tex", language="zh", mode="quick-audit", issues=[info_issue]
    )
    result["info_scoring"] = {
        "issue": dataclasses.asdict(info_issue),
        "legacy_empty": calculate_scores([]),
        "legacy_info": calculate_scores([info_issue]),
        "scholar_info": evaluate_from_audit([dataclasses.asdict(info_issue)]),
        "json_report": json.loads(render_json_report(info_result)),
        "quick_info_visible": "NEEDS-LLM 合成观察" in render_self_check_report(info_result),
        "deep_info_visible": "NEEDS-LLM 合成观察" in render_deep_review_report(info_result),
        "gate_info_visible": "NEEDS-LLM 合成观察" in render_gate_report(info_result),
        "phase0": audit.export_phase0_context(info_result),
        "presubmission_promoted": audit._presubmission_phase0_issues(info_result, []),
    }
    with tempfile.TemporaryDirectory(prefix="probe-work-", dir=HERE) as temporary:
        work = Path(temporary).resolve()
        assert work.is_relative_to(HERE.resolve())
        fixtures = {
            "clean": "\\documentclass{ctexbook}\n\\begin{document}\n\\chapter{绪论}\n卷积神经网络（CNN）用于识别。本文使用CNN，后续仍使用CNN。\n\\end{document}\n",
            "late_definition": "\\documentclass{ctexbook}\n\\begin{document}\n\\chapter{绪论}\n采用CNN得到结果，卷积神经网络（CNN）用于识别。\n\\end{document}\n",
            "equivalent_expansions": "\\documentclass{ctexbook}\n\\begin{document}\n\\chapter{绪论}\n卷积神经网络（CNN）用于识别。\n\\chapter{模型}\nconvolutional neural network (CNN)用于分类。\n\\end{document}\n",
            "missing_include": "\\documentclass{ctexbook}\n\\begin{document}\n\\chapter{绪论}\n本文研究一种方法。\n\\input{missing_chapter}\n\\end{document}\n",
            "multi_file": "\\documentclass{ctexbook}\n\\begin{document}\n\\input{introduction}\n\\input{method}\n\\end{document}\n",
            "legal_synthesis": "\\documentclass{ctexbook}\n\\begin{document}\n\\chapter{相关工作}\n现有研究通常通过约束输入表示改善小样本识别，相关工作共同支持这一技术路线\\cite{a,b,c}。本文比较其适用条件，并保留样本边界。\n\\end{document}\n",
            "distinct_concepts": "\\documentclass{ctexbook}\n\\begin{document}\n\\chapter{绪论}\n数据处理包含数据预处理。算法嵌入模型，系统调用模型。训练数据和测试数据保持不同用途。\n\\end{document}\n",
        }
        (work / "introduction.tex").write_text(
            "\\chapter{绪论}\n采用CNN得到结果。此处首次使用缩略语。\n", encoding="utf-8"
        )
        (work / "method.tex").write_text(
            "\\chapter{模型}\n卷积神经网络（CNN）用于识别。独有标记：模型章完整证据。\n", encoding="utf-8"
        )
        result["fixtures"] = {
            **fixtures,
            "introduction.tex": (work / "introduction.tex").read_text(encoding="utf-8"),
            "method.tex": (work / "method.tex").read_text(encoding="utf-8"),
        }
        for name, source in fixtures.items():
            path = work / f"{name}.tex"
            path.write_text(source, encoding="utf-8")
            raw = command([str(ZH / "scripts/check_consistency.py"), str(path)])
            issues, kind = audit._ingest_check_output(
                "consistency", ZH / "scripts/check_consistency.py",
                raw["returncode"], raw["stdout"], raw["stderr"],
            )
            checklist = audit._run_checklist(source, str(path), "zh")
            case = {
                "raw_consistency": raw,
                "raw_consistency_json": command([
                    str(ZH / "scripts/check_consistency.py"), str(path), "--json",
                ]),
                "ingest_kind": kind,
                "ingested_issues": [dataclasses.asdict(issue) for issue in issues],
                "consistency_only_score": evaluate_from_audit(
                    [dataclasses.asdict(issue) for issue in issues]
                ),
                "acronym_checklist": [
                    dataclasses.asdict(item) for item in checklist
                    if "Acronyms" in item.description
                ],
            }
            minimal = AuditResult(
                file_path=str(path), language="zh", mode="quick-audit",
                issues=issues, checklist=checklist,
            )
            case["phase0_context"] = audit.export_phase0_context(minimal)
            result["cases"][name] = case

        # Run the complete public quick-audit CLI once; all modules really execute.
        result["complete_quick_audit"] = command([
            str(AUDIT / "scripts/audit.py"), str(work / "clean.tex"),
            "--mode", "quick-audit", "--lang", "zh", "--format", "json",
        ])

        # Verify that legal synthesis evidence reaches the existing literature adapter.
        result["legal_synthesis_literature"] = command([
            str(ZH / "scripts/analyze_literature.py"), str(work / "legal_synthesis.tex"),
        ])

        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            workspace = prepare_workspace(str(work / "multi_file.tex"), str(work / "reviews"))
        layout = WorkspaceLayout(workspace)
        result["workspace"] = {
            "prepare_stdout": captured.getvalue(),
            "full_text": layout.full_text.read_text(encoding="utf-8"),
            "section_index": json.loads(layout.section_index.read_text(encoding="utf-8")),
            "references": sorted(path.name for path in layout.references_dir.iterdir()),
            "legacy_input_paths_exist": {
                name: (workspace / name).exists()
                for name in ("paper_summary.md", "claim_map.json", "sections", "references")
            },
        }
        issue = {
            "title": "合成评论路径探针", "quote": "本文研究一种方法",
            "explanation": "仅用于验证评论路径被真实合并入口消费。",
            "comment_type": "missing_information", "severity": "minor",
            "source_kind": "llm", "source_section": "introduction",
            "review_lane": "zh_thesis_review",
        }
        legacy_comments = workspace / "comments"
        legacy_comments.mkdir()
        (legacy_comments / "zh_thesis_review.json").write_text(
            json.dumps([issue], ensure_ascii=False), encoding="utf-8"
        )
        result["workspace"]["documented_output_seen_by_consumer"] = len(
            consolidate_findings(load_comment_files(layout.comments_dir))
        )
        layout.comment_file("zh_thesis_review.json").write_text(
            json.dumps([issue], ensure_ascii=False), encoding="utf-8"
        )
        result["workspace"]["canonical_output_seen_by_consumer"] = len(
            consolidate_findings(load_comment_files(layout.comments_dir))
        )
        result["workspace"]["consolidation_cli"] = command([
            str(AUDIT / "scripts/consolidate_review_findings.py"), str(workspace),
        ])
        result["workspace"]["cli_final_issues"] = json.loads(
            layout.final_issues.read_text(encoding="utf-8")
        )
    result["temporary_directory_removed"] = not work.exists()
    output = HERE / "probe-results.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output),
        "clean_issues": len(result["cases"]["clean"]["ingested_issues"]),
        "clean_score": result["cases"]["clean"]["consistency_only_score"],
        "late_checklist": result["cases"]["late_definition"]["acronym_checklist"],
        "multi_file_workspace": result["workspace"]["full_text"],
        "legacy_comment_loaded": result["workspace"]["documented_output_seen_by_consumer"],
        "canonical_comment_loaded": result["workspace"]["canonical_output_seen_by_consumer"],
        "temporary_directory_removed": result["temporary_directory_removed"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
