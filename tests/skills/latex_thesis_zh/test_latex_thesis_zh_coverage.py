"""Coverage layer for latex-thesis-zh (audit F19/F20/F21).

- Smoke-runs every SKILL.md Module Router primary command against the
  vendored fixture thesis project (multi-file thuthesis-style skeleton).
- Unit tests for the previously untested scripts: check_format,
  check_references, deai_batch, generate_table, online_bib_verify.
- Orphan scan: every file under references/ and templates/ must be linked
  from somewhere in the skill.
"""

import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

from tests.support.paths import SKILLS_ROOT

_SKILL_DIR = SKILLS_ROOT / "latex-thesis-zh"
_ZH_DIR = _SKILL_DIR / "scripts"
FIXTURE = _SKILL_DIR / "evals" / "fixtures" / "thesis-project"
MAIN_TEX = FIXTURE / "main.tex"
REFS_BIB = FIXTURE / "references.bib"


def _load_zh(name: str):
    zh_str = str(_ZH_DIR)
    inserted = False
    if zh_str not in sys.path or sys.path.index(zh_str) != 0:
        sys.path.insert(0, zh_str)
        inserted = True

    _collision_names = ("parsers", "tex_loader", "online_bib_verify", "map_structure")
    _saved = {}
    for mod_name in list(sys.modules):
        if mod_name in _collision_names:
            _saved[mod_name] = sys.modules.pop(mod_name)

    spec = importlib.util.spec_from_file_location(f"zh_cov_{name}", _ZH_DIR / f"{name}.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)

    for mod_name in _collision_names:
        if mod_name in sys.modules and mod_name not in _saved:
            del sys.modules[mod_name]
        if mod_name in _saved:
            sys.modules[mod_name] = _saved[mod_name]

    if inserted and zh_str in sys.path:
        sys.path.remove(zh_str)
        sys.path.append(zh_str)

    return mod


check_format = _load_zh("check_format")
check_references = _load_zh("check_references")
deai_batch = _load_zh("deai_batch")
generate_table = _load_zh("generate_table")
online_bib_verify = _load_zh("online_bib_verify")


def _run(script: str, *args: str) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(
        [sys.executable, "-B", str(_ZH_DIR / script), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=str(FIXTURE),
        env=env,
        check=False,
    )


# ── SKILL.md 路由主命令冒烟（固化"文档命令可执行"父任务验收） ──
#
# (script, args, allowed exit codes, must-contain marker)
# compile 模块只测 --help（CI 不装 TeX）。

SMOKE_COMMANDS = [
    ("compile.py", ["--help"], {0}, "usage"),
    ("check_format.py", ["main.tex"], {0, 1}, "Format Check Report"),
    ("map_structure.py", ["main.tex"], {0}, "论文结构树"),
    ("check_consistency.py", ["main.tex", "--terms"], {0}, "Term consistency"),
    ("detect_template.py", ["main.tex"], {0}, "thuthesis"),
    ("verify_bib.py", ["references.bib", "--standard", "gb7714"], {1}, "Missing required field"),
    ("optimize_title.py", ["main.tex", "--check", "--headings"], {0}, "TITLE-ARCH"),
    ("deai_check.py", ["main.tex", "--section", "introduction"], {0}, "章节: introduction"),
    ("analyze_logic.py", ["main.tex"], {0}, "缺少导语段落"),
    ("analyze_literature.py", ["main.tex", "--section", "related"], {0}, "文献综述"),
    ("analyze_experiment.py", ["main.tex"], {0}, "% EXPERIMENT"),
    ("check_references.py", ["main.tex"], {1}, "Undefined reference"),
    ("check_tables.py", ["main.tex"], {1}, "Vertical lines detected"),
    ("analyze_abstract.py", ["main.tex", "--lang", "zh"], {0}, "Abstract Structure Diagnosis"),
    (
        "check_spec.py",
        ["main.tex", "--template", "yanshan", "--degree", "doctor", "--year", "2026"],
        {1},
        "规范逐项终检报告",
    ),
    ("blind_review.py", ["main.tex", "--check"], {1}, "盲审匿名化检查报告"),
]


@pytest.mark.parametrize(
    ("script", "args", "codes", "marker"),
    SMOKE_COMMANDS,
    ids=[c[0] for c in SMOKE_COMMANDS],
)
def test_router_command_smoke(script: str, args: list, codes: set, marker: str):
    result = _run(script, *args)
    output = result.stdout + result.stderr
    assert result.returncode in codes, f"{script} rc={result.returncode}\n{output[:2000]}"
    assert marker in output, f"{script} output missing {marker!r}\n{output[:2000]}"


def test_smoke_commands_cover_router_table():
    """冒烟清单必须覆盖 SKILL.md 路由表的每一个脚本。"""
    skill_md = (_SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    router_scripts = set(re.findall(r"\$SKILL_DIR/scripts/(\w+\.py)", skill_md))
    smoke_scripts = {c[0] for c in SMOKE_COMMANDS}
    assert router_scripts <= smoke_scripts, f"未覆盖: {router_scripts - smoke_scripts}"


def test_logic_findings_point_at_source_files():
    """多文件工程的诊断必须定位 源文件:行号（父任务集成验收）。"""
    result = _run("analyze_logic.py", "main.tex")
    assert "chapters/intro.tex:" in result.stdout
    # C3 闭合：绪论承诺未在结论回应（埋点 #20）
    assert "跨章节逻辑链可能不完整" in result.stdout
    # GB18030 附录显式告警（埋点 #22）
    assert "GB18030" in result.stdout


def test_deai_analyze_covers_all_planted_chapters():
    result = _run("deai_check.py", "main.tex", "--analyze")
    output = result.stdout + result.stderr
    assert result.returncode in {0, 1, 2}
    # 埋点 #16：破折号 6 处（上限 5）
    assert "破折号 6 处" in output
    # 埋点 #13：本系统排比
    assert "parallel_structure" in output or "相同模式开头" in output


# ── check_format ─────────────────────────────────────────────


class TestCheckFormat:
    def test_mixed_punctuation_detected(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text("中文句子,使用了半角逗号。\n", encoding="utf-8")
        result = check_format.FormatChecker(str(tex)).check()
        hits = [i for i in result["issues"] if i["code"] == "mixed_punctuation"]
        assert hits and hits[0]["severity"] == "warning"
        assert hits[0]["line"] == 1

    def test_missing_space_after_cite_info(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text("方法来自\\cite{fixture_key}的工作。\n", encoding="utf-8")
        result = check_format.FormatChecker(str(tex)).check()
        hits = [i for i in result["issues"] if i["code"] == "missing_space_after_cite"]
        assert hits and hits[0]["severity"] == "info"

    def test_multifile_issue_points_at_source(self, tmp_path: Path):
        (tmp_path / "chapters").mkdir()
        (tmp_path / "main.tex").write_text("\\include{chapters/body}\n", encoding="utf-8")
        (tmp_path / "chapters" / "body.tex").write_text("效果非常好。\n", encoding="utf-8")
        result = check_format.FormatChecker(str(tmp_path / "main.tex")).check()
        vague = [i for i in result["issues"] if i["code"] == "oral_vague"]
        assert vague and vague[0]["file"] == "chapters/body.tex"
        assert vague[0]["line"] == 1


# ── check_references ─────────────────────────────────────────


class TestCheckReferences:
    def test_undefined_ref_critical(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text("见图~\\ref{fig:nothing}。\n", encoding="utf-8")
        issues = check_references.ThesisReferenceChecker(str(tex)).run_all()
        undefined = [i for i in issues if "Undefined reference" in i["message"]]
        assert undefined and undefined[0]["severity"] == "Critical"

    def test_unreferenced_label_minor(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\begin{figure}\n\\caption{占位}\n\\label{fig:lonely}\n\\end{figure}\n",
            encoding="utf-8",
        )
        issues = check_references.ThesisReferenceChecker(str(tex)).run_all()
        assert any("Unreferenced label" in i["message"] for i in issues)

    def test_multifile_include_resolution(self, tmp_path: Path):
        (tmp_path / "chapters").mkdir()
        (tmp_path / "main.tex").write_text(
            "\\include{chapters/a}\n\\include{chapters/b}\n", encoding="utf-8"
        )
        (tmp_path / "chapters" / "a.tex").write_text(
            "\\begin{figure}\n\\caption{x}\n\\label{fig:a}\n\\end{figure}\n", encoding="utf-8"
        )
        (tmp_path / "chapters" / "b.tex").write_text("如图~\\ref{fig:a}所示。\n", encoding="utf-8")
        issues = check_references.ThesisReferenceChecker(str(tmp_path / "main.tex")).run_all()
        # 跨文件 label/ref 配对成功：无 undefined，也无 unreferenced
        assert not any("Undefined reference" in i["message"] for i in issues)
        assert not any("Unreferenced label" in i["message"] for i in issues)

    def test_fixture_missing_caption_detected(self):
        issues = check_references.ThesisReferenceChecker(str(MAIN_TEX)).run_all()
        assert any(
            "Missing caption" in i["message"] and "fig:orphan" in i["message"] for i in issues
        )


# ── deai_batch ───────────────────────────────────────────────


class TestDeaiBatch:
    def test_section_ranges_from_multifile_project(self):
        processor = deai_batch.ChineseDeAIBatchProcessor(MAIN_TEX)
        # 两个"方法"章都保留（method + method_2），实验章可达
        assert "method" in processor.section_ranges
        assert "method_2" in processor.section_ranges
        assert "experiment" in processor.section_ranges

    def test_analyze_section_finds_planted_traces(self):
        processor = deai_batch.ChineseDeAIBatchProcessor(MAIN_TEX)
        # 章标题与小节标题都命中 experiment 规则 → experiment / experiment_2，
        # 埋点正文在小节区间，扫描全部 experiment* 键。
        patterns = []
        for key in processor.section_ranges:
            if key.startswith("experiment"):
                analysis = processor.analyze_section(key)
                patterns.extend(p for t in analysis["traces"] for p in t["patterns"])
        assert any("显著提升" in p for p in patterns)

    def test_process_section_file_writes_annotated_copy(self, tmp_path: Path):
        chapter = tmp_path / "chap.tex"
        chapter.write_text("近年来，研究增多。\n", encoding="utf-8")
        out_dir = tmp_path / "out"
        out_dir.mkdir()
        processor = deai_batch.ChineseDeAIBatchProcessor(MAIN_TEX)
        assert processor.process_section_file(chapter, out_dir)
        annotated = (out_dir / "chap.tex").read_text(encoding="utf-8")
        assert "去AI化" in annotated
        assert "近年来，研究增多。" in annotated  # 原文保留，只加注释


# ── generate_table ───────────────────────────────────────────


class TestGenerateTable:
    HEADERS = ["Model", "Accuracy", "F1"]
    ROWS = [["Baseline", "85.3", "83.7"], ["Ours", "91.2", "90.4"]]

    def test_latex_output_is_three_line_table(self):
        gen = generate_table.TableGenerator()
        result = gen.generate(self.HEADERS, self.ROWS)
        latex = result["latex"]
        for rule in ("\\toprule", "\\midrule", "\\bottomrule"):
            assert rule in latex
        assert "\\hline" not in latex
        assert "|" not in latex.split("\\begin{tabular}")[1].split("}")[0]

    def test_markdown_preview_contains_rows(self):
        gen = generate_table.TableGenerator()
        result = gen.generate(self.HEADERS, self.ROWS)
        assert "Baseline" in result["markdown"]
        assert "91.2" in result["markdown"]

    def test_csv_loading(self, tmp_path: Path):
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("Model,Accuracy\nBaseline,85.3\n", encoding="utf-8")
        headers, rows = generate_table.load_csv(str(csv_file))
        assert headers == ["Model", "Accuracy"]
        assert rows == [["Baseline", "85.3"]]

    def test_stats_note_added_on_demand(self):
        gen = generate_table.TableGenerator()
        result = gen.generate(self.HEADERS, self.ROWS, stats=True)
        assert "p < 0.05" in result["stats_note"]


# ── online_bib_verify（仅离线部分，网络调用 mock） ────────────


class TestOnlineBibVerify:
    def test_parse_bib_entries(self, tmp_path: Path):
        bib = tmp_path / "refs.bib"
        bib.write_text(
            "@article{fixture_a, title = {Fictional Title}, year = {2024}, "
            "doi = {10.0000/fixture}}\n",
            encoding="utf-8",
        )
        entries = online_bib_verify._parse_bib_entries(bib)
        assert len(entries) == 1
        assert entries[0]["key"] == "fixture_a"
        assert entries[0]["doi"] == "10.0000/fixture"

    def test_cross_check_detects_year_mismatch(self, monkeypatch: pytest.MonkeyPatch):
        verifier = online_bib_verify.OnlineBibVerifier()
        monkeypatch.setattr(
            verifier,
            "verify_doi",
            lambda doi: online_bib_verify.VerifyResult(
                valid=True,
                metadata={"title": "T", "authors": [], "year": "2020", "journal": "J"},
            ),
        )
        result = verifier.verify_entry(
            {"key": "fixture_b", "doi": "10.0000/x", "year": "2024", "journal": "J"}
        )
        assert result.status == "mismatch"
        assert any("year" in m for m in result.mismatches)

    def test_verified_when_metadata_agrees(self, monkeypatch: pytest.MonkeyPatch):
        verifier = online_bib_verify.OnlineBibVerifier()
        monkeypatch.setattr(
            verifier,
            "verify_doi",
            lambda doi: online_bib_verify.VerifyResult(
                valid=True,
                metadata={"title": "T", "authors": [], "year": "2024", "journal": "Fict J"},
            ),
        )
        result = verifier.verify_entry(
            {"key": "fixture_c", "doi": "10.0000/x", "year": "2024", "journal": "Fict J"}
        )
        assert result.status == "verified"

    def test_unverifiable_without_doi_or_match(self, monkeypatch: pytest.MonkeyPatch):
        verifier = online_bib_verify.OnlineBibVerifier()
        monkeypatch.setattr(verifier, "search_by_title", lambda title: [])
        result = verifier.verify_entry({"key": "fixture_d", "title": "No Such Fictional Paper"})
        assert result.status == "unverifiable"


# ── evals.json 与 fixture 的绑定 ──────────────────────────────


def test_core_evals_bind_real_fixture_files():
    payload = json.loads((_SKILL_DIR / "evals" / "evals.json").read_text(encoding="utf-8"))
    with_files = [e for e in payload["evals"] if e["files"]]
    assert len(with_files) >= 6, "至少 6 条核心用例须绑定 fixture"
    for item in with_files:
        for rel in item["files"]:
            assert (_SKILL_DIR / rel).exists(), f"eval {item['id']} fixture 不可达: {rel}"


# ── 孤儿扫描：references/ 与 templates/ 下无文件缺少入链 ──────


def test_no_orphan_reference_files():
    linkable = []
    for base in ("references", "templates"):
        linkable.extend((_SKILL_DIR / base).rglob("*"))
    targets = [p for p in linkable if p.is_file()]

    corpus = ""
    for md in [
        _SKILL_DIR / "SKILL.md",
        *(_SKILL_DIR / "references").rglob("*.md"),
        *(_SKILL_DIR / "templates").rglob("*.md"),
        *(_SKILL_DIR / "examples").rglob("*.md"),
        *(_SKILL_DIR / "scripts").rglob("*.py"),
    ]:
        corpus += md.read_text(encoding="utf-8", errors="replace")

    orphans = []
    for target in targets:
        name = target.name
        # 自引用不算入链：从语料中剔除该文件自身内容后再查
        self_text = target.read_text(encoding="utf-8", errors="replace")
        rest = corpus.replace(self_text, "", 1)
        # 目录级引用（templates/、references/modules/ 等）对 *.md 同样视为可达
        dir_ref = f"{target.parent.name}/" in rest and target.suffix == ".md"
        if name not in rest and not dir_ref:
            orphans.append(str(target.relative_to(_SKILL_DIR)))
    assert not orphans, f"孤儿文件（无任何入链）: {orphans}"
