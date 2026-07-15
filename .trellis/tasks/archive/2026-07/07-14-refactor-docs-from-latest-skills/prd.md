# 根据最新技能重构双语文档

## Goal

以 `academic-writing-skills/` 下 6 个公开技能包为事实来源，重构 VitePress
文档站的英文与中文入口、技能概览、资源导航和跨技能路由，使用户看到的能力、
命令、输入、输出和边界与当前 `SKILL.md` 及其公开 references 一致。

## Background

- 当前公开技能为 `bib-search-citation`、`cover-letter`、`latex-paper-en`、
  `latex-thesis-zh`、`paper-audit` 和 `typst-paper`。
- `docs/` 是 VitePress 1.6 文档站，英文位于根路由，中文位于 `/zh/`；
  `docs/.vitepress/config.ts` 手工维护两套导航和技能资源链接。
- 现有技能页采用统一的用户导向结构：适用/不适用场景、模块或模式路由、
  最小输入、脚本入口、输出产物和常见请求。
- 2026-07-09 的 `358d2f7` 将 6 个 `SKILL.md` 的细节下沉到新增 references，
  但这些新增路由资料尚未接入文档站。
- 最新 `latex-thesis-zh` 已增加摘要、结论和专章写作材料；例如 `f494250`
  新增的 `references/modules/conclusion.md` 与
  `references/writing/conclusion-guide-zh.md` 当前未出现在 `docs/`。
- 资源内容散列盘点显示，现有英文/中文资源镜像中有大量文件不再与当前技能源
  内容完全一致；这证明存在内容漂移，但不代表技能目录中的每个内部文件都应公开。
- 基线 `npm --prefix docs run docs:build` 已通过，因此当前主要问题是内容与信息架构
  漂移，而不是 VitePress 无法构建。
- 工作树中已有 Trellis 运行时和 `README.md` / `README_CN.md` 改动；这些属于用户
  现有工作，不纳入本任务。

## Requirements

### R1. Source-of-truth alignment

- 以每个技能的 `SKILL.md` 为一级事实来源。
- 以 `SKILL.md` 的 module/mode router、Reference Map、脚本入口和输出契约决定
  文档公开内容，不从旧文档反向推断能力。
- 不改变技能行为、脚本接口、测试契约或 reference 原文。

### R2. User-facing information architecture

- 重构英文与中文首页、技能总览、quick start、usage 以及 6 个技能概览页中
  已过时或重复的内容。
- 每个技能概览保持一致、可扫描的结构，并清楚说明触发边界、最小输入、
  推荐首条命令、输出和相邻技能的分工。
- 跨技能路由必须明确区分源码编辑、审稿/门禁、投稿信和本地文献库检索。

### R3. Public resource coverage

- 将 `SKILL.md` 明确路由的公开资源接入对应文档资源树和侧栏。公开资源定义为：
  `references/**/*.{md,yaml,yml}`、`templates/**/*.md`、`examples/**/*.md`，以及
  `agents/**/*.md` 中由技能契约路由的 agent 说明。
- 清理不再由当前技能契约支持的陈旧资源或导航项。
- 新增资源页必须可从技能概览或侧栏到达；不得留下孤立页面或失效链接。
- 所有资源统一迁移到
  `docs/{locale}/skills/<skill>/resources/{references,templates,examples,agents}/...`；
  英文站省略 `{locale}`，中文站使用 `zh`。
- 不保留旧资源路径的副本、兼容页或重定向；本次重构允许旧资源 URL 失效。
- YAML 等语言无关的机器配置在两种语言目录中保持字节级一致，不伪造“翻译版”。
- 内部实现资料、脚本源码、测试 fixtures、evals 和 `agents/openai.yaml` 等机器配置
  不纳入文档站。

### R4. Bilingual consistency

- 英文站与中文站保持相同的技能覆盖、路由层级和链接可达性。
- 两种语言的概览与操作说明必须语义一致，不能一侧出现独有能力或过期命令。
- 所有由当前技能契约公开路由的 resources 必须提供完整的英文版与中文版；
  不得用原文直接复制到另一语言目录充当翻译。
- 原文为英文时，英文资源忠实同步技能源，中文资源提供完整中文翻译；原文为中文时，
  中文资源忠实同步技能源，英文资源提供完整英文翻译。
- 代码块、命令、路径、配置键、文件名、CLI 参数、公式、引用键、标准编号和产品名
  保持原样；只翻译叙述文字、标题、表头、注释性示例和面向用户的说明。
- 双语版本必须保持相同的章节层级、约束强度、警告、示例覆盖和内部链接语义，
  不得在翻译中新增技能原文没有的行为承诺。

### R5. Maintainability

- 避免继续维护无来源说明的重复内容；在设计阶段明确“人工编写概览”与
  “从技能包同步资源”的边界。
- 只增加能实际防止再次漂移的最小同步或一致性检查，不引入与本任务无关的
  文档框架或主题重写。

### R6. Change boundaries

- 实现范围限于 `docs/`、必要的文档同步/校验脚本或测试，以及本任务工件。
- 不覆盖或吸收当前工作树中已有的 `README*` 与 Trellis 运行时改动。
- 不做视觉主题重设计；仅在内容结构需要时调整导航和页面组织。

## Acceptance Criteria

- [x] AC1: 6 个技能概览页的模块/模式、主命令、输入、输出与当前 `SKILL.md`
      一致，英文与中文页面逐项对应。
- [x] AC2: 首页、技能总览、quick start 和 usage 不再描述已删除或更名的能力，
      并能把常见任务路由到正确技能。
- [x] AC3: 所有由 `SKILL.md` 明确公开路由的 reference、template、example 和
      Markdown agent 说明均有可达的中英文文档入口；新增的 skill-routing、
      output/workflow detail、abstract/conclusion 等资料按所属技能接入。
- [x] AC4: 文档资源树、技能概览和 `docs/.vitepress/config.ts` 之间不存在失效链接、
      孤立的公开资源或指向旧文件名的导航。
- [x] AC5: 每个公开 resource 都同时存在英文版和中文版；两版的标题层级、代码块、
      命令、路径、关键标识符和链接目标通过自动检查保持对齐，抽样人工复核确认译文
      没有降低约束强度或增加不存在的能力。
- [x] AC6: 建立最小可执行的一致性检查，能够在技能路由、公开资源、双语结构或
      不可翻译 token 再次漂移时失败。
- [x] AC7: `npm --prefix docs run docs:build`、相关定向检查、`git diff --check`
      以及仓库适用的完整质量门禁通过。
- [x] AC8: 最终 diff 不包含任务开始前已有的 `README*` 或 Trellis 运行时改动。

## Out of Scope

- 修改技能功能、CLI、脚本输出或测试行为。
- 重写 VitePress 主题、首页视觉风格或部署流程。
- 发布、推送、创建 PR，或处理任务开始前已有的未提交改动。
- 将 eval fixtures、内部 agent 配置或全部实现细节无差别复制到文档站。

## Task Map

父任务 `07-14-refactor-docs-from-latest-skills` 只负责需求、共享设计、执行顺序和
最终集成验收，不直接承载批量翻译实现。

| Child task | Deliverable | Dependency |
| --- | --- | --- |
| `07-14-docs-bilingual-core` | 公开资源清单、双语映射/一致性检查、导航骨架、首页/安装/quick-start/usage | First |
| `07-14-docs-bib-search-citation` | `bib-search-citation` 概览与全部公开资源双语化 | Core contract |
| `07-14-docs-cover-letter` | `cover-letter` 概览、references、templates、examples、公开 agent 说明双语化 | Core contract |
| `07-14-docs-latex-paper-en` | `latex-paper-en` 概览与全部公开资源双语化 | Core contract |
| `07-14-docs-latex-thesis-zh` | `latex-thesis-zh` 概览与全部公开资源双语化 | Core contract |
| `07-14-docs-paper-audit` | `paper-audit` 概览、references、templates、examples、公开 agent 说明双语化 | Core contract |
| `07-14-docs-typst-paper` | `typst-paper` 概览与全部公开资源双语化 | Core contract |

技能子任务可独立验收，但在 inline 模式下按顺序执行；全部完成后由父任务运行最终
双语覆盖、链接、构建和仓库质量门禁。
