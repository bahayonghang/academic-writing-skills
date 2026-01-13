# Claude Code 学术写作 Skills

[English](README.md) | [📚 文档](https://github.com/bahayonghang/academic-writing-skills/tree/main/docs)

> 基于 Claude Code 的 LaTeX 学术写作助手，支持英文论文和中文学位论文。

## 文档

**📖 完整文档请访问 [docs](https://github.com/bahayonghang/academic-writing-skills/tree/main/docs) 目录。**

本地查看文档：

```bash
cd docs
npm install
npm run docs:dev
```

然后在浏览器中打开 http://localhost:5173。

## 功能特性

### latex-paper-en（英文学术论文）
- **格式检查**：集成 ChkTeX 进行 LaTeX 语法检查
- **编译支持**：通过 latexmk 支持 pdfLaTeX/XeLaTeX/LuaLaTeX
- **语法分析**：中式英语检测、弱动词替换建议
- **长难句分析**：复杂句子拆解与重构建议
- **表达优化**：学术语气改进
- **期刊适配**：IEEE、ACM、Springer、NeurIPS、ICML 格式指南

### latex-thesis-zh（中文学位论文）
- **结构映射**：多文件论文结构分析
- **国标检查**：符合 GB/T 7714-2015 参考文献规范
- **模板检测**：支持 thuthesis、pkuthss、ustcthesis、fduthesis 等模板
- **中文学术规范**：口语化表达检测、术语一致性检查
- **编译支持**：XeLaTeX/LuaLaTeX 完整中文支持

## 安装方法

将 skill 文件夹复制到 Claude Code 的 skills 目录：

### Linux / macOS

```bash
# 创建 skills 目录（如不存在）
mkdir -p ~/.claude/skills

# 复制 skill 文件夹
cp -r .claude/skills/latex-paper-en ~/.claude/skills/
cp -r .claude/skills/latex-thesis-zh ~/.claude/skills/
```

### Windows (PowerShell)

```powershell
# 创建 skills 目录（如不存在）
New-Item -ItemType Directory -Path "$env:USERPROFILE/.claude/skills" -Force

# 复制 skill 文件夹
Copy-Item -Recurse ".claude/skills/latex-paper-en" "$env:USERPROFILE/.claude/skills/"
Copy-Item -Recurse ".claude/skills/latex-thesis-zh" "$env:USERPROFILE/.claude/skills/"
```

### Windows (CMD)

```cmd
:: 创建 skills 目录（如不存在）
mkdir "%USERPROFILE%\.claude\skills"

:: 复制 skill 文件夹
xcopy /E /I ".claude\skills\latex-paper-en" "%USERPROFILE%\.claude\skills\latex-paper-en"
xcopy /E /I ".claude\skills\latex-thesis-zh" "%USERPROFILE%\.claude\skills\latex-thesis-zh"
```

## 快速开始

### 编译文档

```bash
# 自动检测编译器
python scripts/compile.py main.tex

# 使用指定配方（VS Code LaTeX Workshop 风格）
python scripts/compile.py main.tex --recipe xelatex-biber    # 中文论文推荐
python scripts/compile.py main.tex --recipe pdflatex-biber   # 英文论文推荐

# 监视模式（持续编译）
python scripts/compile.py main.tex --watch
```

### 编译配置

| 配置 | 步骤 | 适用场景 |
|------|------|----------|
| `xelatex` | 仅 XeLaTeX | 中文快速编译 |
| `pdflatex` | 仅 PDFLaTeX | 英文快速编译 |
| `latexmk` | LaTeXmk 自动 | 自动处理依赖 |
| `xelatex-bibtex` | xelatex → bibtex → xelatex×2 | 中文 + BibTeX |
| `xelatex-biber` | xelatex → biber → xelatex×2 | 中文 + Biber（推荐）|
| `pdflatex-bibtex` | pdflatex → bibtex → pdflatex×2 | 英文 + BibTeX |
| `pdflatex-biber` | pdflatex → biber → pdflatex×2 | 英文 + Biber |

### 其他工具

```bash
# 格式检查
python scripts/check_format.py main.tex

# BibTeX 验证
python scripts/verify_bib.py references.bib

# 论文结构映射（仅中文论文）
python scripts/map_structure.py main.tex

# 术语一致性检查（仅中文论文）
python scripts/check_consistency.py main.tex
```

## 项目结构

```
academic-writing-skills/
├── .claude/
│   └── skills/
│       ├── latex-paper-en/           # 英文论文 skill
│       │   ├── SKILL.md              # Skill 定义
│       │   ├── scripts/              # Python 工具
│       │   │   ├── compile.py        # 统一编译器
│       │   │   ├── check_format.py   # ChkTeX 包装器
│       │   │   ├── verify_bib.py     # BibTeX 检查器
│       │   │   └── extract_prose.py  # 文本提取器
│       │   └── references/           # 参考文档
│       │       ├── STYLE_GUIDE.md    # 写作风格指南
│       │       ├── COMMON_ERRORS.md  # 常见错误
│       │       ├── VENUES.md         # 期刊/会议规则
│       │       └── ...
│       │
│       └── latex-thesis-zh/          # 中文论文 skill
│           ├── SKILL.md
│           ├── scripts/
│           │   ├── compile.py
│           │   ├── map_structure.py  # 论文结构映射
│           │   ├── check_format.py
│           │   └── check_consistency.py
│           └── references/
│               ├── GB_STANDARD.md    # 国标格式规范
│               ├── ACADEMIC_STYLE_ZH.md  # 中文学术规范
│               ├── STRUCTURE_GUIDE.md    # 结构指南
│               └── UNIVERSITIES/     # 学校模板
│                   ├── tsinghua.md   # 清华大学
│                   ├── pku.md        # 北京大学
│                   └── generic.md    # 通用模板
│
├── docs/                             # 文档站点
│
└── dist/                             # 打包的 skills
    ├── latex-paper-en.skill.zip
    └── latex-thesis-zh.skill.zip
```

## 系统要求

- Python 3.8+
- TeX Live 或 MiKTeX（需包含 latexmk、chktex）
- 中文文档需要：XeLaTeX 及中文字体（SimSun、SimHei、KaiTi）

## 支持的学校模板

| 学校 | 模板名称 | 特殊要求 |
|------|----------|----------|
| 清华大学 | thuthesis | 图表编号格式：图 3-1 |
| 北京大学 | pkuthss | 需包含符号说明章节 |
| 中国科学技术大学 | ustcthesis | - |
| 复旦大学 | fduthesis | - |
| 通用 | ctexbook | 遵循 GB/T 7713.1-2006 |

## 工作流程

### 英文论文审查流程

1. **Layer 0**：格式预检（ChkTeX + BibTeX 验证）
2. **Layer 1**：语法分析（只读模式）
3. **Layer 2**：长难句拆解
4. **Layer 3**：表达重构（注释形式输出）

### 中文论文审查流程

1. **Layer 0**：结构映射（必须首先执行）
2. **Layer 1**：结构完整性检查
3. **Layer 2**：国标格式审查（GB/T 7714）
4. **Layer 3**：中文学术表达检查
5. **Layer 4**：长难句拆解
6. **Layer 5**：表述重构

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
