# 中文学位论文学院数字、公式、表身和中文题注契约

## 1. Scope / Trigger

维护 `latex-thesis-zh` 的 `--school`、数字/单位候选、公式源码候选、表身候选、
中文题注末标点，或对应公开指南时适用。面向作者的规则由技能内
`references/formatting/number-unit-guide-zh.md`、`formula-guide.md`、
`caption-guide.md`、`table-guide.md` 与相关模块页拥有。复制安装后的技能不得依赖本
spec 或私有论文语料。

## 2. Signatures

```text
uv run python scripts/check_style_zh.py INPUT
    [--degree-wording] [--school yanshan-ee-2025|generic]
uv run python scripts/check_format.py INPUT [--strict] [--school yanshan-ee-2025|generic]
uv run python scripts/check_tables.py INPUT [--fix-suggestions] [--school yanshan-ee-2025|generic]
uv run python scripts/check_references.py INPUT [--school yanshan-ee-2025|generic]
```

`--school` 的可选值只有 `yanshan-ee-2025` 和 `generic`。省略和默认都是 `generic`。
不接受单独的 `yanshan`。非法取值走既有 argparse 错误路径，退出码非零，且不打印通过。

## 3. Contracts

- 新增规则只在 `yanshan-ee-2025` 运行。`generic` 和缺省路径不新增候选，默认 stdout、stderr 和退出码保持不变。`--help` 不属于旧输出基线。
- 数字、单位和千分空只在 `check_style_zh.py`。公式源码只在 `check_format.py` 的原始装配文本上检查，不用抽掉数学的可见文本。表身「同上」「同左」、同单位列表头和表题末标点只在 `check_tables.py`。非表浮动体的中文题注末标点只在 `check_references.py`。同一浮动体只由一个脚本报告。
- `check_references.py` 的 `--school` 不增加引文位置、页码或文献著录规则。
- 新候选为 `[Script]`、Info/P3、`Meaning-Check: NEEDS-LLM`。只报告局部位置或片段，不输出整句替换，不改写数学。
- 百分号和摄氏度在学院模式中按普通单位检查间隔。平面角的度、分、秒保持紧贴，不把 `℃` 一并豁免。半角空格、`~` 和 `\,` 等显式间隔不算违规。指南推荐 `~`，这是项目源码约定，不是学院逐字条文。
- 千分空从小数点向两侧每 3 位分组，负号不计位数。年份紧接「年」、时刻、DOI、路径、科学计数、带字母型号、编号标签和 TikZ 坐标不报确定违规。未分类裸数字只给覆盖说明，既不是确定违规，也不写成学院豁免。不使用年份或型号闭集。
- 简单 `tabular` 的单元格在 `check_style_zh.py` 里按同一套数字规则扫描。紧贴的 `50\%` 是 `NUM-SPACE`，不要求三行；三行阈值只属于 `TB-UNITHEAD`。纯数字单元格里未分组的 `1004` 或 `1004.1` 是 `NUM-GROUP`。只写单位的表头、`降幅/\%` 和「百分点」不是数字后单位。`multicolumn`、`multirow` 和嵌套 `tabular` 不合并列，只给一条覆盖说明。`longtable` 和 `sidewaystable` 各给一条覆盖说明，不扫描单元格。
- `EQ-CONT` 只对单条长等式续行行首重复的关系符或运算符给候选。`A &= B + C \\ &= D` 是候选；`A = B + C = \\ D` 不是。`cases`、独立左端定义和约束行不报。无法区分推导链与续行时给一条覆盖说明。
- `EQ-LEADIN` 只看编号展示块前的可见正文句是否以中文冒号结束。`EQ-TAILPUNCT` 看最后数学片段后的中文句号或逗号，不把 `cases` 条件分隔符当成该标点。`EQ-CITE` 看可见的「上式」「下式」，但 `以上式子` 不命中；`以上式` 仍可命中。`EQ-NOTE` 区分「式中」的两格半角空格加破折号和「其中」的无空格、无破折号。顶格和破折号视觉对齐仍人工。注释中的「其中」不是正文。
- `TB-SAMEAS` 不看题注和表注。`TB-UNITHEAD` 要求简单表格中至少三行数值的字面单位相同且表头没有该单位，不换算单位。`multicolumn`、`multirow` 或嵌套表给未覆盖说明，不合并命中。空白和破折号不推断测量事实。
- 中文题注只看中文主参数的可见正文是否以中文标点结束。可选短参数、`\bicaption` 第二参数、英文句点，以及代码、数学和引用键中的标点不算。无法确认中文主参数时留人工。
- `--degree-wording` 与 `--school yanshan-ee-2025` 可以同时使用，互不吞掉或复制发现。
- 未知宏展开和未闭合环境是覆盖不足，不作为通过。不新增 siunitx、配置文件、依赖、PDF 几何、字体检查或单位换算。

## 4. Validation & Error Matrix

| 条件 | 必须行为 |
| --- | --- |
| 未传 `--school`，或 `--school generic` | 四个入口的旧输出不变，且没有本契约的新候选 |
| `--school yanshan-ee-2025` | 只增加本契约的候选；默认严重度体系不批量改写 |
| `--school yanshan` 或其他非法值 | 非零退出，不打印通过 |
| 数学环境中的百分号或摄氏度缺间隔 | 只报告位置，建议字段为空 |
| 续行关系符留在上一行，或 `cases` / 独立定义 / 约束行 | 不报 `EQ-CONT` |
| 未闭合环境、复杂公式，或无法区分推导链与续行 | `check_format.py` 给出 `EQ-COVERAGE`，总状态不是 `PASS` |
| 表题末标点与图题末标点 | 分别只出现在 tables 与 references |

## 5. Good / Base / Bad Cases

- Good：`50~\%`、`1\,004.1`、`0.174\,6`、引导句以「：」结束、公式末无中文标点、关系符留在上一行、表头已含该列字面单位、中文题注无末标点。
- Base：不传 `--school` 时，旧的 `E-*`、格式、表格和交叉引用输出保持不变。
- Bad：把 AMS 推导链写成学院唯一正确写法；把平面角和摄氏度一起豁免；用可见文本抽掉公式后再判公式；把 `bicaption` 的英文参数当成中文标点；把未分类裸数字写成学院豁免或确定违规。

## 6. Tests Required

`tests/skills/latex_thesis_zh/test_number_equation_table.py` 按路径加载四个 ZH 脚本，并恢复 `sys.path` 与 `sys.modules`。
子进程设置 `PYTHONIOENCODING=utf-8`，解释器使用 `python -X utf8`。
断言学院模式与 generic 的差异、非法 school、C1 `--degree-wording` 组合、数字/公式/表身/题注的正反例，以及无新参数基线的字节比较。
`test_polish_unit_zh.py` 只更新 `check_style_zh.py` 的 LF 规范化哈希。
公开资源同步源文件、另一语言译文、中文或英文同语言镜像和 manifest。最终运行目标测试、资源同步、`just ci` 和 `just doc-build`。

真实论文、PDF 页面和五个宿主不由本契约的合成测试证明。

## 7. Wrong vs Correct

错误：修改 `UNIT_NO_SPACE` 后声称百分号间隔已按学院规则修复，或让 `yanshan` 模板静默打开学院模式。

正确：默认 `E-NUMSPACE` 仍按国标处理百分号和摄氏度；学院间隔、千分空、公式和表身候选只在显式 `--school yanshan-ee-2025` 后出现。
