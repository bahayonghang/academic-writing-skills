# zh 英文摘要时态门控修复

## Goal

修复 latex-thesis-zh 新增时态检测（commit 3a8e3c2）的英文摘要区域门控在主流学位论文模板上静默失效的问题，并补齐 zh 侧专项测试与文档。

证据详情：`../07-05-skills-deep-analysis-optimization/research/zh-findings.md`

## 问题清单

- **ZH-1 [high]** `latex-thesis-zh/scripts/deai_check.py` `_english_abstract_range()`（约 :774-791）只匹配明文 `\begin{abstract}` 与英文 `Abstract` 标题章节：
  - thuthesis：`\begin{abstract}` 是**中文**摘要，英文摘要在 `abstract*` 环境——正则 `\\begin\{abstract\}` 不匹配 `abstract*`，英文摘要漏检；时态检查实际跑在中文摘要区间（被 `_is_english_line` 过滤后近似 no-op）。
  - pkuthss：英文摘要环境是 `eabstract`，完全不被识别。
  - 代码注释（:378 附近）与 YAML（:89）把 thuthesis 中文摘要错写成 `cabstract`（`cabstract` 实为 pkuthss 环境）。
- **ZH-2 [medium]** 同函数只取首个 `\begin{abstract}`：中文在前、英文在后的双 abstract 布局下英文摘要漏检（已实测复现）。
- **ZH-3 [medium]** `tests/test_deai_tense.py` 只测 EN 副本 `AITraceChecker`；zh 版 `_check_tense`/`_english_abstract_range` 零覆盖，全仓无摘要环境 fixture。
- **ZH-4 [low-med]** 时态检查器在 zh 的 `deai.md`/`guide.md`/`SKILL.md` 中无记载，`tense-guide-zh.md` 成孤儿文档。

## Requirements

- R1 `_english_abstract_range` 识别 generic `abstract`、thuthesis `abstract*`、pkuthss `eabstract`，并正确跳过中文摘要环境（thuthesis `abstract`、pkuthss `cabstract`）。
- R2 多摘要环境时选择英文摘要（而非首个匹配）。
- R3 修正错误注释/YAML 中的模板-环境映射。
- R4 新增 zh 专项测试：generic / thuthesis / pkuthss / 中文前英文后双摘要 四类 fixture；**必须用 importlib 按路径加载 zh 副本**，不得 bare `import deai_check`（会解析到 EN 副本）。
- R5 在 zh 的 SKILL.md 工作流与 references 中登记时态检查器，链接 `tense-guide-zh.md`。

## Acceptance Criteria

- [ ] thuthesis `abstract*` 与 pkuthss `eabstract` 中的时态信号词被检出（新测试断言）。
- [ ] thuthesis 中文 `abstract` 环境不产生时态 trace。
- [ ] 双摘要布局（中文前英文后）英文摘要被检出。
- [ ] 新测试通过 importlib 路径加载 zh 副本，`just ci` 全绿。
- [ ] `tense-guide-zh.md` 至少被 SKILL.md 或 deai.md 引用一次。

## Notes

- 不修改 `\cite{}`/`\ref{}`/`\label{}`/math 内容（红线）。
- 只改 last_updated，不 bump SKILL.md version（全仓同步约定）。
- ZH-5（繁体变体不检测）为已知局限，本任务不处理。
