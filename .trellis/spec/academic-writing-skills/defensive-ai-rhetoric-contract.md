# 防御性推测解释契约

> 适用于 `latex-paper-en`、`latex-thesis-zh`、`typst-paper` 的 de-AI / experiment
> references，以及 `paper-audit` 的 claims-vs-evidence lane。

## Contract: 只按组合行为识别防御性推测解释

**What**：`[LLM]` 必须先把讨论段拆成 `observation`、`candidate_explanations`、
`evidence_anchors`、`discriminators`、`epistemic_status` 与 `terminal_caveat`。只有以下信号
组合出现时，才把段落视为防御性推测解释：

1. 一个观察结果后列出两个或更多具体机制或原因；
2. 至少一项机制没有局部 evidence anchor，也没有区分候选解释的检验；
3. 段尾 caveat 声明当前数据或比较无法验证这些机制；
4. 这些机制仍被当作主要结果解释，而不是显式、可检验的未来假设。

**Automation boundary**：这是 C 档 `llm-only` 判断。不得在三份 `deai_check.py` 中为
`may`、`could`、`可能`、`假设`、`未验证`、句长、连接词或 hedge 数量新增正则或阈值。
单个词面信号不能完成段落级证据映射。

现有脚本的 `hedge` / `hedge_application` 建议仍然有效：它们用于降低过度自信措辞或
未演示应用的确定性。`results suggest`、`may / could` 与“可能/或许”只校准单项 claim
的强度，不会创造 evidence anchor，也不构成机制堆叠的许可。

**Tests Required**：

- `tests/contracts/test_defensive_ai_rhetoric_contract.py` 必须逐文件锁定 13 个 runtime
  source 的组合判据、脚本建议边界和 `[LLM]` 归属。
- `tests/contracts/test_deai_alignment.py` 必须继续通过，三份 `deai_check.py` 不得出现行为
  diff。

## Contract: 修复不得提高证据未赚到的确定性

按最小改动依次处理：

1. 保留 observation、数值、引用、标签、公式与适用边界。
2. 某项解释有最接近的证据时，只保留该项并明确 evidence anchor 与 certainty rung。
3. 多项解释都有证据时逐项绑定；必要时拆句或移入独立假设段。
4. 没有任何解释得到支持时，删去具体机制枚举，直接说明机制 `undetermined`。
5. 必须保留的备选解释进入未来工作，并写出所需消融、对照或分层分析。

禁止把“删除最后的 caveat”或“写得更肯定”单独视为修复；不得发明消融、对照、指标、
引用或机制证据。原有 stance-less discussion 规则也采用条件分支：证据能区分时选择较可信
解释并说明理由；不能区分时明确原因未定。

### Wrong vs Correct

```text
Wrong: 结果提升。可能是机制 A，也可能是机制 B；现有数据无法验证。删掉末句并改成“机制 A 导致提升”。
Correct: 结果提升。当前设计不能确定形成该差异的机制。
```

## Convention: 每个 surface 本地保护全部边界

每个 EN、ZH、Typst 与 paper-audit 组合 fixture 必须同时包含以下五种情况，不能依赖跨
surface 并集：

| Case | 本地证据形态 | 预期 |
| --- | --- | --- |
| 目标正例 | 多机制、无逐项证据、末句整体撤回 | 命中并给证据校准修复 |
| 合理 hedge | 单一解释且有局部 evidence anchor | 不误报 |
| 有证据的多假设 | 每项都有证据和 discriminator | 不误报 |
| 诚实未知 | 简洁说明机制未定，不枚举具体原因 | 保留限制 |
| 受控强结论 | 干预或消融支持机制措辞 | 不强制降级 |

新 eval 必须绑定真实 fixture，只追加、不重排、不复用 paper-audit 的历史 ID 空洞。测试通过
唯一 fixture 路径和 prompt 语义定位，不把整数 ID 当作长期行为锚点。

**Validation**：四份 eval JSON 均可由 `json.loads` 解析、ID 唯一、新用例位于数组末尾，且
fixture 中五个 case 都能从对应 skill 本地读取。静态 fixture 只证明契约和回归样例存在；
未执行 provider-backed output eval 时，模型效果必须标为 `missing evidence`。

## Convention: paper-audit 复用既有 lane 与 issue budget

目标模式属于 `unsupported extrapolation` / claim wording outruns evidence 的具体形态，
不得新增 schema 字段或独立配额。`claims_vs_evidence` 达到 max 8 时：

1. 先按中心主张或 gate 影响排序，再比较 severity 与 evidence-gap size；
2. 同一根因的多处机制堆叠合并成一条 finding，并保留多个位置；
3. 只影响局部 AI 语气、没有改变 claim-evidence 关系的 finding 先省略。

**Tests Required**：contract test 必须同时检查 `CLAIM_EVIDENCE_CONTRACT.md`、
`OVER_CLAIM_GUARD.md`、`SUBAGENT_TEMPLATES.md` 和 reviewer agent 中的 subtype、max-8、
重复位置合并与 style-only 让位规则。
