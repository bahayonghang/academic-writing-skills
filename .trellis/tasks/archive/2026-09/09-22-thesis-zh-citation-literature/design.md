# C3 设计

## 1. Files / signatures
改 skill=academic-writing-skills/latex-thesis-zh 下 scripts/check_references.py、
verify_bib.py、analyze_literature.py。
资源 references/modules/references.md、bibliography.md、literature.md、routing-rules.md；
references/citations/gb-standard.md；新增 references/writing/literature-progression-zh.md。
新增 tests/skills/latex_thesis_zh/test_citation_literature.py；
扩展 test_verify_bib_scanner.py、test_latex_thesis_zh_coverage.py；
fixture=skill/evals/fixtures/citation-literature/。
实施时新增 .trellis/spec/academic-writing-skills/citation-placement-contract.md。
公开入口/SKILL/evals/双语mirror/manifest按父design§3。

check_references的--author-cite与--repeat-cite相互独立，可与C2 --school组合。
verify_bib --college-details 要求 --standard gb7714 或 gb7714-2025；
其他组合参数错误，不猜测学校。该flag不改变既有standard语义。
analyze_literature --progression-density可和--section组合，与--intro-citations互斥。

## 2. Citation collection / author placement (AC1)
在check_references内增加局部位置保留扫描，使用assemble入口顺序和源映射；
保留原引用完整性流程，未选flag时不建新扫描数据。
支持明示 \cite / \citep / \citet / \parencite / \textcite / \autocite 及其星号，
命令与参数允许合法空白、注释、0/1/2个平衡方括号。
对显式textcite/citet的作者位置不重复提示，渲染作者并未出现在源码。
仅以可见句内“姓氏 等/等人”加报告谓词、或清晰作者名+谓词候选定位；
不能推断每个中文2–4字词都是姓名。候选明确“不确定是否作者主语，请核读”。
ASCII句点缩写不粗暴切断引用；不完整句/跨段不猜测绑定。
不匹配“文献[...]”“已有研究”等非姓名主语；紧跟完整作者短语即合规。
附原文件行号、短命中片段与cite key，不输出改写句或修改key。

## 3. Repeat-page semantics (AC2)
每个支持命令的每个key计1次；一个命令中重复key去重计一次。
单可选参数为postnote；双参数第1为prenote、第2为postnote；空白postnote视为空。
完整文档中caption等可见引用也计数，无自动学校豁免；
bibliography数据、注释、宏定义、verbatim、\nocite不计。
同key至少两次且有缺postnote→RC-REPEATPAGE，标出需要人工核验的位置。
多key共享postnote不能证明各key页码分别成立，即使有值也发NEEDS-LLM说明。
非页码自然语言postnote或传统页码未知同样需人工核读，不能只因非空就PASS学校。
支持的字面页码形态包括整数、罗马数字和明确页段；此检查仍不证明页码支持当前句。
\cites等多重命令、自定义宏传key与未展开参数不计为已覆盖；新模式给覆盖不足说明。
不为该边界复制/改造bib_scan，也不新增持久化引用索引。

## 4. Bibliography / progression (AC3–AC4)
college-details在现有entries解析后生成额外info issues，不改变旧校验issue序列。
book/phdthesis/mastersthesis查address或location至少其一；pages缺失给来源核验候选。
inproceedings缺pages也提示学院第101项需核实；article沿用原缺字段结果避免重复。
正常完整个人姓名不做大小写违规判定；有作者数据时最多一条文件级样式说明，
列出核对最终BBL/PDF中姓在前、大写、首字母显示的人工步骤；
不认可“LI G Z”作为原始BibTeX数据的正确性证据，不生成缩写姓名。
无传统页码/文章号仅列待核，不新增猜测页数。

progression使用既有section解析，可见正文排除题注、引用键、数学和代码。
按词的实际出现次数计数，不按行数/句数；严格>5或>7触发，阈值标UNVERIFIED。
命令未指section时只使用已有related范围，找不到时沿用可见错误提示；
不得静默统计全文。不提供YAML覆盖层；需别的阈值另开有证据需求。
六类方向与四种组织放指南，用合成片段演示，不脚本轮换同义词。

## 5. Traceability / compatibility
AC1→§2；AC2→§3；AC3/AC4→§4；AC5→§1及父design§4。
反例必须包括机构作者/重音姓名、biblatex location、文章号、宏参数引用、图题、
多文件顺序、双可选注记、无匹配section。
默认基线覆盖references，verify_bib三种standard，literature普通/intro-citations；
仅新增flag路径变化。与C2 school并用时各候选保留且不双报同一题注。
回滚本子差异保持C2 caption规则；不触碰其他skill副本。
