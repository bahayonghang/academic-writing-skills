# 融合 Nature、IEEE 与 Elsevier 的学术写作润色 skill

## Goal

在 `academic-writing-skills/paper-writing-studio/` 从零建立一个可复用的学术写作润色 skill。它以 `ref/nature-writing-studio/skill/` 的证据约束、分节编排和输出形状为基础，同时把 `materials/IEEE/` 与 `materials/Elsevier/` 的 Zotero 语料知识作为隔离的 venue profiles 接入。用户可以明确选择 Nature、IEEE 或 Elsevier 风格，得到可追溯、不会混用刊物句式的润色结果。

## Background and confirmed facts

- 目标目录当前为空，只有目录本身；需要从零建立 skill 包。
- Nature 参考包在 `ref/nature-writing-studio/skill/SKILL.md:1-47,104-127` 定义了分节输入、`text`/`text_compact`/`summary` 输出、`multi_section` 的 `logic_line`/`story_arc`/`entity_registry` 前置、跨节审计、反编造验证和 em-dash scrub。 `agents/openai.yaml:1-31` 补充分层加载与 required files。
- Nature 的规则与材料存在数字口径差异：SKILL 描述写 95 条规则，元数据摘要写 85 条；实现必须以实际 TSV 和 `knowledge/PROVENANCE.md` 校准，不能复制未经核对的统计 claim。
- IEEE 根路由在 `materials/IEEE/SKILL.md:2-36`，要求按 section 加载 `style-guide.md`、一个 writing reference 和匹配 TSV；只引用 `core` 或 `paper_count >= 5` 的统计 opener。其 provenance 记录 353 条 inventory、261 条 complete、92 条 degraded（`materials/IEEE/knowledge/PROVENANCE.md:5-25`）。
- Elsevier 根路由在 `materials/Elsevier/SKILL.md:2-36`，采用同样的按节加载和晋升门。其 provenance 记录 150 条 inventory、98 条 complete、52 条 degraded（`materials/Elsevier/knowledge/PROVENANCE.md:5-18`）。
- IEEE 与 Elsevier 的 style guide 都明确不把 Nature 的 `Here we` 或 methods-last 作为本刊规则；两者允许 Related Work 独立或并入 Introduction，但自称、节序和结论收束句式存在差异（`materials/IEEE/references/style-guide.md:1-36`; `materials/Elsevier/references/style-guide.md:1-28`）。
- 三套材料都把 TSV 作为规则来源、reference 作为人读摘要，并要求保持语料隔离；不能把三套 TSV 行直接拼接成一个全局规则表。

## Requirements

### R1. 统一入口与 venue 选择

提供一个可发现的根 `SKILL.md` 和 `agents/interface.yaml`。输入至少包括 `input_text`、`target`、可选 `venue`、可选 `journal`、可选 `domain`；支持 `nature`、`ieee`、`elsevier` 和 `unspecified`。选择优先级固定为：显式 `venue` > 已知 journal allowlist > 明确 domain 映射 > `unspecified`；无法安全判断时不得猜测，应报告缺失信息或使用中性基线。

### R2. Profile 隔离与按需加载

Nature、IEEE、Elsevier 的 prompts、references、TSV 和 provenance 保持来源隔离。每次只加载目标 section 所需资源；不得默认读取全部 observations 或全量 TSV。统一 section 别名只做接口映射：`methods`/`method`、`results`/`experiments`、`discussion`/`conclusion`、`related_work`；映射后仍由 profile 决定具体规则。

### R3. 风格融合边界

只把跨 venue 重复且具有独立证据价值的机制提升到 core：证据不编造、保护用户数字/引用/实体、按证据强度使用 hedge、显式标记 degraded、输出可追溯摘要。Nature 的 `Here we`、Nature methods-last、IEEE/Elsevier 的 self-reference、Related Work 节序和 roadmap 句式必须留在各自 profile。

### R4. 输出契约

默认返回 inline Markdown，包含 `text`、`text_compact` 和 `summary`。summary 至少记录 `venue`、`profile_version`、`section`、`domain`、`rules_applied`、`patterns_used`、`evidence_rows`、`ai_tells_avoided`、`untraceable_tokens`、`degraded`。只有用户明确要求时才返回 JSON 或写文件。`multi_section` 保留 Nature 的共享上下文和跨节审计思想，但审计规则按 profile 分层。

### R5. 触发和排除

触发包括“按 Nature/IEEE/Elsevier 风格润色”“学术英文改写”“按目标期刊章节改写”“中译英学术润色”及单节/整稿请求。明确排除 LaTeX 排版、引用格式编译、期刊模板检查、Zotero 写入、凭空补充实验/数字/引用，以及将不同 venue 的风格强行混合。

### R6. 评估、文档与同步

提供 Production 级 README、interface、trigger cases、输出契约案例和 provenance/缺证据说明。验证三种 venue 的正触发、错误 venue、未指定 venue、journal 冲突、section 别名、候选规则不得被引用、保护 token 与 degraded 输出。同步项目资源清单和 docs 镜像（若仓库清单要求），不把 `materials/` 当作可安装 catalog skill。

## Acceptance Criteria

- [ ] AC1：`academic-writing-skills/paper-writing-studio/` 包含唯一根 `SKILL.md`、`agents/interface.yaml`、README、profile 路由和按需资源；`validate_skill.py` 通过。
- [ ] AC2：给出同一输入的 `venue=nature|ieee|elsevier` 三种结果时，summary 标出对应 profile/version，且 Nature `Here we`、IEEE/Elsevier self-reference 等专属规则不会跨 profile 自动出现；混用冲突会被报告。
- [ ] AC3：未给 venue 时只按 allowlist/domain 的确定映射选择；仍不确定时返回 `unspecified`/缺失证据，不猜刊物风格。journal 与显式 venue 冲突时显式 venue 胜出并记录冲突。
- [ ] AC4：每个目标 section 只读取匹配 profile 的 style guide、section reference 和 TSV；`candidate` 行不会进入 `rules_applied`，统计 opener 遵守 `paper_count >= 5` 门槛。
- [ ] AC5：输出包含 `text`、长度有实质差异的 `text_compact`、可追溯 summary；用户数字、引用、实体不新增，em-dash/anti-AI 处理结果可审计，无法验证的 section 标 `degraded`。
- [ ] AC6：trigger eval、输出 eval、skill IR 和 prior-art report 均生成；至少覆盖三种 venue、未指定 venue、冲突和保护 token 边界。不能由本地 fixture、静态检查或目录存在性证明的真实论文质量、provider、安装和人工可读性保持 `missing evidence`。
- [ ] AC7：`just check-versions`、`just lint`、`just typecheck`、`just test`、资源同步检查和文档构建按批准后的改动范围执行；现有 `materials/IEEE`、`materials/Elsevier`、Nature 参考包无非必要改动。

## Out of Scope

- 修改 `ref/nature-writing-studio`、`materials/IEEE`、`materials/Elsevier` 的原始语料和抽取脚本。
- 将三套 TSV 合并、重命名或复制成一个无 provenance 的大表。
- 期刊排版、LaTeX/Typst 编译、BibTeX 生成、Zotero 写入或远程 catalog 安装。
- 声称“更像 Nature/IEEE/Elsevier”、真实投稿成功、人工审校通过或跨平台安装成功，除非取得对应证据。

## Confirmed decisions

- 未指定 venue 时使用 `unspecified` 中性基线并显式报告缺失信息，避免误套 Nature、IEEE 或 Elsevier 规则。
