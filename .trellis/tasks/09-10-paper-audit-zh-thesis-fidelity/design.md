# Design

## Ownership and Traceability

基线 `41c0cf7`，阶段 planning。paper-audit 拥有审查规则、工作区和结果消费；latex-thesis-zh 继续拥有已完成的一致性和编译实现。本任务仅修审查消费边界。

| Requirement | Mechanism | Acceptance |
| --- | --- | --- |
| R1 | D1：规则校准、canonical 工作区输入/输出 | AC1 |
| R2 | D2：具名 adapter、正常返回码、Info 消费、去除重复清单 | AC2 |
| R3 | D3：同一次装配的全文、来源和覆盖传递 | AC3 |
| R4 | D4：审阅作者给出的构建记录 | AC4 |
| R5 | D5：真实响应、消费链、跨语言/资源验证 | AC5 |

## D1 — 判据及 reviewer 的实际链路

保留上位 `CLAIM_EVIDENCE_CONTRACT.md` 的四级支持度和事实保护。修改 `OVER_CLAIM_GUARD.md` 的 causal、firstness、effect-size、trap、reverse-calibration：明确支持度标签不等于因果资格，试验名称不是充分条件；分别判断观察、受控组件贡献和具体机制。未知首次不能以 hedge 保留；数值槽位只用已提供的记录，缺失时写待核或收窄主张。强证据允许强措辞，理论证明不强制实验数字。

中文准则保留15行和既有维度映射，在解释层明确学校、学位和章节实际功能优先；脚本提示是局部证据，不以 GPU、章号、篇幅或实验数量代替语义判断。用既有 reviewer 指引回查“章目标—段主题—原文证据—处理意见”；合法综合引用不因 cite key 数量强制拆分，邻节仅作证据；不同概念共现不自动要求统一。

修本次共用模板/workflow 的旧根路径为 `WorkspaceLayout` 已有 `artifacts/...` 路径；zh agent 输出为 `<review_dir>/artifacts/comments/zh_thesis_review.json`。不搜旧目录、不双写、不加兼容别名。`_copy_workspace_references` 只追加 `ZH_THESIS_REVIEW_CRITERIA.md` 和 `OVER_CLAIM_GUARD.md`；其上位 claim 契约已在清单中。模板和 agent 区分 skill 内角色卡与 workspace 的 `artifacts/references` 规则。中文 reviewer 输入加入 CONSISTENCY/Info 的 Phase0 材料。规则提及的其它资源明确从 skill 相对路径读取，不盲目复制整个 references。

原 full/editor、lang=zh、max8 条件保持。共享模板的路径修正也服务其它原有 lanes，但不借机迁移全库旧文档。文档路径测试必须从修正后的指令目标写 reviewer JSON，再由真实 consolidation CLI 消费。

## D2 — 一致性协议在一个边界解释

仅对解析到中文 producer 的 consistency 调用附加现有 `--json`。在 `zh_check_adapters.py` 注册专属 adapter，仍使用 `parse(stdout) -> list[AuditIssue]`，不改其他脚本通用解析器或新建 envelope。

真实协议是固定 `[INFO] Checking N files...` 前导后接单个 JSON，含 `terms.inconsistencies`、`abbreviations.issues` 及各自 status；coverage 在 stderr。只允许去除完整匹配的固定前导，再严格解析整串，结构不符抛已有 `AdapterParseError`，禁止找首括号或泛型 JSON/text 猜测。

| 输入 | 映射与消费 |
| --- | --- |
| clean PASS，无问题 | 缺陷0；固定进度/PASS/标题/分隔线不转成 finding |
| 确定首用错误 | 一对一 CONSISTENCY Minor/P2 advisory；从 `first_usage=[file,line]` 取行，原路径和上下文保留在 message，不伪造 quote |
| `terms.inconsistencies` 语义候选或含显式 NEEDS-LLM 的缩写条目 | Info/P3，保留 suggestion/message/定义位置；`undefined` type 也可为待核，不能只按type判缺陷 |
| 实际有限覆盖 / loader 警告 | 既有 Info/P3，只展示一次，保留具体限制；普通无附加限制的固定 INFO 进度不制造噪声 |
| 合法 payload 的 exit0 / exit1 | 直接使用解析结果；exit1 是既有问题/候选协议，不追加 `checker exited 1` Minor |
| exit2、超时、异常或无效 JSON | 走既有显式 error 路径，保留关键错误，不返回 clean，不重设计其他脚本错误政策 |

stderr 的 coverage 只在 `_ingest_check_output` 的 consistency 专属分支处理，既有 message/rationale 足够。文件名不得塞进 quote，局部源行号不得直接当成装配 section 行号。

`report_generator.calculate_scores` 在评分入口过滤 Info；ScholarEval 已过滤，只增加回归，不改其代码、权重、扣分表。Info 继续留在 AuditResult、quick/JSON/Phase0 中，LLM 依据原文确认后才产生现有三档 deep issue。不得直接把 Info 送入 `sanitize_issue` 变成 moderate。现有 deterministic fallback 保持其能力披露，不增加新的模型运行器。

对 `lang=zh && fmt=.tex`，移除独立 `Acronyms defined on first use` checklist 项，唯一首用检查由现有 consistency 调用承担。不得改成 failed ChecklistItem，因为任意 false 都会影响 gate。EN/Typst 分支保持；gate 不额外运行 consistency，`GATE_ELIGIBLE_ZH={spec,blind}` 和模式适用集合不变。gate PASS 不能当完整语义审查通过。

## D3 — 共用装配文本与原始来源

`prepare_workspace` 在 `.tex` 格式读取边界调用现成 `assemble(source)` 一次。`assembled.content` 统一用于语言识别、标题、full_text、section index/文件和 claim map；将同一对象传给 `prepare_subsection_artifacts`，避免第二份快照。其它既有调用（包括 polish）仍能自行装配；这是内部复用，无新增 CLI/缓存层。

section index 的 start/end/line_base 是装配文本坐标，不冒充主文件原行。已有 `origin` / `_source_span` 和 subsection public payload 保留源坐标；必要的章节到源文件/原行说明写入现有 `artifacts/summary/paper_summary.md`，不增 JSON 字段。没有精确位置时沿用章节＋原句证据，不补造行号。复核 PRESUBMISSION 的 source/assembled section mapping，必要时只修本任务 `audit.py` 消费者，不改 parser/loader。

生成 summary stub 后写入可达文件说明和 `assembled.warning_lines`，防止 stub 覆盖它们；同时输出 stderr，由模板要求 reviewer 读取 summary。full_text 不混入警告文本，最终 `verify_quotes.py` 直接在含子文件正文的 full_text 核验原句。

主文件读失败显式报错；缺 include、includeonly 等按现有 loader 语义保留可见内容并披露限制，不扫描全目录。全 `.tex` 统一此边界，避免主文件只有 include 时先判中文的循环问题；EN 多文件纳入测试。`.typ/.pdf`、原 overwrite 行为不变。本次不实现完整宏展开或修改学校模板。

## D4 — 只审核提供的构建证据

在中文准则说明审查不运行编译。E15 使用四段明确标为 synthetic 的构建记录作为既有 reviewer context，核对本次命令、返回码、目标路径和产物；目标 PDF＋成功退出才支持已证构建。旧源码 PDF、非零退出或未运行不通过这项证据判断。没有新 CLI/产物 schema，也不重跑旧 C3 编译算法验证；编译与论文质量分别陈述。

## D5 — 文件白名单和独占职责

一个实现者串行负责 runtime 和源规则；独立 checker 负责逐 AC 审阅和必要修复，主线程负责 spec、manifest 和集成。若并行翻译，仅将已冻结源的镜像独占派给文档执行者；不得并发改同一文件。

| 范围 | 白名单 |
| --- | --- |
| runtime | `academic-writing-skills/paper-audit/scripts/audit.py`、`zh_check_adapters.py`、`prepare_review_workspace.py`、`report_generator.py`，仅 D1/D2/D3 消费边界 |
| root与公开源 | `academic-writing-skills/paper-audit/SKILL.md`；`references/OVER_CLAIM_GUARD.md`、`ZH_THESIS_REVIEW_CRITERIA.md`、`SUBAGENT_TEMPLATES.md`、`REVIEW_LANE_GUIDE.md`、`workflow-detail.md`；`agents/zh_thesis_reviewer_agent.md`、`claims_evidence_reviewer_agent.md` |
| evals | paper-audit `evals/evals.json`、`trigger_eval.json`，新增 `evals/fixtures/zh_thesis_fidelity/` 下合成 main/chapters/context/build 记录；旧写作侧 fixture只读 |
| tests | `tests/skills/paper_audit/test_zh_check_adapters.py`、`test_zh_dispatch_integration.py`、`test_zh_thesis_lane_wiring.py`、`test_paper_audit_deep_review.py`、`test_workspace_layout.py`、`test_paper_audit.py`、`test_paper_audit_topology_docs.py`；新增 `tests/contracts/test_paper_audit_zh_fidelity.py` |
| mirrors | 上述7份公开Markdown的 `docs/skills/paper-audit/resources/`、`docs/zh/skills/paper-audit/resources/` 精确对应页；`docs/resource-manifest.json` 对应记录 |
| maintainer | `.trellis/spec/academic-writing-skills/paper-audit-boundary-contracts.md`、`testing-and-tooling.md`、`index.md`，只写已验证的消费/Info/全文与证据边界 |
| task | 本任务规划、JSONL、task元数据、research/reports；旧归档任务只读 |

`paths.py`、consolidator、quote verifier、ScholarEval、scoring_model、ISSUE_SCHEMA、CLAIM_EVIDENCE_CONTRACT、共享 parsers/loaders、其它五技能源码与所有版本字段只读。评分权重/扣分表不改。根 README/README_CN 和两语 usage 核查现有承诺一致；本次修已有能力，无新接口，默认不编辑；若存在必须修改的对外冲突，先提出具体范围修订。

## Rollback and Evidence

按 D1规则/镜像、D2适配/Info、D3工作区三个逻辑组回滚，并同步各组测试/manifest，不回退原 C1/C2/C3 提交。没有旧 workspace 迁移/回填。验收采用 implement.md 命令和 acceptance-cases 逐例判据；真实输出的引用、概念、强度和合法反例由独立强模型核读，静态门禁不证明效果。
