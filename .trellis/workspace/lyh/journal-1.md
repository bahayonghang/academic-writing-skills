# Journal - lyh (Part 1)

> AI development session journal
> Started: 2026-06-05

---



## Session 1: Paper section reference integration

**Date**: 2026-06-05
**Task**: Paper section reference integration
**Package**: claude-scholar
**Branch**: `dev`

### Summary

Integrated section-specific writing references into latex-paper-en, added a bounded thesis-writing adaptation for latex-thesis-zh, reorganized both reference trees into lowercase category directories, mirrored docs resources, added layout contracts, and verified with just ci.

### Main Changes

(Add details)

### Git Commits

| Hash | Message |
|------|---------|
| `8d9fa96` | (see git log) |

### Testing

- [OK] (Add test results)

### Status

[OK] **Completed**

### Next Steps

- None - task complete


## Session 2: latex-thesis-zh 章引言承上启下能力补强

**Date**: 2026-06-12
**Task**: latex-thesis-zh 章引言承上启下能力补强
**Package**: claude-scholar
**Branch**: `dev`

### Summary

新增 _check_chapter_intro（随 logic 默认输出）对正文各章引言做承上/启下/相对指代/篇幅检查，绪论显式排除；新增 thesis-writing-guide 章引言写作节 + structure-guide/logic.md 指向 + SKILL.md 路由接线 + 4 个 fixture。归档了旧 academic-writing-skill-supplement 父子任务（保留 00），新建并完成本任务。完整 tests 623 passed、pyright 0 error。

### Main Changes

(Add details)

### Git Commits

| Hash | Message |
|------|---------|
| `7cf89e8` | (see git log) |

### Testing

- [OK] (Add test results)

### Status

[OK] **Completed**

### Next Steps

- None - task complete


## Session 3: Bootstrap project guidelines

**Date**: 2026-06-12
**Task**: Bootstrap project guidelines
**Package**: claude-scholar
**Branch**: `dev`

### Summary

Populated .trellis/spec for claude-scholar, PaperSpine, and Research-Paper-Writing-Skills, updated the bootstrap task checklist, and archived 00-bootstrap-guidelines.

### Main Changes

(Add details)

### Git Commits

| Hash | Message |
|------|---------|
| `5594f3f` | (see git log) |

### Testing

- [OK] (Add test results)

### Status

[OK] **Completed**

### Next Steps

- None - task complete

---

## 2026-06-12: latex-thesis-zh 审计任务树全量实施（6/6 子任务完成）

### Summary

按 06-12-latex-thesis-zh-optimization 任务树完成全部 24 项审计发现（F1-F24）的修复，
6 个子任务各一个 commit，`just ci` 全绿（724 tests passed）。

### Key Changes

- **parsers-multifile (P0)**：新增 tex_loader.py 统一 include 解析（行号映射回 源文件:行号、
  编码三级回退）；split_sections 重写（同名章节 method_2 后缀、注释/starred/空格标题修复）；
  9 个分析脚本接入；--section 支持中文章节名。
- **gb7714-validation (P0)**：--standard gb7714 真实生效（[D]/[R]/[P]/[S]/[EB/OL] 必填字段、
  期刊卷页、等/et al. 混用）；新增 gb7714-2025 取值与过渡期文档。
- **checker-precision (P1)**：破折号 run 计数、未匹配章节纳入检查、PyYAML 可选化、
  术语组语义重设计（国标"全称（缩写）"惯例零误报）、check_format 降噪、AIGC 政策一节。
- **router-cli-alignment (P1)**：C3 并入默认全文档模式；新增 references 模块行；
  $SKILL_DIR 约定显式化；docs 双语镜像同步。
- **template-knowledge (P1)**：删除 university-templates 冗余（templates/ 单源）；
  thuthesis v7.6.0/bst 事实更新；pkuthss 归档标注；figure_format 出脚本。
- **fixtures-evals (P2)**：evals/fixtures/thesis-project 多文件虚构工程（23 项埋点）；
  7 条 evals 绑定 fixture；41 例覆盖测试（含 14 条路由命令冒烟）；孤儿清零。

### Git Commits

| Hash | Message |
|------|---------|
| `e46bddd` | refactor: 多文件论文解析与章节切分修复 (F3/F4/F11/F22) |
| `7ee5dc4` | chore: ruff 排除 .trellis 工具码 |
| `3e0e4ec` | feat: GB/T 7714 校验真实现并适配 2025 新国标 (F1/F2/F12/F18) |
| `59810a2` | fix: 检查器精度修复与 AIGC 政策对接 (F5-F8/F16/F23/F24) |
| `83a933d` | docs: 对齐 SKILL.md 路由契约与脚本 CLI (F9/F10/F13) |
| `71d4d0b` | refactor: 模板知识单源化并更新 2026 事实 (F14/F15/F18/F20) |
| `7e0b5c5` | test: fixture 论文工程与评测/测试补全 (F19/F20/F21) |

### Learnings / Gotchas

- ZH analyze_abstract/check_tables 因引入 tex_loader 退出 TIER1 字节对齐组
  （test_writing_modules_alignment.py 已记录）；改共享模块前先查三个对齐测试：
  test_parsers_alignment / test_writing_modules_alignment / test_venue_templates_layout。
- deai_batch 的 template_exprs 正则曾整体非法（(?:?:...)），零测试导致带病上线 18 个月 —
  新增脚本必须随手配冒烟测试。
- evals fixture 放 skill 内 evals/fixtures/（非 PRD 原定 tests/fixtures/），
  保证 skill-creator 评测 files 路径可达且安装后自包含。

### Status

[OK] **Completed** — 父任务 5 条集成验收全部满足；6 个子任务目录保留待 review 后 archive。

### Next Steps

- 用户 review 后可逐个 `task.py archive` 六个子任务与父任务。
- GB/T 7714-2025 于 2026-07-01 实施后，可考虑把 gb7714-2025 设为默认。



## Session 4: cover-letter C1-C23 收尾(C21 中文触发)+ 投稿合规任务提交归档

**Date**: 2026-06-13
**Task**: cover-letter C1-C23 收尾(C21 中文触发)+ 投稿合规任务提交归档
**Package**: claude-scholar
**Branch**: `dev`

### Summary

完成 06-13-cover-letter-compliance 收尾:C21 中文触发(SKILL.md description/when_to_use 补中文 token+求职信负向边界,trigger_eval 补 5 条中文例至 21 条 11正/10负)。整任务 R1-R5/C1-C23 经 just ci 全绿验收(821 passed,lint/pyright 0 error),修复 \thanks 作者提取、align-check 段级数字共现、ICMJE 2026.1 ai_disclosure、检查器健壮性等。提交 6155dea(36 文件 962+/289-)。本轮一并归档 5 个完成任务:cover-letter-compliance + bib-robustness/en-family-parsers/en-paper-precision/typst-reality。父任务 06-12-five-skills-optimization 余 paper-audit-integrity 1 个待做。

### Main Changes

(Add details)

### Git Commits

| Hash | Message |
|------|---------|
| `6155dea` | (see git log) |

### Testing

- [OK] (Add test results)

### Status

[OK] **Completed**

### Next Steps

- None - task complete


## Session 5: 优化 latex-thesis-zh 章节标题架构

**Date**: 2026-06-14
**Task**: 优化 latex-thesis-zh 章节标题架构
**Package**: claude-scholar
**Branch**: `dev`

### Summary

为 latex-thesis-zh 增加 --headings 章节标题架构诊断，覆盖对象-问题-方法、每章最多 5 个直属小节、小节扣合章标题，并完成 skill-creator 评测与本地验证。

### Main Changes

(Add details)

### Git Commits

| Hash | Message |
|------|---------|
| `95ee0bc` | (see git log) |

### Testing

- [OK] (Add test results)

### Status

[OK] **Completed**

### Next Steps

- None - task complete


## Session 6: Optimize latex-thesis-zh formula guidance

**Date**: 2026-06-15
**Task**: Optimize latex-thesis-zh formula guidance
**Package**: claude-scholar
**Branch**: `dev`

### Summary

Added formula line-break guidance for latex-thesis-zh, including format routing, a formula layout reference, template wording, and eval coverage for equation-number displacement.

### Main Changes

(Add details)

### Git Commits

| Hash | Message |
|------|---------|
| `a99eb32` | (see git log) |

### Testing

- [OK] (Add test results)

### Status

[OK] **Completed**

### Next Steps

- None - task complete


## Session 7: Optimize latex-thesis-zh chapter summary guidance

**Date**: 2026-06-18
**Task**: Optimize latex-thesis-zh chapter summary guidance
**Branch**: `dev`

### Summary

Added single-paragraph 本章小结 routing and writing guidance to latex-thesis-zh, synced docs mirrors and VitePress output, added eval/trigger coverage, and validated with doc-build plus full CI.

### Main Changes

(Add details)

### Git Commits

| Hash | Message |
|------|---------|
| `04c7009` | (see git log) |
| `eb0fdd0` | (see git log) |

### Testing

- [OK] (Add test results)

### Status

[OK] **Completed**

### Next Steps

- None - task complete


## Session 8: 借鉴 follow-up：⑤时态信号词检测 / ⑥reviewer怀疑点排序 / ①over-claim进paper-audit

**Date**: 2026-06-20
**Task**: 借鉴 follow-up：⑤时态信号词检测 / ⑥reviewer怀疑点排序 / ①over-claim进paper-audit
**Branch**: `dev`

### Summary

承接 borrow-writing-judgment 的 3 项 follow-up。⑤ deai_check×3 加 _check_tense（同构 _check_overclaim）：en/typst 门控 method/experiment/result 段，zh 用 \begin{abstract} 英文摘要区域门控（排除 cabstract，无则 no-op）+English-line 门控挂 document_traces；只收无歧义现在时报告动词，is/are 刻意不进正则，图表/软件假阳性过滤；+tense YAML 段+3 时态文档+tests/test_deai_tense.py(7例)。⑥ 新增 paper-audit REVIEWER_PSYCHOLOGY.md（8层怀疑点降序）接 critical_reviewer/synthesis agent（severity 层内 tie-break）。① 新增 OVER_CLAIM_GUARD.md 接 claims_vs_evidence lane(SUBAGENT_TEMPLATES)+claims_evidence_reviewer_agent+CHECKLIST，不改 scholar_eval 权重。关键发现：paper-audit 跑 deai 不传 --analyze，deai trace 不流入 audit（既有行为），故 paper-audit 时态/over-claim 觉察走 ⑥①（文档+LLM lane）非脚本。just ci 837 passed 全绿，未动 parsers.py/scholar_eval 权重/bib/cover-letter。已 fast-forward 合并 dev。

### Main Changes

(Add details)

### Git Commits

| Hash | Message |
|------|---------|
| `3a8e3c2` | (see git log) |
| `8cf4622` | (see git log) |

### Testing

- [OK] (Add test results)

### Status

[OK] **Completed**

### Next Steps

- None - task complete


## Session 9: 学术去 AI 味三技能优化

**Date**: 2026-07-05
**Task**: 学术去 AI 味三技能优化
**Branch**: `dev`

### Summary

优化 latex-thesis-zh、typst-paper、latex-paper-en 的 de-AI 工作流：先保留学术证据链和语法锚点，再检测结构壳/修辞脚手架，并补齐测试、eval、docs 镜像与 Trellis 规范。

### Main Changes

(Add details)

### Git Commits

| Hash | Message |
|------|---------|
| `7311420` | (see git log) |
| `5443df8` | (see git log) |

### Testing

- [OK] (Add test results)

### Status

[OK] **Completed**

### Next Steps

- None - task complete


## Session 10: P0 双任务：zh 摘要时态门控修复 + typst deai 副本同步

**Date**: 2026-07-06
**Task**: P0 双任务：zh 摘要时态门控修复 + typst deai 副本同步
**Branch**: `dev`

### Summary

六技能深审后的两个 P0 修复落地：① latex-thesis-zh 英文摘要时态门控重写（识别 thuthesis abstract*/pkuthss eabstract、多摘要按语种择优），修正模板映射，10 条 zh 专项测试；② typst deai 与 EN 副本同步（E17 证据检查、@fig 护栏、term 表、presents 三副本统一），8 条 typst 测试 + evals/文档补登。guard_text 偏移疑点核实为非 bug 并加回归锁。just ci 861 绿。新增 spec：副本测试 importlib 加载、阈值双层配置、evals.json hook 陷阱。alignment-lock 上锁前提已满足。

### Main Changes

(Add details)

### Git Commits

| Hash | Message |
|------|---------|
| `75a763a` | (see git log) |
| `a6eb919` | (see git log) |
| `fa714a9` | (see git log) |

### Testing

- [OK] (Add test results)

### Status

[OK] **Completed**

### Next Steps

- None - task complete


## Session 11: 四子任务闭环：deai 对齐锁 + 评分链修复 + CL/bib 修复 + 文档一致性

**Date**: 2026-07-06
**Task**: 四子任务闭环：deai 对齐锁 + 评分链修复 + CL/bib 修复 + 文档一致性
**Branch**: `dev`

### Summary

六技能深审剩余四个必做子任务全部实施、质检、提交、归档：① tests/test_deai_alignment.py 为 en/zh/typst 三份 deai_check.py 上锁（strict 字节锁 + AST 去 docstring 逻辑锁把中文注释的 zh 也锁进来 + 关系锁；burstiness 2/4/8 判定为语言驱动有意分歧并 pin 值；漂移红测验证）；② paper-audit 评分链贯通 critical_count 惩罚、空文献检索置 None 按剩余权重归一化并显式标注、dims_below_5 排除 overall，补 REVIEWER_PSYCHOLOGY/OVER_CLAIM_GUARD 契约测试与 evals 21/22；③ cover-letter 指标张冠李戴双路泄漏封堵（数字贴身指标词须全数复现 + unverified 清弱数字锚，质检补修聚合计数）与 bib 重复键/百分号注释条目警告；④ 九项文档元数据清理（pyright basic、dist 解除跟踪、docs 双语补 tense-guide 与 paper-audit 镜像、PA-4/5/6、category/last_updated、孤儿报告删除）。每任务独立 trellis-check 质检；just ci 861→906 绿；docs build 零死链。剩余：cover-letter-deai-enhancement（可选，待拍板）。

### Main Changes

(Add details)

### Git Commits

| Hash | Message |
|------|---------|
| `2a0d9be` | (see git log) |
| `762bf80` | (see git log) |
| `2a31fd9` | (see git log) |
| `02dd30d` | (see git log) |

### Testing

- [OK] (Add test results)

### Status

[OK] **Completed**

### Next Steps

- None - task complete


## Session 12: cover-letter CL-3/CL-4 增强收口，六技能深审父任务 7/7 归档

**Date**: 2026-07-06
**Task**: cover-letter CL-3/CL-4 增强收口，六技能深审父任务 7/7 归档
**Branch**: `dev`

### Summary

实施可选任务 07-05-cover-letter-deai-enhancement：align_check 新增 AI 披露一致性 lane（三情形 moderate finding，comment_type=disclosure_consistency，% 注释披露不触发）；presubmission 同词 AI-tone 阈值 2+/3+ 阶梯、AI-DIV 聚合多样性（3 词 Minor/4 词 Major）、S1 平行段首、S2 句长均匀性（≥8 句 CV<0.25）——按 en 结构壳裁剪移植，不新建 deai_check 副本，对齐锁范围不变。独立质检零缺陷，对抗探针全过；just ci 906→918 绿。取舍：阈值固定 2 不做长度自适应（信件长度方差小、无模板时无基准）；不移植 throat-clearing/低信息密度（信件已有 L2/G3 等价物、声明段易误报）。另单独收纳 Trellis 框架升级 9 文件（agents/config.yaml 仅 EOL 差异未入）。父任务 07-05-skills-deep-analysis-optimization 7/7 全部完成归档。

### Main Changes

(Add details)

### Git Commits

| Hash | Message |
|------|---------|
| `93a67f4` | (see git log) |
| `9bc15d8` | (see git log) |

### Testing

- [OK] (Add test results)

### Status

[OK] **Completed**

### Next Steps

- None - task complete


## Session 13: 整理 tests 测试目录结构

**Date**: 2026-07-07
**Task**: 整理 tests 测试目录结构
**Branch**: `dev`

### Summary

将根 tests 目录的平铺测试按 contracts/shared/skills 分组，新增 tests.support.paths 统一路径常量，更新 conftest、justfile、CLAUDE、Trellis spec 与相关文档引用；验证 pytest 918 passed、ruff、pyright 与 diff check。

### Main Changes

(Add details)

### Git Commits

| Hash | Message |
|------|---------|
| `d516f97c3e8c94cfff2f2e32a898e47a53382567` | (see git log) |

### Testing

- [OK] (Add test results)

### Status

[OK] **Completed**

### Next Steps

- None - task complete

---

## 2026-07-09 — thu/pku/generic 模板检查清单扩充（任务树收尾）

**Date**: 2026-07-09
**Task**: 07-08-template-checklists（父任务 07-08-spec-check-blind-review 第 3/3 子任务）
**Branch**: `dev`

### Summary

trellis-research 网络核实三校规范来源（清华/北大写作指南逐字摘录、thuthesis v7.7.1 手册、GB/T 7713.1 版本关系，10 项缺证如实记录）；三模板各落地逐项检查清单（THU 37 / PKU 35 / GEN 27 条，全部可溯源）；check_spec.py 阈值窄幅参数化（键缺省=燕山原行为，基线逐字节零回归）；负面证据以 BANNED_NON_YS_METHODS 测试固化防阈值外溢；三处有据事实修正（thuthesis 点号默认、pkuthss 符号说明条件式、GB/T 7713.1-2025 版本注记）。质检 9/9 PASS 含零编造逐字抽查 35 条。父任务六条跨子任务验收全过，任务树四目录统一归档。

### Main Changes

- templates/{thuthesis,pkuthss,generic}.md：新增清单节 + 事实修正 + 来源头
- scripts/check_spec.py：TEMPLATE_THRESHOLDS 三模板键 + title_len/kw_count 参数化 + .get() 降级
- 测试净增 15 用例（阈值覆盖/CLI 集成/key_requirements 回归锁）；unknown-template 测试改名
- 文档同步：spec-check.md、SKILL.md 路由行、spec-checklist-convention.md（参数化边界+负面证据规则）

### Git Commits

| Hash | Message |
|------|---------|
| `b6679c6` | feat(latex-thesis-zh): [AI] ✨ thu/pku/generic 逐项检查清单与模板阈值参数化 |
| (archive×4) | chore(task): archive 07-08-*（spec-final-check / blind-review / template-checklists / 父任务） |

### Testing

- [OK] just ci 全绿：1015 passed（基线 1000）；pyright 0 errors 0 warnings
- [OK] yanshan fixture check_spec 输出与改动前逐字节一致（PYTHONIOENCODING=utf-8 采集）
- [OK] detect_template key_requirements diff 仅限三处有据修正

### Status

[OK] **Completed** — 任务树 3/3 子任务完成并归档

### Next Steps

- 遗留（超范围，未排期）：ustcthesis/fduthesis 等 documentclass 自动推断仍 exit 2，需显式 --template generic

## 2026-07-11: latex-thesis-zh 绪论优化（07-10-thesis-zh-intro-optimization）

### 关键决策

- 五项新能力全部挂现有 literature/logic 模块新 flag（--intro-citations / --intro-mainline），不加 Module Router 行，默认行为零变化
- 检查编号用 B1~B5：logic.md 已占用 A4（funnel citation density），沿 A 续排会撞名
- 甘特图判定不入绪论（属开题进度安排），以研究演进时间线图+文献对比矩阵承接用户诉求

### 教训

- [WARN] pytest 命令别加 PYTHONIOENCODING=utf-8：contract 测试 subprocess 跑 --help 时 reader 线程按 cp936 解码 UTF-8 失败，stdout 变 None（已写入 spec/testing-and-tooling.md）
- [WARN] bash 管道统计 \cite 键数（sort -u | wc -l）在 CRLF 文件上会虚高（128 vs Python 精确 121），量化结论以 Python 为准

### Status

[OK] **Completed** — just ci 1040 绿（+25 测试）；真实 chapter1.tex 回归：121 唯一键、15 处堆引、近三年 21% 被 B4 命中、表 1-2 五行科学问题全中 L-SCI；4 个功能 commit + 1 个归档 commit

## 2026-07-12: latex-thesis-zh 第二章过程分析章优化（07-11-thesis-zh-process-chapter）

### 关键决策

- P-FLOW/P-DERIVE/P-FRAME/P-ORDER/P-PAPER 挂 logic 新 flag --process-chapter、F-MD/F-NOTE 挂 format 现有 CHINESE_CHECKS，默认行为只有 R2 章引言编号形态 bug-fix
- “第X章”显式章号映射定 Info 推荐加强项（用户决策）：9 子代理精读证实 5/5 范文框架节均不写章号（映射独占绪论组织结构节），不可升 Major
- 第二章引言 5/5 为“本章概述式”不承接前章，承上启下检查从第 3 章起适用；编号“2.1 引言”与章后导语 4:1，R2 两形态均适配
- 本轮只做技能能力建设、不对用户论文出诊断（用户决策）

### 教训

- [WARN] 检查器适配新结构形态要跑完整输出回归：R2 修完 _check_chapter_intro，S1 _check_heading_leads 对同一编号引言章仍误报“未发现导语段落”，追加 _has_numbered_intro_section 豁免（已写入 spec/testing-and-tooling.md）
- [WARN] ref/thesis 加密 PDF：pikepdf 解密后 Read 工具仍拒读，改走 PyMuPDF 抽全文 .txt 带页码标记再派子代理；解密副本只留 ref/（已 gitignore）绝不入库
- [WARN] 子代理带回超范围 pyproject.toml version bump（5.3.0→5.4.0）+ uv.lock 波动，git checkout 还原；version 全仓同步不随单 skill 任务动

### Status

[OK] **Completed** — just ci 1072 绿（+32 测试）；5 个功能 commit + 新指南 process-chapter-guide-zh.md（245 行）；关键证据升级：框架节不写章号 3/5→5/5
