# 编译模块参考

用途：诊断并修复中文 LaTeX 学位论文项目中的编译问题。

## 编译器选择

| 编译器 | 最适合 | 命令 |
|----------|----------|---------|
| XeLaTeX | 中文文档、Unicode、系统字体 | `latexmk -xelatex main.tex` |
| LuaLaTeX | 现代功能、Lua 脚本、面向未来 | `latexmk -lualatex main.tex` |
| pdfLaTeX | 纯英文论文（CJK 支持较弱） | `latexmk -pdf main.tex` |

## latexmk 配置

在项目根目录创建 `.latexmkrc`：
```perl
$pdf_mode = 5;  # xelatex
$xelatex = 'xelatex -interaction=nonstopmode -no-shell-escape %O %S';
$bibtex_use = 2;
$biber = 'biber %O %S';
```

仅对已经明确验证为可信的源文件启用 `-shell-escape`。

## 常见问题

| 问题 | 解决方案 |
|---------|----------|
| 找不到中文字体 | 指定字体：`\setCJKmainfont{SimSun}[BoldFont=SimHei]` |
| 缺少宏包 | `tlmgr install <package-name>` |
| 参考文献未更新 | `latexmk -C main.tex && latexmk -xelatex main.tex` |

## 监视模式

```bash
latexmk -xelatex -pvc main.tex  # auto-recompile on changes
```

> 完整说明：参见 [`../latex/compilation.md`](../latex/compilation.md)
