# 模块：编译
**触发词**: compile, 编译, build, typst compile, typst watch

**Typst 编译命令**:
| 命令 | 用途 | 说明 |
|------|------|------|
| `typst compile main.typ` | 单次编译 | 生成 PDF 文件 |
| `typst watch main.typ` | 监视模式 | 文件变化时自动重新编译 |
| `typst compile main.typ output.pdf` | 指定输出 | 输出为位置参数（无 `--output` flag） |
| `typst compile --format png main.typ "page-{p}.png"` | 其他格式 | PNG/SVG 多页须含 `{p}` 页码模板 |
| `typst fonts` | 字体列表 | 查看系统可用字体 |

**使用示例**:
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

**编译速度优势**:
- Typst 编译速度通常在毫秒级（vs LaTeX 的秒级）
- 增量编译：只重新编译修改的部分
- 适合实时预览和快速迭代

**中文支持**:
```typst
// 中文字体配置示例
#set text(
  font: ("Source Han Serif", "Noto Serif CJK SC"),
  lang: "zh",
  region: "cn"
)
```
