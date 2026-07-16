# module:compile
**Trigger words**: compile, compile, build, typst compile, typst watch

**Typst compilation command**:
|Order|use|illustrate|
|------|------|------|
| `typst compile main.typ` |single compilation|Generate PDF file|
| `typst watch main.typ` |Monitor mode|Automatically recompile when files change|
| `typst compile main.typ output.pdf` |Specify output|The output is a positional argument (none`--output`flag)|
| `typst compile --format png main.typ "page-{p}.png"` |other formats|PNG/SVG Multiple pages must be included`{p}`Page number template|
| `typst fonts` |Font list|View available fonts on the system|

**Usage Example**:
```bash
# 基础编译（推荐）
typst compile main.typ

# 监视模式（实时预览）
typst watch main.typ

# 指定输出文件（输出是位置参数，没有 --output 选项）
typst compile main.typ build/paper.pdf

# 导出为 PNG（多页须用 {p} 页码模板，否则多页文档会报错）
typst compile --format png main.typ "preview-{p}.png"

# 查看可用字体
typst fonts

# 使用自定义字体路径
typst compile --font-path ./fonts main.typ
```

**Compilation speed advantage**:
- Typst compilation speed is usually on the millisecond level (vs. LaTeX’s second level)
- Incremental compilation: only recompile the modified parts
- Ideal for real-time preview and rapid iteration

**Chinese support**:
```typst
// 中文字体配置示例
#set text(
  font: ("Source Han Serif", "Noto Serif CJK SC"),
  lang: "zh",
  region: "cn"
)
```
