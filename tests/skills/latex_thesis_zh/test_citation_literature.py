"""Opt-in citation placement, repeat pages, and literature progression density."""

from __future__ import annotations

import importlib.util
import os
import re
import subprocess
import sys
from pathlib import Path

from tests.support.paths import REPO_ROOT, SCRIPT_DIR_ZH, SKILLS_ROOT

_BASELINES = REPO_ROOT / "tests/fixtures/thesis-zh-baselines"
BASELINE = _BASELINES / "citation-literature"
C2_REFERENCES = _BASELINES / "number-equation-table"
SKILL = SKILLS_ROOT / "latex-thesis-zh"
FIXTURE = SKILL / "evals/fixtures/thesis-project"
MAIN_TEX = FIXTURE / "main.tex"
REFS_BIB = FIXTURE / "references.bib"
GUIDE = SKILL / "references/writing/literature-progression-zh.md"


def _load_zh(name: str):
    saved_path = list(sys.path)
    collisions = ("bib_scan", "parsers", "tex_loader")
    saved = {module: sys.modules.pop(module, None) for module in collisions}
    loaded_name = f"zh_citation_{name}"
    try:
        sys.path.insert(0, str(SCRIPT_DIR_ZH))
        spec = importlib.util.spec_from_file_location(loaded_name, SCRIPT_DIR_ZH / f"{name}.py")
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[loaded_name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = saved_path
        sys.modules.pop(loaded_name, None)
        for module, value in saved.items():
            if value is None:
                sys.modules.pop(module, None)
            else:
                sys.modules[module] = value


check_references = _load_zh("check_references")
verify_bib = _load_zh("verify_bib")
analyze_literature = _load_zh("analyze_literature")


def test_loader_reads_zh_citation_scripts() -> None:
    assert hasattr(check_references, "ThesisReferenceChecker")
    assert "author_cite" in check_references.ThesisReferenceChecker.__init__.__annotations__ or (
        "author_cite" in check_references.ThesisReferenceChecker.__init__.__code__.co_varnames
    )
    assert "college_details" in verify_bib.BibTeXVerifier.__init__.__code__.co_varnames
    assert "progression" in analyze_literature.analyze.__code__.co_varnames


def _write(tmp_path: Path, body: str, name: str = "main.tex") -> Path:
    path = tmp_path / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return path


def _issues(path: Path, **flags: object) -> list[dict]:
    checker = check_references.ThesisReferenceChecker(str(path), **flags)
    return checker.run_all()


def _by_code(issues: list[dict], code: str) -> list[dict]:
    return [issue for issue in issues if issue.get("code") == code]


def _mention(issues: list[dict], code: str, key: str) -> list[dict]:
    return [issue for issue in _by_code(issues, code) if key in issue["message"]]


def _run(script: str, *args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, "-X", "utf8", "-B", str(SCRIPT_DIR_ZH / script), *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        check=False,
    )


def _run_bytes(script: str, *args: str) -> subprocess.CompletedProcess[bytes]:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, "-X", "utf8", "-B", str(SCRIPT_DIR_ZH / script), *args],
        capture_output=True,
        env=env,
        check=False,
    )


def _norm(data: bytes) -> bytes:
    text = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return re.sub(rb"(?m)^BibTeX Check:.*$", b"BibTeX Check: <BIB>", text)


def test_flags_off_do_not_assemble_or_emit_citation_codes(monkeypatch, tmp_path: Path) -> None:
    def boom(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("assemble should not run without citation flags")

    monkeypatch.setattr(check_references, "assemble", boom)
    path = _write(tmp_path, "见图~\\ref{fig:none}。\\cite{k}\\cite{k}\n")
    issues = _issues(path)
    assert any("Undefined reference" in issue["message"] for issue in issues)
    assert not any(str(issue.get("code", "")).startswith("RC-") for issue in issues)


def test_clear_author_plus_deng_hits_until_cite_moves(tmp_path: Path) -> None:
    lagged = _write(tmp_path, "Example 等人提出了合成路径\\cite{example2020}。\n")
    hits = _mention(_issues(lagged, author_cite=True), "RC-AUTHOR", "example2020")
    assert len(hits) == 1
    hit = hits[0]
    assert hit["file"] == "main.tex"
    assert hit["line"] == 1
    assert hit["severity"] == "Info"
    assert hit["priority"] == "P3"
    assert "[Script]" in hit["message"]
    assert "Meaning-Check: NEEDS-LLM" in hit["message"]
    assert "Example" in hit["message"]
    assert "不确定" not in hit["message"]
    assert "改为" not in hit["message"]
    assert "Example 等人\\cite{example2020}提出" not in hit["message"]

    moved = _write(tmp_path, "Example 等人\\cite{example2020}提出了合成路径。\n", "moved.tex")
    assert _mention(_issues(moved, author_cite=True), "RC-AUTHOR", "example2020") == []


def test_clear_names_cover_accent_hyphen_particle_and_predicate(tmp_path: Path) -> None:
    body = (
        "García 等人指出了差异\\cite{garcia2020}。\n"
        "Smith-Jones 等人提出了结构\\cite{hyphen2020}。\n"
        "van der Waals 等人提出了模型\\cite{particle2020}。\n"
        "Smith proposed a synthetic method\\cite{smith2020}.\n"
    )
    issues = _issues(_write(tmp_path, body), author_cite=True)
    for key in ("garcia2020", "hyphen2020", "particle2020", "smith2020"):
        assert _mention(issues, "RC-AUTHOR", key), key


def test_fact_sentence_and_non_author_subjects_do_not_hit(tmp_path: Path) -> None:
    body = (
        "该方法保持稳定\\cite{stable2020}。\n"
        "由文献\\cite{doc2020}可知该路径存在。\n"
        "由文献[1]可知该路径存在。\n"
        "已有研究\\cite{prior2020}讨论了范围。\n"
    )
    issues = _issues(_write(tmp_path, body), author_cite=True)
    for key in ("stable2020", "doc2020", "prior2020"):
        assert _mention(issues, "RC-AUTHOR", key) == []
        assert _mention(issues, "RC-AUTHOR-UNCERTAIN", key) == []


def test_uncertain_chinese_name_does_not_claim_an_author_fact(tmp_path: Path) -> None:
    bare = _write(tmp_path, "李明提出了另一条路径\\cite{liming2020}。\n")
    hits = _mention(_issues(bare, author_cite=True), "RC-AUTHOR-UNCERTAIN", "liming2020")
    assert len(hits) == 1
    assert "不确定" in hits[0]["message"]
    assert "作者主语" in hits[0]["message"]
    assert "作者是李明" not in hits[0]["message"]
    assert _mention(_issues(bare, author_cite=True), "RC-AUTHOR", "liming2020") == []

    with_deng = _write(tmp_path, "李明等人提出了另一条路径\\cite{liming2020}。\n", "deng.tex")
    deng_hits = _mention(_issues(with_deng, author_cite=True), "RC-AUTHOR-UNCERTAIN", "liming2020")
    assert deng_hits
    assert "作者主语" in deng_hits[0]["message"]
    assert _mention(_issues(with_deng, author_cite=True), "RC-AUTHOR", "liming2020") == []

    coverage = _by_code(_issues(bare, author_cite=True), "RC-AUTHOR-COVERAGE")
    assert coverage
    assert "作者主语不确定" in coverage[0]["message"]
    assert "2–4" in coverage[0]["message"]


def test_textcite_and_citet_do_not_add_an_author_position_hint(tmp_path: Path) -> None:
    body = (
        "Example 等人提出了合成路径\\textcite{example2020}。\n"
        "\\citet{other2020}提出了另一路径。\n"
        "\\citet*{third2020}提出了第三条路径。\n"
    )
    issues = _issues(_write(tmp_path, body), author_cite=True)
    for key in ("example2020", "other2020", "third2020"):
        assert _mention(issues, "RC-AUTHOR", key) == []
        assert _mention(issues, "RC-AUTHOR-UNCERTAIN", key) == []


def test_dotted_abbreviation_does_not_split_the_sentence(tmp_path: Path) -> None:
    same = _write(tmp_path, "Smith 等人提出了方法 e.g. 相关结果\\cite{smith2020}。\n")
    assert _mention(_issues(same, author_cite=True), "RC-AUTHOR", "smith2020")

    split = _write(
        tmp_path,
        "Smith 等人提出了方法。\n见图 e.g. 的结果\\cite{other2020}。\n",
        "split.tex",
    )
    issues = _issues(split, author_cite=True)
    assert _mention(issues, "RC-AUTHOR", "other2020") == []
    assert _mention(issues, "RC-AUTHOR", "smith2020") == []


def test_incomplete_sentence_and_paragraph_boundary_are_not_guessed(tmp_path: Path) -> None:
    incomplete = _write(tmp_path, "Smith 等人提出了方法\\cite{smith2020}\n")
    assert _mention(_issues(incomplete, author_cite=True), "RC-AUTHOR", "smith2020") == []

    blank = _write(
        tmp_path,
        "Smith 等人提出了方法。\n\n后续结果\\cite{other2020}。\n",
        "blank.tex",
    )
    issues = _issues(blank, author_cite=True)
    assert _mention(issues, "RC-AUTHOR", "smith2020") == []
    assert _mention(issues, "RC-AUTHOR", "other2020") == []


def test_author_and_repeat_flags_are_independent(tmp_path: Path) -> None:
    path = _write(
        tmp_path,
        "Example 等人提出了合成路径\\cite{example2020}。\n\\cite{repeat2020}\\cite{repeat2020}\n",
    )
    author_only = _issues(path, author_cite=True)
    repeat_only = _issues(path, repeat_cite=True)
    assert _mention(author_only, "RC-AUTHOR", "example2020")
    assert _by_code(author_only, "RC-REPEATPAGE") == []
    assert _mention(repeat_only, "RC-REPEATPAGE", "repeat2020")
    assert _by_code(repeat_only, "RC-AUTHOR") == []


def test_repeat_page_counts_keys_postnotes_and_dedup(tmp_path: Path) -> None:
    missing = _write(tmp_path, "\\cite{repeat2020}\n\\cite{repeat2020}\n")
    assert _mention(_issues(missing, repeat_cite=True), "RC-REPEATPAGE", "repeat2020")

    paged = _write(tmp_path, "\\cite[12]{repeat2020}\n\\cite[iv--vi]{repeat2020}\n", "paged.tex")
    assert _mention(_issues(paged, repeat_cite=True), "RC-REPEATPAGE", "repeat2020") == []

    once = _write(tmp_path, "\\cite{once2020}\n", "once.tex")
    assert _by_code(_issues(once, repeat_cite=True), "RC-REPEATPAGE") == []

    empty = _write(tmp_path, "\\cite[]{empty2020}\n\\cite[note][]{empty2020}\n", "empty.tex")
    assert _mention(_issues(empty, repeat_cite=True), "RC-REPEATPAGE", "empty2020")

    optional = _write(
        tmp_path,
        "\\cite[见][12]{opt2020}\n\\cite[prenote][101-108]{opt2020}\n",
        "optional.tex",
    )
    assert _mention(_issues(optional, repeat_cite=True), "RC-REPEATPAGE", "opt2020") == []

    one_empty = _write(
        tmp_path,
        "\\cite[见][]{opt2020}\n\\cite[见][12]{opt2020}\n",
        "one-empty.tex",
    )
    assert _mention(_issues(one_empty, repeat_cite=True), "RC-REPEATPAGE", "opt2020")

    deduped = _write(tmp_path, "\\cite{dup2020,dup2020}\n", "dedup.tex")
    assert _mention(_issues(deduped, repeat_cite=True), "RC-REPEATPAGE", "dup2020") == []

    commented = _write(
        tmp_path,
        "\\cite% note\n[12]{pagekey}\n\\cite% note\n[iv--vi]{pagekey}\n",
        "commented.tex",
    )
    assert _mention(_issues(commented, repeat_cite=True), "RC-REPEATPAGE", "pagekey") == []

    commented_gap = _write(
        tmp_path,
        "\\cite% note\n[12]{pagekey}\n\\cite{pagekey}\n",
        "commented-gap.tex",
    )
    assert _mention(_issues(commented_gap, repeat_cite=True), "RC-REPEATPAGE", "pagekey")

    stars = _write(tmp_path, "\\cite*{star2020}\n\\citep{star2020}\n", "stars.tex")
    assert _mention(_issues(stars, repeat_cite=True), "RC-REPEATPAGE", "star2020")

    forms = _write(
        tmp_path,
        "\\citep[3]{mix2020}\n\\parencite[iv]{mix2020}\n\\autocite[10-12]{mix2020}\n",
        "forms.tex",
    )
    assert _mention(_issues(forms, repeat_cite=True), "RC-REPEATPAGE", "mix2020") == []


def test_shared_and_natural_language_postnotes_do_not_pass(tmp_path: Path) -> None:
    shared = _write(tmp_path, "\\cite[12]{alpha,beta}\n")
    issues = _issues(shared, repeat_cite=True)
    assert _by_code(issues, "RC-REPEATPAGE") == []
    notes = _by_code(issues, "RC-SHARED")
    assert len(notes) == 1
    assert "alpha" in notes[0]["message"] and "beta" in notes[0]["message"]
    assert "不能证明" in notes[0]["message"]
    assert "不发明页码" in notes[0]["message"]
    assert "Meaning-Check: NEEDS-LLM" in notes[0]["message"]

    natural = _write(tmp_path, "\\cite[见综述]{nat2020}\n\\cite[同上]{nat2020}\n", "natural.tex")
    natural_issues = _issues(natural, repeat_cite=True)
    assert _by_code(natural_issues, "RC-REPEATPAGE") == []
    post = _mention(natural_issues, "RC-POSTNOTE", "nat2020")
    assert post
    assert "不发明页码" in post[0]["message"]
    assert "建议页" not in post[0]["message"]


def test_repeat_mode_skips_non_visible_cites_and_states_incomplete_coverage(
    tmp_path: Path,
) -> None:
    body = (
        "\\begin{thebibliography}{1}\n\\bibitem{x} \\cite{hidden2020}\n"
        "\\end{thebibliography}\n"
        "\\begin{verbatim}\n\\cite{hidden2020}\n\\end{verbatim}\n"
        "% \\cite{hidden2020}\n"
        "\\nocite{hidden2020}\n"
        "\\newcommand{\\foo}{\\cite{hidden2020}}\n"
        "\\cites{multi2020}{multi2020}\n"
        "\\mycite{custom2020}\\mycite{custom2020}\n"
        "见 \\cite 。\n"
        "正文\\cite{shown2020}。\n"
        "正文\\cite{shown2020}。\n"
    )
    issues = _issues(_write(tmp_path, body), repeat_cite=True)
    shown = _mention(issues, "RC-REPEATPAGE", "shown2020")
    assert shown
    assert "hidden2020" not in shown[0]["message"]
    assert "multi2020" not in shown[0]["message"]
    assert "custom2020" not in shown[0]["message"]
    coverage = _by_code(issues, "RC-COVERAGE")
    assert coverage
    text = coverage[0]["message"]
    assert "覆盖不足" in text
    assert "cites" in text
    assert "自定义宏" in text
    assert "未展开" in text


def test_caption_cites_count_and_school_caption_is_not_duplicated(tmp_path: Path) -> None:
    body = (
        "\\begin{figure}\n"
        "\\caption{合成路径\\cite{capkey}。}\n"
        "\\label{fig:demo}\n"
        "\\end{figure}\n"
        "正文再次引用\\cite{capkey}。\n"
    )
    issues = _issues(
        _write(tmp_path, body),
        school="yanshan-ee-2025",
        author_cite=True,
        repeat_cite=True,
    )
    assert len(_by_code(issues, "CAP-PUNCT")) == 1
    assert _mention(issues, "RC-REPEATPAGE", "capkey")
    assert _by_code(issues, "RC-AUTHOR-COVERAGE")
    assert _by_code(issues, "RC-COVERAGE")


def test_repeat_cite_uses_assemble_order_across_files(tmp_path: Path) -> None:
    _write(tmp_path, "\\include{chapters/a}\n\\include{chapters/b}\n")
    _write(tmp_path, "前文\\cite{order2020}。\n", "chapters/a.tex")
    _write(tmp_path, "后文\\cite{order2020}。\n", "chapters/b.tex")
    hits = _mention(_issues(tmp_path / "main.tex", repeat_cite=True), "RC-REPEATPAGE", "order2020")
    assert len(hits) == 1
    message = hits[0]["message"]
    assert message.index("chapters/a.tex") < message.index("chapters/b.tex")
    assert hits[0]["severity"] == "Info"
    assert "不发明页码" in message


def test_progression_thresholds_count_occurrences_inside_the_section(tmp_path: Path) -> None:
    def report(body: str, section: str | None = "related") -> str:
        path = _write(tmp_path, body, "density.tex")
        return "\n".join(analyze_literature.analyze(path, section, progression=True))

    six = report("\\chapter{文献综述}\n" + "进一步" * 6 + "\n")
    assert "出现 6 次" in six
    assert "严格多于 5" in six
    assert "UNVERIFIED" in six
    assert "[Script]" in six
    assert "Meaning-Check: NEEDS-LLM" in six
    assert "[Severity: Info]" in six
    assert "[Priority: P3]" in six
    assert "改为" not in six
    assert "进而" not in six

    five = report("\\chapter{文献综述}\n" + "进一步" * 5 + "\n")
    assert "UNVERIFIED" not in five
    assert "出现 5 次" not in five

    eight = report("\\chapter{文献综述}\n" + "针对" * 8 + "\n")
    assert "出现 8 次" in eight
    assert "严格多于 7" in eight
    seven = report("\\chapter{文献综述}\n" + "针对" * 7 + "\n")
    assert "出现 7 次" not in seven

    outside = report(
        "\\chapter{文献综述}\n本节没有递进词。\n\\chapter{实验}\n" + "进一步" * 8 + "\n"
    )
    assert "UNVERIFIED" not in outside
    selected = report(
        "\\chapter{文献综述}\n本节没有递进词。\n\\chapter{实验}\n" + "进一步" * 6 + "\n",
        "experiment",
    )
    assert "出现 6 次" in selected

    hidden = report(
        "\\chapter{文献综述}\n"
        "\\begin{figure}\\caption{" + "进一步" * 6 + "}\\end{figure}\n"
        "$" + "进一步" * 6 + "$\n"
        "\\begin{verbatim}\n" + "进一步" * 6 + "\n\\end{verbatim}\n"
        "\\cite{" + "进一步" * 6 + "}\n"
        "正文。\n"
    )
    assert "UNVERIFIED" not in hidden


def test_missing_section_does_not_scan_the_whole_file(tmp_path: Path) -> None:
    path = _write(tmp_path, "\\chapter{实验}\n" + "进一步" * 8 + "\n")
    plain = analyze_literature.analyze(path, "related", progression=False)
    flagged = analyze_literature.analyze(path, "related", progression=True)
    assert plain == flagged
    text = "\n".join(plain)
    assert "未找到章节: related" in text
    assert "UNVERIFIED" not in text
    assert "PASS" not in text


def test_progression_and_intro_citations_are_mutually_exclusive(tmp_path: Path) -> None:
    path = _write(tmp_path, "\\chapter{文献综述}\n正文。\n")
    result = _run(
        "analyze_literature.py",
        str(path),
        "--progression-density",
        "--intro-citations",
        "--current-year",
        "2026",
    )
    assert result.returncode != 0
    assert "PASS" not in result.stdout
    assert "文献综述重写蓝图" not in result.stdout
    assert "不能同时" in result.stderr


def test_progression_without_section_uses_related_only(tmp_path: Path) -> None:
    path = _write(
        tmp_path,
        "\\chapter{绪论}\n" + "进一步" * 8 + "\n\\chapter{文献综述}\n本节没有递进词。\n",
    )
    result = _run("analyze_literature.py", str(path), "--progression-density")
    assert result.returncode == 0
    assert "UNVERIFIED" not in result.stdout
    scoped = _run(
        "analyze_literature.py",
        str(path),
        "--progression-density",
        "--section",
        "绪论",
    )
    assert "出现 8 次" in scoped.stdout


def test_default_commands_match_saved_baselines() -> None:
    for suffix in ("stdout", "stderr", "exit"):
        assert (BASELINE / f"references-default.{suffix}").read_bytes() == (
            C2_REFERENCES / f"references-default.{suffix}"
        ).read_bytes()
    commands = {
        "references-default": ("check_references.py", [str(MAIN_TEX)]),
        "verify-default": ("verify_bib.py", [str(REFS_BIB)]),
        "verify-gb7714": ("verify_bib.py", [str(REFS_BIB), "--standard", "gb7714"]),
        "verify-gb7714-2025": ("verify_bib.py", [str(REFS_BIB), "--standard", "gb7714-2025"]),
        "literature-default": (
            "analyze_literature.py",
            [str(MAIN_TEX), "--current-year", "2026"],
        ),
        "literature-intro": (
            "analyze_literature.py",
            [str(MAIN_TEX), "--intro-citations", "--current-year", "2026"],
        ),
    }
    for name, (script, args) in commands.items():
        result = _run_bytes(script, *args)
        assert _norm(result.stdout) == _norm((BASELINE / f"{name}.stdout").read_bytes()), name
        assert _norm(result.stderr) == _norm((BASELINE / f"{name}.stderr").read_bytes()), name
        assert result.returncode == int((BASELINE / f"{name}.exit").read_text(encoding="ascii"))


def test_public_docs_keep_c1_c2_and_state_c3_flags() -> None:
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    assert "--governance" in skill and "--degree-wording" in skill
    assert "yanshan-ee-2025" in skill and "不接受单独的 `yanshan`" in skill
    for flag in ("--author-cite", "--repeat-cite", "--college-details", "--progression-density"):
        assert flag in skill
    guide = GUIDE.read_text(encoding="utf-8")
    for token in ("方向一", "方向二", "方向三", "方向四", "方向五", "方向六"):
        assert token in guide
    for token in ("组织一", "组织二", "组织三", "组织四"):
        assert token in guide
    assert "合成" in guide and "UNVERIFIED" in guide
    spec = (
        REPO_ROOT / ".trellis/spec/academic-writing-skills/citation-placement-contract.md"
    ).read_text(encoding="utf-8")
    index = (REPO_ROOT / ".trellis/spec/academic-writing-skills/index.md").read_text(
        encoding="utf-8"
    )
    assert "citation-placement-contract.md" in index
    assert "RC-REPEATPAGE" in spec and "--college-details" in spec
    routing = (SKILL / "references/modules/routing-rules.md").read_text(encoding="utf-8")
    assert "--author-cite" in routing and "--progression-density" in routing
    assert "yanshan-ee-2025" in routing
    for relative in (
        "references/modules/references.md",
        "references/modules/bibliography.md",
        "references/modules/literature.md",
        "references/citations/gb-standard.md",
    ):
        text = (SKILL / relative).read_text(encoding="utf-8")
        assert "Meaning-Check: NEEDS-LLM" in text
    assert "literature-progression-zh.md" in (SKILL / "references/modules/literature.md").read_text(
        encoding="utf-8"
    )
    for relative in (
        "README.md",
        "README_CN.md",
        "docs/usage.md",
        "docs/zh/usage.md",
        "docs/skills/latex-thesis-zh/index.md",
        "docs/zh/skills/latex-thesis-zh/index.md",
    ):
        text = (REPO_ROOT / relative).read_text(encoding="utf-8")
        assert "--author-cite" in text
        assert "yanshan-ee-2025" in text
        assert "--degree-wording" in text


def test_footcite_is_supported_by_author_and_repeat_scans(tmp_path: Path) -> None:
    body = (
        "Example 等人提出了合成路径\\footcite{foot2020}。\n"
        "再次提到\\footcite[见][12]{foot2020}与\\footcite{foot2020}。\n"
    )
    path = _write(tmp_path, body)
    assert _mention(_issues(path, author_cite=True), "RC-AUTHOR", "foot2020")
    assert _mention(_issues(path, repeat_cite=True), "RC-REPEATPAGE", "foot2020")


def test_capitalized_non_author_words_do_not_hit(tmp_path: Path) -> None:
    body = (
        "本文采用Adam优化器训练模型，结果表明该方法有效\\cite{adam}。\n"
        "本文在ImageNet上做实验，结果表明该方法有效\\cite{img}。\n"
        "The Kalman filter was proposed for tracking\\cite{kal}.\n"
        "采用Python实现，结果表明有效\\cite{py}。\n"
        "Smith等提出了方法A，该方法表现良好\\cite{s}。\n"
    )
    issues = _issues(_write(tmp_path, body), author_cite=True)
    for key in ("adam", "img", "kal", "py"):
        assert _mention(issues, "RC-AUTHOR", key) == [], key
    assert _mention(issues, "RC-AUTHOR", "s")
