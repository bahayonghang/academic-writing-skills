# 安装

## 前置要求

在安装 Academic Writing Skills 之前，请确保您已安装：

1. **Claude Code CLI**：Claude Code 官方命令行界面
2. **LaTeX 发行版**：可用的 LaTeX 安装
   - **macOS**：[MacTeX](https://www.tug.org/mactex/)
   - **Windows**：[MiKTeX](https://miktex.org/) 或 [TeX Live](https://www.tug.org/texlive/)
   - **Linux**：TeX Live（通过包管理器）
3. **Python 3.6+**：技能脚本所需

### 验证前置要求

```bash
# 检查 Claude Code
claude --version

# 检查 LaTeX
pdflatex --version
xelatex --version

# 检查 Python
python --version  # 或 python3 --version
```

## 安装方法

1. **克隆仓库**：
   ```bash
   git clone https://github.com/bahayonghang/academic-writing-skills.git
   cd academic-writing-skills
   ```

2. **将技能复制到 Claude Code 的技能目录**：

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

## 验证安装

安装后，通过检查目录验证技能是否可用：

```bash
# Linux / macOS
ls ~/.claude/skills/

# Windows (PowerShell)
Get-ChildItem "$env:USERPROFILE/.claude/skills"

# 您应该看到：
# - latex-paper-en
# - latex-thesis-zh
```

## 安装可选依赖

### ChkTeX（推荐）

ChkTeX 提供 LaTeX 格式检查：

```bash
# macOS（通过 Homebrew）
brew install chktex

# Ubuntu/Debian
sudo apt-get install chktex

# Windows（通过 MiKTeX）
mpm --install=chktex
```

### latexmk（推荐）

latexmk 自动化 LaTeX 编译并处理依赖：

```bash
# 通常包含在 TeX Live/MacTeX 中
# 如果不可用：

# macOS（通过 Homebrew）
brew install latexmk

# Ubuntu/Debian
sudo apt-get install latexmk

# Windows
# 包含在 MiKTeX 和 TeX Live 中
```

### Biber（用于现代参考文献）

Biber 是现代 BibLaTeX 后端：

```bash
# 通常包含在 TeX Live/MacTeX 中
# 如果不可用：

# macOS（通过 Homebrew）
brew install biber

# Ubuntu/Debian
sudo apt-get install biber

# Windows
# 包含在 MiKTeX 和 TeX Live 中
```

## 配置

### LaTeX 编译器优先级

技能将自动检测并按以下顺序使用可用的编译器：

**对于英文论文（latex-paper-en）**：
1. pdfLaTeX（推荐用于纯英文论文）
2. XeLaTeX（用于 Unicode/国际字符）
3. LuaLaTeX（XeLaTeX 的替代方案）

**对于中文论文（latex-thesis-zh）**：
1. XeLaTeX（推荐用于中文文档）
2. LuaLaTeX（中文的替代方案）
3. pdfLaTeX（不推荐用于中文）

### 自定义配置

您可以通过编辑技能文件来自定义技能行为：

```bash
# 编辑英文论文技能配置
nano ~/.claude/skills/latex-paper-en/SKILL.md

# 编辑中文论文技能配置
nano ~/.claude/skills/latex-thesis-zh/SKILL.md
```

## 更新

更新到最新版本，重新克隆仓库并再次复制 skill 文件夹：

```bash
git clone https://github.com/bahayonghang/academic-writing-skills.git
cd academic-writing-skills

# 然后使用上面对应平台的命令复制 skills
```

## 卸载

移除技能：

### Linux / macOS

```bash
rm -rf ~/.claude/skills/latex-paper-en
rm -rf ~/.claude/skills/latex-thesis-zh
```

### Windows (PowerShell)

```powershell
Remove-Item -Recurse -Force "$env:USERPROFILE/.claude/skills/latex-paper-en"
Remove-Item -Recurse -Force "$env:USERPROFILE/.claude/skills/latex-thesis-zh"
```

## 故障排除

### "Skill not found" 错误

**问题**：`claude skill install` 失败，提示 "skill not found"

**解决方案**：
1. 验证您的网络连接
2. 检查 GitHub URL 是否正确
3. 尝试手动下载 `.skill.zip` 文件并本地安装

### "LaTeX not found" 错误

**问题**：编译失败，提示 "command not found: pdflatex"

**解决方案**：
1. 验证 LaTeX 已安装：`which pdflatex`
2. 将 LaTeX 添加到 PATH：
   ```bash
   # macOS（MacTeX）
   export PATH="/usr/local/texlive/2024/bin/universal-darwin:$PATH"

   # Linux（TeX Live）
   export PATH="/usr/local/texlive/2024/bin/x86_64-linux:$PATH"
   ```

### "Python not found" 错误

**问题**：技能脚本失败，提示 "python: command not found"

**解决方案**：
1. 安装 Python 3.6+
2. 创建符号链接：`ln -s /usr/bin/python3 /usr/local/bin/python`
3. 或在技能脚本中显式使用 `python3`

### 权限被拒绝错误

**问题**：安装失败，提示 "permission denied"

**解决方案**：
```bash
# 修复权限
chmod -R 755 ~/.claude/skills/

# 或使用 sudo 进行系统级安装
sudo claude skill install ...
```

## 下一步

- [快速开始指南](/zh/quick-start) - 几分钟内上手
- [使用指南](/zh/usage) - 学习如何使用技能
- [编译配方](/zh/guides/compilation) - 了解编译工作流

## 获取帮助

- **文档**：浏览本站获取指南和参考
- **GitHub Issues**：[报告错误或请求功能](https://github.com/bahayonghang/academic-writing-skills/issues)
- **社区**：在 GitHub 上加入讨论
