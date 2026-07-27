# Design: 共享润色契约（C1）

本文件是 C2/C3 的**冻结契约**。字段名、枚举、参数名一经此处定稿，C2/C3 一字不差复用。

## 落点与边界

- 改：三方 `SKILL.md` 的 Output Contract / Required Inputs 段、三方 `references/modules/`
  下润色分支的模块文档、三方 `routing-rules`。
- 加：一个跨 skill 契约测试。
- **不改**：任何检查器逻辑、`deai_check.py`（三副本）、`_TIER_FACTORS`、任何顶层 Reference
  Map。

## 一、三轴命名（冻结）

| 轴           | 参数名                | 取值（冻结）                                          | 默认       | 归属                     |
| ------------ | --------------------- | ----------------------------------------------------- | ---------- | ------------------------ |
| 编辑目标     | `--goal`              | `grammar` / `clarity` / `concision` / `coherence`      | `grammar`  | 润色类脚本（C2/C3 实现） |
| 编辑幅度     | `--strength`          | `minimal` / `moderate` / `restructure`                 | `minimal`  | 润色类脚本（C2/C3 实现） |
| 检测灵敏度   | `--tier`（**不动**）  | `light` / `medium` / `heavy`                           | 无（不传即默认阈值） | 仅 `deai_check.py` |

**命名理由**：

- `--strength` 取值刻意**避开** `light|medium|heavy` 三个字面，改用
  `minimal|moderate|restructure`，从词形上杜绝与 `--tier` 混淆。参照 skill 的
  `light polish / moderate rewrite / heavy restructure`（SKILL.md:47）语义被完整保留，只是
  首尾两档换了不歧义的词。
- `--goal` 取值对应参照 skill Revision Modes 的前四项（SKILL.md:55-58）。**不采纳**其余三项
  （Reviewer response / Peer-review feedback / Editorial feedback）——父任务 Out of Scope。
- 两轴**正交**：`--goal concision --strength minimal` 与 `--goal coherence --strength
  restructure` 都是合法组合。不得把 `--goal` 当成阶梯。

**幅度语义（三方一致）**：

| 值            | 允许动的层级                       | 禁止                     |
| ------------- | ---------------------------------- | ------------------------ |
| `minimal`     | 词汇、标点、明显语法错             | 改句子结构、改段落顺序   |
| `moderate`    | 上加：拆分/合并句子、语序调整      | 改段落顺序、增删论断     |
| `restructure` | 上加：段落顺序、话题句位置         | 增删论断（红线，永远禁） |

三档**都**受 Core Rule 约束：任何一档都不得添加论断、机制、引用、结果、局限、方法或作者意图。

## 二、两层输出契约（冻结）

### 字段（三方逐字一致）

在既有 `% MODULE (Line N) [Severity][Priority] [Source]: ...` 块之后追加：

```
% Changed:       <脚本可验证的变更事实；或 none>
% Protected:     <本行内被识别并跳过的受保护 token；或 none>
% Meaning-Check: <PRESERVED | NEEDS-LLM>
% Risk-Flags:    <闭集，逗号分隔>
```

ZH 侧字段名**保持英文标识符不变**（与 EN/Typst 逐字一致，便于同一个契约测试断言），冒号后的
说明文本可用中文。这与仓库既有做法一致：`check_spec.py` 的状态值 `NEEDS-LLM` 本身就是英文，
中文只出现在 evidence 里。

### 分层规则

| 层        | `Meaning-Check` 允许值 | `Changed` | `Risk-Flags`                              |
| --------- | ---------------------- | --------- | ----------------------------------------- |
| `[Script]`| **只能** `NEEDS-LLM`   | 必填，只陈述可验证事实（命中了哪条规则、替换了哪个 token） | 只能置**规则可确定**的标记：`lexical-substitution`、`whitespace-normalized`、`not-assessed` |
| `[LLM]`   | `PRESERVED` 或 `NEEDS-LLM` | 必填 | 全枚举可用 |

**核心约束**：`[Script]` 永远不得输出 `Meaning-Check: PRESERVED`。规则脚本没有语义判定能力，
肯定式声明即虚假可审计性。`[LLM]` 输出 `PRESERVED` 时，SKILL.md 须写明这是**提案**，作者仍需
核对。

### `Risk-Flags` 闭集（冻结）

| 值                       | 含义                                     | `[Script]` 可置 |
| ------------------------ | ---------------------------------------- | --------------- |
| `none`                   | 无风险                                   | 是              |
| `not-assessed`           | 本层无法评估（`[Script]` 的常态兜底）    | 是              |
| `lexical-substitution`   | 发生了词汇替换，语义影响待核              | 是              |
| `whitespace-normalized`  | 空白/排版被规范化                        | 是              |
| `overstatement`          | 措辞强度被升高（见第四节）               | 否（仅 LLM）    |
| `ambiguity`              | 原文含义不清，改写基于假设                | 否（仅 LLM）    |
| `terminology-drift`      | 术语被改动                                | 否（仅 LLM）    |
| `invented-claim`         | 疑似引入了原文没有的论断                  | 否（仅 LLM）    |

`[Script]` 层在无其他可确定标记时，默认置 `not-assessed`——这正是 Codex 复审指出的缺口。

## 三、契约适用范围（冻结）

判定标准：**该模块是否产出可直接替换原文的具体文本**。

**纳入**（Script + LLM 两层）：EN/Typst `expression`、`grammar`、`sentences`、`translation`；
ZH 新增 `expression`。

**仅 LLM 层**（无脚本或脚本只出指令）：EN `section-writing` / `caption` / `adapt`；三方
`deai`（其输出是行为指令如"长短句交替"，不是替换文本）。

**排除**（不加契约段）：compile、format、bibliography、references、tables、figures、
pseudocode、structure、consistency、template、title、abstract、conclusion、logic、
literature、experiment、spec-check、blind-review。

排除清单**写进文档**，不靠默认——否则实现者会按"看起来像润色"逐个加，制造噪音。

## 四、over-claim 指针（分支级，非顶层）

在下列文件加强指针，**不动 SKILL.md 顶层 Reference Map**：

| Skill | 文件                                              | 指向                                     |
| ----- | ------------------------------------------------- | ---------------------------------------- |
| EN    | `references/modules/{expression,grammar,sentences}.md` | `../evidence/over-claim-guard.md`   |
| Typst | `references/modules/{EXPRESSION,GRAMMAR,SENTENCES}.md` | `../OVER_CLAIM_GUARD.md`            |
| ZH    | `references/modules/expression.md`（C3 建，C1 供文案） | `../writing/over-claim-guard.md`    |

统一规则文案：**改写不得升高措辞强度**；若改写涉及强度变化，`[LLM]` 层须置
`Risk-Flags: overstatement`。判据引用既有 guard 表与 EN `references/writing/style-guide.md:81-91`
的四级 reporting verb 阶梯，不新建替换表。

## 五、`NEEDS-LLM` 跨 skill 引入

`NEEDS-LLM` 目前仅存在于 `latex-thesis-zh`（`check_spec.py:56` 枚举
`PASS | FAIL | NEEDS-LLM | MODULE | MANUAL | SKIP`，另见 `blind_review.py`、
`analyze_conclusion.py`）。C1 将其语义原样引入 EN 与 Typst：**"本层无判定能力，需上层
LLM/人工复核"**。不改 ZH 既有用法，不引入 `requires-review` 等新词。

## 六、文件改动面

| 文件                                                        | 改动                                    |
| ----------------------------------------------------------- | --------------------------------------- |
| `latex-paper-en/SKILL.md`                                    | Output Contract + Required Inputs        |
| `latex-thesis-zh/SKILL.md`                                   | Output Contract + Required Inputs        |
| `typst-paper/SKILL.md`                                       | Output Contract + Required Inputs        |
| 三方 `references/modules/routing-rules.md`（Typst 对应文件）| 追问边界 + 契约适用范围 + 排除清单      |
| EN `references/modules/{expression,grammar,sentences}.md`    | over-claim 指针 + 契约段示例             |
| Typst `references/modules/{EXPRESSION,GRAMMAR,SENTENCES}.md` | 同上                                     |
| `tests/contracts/test_polish_contract_alignment.py`（新）    | 三方一致性断言                           |

三方 `last_updated` 更新，`version` 不动。

## 兼容性

- 契约段是**追加**，既有 `% MODULE (...) [Severity][Priority]` 行格式不变，下游解析不受影响。
- `analyze_sentences.py` 现用 `Suggested:` 而非 `Revised:`——C1 **不统一**它（那是行为改动），
  只在契约里规定新增的四个字段名一致。字段统一与否由 C2 在 design 阶段单独判断。
- 无脚本行为变化，故不触发 `.trellis/spec` 的「检查器默认行为变化须双声明」条款。

## Validation Shape

```bash
uv run --extra dev python -m pytest tests/contracts/test_polish_contract_alignment.py -q
uv run --extra dev python -m pytest tests/contracts/ -q     # ROUTER_ROW_RE 等既有锁
git diff --stat -- '*/scripts/'                             # 期望：空（C1 不改脚本）
just ci
```
