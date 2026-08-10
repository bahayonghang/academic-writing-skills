# Design: academic de-AI pattern clusters 与保真闭环

## 1. Boundary And Ownership

保持现有模块架构，不创建 `writing-anti-ai` 的仓库内副本：

- `latex-paper-en`：英文 canonical 语义与 LaTeX 保护；
- `latex-thesis-zh`：中文学位论文语域与 LaTeX 保护；
- `typst-paper`：中英文 pattern 适配与 Typst 保护；
- `.trellis/spec/academic-writing-skills`：跨 surface 的 H-* / F-* 开发契约；
- docs resource pipeline：公开 source 的双语镜像与 manifest。

`paper-audit` 不在本任务修改范围。若审阅发现 unsupported extrapolation 或 claim wording
outruns evidence，沿用既有 claim-evidence lane；纯风格 finding 留在 de-AI，不争用 max-8 配额。

## 2. Progressive Disclosure Shape

每个 skill 增加一个详细 reference：

| Skill | New detailed source | Existing entry points to update |
| --- | --- | --- |
| latex-paper-en | `references/deai/pattern-clusters.md` | `references/deai/guide.md`, `references/modules/deai.md` |
| latex-thesis-zh | `references/deai/pattern-clusters.md` | `references/deai/guide.md`, `references/modules/deai.md` |
| typst-paper | `references/DEAI_PATTERN_CLUSTERS.md` | `references/DEAI_GUIDE.md`, `references/modules/DEAI.md` |

entry point 只说明何时加载和共同边界；详细判据、反例和 workflow 单点定义在新 reference。
不修改 `SKILL.md` 路由，因为 de-AI module 已可达，重复表格会产生第四份事实来源。

## 3. Judgment Model

LLM 对每个候选位置先抽取：

1. `source_span`：实际触发的句/段，不以整章作为证据；
2. `rhetorical_move`：评价、归因、范围、谓词关系、术语替换或 outlook；
3. `claim`：该修辞实际增加或改变的主张；
4. `evidence_anchor`：数字、比较、figure/table、实验、引用或可见定义；
5. `scope_and_certainty`：适用条件、hedge、limitation、certainty rung；
6. `protected_units`：语法锚点、术语、数字、引用、实体与 source layout。

随后才按 `research/delta-matrix.md` 判断 H-ING、H-PROMO、H-ATTR、H-PRED、H-TERM、
H-SCOPE、H-OUTLOOK。finding 必须说明“修辞 move 与证据/含义的关系”，不能输出“这个词像
AI”或“AI probability”。

所有 H-* 均为 C 档 `llm-only`：单词、词尾、标点和枚举数量都不能完成上述抽取。因此不向
`DEFAULT_THRESHOLDS`、`DIMENSION_MAP`、pattern tables 或 YAML 添加类别。

### Cross-contract ownership and deduplication

H-OUTLOOK 只处理 challenge/limitation 后没有具体结果、行动、条件或边界的积极回弹。
defensive-rhetoric 契约处理的是多个具体机制、逐项证据/区分检验缺口与 terminal caveat 的
组合。诚实的 `mechanism undetermined` 和 scope limitation 均不是 H-OUTLOOK。

同一 Discussion 段同时满足两者时，先按根因和 repair 去重：同一 claim-evidence 缺口只输出
一条 finding；满足 defensive 组合判据时以 evidence-calibration finding 为 primary，空泛 outlook
只作为 secondary style facet。只有 source span、根因和 repair 可分别定位时才允许两条 finding，
且 style-only H-OUTLOOK 不进入 `paper-audit` lane。

## 4. Rewrite And Fidelity Data Flow

```text
visible prose
  -> protect syntax and academic payload
  -> claim-local H-* audit
  -> findings / blueprint (default stop)
  -> explicit prose request?
       no  -> return audit
       yes -> local rewrite
              -> fidelity audit
              -> four-field proposal + unresolved risks
```

“信息优先于原修辞结构”允许删除修辞壳、合并同义句或拆分过载句，但不等于授权重排章节。
默认保留 source layout；跨段或章节重构需要用户另行授权。

### Fidelity audit

对改写前后的 ledger 做逐项集合核对：

- `claims_before - claims_after`：只能是明确说明的删除/降级，不能静默丢失；
- `claims_after - claims_before`：必须为空，否则 `invented-claim`；
- 数字、单位、引用、标签、公式、术语和实体逐项相等；
- certainty 不得上升；hedge 合并只消除重复，不删除真实不确定性；
- scope/limitation 不得扩大或消失。

输出复用：

```text
Changed: <what changed>
Protected: <anchors and academic payload kept>
Meaning-Check: PRESERVED | NEEDS-LLM
Risk-Flags: <existing closed set>
```

`PRESERVED` 只是 `[LLM]` 建议层结论，不是工具验证或作者批准。

## 5. Author Sample Calibration

作者样本是可选的 style constraint，优先级低于：

1. 用户本次明确要求；
2. 目标 venue/学术体裁；
3. 术语表、引用和语法保护；
4. claim-evidence、certainty 和 scope；
5. 作者样本中的节奏、句法和语气偏好。

样本不得提供新的事实或主张，也不得因为样本含第一人称/幽默就把这些特征注入目标稿。
没有样本时使用目标 skill 的既有 academic tone，不推测作者人格。

## 6. Runtime And Documentation Surface

计划修改 9 个 public source（3 个新增、6 个 entry point），对应 18 个双语 docs target，并更新
manifest。另新增：

- `.trellis/spec/academic-writing-skills/deai-pattern-cluster-contract.md` 与 index 条目；
- `tests/contracts/test_deai_pattern_cluster_contract.py`；
- 三个本地 composite fixture；
- 三份 `evals/evals.json` 的 append-only 新条目。

不修改脚本、threshold、tone-term reference、batch、CLI、frontmatter、schema、依赖或
paper-audit 文件。路径差异保持原样：EN/ZH 阈值在 `references/deai/tone-thresholds.yaml`，
Typst 阈值与术语说明分别在 `references/AI_TONE_THRESHOLDS.yaml` 和
`references/AI_TONE_TERMS.md`。

## 7. Eval Design

每个 surface 的 fixture 必须本地包含以下可区分 case：

| Case | 内容 | Expected |
| --- | --- | --- |
| A | 一个段落组合无证据尾句、宣传评价、模糊归因、虚假范围与空泛结尾 | 命中 H-ING/H-PROMO/H-ATTR/H-SCOPE/H-OUTLOOK；不以“AI 作者”表述 |
| B | `serves as / represents / marks` 等间接谓词只延长句子，没有技术关系 | 命中 H-PRED，并给关系不变的简化建议 |
| C | 同一 domain entity 在短距离内无定义地循环换名并造成范围歧义 | 命中 H-TERM，恢复 canonical term，不改实体含义 |
| D | 有 metric/citation anchor 的 participial implication 与评价 | 不报 H-ING/H-PROMO |
| E | 具名、可解析引用和明确 scope 的 attribution | 不报 H-ATTR |
| F | 三项均真实必要且范围精确的贡献/实验枚举 | 不报 H-SCOPE，不为 rule of three 强制增删 |
| G | `represents`/系动关系具有精确技术语义，术语切换有显式定义 | 不报 H-PRED/H-TERM |
| H | 诚实 limitation + 具体 future test 或 scope-bounded conclusion | 不报 H-OUTLOOK，不删 hedge |

eval 断言至少覆盖：路由到 deai、A-C 对七模式的应命中语义、D-H 的证据充分边界、
`Changed/Protected/Meaning-Check/Risk-Flags`、跨契约去重与不虚构。fixture 真实路径必须写入
`files`；ID 取当前最大值 + 1，只追加、不填空洞、不重排。

静态 eval/contract test 只证明契约和样例存在。provider 输出、precision/recall、作者盲评和真实
论文效果仍为 `missing evidence / UNVERIFIED`。

## 8. Compatibility, Rollout, Rollback

- 兼容：默认 CLI 和脚本输出零变化；新增内容只在 LLM 读取 de-AI reference 时生效。
- rollout：先落 canonical EN + spec/test，再落 ZH、Typst 语言适配，最后同步 docs/manifest 与全量
  校验；每步都以反例保护优先。
- rollback：按“source + 双语 docs + manifest”成组回滚；fixture 与 eval 成组回滚；最后回滚
  contract test/spec。没有数据库或外部状态迁移。
- 未来脚本化：必须另建任务，以真实学术语料证明高精度、明确排除条件和默认兼容；新能力放
  显式 flag 后，且不得复用 `--tier` 表示编辑幅度。
