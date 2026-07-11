# Format Module Reference

Purpose: Check thesis page layout, heading format, figure/table/equation numbering, and displayed formula layout against GB/T 7713.1 and university template rules.

## Chapter Heading & Figure/Table Numbering

这些是**校级排版约定**（各校自定，非国标强制）：常见设定见
[`../../templates/generic.md`](../../templates/generic.md) 的"常见校级排版约定"一节；
已知模板时改读 `templates/thuthesis.md`（图 3-1 连字符风格）或
`templates/pkuthss.md`（图3.1 点号风格），模板会自动处理格式。

## Displayed Formula Layout

公式排版问题（如“公式编号被挤到下一行”“这个长公式是否应该拆成两行”“相邻公式要不要同步拆行”）
属于 `format` 路由。先读 [`../formatting/formula-guide.md`](../formatting/formula-guide.md)，再按学校模板判断。

核心判断：

- 公式超出版心、贴近页边距、或把编号挤到下一行时，建议受控拆行。
- 推导链按 `=` / `\approx` / `\le` / `\Rightarrow` 等关系符号对齐。
- 方程组、分段条件、成组约束用 `aligned` / `cases` 等结构。
- 已经能正常放下、编号未被挤行、且没有推导/成组语义的公式，不要为视觉统一强行拆分。

## Source Hygiene (源码卫生：F-MD / F-NOTE)

`check_format.py` 默认输出内置两项源码卫生检查（无需额外 flag），仅定位提示、不改写：

| Check | Rule | Severity |
|-------|------|----------|
| F-MD | 可见正文命中 Markdown 加粗 `**…**`（`\*\*` 转义星号不计）——LaTeX 中按字面星号排版，应改 `\textbf{}` | Major/P1 |
| F-NOTE | 可见正文命中草稿备注词表（"后续可根据…替换/更新/补充""此处占位""待补充/待确认""TODO/FIXME"）——疑似草稿备注泄漏进正文，定稿前应删除或移入注释 | Info/P3 |

两项均只扫可见正文（数学环境/verbatim/注释排除）；F-NOTE 词表刻意收窄，"仍需实验确认"
一类正常学术让步表述不命中。

## Key Checks

- Page margins and layout per university template
- Heading numbering consistency (chapter-based or sequential)
- Caption placement (figures below, tables above)
- Equation numbers right-aligned without being displaced to a separate line
- Displayed formulas split only when width, alignment, derivation, grouping, or readability requires it
- Font and size compliance per heading level — 以本校最新格式规范为准
