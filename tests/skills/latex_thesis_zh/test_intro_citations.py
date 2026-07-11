"""Intro citation diagnostics (B1~B5) for the latex-thesis-zh copy of
analyze_literature.py.

The zh copy is loaded by file path via importlib — a bare
``import analyze_literature`` resolves to the latex-paper-en copy on sys.path
(see conftest), which has no ``analyze_intro_citations`` and would silently
test the wrong object.
"""

import importlib.util
import sys
from pathlib import Path

from tests.support.paths import SCRIPT_DIR_ZH

_ZH_DIR = SCRIPT_DIR_ZH
_SHARED_MODULE_NAMES = ("parsers", "tex_loader")


def _load_zh(name: str):
    """Load a zh scripts module by file path, isolated from other skills'
    cached ``parsers`` / ``tex_loader`` modules (canonical loader pattern,
    see test_deai_tense_zh.py)."""
    path = _ZH_DIR / f"{name}.py"
    saved_path = list(sys.path)
    saved_modules = {n: sys.modules.pop(n, None) for n in _SHARED_MODULE_NAMES}
    try:
        sys.path.insert(0, str(_ZH_DIR))
        spec = importlib.util.spec_from_file_location(f"zh_{name}", path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = saved_path
        for n, mod in saved_modules.items():
            if mod is not None:
                sys.modules[n] = mod
            else:
                sys.modules.pop(n, None)


lit = _load_zh("analyze_literature")

# Synthetic intro fixture (desensitized equivalent of the real bad chapter1):
# stacked cites, one same-prefix cluster, no summary table/figure.
_INTRO_TEX = r"""\chapter{绪论}

智能制造正在快速发展，生产数据规模持续增长。本文围绕数据驱动的运行优化展开研究。

\section{研究背景与意义}

过程工业面临质量波动难题\cite{sunEnergy2018}，已有综述总结了主要路线\cite{gaoReview2016}。

\section{国内外研究现状}

深度建模研究众多\cite{wangDeep2018,wangDeep2019,wangDeep2020}。
时序预测方法持续演进\cite{liuSeq2021,chenAttn2022,zhouSparse2021}。
近期出现了新的融合思路\cite{kimFusion2024}。

\section{论文组织结构}

全文共分五章，各章依次递进。
"""

_BIB_OLD_HEAVY = "\n".join(
    f"@article{{{key},\n  title = {{T{idx}}},\n  year = {{{year}}},\n}}"
    for idx, (key, year) in enumerate(
        [
            ("sunEnergy2018", 2018),
            ("gaoReview2016", 2016),
            ("wangDeep2018", 2018),
            ("wangDeep2019", 2019),
            ("wangDeep2020", 2020),
            ("liuSeq2021", 2021),
            ("chenAttn2022", 2022),
            ("zhouSparse2021", 2021),
            ("kimFusion2024", 2024),
        ]
    )
)


def _write(tmp_path: Path, tex: str = _INTRO_TEX, bib: str | None = None):
    tex_file = tmp_path / "intro.tex"
    tex_file.write_text(tex, encoding="utf-8")
    bib_file = None
    if bib is not None:
        bib_file = tmp_path / "refs.bib"
        bib_file.write_text(bib, encoding="utf-8")
    return tex_file, bib_file


def _run(tmp_path: Path, **kwargs) -> str:
    tex_file, bib_file = _write(tmp_path, bib=kwargs.pop("bib", None))
    return "\n".join(lit.analyze_intro_citations(tex_file, bib_path=bib_file, **kwargs))


def test_loads_the_zh_copy_not_the_en_copy() -> None:
    # Guards the importlib path-load: only the zh copy ships intro diagnostics.
    assert hasattr(lit, "analyze_intro_citations")
    assert hasattr(lit, "author_prefix")


def test_author_prefix_normalization() -> None:
    # lowercase-first keys take the leading lowercase run
    assert lit.author_prefix("zhaoOnlineCementClinker2021") == "zhao"
    assert lit.author_prefix("kadlec2009data") == "kadlec"
    # surname + year keys take the first camel segment
    assert lit.author_prefix("Zhang2021CementTransition") == "zhang"
    assert lit.author_prefix("Ha2018WorldModels") == "ha"
    # pinyin full-name camel keys take the first two segments
    assert lit.author_prefix("ChaiTianYouFuZaGongYe2008") == "chaitian"
    # given-name segment followed by a year falls back to the surname
    assert lit.author_prefix("LiuHui2010JinanSoftSensor") == "liu"


def test_a4_below_minimum_flags_major(tmp_path: Path) -> None:
    report = _run(tmp_path, min_cites=20, max_cites=30)
    assert "B1 引用数量不足" in report
    assert "[Severity: Major]" in report


def test_a4_within_range_reports_info(tmp_path: Path) -> None:
    report = _run(tmp_path, min_cites=5, max_cites=30)
    assert "处于基准区间" in report
    assert "B1 引用数量不足" not in report


def test_a5_stacked_cites_detected(tmp_path: Path) -> None:
    report = _run(tmp_path, min_cites=5)
    assert "B2 检测到 2 处单点堆引" in report


def test_a6_same_prefix_cluster_detected(tmp_path: Path) -> None:
    report = _run(tmp_path, min_cites=5)
    assert "前缀“wang”文献 3 篇" in report
    assert "整簇共引" in report  # all three wangDeep* sit in one \cite


def test_a7_old_heavy_bib_flags_recency(tmp_path: Path) -> None:
    report = _run(tmp_path, min_cites=5, bib=_BIB_OLD_HEAVY, current_year=2026)
    # 2026 baseline: recent-3 = 2024+ -> only kimFusion2024 (1/9), below 30%.
    assert "B4 年份分布" in report
    assert "B4 近期文献占比不足" in report


def test_a7_recent_bib_passes(tmp_path: Path) -> None:
    recent_bib = (
        _BIB_OLD_HEAVY.replace("2016", "2024")
        .replace("2018", "2025")
        .replace("2019", "2024")
        .replace("2020", "2025")
        .replace("2021", "2024")
        .replace("2022", "2025")
    )
    report = _run(tmp_path, min_cites=5, bib=recent_bib, current_year=2026)
    assert "B4 年份分布" in report
    assert "B4 近期文献占比不足" not in report


def test_a7_without_bib_downgrades_to_hint(tmp_path: Path) -> None:
    report = _run(tmp_path, min_cites=5)
    assert "未提供 --bib" in report
    assert "近期文献占比不足" not in report


def test_a8_missing_visual_summary_flagged(tmp_path: Path) -> None:
    report = _run(tmp_path, min_cites=5)
    assert "B5 研究现状范围内未发现总结性表格或图示" in report


def test_a8_silent_when_table_present(tmp_path: Path) -> None:
    tex = _INTRO_TEX.replace(
        "\\section{论文组织结构}",
        "\\begin{table}\n\\begin{tabular}{ll}\n方法 & 局限 \\\\\n\\end{tabular}\n"
        "\\end{table}\n\n\\section{论文组织结构}",
    )
    tex_file, _ = _write(tmp_path, tex=tex)
    report = "\n".join(lit.analyze_intro_citations(tex_file, min_cites=5))
    assert "B5" not in report


def test_bib_year_parsing_handles_biblatex_date() -> None:
    years = lit.parse_bib_years(
        "@article{a2024x,\n  date = {2024-06-01},\n}\n"
        "@article{b2020y,\n  year = 2020,\n}\n"
        "@string{venue = {SomeConf}}\n"
    )
    assert years == {"a2024x": 2024, "b2020y": 2020}
