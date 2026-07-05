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
