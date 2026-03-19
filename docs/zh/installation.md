# 安装

## 前置环境

按你要使用的技能安装对应工具链。

| 领域 | 需要 |
| --- | --- |
| Python | Python 3.8+ 与 `uv` |
| LaTeX 技能 | TeX Live 或 MiKTeX，以及 `latexmk`、`chktex`、`bibtex` 或 `biber` |
| Typst 技能 | `typst-cli` |
| 文档站点 | 若要本地运行文档，需要 Node.js |

本仓库内的 Python 示例命令统一使用 `uv run python ...`。测试统一使用 `uv run python -m pytest ...`。

## 获取仓库

```bash
git clone https://github.com/bahayonghang/academic-writing-skills.git
cd academic-writing-skills
uv sync
```

## 安装技能

推荐方式：直接使用 `npx skills` 安装。

```bash
# 安装单个技能
npx skills add github.com/bahayonghang/academic-writing-skills/latex-paper-en
npx skills add github.com/bahayonghang/academic-writing-skills/latex-thesis-zh
npx skills add github.com/bahayonghang/academic-writing-skills/typst-paper
npx skills add github.com/bahayonghang/academic-writing-skills/paper-audit
npx skills add github.com/bahayonghang/academic-writing-skills/industrial-ai-research

# 或一次性安装全部技能
npx skills add github.com/bahayonghang/academic-writing-skills
```

如果你更偏好手动安装，再将需要的技能目录复制到本地 Claude 技能目录。

常用目录：

- `academic-writing-skills/latex-paper-en`
- `academic-writing-skills/latex-thesis-zh`
- `academic-writing-skills/typst-paper`
- `academic-writing-skills/paper-audit`
- `academic-writing-skills/industrial-ai-research`

### 手动复制示例

```powershell
New-Item -ItemType Directory -Path "$env:USERPROFILE/.claude/skills" -Force
Copy-Item -Recurse "academic-writing-skills/latex-paper-en" "$env:USERPROFILE/.claude/skills/"
Copy-Item -Recurse "academic-writing-skills/latex-thesis-zh" "$env:USERPROFILE/.claude/skills/"
Copy-Item -Recurse "academic-writing-skills/typst-paper" "$env:USERPROFILE/.claude/skills/"
Copy-Item -Recurse "academic-writing-skills/paper-audit" "$env:USERPROFILE/.claude/skills/"
Copy-Item -Recurse "academic-writing-skills/industrial-ai-research" "$env:USERPROFILE/.claude/skills/"
```

如果你的运行时不是 `~/.claude/skills`，把目标路径替换成你的实际技能目录即可。

## 检查工具链

```bash
uv --version
python --version
pdflatex --version
xelatex --version
typst --version
chktex --version
```

## 推荐附加工具

```bash
# macOS
brew install chktex biber typst

# Ubuntu / Debian
sudo apt-get install chktex biber
```

`latexmk` 和大多数 TeX 工具通常已随 TeX 发行版提供。

## 验证仓库环境

在仓库根目录执行：

```bash
uv run ruff check .
uv run pyright
uv run python -m pytest tests/
```

## 本地运行文档站点

```bash
cd docs
npm install
npm run docs:dev
```

## 常见问题

### 找不到 `pdflatex` 或 `xelatex`

先安装 LaTeX 发行版，并确认二进制已加入 `PATH`。

### 找不到 `typst`

安装 `typst-cli`，再确认 `typst --version` 能执行。

### `uv run python` 失败

通常是因为还没在仓库根目录执行 `uv sync`。
