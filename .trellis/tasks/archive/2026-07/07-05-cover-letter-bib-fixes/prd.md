# cover-letter 与 bib-search 修复

## Goal

修复 cover-letter align-check 的数值指标"张冠李戴"泄漏与 bib-search-citation 的重复键静默问题，并补齐对应测试盲区。

证据详情：`../07-05-skills-deep-analysis-optimization/research/bib-cover-findings.md`

## 问题清单

- **CL-1 [medium，红线相邻]** `cover-letter/scripts/verify_letter_against_manuscript.py:57-100` `_has_numeric_match`：稿件只有 "3% accuracy improvement"，信里写 "3% throughput improvement" 仍 verified=True 且不产生 finding。根因：邻近窗口只要求 claim 的任意指标关键词与数字共现，不校验紧贴数字的具体指标词身份是否一致（已实测复现）。
- **BIB-1 [medium]** `bib-search-citation/scripts/search_bib.py:777-857` 重复引用键被静默当两条独立结果返回并导出相同 `\cite{}`，无 duplicate_key warning——重复 key 在真实编译中是错误。
- **BIB-2 [low]** `%` 行注释掉的条目仍被解析为有效条目（与原生 BibTeX 语义一致但违反 JabRef 用户直觉，已禁用条目可能重现）。
- **CL-2 [low]** 句子切分把 "Dear Editor," 粘进首个 claim 句，仅膨胀 quote，不影响检测。
- **测试盲区**：无重复 key / `%` 注释条目测试；无"同数字异指标"泄漏测试（现有 C4 测试只覆盖数字与关键词相距过远的情形）。

## Requirements

- R1 CL-1：`_has_numeric_match` 校验数字邻近窗口内的指标词与 claim 中紧贴该数字的指标词一致（而非任意关键词共现）；不一致时降为 unverified 并产生 finding。
- R2 BIB-1：检测到重复键时对每条命中附 duplicate_key warning（不静默去重，保留用户决策权）。
- R3 BIB-2：为 `%` 注释行内的条目加提示性 warning 或跳过（选择方案时在 design 里写明取舍，默认倾向 warning 保持解析语义不变）。
- R4 CL-2：切分时剥离称呼行。
- R5 补测试：同数字异指标泄漏用例、重复 key 用例、`%` 注释条目用例。

## Acceptance Criteria

- [ ] "3% throughput improvement" vs 稿件 "3% accuracy improvement" → unverified + finding（新测试断言）。
- [ ] 既有的距离过远（C4）用例行为不回归。
- [ ] 重复 key 的 .bib 搜索结果携带 duplicate_key warning。
- [ ] `just ci` 全绿；cover-letter 测试继续用 importlib 加载（不遮蔽 canonical parsers）。

## Notes

- 红线：不捏造 bibliography 条目/作者/venue；align-check 修复方向是"更严"，不引入自动改写。
- CL-3/CL-4（enhancement）在 `07-05-cover-letter-deai-enhancement` 处理。
