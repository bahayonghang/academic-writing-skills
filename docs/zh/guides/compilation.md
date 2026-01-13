# 编译配置指南

Academic Writing Skills 中 LaTeX 编译配置的完整指南。

## 概述

Academic Writing Skills 提供多种针对不同场景优化的编译配置。

## 配置架构

每个配方是一系列编译步骤：

```
配方 = [步骤1, 步骤2, ..., 步骤N]
```

例如 `pdflatex-biber`：
```
[pdflatex, biber, pdflatex, pdflatex]
```

## 可用配置

### 单次编译配置

#### pdflatex

**用途**：快速英文草稿

| 优点 | 缺点 |
|------|------|
| 最快（1-2秒） | Unicode 支持有限 |
| 稳定成熟 | 无系统字体 |
| 兼容性广 | 仅 ASCII |

```bash
python compile.py paper.tex --recipe pdflatex
```

#### xelatex

**用途**：Unicode/中文文档（推荐）

| 优点 | 缺点 |
|------|------|
| 完整 Unicode 支持 | 比 pdfLaTeX 慢（3-5秒） |
| 系统字体访问 | 输出文件较大 |
| CJK 支持 | |

```bash
python compile.py thesis.tex --recipe xelatex
```

#### lualatex

**用途**：复杂字体需求的中文文档

| 优点 | 缺点 |
|------|------|
| 完整 Unicode 支持 | 比 XeLaTeX 慢 |
| Lua 脚本能力 | 生态不如 XeLaTeX 成熟 |
| 现代字体处理 | |

```bash
python compile.py thesis.tex --recipe lualatex
```

### 参考文献工作流

#### pdflatex-bibtex

**步骤**：pdflatex → bibtex → pdflatex → pdflatex

**用途**：传统 BibTeX 的英文论文

```bash
python compile.py paper.tex --recipe pdflatex-bibtex
```

#### pdflatex-biber

**步骤**：pdflatex → biber → pdflatex → pdflatex

**用途**：现代参考文献的英文论文（推荐）

```bash
python compile.py paper.tex --recipe pdflatex-biber
```

#### xelatex-biber

**步骤**：xelatex → biber → xelatex → xelatex

**用途**：中文论文（推荐）

```bash
python compile.py thesis.tex --recipe xelatex-biber
```

#### lualatex-biber

**步骤**：lualatex → biber → lualatex → lualatex

**用途**：复杂字体需求的中文论文

```bash
python compile.py thesis.tex --recipe lualatex-biber
```

#### latexmk

**用途**：自动依赖处理

```bash
python compile.py paper.tex --recipe latexmk
```

## 配方选择决策树

```
开始
  │
  ├─ 包含中文？
  │   ├─ 是 → 使用 XeLaTeX
  │   │   ├─ 有参考文献？
  │   │   │   ├─ 是 → xelatex-biber（推荐）
  │   │   │   └─ 否 → xelatex
  │   └─ 否 → 使用 pdfLaTeX
  │       ├─ 有参考文献？
  │       │   ├─ 是 → pdflatex-biber（推荐）
  │       │   └─ 否 → pdflatex
  │
  ├─ Unicode 字符？
  │   └─ 是 → 使用 XeLaTeX
  │
  ├─ 自定义字体？
  │   └─ 是 → 使用 XeLaTeX
  │
  └─ 默认 → pdflatex 或 pdflatex-biber
```

## 性能对比

| 配方 | 小文档 | 大文档 | 输出大小 |
|------|--------|--------|----------|
| pdflatex | 1-2秒 | 5-10秒 | 小 |
| xelatex | 3-5秒 | 15-30秒 | 中 |
| lualatex | 4-6秒 | 20-40秒 | 中 |
| pdflatex-biber | 6-10秒 | 25-50秒 | 小 |
| xelatex-biber | 12-20秒 | 60-120秒 | 中 |
| lualatex-biber | 15-25秒 | 80-150秒 | 中 |

## 故障排除

### 参考文献未显示

**问题**：参考文献部分为空

**解决**：使用完整配方
```bash
python compile.py paper.tex --recipe pdflatex-biber
```

### 引用显示为 [?]

**问题**：引用显示为 `[?]`

**解决**：运行完整配方（需要多次编译）

### 中文字符未显示

**问题**：中文显示为方框

**解决**：切换到 XeLaTeX
```bash
python compile.py thesis.tex --recipe xelatex-biber
```

### 编译太慢

**解决方案**：
1. 草稿阶段使用快速配方：
   ```bash
   python compile.py paper.tex --recipe pdflatex
   ```
2. 使用 LaTeX 草稿模式：
   ```latex
   \documentclass[draft]{article}
   ```

## 最佳实践

### 1. 根据阶段选择配方

**草稿阶段**：快速单次编译
```bash
python compile.py paper.tex --recipe pdflatex
```

**审阅阶段**：完整工作流
```bash
python compile.py paper.tex --recipe pdflatex-biber
```

**最终提交**：完整工作流 + 清理
```bash
python compile.py paper.tex --recipe pdflatex-biber
python compile.py paper.tex --clean
```

### 2. 保持配方一致

每个项目坚持使用同一配方，避免不一致。

### 3. 定期清理辅助文件

```bash
python compile.py paper.tex --clean
```

### 4. 复杂项目使用 latexmk

```bash
python compile.py thesis.tex --recipe latexmk
```

## 下一步

- [格式检查指南](/zh/guides/format-checking)
- [参考文献指南](/zh/guides/bibliography)
