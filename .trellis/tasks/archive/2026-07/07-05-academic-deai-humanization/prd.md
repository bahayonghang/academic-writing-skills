# 优化学术去 AI 味写作工作流

## Goal

借鉴 `ref/rnskill` 中 `renhua` skill 对“AI 味结构壳”的识别方法，优化
`academic-writing-skills` 现有 de-AI 能力，让它在降低 AI 腔、模板腔、讲义腔时
仍优先保留论文的学术逻辑、引用规范、实验事实、术语一致性和证据边界。

## User Value

用户在中文学位论文、英文论文或 Typst 论文中请求“降低 AI 味”时，skill 不应把正文
改成顺滑但空泛的文本，也不应为了过检测而牺牲学术规范。它应该先保护
“问题 -> 方法 -> 证据 -> 结论 -> 边界”的论证链，再移除明显的 AI 写作外壳。

## Confirmed Facts

- `ref/rnskill/skills/renhua/SKILL.md` 是中文 AI/技术写作去 AI 味 skill，核心做法是：
  先保留事实、数字、模型名、技术术语、作者判断和不确定性，再删除二元对比壳、
  命令式开头、伪洞察标记、冒号讲义腔、空泛指代、错误时间姿态和口号式结尾。
- `renhua` 面向 X/Twitter、中文技术文章、产品笔记和模型测评，默认输出“改后文本”；
  这不能原样搬进学术写作，因为学术 skill 需要默认先诊断、再给改写蓝图，且不得新增
  引用、数据、实验结论或作者未提供的个人经验。
- 当前仓库已有 de-AI surface：`latex-paper-en`、`latex-thesis-zh`、`typst-paper` 均有
  `deai` 模块、`deai_check.py` / `deai_batch.py`、D1-D5 分级维度、词频阈值、
  低信息密度、模板表达、并列开头、段首套话、标点、过度声称和时态相关检查。
- 当前中文学位论文 de-AI 已覆盖“近年来”“显著提升”“综上所述”等常见模板，
  但还没有系统吸收 `renhua` 的“结构壳优先删除”模式，例如：
  `不是 A，而是 B`、`不在于 A，而在于 B`、`真正/其实/本质上/核心在于`、
  `我的结论是：`、`原因很简单：`、`这件事/这些东西`、`更适合/更像` 等。
- 本仓库要求 source-preserving：默认保留 `\cite{}`、`\ref{}`、`\label{}`、数学环境、
  Typst `@cite` / `<label>` 和模板宏；生成文本只能作为建议，不能默默改源文件。
- 本任务使用 `yao-meta-skill` 的轻量流程：不创建新 skill，而是优化已有 skill；
  由于本地 `C:\Users\lyh\.skillsmanage\skills\yao-meta` 缺少 `references/` 目录，
  本计划只采用其 `SKILL.md` 中可验证的边界：保持 entrypoint 精简、细节放入
  references、风险匹配验证、trigger/output eval 跟随路由改动。

## Requirements

1. 不新增独立的“人话/renhua” skill；优化现有 `deai` 模块和文档。
2. 将 `renhua` 的“四桶保留”改造成学术版：
   - facts/evidence：数据、公式、实验设置、引用、图表、指标；
   - claims/stance：本文主张、研究判断、方法选择和不确定性；
   - logic：章节主线、段落角色、claim-evidence 映射；
   - boundaries：适用条件、局限、未验证处、待补证处。
3. 一次性覆盖三个现有写作 skill：`latex-thesis-zh`、`latex-paper-en`、`typst-paper`。
4. 在中文学位论文 de-AI 中补充“结构壳”识别与建议，但避免把合法学术对比误报成 AI 味。
5. 对 Typst 的中文/双语 de-AI 同步结构壳识别、Typst 语法保护、eval 与必要测试。
6. 英文论文 de-AI 同步学术版结构壳思想：以英文 rhetorical scaffold、empty framing、
   unsupported contrast、vague metadiscourse 等等价模式为主；不硬套中文 `renhua` 的词面禁用表。
7. 默认输出仍是诊断、风险摘要、改写蓝图或局部改写建议；只有用户明确要求改写正文时才给 prose proposal。
8. 所有新增规则必须继续声明：这不是 detector-evasion 工具，也不能替代目标学校或投稿 venue 的 AI 使用声明义务。
9. 更新测试/eval 以覆盖：
   - 路由到 de-AI 且保留学术逻辑和引用；
   - 中文结构壳 pattern 命中；
   - 英文/Typst 等价结构壳 pattern 命中；
   - 有证据支撑的合法对比不过度误报；
   - docs/skill contract 不破坏现有模块清单和命令契约。
10. 用户可见文档如有行为变化，需同步 `docs/` 与 `docs/zh/` 镜像。

## Acceptance Criteria

- [ ] `latex-thesis-zh` 的 de-AI 指南明确描述“学术去 AI 味”的优先级：
      论证/证据/规范优先于语气润色。
- [ ] `latex-thesis-zh` 的 de-AI 检查能报告至少 3 类 `renhua` 借鉴的结构壳，
      并给出学术写作导向的修复建议。
- [ ] `typst-paper` 的 de-AI 文档、eval、脚本检查与测试同步覆盖中文/双语结构壳，
      并继续保护 `@cite`、`<label>`、math 和 Typst 宏。
- [ ] `latex-paper-en` 的 de-AI 文档、eval、脚本检查与测试同步覆盖英文 rhetorical scaffold
      类问题，并采用 claim-evidence-first 的去 AI 工作流。
- [ ] 新增或更新测试覆盖三类 skill 的结构壳、合法学术对比边界和 source-preserving 约束。
- [ ] `README` / docs 中对“去 AI 味”的描述不承诺绕过检测，不承诺降低某个平台分数。
- [ ] 目标验证通过：相关 de-AI pytest 子集、skill contract tests、必要时 `just ci`。

## Out Of Scope

- 不保证通过知网、维普、Turnitin 或任何 AIGC 检测平台。
- 不代写核心学术内容，不新增实验、指标、引用或结论。
- 不改变 compile / bibliography / logic / experiment 等非 de-AI 模块的核心行为。
- 不把 `renhua` 的公开写作风格原样迁移到论文，例如粗粝口语、X/Twitter 段落、
  第一人称经验叙述或面向读者的行动号召。

## Scope Decision

用户已确认需要一次性覆盖三个 skill。本任务保持单一 Trellis 任务，不拆子任务：
三个 de-AI 模块共用同一个学术人味契约和验证门槛；实施时按
`latex-thesis-zh` -> `typst-paper` -> `latex-paper-en` 的顺序落地，但最终交付必须
同时覆盖三者。
