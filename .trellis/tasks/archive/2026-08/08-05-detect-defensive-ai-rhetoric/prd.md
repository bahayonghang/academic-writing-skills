# 强化防御性 AI 话术识别

## Goal

让英文论文、中文学位论文、Typst 论文与 `paper-audit` 能识别并修复一种现有规则未明确覆盖的 AI 写作痕迹：作者在证据不足时连续提出多个具体机制或原因，再用“当前数据/比较无法验证这些机制”整体撤回，使段落形式上谨慎、实质上却没有完成可核查的解释。

## User Value

用户应得到证据校准后的讨论段，而不是两种同样有害的结果：一是继续堆叠 `may/could/可能` 与免责声明，二是删掉限定并把未证实推断写得更肯定。skill 应保留真正的学术不确定性，同时压缩没有证据锚点的机制叙事。

## Confirmed Facts

- 三套写作 skill 已有 claim-evidence-first / 学术人味契约，并要求保留事实、主张、逻辑与边界（EN 模块见 `academic-writing-skills/latex-paper-en/references/modules/deai.md:29`；ZH 见 `academic-writing-skills/latex-thesis-zh/references/modules/deai.md:13`；Typst 见 `academic-writing-skills/typst-paper/references/modules/DEAI.md:35`）。
- 现有指南要求对推测使用适当限定，同时要求 Discussion “解释机制”；两条原则若缺少组合判据，可能共同生成本任务要处理的句式（EN 见 `academic-writing-skills/latex-paper-en/references/deai/guide.md:69`、`:401`；ZH 见 `academic-writing-skills/latex-thesis-zh/references/deai/guide.md:71`、`:441`；Typst 见 `academic-writing-skills/typst-paper/references/DEAI_GUIDE.md:66`、`:334`）。
- 三套指南都能识别“无立场讨论”，但当前修复都要求作者明确表态，没有处理“证据不足时应明确机制未定”的分支（EN `academic-writing-skills/latex-paper-en/references/deai/guide.md:174`、`:177`；ZH `academic-writing-skills/latex-thesis-zh/references/deai/guide.md:218`、`:221`；Typst `academic-writing-skills/typst-paper/references/DEAI_GUIDE.md:172`、`:175`）。
- 三份 `deai_check.py` 仅对过度自信措辞和未演示应用建议添加限定语；EN/Typst 的 `hedge_application` 明示 `may / could`，ZH 明示“可能/或许”。这些建议针对不同风险，仍然正确，但现有文档没有声明它们不构成多机制堆叠的许可。
- `paper-audit` 的 claims-vs-evidence lane 当前关注 overclaim、unsupported extrapolation、措辞强于证据和 missing caveats（`academic-writing-skills/paper-audit/agents/claims_evidence_reviewer_agent.md:7`）。实际 deep-review lane 指令还来自 `references/SUBAGENT_TEMPLATES.md:64`，并受 max 8 issues 限制（`:90`）。
- 当前 output eval 覆盖结构壳、时态、overclaim 与普通 claim-evidence 校准，但没有本任务的正例或边界反例（EN `academic-writing-skills/latex-paper-en/evals/evals.json:467`；ZH `academic-writing-skills/latex-thesis-zh/evals/evals.json:529`；Typst `academic-writing-skills/typst-paper/evals/evals.json:286`；audit `academic-writing-skills/paper-audit/evals/evals.json:247`）。
- `paper-audit` 的每条 eval 都必须绑定存在的 fixture；EN/ZH/Typst 的通用 shape 只要求 `files` 为列表，但本任务需要更强的本地回归约束。
- 本任务会修改 13 个 manifest 登记的公开 source，必须同步 26 个 EN/ZH target 页面与 `sourceSha256`。`just ci` 会通过 inventory contract 检查散列；完整页面一致性另需逐 skill/full resource checker 与 VitePress build。
- 现有规范把依赖上下文语义的规则归为 C 档 `llm-only`，脚本不得假装能判定（`.trellis/spec/academic-writing-skills/polish-rewrite-contract.md:64`、`:72`）。

## Requirements

1. 在 `.trellis/spec/academic-writing-skills/` 记录跨 skill 的“防御性推测解释”契约，并在三列表格 index 中登记；名称描述行为，不把截图原句做成词面黑名单。
2. 将核心正例定义为组合行为，而非单个 hedge：
   - 从一个观察结果跳到两个或更多具体机制/原因；
   - 各机制没有局部证据锚点、区分性证据或可证伪测试；
   - 段尾用总括性 caveat 声明当前数据并未验证这些机制；
   - 机制枚举制造了解释完整感，但没有提高可核查性。
3. 把该判断归为 C 档 `[LLM]`：不得给 `deai_check.py` 新增 `may/could/可能/假设/未验证` 等正则，也不得仅凭句长、连接词或 hedge 数量判错。
4. 明确脚本建议边界：对过度自信或未演示应用添加适当 hedge 仍然正确；`may/could/可能` 只能校准单项 claim 的强度，不能替代逐机制证据或使机制堆叠自动安全。
5. 在 `latex-paper-en`、`latex-thesis-zh`、`typst-paper` 的 de-AI 与 experiment/discussion 指南中落地同一语义契约，并修订三处“无立场讨论”修复：证据足够才选择较可信解释，否则明确机制未定。
6. 在 `paper-audit` 的 claim-evidence/over-claim references、实际 lane 模板和 reviewer agent 中复用该契约。它是 `unsupported extrapolation` 的具体形态，不新增独立 issue 配额或 schema 字段。
7. `claims_vs_evidence` lane 达到 8 条上限时，按中心主张影响、严重度、证据缺口排序；重复机制堆叠合并为一条多位置 finding，局部风格问题让位于中心 claim-evidence 缺口。
8. 修复建议必须先陈述观察，再只保留证据最接近的解释并标明推断等级；没有支持时直接说明机制尚未确定；确需保留的备选机制移入可验证的未来工作或显式假设清单。
9. 禁止把“删除最后免责声明”或“写得更肯定”作为通用修复。任何改写都不得升高证据没有赚到的确定性，不得发明消融、对照、指标、引用或机制证据。
10. EN、ZH、Typst 与 paper-audit 各增加一个本地组合 fixture/eval；每个 surface 都必须覆盖目标正例及四类边界反例，而不是依赖跨 surface 并集。
11. 新 eval 只追加、不重排既有项，不复用 paper-audit 的 ID 空洞；contract test 通过唯一 prompt/fixture 语义锚点定位新用例，不把整数 ID 作为长期行为锚点。
12. 逐文件遵守 `docs/resource-manifest.json` 的 `sourceLocale`，同步同语言忠实页面、另一语言完整翻译和 manifest 散列，并运行完整资源校验与 docs build。
13. 保持现有 CLI、frontmatter、issue schema、trigger 边界和脚本哈希锁不变；不新增依赖、不新增独立 skill、不承诺规避任何 AIGC 检测器。

## Acceptance Criteria

- [ ] AC1：新增 Trellis spec 使用 `## Contract:` / `## Convention:` 段式，包含 `**Tests Required**` 或 `**Validation**`，明确定义组合信号、C 档边界、正反例、修复阶梯、lane 饱和规则和脚本 hedge 建议边界，并从三列 index 可发现。
- [ ] AC2：EN、ZH、Typst 的 de-AI 与 experiment references 都能区分防御性机制堆叠和合理不确定性；三处“无立场讨论”不再无条件要求明确表态。
- [ ] AC3：`paper-audit` 的 `SUBAGENT_TEMPLATES.md`、claim-evidence/over-claim references 与 reviewer agent 会检查逐机制 evidence anchor，并在 max 8 预算内优先中心证据缺口、合并重复位置。
- [ ] AC4：四个 surface 各有一个真实 fixture 绑定的新 eval；每个 fixture/eval 同时覆盖目标正例、单一有证据谨慎推断、逐项有证据的多假设、简洁承认机制未知、受控实验强结论五种情形。
- [ ] AC5：新增 contract test 以 prompt/fixture 语义锚点定位新用例，锁定 finding、证据映射、校准措辞和禁止过度声称；既有 eval ID/order 不变且所有 JSON 可解析、ID 唯一。
- [ ] AC6：13 个 source 对应的 26 个双语页面和 manifest 散列同步；四个 affected skill、全量 resource checker 与 VitePress build 通过。
- [ ] AC7：三份 `scripts/deai_check.py` 及阈值文件无行为变更；现有 de-AI 对齐锁通过，最终 scoped diff 确认脚本未改。
- [ ] AC8：目标 contract tests、`tests/contracts` 与 `just ci` 通过；若 provider-backed output eval 因凭据或成本未运行，必须标记为 `missing evidence`，不得声称模型行为已验证。

## Out Of Scope

- 不实现基于 hedge、免责声明、句长或连接词的自动正则判定。
- 不删除真实局限、不把相关性改写为因果、不替作者选择没有证据支持的机制。
- 不重写整篇论文，不新增实验设计工具或统计推断功能。
- 不修改 skill frontmatter、CLI、issue schema、AIGC density score 或检测阈值。
- 不创建或发布新的 skill/package，不执行 GitHub 发布流程。
