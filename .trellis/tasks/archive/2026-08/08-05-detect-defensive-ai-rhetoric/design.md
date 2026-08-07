# Design: 防御性 AI 话术识别

## 1. Boundary And Task Shape

本任务扩展既有 skill 的判断契约、公开 references、双语文档与 output eval，不扩展确定性脚本：

- `deai`：识别复合修辞及其 AI 味，给局部诊断或改写蓝图。
- `experiment`：判断 Discussion 中候选机制是否有实验、消融、对照或文献证据。
- `paper-audit/claims_vs_evidence`：在全文审阅中判断解释是否超出可见证据，并按论证影响定严重度。
- `.trellis/spec/academic-writing-skills`：保存跨 surface 的开发约定与正反例。

保持单一 Trellis 任务，不拆 child：四个 surface 共享同一语义契约和一组跨 surface acceptance，资源同步必须与 source 原子落地；拆分会让某个可安装 skill 暂时暴露不一致行为或过期双语页面。

## 2. Judgment Contract

### Input decomposition

`[LLM]` 先把段落拆为：

1. `observation`：结果或现象原文；
2. `candidate_explanations`：每个机制/原因，不因 `may/could/可能` 自动变成安全；
3. `evidence_anchors`：指标、图表、消融、受控对比、引用或分析 artifact；
4. `discriminators`：什么观察能区分候选解释；
5. `epistemic_status`：`supported | consistent | speculative | undetermined`；
6. `terminal_caveat`：是否用一句免责声明整体撤回前述机制。

### Classification

只有以下组合才命中 `defensive_speculative_explanation`：

- 至少两个具体 candidate explanation；
- 至少一个解释缺少可见 evidence anchor，且没有 discriminator；
- terminal caveat 表示当前设计/数据不能验证这些解释；
- 该段仍把这些机制写成主要结果解释，而不是明确的未来假设清单。

该标签是内部契约名，不要求暴露给所有用户。finding 应描述实质问题，例如“多个机制未逐项绑定证据，末句免责声明不能替代验证”。

### Boundary With Existing Script Advice

`deai_check.py` 的 `hedge` / `hedge_application` 建议保持有效：它们分别修复过度自信措辞和未演示应用。新契约处理的是另一维度：候选机制是否逐项获得证据。添加 `results suggest`、`may/could` 或“可能/或许”只能降低单项 claim 的强度，不能补足 evidence anchor、discriminator，也不能让机制枚举自动通过。

## 3. Repair Policy

修复按最小变更从上到下选择：

1. 保留 observation 原句与数值边界。
2. 若一项解释有最接近的证据，只保留该项，写明 anchor，并使用证据允许的 certainty rung。
3. 若多项解释都有证据，逐项绑定；篇幅过载时拆句或移入单独假设段。
4. 若没有任何解释有证据，删去具体机制枚举，直接写“当前设计不能识别该差异的原因”。
5. 需要保留的备选机制转为未来工作，并说明验证它需要的消融、分层分析或对照。

现有 “stance-less discussion” 规则改为条件分支：证据能区分候选解释时明确较可信者及理由；证据不能区分时明确 `undetermined`，不得为了“有立场”制造过度声称。禁止把“删掉 caveat”与“写得更肯定”单独视为修复。

## 4. Exact Runtime And Documentation Surface

以下 13 个公开 source 全部已登记在 `docs/resource-manifest.json`；实施须按记录的 `sourceLocale` 写作，并同步每个 source 的 EN/ZH target，共 26 个页面。

| Skill | Source | Locale | Purpose |
| --- | --- | --- | --- |
| latex-paper-en | `references/deai/guide.md` | en | 完整判断、反例、stance-less 修复 |
| latex-paper-en | `references/modules/deai.md` | en | module 路由与脚本 hedge 边界 |
| latex-paper-en | `references/modules/experiment.md` | en | Discussion 逐机制证据要求 |
| latex-thesis-zh | `references/deai/guide.md` | zh | 完整中文判断、反例、stance-less 修复 |
| latex-thesis-zh | `references/modules/deai.md` | en | 保持英文 source，不擅自改成中文 |
| latex-thesis-zh | `references/modules/experiment.md` | zh | 中文 Discussion 证据要求 |
| typst-paper | `references/DEAI_GUIDE.md` | en | 完整判断、反例、stance-less 修复 |
| typst-paper | `references/modules/DEAI.md` | zh | 中文 module 路由与脚本 hedge 边界 |
| typst-paper | `references/modules/EXPERIMENT.md` | en | Typst Discussion 证据要求 |
| paper-audit | `references/CLAIM_EVIDENCE_CONTRACT.md` | en | evidence anchor 与推断状态 |
| paper-audit | `references/OVER_CLAIM_GUARD.md` | en | hedge/反向校准边界 |
| paper-audit | `references/SUBAGENT_TEMPLATES.md` | en | 实际 claims lane prompt 与 max-8 排序 |
| paper-audit | `agents/claims_evidence_reviewer_agent.md` | en | reviewer persona/独立 agent 对齐 |

不修改 `deai_check.py`、threshold YAML、CLI、frontmatter 或 issue schema。manifest 通过 `--write-manifest --inventory-only` 重建散列后，必须审查上述 13 条 `sourceLocale` 未漂移。

## 5. Paper-Audit Lane Saturation

目标模式属于 `unsupported extrapolation` / claim wording outruns evidence 的具体形态，不增加第 5 个并列配额。`claims_vs_evidence` 达到 max 8 时：

1. 先按 `Critical/Major > Moderate > Minor` 和 gate/中心结论影响排序；
2. 同级先保留无证据的中心主张，再保留影响主要 Discussion 解释的机制堆叠；
3. 同一根因的多个位置合并为一条 finding，保留所有 example locations；
4. 只影响局部措辞、没有改变 claim-evidence 关系的 AI 风格 finding 可被省略。

这与 `SUBAGENT_TEMPLATES.md` 现有 “surface only the strongest gaps” 和 recurring-issue collapse 一致。

## 6. Eval Design

每个 surface 新增一个本地组合 fixture 和一个 append-only eval；一个 fixture 内放置五个明确区分的 case，避免创建 20 条碎片 eval：

| Case | EN | ZH | Typst | paper-audit | Expected |
| --- | --- | --- | --- | --- | --- |
| 多机制 + 无逐项证据 + 总括撤回 | required | required | required | required | 命中并给 evidence-calibrated repair |
| 单一解释 + 局部证据 + 合理 hedge | required | required | required | required | 不误报 |
| 多假设 + 逐项证据 + discriminator | required | required | required | required | 不按 AI 味误报 |
| 明确“原因未定”且不列机制 | required | required | required | required | 保留诚实限制 |
| 受控实验支持强机制措辞 | required | required | required | required | 不强制降级或加 caveat |

四条新 eval 的 `files` 均非空并指向各自新 fixture；这对 paper-audit 是已有硬契约，对另三套 skill 是本任务主动采用的更强回归要求。新 eval 使用当前最大 ID + 1 追加，不填补空洞、不重排既有项。contract test 通过唯一 fixture 路径和 prompt 语义定位，不依赖整数 ID。

## 7. Compatibility, Evidence, And Rollback

- 兼容：references/evals/fixtures/contract-test/spec/docs/manifest 变更；无 API、CLI、schema、依赖或脚本输出变化。
- 文档：`just ci` 只保证 inventory 散列等硬契约，最终完成还需 affected skill/full resource checker 和 `just doc-build`。
- 回滚：每个 source 与其 EN/ZH target 成组回滚；fixture 与 eval 成组回滚；最后回滚 manifest 与 Trellis spec/index。
- 缺失证据：静态 contract test 只能证明资源存在且契约一致，不能证明任一 provider 的真实输出质量。未执行的 provider eval 必须明确标为 `missing evidence`。
