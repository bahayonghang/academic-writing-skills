# 将 `writing-anti-ai` 增量整合到 academic de-AI

## Goal

在不新增 skill、不扩大默认脚本检测、不牺牲论文事实与证据边界的前提下，将
`ref/claude-scholar/skills/writing-anti-ai/` 中尚未覆盖且适合学术写作的能力，整合到
`latex-paper-en`、`latex-thesis-zh` 与 `typst-paper` 的现有 de-AI 功能。

本任务的目标不是判断文本是否由 AI 生成，也不是规避检测器；目标是识别通用 humanizer
清单中对学术论文确有价值的低信息修辞，并在用户要求改写时证明 claim、evidence、数字、
引用、术语和适用边界没有被改坏。

## Planning Evidence

- `research/source-basis.md`：来源定级、学术适用边界及参考示例的捏造风险。
- `research/prior-art-research.md`：qiaomu 先例检索、keep/adapt/reject 决策。
- `research/delta-matrix.md`：W1-W22 逐项差异、H-* 模式簇和 F-* fidelity 契约。
- `research/review-verification.md`：Claude Code 审阅意见的逐项证据、采纳边界与修订结果。
- `research/skillsmp-*.json`：SkillsMP 原始候选，仅作发现证据，不作质量或流行度证明。

## Requirements

### R1. 差量整合，不复制词表

- W1-W22 每项必须按 `research/delta-matrix.md` 落地或明确不实现。
- 新增能力限定为 H-ING、H-PROMO、H-ATTR、H-PRED、H-TERM、H-SCOPE、H-OUTLOOK 七个
  C 档 `llm-only` 模式簇。
- 命中必须基于语义组合与局部证据，不得把 `-ing`、`serves as`、破折号、三个并列项、
  hedge 或单个“AI 高频词”当作 AI 归因证据。

### R2. 学术保真闭环

- 默认只输出诊断、风险摘要或 rewrite blueprint；只有用户明确要求正文改写时才给 prose
  proposal。
- prose proposal 执行 `audit -> rewrite -> fidelity audit`，逐项保护 claim、evidence、数字、
  引用、公式、标签、术语、certainty rung、limitation 与 scope。
- 输出复用 `Changed / Protected / Meaning-Check / Risk-Flags` 四字段及既有闭集，不增加
  “human score”、AI probability 或检测器通过率。
- 缺少支持时使用 `needs evidence` / `待补证`，不得补造数字、引用、实验、主体、因果或结论。

### R3. 三 surface 一致且可独立安装

- EN 为语义 canonical；ZH 使用中文学术语境适配；Typst 同时覆盖中英文正文并保护 Typst
  语法。
- 每个 skill 新增一个渐进加载的详细 pattern-clusters reference，并从既有 de-AI guide/module
  路由到该文件；不在 `SKILL.md` 复制详细契约。
- 每个 surface 本地对七个 H-* 均至少具有一个应命中正例和一个证据充分反例，并包含
  syntax/citation 保护用例；不能依赖三者并集。

### R4. 可选作者样本校准

- 用户提供代表性已发表/已确认文本时，可用其校准节奏、句法偏好和语气。
- 作者样本不得覆盖 venue、学术体裁、术语表、证据边界、保护 token 或用户本次明确要求。
- 未提供样本时不得推测作者“个性”，不得自动注入第一人称、观点、幽默或情绪。

### R5. 默认兼容

- 不修改三份 `scripts/deai_check.py`、`deai_batch.py`、threshold YAML、tone-term reference、CLI、
  `--tier`、frontmatter、issue schema 或默认输出。EN/ZH 阈值位于
  `references/deai/tone-thresholds.yaml`；Typst 的 flat-layout 路径是
  `references/AI_TONE_THRESHOLDS.yaml`，同级 `AI_TONE_TERMS.md` 也不移动、不修改。
- `--tier` 继续只表示检测灵敏度，不得承担编辑强度。
- H-OUTLOOK 与既有 defensive-rhetoric 契约同时命中同一根因时合并为一条 finding；满足
  defensive 组合判据时 claim-evidence 问题优先，style facet 不重复报告。
- 不向 `paper-audit` 增加 style-only lane、issue 类型或配额；真正的 claim-evidence 问题继续由
  既有契约处理。
- 不新增生产依赖，不安装外部 humanizer skill。

### R6. 公开资源与回归证据

- 新增/修改的 runtime references 必须同步 EN/ZH 文档页和 `docs/resource-manifest.json`。
- 三个 skill 各新增一个 composite fixture 和 append-only eval，覆盖目标模式与合法边界。
- 新增跨 surface contract test，锁定七模式、fidelity loop、作者样本优先级、脚本零扩张和 eval
  绑定。

## Out Of Scope

- 对 AI 作者身份、概率、检测器分数、真实性或“降 AI 率”做判断；
- 自动改写用户论文、provider-backed eval、真实论文盲评或人工作者研究；
- 格式类问题（粗体、列表、标题大小写）和 citation style 检查；
- 新增独立 anti-AI/humanizer skill，或改造 paper-audit；
- 将参考 skill 的示例文本、评分表或 Personality and Soul 规则直接复制进产品。

## Acceptance Criteria

- [ ] W1-W22 的实现与拒绝项逐条符合 `research/delta-matrix.md`，无重复词表扩张
- [ ] 三个本地 pattern-clusters reference 均定义 H-ING/H-PROMO/H-ATTR/H-PRED/H-TERM/
  H-SCOPE/H-OUTLOOK，并为每类提供命中组合、证据充分反例和保真修复
- [ ] H-OUTLOOK 与 defensive-rhetoric 的 owner、同段合并和可拆分边界在三方 reference 与
  contract test 中一致
- [ ] 三方 guide/module 都路由到详细 reference，并声明“模式不是 AI 作者身份判定”
- [ ] prose proposal 仅在明确请求时出现，并带四字段 fidelity ledger；字段值遵守既有闭集
- [ ] 作者样本只校准表达，不覆盖体裁、术语、evidence、claim strength 或受保护语法
- [ ] `git diff --exit-code -- academic-writing-skills/*/scripts/deai_check.py academic-writing-skills/*/scripts/deai_batch.py academic-writing-skills/latex-paper-en/references/deai/tone-thresholds.yaml academic-writing-skills/latex-thesis-zh/references/deai/tone-thresholds.yaml academic-writing-skills/typst-paper/references/AI_TONE_THRESHOLDS.yaml academic-writing-skills/latex-paper-en/references/deai/tone-terms-en.md academic-writing-skills/latex-thesis-zh/references/deai/tone-terms-zh.md academic-writing-skills/typst-paper/references/AI_TONE_TERMS.md` 通过
- [ ] 三个新 composite fixture/eval 均绑定真实文件，ID 唯一、只追加，正反例在本 surface 内闭合
- [ ] focused contract/eval tests、`tests/contracts`、`just ci` 全绿
- [ ] affected skill/full resource sync 通过，重建 manifest 后零漂移，`just doc-build` 成功
- [ ] 未执行的 provider-backed、人工盲评、真实论文精确率与作者样本效果明确标记
  `missing evidence / UNVERIFIED`

## Approval Boundary

本任务保持 `planning`。只有用户后续明确批准实施后，才运行 `task.py start` 并修改产品文件。
