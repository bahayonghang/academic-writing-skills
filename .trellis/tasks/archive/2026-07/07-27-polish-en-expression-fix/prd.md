# C2 EN + Typst 表达链路修复

父任务：`.trellis/tasks/07-27-polish-capability-upgrade`
覆盖 findings：**P0-2、P1-4、P2-1**
触及 skill：`latex-paper-en` **与 `typst-paper`**（由 TIER1 字节锁强制同步，见下）
依赖：C1 `design.md` 已冻结（`--goal` / `--strength` / 四字段 / `Risk-Flags` 闭集）

## Goal

修复 EN 与 Typst 表达润色链路的三处实质缺陷：模块文档与脚本互相矛盾、脚本替换逻辑上下文盲且
损坏大小写、保护清单不覆盖正文里的纯文本专有名词；并落地 C1 契约。

## 为什么 typst-paper 强制在范围内

`tests/contracts/test_writing_modules_alignment.py:71-85` 的 `TIER1_HASH_GROUPS` 要求
`analyze_abstract.py` / `analyze_grammar.py` / `analyze_sentences.py` / `improve_expression.py`
在 `en` 与 `typst` 之间**整文件 sha256 一致**（实测本任务要改的三个当前均 IDENTICAL）。任何单
边改动都会让该锁变红。测试的错误信息提供了"从 `TIER1_HASH_GROUPS` 移除并文档化特化"的逃生
口——**本任务不采纳**：为省事永久牺牲对齐不变量是错误取舍。

且 typst 侧的同类问题**更重**（见 P0-2）。故 C2 = EN 修复 + Typst 逐字节镜像 + Typst 文档修复。

## Problem

### P0-2 — 文档与脚本直接矛盾（EN 与 Typst 各一份）

`scripts/improve_expression.py:27-29` 注释：

> use->employ and show->demonstrate were removed because the deai guide lists
> "we use ..." as correct and "demonstrate the effectiveness" as an AI tell (E15).

但：

- **EN** `references/modules/expression.md:5-9` 仍列 `use → employ, utilize, leverage`、
  `show → demonstrate, illustrate, indicate`。
- **Typst** `references/modules/EXPRESSION.md` 问题更多：
  1. 同样列 `use → employ`、`show → demonstrate`（4 行弱动词表）；
  2. 示例 `We use machine learning to get better results.` →
     `We employ machine learning to achieve superior performance.` 里 `get → achieve`，
     而脚本实际是 `get → obtain`——**示例与脚本二次矛盾**；
  3. 末行 `[STYLE_GUIDE.md](../references/STYLE_GUIDE.md)` 是**坏链**——从
     `references/modules/` 出发解析到 `references/references/`。同文件夹的 `DEAI.md:33` 用的
     是正确的 `../OVER_CLAIM_GUARD.md`。

由于工作流是「读模块参考 → 跑脚本」，LLM 同时收到互相矛盾的两份指令，且文档那份还会污染 LLM
自己的改写建议。

### P1-4 — 替换逻辑缺陷（实测确认，非推断）

对 `improve_expression.py:30-54` 的规则表实测：

| 输入                              | 输出                                | 判定           |
| --------------------------------- | ----------------------------------- | -------------- |
| `Make sure the model converges.`  | `develop sure the model converges.` | 大小写 + 搭配双重损坏 |
| `We make use of a pretrained encoder.` | `We develop use of a pretrained encoder.` | 搭配损坏 |
| `Only very few samples are available.` | `Only highly few samples are available.` | 搭配损坏 |
| `The results  are  aligned in   a table.` | `The results are aligned in a table.` | 空白被压缩 |
| `This makes it possible to scale.` | *（不变）*                           | **无缺陷** |

**已删除的伪 finding**：先前 PRD 断言 `\bmake\b` 会把 `makes it possible` 改坏。实测
`\bmake\b` 不匹配 `makes`（`e` 后接词字符，`\b` 不成立）。**不得为此写回归用例。**

成因：`re.sub` 配普通替换串不保留大小写；`re.IGNORECASE` 放大命中面；规则无搭配排除；
`re.sub(r"\s+", " ", revised)` 无差别压缩空白。

同类大小写损坏在 `references/modules/grammar.md:19-22` 的官方示例里就可见
（`We propose method` → `we propose a method`，首字母 `W` 丢失）。

### P2-1 — 保护清单不覆盖纯文本专有名词

`latex-paper-en/SKILL.md:110` 只保护 `\cite{}`、`\ref{}`、`\label{}`、自定义宏与数学环境。
参照 skill SKILL.md:92 另要求保持统计值、基因/蛋白名、化学名、模型名不变——这些在正文里是
**纯文本 token**（`ResNet-50`、`p < 0.05`、`CIFAR-100`、`TP53`），无 LaTeX/Typst 语法标记，
当前无任何护栏。

**但参照 skill 只给原则，未给识别方法**。C2 不得把原则当成"脚本能自动识别全部类别"来实现，
分级方案见 `design.md`。

## Requirements

### R1 — 消除文档/脚本矛盾（P0-2）

- EN `expression.md` 与 Typst `EXPRESSION.md` 的替换表与脚本实际规则**逐条一致**。
- **保留 E15 判定**：`use → employ`、`show → demonstrate` 不得恢复；文档须写明删除原因并指向
  de-AI 指南，防止后人"修回去"。
- 修 Typst `EXPRESSION.md` 的示例（使其与脚本实际规则一致）与坏链（`../STYLE_GUIDE.md`）。
- 核对剩余规则与 `references/deai/` 下 `forbidden-terms.md`、`tone-terms-en.md`（Typst 侧
  `AI_TONE_TERMS.md`）是否还有同类冲突。

### R2 — 修复替换逻辑（P1-4）

- **保大小写**：替换保留原 token 大小写形态（句首大写、全大写缩写）。
- **上下文安全**：多义动词加搭配排除，或改为只报告不自动替换（分级见 `design.md`）。
  **不允许保留当前会产出错误英文的形态。**
- **不压缩空白**：`Revised:` 行保留原始空白结构。
- 每条规则须有一个反例测试（fixture 放会误伤的句子，断言不被改坏）。

### R3 — 落地 C1 契约

- `improve_expression.py`、`analyze_grammar.py`、`analyze_sentences.py`、
  `translate_academic.py` 输出追加 C1 冻结的 `Changed` / `Protected` / `Meaning-Check` /
  `Risk-Flags` 四字段；`[Script]` 层 `Meaning-Check` 恒为 `NEEDS-LLM`。
- 实现 `--goal` / `--strength`，默认 `grammar` / `minimal`。
- `translate_academic.py` 输出形态是 Markdown 报告（`### Translation Draft` +
  `% ORIGINAL:` / `% TRANSLATION:` + `### Notes`），与其余三个的注释流不同——契约字段如何嵌入
  见 `design.md`。
- 相应更新 EN/Typst 的模块文档 Output format 示例。

### R4 — 保护 token 分级（P2-1）

- 按 `design.md` 的三级分类实现：可确定自动跳过 / 只报告候选 / 交 LLM 判断。
- 类别清单落在**一处**，SKILL.md 与模块文档只做指向，避免副本漂移。
- 被跳过的 token 通过 C1 契约的 `Protected` 字段可见，不静默。

### R5 — Typst 同步

- 三个 TIER1 脚本的每次改动**同 commit** 逐字节镜像到 `typst-paper/scripts/`。
- Typst `translate_academic.py` **不在** TIER1 锁内（实测与 EN DIFFERS），按其自身形态独立
  落地契约，不强行统一。
- Typst SKILL.md 的 Output Contract 由 C1 负责；C2 只负责其模块文档与脚本。

## Out of Scope

- 不改 `deai_check.py`（三副本，受 strict/logic 双层哈希锁保护，且只出指令不出替换文本）。
- 不改 `analyze_abstract.py`（虽同在 TIER1 锁内，但不属润色链路）。
- 不改 ZH skill 任何文件（→ C3）。
- 不统一 `analyze_sentences.py` 的 `Suggested:` 与其余的 `Revised:`——若判断需要统一，须在
  `design.md` 显式论证并作为行为变化双声明；默认不动。
- 不新增 reviewer-response 能力。

## Constraints

- **TIER1 字节锁**：三个脚本 en/typst 必须整文件 sha256 一致，按成员级镜像会漏掉空白/顺序差异
  仍会红。
- `scripts/parsers.py` 的 EN 副本是 `test_parsers_alignment` 的 canonical copy；**优先不改**
  `parsers.py`，若必须改则同步评估 zh/typst/cover_letter 副本与 `ALIGNMENTS`。
- 检查器默认行为变化只允许"误报/假绿修复"例外，且须在 commit message 双声明——R2 的修复属此类，
  须按规执行并同 commit 更新受影响的存量用例。
- 改 `evals.json` 走 Bash python 写入；不给 pytest 加 `PYTHONIOENCODING=utf-8`。
- 只改 `last_updated`，不 bump `version`。

## Acceptance Criteria

- [ ] EN `expression.md` 与 Typst `EXPRESSION.md` 的替换表与脚本逐条一致，均写明 E15 删除原因
- [ ] Typst `EXPRESSION.md` 的示例与脚本规则一致（`get → obtain` 非 `achieve`），坏链已修为
      `../STYLE_GUIDE.md`
- [ ] 回归测试：句首大写 token 替换后大小写不损坏
- [ ] 回归测试：`Make sure` / `make use of` / `very few` 不被改成错误英文
- [ ] 回归测试：`Revised:` 行不压缩原始空白
- [ ] **不存在** `makes it possible` 相关用例（已证伪）
- [ ] 四个脚本输出含 C1 四字段，`[Script]` 层 `Meaning-Check` 恒为 `NEEDS-LLM`
- [ ] `--goal` / `--strength` 可用，默认 `grammar` / `minimal`
- [ ] 保护 token 三级分类实现，清单单点定义，跳过项经 `Protected` 字段可见
- [ ] `test_writing_modules_alignment` 绿：三个脚本 en/typst 整文件哈希一致
- [ ] `git diff -- '*/scripts/deai_check.py' '*/scripts/analyze_abstract.py'` 为空
- [ ] `just ci` 全绿，passed ≥ 1338，pyright error = 0
