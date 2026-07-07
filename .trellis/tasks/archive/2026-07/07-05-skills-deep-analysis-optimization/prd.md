# 六技能深度问题分析与优化

## Goal

对 `academic-writing-skills/` 下六个 skill（latex-paper-en、latex-thesis-zh、typst-paper、bib-search-citation、cover-letter、paper-audit）做一轮深度问题分析，重点覆盖 2026-06-20 复审之后新增且未经独立审计的功能（deai 结构壳检查、时态信号词检测、REVIEWER_PSYCHOLOGY、OVER_CLAIM_GUARD），以及横切面（版本一致性、测试架构、文档站漂移）。将确认的问题按主题聚合为可独立验收的子优化任务。

本任务为**父任务**：持有问题总集、子任务地图与跨子任务验收，自身不做实现。

## Scope

- 分析输入：六个 skill 的 scripts/、SKILL.md、references/、agents/、evals/、examples/，根 tests/、docs/、CI 配置。
- 排除（历史审计已确认修复或有意为之，不重复报告）：
  - parsers.py 按技能副本差异（test_parsers_alignment.py ALIGNMENTS 锁定）
  - latex-thesis-zh F1-F24（已全量修复）
  - 五技能优化 / 六技能复审已关闭的项
  - paper-audit 跑 deai 不传 --analyze（有意设计：deai trace 不流入 audit 评分）

## Requirements

- R1 每个发现必须有文件:行号级证据，标注严重度（high/medium/low）或 enhancement。
- R2 分析产物持久化在本任务 `research/` 下（5 份分组 findings）。
- R3 确认的问题按主题聚合为子任务（`--parent` 挂本任务），每个子任务有独立可测的验收标准。
- R4 无证据不立项；分析结论与历史 memory 冲突时以现场代码为准并注明。

## Acceptance Criteria

- [ ] research/ 下 5 份 findings 文件齐全（en-typst、zh、paper-audit、bib-cover、crosscut）。
- [ ] 发现的问题经过主会话复核（剔除误报）后写入本 PRD 的"问题总集"章节。
- [ ] 每个确认的问题主题都有对应子任务，子任务 prd.md 含验收标准。
- [ ] 子任务地图记录在本 PRD；跨子任务的顺序依赖写入各子任务 prd.md。

## 问题总集

来源：research/ 下 5 份 findings（en-typst / zh / paper-audit / bib-cover / crosscut）。主会话已抽查坐实 ZH-1、XA-1、PA-1、CL-1 四项最高价值发现的代码现场。CI 基线：`just ci` 843 tests 全绿。

| 编号 | 严重度 | 位置 | 一句话描述 | 子任务 |
|---|---|---|---|---|
| ZH-1 | high | latex-thesis-zh deai_check.py:774-791 | 英文摘要时态门控不识别 thuthesis `abstract*`/pkuthss `eabstract`，旗舰模板上静默 no-op | zh-abstract-tense-gating |
| ZH-2 | medium | 同上 | 多 abstract 只取首个，中前英后布局漏检 | zh-abstract-tense-gating |
| ZH-3 | medium | tests/test_deai_tense.py | zh 时态逻辑零测试覆盖 | zh-abstract-tense-gating |
| ZH-4 | low-med | zh references | 时态检查器无文档，tense-guide-zh.md 孤儿 | zh-abstract-tense-gating |
| XA-1 | medium | typst deai_check.py:602 | low_information_density 在剥掉 @cite 的文本上查证据，引用密集段误报；EN 的 E17 修复未同步 | typst-deai-sync |
| XA-2 | low | typst deai_check.py | @fig 交叉引用被剥导致图表时态护栏失效 | typst-deai-sync |
| XA-3 | low | typst deai_check.py | term 列表较 EN 漂移 | typst-deai-sync |
| SH-1 | low-med | en+typst deai_check.py | `presents?` 正则误伤 "the present study" | typst-deai-sync |
| TST-1 | medium | tests/ | deai 系测试只导入 EN 副本，typst 零覆盖 | typst-deai-sync |
| XC-3 | medium | tests/ | deai_check 三副本无对齐锁（parsers.py 有、deai 没有） | deai-alignment-lock |
| XC-3b | low | tests/ | bare import deai_check 永远拿 EN 副本的静默陷阱 | deai-alignment-lock |
| PA-1 | medium | scholar_eval.py:265 | critical_count 惩罚生产路径死代码，单测直连掩盖断链 | paper-audit-scoring-fixes |
| PA-2 | medium | literature_compare.py:225 | 空文献检索结果被当"文献根基差"拉低总分 | paper-audit-scoring-fixes |
| PA-3 | low | scoring_model.py:159 | dims_below_5 把 overall 计入维度 | paper-audit-scoring-fixes |
| CL-1 | medium | verify_letter_against_manuscript.py:57-100 | 数值校验不验指标身份，"3% 吞吐提升"冒充"3% 精度提升"可通过 | cover-letter-bib-fixes |
| BIB-1 | medium | search_bib.py:777-857 | 重复引用键静默双条返回，无 warning | cover-letter-bib-fixes |
| BIB-2 | low | search_bib.py:793-801 | % 注释条目仍被解析 | cover-letter-bib-fixes |
| CL-2 | low | cover-letter scripts | "Dear Editor," 粘进首 claim 句 | cover-letter-bib-fixes |
| XC-5 | medium | CLAUDE.md:104 | pyright 写 "off" 实为 "basic" | docs-metadata-consistency |
| XC-6 | medium | docs/.vitepress/dist | 编译产物被 git 跟踪（且在 .gitignore） | docs-metadata-consistency |
| XC-4 | low | docs/ | docs 镜像缺 tense-guide 与 paper-audit 新功能 | docs-metadata-consistency |
| PA-4/5/6 | low | paper-audit SKILL.md/agents | "regression-based" 措辞矛盾、argument-hint 缺 flag、"8 Challenges" 实为 11 | docs-metadata-consistency |
| XC-1/1b | low | SKILL.md 元数据 | last_updated 滞后、bib category 不统一 | docs-metadata-consistency |
| XC-6b | low | docs/report/ | csw-vs-aws-analysis.md 疑似孤儿 | docs-metadata-consistency |
| CL-3/CL-4 | enhancement | cover-letter | 缺结构级 AI 痕迹检查与信↔稿件 AI 披露一致性交叉检查 | cover-letter-deai-enhancement（可选） |

确认干净、无需立项的维度：红线合规（全部 skill 的脚本只读只报告）；GB/T 7714 2015/2025 分支分离；REVIEWER_PSYCHOLOGY / OVER_CLAIM_GUARD 自身逻辑（权重精确 1.00、四侧接入一致）；bib 解析的 @string/crossref/嵌套/编码；SKILL.md version 全仓 5.2.0 同步；docs EN/zh locale 137=137；parsers.py 副本分歧（ALIGNMENTS 有意锁定）。

## 子任务地图

| 子任务 | 主题 | 优先级 | 顺序依赖 |
|---|---|---|---|
| 07-05-zh-abstract-tense-gating | ZH-1 high + 同根因链 | P0 | 无 |
| 07-05-typst-deai-sync | typst 副本同步 + 测试 | P0 | 无（与 zh 任务可并行） |
| 07-05-deai-alignment-lock | 三副本对齐锁 | P1 | **须在上两个任务之后** |
| 07-05-paper-audit-scoring-fixes | 评分链断链 | P1 | 无 |
| 07-05-cover-letter-bib-fixes | CL-1/BIB-1 等 | P1 | 无 |
| 07-05-docs-metadata-consistency | 纯文档/元数据 | P2 | 建议在 zh/typst 修复后（last_updated 一次到位） |
| 07-05-cover-letter-deai-enhancement | enhancement | 可选 | 用户确认后再 start；父任务验收不含此项 |

## 遗留事项

- `research/_scratch/`（en-typst 代理复现用临时目录）删除被权限拦，需手动清理，内容无害。
