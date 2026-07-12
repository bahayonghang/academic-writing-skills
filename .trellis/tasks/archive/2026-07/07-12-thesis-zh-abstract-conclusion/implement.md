# Implement: latex-thesis-zh 摘要与结论章节优化

执行顺序按依赖排列；每步含验证命令与回滚点。约定：每完成一个 Step 提交一次（scoped conventional commit），回滚粒度=单提交 revert。

## Step 0 摸底基线 `[验证前置]`

- [ ] `just ci` 确认起点全绿，记录测试数
- [ ] `grep -rn "analyze_abstract" tests/` 列出受 D1 默认值影响的既有用例清单，写入本文件附注

验证：ci 绿；清单落地。
回滚点：无改动。

## Step 1 摘要 thesis 模式（design D1；PRD R1）

- [ ] `analyze_abstract.py`：新增 `ThesisAbstractAnalyzer`（T-OPEN/T-PAIN/T-LEAD/T-ENUM/T-PROB/T-VERIFY/T-VERB/T-ABBR/T-NUM-HEDGE/T-KW-FIRST/T-INNOV/T-TOC-STYLE/T-VOICE），CLI 加 `--model {thesis,five}`（默认 thesis）、`--degree {doctor,master}`（默认 doctor）
- [ ] 字数阈值常量对齐 check_spec 燕山值（900,1200）/（500,650），注释标注来源；`--max-chars` 覆盖逻辑保留
- [ ] 每个检查 ID 在代码注释标注 research 溯源（★A1 等）
- [ ] 新增 `tests/skills/latex_thesis_zh/test_abstract_thesis_mode.py`：T-* 正反例、常量一致性锁、`--model five` 回退
- [ ] 更新 Step 0 清单中受默认值影响的既有用例

验证：`uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/ -x` 绿；手工冒烟 `uv run python -B academic-writing-skills/latex-thesis-zh/scripts/analyze_abstract.py <fixture>.tex` 输出含 thesis 模式报告。
回滚点：revert 本步提交即恢复五要素默认。

## Step 2 中英摘要一致性（design D3；PRD R2）

- [ ] `analyze_abstract.py`：`_extract_english_abstract` + `--bilingual`（B-ORD/B-NUM/B-ENUM/B-LEN [Script]；B-SEM 输出 LLM lane 提示）；报告尾注指路 deai 时态检测，**不实现时态**
- [ ] test_abstract_thesis_mode.py 补 B-* 正反例（含无英文摘要、数值不一致、序词错位）

验证：pytest 同上；冒烟 `--bilingual --json` 结构完整。
回滚点：revert 本步提交，Step 1 成果不受影响。

## Step 3 结论内容检查器（design D2；PRD R4）

- [ ] 新建 `scripts/analyze_conclusion.py`：CC-TRIAD/CC-OPEN/CC-ENUM/CC-OUTLOOK-EMPTY/CC-OUTLOOK-TRANS/CC-OUTLOOK-COUNT/CC-VERBATIM/CC-QUANT/CC-NO-FIG/CC-RATIO/CC-SUBSEC [Script] 项 + CC-SKELETON/CC-NEW-CONCEPT 的 LLM lane 输出；`--json` 支持；复用 parsers.split_sections/tex_loader.assemble/extract_abstract，**不改 parsers.py**
- [ ] 展望空话黑名单落为脚本内词表或数据文件（对齐 deai 词表维护约定），黑名单命中需同句无具体技术名词才报
- [ ] 报告尾注指路 spec-check（cite/字数/模糊措辞）与 over-claim-guard，零重复报告
- [ ] 每个检查 ID 注释标注溯源（C-* / web C*）
- [ ] 新建 `tests/skills/latex_thesis_zh/test_analyze_conclusion.py`：各 [Script] 项正反例 + 多文件 include 场景 + CC-VERBATIM 阈值边界例

验证：pytest 绿；冒烟跑一篇含"总结与展望"的 fixture。
回滚点：新文件 + 新测试，revert 即净移除。

## Step 4 写作指南与模块文档（design D4；PRD R3/R5）

- [ ] 新建 `references/writing/conclusion-guide-zh.md`（体例对齐 introduction-guide-zh.md；含 checker 映射表与分级说明）
- [ ] `references/writing/abstract-structure.md` 追加学位论文骨架节
- [ ] 新建 `references/modules/conclusion.md`；更新 `references/modules/abstract.md`
- [ ] `thesis-writing-guide.md` §摘要/创新点/总结改指路；`blind-review.md` 加规范性维度联动一行
- [ ] SKILL.md：路由表加 conclusion 模块与触发词（结论/总结与展望/展望/结论章），更新 abstract 模块描述与 `last_updated`（version 不动）

验证：`just ci`（含 SKILL.md 契约测试 ROUTER_ROW_RE / 字符串锁）；grep 确认路由行格式未被 hook 重排。
回滚点：纯文档提交，revert 无副作用。

## Step 5 全量质检与收尾（PRD R6）

- [ ] `just ci` 全绿（lint + pyright error 数 + 全部测试），对比 Step 0 基线测试数只增不减
- [ ] 溯源抽查：每条新检查规则可从代码/指南回溯到 research/ 编号条目
- [ ] trellis-check 全范围检查（拼接表述默认全章检查约定）
- [ ] 更新 `.trellis/spec/academic-writing-skills/` 相关规范（若有新约定沉淀，走 trellis-update-spec）

验证：ci 输出粘贴到任务 journal；验收标准逐条勾选 prd.md。

## Review Gates

1. **Gate A（Step 1 后）**：thesis 模式默认值切换的既有用例改动 diff 人工过目——确认没有为迁就新默认而弱化断言。
2. **Gate B（Step 3 后）**：CC-VERBATIM/CC-QUANT 阈值与误报率用 ref/thesis 五篇真实摘要+结论抽样验证一轮。
3. **Gate C（Step 5）**：与 check_spec/deai/analyze_logic 的边界零重复终审。

## 附注

- 禁改清单：parsers.py、check_spec.py 既有规则、tests/contracts 哈希锁、justfile/构建配置（授权边界）、SKILL.md version。
- evals.json 如需改动走 Bash python 写入（格式化 hook 陷阱）。
- Windows 重定向 JSON 输出记得 `PYTHONIOENCODING=utf-8`（勿全局 export）。
