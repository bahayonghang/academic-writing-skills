# 设计：claim-forward 四类处置与改写侧立场保真

本设计按 PRD 的建议决策（D1 新增标记、D2 不移植 Typst 模块、D3 不给新码、D4 不动词表、
D5 不动 paper-audit）编写。评审若改变任一决策，先改本文件对应小节再实施。

## 1. 边界与文件归属

三个阶段各自可独立验证，按 P1 → P2 → P3 顺序串行。阶段内文件只由该阶段写。

### P1 改写侧立场保真（三方契约）

| 文件 | 改动 |
|---|---|
| `latex-paper-en/SKILL.md`、`latex-thesis-zh/SKILL.md`、`typst-paper/SKILL.md` | `Risk-Flags` 行加 `understatement`；紧随其后的强度规则改为双向 |
| `latex-paper-en/references/modules/{routing-rules,expression,grammar,sentences,translation}.md` | 强度规则改为双向，指向 over-claim-guard |
| `typst-paper/references/modules/{EXPRESSION,GRAMMAR,SENTENCES,TRANSLATION}.md`、`typst-paper/references/skill-routing-notes.md` | 同上 |
| `latex-thesis-zh/references/modules/{routing-rules,expression,polish}.md`、`references/writing/unit-polish-zh.md` | 枚举行加值；`unit-polish-zh.md` 已有双向规则，只对齐标记名 |
| 三份 `pattern-clusters` 文档（EN、ZH、Typst） | `Risk-Flags` 枚举行加值；保真复核句补"或降低 certainty" |
| `tests/contracts/test_polish_contract_alignment.py`、`test_deai_pattern_cluster_contract.py` | `RISK_FLAGS` 加值；`SCRIPT_SETTABLE_FLAGS` 不变；新增双向规则存在性断言 |
| `.trellis/spec/academic-writing-skills/polish-rewrite-contract.md` | 四字段闭集与分层表更新 |

### P2 claim-forward 指南（EN、ZH）

| 文件 | 改动 |
|---|---|
| `latex-thesis-zh/references/writing/claim-forward-zh.md` | 在"防御性说明的三类处置"后新增四类处置、修复顺序、去重规则 |
| `latex-paper-en/references/writing/claim-forward.md` | 新增三类处置（对齐中文）加同样的四类处置 |
| 两份 `references/modules/claim-forward.md` | 触发词、仅 LLM 判断清单、零发现合法、与 deai 和 over-claim-guard 的边界 |
| 两份 `references/modules/deai.md` | 边界句补"预设反驳壳、让步后否定交给 claim-forward 与 over-claim-guard" |
| EN `references/evidence/over-claim-guard.md`、ZH `references/writing/over-claim-guard.md` | "向上校准"节后补一段：让步后否定属向下校准，指回本节与 claim-forward 指南 |
| `tests/contracts/test_claim_forward_contract.py`、`test_thesis_zh_guidance_fidelity.py` | 新增独立断言，不改既有断言 |
| `.trellis/spec/academic-writing-skills/claim-forward-contract.md` | §3.1 扩为七类文档层处置；写明仍不新增码 |
| `.trellis/spec/academic-writing-skills/deai-pattern-cluster-contract.md` | 仅把 `Risk-Flags` 旧八值枚举同步为九值（P1 评审发现的遗留，2026-11-11 并入） |

### P3 路由、eval、示例与镜像

| 文件 | 改动 |
|---|---|
| 两份 `SKILL.md`（EN、ZH） | 路由行与路由说明补触发说法；`last_updated`；描述在 400 字符内微调 |
| `typst-paper/SKILL.md` | 仅 `last_updated`（P1 已改契约行） |
| 三份 `evals/evals.json`、EN/ZH `evals/trigger_eval.json` | 追加条目 |
| `latex-paper-en/evals/fixtures/claim_forward_shell_cases.tex`、`latex-thesis-zh/evals/fixtures/claim_forward_shell_cases_zh.tex` | 新增合成 fixture |
| `latex-paper-en/examples/claim-forward-shells.md`、`latex-thesis-zh/examples/claim-forward-shells.md` | 新增示例文档 |
| `docs/skills/**`、`docs/zh/skills/**`、`docs/resource-manifest.json`、`docs/usage.md`、`docs/zh/usage.md` | 镜像、译文、manifest |
| `README.md`、`README_CN.md` | 仅在已有的"LLM 判读"段落后各补一句，说明四类处置与双向强度规则（2026-11-11 P2 评审并入） |
| `.trellis/spec/academic-writing-skills/index.md`、`claim-forward-contract.md` §8 | 索引行"三类处置"改为"七类处置"；§8 补列新增测试函数（P2 评审发现的遗留） |
| `tests/contracts/test_subsection_context_contract.py` | 仅把钉住中文 `SKILL.md` 的 `last_updated` 日期断言同步为 `2026-11-11`（P3 评审并入，主会话直接修改） |
| 四个 skill 的 docs index 页、`typst-paper/evals/fixtures/stance_fidelity_cases.typ` | 新示例的导航链接；Typst eval 17 的合成 fixture（P3 实施时新增，评审接受） |
| 两份 claim-forward 指南中"让步后否定"的中文示例 | 更换示例领域，避开与来源文章案例相近的用词（P2 评审意见） |

写入白名单之外的文件即越界，先停下回到规划。全部 `scripts/`、两份词表、paper-audit 目录不在任何阶段的白名单内。

## 2. 四类处置的文档机制

沿用中文指南"三类处置"的体例：每类一个三级标题，含**范围**、**可保留**、**不可改**三行，
末尾附 `[LLM]` 建议块。四类都只由 LLM 判断。

| 处置 | 判据（同时满足才成立） | 去向 | 不可改 |
|---|---|---|---|
| 预设反驳壳 | 句子回应的异议在稿件数据与所引文献中都找不到来源；回应本身没有证据、条件或范围 | 有真实混杂时改写为一条带原因的具体边界；无真实异议时删壳留主张；定义性区分保留 | 把壳删掉的同时抬高动词；把"材料不能说明什么"删掉 |
| 让步后否定 | 让步从句指向稿件中真实存在的差异或混杂；主句不给分析就否定其影响 | 稿件有分析则绑定该分析；无分析则把结论收回到数据支持的范围或标【待补证】 | 删除让步句；补造对照、分层或显著性结论 |
| 断言与让步壳共现 | 同一段内既有高于证据等级的动词，又有模糊让步 | 固定三步：证据前置 → 按阶梯校准断言 → 模糊让步换成具体边界 | 只做第三步；把两处拆成两条 finding 重复计数 |
| 空泛谦辞 | 限制句没有对象，也没有条件或量值，且不是结论章已写出具体局限的承接句 | 从稿件补对象与条件；稿件没有则标【待补证】；与已有限制重复则删副本 | 删掉唯一一处限制；替作者编一个局限 |

合成短例（自写，仅示意体例，实施时按各语种语境展开）：

```latex
% 主张前置（合成）[Severity: Minor] [Priority: P2]: [LLM] 断言与让步壳共现
% 原文：问卷结果充分证明排班方式是离职意向的决定因素。当然，不能简单地认为所有科室都如此，
%       但总体而言该因素在一定程度上起到了关键作用。
% 修改后：312 份有效问卷中，轮班组的离职意向得分高于固定班组（表 4-2）。
%         问卷为单一时点的横断面数据，现有结果不能区分排班方式与科室工作量各自的影响。
% 理由：先把"充分证明…决定因素"收回到表 4-2 支持的比较，再把模糊让步换成一条带原因的边界。
%       修改后断言强度低于原文；数字与表号来自稿件，未新增结论。
```

修复顺序是本任务唯一新增的流程规则，写进指南的"五步改写"之后作为第六条说明，不改五步本身。

### 去重

- 清嗓子引导语（值得注意的是）仍归 `deai`；同一句同时含引导语和预设反驳壳时，
  `deai` 只报引导语，壳的处置在 claim-forward 输出。
- 三个及以上 hedge 且脚本已报 `CF-HEDGE-STACK` 的句子若同时构成让步壳，合并为一条，
  以壳的处置为主，hedge 计数作为佐证。
- 多机制堆叠加末尾统一撤回仍按 `defensive-ai-rhetoric-contract.md` 归 `deai`，本任务不重叠。

## 3. 立场保真的契约机制

闭集变为九个值，新值 `understatement` 排在 `overstatement` 之后。

| 层 | 可置的值 |
|---|---|
| `[Script]` | 不变：`none` / `not-assessed` / `lexical-substitution` / `whitespace-normalized` |
| `[LLM]` | 全闭集，含 `understatement` |

规则文字（三方同义，英文与中文各一份）：

1. 改写不得升高也不得降低措辞强度。强度发生变化时置 `overstatement` 或 `understatement` 并说明依据。
2. 没有证据理由时保持原强度。
3. 原文断言强于证据时，输出过度声称 finding（判据见 over-claim-guard），改写块保持原强度；
   只有用户明确要求校准时才给降强度的改写，并置 `understatement`。
4. `deai` 脚本的 `hedge` 建议只对缺少证据等级的断言生效；断言落在"反向校准"清单内时保持原样。

第 3 条使"立场保真"不变成抬高断言的许可：它管的是静默改动，不管是否该校准。

脚本不变的理由：TIER1 四脚本与 `check_style_zh.py` 只输出 `[Script]` 可置的四个值，不含完整枚举；
实施第一步用 `grep` 再核一次，若发现脚本内嵌完整枚举则停下回到规划。

## 4. 路由与触发

- 新模块行：无。四类处置都在既有 `claim-forward` 行下。
- ZH 触发说法：去除防御性表述、防御性写作、预设辩解、先让步再解释、观点被润色磨平。
- EN 触发说法：defensive writing、pre-emptive rebuttal、over-hedged、concession that dismisses a confound、
  polish flattened the argument。
- 边界查询：包含"多个可能机制、最后说无法验证"的请求应路由到 `deai`，不到 `claim-forward`。
- 描述预算：EN 仅余 27 字符，触发说法主要放路由行与模块文档；描述只做等长替换。

## 5. Fixture 与 eval

每份 fixture 八个带标签的段落：

| 样例 | 形态 | 期望 |
|---|---|---|
| A | 预设反驳壳，无真实异议 | 删壳留主张 |
| B | 让步后否定，分母变化 | 保留让步，结论收回，转结果分析 |
| C | 断言与让步壳共现，质性证据 | 三步修复，一条 finding |
| D | 空泛谦辞 | 补对象与条件或【待补证】 |
| E | 带原因的真实证据边界 | 保持不动 |
| F | 定义性否定 | 保持不动 |
| G | 对带引用的前人工作的让步 | 保持不动 |
| H | 结论章写出具体局限的承接句加展望 | 保持不动 |

eval 编号：EN 25、ZH 61、Typst 17（Typst 一条只测立场保真：改写不得新增 hedge 或缩窄范围）。
断言沿用现有 `regex` 与 `not_contains` 两种类型。`evals.json` 用 Python 读写并保持各文件原有换行与缩进风格。
新 fixture 不改变现有脚本测试：`check_claim_forward.py` 的测试只读原有 fixture。

## 6. 兼容性

- `Risk-Flags` 加值是向后兼容的扩展：旧输出仍合法，没有脚本解析该枚举。
- 四类处置不改变任何脚本输出，默认行为零变化。
- 文档站镜像按 `docs-bilingual-resources.md`：同语言页面与源一致，另一语言完整翻译，
  manifest 重建后仍须跑完整检查。

## 7. 回滚

按阶段逆序回退：P3（eval、示例、镜像）→ P2（指南、spec、断言）→ P1（枚举、契约测试）。
P1 的枚举改动三方锁定，必须整组回退。每阶段一个提交，回滚点即提交边界。

## 8. 证据口径

契约测试与结构检查只能证明规则文本和 eval 条目存在。四类处置与 `understatement`
的实际执行效果依赖模型，未做 provider 实跑与真实论文评估前一律记 UNVERIFIED。
