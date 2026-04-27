# 投稿前机械规则

`paper-audit` v4.5 新增确定性的 `PRESUBMISSION` 层，用于投稿前最后
3 到 5 天的机械审计。它被接入现有模式，不新增公开的 `pre-submission`
模式。

来源说明：规则结构改写自
`ref/Supervisor-Skills/plugins/phd-research/skills/pre-submission-reviewer`
（license: CC-BY-4.0）。

## 在哪些模式中运行

- `quick-audit`：展示带 `[Script]` provenance 的机械就绪性发现。
- `gate`：Critical 是 blocker；Major/Minor 只是 advisory。
- `re-audit`：用于比较修订前后的机械问题回归。
- `deep-review` Phase 0：作为上下文输入。full/editor focus 可把高信号问题提升到
  `pre_submission_readiness` lane；methodology、theory、literature、logic
  聚焦深审不会把这些机械问题写进最终 focused bundle。

## Severity 映射

| 来源 taxonomy | quick/gate severity | deep-review severity |
| --- | --- | --- |
| CRITICAL | Critical / P0 | major + gate blocker |
| MAJOR | Major / P1 | moderate |
| MINOR | Minor / P2 | minor 或仅保留在 Phase 0 |

## 脚本可确定检查

- G1：reader-visible prose 中出现 em dash。
- G2：段落超过 180 词或超过 8 句。
- G3：topic sentence 只用转折词开头，缺少 claim-like 开场。
- G4：禁用 AI-tone 词组出现 3 次或以上。
- G5：摘要缺 background、objective、method、results、conclusion，或缺定量结果线索。
- L1：LaTeX 引用前缺少 non-breaking tie，例如应使用 `Method~\cite{key}`。
- L2：LaTeX label 含空格。
- L3：LaTeX label 使用连字符，建议改为下划线。
- L4：编号公式没有 label。
- L5：编号公式 label 从未被正文引用。
- F1：source caption 缺少具体 finding 或 comparison cue。

## PDF 与源码差异

PDF 模式只运行文本可证实项：

- em dash 扫描
- AI-tone 频率
- abstract 完整性
- 段落形状弱信号

PDF 模式会跳过源码限定项：

- LaTeX citation tie
- label 命名
- 编号公式引用
- source caption

脚本会用可忽略的 metadata/comment 文本说明跳过项，不把它们伪装成问题。
