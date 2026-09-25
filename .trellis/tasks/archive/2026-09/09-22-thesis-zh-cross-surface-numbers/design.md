# C4 设计

## 1. Files / signature
只改skill=academic-writing-skills/latex-thesis-zh下 scripts/analyze_experiment.py；
references/modules/experiment.md、routing-rules.md、references/writing/results-analysis-guide-zh.md、
SKILL.md与父design公共文档面。
新增 tests/skills/latex_thesis_zh/test_cross_surface_numbers.py、
skill/evals/fixtures/cross-surface/；
扩展 .trellis/spec/academic-writing-skills/results-analysis-checker-contract.md；
SMOKE_COMMANDS在tests/skills/latex_thesis_zh/test_latex_thesis_zh_coverage.py。

analyze_experiment.py INPUT --cross-surface [--section KEY] [--cross-surface-terms FILE]
--cross-surface-terms仅配合本模式。普通和--results-analysis独立；同时传两个分析开关则分别运行并串接输出，
不得让新字典改变旧RA词表或默认报告。新配置是JSON：{"metrics":["合成指标"],"eval_sets":["合成评价集"]}；
显式字段替换新功能自己的默认列表，未提供字段保留默认；空数组有明确空覆盖语义。
不添加新依赖或YAML回退；误格式显式报错。

## 2. Extraction (AC1–AC2)
复用assemble及parser.chapter_ranges；chapter内用标题识别“小结/本章小结”范围，
段落保留raw引用与可见文本两种局部视图；不可用RA清洗后已抹引用的文本重建绑定。
表格只支持table/table*中的简单tabular，以及独立longtable；剥离caption/label/规则行，
以顶层&和\\切格，支持数值内\,。多层multicolumn/multirow/宏封装、未知表头跨列
整体列入未覆盖，不局部猜列后报一致。
记录为函数局部字典，存原文件行号、表label、行标签、列表头与数值，不建立公共IR。

数量用Decimal解析；去除数值内显式分组\,、空格，保留负号与小数。
百分号规范化为相同百分单位，但92.1%不转换成0.921；区间比较有序两端，
不把两个端点拆成任意值集合。单位仅明确字面一致，禁止自动比例或量纲换算。
科学计数可作同一Decimal显示值，但缺unit/区间口径仍不比较。

## 3. Unique binding / mismatch (AC1–AC2)
内部比较键=(chapter, table label, metric header, method/object row label, eval set, unit)。
表头指标名需在新词表内；方法/对象直接取明确行标签。
评价集必须在表caption/header或同句明示，且正文/小结显式匹配该名称；
不从“同章”推断评价集相同。无单位指标仅在表头/正文明确“无量纲”或同一明确%时可绑定，
不因没写单位假定单位相同。复合量纲不能识别时NEEDS-LLM。

正文/小结同句需有唯一\ref{tab:*}、显式指标、行标签、评价集与可识别单位；
不从段落附近距离猜测归属。范围相同且各分量唯一才比较Decimal值。
小结无引用但数值相同仍是未绑定，不能因同值跳过。
按正文/小结已明确提及的键的并集建立“关键结果集合”；表中未在叙述提及的其他数值
不强制重复书写。对集合每键检查table/body/summary存在性与唯一终值：
- body与table不同→RA-XS-BODY；
- summary与table不同或已明确绑定表中无该记录→RA-XS-SUMMARY；
- 缺body或summary→RA-XS-MISSING，报告缺的表面；
- 无法绑定、冲突多值或未覆盖语法→NEEDS-LLM覆盖说明，不产出差异判定。
新模式即使没有finding，也显示已比较键数/未覆盖数和“非全文合规证明”。
不选新模式时不显示这些统计。所有候选Info/P3，不把数差大小作为严重度依据。

## 4. Other cues (AC3)
RA-XS-EVALSET：同一明确table引用与同对象同指标的记录分别明确使用两个不同eval_sets词，
只提示口径混用；“不使用A而使用B”等否定对照不给两个肯定绑定。
RA-XS-METRIC：肯定句中“由A可得B/A换算为B”且A/B是两个不同metric词，定位人工复核；
“不能由A可得B”不报。不同指标名不进入数值相等比较。
不声明同一表只能含一个评价集；比较须同时满足对象/指标绑定。

## 5. Verification matrix / documents (AC4)
| 用例 | 预期 |
| --- | --- |
| 简单表，明确ref+方法+指标+评价集+单位三处一致 | 比较键数1、差异0 |
| table92.3%，body92.1%，summary92.3% | 只报body差异 |
| 表另一个指标92.1%，目标仍92.3% | 差异不被同数抵消 |
| 缺summary/body或绑定表无对应行 | 对应缺面/缺记录候选 |
| 两表候选、不同单位、无评价集、无对象 | NEEDS-LLM，比较键数0 |
| \,、负号、区间、科学计数 | 规范化但不单位换算 |
| multirow/宏、无表/无小结、include多章 | 覆盖说明、章隔离、源位置正确 |
| eval词表覆盖与非法JSON、互推否定句 | 生效/报错/零误报 |

人工指南保持三表面全量核读的目标；脚本只是窄支持子集，不声称覆盖所有自然语言。
默认/旧RA基线与组合开关测试证明独立；父design质量门禁。
回滚该脚本和配套资源差异，其他子脚本不受影响。
