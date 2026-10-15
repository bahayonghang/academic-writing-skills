"""Isolated thesis rebuttal modules and synthetic revision fixtures."""

from __future__ import annotations

import contextlib
import importlib.util
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest

from tests.support.paths import SKILLS_ROOT

SKILL_ROOT = SKILLS_ROOT / "latex-thesis-zh"
SCRIPTS = SKILL_ROOT / "scripts"
FIXTURE_DIR = SKILL_ROOT / "evals" / "fixtures" / "rebuttal" / "mini-thesis"
REBUTTAL_REVIEWS = SKILL_ROOT / "evals" / "fixtures" / "rebuttal" / "reviews"
_SHARED_MODULE_NAMES = ("tex_loader", "rebuttal_common")

# PyMuPDF binds sys.stdout for its messages at first import. Import it here, under
# pytest's session capture, rather than inside a capsys test whose stream closes at teardown.
with contextlib.suppress(ImportError):
    importlib.import_module("pymupdf")


def load_script(name: str) -> ModuleType:
    """Load ``scripts/<name>.py`` in isolation from other skills' modules."""
    saved_path = list(sys.path)
    module_name = f"_thesis_{name}"
    names = (*_SHARED_MODULE_NAMES, module_name)
    saved_modules = {module: sys.modules.pop(module, None) for module in names}
    try:
        sys.path.insert(0, str(SCRIPTS))
        spec = importlib.util.spec_from_file_location(f"_thesis_{name}", SCRIPTS / f"{name}.py")
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = saved_path
        for module, saved in saved_modules.items():
            if saved is None:
                sys.modules.pop(module, None)
            else:
                sys.modules[module] = saved


class _Scripts:
    """Attribute access loads the script of the same name once."""

    def __getattr__(self, name: str) -> ModuleType:
        if name.startswith("_"):
            raise AttributeError(name)
        module = load_script(name)
        setattr(self, name, module)
        return module


_SCRIPTS = _Scripts()


@pytest.fixture
def thesis_rebuttal_scripts() -> _Scripts:
    return _SCRIPTS


REBUTTAL_DOCUMENT_AUX = r"""\relax
\bibcite{zhang2020flow}{{1}{2020}{{Zhang}}{{}}}
\bibcite{li2021graph}{{2}{2021}{{Li}}{{}}}
\bibcite{wang2019survey}{{3}{2019}{{Wang}}{{}}}
\newlabel{chap:c2}{{2}{11}{问题形式化}{chapter.2}{}}
\newlabel{sec:c2-3}{{2.3}{13}{问题形式化}{section.2.3}{}}
\newlabel{chap:c3}{{3}{19}{时空补全方法}{chapter.3}{}}
"""


@pytest.fixture
def rebuttal_thesis(tmp_path: Path) -> Path:
    """Copy of the mini-thesis with a document.aux that adds bibcites and chapter/section labels."""
    root = tmp_path / "thesis"
    shutil.copytree(FIXTURE_DIR, root)
    (root / "document.aux").write_text(REBUTTAL_DOCUMENT_AUX, encoding="utf-8")
    return root


@pytest.fixture
def rebuttal_reviews(tmp_path: Path) -> Path:
    """Copy of the synthetic review reports at ``tmp_path/pre-review/review_results``."""
    reviews = tmp_path / "pre-review" / "review_results"
    shutil.copytree(REBUTTAL_REVIEWS, reviews)
    return reviews


REBUTTAL_DONE_LEDGER = SKILL_ROOT / "evals" / "fixtures" / "rebuttal" / "concerns-done.yaml"
REBUTTAL_NEW_FIGURE = r"""\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.7\textwidth]{chapter2/detectors.png}
  \bicaption{示例检测器布设位置}{Layout of example detectors}
  \label{fig:c2-layout}
\end{figure}
"""
# chapter2.aux after the revision: a new figure 2-1, so the profile figure becomes 2-2
# and every later page moves by one.
REBUTTAL_REVISED_CHAPTER2_AUX = r"""\relax
\newlabel{fig:c2-layout}{{2-1}{12}{示例检测器布设位置}{figure.caption.5}{}}
\newlabel{fig:c2-profile}{{2-2}{13}{示例检测器流量的日变化曲线}{figure.caption.6}{}}
\newlabel{eq:c2-target}{{2-1}{14}{问题形式化}{equation.2.3.1}{}}
\newlabel{eq:c2-objective}{{2-2}{14}{问题形式化}{equation.2.3.2}{}}
\newlabel{fig:c2-framework}{{2-3}{15}{总体研究框架}{figure.caption.7}{}}
"""
REBUTTAL_BIB = """@article{wang2019survey,
  author = {Wang, Example},
  title = {A synthetic survey of traffic prediction},
  journal = {Example Journal},
  year = {2019},
  volume = {3},
  number = {2},
  pages = {10--20},
}
"""


def git(repo: Path, *args: str) -> str:
    identity = ("-c", "user.name=test", "-c", "user.email=test@example.invalid")
    result = subprocess.run(
        ["git", "-C", str(repo), *identity, *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout


def set_aux_newer(thesis: Path) -> None:
    """Make every aux newer than every tex, as after a full compile."""
    base = time.time() - 1000
    for path in thesis.rglob("*.tex"):
        os.utime(path, (base, base))
    for path in thesis.rglob("*.aux"):
        os.utime(path, (base + 100, base + 100))


@pytest.fixture
def rebuttal_case(
    rebuttal_thesis: Path, thesis_rebuttal_scripts: _Scripts, capsys
) -> SimpleNamespace:
    """A submitted thesis in git, the rebuttal root inside it, a revised and recompiled copy.

    Steps: commit the submitted version; copy the reviews to rebuttal/pre-review/ (untracked,
    like the user's layout); run intake; revise chapter 2 (new figure 2-1, one rewritten
    sentence) and the bibliography, update the aux files, commit; install the completed
    ledger; make the aux files newer than the tex files.
    """
    if shutil.which("git") is None:
        pytest.skip("git is not installed")
    thesis = rebuttal_thesis
    git(thesis, "init", "-q")
    git(thesis, "add", "-A")
    git(thesis, "commit", "-q", "-m", "submitted")
    root = thesis / "rebuttal" / "pre-review"
    reviews = root / "review_results"
    shutil.copytree(REBUTTAL_REVIEWS, reviews)
    code = thesis_rebuttal_scripts.rebuttal_intake.main(
        ["--reviews", str(reviews), "--thesis", str(thesis), "--main", "document.tex"]
    )
    assert code == 0
    capsys.readouterr()

    chapter = thesis / "chapters" / "chapter2.tex"
    heading = "\\section{交通流量数据特性分析}\n"
    text = chapter.read_text(encoding="utf-8").replace(heading, heading + REBUTTAL_NEW_FIGURE, 1)
    text = text.replace(
        "预测目标为", "预测函数记为 $f_{\\theta}$，历史窗口长度记为 $T$。预测目标为", 1
    )
    chapter.write_text(text, encoding="utf-8")
    (thesis / "chapters" / "chapter2.aux").write_text(
        REBUTTAL_REVISED_CHAPTER2_AUX, encoding="utf-8"
    )
    (thesis / "document.aux").write_text(
        REBUTTAL_DOCUMENT_AUX.replace("{2.3}{13}", "{2.3}{14}"), encoding="utf-8"
    )
    (thesis / "references.bib").write_text(REBUTTAL_BIB, encoding="utf-8")
    git(thesis, "add", "chapters", "document.aux", "references.bib")
    git(thesis, "commit", "-q", "-m", "revised")

    workspace = root / "workspace"
    shutil.copyfile(REBUTTAL_DONE_LEDGER, workspace / "concerns.yaml")
    set_aux_newer(thesis)
    return SimpleNamespace(root=root, reviews=reviews, thesis=thesis, workspace=workspace)
