# 写作规则分级与因果门禁治理

父任务：`.trellis/tasks/08-25-thesis-zh-quality-closure`
证据源：父任务 `research/evidence-audit.md`（V7、V8）

## Goal

给通用写作规则加适用条件与优先级（手册 P1-1），并把因果资格从「实验类型标签」
改为「区分性证据判断」（手册 P1-2）。

两个后果导向的问题：
- 工学博士章节可能被压成模板化文章，或被要求补做超出当前证据范围的实验
- 不等预算的设置级比较可能被升级为单组件净效应，强措辞与真实实验协议不匹配

## Scope

**改**：`academic-writing-skills/latex-thesis-zh/references/writing/writing-philosophy-zh.md`、
`academic-writing-skills/latex-thesis-zh/references/writing/over-claim-guard.md`、
`academic-writing-skills/latex-thesis-zh/references/writing/results-analysis-guide-zh.md`、
`academic-writing-skills/latex-thesis-zh/references/writing/academic-style-zh.md`；
`scripts/analyze_experiment.py` 的 RA-* 判据（若需要）；
`tests/skills/latex_thesis_zh/`；`docs/` 镜像 + manifest。

**不改**：deai 词表与 `tone-thresholds.yaml` 的既有判定项；IR / mode / artifacts
实现。

## Requirements

- R1：规则分级（V7）。
  `academic-writing-skills/latex-thesis-zh/references/writing/writing-philosophy-zh.md`
  分章节指南表把篇幅写成无条件要求。每条规则增加 `level`（must / should / may）、
  `applies_when`、`exceptions`、`authority`、`counterexample`。稳定原则与样例偏好
  分开。项目规范（学校模板）优先于通用建议。工学实验的硬件/统计项改为 `may` 并带
  `applies_when`，与
  `academic-writing-skills/latex-thesis-zh/references/writing/method-chapter-guide-zh.md`
  防误报红线 12 条一致。

- R2：跨文件套语张力按当前 analyzer 复现后再裁决，不把未入表短语写成已验证
  直接冲突（TPR-12）。已核实事实：精确短语「基于上述分析」不在
  `academic-writing-skills/latex-thesis-zh/references/deai/tone-thresholds.yaml`
  的 `throat_clearing.patterns` 中；`deai_check.py` 对命中的 throat-clearing
  pattern 逐段产生一条 finding，没有名为 throat-clearing=2 的阈值。
  `burstiness.consecutive_paragraphs` 现值为 3，与 throat-clearing 是不同合同。
  本任务第一步用最小 fixture 跑当前 analyzer，记录真实输出，再决定改指南示例、
  加 `applies_when`，或只消除读者可察的语义张力。不改 deai 词表与阈值文件字节。

- R3：因果门禁（V8）。为
  `academic-writing-skills/latex-thesis-zh/references/writing/over-claim-guard.md`
  增加 `single_changed_factor`、`budget_comparable`、`replication`、
  `alternative_explanations`、`estimand`。不满足时只允许「当前设置级关联 / 记录」
  表述。保留「消融实验 / 消融设置」称谓。

- R4：证据阶梯单一 owner。`results-analysis-guide-zh.md` 与
  `over-claim-guard.md` 去重：一个 canonical definition，另一处只链接。归属按
  `academic-writing-skills/latex-thesis-zh/references/modules/routing-rules.md`
  既有边界：结果分析的事实组织归 `--results-analysis`；论断强度与证据阶梯的语义
  裁决读 over-claim-guard。

- R5：docs manifest、SKILL.md `version` 保持 `6.0.0`、相关对齐测试、
  `just ci` 与 `just doc-build` 通过。

## Acceptance Criteria

- [ ] AC1（R1）：同一规则在适用与不适用 fixture 上分别触发 / 静默，且输出说明
      `authority`
- [ ] AC2（R1）：不具备多随机种子或 GPU 报告需求的既有工学实验不被自动报 Major
- [ ] AC3（R1）：分级结果与 method-chapter-guide 防误报红线 12 条无冲突，逐条
      记录在 design.md
- [ ] AC4（R2）：最小 fixture 复现记录写入 design.md；精确短语「基于上述分析」
      的真实 finding 集合以该记录为准。写作指南侧完成裁决后，读者可察的「一边
      推荐一边禁止同族套语」张力消除。deai 词表与 `tone-thresholds.yaml` 字节
      不变。不把 throat-clearing=2 当作锁点
- [ ] AC5（R3）：保留「消融实验 / 消融设置」术语；不重命名
- [ ] AC6（R3）：不等预算的 A1-A6 消融记录不得推导单组件净效应；「证明」类因果
      动词被阻断
- [ ] AC7（R3）：缺失的区分性证据被明确列出；claim strength 不越级
- [ ] AC8（R4）：证据阶梯只有一个 canonical definition；重复定义搜索清零，
      结果记入 design.md
- [ ] AC9（R5）：改 references 后在本提交内重建 manifest + 双语页面；SKILL.md
      只改 `last_updated`；`just ci` 全绿；`just doc-build` 成功
- [ ] AC10（R1）：规则分级对真实论文的误报率变化标 **missing evidence**

## Constraints

- 不改 deai 词表与阈值文件字节：
  `academic-writing-skills/latex-thesis-zh/references/deai/tone-terms-zh.md`、
  `tone-thresholds.yaml`、`deai/guide.md`。burstiness 的
  `consecutive_paragraphs=3` / `opening_token_count=4` 与 throat-clearing
  pattern 列表是不同合同，本任务都不改
- 不重命名任何实验术语
- 不移植 throat-clearing 到其他 skill
- 不改构建配置；不修改用户论文
- `tests/contracts/test_writing_modules_alignment.py` 的 `TIER1_HASH_GROUPS`
  只锁脚本；目标 `references/writing/*.md` 不在其中。若改动波及
  `analyze_experiment.py` 之外的脚本，须先确认是否落入该表
- `tests/contracts/test_polish_contract_alignment.py` 锁两条：
  ① `references/modules/expression.md` 必须含指向 `../writing/over-claim-guard.md`
  的指针与 `NEEDS-LLM`；② over-claim-guard 不得出现在 SKILL.md 的
  `## Reference Map` 节
- `tests/skills/latex_thesis_zh/test_results_analysis.py` 断言
  `results-analysis-guide-zh.md` 的存在与内容；R4 去重时须同步该测试
- 格式化/回滚/提交遵循父任务 dirt 冻结清单与 Phase 3.4

## Dependencies

依赖子任务 1（`08-25-thesis-zh-visible-prose-ir`）仅在提交顺序上（manifest 单写者），
规则内容不依赖 IR。与子任务 2-4 无内容依赖，可并行规划、串行提交。

## 修订记录

- 2026-08-25 审阅返回：TPR-01 R/AC ID；TPR-12 补核精确短语零 deai finding，
  裁决改指南侧；分开 pattern / burstiness / 触发计数。
