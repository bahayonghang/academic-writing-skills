# 快速开始

几分钟内开始使用 Academic Writing Skills。

## 安装

将 skill 文件夹复制到 Claude Code 的 skills 目录：

### Linux / macOS

```bash
mkdir -p ~/.claude/skills
cp -r .claude/skills/latex-paper-en ~/.claude/skills/
cp -r .claude/skills/latex-thesis-zh ~/.claude/skills/
```

### Windows (PowerShell)

```powershell
New-Item -ItemType Directory -Path "$env:USERPROFILE/.claude/skills" -Force
Copy-Item -Recurse ".claude/skills/latex-paper-en" "$env:USERPROFILE/.claude/skills/"
Copy-Item -Recurse ".claude/skills/latex-thesis-zh" "$env:USERPROFILE/.claude/skills/"
```

## 第一次编译

### 英文论文

1. **在 Claude Code 中打开您的 LaTeX 项目**
2. **编译论文**：
   ```bash
   # 使用 pdfLaTeX 简单编译
   python ~/.claude/skills/latex-paper-en/scripts/compile.py main.tex

   # 或使用 XeLaTeX
   python ~/.claude/skills/latex-paper-en/scripts/compile.py main.tex --recipe xelatex

   # 包含参考文献的完整工作流
   python ~/.claude/skills/latex-paper-en/scripts/compile.py main.tex --recipe pdflatex-bibtex
   ```

3. **检查格式**：
   ```bash
   python ~/.claude/skills/latex-paper-en/scripts/check_format.py main.tex
   ```

### 中文论文

1. **在 Claude Code 中打开您的 LaTeX 项目**
2. **映射论文结构**：
   ```bash
   python ~/.claude/skills/latex-thesis-zh/scripts/map_structure.py main.tex
   ```

3. **使用 XeLaTeX 编译**：
   ```bash
   python ~/.claude/skills/latex-thesis-zh/scripts/compile.py main.tex --recipe xelatex-biber
   ```

4. **检查 GB/T 7714 合规性**：
   ```bash
   python ~/.claude/skills/latex-thesis-zh/scripts/verify_bib.py references.bib
   ```

## 常见工作流

### 工作流 1：快速论文草稿

适合快速迭代：

```bash
# 使用 pdfLaTeX 编译（最快）
python ~/.claude/skills/latex-paper-en/scripts/compile.py paper.tex --recipe pdflatex

# 检查常见错误
python ~/.claude/skills/latex-paper-en/scripts/check_format.py paper.tex
```

### 工作流 2：最终提交

用于发表就绪的输出：

```bash
# 包含参考文献的完整编译
python ~/.claude/skills/latex-paper-en/scripts/compile.py paper.tex --recipe pdflatex-biber

# 格式检查
python ~/.claude/skills/latex-paper-en/scripts/check_format.py paper.tex

# 参考文献验证
python ~/.claude/skills/latex-paper-en/scripts/verify_bib.py references.bib
```

### 工作流 3：中文论文

完整的论文工作流：

```bash
# 1. 映射结构（识别模板和章节）
python ~/.claude/skills/latex-thesis-zh/scripts/map_structure.py thesis.tex

# 2. 使用 XeLaTeX 和 Biber 编译
python ~/.claude/skills/latex-thesis-zh/scripts/compile.py thesis.tex --recipe xelatex-biber

# 3. 检查 GB/T 7714 合规性
python ~/.claude/skills/latex-thesis-zh/scripts/verify_bib.py refs.bib

# 4. 检查术语一致性
python ~/.claude/skills/latex-thesis-zh/scripts/check_consistency.py data/
```

## 理解编译配方

Academic Writing Skills 支持多种编译配方：

| 配方 | 使用场景 | 速度 |
|------|----------|------|
| `pdflatex` | 纯英文论文，最快 | ⚡⚡⚡ |
| `xelatex` | Unicode、中文、自定义字体 | ⚡⚡ |
| `latexmk` | 自动依赖处理 | ⚡ |
| `pdflatex-bibtex` | 英文 + BibTeX 参考文献 | ⚡⚡ |
| `xelatex-biber` | 中文 + 现代参考文献 | ⚡ |

根据需求选择：
- **速度**：pdflatex
- **Unicode/中文**：xelatex 或 lualatex
- **现代参考文献**：biber
- **自动依赖**：latexmk

## 与 Claude Code 协作

### 交互模式

在 Claude Code 中交互式使用技能：

```
您：使用 XeLaTeX 编译我的论文并检查格式错误

Claude：我将使用 xelatex 配方编译您的论文并运行格式检查。

[运行编译和格式检查]

Claude：编译成功！发现 3 个小格式问题：
1. 第 42 行：\cite 命令间距
2. 第 87 行：章节标题大小写不一致
3. 第 120 行：句号后缺少空格
```

### 自动化工作流

为常见任务创建自动化工作流：

```bash
# 创建编译脚本
cat > compile_all.sh << 'EOF'
#!/bin/bash
echo "正在编译论文..."
python ~/.claude/skills/latex-paper-en/scripts/compile.py paper.tex --recipe pdflatex-biber

echo "正在检查格式..."
python ~/.claude/skills/latex-paper-en/scripts/check_format.py paper.tex

echo "正在验证参考文献..."
python ~/.claude/skills/latex-paper-en/scripts/verify_bib.py references.bib

echo "完成！"
EOF

chmod +x compile_all.sh
./compile_all.sh
```

## 成功技巧

### 1. 使用正确的配方

**英文论文**：
- 从 `pdflatex` 开始以获得速度
- 如果需要 Unicode 字符，切换到 `xelatex`

**中文论文**：
- 始终使用 `xelatex` 或 `lualatex`
- 使用 `biber` 进行现代参考文献（GB/T 7714）

### 2. 经常检查

频繁运行格式检查以尽早发现问题：

```bash
# 快速格式检查（快速）
python ~/.claude/skills/latex-paper-en/scripts/check_format.py paper.tex --quick

# 完整格式检查（彻底）
python ~/.claude/skills/latex-paper-en/scripts/check_format.py paper.tex
```

### 3. 了解您的模板

对于中文论文，首先映射结构：

```bash
python ~/.claude/skills/latex-thesis-zh/scripts/map_structure.py thesis.tex
```

这有助于识别：
- 大学模板（清华、北大、中科大、复旦、通用）
- 主文件和章节结构
- 必需与可选组件

### 4. 保持参考文献整洁

在最终提交前验证参考文献格式：

```bash
# 检查 BibTeX 格式
python ~/.claude/skills/latex-paper-en/scripts/verify_bib.py references.bib

# 检查 GB/T 7714 合规性（中文）
python ~/.claude/skills/latex-thesis-zh/scripts/verify_bib.py references.bib --standard gbt7714
```

## 常见问题

### 编译失败

**错误**：`! LaTeX Error: File 'xxx.sty' not found`

**解决方案**：安装缺失的包：
```bash
# TeX Live
tlmgr install <package-name>

# MiKTeX
mpm --install=<package-name>
```

### 参考文献未显示

**错误**：参考文献部分为空

**解决方案**：使用正确的完整配方：
```bash
# 对于 BibTeX
python compile.py paper.tex --recipe pdflatex-bibtex

# 对于 Biber
python compile.py paper.tex --recipe xelatex-biber
```

### 中文字符未显示

**错误**：中文文本显示为方框或错误

**解决方案**：使用 XeLaTeX 或 LuaLaTeX：
```bash
python compile.py thesis.tex --recipe xelatex
```

## 下一步

- [完整使用指南](/zh/usage) - 详细功能文档
- [编译配方](/zh/guides/compilation) - 深入了解配方
- [格式检查](/zh/guides/format-checking) - 理解格式检查
- [参考文献管理](/zh/guides/bibliography) - 管理参考文献

## 需要帮助？

- **文档**：浏览技能特定指南
- **示例**：查看 `.claude/skills/*/references/` 获取示例
- **问题**：[GitHub Issues](https://github.com/bahayonghang/academic-writing-skills/issues)
