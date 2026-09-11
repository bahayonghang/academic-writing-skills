# Research: 中文大论文审稿链与新保真契约差距

- Query: paper-audit 是否能通过真实自动检查、工作区、reviewer lane 和最终合并链审查已完成的 C1 指南保真、C2 一致性语义和 C3 编译产物边界？
- Scope: internal；产品只读，合成 CLI/API 探针只写本任务 research 中的独占临时目录。
- Date: 2026-09-10
- Task: `.trellis/tasks/09-10-paper-audit-zh-thesis-fidelity`
- Baseline: 已归档父任务 `.trellis/tasks/archive/2026-09/09-10-thesis-zh-spec-gap-optimization/research/integration-validation.md`；本报告基于当前代码和本次实跑，不把历史规划状态当现状。
- Evidence: [probe_audit_chain.py](probe_audit_chain.py)、[probe-results.json](probe-results.json)。JSON 保存完整输入、五份消费者/生产者源码 SHA-256、真实命令/返回码/stdout/stderr、适配结果、评分和工作区内容。

## Findings

### F1 — P1：干净一致性报告被计为十条缺陷，NEEDS-LLM 被提前计分

`audit.py:311-318` 把 consistency 加入 zh checks，`:439` 解析到 `check_consistency.py`，`:2744-2800` 以真实主入口调用且不附参数。因此新 C2 的入口装配与首用顺序算法已经复用，**不需要再造 checker**。

问题在消费端：`zh_check_adapters.py:391-400` 七个具名适配器没有 consistency；`audit.py:608-621` 将其交给 `_parse_script_output`。该通用解析器 `:705-782` 把每个非空非 Markdown 标题的行当 `Minor/P2`，正则 `:772` 还会去掉行首一个“模块词”。生产者却在 `check_consistency.py:369-405` 输出人类报告，其标题、分隔线、状态和覆盖说明都不是 finding。

实测：

- `clean` 输入已在首次使用处定义 CNN，checker 的术语和缩写状态均为 PASS，适配后有 **10 条 Minor/P2**；包括 `No inconsistencies found`、`No abbreviation issues found within checked scope`、分隔线及标题。
- `scholar_eval.py:62,71,154` 的既有契约是 Minor 扣 0.5、CONSISTENCY 属于 clarity、Info 不扣分。把上述十条独立送入真实 `evaluate_from_audit` 后 clarity=**5.0**，其他可计算维度=10。这里验证的是十条伪 finding 的独立分数效应，未声称整份论文总分下降五分。
- 中英文等价全称重引仅产生一个 `NEEDS-LLM` 候选，但适配结果为十二条 Minor，候选也提前当缺陷扣分；未调用 LLM，不能把不同可见片段判为语义冲突。
- `missing_include` 的 loader 警告仍在 human stdout 内，因此**并非完全丢失**，但被降为普通 Minor 问题；覆盖说明甚至被削掉开头“按入口”。应保留“覆盖受限”的证据意义，不能用其作为作者写作质量扣分。
- `distinct_concepts` 的数据处理/预处理、算法/模型/系统在新 checker 中无混同候选，仍因相同报告装饰产生十条伪问题。故算法修复成立，审稿侧呈现不成立。

最小建议：在既有 `zh_check_adapters.py` 为已存在的一致性输出补具名适配，保持一项真实问题对应一项 finding，保留源文件/行号和 `NEEDS-LLM` 语义；候选与覆盖限制使用既有 Info/P3 观察并进入 Phase 0，不进入评分。保留确定的首用错误为既有非阻断缺陷。不要改通用解析器为所有脚本猜 JSON/文本，不新增评分维度、权重、CLI 或 schema。若选现成 `--json`，必须处理生产者在 JSON 前打印固定 INFO 行及 stderr 覆盖信息的真实协议；不能假设纯 JSON。

### F2 — P1：多文件论文的自动证据与 reviewer 全文不属于同一可见范围

`prepare_review_workspace.py:871-876` 只读取主 `.tex`；`:878-896` 用该内容生成 `full_text.md`；`:898-924` 的 section index、section files 和 claim map 同样来自主文件。只有 `prepare_subsection_artifacts` 的 `:701` 调用已有 `assemble(source)`。`audit.py:2037-2042` 最后还对这份不完整 `full_text` 验证引用。

双 include 合成输入实测：新 C2 准确报告 `introduction.tex:2` 首用在 `method.tex:2` 定义之前；生成工作区的全文只有 `ctexbook / document / introduction / method / document` 指令残片，包含“模型章完整证据”的子文件正文不存在，section index 为空。LLM 无法从模板指定的全文/分节证据核验 checker 所说的定义，也无法审查 C1 在这些章节里的事实边界；最后 quote verification 也缺原文。

最小建议：对 `.tex` 工作区复用现有 `tex_loader.assemble` 作为该工作区全文、分节和 claim map 的同一输入；保持现有 origin/source-coordinate 能力，不新建 loader 或 schema。核对单文件、跨文件章节和 quote verification 的坐标语义，缺失 include 明示有限覆盖。既有 subsection window 的 source 坐标不能因改用装配行号被改写。`.typ/.pdf` 行为不应随本任务改动。

### F3 — P1：reviewer 的具体保真规则仍建议保留未经支持的首次/因果资格

传播链是实在的：`SUBAGENT_TEMPLATES.md:141-178` 的 claims lane 要求分类 overclaim 并从 `OVER_CLAIM_GUARD.md` 取 conservative rewrite；`agents/claims_evidence_reviewer_agent.md:14-18` 作相同指引。`ZH_THESIS_REVIEW_CRITERIA.md:30,51-54` 要求按学位判断创新，却未补新 C1 对“首次资格”的证据边界。

当前审稿规则与已完成写作规则的冲突：

| 审稿侧当前规则 | 新 C1 的对应约束 | 最小修复 |
| --- | --- | --- |
| `OVER_CLAIM_GUARD.md:52-53,117` 用 ablation/RCT/A-B 名称许可因果/`demonstrate` | `latex-thesis-zh/references/writing/over-claim-guard.md:43-45,122` 要核对混杂、区分性证据和具体主张 | 按设计/协议/对象/范围判断，保留有资格的强表达负例 |
| 审稿 guard `:59,108` 把 first 换成 among first/to our knowledge | 写作 guard `:52-58,129` 未检索必须去除优先权或标待核 | 不以 hedge 保留未知优先权；复用既有 `missing_evidence` |
| 审稿 guard `:75-79` 给出 X/Y/p/CI/N 槽位却未指明缺数据处理 | 写作 guard `:79` 只允许已有记录，否则待补 | 使示例自足，不补造数字，也不只生成未填的结论句 |

`CLAIM_EVIDENCE_CONTRACT.md:54-58` 已明确不编造和显式 missing evidence，是可保留的上位规则；这并不能使下游具体错误模板自动安全。建议修现有审稿 guard、中文指标和对应 lane 指引，不引入因果词典、优先权检查器或新错误码。LLM 尚未实跑，因此本项证明**规则冲突和可达性**，不声称某个真实 reviewer 已实际给出错误结论。

### F4 — P1：模板让 reviewer 写入不被真实合并消费的目录

`SUBAGENT_TEMPLATES.md:12-15,35-47,61-74,340-341` 仍用工作区根下的 `paper_summary.md`、`claim_map.json`、`sections/`、`references/`、`comments/`；`zh_thesis_reviewer_agent.md:22` 同样写 `<review_dir>/comments/zh_thesis_review.json`；`workflow-detail.md:78-82` 延续旧路径。真实 `WorkspaceLayout` 在 `paths.py:67-68,137-146` 指向 `artifacts/summary`、`artifacts/sections`、`artifacts/comments`，consolidator `consolidate_review_findings.py:191` 只读该 canonical comments 目录。

实测先向文档指示旧 comments 路径写一条合成 reviewer issue，真实 consumer 读取 **0 条**；同一条写进 canonical `artifacts/comments` 后读取 **1 条**，真实 consolidation CLI exit0 并保存该条。旧输入路径也全部不存在。

此外 `_copy_workspace_references` (`prepare_review_workspace.py:836-847`) 实际复制的十份引用不含中文准则及 overclaim guard，而模板专属块要求 reviewer 使用它们。不应把“skill 内有这个文件”写成“自足工作区已经提供它”。可选的最小修复是补这两份必要引用到既有清单并统一工作区引用位置；或明示允许从 skill 内读取的真实路径，两者择一作为唯一契约。不新增路径兼容层、旧目录回填或别名查找。

建议只同步这次链路会读取的 SKILL、模板、中文 agent、workflow/相应 lane/claims agent 的路径；不要把本次规划变成全仓库的旧路径迁移。路径负例测试应证明“从**文档指定路径**写入的 reviewer issue 被 consolidate CLI 消费”，不能只测 `WorkspaceLayout` 自己一致。

### F5 — P2：独立 acronym checklist 对已知首用缺陷打勾

`audit.py:2201-2244` 另写一个 acronym heuristic：用 `\b[A-Z]{2,6}\b` 找缩写，任意位置出现 `(ACR)`/`{ACR}` 就视为定义，排除 CNN 等固定清单，且未定义数≤3仍打勾。`lang` 形式上保留但该项未按 zh 走 C2 结果。

在同句“采用CNN得到结果，卷积神经网络（CNN）……”上，真实 checker 报告 first-use error；同一输入的 `Acronyms defined on first use` checklist 却 `passed=true`。多文件 main-only 内容更无法判定。`export_phase0_context` (`audit.py:2987-2994`) 将矛盾的勾选直接写给 agent。

最小建议：zh `.tex` 的该项统一从本轮已运行的 consistency 结果/覆盖范围导出，或明确交给 consistency 观察而停止独立全称“首用已通过”的断言；不要重复再跑 checker，不新增阈值/词表；英文和 Typst 旧行为不随本轮扩大。同时维持既有 `GATE_ELIGIBLE_ZH={spec,blind}`：对一个原本 advisory 的首用项，不能因复用 checklist 而新造 gate blocker。缺证据时不能打“验证通过”。

## 三项旧交付的审稿覆盖矩阵

| 旧验收对象 | 当前自动/LLM/不适用边界 | 本轮规划应覆盖的缺口 |
| --- | --- | --- |
| C1 学校/学位/体裁优先 | 中文准则已有学位差异且不增 CLI；abstract 默认脚本仍执行，第9行只标 Script | 在中文 reviewer 明示学校要求和论文功能优先；启发式摘要结果不得自动升格通用规则。保留论文骨架及无数字理论研究的合法负例，不改学校阈值 |
| C1 数字/因果/首次事实保真 | claim-evidence 上位保护已有；guard 有 F3 冲突 | 修现有规则和实际 reviewer 调用输入，测试原数字不变、未知数字/首次不补、混杂消融不获因果许可、已证强主张不降格 |
| C1 合法综合引用/逆向提纲 | `section_intro_related` 已有 P-ARC 四观察和“不以缺过渡词判断裂”；但无新逆向提纲证据回查例 | 用既有 lane 指引/示例检查本章目标→段落角色→原文证据→处理意见；合法多引文综合不能因三个 cite key 强制拆成逐篇罗列。保持 review 只提建议，邻节只作证据 |
| C2 不混同概念/首用顺序/同义重引 | checker 新算法已真实跑通 | F1/F2/F5 修正消费、全文证据和勾选矛盾；中文 agent 输入应包含既有 CONSISTENCY 结果（当前清单未列） |
| C2 NEEDS-LLM/有限覆盖 | producer 保留候选和警告；通用适配器错误计分 | 限制/候选保留到 Phase0，LLM 复核同义与概念后才成立；Info 不扣分，缺 include 不能宣称全篇通过 |
| C3 outdir/退出码/目标PDF | `SKILL.md:3,8,21-22,65-66` 明确审稿不是 compile repair；`audit.py` 的 SCRIPT_MAP 没有 compile | **不自动执行编译，编译算法验收不适用 paper-audit。** 审查作者交付的构建证据时核对命令、退出码、目标路径/产物；没有这些就 missing evidence，不能用源目录旧PDF或脚本静态阅读证明构建通过。继续引用旧任务真实TeX证据，不重跑或复制 compile.py |

### 正例和反例的有限观察

`legal_synthesis` 合成相关工作只含一段、三个 cite keys。真实 `analyze_literature.py` 未把它判为作者年份罗列，给出的是“末尾未见研究空白”的独立 Major；本输入不是完整相关工作，不能把这个结果当作 C1 段落全部合格或误报证据。新计划需用原八场景中的充分上下文生成 native/sequential reviewer 响应，以比较保真与合法负例；本次没有调用 LLM，不声称 synthetic CLI 已证审稿语义质量。

## Files found and code patterns

| 文件 | 职责/可复用模式 |
| --- | --- |
| `paper-audit/SKILL.md` | 深审工作流、读写/编译边界、中文 lane 触发 |
| `paper-audit/scripts/audit.py` | `_resolve_check`→具名适配→Phase0；已有 `Info/P3` 表达，不新增标签 |
| `paper-audit/scripts/zh_check_adapters.py` | 每脚本独立协议类；可容纳 consistency 专属适配 |
| `paper-audit/scripts/prepare_review_workspace.py` | 工作区内容所有权、现成 `assemble` 和 source-coordinate subsection 机制 |
| `paper-audit/scripts/paths.py` | 唯一工作区路径来源，无需新路径抽象 |
| `paper-audit/scripts/consolidate_review_findings.py` | canonical comments 消费和既有去重/根因合并 |
| `paper-audit/scripts/scholar_eval.py` | `CONSISTENCY→clarity` 和 Info 免扣分，维持映射/权重 |
| `paper-audit/references/ZH_THESIS_REVIEW_CRITERIA.md` | 15项指标和学位语境，保留维数与等级边界 |
| `paper-audit/references/SUBAGENT_TEMPLATES.md` | 一组通用输入/输出路径+既有 focus blocks，修同一契约 |
| `paper-audit/references/OVER_CLAIM_GUARD.md` | 当前具体改写冲突源，需 source + EN/ZH mirrors 同步 |
| `latex-thesis-zh/scripts/check_consistency.py` | 新 C2 可复用 producer，禁止复制其实现到 audit |

上表省略共同目录 `academic-writing-skills/` 前缀；所有行号以本次 probe 所记 hash 的工作树为准。

## Existing tests and proportionate validation

- `tests/skills/paper_audit/test_zh_check_adapters.py`：已有七类实际协议样例、返回码2/非法 JSON、Info 映射；追加 consistency 干净/确定问题/语义候选/覆盖警告，不测私有行实现。
- `test_zh_dispatch_integration.py:13-28,157-178`：可复用捕获真实子进程方法，锁定主入口与参数及输出。已有测试只证明解析到 checker，未锁其报告被正确消费。
- `test_zh_thesis_lane_wiring.py:13-18,95-120`：已有中文/full|editor门控和合并；补从模板指定路径写入后经 CLI 消费，不能只重复 Layout 单元断言。
- `test_paper_audit_deep_review.py:248-249` 和 `test_workspace_layout.py`：已有资源/布局断言；补正文只在 include 文件的工作区、source quote、缺失 include 边界。
- `test_paper_audit.py:509-586` 的结构化块/InfoP3 既有协议、`test_zh_script_resolution.py:166-170` 的 gate 资格锁必须保留。
- `test_paper_audit_topology_docs.py` / `tests/contracts`：已有 lane 角色、canonical severity、P-ARC/方法/defensive 等契约。对新保真规则用充分上下文正反场景，不把固定关键词出现当作实际质量证明。
- 产品实施后先 `uv run --no-sync --extra dev python -m pytest tests/skills/paper_audit tests/contracts -q`，再资源单技能/全量检查、`just doc-build`、`just ci`。本轮只研究，不重复执行上轮已绿的1908测试来掩盖这些新缺口。

## Reproduction

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
rtk proxy uv run --no-sync python -B .trellis/tasks/09-10-paper-audit-zh-thesis-fidelity/research/probe_audit_chain.py
```

脚本真实运行七组 consistency CLI（每组各一轮 human / `--json` 输出）、一次完整 quick-audit CLI、一次 literature CLI、工作区 API 和 consolidation CLI；使用唯一 `TemporaryDirectory(dir=research)`，验证 resolved 路径仍在 research 内。最终 `temporary_directory_removed=true`。输出只保留脚本与 JSON 研究证据，没有更改论文/产品/依赖/任务状态或执行任何 Git 操作。

完整 quick-audit 的合成稿缺真实摘要、学校模板、文献等，exit1 是该受控输入的其他失败项；其 `consistency: 10 issues found` 与直接 API 探针一致。不得称这个单次 full CLI 是有效论文整链通过或既有产品回归测试失败。

## Related specs

- `.trellis/spec/academic-writing-skills/index.md`
- `paper-audit-boundary-contracts.md`：severity、module 唯一评分维度、Info/数据流纪律。
- `method-narrative-contract.md`：zh 必须显式选章，自动 audit 不补方法 pass；不把这次覆盖补齐扩成该能力。
- `results-analysis-checker-contract.md`：RA 启发式≠语义验收；本次不自动接 RA 新参数、不改证据窗口。
- `paragraph-arc-audit-contract.md`：P-ARC 是现有 LLM 观察，不新增评分或 pre-submission 路由。
- `testing-and-tooling.md`：C1/C2/C3 当前维护契约及按技能测试加载。
- `docs-bilingual-resources.md`：任何公开源改动必须同步 source-faithful EN、完整ZH译文、manifest 和构建。

## External references

本研究按派发边界只读本仓库并运行本地既有 CLI，未联网。外部先例、许可与 qiaomu 采用/拒绝决策由主线程独立研究；本文件不编造外部验证。

## 最小设计收敛（追加的消费者实证）

### 一致性 JSON 协议与承载方式

真实 `--json` 不是纯 JSON：第一行为 `[INFO] Checking N files...`，随后是一个 JSON object：

```json
{
  "terms": {
    "term_occurrences": {"卷积神经网络": 1, "CNN": 3},
    "inconsistencies": [],
    "status": "PASS"
  },
  "abbreviations": {
    "definitions": {"CNN": 1},
    "usages": {"CNN": 2},
    "issues": [],
    "status": "PASS"
  }
}
```

- `terms.inconsistencies[]` 为 `{type, group, counts, suggestion}`；新 C2 的同组表面形式/全称风格均为语义候选，保留 `suggestion`，映射 Info/P3。
- `abbreviations.issues[]` 的确定首用错误为 `{type:"undefined", abbreviation, first_usage:[file,line], usage_count, message}`；可保留非阻断 Minor/P2。注意同一个 `undefined` type 还承载“括号前无可靠全称边界”的 `NEEDS-LLM`：不能只按 type 机械判定缺陷，应保留生产者的显式待核语义。
- 不同全称候选为 `{type:"multiple_definitions", abbreviation, definitions:[[name,file,line],...], message:"NEEDS-LLM: ..."}`，映射 Info/P3；不得转成冲突。
- exit0 表示没有 candidate/issues；exit1 同时涵盖确定首用错误和仅 NEEDS-LLM 的情况。缺失 include 仅产生 coverage stderr 时仍 exit0。
- JSON 不含覆盖容器；stderr 的 `[INFO]` 覆盖声明及 `[WARNING]` loader 警告必须在这一个 consistency 专属消费边界保留为 Info/P3。现有 `AuditIssue` (`report_generator.py:17-28`) 和 `AuditResult` (`:98-128`) **没有 CheckResult/coverage/warnings 新容器**；已有 `message`、`line`、`rationale` 足够，文件名和上下文可原样保留在 message，不能拿 `location` 填造 quote。
- 新具名 JSON adapter 只允许去掉上述固定、完整匹配的一行前缀，然后 `json.loads` 剩余整串；禁止通用“找第一个 `{` 再试”、逐层静默 fallback。协议失败必须可见，不能落入现有 `audit.py:668` 的 exit0 假 clean；正常 exit1 已有合法 payload 时不要再走 `:637-648` 追加一个 Minor/P3 `checker exited 1`，否则 Info 会重新造成扣分。异常退出仍用既有错误呈现，不扩展错误码体系。

### Info 的实际消费检查：需要一个报告评分入口修复

本次 `probe-results.json.info_scoring` 保存真实结果：

| 消费面 | 一条 CONSISTENCY Info/P3 的现状 |
| --- | --- |
| ScholarEval `evaluate_from_audit` | clarity=10，其余保持原值，符合免扣分 |
| quick Markdown / deep Phase0 table / gate advisory / Phase0 context | 均可见原始 NEEDS-LLM 观察 |
| `_presubmission_phase0_issues` | 空列表；只接受 PRESUBMISSION Critical/Major (`audit.py:1361-1363`) |
| editor fallback | 仅收 Critical (`audit.py:1495-1496`)，不把 Info 升级 |
| 四维 `calculate_scores` / JSON report | **clarity=5.75而空列表为6，overall=5.92而空列表为6** |

原因是 `report_generator.py:340-352` 未过滤 Info，并用未知 severity 默认 deduction=0.25。最小修复是在 `calculate_scores` 评分入口统一过滤 Info，沿用 `scholar_eval.py:154` 的既有纪律；不改四维映射、权重、扣分表或新建评分。Info 仍存在 `AuditResult.issues` 并能正常显示。深审最终三档 bundle 不增加第四种 severity：未经 LLM 确认的 Info 留在 Phase0，不能把其直接送入 `sanitize_issue` 并因未知值变成 moderate。

### checklist 的确定选择

对于 `lang=="zh" && fmt==".tex"`，**移除重复的 acronym checklist 项**，首用相关结果以唯一一次 consistency 调用为准。相比将其布尔值改成 false，这一选择不会触发 `render_gate_report` (`report_generator.py:1225-1226`) 的“任意 checklist false 就 FAIL”，也不需要新三态 checklist/coverage schema。必要覆盖说明已经作为一致性 Info/P3 呈现。英文、Typst 原分支保留，`GATE_ELIGIBLE_ZH={spec,blind}` 不变。

### 工作区格式边界与坐标

推荐在 `.tex` 格式边界统一复用已有装配输入；这属于同一工作区输入正确性，而不是新的语言功能。仅对 zh 分支修复会遇到主文件本身没有中文、中文全在 include 内导致无法先识别 zh 的循环条件，并造成一个共享 prepare CLI 两套 LaTeX 真源。应明确列入设计：所有 `.tex` 工作区改读装配内容，EN 多文件增加回归；`.typ/.pdf` 保持现有行为。若主线程选择只做 zh，则必须给出明确可靠的既有语言锁定来源，不能从空的主文件推断。

现有 `AssembledDocument` 与 `_source_span` (`prepare_review_workspace.py:259-272`) 已能通过 `doc.origin` 返回源坐标；`build_subsection_units` 和 window 流已使用这些坐标。全文、section files、claim map 采用同一装配 content，section index 保持既有字段；quote verification (`verify_quotes.py:14-30`) 本来就是全文字符串包含判断，补齐全文即可使子文件原文 quote 可核验，无需改其 schema 或算法。不能把源文件局部行号误说成装配行号；CONSISTENCY 的文件/行保持 producer message，不自动用该行数调用 `_section_for_phase0_issue`。实施须确认已有 PRESUBMISSION section mapping 的坐标基准仍一致，必要时只修消费者，不扩张共享 parser/loader。

可将现有装配对象传入 subsection 生成路径以在准备工作区时只装配一次；这是 `prepare_review_workspace.py` 内部调用整理，需同时核对 `audit.py:2607` 的 polish 调用和已有 `.tex/.typ/.pdf` subsection tests，不能增加新公开 CLI 或兼容层。

### 路径与资源同步的建议白名单

- 产品脚本：`paper-audit/scripts/audit.py`、`zh_check_adapters.py`、`prepare_review_workspace.py`、`report_generator.py`。当前证据不要求修改 `paths.py`、consolidator、quote verifier、shared loader/parser、ScholarEval 权重文件。
- 当前链的路径事实源：`paper-audit/SKILL.md`、`references/SUBAGENT_TEMPLATES.md`、`references/workflow-detail.md`、`agents/zh_thesis_reviewer_agent.md`。把读写路径统一到现存 `WorkspaceLayout`；需要同步触发/用法的 `references/REVIEW_LANE_GUIDE.md` 和 `MODE_GUIDE.md` 由主计划明确列入，不能临时扩张全 agent 目录。
- 中文内容边界：`references/ZH_THESIS_REVIEW_CRITERIA.md`、`references/OVER_CLAIM_GUARD.md`；现有 claims/notation playbooks如需具体指引分别为 `agents/claims_evidence_reviewer_agent.md`、`agents/notation_consistency_reviewer_agent.md`，复用现有模板 lane，不新增 reviewer。
- `_copy_workspace_references` 最少新增两份实际依赖：`ZH_THESIS_REVIEW_CRITERIA.md`、`OVER_CLAIM_GUARD.md`；后者上位 `CLAIM_EVIDENCE_CONTRACT.md` 已在清单内。中文准则若继续引用其他详细资源，明确相对 skill 读取边界或补必要源，禁止“全部复制 references”来掩盖未梳理的依赖。
- 公开改动均需对应 `docs/skills/paper-audit/resources/`、`docs/zh/skills/paper-audit/resources/`、`docs/resource-manifest.json`；eval/fixtures 和上文列出的相关 tests 在主计划按实际 source 文件逐一绑定。仅调教学保真与消费接线，不新增 mode/flag/threshold/schema/score dimension。

## Caveats / Not Found

- 没有真实论文、LLM/provider 审稿样本、学校验收或五宿主 fresh-session 证据；语义质量保持 `UNVERIFIED / missing evidence`。
- 当前 `run_deep_review` (`audit.py:1962,2023-2042`) 是 deterministic fallback，未调用模型；中文 fallback 检测到中文就写“评阅维度待复核”，本次不得把其 generic issue 说成独立中文审稿完成。无需本轮改造新 agent runtime。
- 根因报告只要求 paper-audit 的上述必要消费边界；C1/C2/C3 producer 已完成，原 compile 修复/全套 tests 不应再次修改。其他无关启发式/评分基线失败留给各自任务。
- 研究角色仅允许写本任务 research，未写 Basic Memory checkpoint；主线程应按其会话授权与可用技能处理持久交接。
