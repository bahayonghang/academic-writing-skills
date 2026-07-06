# typst deai/时态检查与 EN 副本同步

## Goal

把 latex-paper-en 侧已修复但未同步到 typst-paper 的 deai/时态检查行为搬齐，消除两副本无意漂移，并补齐 typst 专项测试与 evals/文档。

证据详情：`../07-05-skills-deep-analysis-optimization/research/en-typst-findings.md`

## 问题清单

- **XA-1 [medium]** `typst-paper/scripts/deai_check.py:602` 附近 low_information_density 在 visible text 上查 `EVIDENCE_MARKERS`，而 typst `extract_visible_text` 剥掉 `@cite`/`#cite()`，引用密集但无内联数字的相关工作段被误报。EN 副本同处已修（:479-480，E17：在 raw_text 上查证据标记），typst 未同步。已实测复现：同段内容 LaTeX 不报、Typst 报。
- **XA-2 [low]** typst 时态检测的图表假阳性护栏失效：`@fig-loss` 被剥掉后 "`@fig-loss` shows ..." 被误判时态；LaTeX 侧 "Figure~\ref{}" 的 "Figure" 字面保留所以 EN 正常。
- **XA-3 [low]** term 列表漂移：EN 检查 remarkable/obvious 等词，typst 缺失。
- **SH-1 [low-med]** `\bpresents?\b` 误伤形容词用法 "the present study"（en 与 typst 共有）。
- **TST-1 [medium]** `tests/test_deai_tense.py` / `test_deai_overclaim.py` 只导入 EN 副本，typst deai/时态零测试——XA-1/XA-2 漂移因此未被发现。
- **DOC-1 / EVAL-1 [low]** en/typst 的文档与 evals 未覆盖新增 checker。

## Requirements

- R1 XA-1：把 EN 的 raw_text 证据检查逻辑同步到 typst 副本。
- R2 XA-2：typst 时态检查在剥引用前的 raw 行上做图表护栏判断（或等效方案）。
- R3 XA-3：对齐 en/typst 的 term 列表（以 EN 为准）。
- R4 SH-1：修 `presents?` 正则误伤（en、typst 两侧同改，保持一致）。
- R5 新增 typst deai/时态专项测试；**用 importlib 按路径加载 typst 副本**，不得 bare import。
- R6 en/typst 的 evals 与 references 文档补登新 checker（就近最小改动）。

## Acceptance Criteria

- [ ] 复现用例（引用密集段）在 typst 下不再误报 low_information_density（新测试断言）。
- [ ] "`@fig-loss` shows" 类句子不再被误判时态。
- [ ] "the present study" 不触发 SH-1 命中；动词 "presents" 仍命中（en+typst 双侧断言）。
- [ ] typst 副本有独立测试文件且通过 importlib 加载，`just ci` 全绿。

## Notes

- 与 `07-05-zh-abstract-tense-gating` 无硬依赖，可并行。
- 完成后 `07-05-deai-alignment-lock` 才能上锁（先修齐再锁）。
- 只改 last_updated，不 bump version。
