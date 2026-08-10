# paper-audit 方法叙述接线与契约文档同步

## Goal

把方法叙述候选检查接进 paper-audit 的评分链（Phase 0 双调用 + 解析升级）与报告层
（focus block / C5），完成 paper-audit 公开资源的双语契约同步，并承担父任务跨子集成验收。
依赖 C1/C2 归档。能力命名一律为**方法论接口与论证完整性**（父 design §5，不用"写作质量/
叙述质量"措辞）。

## 背景（已核实机制，见父 research/repo-recon.md §2.1）

- Phase 0 logic 委托三技能 `analyze_logic.py`（audit.py:372-425），现只传 `--cross-section`
  单次调用（:2465）；EN/typst 传 `--section` 会关闭全文检查（互斥门控）→ 必须双调用。
- `_parse_script_output`（:458-514）逐行成 issue、只认 Critical|Major|Minor 与 P0-2：
  一条 4 续行 finding 膨胀为 5 条 Minor/P2（soundness 10→7.5），Info 头行升级为 Minor。
  评分链验收前必须修块感知解析与 Info/P3 语义。
- LLM 车道发现不进分数（:2586-2593）；LOGIC→soundness 映射已存在，不改
  `MODULE_DIMENSION_MAP`。

## Requirements

### R1 Phase 0 双调用

logic 检查对 `.tex`(en)/`.typ` 文档增加第二次调用 `--section methods`；第一次全文调用
（`--cross-section`）参数与解析路径不变。两次输出各自解析后合并为 LOGIC 模块 issue（去重
无必要——两次调用的检查集合互斥）。zh 文档不做第二调用（zh 方法叙述需显式选章，audit 无
章号语境）；该边界写入 paper-audit 的 SKILL.md 或模块文档作为已声明限制。

### R2 解析升级 `_parse_script_output`

1. 块感知：finding 头行（含 `[Severity: ...] [Priority: ...]`）开一条 issue；后续
   Current/Suggested/Rationale/Meaning-Check 续行并入该 issue（进 message 附注或丢弃，
   设计定：丢弃续行、保留头行消息——issue 语义最小充分），空行结块。无头行的裸输出行维持
   现状（逐行 Minor 兜底）。
2. severity 识别扩 `Info`、priority 扩 `P3`；Info issue 进报告与上下文，不参与 ScholarEval
   扣分（`scholar_eval` 侧显式过滤或计 0，实现时核实其对未知 severity 的现行为后选点）。
3. 回归策略：本修复改变**所有**委托模块的 issue 计数与分数基线。本任务验收范围 = logic 链
   正确 + 现有 paper-audit 测试套调整到新语义（逐一审视，调整理由写测试注释）；其他模块的
   语义级影响面清理在遗留清单（父 research/repo-recon.md §4.3）。

### R3 报告层（措辞按能力命名约束）

1. `SUBAGENT_TEMPLATES.md`：`section_methods` 增专属 focus block（对齐 cross-cutting lane 的
   DO/DON'T 格式）。DO：六角色必答、逐边三对象（上游产出/连接变换/下游用途）、M-NONDIRECT、
   公式闭环缺失检测（区别于 notation 矛盾检测）、收益表述对照 OVER_CLAIM_GUARD 阶梯。
   DON'T：不评 notation 矛盾、不评格式与语言表面质量、三处合法行内小标题不报、不改
   severity 定义。
2. `critical_reviewer_agent.md` C5：增模块小节粒度的邻接完整性检查（连接类型增
   interface/residual-constraint 两型），分级沿用 C5 现有口径。
3. `DEEP_REVIEW_CRITERIA.md` #16 与 `REVIEW_LANE_GUIDE.md` section_methods 行各补一句
   （接口与论证完整性框架）。

### R4 双语契约全链（paper-audit 公开资源）

本任务改动的 `references/*.md` 与 `agents/*.md` 均为公开源（spec §3 范围含 agents/**/*.md）：
`check_resource_sync.py --write-manifest` → docs/ 英文页与源一致 + docs/zh 完整中文译文
（含新增/修改的每个文件页对）→ `--skill paper-audit` → 全量 checker + `just doc-build`。

### R5 跨子集成验收（父 implement.md §2 五项）

1. `test_method_narrative_alignment.py` 绿（契约锁替代人工 diff）。
2. 红线负例三条在三技能 fixture 锁定情况核对。
3. spec §9 病例端到端：三技能检查器 + paper-audit Phase 0 输出摘要存 research/。
4. 评分链验收：单条 M-* finding 计 1 issue；Info 不扣分；病例 fixture soundness 分差仅来自
   Minor 项（干净版对照）。
5. 全仓 `just ci`、四技能 `--skill` 自查、全量 checker、`just doc-build`；hypothesis 结论
   记父任务 journal。

## Acceptance Criteria

- [x] 双调用落地：EN/typst 文档 audit 产出方法节 M-* issue，全文检查（cross-section 等）
      无回归；zh 边界已在 paper-audit 文档声明。
- [x] 解析升级落地：块感知 + Info/P3 语义有专项单测（含"一条 4 续行 finding 计 1 issue"与
      "Info 不扣分"断言）；现有测试套调整完成且逐条有注释理由。
- [x] focus block / C5 / 两处参考同步完成，新增 diff 无"写作质量/叙述质量"措辞。
- [x] R4 双语全链通过（`--skill paper-audit` + 全量 checker + `just doc-build`）。
- [x] R5 自动化集成验收与 research 证据已完成；真实论文语料的查准率与召回率保持
      `UNVERIFIED`，父任务 journal 记录由主会话收口。
- [x] `MODULE_DIMENSION_MAP`、九维权重及 Critical/Major/Minor 既有扣分权重零改动；新增 Info
      显式零扣分语义；paper-audit SKILL.md version 未变更。

## 排除项

- 不改 methodology_reviewer / synthesis / EIC 职责边界。
- 不为 paper-audit 新建方法写作参考文件（focus block 指路 EN 权威参考路径，说明性引用）。
- audit 解析膨胀对 logic 以外模块的语义级清理（遗留清单）。
