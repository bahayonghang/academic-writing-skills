# 中文大论文审查与写作保真规范对齐

## Goal

让 `paper-audit` 的中文学位论文审查真正消费已完成的写作保真与一致性修复，定位无依据的数字、因果、首次和范围主张，同时保留合法综合、理论/工程表达与强证据结论。审查必须来自实际全文和规则输入。

本轮只创建可执行规划，未授权新任务实施。先行收口已完成：旧实施提交 `4e47e8e`，父子四任务归档到 `.trellis/tasks/archive/2026-09/`；journal 后基线 `41c0cf7447989391e96a3bd79c8e7e697cf8d0f6`。旧 24 项 AC / 1908 passed / 2 skipped 是写作侧证据，不是新审查效果。

## Confirmed Facts

实跑命令、输入和 hash 见 [链路研究](research/audit-chain.md) 与 [探针结果](research/probe-results.json)。

| 事实 | 当前证据 | 意义 |
| --- | --- | --- |
| 中文 profile、15 行指标和 zh lane 已存在 | `academic-writing-skills/paper-audit/references/ZH_THESIS_REVIEW_CRITERIA.md:1` | 增量修复，不重建 profile |
| consistency 调用新版 checker，但无具名 adapter | `academic-writing-skills/paper-audit/scripts/audit.py:2744`；`academic-writing-skills/paper-audit/scripts/zh_check_adapters.py:391` | clean 变成 10 条 Minor，独立送 ScholarEval 后 clarity 10→5 |
| 四维评分不滤 Info；正常结果 exit1 还追加 Minor | `academic-writing-skills/paper-audit/scripts/report_generator.py:325`；`academic-writing-skills/paper-audit/scripts/audit.py:637` | 仅映射 Info 不够，两处消费边界须修正 |
| zh 首用清单另用白名单、任意位置定义和≤3容差 | `academic-writing-skills/paper-audit/scripts/audit.py:2201` | 同句先用后定义仍打勾 |
| 深审只读入口，子节窗口才装配 include 图 | `academic-writing-skills/paper-audit/scripts/prepare_review_workspace.py:871`；`academic-writing-skills/paper-audit/scripts/prepare_review_workspace.py:701` | 两子文件正文未进入全文、section/claim map 和 quote 核验 |
| zh 模板写旧目录，workspace 未复制必要规则 | `academic-writing-skills/paper-audit/agents/zh_thesis_reviewer_agent.md:22`；`academic-writing-skills/paper-audit/scripts/prepare_review_workspace.py:836` | 旧路径评论消费0条，canonical路径同条消费1条 |
| guard 以消融名称许可强因果，并用 hedge 保留首次资格 | `academic-writing-skills/paper-audit/references/OVER_CLAIM_GUARD.md:52`；`academic-writing-skills/paper-audit/references/OVER_CLAIM_GUARD.md:59` | 与旧 C1 冲突；已证规则可达，未证明真实 LLM 已犯错 |

## Requirements

- R1: 判据与交付链。修正数字/因果/首次模板；中文准则明确学校、学位、理论/工程功能、合法综合引用、逆向提纲和概念区分。规则从 workspace 可加载，评论进入真实合并目录；原 lane 条件、max 8 和只审不改边界保持。
- R2: 一致性结果保真。消费已有 JSON 协议，确定首用问题一对一作为 advisory，NEEDS-LLM/覆盖信息为 Info/P3，clean 不造问题。正常 exit1 不追加工具失败；Info 在两套评分均不扣分，Phase0/报告可见但不自动升级 deep issue。删除 zh `.tex` 重复首用 checklist 项，不把 advisory 新变成 gate blocker。
- R3: 多文件证据。复用已有 `tex_loader.assemble`，`.tex` workspace 的全文、语言识别、分节、claim map 和子节窗口共用一次装配；区分原文件与提取坐标，持久披露 loader 覆盖警告。不扫描不可达草稿、不新建 loader/schema；共享修复包含英文 `.tex` 回归，`.typ/.pdf` 保持原路径。
- R4: 编译证据。audit 不自动编译或修工程。仅在作者提供本次命令、目标目录、退出码和目标 PDF 证据时评议构建；缺证据标未验证。成功不证明学术结论、学校版式或现场验收；C3 算法验收继续由旧任务承担。
- R5: 验证与同步。执行 [E01—E16 场景合同](research/acceptance-cases.md)，保护历史 trigger/eval 顺序、评分权重、15行指标、issue schema 和 gate；源规则/双语镜像/manifest/spec 同步，实际 reviewer 响应与独立核读不能被 fixture/fallback 代替。

## Acceptance Criteria

- [ ] AC1 (R1): E01—E08、E12 同输入前后实际 reviewer 输出完成独立核读，新版全部满足场景合同；保存输入/规则 hash 与原始响应，合法反例允许空 issues。至少一例真实 reviewer JSON 从文档指定 `artifacts/comments` 经 consolidation 和 quote verification 消费；两份必要规则在 workspace 可读，原语言/focus 条件不漂移。
- [ ] AC2 (R2): 真实 checker clean 缺陷为0；E10 每项确定问题一次且原文件/行号正确；E11 仅 Info/P3，正常 exit1 无额外失败，两套评分与空缺陷基线一致，gate 不因 Info/consistency 新失败。Phase0/quick/JSON 可见待判或覆盖，deep 不自动升级；zh 重复首用清单消失，EN/Typst 清单不变。非法JSON、exit2、超时显式报错，不视为clean。
- [ ] AC3 (R3): E13 两子文件正文进入 full_text、分节与 claim map，子文件原句通过 quote verification；同次 workspace 只装配一次，既有 subsection source 坐标不变。E14 警告保存在 summary 并进入 reviewer 输入，最终报告说明限制。单文件/英文多文件 `.tex` 及既有 Typst/PDF/overwrite 行为通过相关回归。
- [ ] AC4 (R4): E15 四种构建记录的实际 reviewer 响应分别判为已证构建、不能通过、不能通过、UNVERIFIED；数值/路径不变，不启动 TeX，不外推学术/学校/现场通过。
- [ ] AC5 (R5): 历史24条eval/20条trigger的对象与顺序完整保留，新例追加且ID不冲突；paper-audit tests、受影响 contracts、资源单技能/全量、docs build、`just ci`四步通过。权重/扣分表、ScholarEval维度、gate eligible、issue schema、写作侧产品无范围外diff；已通过/失败/跳过/未验证证据分列。

## Scope and Decisions

单一复杂任务，按 `implement.md` 顺序推进，同一 `audit.py` 不并发写；白名单见 `design.md`。共享 over-claim、Info 免扣分和 `.tex` workspace 的跨语言影响已纳入验证。

不新增技能包、模式/CLI/配置/依赖/IR/安装器、评分体系或学校阈值；不扩自动 method-narrative/RA/P-ARC；不改共享 parser/loader 或重做旧 producer；不加旧 comments 兼容层。真实论文编辑、GUI、在线论文核验、真实盲评、五宿主和发布/推送不在范围。

## Risks and Evidence Limits

当前探针仅证明缺口，不证明优化效果。语义 AC 在实施期必须实跑，能力不可用时保持未完成；真实论文总体质量、学校版式、五宿主/provider benchmark 单列 UNVERIFIED，不作为本增量任务额外完成门槛。先例与拒绝见 [prior-art-research](reports/prior-art-research.md)。
