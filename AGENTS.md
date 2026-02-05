# AGENTS.md

本仓库是 Claude Code 学术写作技能包，面向 LaTeX 与 Typst 的英文论文与中文学位论文场景。

**核心目录**
- `academic-writing-skills/latex-paper-en/`
- `academic-writing-skills/latex-thesis-zh/`
- `academic-writing-skills/typst-paper/`
- `docs/`
- `tests/`

**入口与规范**
- 每个技能以 `SKILL.md` 作为入口与规范定义
- 工具脚本位于 `scripts/`
- 参考资料位于 `references/`

**技能能力概览**
- `latex-paper-en`: 编译、格式检查、参考文献校验、语法与表达分析、去 AI 化、标题优化、图表检查
- `latex-thesis-zh`: 编译、格式检查、论文结构映射、引用一致性、模板检测、去 AI 化、标题优化
- `typst-paper`: 编译、格式检查、参考文献校验、去 AI 化、标题优化

**脚本分布（按技能）**
- `latex-paper-en/scripts`: `compile.py`、`check_format.py`、`verify_bib.py`、`extract_prose.py`、`deai_check.py`、`deai_batch.py`、`optimize_title.py`、`check_figures.py`、`parsers.py`
- `latex-thesis-zh/scripts`: `compile.py`、`check_format.py`、`map_structure.py`、`check_consistency.py`、`detect_template.py`、`verify_bib.py`、`deai_check.py`、`deai_batch.py`、`optimize_title.py`、`parsers.py`
- `typst-paper/scripts`: `compile.py`、`check_format.py`、`verify_bib.py`、`deai_check.py`、`deai_batch.py`、`optimize_title.py`、`parsers.py`

**文档与测试**
- 文档站点：`docs/`（VitePress）
- 单元测试：`tests/test_parsers.py`

**依赖与工具链（摘要）**
- Python 3.8+，使用 `uv` 管理依赖
- LaTeX 工具链：TeX Live 或 MiKTeX，`latexmk`、`chktex`、`bibtex`/`biber`
- Typst：`typst-cli`

**常用命令**
```bash
uv sync
ruff check .
ruff format .
pyright
python -m pytest tests/

cd docs
npm install
npm run docs:dev
```
