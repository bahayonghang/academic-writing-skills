# Spec-Check Module Reference

Purpose: 定稿阶段对照学校规范清单**逐项终检**。清单来自 `templates/<template>.md` 的
「## 逐项检查清单」段（或 `--spec-file` 自定义文件），脚本执行可自动判定项，其余按
NEEDS-LLM / MODULE / MANUAL 分流，最终汇总为一份逐项符合性报告。

## Primary Command

```bash
uv run python $SKILL_DIR/scripts/check_spec.py main.tex --template yanshan --degree doctor
```

- `--template <id>`：使用 `templates/<id>.md` 的清单（当前带清单的模板：yanshan、thuthesis、
  pkuthss、generic；未指定时按 documentclass 自动推断，推断到无清单的模板会报错并列出可用清单）。
- `--spec-file <path>`：使用任意符合清单表格格式的自定义规范文件（通用入口：任何学校的
  规范都可整理成清单后接入；引用了不存在检查器的条目自动降级为 NEEDS-LLM，不会中断）。
- `--degree master|doctor`：学位类型（影响字数/文献数量阈值与条目适用范围；缺省时从正文
  自动识别，识别失败按 master 并在报告头注明）。
- `--bib <path>`：指定 .bib（缺省从 `\bibliography` / `\addbibresource` 自动发现，
  或回退统计 `thebibliography` 环境）。
- `--year <yyyy>`：近五年/近两年判定的基准年份（缺省当前年份；测试或复现时固定它）。
- `--json`：结构化输出（items + summary + status）。

退出码：存在 FAIL → 1；清单文件缺失/不合法 → 2；否则 0。

## Workflow（五步）

1. **确认清单**：已知学校/模板时直接 `--template`；未知时先跑 `template` 模块识别，
   仍无清单则请用户提供学校名或规范文件（转成 `--spec-file` 清单，格式见下）。
2. **跑脚本**：执行 Primary Command，得到六类状态的逐项结果
   （PASS / FAIL / NEEDS-LLM / MODULE / MANUAL / SKIP）。
3. **处理 MODULE 项**：按报告中的建议命令逐条执行既有模块（tables / references /
   bibliography / consistency / format），把各模块的发现挂回对应清单条目。
4. **LLM 逐项判读 NEEDS-LLM 项**：每条打开 `templates/<template>.md` 中该条目
   `规范依据` 指向的要点段（如 §1.5.3 结论要求），对照论文对应章节文本判断
   符合 / 不符合 / 无法判定，并给出证据（源文件:行号 + 原文摘录）。判读结论标注 `[LLM]`，
   与脚本结果（`[Script]`）分开陈述，不得混淆。
5. **汇总报告**：按清单顺序输出逐项结论表（ID / 检查项 / 结果 / 证据 / 建议），
   FAIL 与 LLM 判定不符合的条目给出可执行的修改建议（diff/suggestion 形式）；
   MANUAL 项原样输出为**打印前自查单**交给用户（版式/印刷项无法静态判定，不要虚构结论）。

## 状态语义

| 状态        | 含义                                                       | 后续动作            |
| ----------- | ---------------------------------------------------------- | ------------------- |
| PASS / FAIL | 脚本自动判定，附证据与规范依据                             | FAIL 给修改建议     |
| NEEDS-LLM   | 脚本无法判定（语义类，或缺输入，或自定义清单的未知检查器） | 第 4 步逐项判读     |
| MODULE      | 由既有模块覆盖                                             | 第 3 步执行对应命令 |
| MANUAL      | 需编译 PDF / 打印核对                                      | 列入打印前自查单    |
| SKIP        | 适用范围与当前学位不符                                     | 无                  |

## 自定义清单格式（--spec-file）

与 `templates/yanshan.md` 的「## 逐项检查清单」一致：五列 markdown 表格。

```markdown
## 逐项检查清单

| ID    | 检查项               | 规范依据 | 检查方式        | 适用 |
| ----- | -------------------- | -------- | --------------- | ---- |
| XX-01 | 关键词 3～8 个       | §2.1     | script:kw_count | 通用 |
| XX-02 | 摘要含研究目的与结论 | §1.2     | llm             | 通用 |
```

- `ID`：`大写前缀-两到三位序号`（如 `XX-01`），文件内唯一。
- `检查方式`：`script:<checker>`（内建检查器见下）/ `module:<模块名>`（SKILL.md 路由表内
  的模块）/ `llm` / `manual`。
- `适用`：`通用` / `硕士` / `博士`。
- 字数/数量类内建检查器的阈值取自脚本内 `TEMPLATE_THRESHOLDS`（按模板 id）；自定义清单
  无阈值依据时这类条目会报实测值并降级 NEEDS-LLM，不会套用别校阈值。

## 内建检查器（script:）

`title_len`（题名≤25/含副题≤35）· `abstract_no_cite`（摘要禁引用/图表/公式）·
`kw_count`（关键词 3~8 且分号分隔）· `kw_zh_en_match`（中英关键词数量一致）·
`abstract_len` · `abstract_order`（中前英后）· `wordcount`（正文字数）·
`intro_len`（绪论字数）· `chapter_summary`（各章本章小结）·
`conclusion_no_cite`（结论不引文献且为末章）· `conclusion_len`（结论≤2000 字）·
`conclusion_hedge`（结论模糊措辞）· `bib_count` · `bib_recency`（近五年≥1/3 且有近两年）·
`heading_len`（标题≤15 字）· `heading_depth`（层次≤4 级）·
`cite_in_heading`（标题内禁 \cite）· `new_page_chapter`（每章另起页）·
`appendix_letter`（附录字母编号）

判定为区间/下限的检查器带 ±10% 缓冲带：落在缓冲带内报 NEEDS-LLM（规范多用“一般”措辞），
超出才报 FAIL。字数口径为“可见文本去空白字符数”（近似，含图表文字），报告中已注明。
上列括号内为缺省值；字数/个数/分隔符阈值可被 `TEMPLATE_THRESHOLDS[<模板>]` 按校覆盖
（如清华题名 25 无副题名扩展、北大题名 20 且关键词 3~5 逗号分隔、generic 关键词不查分隔符），
键缺省时保持缺省行为，不套用别校数值。

## Output Contract

- FAIL 行格式：`% SPEC-CHECK [High] [P1] [Script]: <ID> <检查项> — <证据>（依据 <§>）`。
- LLM 判读补充结论时用相同行格式、来源标 `[LLM]`，定位写 `源文件:行号`。
- 不修改任何源文件；`\cite{}` / `\ref{}` / `\label{}` / 数学环境一律不动。
- 报告必须保留 MANUAL 自查单——版式项对通过与否保持沉默即是结论（无法静态判定），
  不要替用户宣称“已符合”。

## 常见追问

- **“我是燕山大学的，帮我做毕业前最后检查”** → `--template yanshan`，学位从上下文确认。
- **“我们学校没有清单”** → 请用户提供规范原文/PDF 文本，先整理成 `--spec-file` 清单
  （每条注明规范原文出处；整理结果先给用户确认，不得凭通例编造条目），再跑终检。
- **盲审送审前** → 终检之外另跑 `blind-review` 模块（个人信息隐匿检查）。
