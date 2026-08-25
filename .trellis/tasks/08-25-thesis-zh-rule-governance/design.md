# 设计：写作规则分级与因果门禁治理

## 改造前基线

`writing-philosophy-zh.md` 把篇幅与实验清单写成无条件要求。
`over-claim-guard.md` 用实验类型标签授予因果动词。

跨文件套语：`writing-philosophy-zh.md` 示例「基于上述分析，本文提出…」，
`academic-style-zh.md` 把「基于上述分析」列入因果连接词。
`tone-thresholds.yaml` 的 `throat_clearing.patterns` **不含**该精确短语。
`deai_check.py` `_check_throat_clearing` 对命中 pattern 逐段一条 finding，
没有 throat-clearing=2 阈值。burstiness 是另一合同
（`consecutive_paragraphs=3`）。父任务 evidence-audit 已写明这是同族推导，
不是已复现的双重判定（TPR-12）。

## 变更清单

| 文件 | 变更 |
| --- | --- |
| `academic-writing-skills/latex-thesis-zh/references/writing/writing-philosophy-zh.md` | 分级字段 + 示例裁决 |
| `academic-writing-skills/latex-thesis-zh/references/writing/academic-style-zh.md` | 与 philosophy 示例对齐 |
| `academic-writing-skills/latex-thesis-zh/references/writing/over-claim-guard.md` | 区分性证据门禁；canonical 证据阶梯 |
| `academic-writing-skills/latex-thesis-zh/references/writing/results-analysis-guide-zh.md` | 删除重复阶梯，改为链接 |
| `academic-writing-skills/latex-thesis-zh/scripts/analyze_experiment.py` | 仅当 RA-* 必须随门禁改判据时 |
| `tests/skills/latex_thesis_zh/test_rule_governance.py` | 新增 |
| docs 镜像 + manifest | 本提交内重建 |

不改：`tone-thresholds.yaml`、`tone-terms-zh.md`、`deai/guide.md` 字节。

## R2 复现后再裁决

S1 用最小 fixture（正文仅一段「基于上述分析，本文提出一种方法。」）跑当前
`deai_check.py`，把 stdout 写入本文件「复现记录」节。

裁决规则：

- 若零 throat-clearing finding：冲突只存在于指南示例 vs 同族套语观感。改
  philosophy / academic-style 的示例或加 `applies_when`（例如「段首连续使用
  同族套语时不推荐」），不改 deai 表。
- 若其它 checker 命中（如 term_threshold「提出」等）：记录实际 rule_id，不把它
  写成 throat-clearing 冲突。
- 禁止把 burstiness 阈值或虚构的 throat-clearing=2 写入锁或测试。

三个分开描述的合同：

| 合同 | 现状 | 本任务 |
| --- | --- | --- |
| throat-clearing patterns | yaml 正则列表，逐段命中一条 | 字节不变 |
| burstiness | consecutive_paragraphs=3, opening_token_count=4 | 字节不变 |
| 指南示例 | 推荐「基于上述分析」 | 按复现结果改指南侧 |

## 规则分级

每条指南增加：`level` `applies_when` `exceptions` `authority` `counterexample`。
学校模板 > 通用 must > should > may。工学硬件/统计项为 may，且
`applies_when` 排除无多随机种子/GPU 需求的既有工业实验。

design 定稿时把 method-chapter-guide 防误报红线 12 条逐条映射到分级结果，
写入本节附录（实现时补表，不得与红线互斥）。

## 因果门禁

在 over-claim-guard 增加五项门禁。任一为假则禁止「证明」类因果动词，只允许
设置级关联/记录，并列出缺失证据。不重命名「消融实验 / 消融设置」。

证据阶梯 canonical 放 over-claim-guard；results-analysis-guide 只链接。
同步 `test_results_analysis.py` 中对 guide 文件内容的断言。

## 验证边界

自动化：适用/不适用 fixture、GPU Major 不误报、消融不等预算、deai 三文件
字节 diff 为空、重复阶梯搜索。
不自动化：真实论文误报率（missing evidence）。

## 回滚

`git restore` 四份 writing md 与可能改动的 `analyze_experiment.py`。
不 restore deai 文件（本任务不改它们）。

## 已考虑不做

- 把「基于上述分析」补进 throat-clearing 表：违反「不改 deai 词表」。
- 未复现就当直接冲突修：证据不足。
- 把 throat-clearing 阈值写成 2：该合同不存在。

## 复现记录（TPR-12，2026-08-25 规划期补核）

命令（仓库根，`PYTHONIOENCODING=utf-8`）：

```
uv run --extra dev python academic-writing-skills/latex-thesis-zh/scripts/deai_check.py <tmp>/tpr12-throat.tex --analyze
```

fixture 正文：

```
\documentclass{article}
\begin{document}
\chapter{绪论}
基于上述分析，本文提出一种方法。
\end{document}
```

退出码：0。详细痕迹列表为空：无 throat-clearing finding，无 term_threshold，
无其它 traces。

对照：`tone-thresholds.yaml` 的 `throat_clearing.patterns` 不含「基于上述分析」；
burstiness 合同为 `consecutive_paragraphs=3`，本 fixture 只有一段，不触发。

裁决：精确短语与 deai 无双重判定。读者可察张力只存在于
`writing-philosophy-zh.md` / `academic-style-zh.md` 的推荐示例与同族套语观感。
本任务改指南示例或加 `applies_when`（例如「段首连续使用同族套语时不推荐」），
不改 deai 词表与阈值文件。不把 throat-clearing=2 写入测试。
