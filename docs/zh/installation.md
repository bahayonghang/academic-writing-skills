# 安装

有两条路径。两条路径分开使用。

1. 维护本开发仓库（clone、`uv`、测试、文档站）。
2. 把技能安装进论文项目（复制或 `npx skills add`）。

新 clone 通过已跟踪的 `AGENTS.md` 与 `CLAUDE.md` 加载共同维护规则。Claude Code 用 `@AGENTS.md` 导入 `AGENTS.md`。其他工具通过原生发现加载 `AGENTS.md`，或在会话中打开 `AGENTS.md`。不要依赖被忽略的 `.claude/`、`.codex/`、`.agents/`、`.cursor/`、`.grok/`、`.kimi-code/`、`.omp/` 目录、私有绝对路径或隐含全局 hook。各工具入口、加载、委派与权限差异见[工具接入](/zh/harnesses)。

## 环境要求

只安装你实际使用的技能所需工具链。

| 领域 | 要求 |
| --- | --- |
| 仓库 Python | Python 3.10+ 与 `uv` |
| LaTeX 技能 | TeX Live 或 MiKTeX；`latexmk`、BibTeX/Biber 和可选 `chktex` |
| Typst 技能 | Typst CLI |
| 文档站 | Node.js 与 npm |

## 路径 1：维护本开发仓库

```bash
git clone https://github.com/bahayonghang/academic-writing-skills.git
cd academic-writing-skills
uv sync --extra dev
```

贡献者测试使用统一 pytest 入口：

```bash
just test
```

`just test` 运行 `uv run --extra dev python -m pytest`。该命令与直接执行 `uv run --extra dev python -m pytest` 使用同一份 pytest 配置（`testpaths` 覆盖 `tests/` 与 `academic-writing-skills/`）。历史上根目录 `uv run pytest` 曾漏掉 `bib-search-citation` 包内 42 项测试。

完整 Python 门禁：

```bash
just ci
```

`just ci` 共四步：`just check-versions`、`just lint`、`just typecheck`、`just test`。

文档资源门禁（不属于 `just ci`）：

```bash
uv run --extra dev python docs/scripts/check_resource_sync.py
```

把七个 catalog 技能安装进本 clone（或其他项目）的 agent 技能目录，使用本地安装器。这是面向本仓库 clone 的维护者辅助命令。它不替代 `npx skills add`，也不验证 `npx` 安装器、符号链接布局或五套工具运行时发现。

```bash
just skills-install
just skills-install latex-paper-en paper-audit
just -- skills-install --list
just -- skills-install --agent cursor --copy -y
just -- skills-install --dest path/to/manuscript --all
```

`just` 会把以 `-` 开头的参数当成自己的 flag，因此 GNU 风格选项需写成 `just -- skills-install ...`。目标目录为 `.claude/skills`、`.cursor/skills`、`.agents/skills`、`.grok/skills`、`.kimi-code/skills`、`.omp/skills`。Windows 默认 copy，其他平台默认 symlink。这些目录在本开发仓库中被 gitignore。

## 路径 2：把技能安装进论文项目

使用 `npx skills` 安装单个技能或完整集合：

```bash
npx skills add bahayonghang/academic-writing-skills/cover-letter
npx skills add bahayonghang/academic-writing-skills/paper-audit
npx skills add bahayonghang/academic-writing-skills/latex-paper-en
npx skills add bahayonghang/academic-writing-skills/latex-thesis-zh
npx skills add bahayonghang/academic-writing-skills/typst-paper
npx skills add bahayonghang/academic-writing-skills/bib-search-citation
npx skills add bahayonghang/academic-writing-skills/paper-writing-studio
npx skills add bahayonghang/academic-writing-skills/latex-defense-zh

# 安装全部七个技能
npx skills add bahayonghang/academic-writing-skills
```

八条 `npx skills add bahayonghang/academic-writing-skills/<skill>` 命令字符串是文档中的安装器界面。`npx` 安装器、安装器可能创建的符号链接布局、以及五套工具运行时发现均保持 **UNVERIFIED**。本轮没有已授权的真实运行记录。

手动安装时，将 `academic-writing-skills/` 下所需技能的完整目录复制到 agent runtime 使用的技能目录。复制完整技能目录。每个技能都依赖本地 scripts、references、templates、examples 与 metadata。若当前工具没有自动加载该技能，打开该技能的 `SKILL.md`，再打开被路由到的 `references/` 文件。

### paper-audit 同级布局 {#paper-audit-layout}

完整的 `paper-audit` `.tex` / `.typ` 脚本检查，从 `paper-audit/` 的父目录解析同级写作技能：

```text
<parent>/
├── cover-letter/
├── paper-audit/
├── latex-paper-en/
├── latex-thesis-zh/
├── typst-paper/
├── bib-search-citation/
└── paper-writing-studio/
```

`audit.py` 在 `paper-audit/` 旁边查找 `latex-paper-en/scripts`、`latex-thesis-zh/scripts`、`typst-paper/scripts`。推荐完整集合：全部七个技能目录作为同级目录。

仅复制 `paper-audit` 时为**覆盖受限**。缺失的同级脚本会被跳过。现有 exit 与 gate 语义保持不变。对 `tests/fixtures/paper_audit/sample_paper.tex` 的已记录隔离探针（`quick-audit --lang en --format json`）：单独安装 RUN=3，missing=8，exit 0。推荐完整同级布局：missing=0。

不要把同级技能的 scripts 复制进 `paper-audit/`。

## 验证环境

```bash
uv --version
python --version
latexmk --version
xelatex --version
typst --version
```

## 运行文档站

维护者命令：

```bash
just docs
```

直接使用 Node 的等价命令：

```bash
npm --prefix docs install
npm --prefix docs run docs:dev
```

生产构建：`just doc-build`，或 `npm --prefix docs run docs:build`。

## 常见问题

### 安装器显示安全告警 {#security-assessments}

`Gen`、`Socket`、`Snyk` 分别显示独立评估。一个供应商的通过结果不能消除另一个
供应商的告警。仅凭告警数量不能判断安装失败，应同时检查安装结果和退出码。

打开链接中的技能页，再进入供应商详情页。记录技能、受影响文件、发现内容、扫描日期
和包标识，并与实际安装版本核对。源码修改不能证明供应商已扫描新包；新扫描尚未
取得时，将扫描状态记为 pending。本地行为测试、安装验证、发布和供应商扫描分别记录。

Socket 对 `latex-thesis-zh` 和 `latex-defense-zh` 的告警指出 include 路径可能读取
项目根目录外的文件。下述 loader 边界处理这一行为，覆盖五个 LaTeX loader 副本：
`latex-paper-en`、`latex-thesis-zh`、`paper-audit`、`cover-letter` 和
`latex-defense-zh`。零告警标记不能代替行为测试。

### loader 报告 `E-INCLUDE-BOUNDARY` {#include-boundary}

默认行为已变化：项目根目录外的 LaTeX include 会在目标读取前终止加载。默认根目录为
解析后的入口文件父目录。检查覆盖 `input`、`include`、`subfile` 及符号链接。
包含 `..` 的相对路径和绝对路径，只要解析后的目标仍在根目录内，就继续有效。

核对错误中的源文件和行号。使用正确的主文件，或将 include 路径修正为所选项目内的
目标。不要自动扩大根目录，也不要把无关私有文件复制进项目。嵌套主文件的调用方可
向 `assemble` 或 `iter_files` 明确传入 `project_root`；答辩提取使用已选择的
`--thesis` 目录。其他命令行工具不会因此新增 `--project-root` 参数。

无效或越界的 include 会使当前操作失败。路径位于根目录内的缺失文件沿用原有缺失
诊断。检查不修改论文文件。include 边界不构成 TeX 执行沙箱，也不保证防护并发链接替换。

### 缺少 TeX 或 Typst 可执行文件

安装对应工具链，并确认可执行文件位于 `PATH`。Python 依赖不会安装 TeX 或 Typst。

### `uv run python` 无法解析环境

在仓库根目录运行 `uv sync --extra dev`，然后重试。

### 技能能打开，但引用文件缺失

重新安装或复制完整技能目录。技能入口会按需加载包内详细资源。

### `paper-audit` 打印 `script not found`

`paper-audit` 目录旁边没有同级写作技能目录。安装[推荐的完整同级布局](#paper-audit-layout)。单技能复制属于覆盖受限。
