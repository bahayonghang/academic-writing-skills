"""blind_review.py（盲审匿名化检查与盲审版生成）单测与 fixture 集成。

加载约定：zh 副本脚本必须 importlib 按路径加载并对称恢复 sys.path/sys.modules
（见 .trellis/spec/academic-writing-skills/testing-and-tooling.md）。
红线断言：--generate 只写 `_blind` 副本、原文件内容哈希不变；
`\\cite`/`\\ref`/`\\label`/数学环境在副本中与原文逐字一致；--dry-run 零写盘。
"""

import hashlib
import importlib.util
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from tests.support.paths import SCRIPT_DIR_ZH, SKILLS_ROOT

_SKILL_DIR = SKILLS_ROOT / "latex-thesis-zh"
FIXTURE = _SKILL_DIR / "evals" / "fixtures" / "thesis-project"
MAIN_TEX = FIXTURE / "main.tex"


def _load_zh():
    saved_path = list(sys.path)
    saved = {m: sys.modules.pop(m, None) for m in ("parsers", "tex_loader")}
    try:
        spec = importlib.util.spec_from_file_location(
            "zh_blind_review", SCRIPT_DIR_ZH / "blind_review.py"
        )
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        sys.path.insert(0, str(SCRIPT_DIR_ZH))
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = saved_path
        for name, mod in saved.items():
            if mod is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = mod


blind_review = _load_zh()


def test_loader_guard_zh_blind_review():
    """加载守卫：确认拿到 zh 副本的 blind_review（防静默退化到别的脚本）。"""
    assert hasattr(blind_review, "BlindReviewChecker")
    assert hasattr(blind_review, "plan_copies")
    assert blind_review.ACK_PLACEHOLDER == "（盲审版本，致谢内容略）"
    assert blind_review.PLACEHOLDER == "□□□"
    assert "TODO-BLIND(R2)" in blind_review.R2_TODO


# ── helpers ──────────────────────────────────────────────────


def _run_cli(*args: str, cwd: Path) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(
        [sys.executable, "-B", str(SCRIPT_DIR_ZH / "blind_review.py"), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=str(cwd),
        env=env,
        check=False,
    )


def _line_of(path: Path, needle: str) -> int:
    for no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if needle in line:
            return no
    raise AssertionError(f"{needle!r} not found in {path}")


def _hash_tree(root: Path) -> dict[Path, str]:
    return {
        p: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


TOKEN_RE = re.compile(r"\\(?:cite|ref|eqref|autoref|label)\{[^}]*\}")
MATH_RE = re.compile(r"\$[^$]+\$")


def _protected_tokens(content: str) -> list[str]:
    out = []
    for line in content.split("\n"):
        if line.strip().startswith("%"):
            continue
        out.extend(TOKEN_RE.findall(line))
        out.extend(MATH_RE.findall(line))
    return out


# ── --check 集成（真实 fixture，只读） ────────────────────────


class TestFixtureCheck:
    def test_detects_all_planted_leaks_with_locations(self):
        result = _run_cli("main.tex", "--check", cwd=FIXTURE)
        assert result.returncode == 1
        out = result.stdout
        assert "盲审匿名化检查报告" in out

        author_line = _line_of(MAIN_TEX, "\\author{测试作者}")
        supervisor_line = _line_of(MAIN_TEX, "supervisor = {测试导师}")
        entry_line = _line_of(FIXTURE / "chapters" / "achievements.tex", "张三, 李四, 王五")
        assert f"(main.tex:L{author_line}) [HIGH] [P0] [Script]: R1 作者字段" in out
        assert f"(main.tex:L{supervisor_line}) [HIGH] [P0] [Script]: R1 导师字段" in out
        assert "(chapters/acknowledgement.tex:L1) [HIGH] [P0] [Script]: R1 致谢内容未隐去" in out
        assert (
            f"(chapters/achievements.tex:L{entry_line}) [HIGH] [P0] [Script]: R2 成果条目含" in out
        )

    def test_compliant_achievement_entry_not_flagged(self):
        result = _run_cli("main.tex", "--check", cwd=FIXTURE)
        compliant_line = _line_of(
            FIXTURE / "chapters" / "achievements.tex", "第一作者，虚构学报，2023"
        )
        assert f"chapters/achievements.tex:L{compliant_line})" not in result.stdout
        # 全文只有一条 R2 finding（条目二已合规）
        assert result.stdout.count("[Script]: R2") == 1

    def test_hints_skipped_name_scan_without_flags(self):
        result = _run_cli("main.tex", "--check", cwd=FIXTURE)
        assert "跳过全文姓名扫描" in result.stdout
        assert "正文出现" not in result.stdout

    def test_name_scan_hits_acknowledgement_high(self):
        result = _run_cli(
            "main.tex", "--check", "--author", "测试作者", "--supervisor", "测试导师", cwd=FIXTURE
        )
        out = result.stdout
        ack = FIXTURE / "chapters" / "acknowledgement.tex"
        sup_line = _line_of(ack, "感谢测试导师")
        author_line = _line_of(ack, "作者测试作者在此")
        assert f"(chapters/acknowledgement.tex:L{sup_line}) [HIGH]" in out
        assert "正文出现导师姓名“测试导师”" in out
        assert f"(chapters/acknowledgement.tex:L{author_line}) [HIGH]" in out
        assert "正文出现作者姓名“测试作者”" in out


# ── --generate / --dry-run（tmp 副本工程，保护真实 fixture） ──


def _copy_fixture(tmp_path: Path) -> Path:
    proj = tmp_path / "proj"
    shutil.copytree(FIXTURE, proj)
    return proj


class TestGenerate:
    def test_generate_writes_blind_copies_and_keeps_originals(self, tmp_path: Path):
        proj = _copy_fixture(tmp_path)
        before = _hash_tree(proj)
        result = _run_cli("main.tex", "--generate", cwd=proj)
        assert result.returncode == 0
        assert "原文件未改动" in result.stdout

        # 红线：所有既有文件内容哈希不变
        after = {p: h for p, h in _hash_tree(proj).items() if p in before}
        assert after == before

        main_blind = proj / "main_blind.tex"
        ack_blind = proj / "chapters" / "acknowledgement_blind.tex"
        ach_blind = proj / "chapters" / "achievements_blind.tex"
        assert main_blind.exists() and ack_blind.exists() and ach_blind.exists()

        main_text = main_blind.read_text(encoding="utf-8")
        assert "\\author{□□□}" in main_text
        assert "supervisor = {□□□}" in main_text
        assert "测试作者" not in main_text.replace("% seed: blind-review R1 作者字段", "")
        # 受影响 include 改指副本；未受影响 include 保持原样
        assert "\\input{chapters/achievements_blind}" in main_text
        assert "\\input{chapters/acknowledgement_blind}" in main_text
        assert "\\include{chapters/intro}" in main_text

        ack_text = ack_blind.read_text(encoding="utf-8")
        assert "\\chapter{致谢}" in ack_text
        assert blind_review.ACK_PLACEHOLDER in ack_text
        assert "% BLIND-AUTO(R1)" in ack_text
        assert "测试导师" not in ack_text
        assert "测试作者" not in ack_text

    def test_r2_entry_gets_todo_comment_and_stays_verbatim(self, tmp_path: Path):
        proj = _copy_fixture(tmp_path)
        assert _run_cli("main.tex", "--generate", cwd=proj).returncode == 0
        src = (proj / "chapters" / "achievements.tex").read_text(encoding="utf-8")
        blind = (proj / "chapters" / "achievements_blind.tex").read_text(encoding="utf-8")
        entry = next(line for line in src.splitlines() if "张三, 李四, 王五" in line)
        blind_lines = blind.splitlines()
        idx = blind_lines.index(entry)  # 条目逐字保留（含 $\alpha$ 数学）
        assert blind_lines[idx - 1].startswith("% TODO-BLIND(R2)")
        assert "$\\alpha$" in blind_lines[idx]
        # 合规条目不加注释
        compliant = next(line for line in src.splitlines() if "第一作者，虚构学报，2023" in line)
        c_idx = blind_lines.index(compliant)
        assert not blind_lines[c_idx - 1].startswith("% TODO-BLIND")

    def test_cite_ref_label_math_identical_in_assembled_blind(self, tmp_path: Path):
        proj = _copy_fixture(tmp_path)
        assert _run_cli("main.tex", "--generate", cwd=proj).returncode == 0
        original = blind_review.assemble(proj / "main.tex")
        blind = blind_review.assemble(proj / "main_blind.tex")
        assert _protected_tokens(original.content) == _protected_tokens(blind.content)
        # 盲审副本可被 tex_loader 组装且不缺文件
        assert blind.multi_file
        assert not blind.missing

    def test_dry_run_writes_nothing(self, tmp_path: Path):
        proj = _copy_fixture(tmp_path)
        before = _hash_tree(proj)
        result = _run_cli("main.tex", "--generate", "--dry-run", cwd=proj)
        assert result.returncode == 0
        assert "DRY-RUN: 未写入任何文件" in result.stdout
        assert "main_blind.tex" in result.stdout  # 计划仍然打印
        assert _hash_tree(proj) == before  # 文件集合与内容均不变

    def test_refuses_existing_blind_without_force(self, tmp_path: Path):
        proj = _copy_fixture(tmp_path)
        assert _run_cli("main.tex", "--generate", cwd=proj).returncode == 0
        sentinel = proj / "main_blind.tex"
        sentinel.write_text("SENTINEL", encoding="utf-8")
        result = _run_cli("main.tex", "--generate", cwd=proj)
        assert result.returncode == 3
        assert "--force" in result.stdout
        assert sentinel.read_text(encoding="utf-8") == "SENTINEL"  # 未被覆盖
        forced = _run_cli("main.tex", "--generate", "--force", cwd=proj)
        assert forced.returncode == 0
        assert "\\documentclass" in sentinel.read_text(encoding="utf-8")

    def test_custom_suffix(self, tmp_path: Path):
        proj = _copy_fixture(tmp_path)
        result = _run_cli("main.tex", "--generate", "--suffix", "_anon", cwd=proj)
        assert result.returncode == 0
        assert (proj / "main_anon.tex").exists()
        assert "\\input{chapters/acknowledgement_anon}" in (proj / "main_anon.tex").read_text(
            encoding="utf-8"
        )


# ── 检测面单测（tmp 微型工程，直接调模块） ────────────────────


def _mini(tmp_path: Path, content: str) -> Path:
    tex = tmp_path / "mini.tex"
    tex.write_text(content, encoding="utf-8")
    return tex


class TestCheckerUnits:
    def test_name_hit_in_body_chapter_is_medium(self, tmp_path: Path):
        tex = _mini(
            tmp_path,
            "\\documentclass{book}\n\\begin{document}\n"
            "\\chapter{占位方法}\n本方法由张三提出并实现。\n\\end{document}\n",
        )
        checker = blind_review.BlindReviewChecker(tex, author="张三")
        findings = checker.run_check()
        names = [f for f in findings if f.kind == "name"]
        assert len(names) == 1
        assert names[0].severity == "MEDIUM"

    def test_ack_with_protected_tokens_downgrades_to_todo(self, tmp_path: Path):
        tex = _mini(
            tmp_path,
            "\\documentclass{book}\n\\begin{document}\n\\chapter{致谢}\n"
            "感谢某某老师的悉心指导，相关工作见文献\\cite{key1}，在此一并表示诚挚谢意。\n"
            "\\chapter{结语}\n完。\n\\end{document}\n",
        )
        checker = blind_review.BlindReviewChecker(tex)
        checker.run_check()
        plans, todo_summary, _ = blind_review.plan_copies(checker, "_blind")
        entry_plan = next(p for p in plans if p.src == checker.tex_file)
        # 未自动替换：占位文本只允许出现在 TODO 注释里，不出现在正文行
        body_lines = [ln for ln in entry_plan.text.splitlines() if not ln.strip().startswith("%")]
        assert all(blind_review.ACK_PLACEHOLDER not in ln for ln in body_lines)
        assert "\\cite{key1}" in entry_plan.text  # 内容原样保留
        assert "感谢某某老师的悉心指导" in entry_plan.text
        assert "TODO-BLIND(R1)" in entry_plan.text
        assert any("降级为 TODO" in item for item in todo_summary)

    def test_unknown_template_reports_needs_llm(self, tmp_path: Path):
        tex = _mini(
            tmp_path,
            "\\documentclass{myschoolthesis}\n\\begin{document}\n"
            "\\chapter{绪论}\n正文。\n\\end{document}\n",
        )
        checker = blind_review.BlindReviewChecker(tex)
        findings = checker.run_check()
        notes = [f.message for f in findings if f.kind == "needs_llm"]
        assert any("myschoolthesis" in m and "NEEDS-LLM" in m for m in notes)
        assert any("未检出作者字段" in m for m in notes)

    def test_r3_findings_are_info_and_labeled_as_convention(self, tmp_path: Path):
        tex = _mini(
            tmp_path,
            "\\documentclass{book}\n\\begin{document}\n"
            "\\chapter{原创性声明}\n签名。\n"
            "\\chapter{绪论}\n本研究受占位基金资助（编号虚构）。\n"
            "作者在虚构占位课题组完成本工作。\n\\end{document}\n",
        )
        checker = blind_review.BlindReviewChecker(tex)
        findings = checker.run_check()
        r3 = [f for f in findings if f.rule == "R3"]
        kinds = {f.kind for f in r3}
        assert {"declaration", "funding", "self_ref"} <= kinds
        assert all(f.severity == "INFO" for f in r3)
        assert all("以学校盲审通知为准" in f.message for f in r3)

    def test_pkuthss_keyval_fields_detected(self, tmp_path: Path):
        tex = _mini(
            tmp_path,
            "\\documentclass{pkuthss}\n\\pkuthssinfo{\n"
            "  cauthor = {某作者},\n  cmentor = {某导师},\n}\n"
            "\\begin{document}\n\\chapter{绪论}\n正文。\n\\end{document}\n",
        )
        checker = blind_review.BlindReviewChecker(tex)
        findings = checker.run_check()
        kinds = [f.kind for f in findings if f.action == "AUTO_FIELD"]
        assert "author_field" in kinds
        assert "supervisor_field" in kinds
