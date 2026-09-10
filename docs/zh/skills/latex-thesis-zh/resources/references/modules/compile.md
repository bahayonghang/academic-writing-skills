# 编译模块参考

用途：诊断并修复中文 LaTeX 学位论文项目中的编译问题。

## Skill 执行边界

通过 skill 自带 wrapper 编译，并使用项目实际入口文件与文献后端：

```bash
uv run python $SKILL_DIR/scripts/compile.py main.tex --recipe latexmk
uv run python $SKILL_DIR/scripts/compile.py main.tex --recipe xelatex-bibtex
uv run python $SKILL_DIR/scripts/compile.py main.tex --recipe xelatex-biber
```

wrapper 也支持 LuaLaTeX recipe。选择前先识别项目；`main.tex`、XeLaTeX 与某一种文献
recipe 都不是通用默认值。下文的原始编译命令用于说明工具选择，不表示可以绕过 wrapper。
不要把清理现有 PDF、安装缺失宏包或启用 `--shell-escape` 作为自动恢复步骤。

## 输出目录与成功判据

```bash
uv run python $SKILL_DIR/scripts/compile.py main.tex --recipe latexmk --outdir build
uv run python $SKILL_DIR/scripts/compile.py main.tex --compiler lualatex --outdir "build output"
```

未指定 `--outdir` 时，目标 PDF 位于源入口文件旁。相对输出目录以源入口所在目录为基准，
不以调用者当前目录为基准；绝对目录保持其位置。包含空格或中文的路径作为单个参数传入。
报告中的 PDF 与 latexmk 命令使用同一个解析后的目录。

默认 latexmk 路径、`--recipe latexmk` 和显式 `--compiler` 均支持 `--outdir`。手动 recipe
（`xelatex`、`lualatex` 及其 `-bibtex` / `-biber` 变体）会在执行工具前拒绝此组合。
需要显式选择受支持的 latexmk 路径；wrapper 不会静默替换已选 recipe。

正常结束的 latexmk 运行仅在退出码为 0 且目标 PDF 存在时成功。源目录旧 PDF 不能替代输出目录
中缺失的 PDF。latexmk 认定无需重建的已有目标仍然有效；此检查不证明新鲜度或版式正确。
即使未指定 `--outdir`，显式 compiler 在 PDF 缺失时也会失败。未指定 `--outdir` 的手动 recipe
保留既有文献后端警告后继续的行为。watch 中断和 shell-escape 信任要求不变。

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
| 缺少宏包 | 报告缺失宏包与安装证据；安装需要单独授权 |
| 参考文献未更新 | 选择匹配的 wrapper recipe，并报告确切退出码与日志证据 |

## 监视模式

```bash
latexmk -xelatex -pvc main.tex  # auto-recompile on changes
```

## 图表版式验收

修改题注、续图、长表、缩放或图像分辨率后：

1. 要求 wrapper 退出码为 0，并使用所选入口和 recipe 报告的 PDF 路径；
2. 涉及编号或续图目录项时，检查 `.aux` 和图/表目录；
3. 渲染并实际查看受影响页面及相邻页；
4. 检查题注顺序、续图标记、溢出、留白、裁切和文字可读性。

仅有编译成功、`.aux` 条目或 PNG 文件不构成视觉证据。渲染器不可用或没有实际查看页面时，
记录 `missing evidence`。不要为这一流程增加 PDF 压缩或 UI 自动化。

> 完整说明：参见 [`../latex/compilation.md`](../latex/compilation.md)
