# 润色改写契约与自动化分级

> 来源：07-27-polish-capability-upgrade 三子任务（C1 契约 / C2 EN+Typst / C3 ZH），2026-07-27。

---

## Contract: 产出改写的模块必须输出两层四字段，`[Script]` 层禁 `PRESERVED`

**What**：任何**产出可直接替换原文的具体文本**的模块，输出块必须追加四个字段（字段名三方逐字一致，注释符按文档语言取 `%` 或 `//`，值右对齐到 `Meaning-Check: ` 宽度）：

```
% Changed:       <脚本可验证的变更事实，或 none>
% Protected:     <本行内被识别并跳过的受保护 token，或 none>
% Meaning-Check: <PRESERVED | NEEDS-LLM>
% Risk-Flags:    <none | not-assessed | lexical-substitution | whitespace-normalized | overstatement | ambiguity | terminology-drift | invented-claim>
```

分层规则：

| 层         | `Meaning-Check`            | `Risk-Flags`                                                                                           |
| ---------- | -------------------------- | ------------------------------------------------------------------------------------------------------ |
| `[Script]` | **只能** `NEEDS-LLM`       | 只能置 `none` / `not-assessed` / `lexical-substitution` / `whitespace-normalized`，兜底 `not-assessed` |
| `[LLM]`    | `PRESERVED` 或 `NEEDS-LLM` | 全闭集；`PRESERVED` 是提案不是事实                                                                     |

**Why**：规则脚本没有语义判定能力。让它输出肯定式的「语义已保全」，等于用契约的形式生产假保证，比没有契约更糟。`NEEDS-LLM` 复用 `latex-thesis-zh/scripts/check_spec.py` 的既有状态枚举（`PASS | FAIL | NEEDS-LLM | MODULE | MANUAL | SKIP`），语义是「本层无判定能力，需上层复核」——**不要发明 `requires-review` 等新词**。

**适用范围三分法**（写进三方路由文档，逐项列出，不靠默认）：

- **纳入**：EN/Typst `expression` / `grammar` / `sentences` / `translation`；ZH `expression`。
- **仅 `[LLM]` 层**：EN `section-writing` / `caption` / `adapt`；Typst `adapt`；三方 `deai`（其 `-> Suggestion:` / `-> 建议:` 是行为指令，不是替换文本）。
- **排除**：全部纯诊断模块（compile / format / bibliography / references / tables / figures / pseudocode / logic / literature / experiment / abstract / conclusion / title / spec-check / blind-review / structure / consistency / template）。给它们加字段只是噪音。

**Tests Required**：`tests/contracts/test_polish_contract_alignment.py` 同时断言三方文档的字段名、`Risk-Flags` 闭集、`[Script]` 禁 `PRESERVED` 规则与排除清单。**该测试只断言文档**——脚本输出的断言归各技能自己的测试（`tests/skills/latex_paper_en/test_polish_pipeline.py`、`tests/skills/latex_thesis_zh/test_check_style_zh.py`）。排除清单的锚点是粗体标记 `**排除` / `**Excluded`，不是裸词「排除」——裸词会把逐检查器排除说明里的反引号名误纳入。

---

## Contract: 三条编辑轴不得一词多义

**What**：

| 轴         | 参数名       | 取值                                              | 默认           | 归属                   |
| ---------- | ------------ | ------------------------------------------------- | -------------- | ---------------------- |
| 编辑目标   | `--goal`     | `grammar` / `clarity` / `concision` / `coherence` | `grammar`      | 润色类脚本             |
| 编辑幅度   | `--strength` | `minimal` / `moderate` / `restructure`            | `minimal`      | 润色类脚本             |
| 检测灵敏度 | `--tier`     | `light` / `medium` / `heavy`                      | 不传即默认阈值 | **仅** `deai_check.py` |

**Why**：三者取值词汇天然重叠（都会用到 light/heavy），一旦互相借用命名就形成一词三义。`--strength` 的取值**刻意避开** `light|medium|heavy` 三个字面，就是为了从词形上杜绝与 `--tier` 混淆。`deai --tier` 的语义是检测灵敏度（`_apply_tier` docstring：light flags fewer, heavy flags more），**不是**编辑幅度——改 `_TIER_FACTORS` 属越界。

**Wrong vs Correct**：

```python
# Wrong：把 --tier 当幅度控制复用，或给 --strength 取 light/medium/heavy
cli.add_argument("--tier", choices=["light", "medium", "heavy"], help="how far to edit")

# Correct：两轴正交、词形不重叠，--tier 保持 deai 专属
cli.add_argument("--goal", choices=GOAL_CHOICES, default="grammar")
cli.add_argument("--strength", choices=STRENGTH_CHOICES, default="minimal")
```

**Validation**：`grep -rn "revision_goal\|edit_strength" academic-writing-skills/ tests/` 应零命中（这两个是规划期的概念名，不是落地符号）；`git diff -- '*/scripts/deai_check.py'` 应为空。

---

## Convention: 规则可判定性分三档，红线阻塞的检查器不得升 A 档

**What**：每条替换规则、每类受保护 token、每个检查器必须落到三档之一：

| 档  | 标记        | 输出行为                                                                       |
| --- | ----------- | ------------------------------------------------------------------------------ |
| A   | `auto`      | 判定确定，给 `Original` / `Revised`（或 `建议`）+ 契约字段                     |
| B   | `candidate` | 模式可检出但依赖上下文，**只报候选、不给替换文本**，`Risk-Flags: not-assessed` |
| C   | `llm-only`  | 规则不可判定，脚本不实现，只在模块文档指导 `[LLM]` 层                          |

**Why**：参照 skill 只给原则不给识别方法。把原则实现成「脚本自动识别全部类别」是不可能的，硬做就会写坏正文——实测 `\bmake\b` → `develop` 会把 `Make sure` 变成 `develop sure`、`make use of` 变成 `develop use of`，`\bvery\b` → `highly` 会把 `very few` 变成 `highly few`。**降级为 B 档而不是加搭配排除表**：`make sense` / `make up` / `make do` / `make it` 是开放集，穷举必漏，漏了就产出错误英文；只报候选把判断交给 LLM，成本低且不会写坏。

**红线例外**：`latex-thesis-zh` 的 `E-UNITFONT`（数学环境内单位斜体）**检出是确定的**，但问题位于数学环境内，而「绝不修改数学环境」是红线一。因此它只读、只报告、永不给替换文本。**它的分档依据是红线而非判定能力**——后续会话不要把它当成「可以升 A 档的漏网之鱼」。

**同类已判定项（勿重开）**：

- `use → employ`、`show → demonstrate` 是**有意删除**的（finding E15）：de-AI 指南把 "we use ..." 列为正确学术英语、把 "demonstrate the effectiveness" 列为 AI 痕迹，套用会让 `expression` 与 `deai` 互相打架。模块文档已写明原因防「修回去」。
- `\bmake\b` **不匹配** `makes`（`e` 后接词字符，`\b` 不成立）。不要写 `makes it possible` 的回归用例——写了等于不断言。
- `academic-style-zh.md` §1.3 的单字动词（用/做/看/想/试）是 C 档：它们是「采用」「制作」「看法」的子串，规则层不可判定。

**Tests Required**：每条降为 B 档的规则须有一条反例测试（断言原文不被改坏）；每个检查器的排除条件须有反例测试——**排除条件是契约的一部分，不是可选优化**。

---

## Convention: 正文里的纯文本 token 需要独立护栏

**What**：`\cite{}` / `\ref{}` / `@cite` / `<label>` / 数学环境由语法规则守住，但统计值、带单位的数值、模型与数据集名、基因与化学名在正文里是**无标记的普通词**。润色脚本必须在替换前遮蔽 A 档可确定的形态（p 值、百分比、数值+单位、含数字的标识符、大写连字符名、全大写缩写），并通过 `Protected:` 字段可见。

**Why**：多护住一个普通词只损失一条润色建议；少护住一个指标会静默损坏实验结果。遮蔽刻意宽松是有意取舍。

**单点定义**：`latex-paper-en/references/writing/protected-tokens.md` 与 `typst-paper/references/PROTECTED_TOKENS.md`。SKILL.md 与模块文档只做**指针**，不复制清单——复制必漂移。基因/化学名的非全大写形态是 C 档，**不引入词典**（维护成本与误报都不可控）。
