# 安装

## 环境要求

只安装你实际使用的技能所需工具链。

| 领域 | 要求 |
| --- | --- |
| 仓库 Python | Python 3.10+ 与 `uv` |
| LaTeX 技能 | TeX Live 或 MiKTeX；`latexmk`、BibTeX/Biber 和可选 `chktex` |
| Typst 技能 | Typst CLI |
| 文档站 | Node.js 与 npm |

## 获取并安装仓库

```bash
git clone https://github.com/bahayonghang/academic-writing-skills.git
cd academic-writing-skills
uv sync --extra dev
```

## 安装技能

使用 `npx skills` 安装单个技能或完整集合：

```bash
npx skills add bahayonghang/academic-writing-skills/cover-letter
npx skills add bahayonghang/academic-writing-skills/paper-audit
npx skills add bahayonghang/academic-writing-skills/latex-paper-en
npx skills add bahayonghang/academic-writing-skills/latex-thesis-zh
npx skills add bahayonghang/academic-writing-skills/typst-paper
npx skills add bahayonghang/academic-writing-skills/bib-search-citation

# 安装全部六个技能
npx skills add bahayonghang/academic-writing-skills
```

手动安装时，将 `academic-writing-skills/` 下所需技能的完整目录复制到 agent runtime
使用的技能目录。不要只复制 `SKILL.md`；每个技能都依赖本地 scripts、references、
templates、examples 与 metadata。

## 验证环境

```bash
uv --version
python --version
latexmk --version
xelatex --version
typst --version
```

在仓库根目录运行质量门禁：

```bash
uv run ruff format --check .
uv run ruff check .
uv run pyright
uv run pytest
```

## 运行文档站

```bash
npm --prefix docs install
npm --prefix docs run docs:dev
```

生产构建使用 `npm --prefix docs run docs:build`。

## 常见问题

### 缺少 TeX 或 Typst 可执行文件

安装对应工具链，并确认可执行文件位于 `PATH`。Python 依赖不会安装 TeX 或 Typst。

### `uv run python` 无法解析环境

在仓库根目录运行 `uv sync --extra dev`，然后重试。

### 技能能打开，但引用文件缺失

重新安装或复制完整技能目录。技能入口会按需加载包内详细资源。
