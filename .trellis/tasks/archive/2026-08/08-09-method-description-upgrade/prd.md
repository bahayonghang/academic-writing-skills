# 方法描述模块升级：模块叙述契约与报幕反模式治理

## Goal

消除三个写作技能产出方法描述时的"行内小标题 + 一段机械介绍、模块间无因果衔接"反模式（标题报幕）。
把用户《方法描述规范》中可泛化的部分落进 latex-thesis-zh、latex-paper-en、typst-paper 与 paper-audit，
使方法节/方法章的改写与诊断满足：模块由约束引出、相邻模块有显式接口、公式有闭环、收益表述不越证据。

## 源需求

1. 用户提供《方法描述规范》spec（会话内全文），核心增量为验收清单 M-* 十项。经全仓差距核查：
   - **零覆盖（本任务核心）**：M-EDGE（逐边接口：上游产出/连接变换/下游用途 + 六类连接类型）、
     M-NONDIRECT（排除非直接依赖误解）、M-HEADING（标题报幕反模式）。
   - **部分覆盖（升级）**：M-EQUATION（zh 仅"式中"释义 LLM 抽样）、M-EVIDENCE（对接现有
     over-claim-guard / claim-evidence-contract，不新建体系）、M-MOTIVE / M-RATIONALE / M-IO
     （EN Module Triad 已有，补"剩余约束链"与逐边视角）。
   - **已覆盖（不动）**：M-REPRO（E-DATA/E-PARAM、Implementation details）、M-CLOSURE（zh 本章小结模板）。
2. 症状实例：用户论文截图（连续 `\paragraph{倒置 DCS 编码。}` 式行内小标题 + 公式，无模块间衔接），
   对应 spec §9 "标题报幕"反例。

## 子任务映射

| 子任务 | 交付物 | 排序约束 |
| --- | --- | --- |
| 08-09-method-desc-zh | zh 新参考 `method-description-guide-zh.md` + `analyze_logic.py --method-narrative`（显式 `--section` 选章）M-* 检查 + 测试 + 文档同步 | 先行（M-* 判据首个实现） |
| 08-09-method-desc-en-typst | EN `section-writing/method.md` 扩展 + EN/typst `--section methods` 补 M-* + typst 镜像参考 + TRANSITIONS 增 `sequence` 类 + 跨技能 M-* 契约测试 | 可与 zh 并行；判据以父 design §2 为唯一权威 |
| 08-09-method-desc-audit-sync | paper-audit：Phase 0 logic 双调用 + `_parse_script_output` 块感知与 Info/P3 语义 + focus block/C5（"方法论接口与论证完整性"框架）+ paper-audit 双语资源全链同步 + 跨子集成验收 | 依赖 C1/C2 定稿后执行 |

## 跨子任务验收标准

- [x] M-EDGE / M-NONDIRECT / M-HEADING 在三个写作技能中均有 LLM 车道参考指导；M-HEADING /
      M-SEQWORD / M-EQUATION 有节门控脚本候选检查，判据与父 design §2 一致，并由
      `test_method_narrative_alignment.py` 契约测试锁定（非人工 diff）。
- [x] 红线负例零误报（写进各自 compliant fixture）：① EN/typst Related Work 的
      `\textbf{...方法组.}` / `*...*` 分组标题；② typst `modules/EXPERIMENT.md` 要求的实验分析段
      `*Title Case Heading.*` lead-in；③ zh `analyze_experiment.py` 要求的 `\paragraph{核心结论概括}`。
- [x] spec §9 "标题报幕"病例在新检查下被检出（M-HEADING 命中），且参考文件给出约束驱动改写骨架。
- [x] paper-audit 评分链验收：块感知解析后单条 M-* finding 计 1 条 issue；Info/P3 finding 不参与
      ScholarEval 扣分；病例 fixture 的 soundness 扣分仅来自 Minor 项。
- [x] `just ci` 全绿；三个写作技能与 paper-audit 分别通过
      `docs/scripts/check_resource_sync.py --skill <skill>`；C3 终检全量 checker + `just doc-build`。
- [x] paper-audit 侧：section_methods lane 有专属 focus block（措辞不含"写作质量"）；zh 文档
      不进 audit 方法节第二调用的边界已在 paper-audit 文档声明。

自动化证据与命令记录见已归档 C3 的 `research/integration-evidence.md`。这些证据只覆盖合成病例、
干净对照和合法标题负例；真实论文语料的查准率与召回率仍为 `UNVERIFIED`。

## 排除项（本任务不做）

- 不新建独立技能；不改变六技能定位（写后打磨/校验）。
- zh 不新建 claim-evidence-contract 文件（spec §6 四类主张映射到现有 over-claim-guard 词表）。
- 不动九维权重、不动 `MODULE_DIMENSION_MAP`、不动 `--strength` / Risk-Flags 等润色契约字段。
- 用户 spec 中四篇本地论文对照与水泥案例不进 core 参考（原文存档于
  `research/user-spec-method-description.md`，fixture 素材须脱敏改写）。
- 不重建 M-REPRO / M-CLOSURE 已覆盖能力（指路现有模块）。
- 遗留清单（登记于 `research/repo-recon.md` §4，另行小任务处理）：TRANSITIONS `example` 类
  扩充；typst `modules/LOGIC.md:86` 大小写引用修复；audit 解析膨胀对 logic 以外委托模块的
  影响面清理。

## 全局约束

- 红线：不修改 `\cite{}`/`\ref{}`/`\label{}`/数学环境与 Typst 对应物；不虚构事实与实验结论。
- 所有 `[Script]` 输出恒 `Meaning-Check: NEEDS-LLM`（既有裁定，勿重开）。
- SKILL.md `version:` 不 bump，只改 `last_updated`（test_skill_versions 锁）。
- 诊断输出沿用 diff/suggestion 块 + Severity + Priority + `[Script]`/`[LLM]` 标注格式。
- EN/typst `analyze_logic.py` 为 Tier-2 同构副本：改动须手工镜像保持函数集同构。
