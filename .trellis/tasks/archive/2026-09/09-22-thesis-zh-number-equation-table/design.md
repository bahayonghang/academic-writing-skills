# C2 设计

## 1. Change list / ownership
skill根=academic-writing-skills/latex-thesis-zh。
脚本：scripts/check_style_zh.py、check_format.py、check_tables.py、check_references.py。
公开资源：references/formatting/formula-guide.md、number-unit-guide-zh.md、caption-guide.md、
table-guide.md；references/modules/expression.md、format.md、tables.md、references.md、routing-rules.md。
SKILL和公开入口、双语镜像、manifest/evals按父 design §3。
新增 tests/skills/latex_thesis_zh/test_number_equation_table.py；扩展 test_check_style_zh.py、
test_polish_unit_zh.py、test_latex_thesis_zh_coverage.py；合成 fixture 在 skill/evals/fixtures/number-equation-table/。
实施时新增 .trellis/spec/academic-writing-skills/numeric-equation-table-contract.md。
旧学校模板无写权限；check_spec.py由C5负责。

## 2. Mode and scanning boundary
四入口新增可选school参数；在各脚本既有入口判断一次，不构造新配置系统。
已有各 checker 的输出结构不强行统一；新增候选字段/说明携带 Info/P3 与 NEEDS-LLM。
旧调用保持原路径；style 新模式的数字分组/单位只用候选，不输出改写数学内容。
脚本已有 assemble/iter_files 和 origin 继续复用，raw扫描不能用extract_visible_text抹掉公式后再检公式。
屏蔽注释、代码、宏定义和路径载荷；Math仅做源码格式观察，禁止更改或提议改数学事实。
未知宏展开、unbalanced环境输出覆盖不足，不作为PASS。

## 3. Number mechanisms (AC2)
按数值token→显式单位→局部上下文处理。学院模式识别 %、\%、℃、\mathrm{...} 及既有单位集；
表头单独单位、降幅/\%、百分点不是数字后单位，不发间隔问题。
数值后有半角空格、~、\,、\ 等显式间隔视为已有空白；指南推荐~，不把已有其他合法间隔
判成学院违规。平面角 °/′/″ 不要求间隔；不能把℃与角度一并豁免。
数学中的数值单位单独扫描原始span，只报告位置。
千分空从小数点向外每3位分组，整数左端/小数右端可不足3位；
1\,004.1和0.174\,6符合，0.17\,46是候选。负号不计位数。
只有明确数量语境或支持的数值表格列作候选；年份+年、时刻、DOI/路径、科学计数、
带字母型号、编号/学号标签和TikZ坐标跳过；未分类裸数字给覆盖说明，不宣称学院豁免。
支持中文/ASCII语境的限定测试，不扩建类型分类器。

## 4. Equations (AC3)
check_format在原始装配文本识别equation/align及其aligned/split子环境，区分编号与星号。
EQ-LEADIN只对独立编号展示块前紧邻可见正文句判末冒号，不把label/comment当引导句；
与正文同行、宏封装或难以绑定者留人工。
EQ-TAILPUNCT检查公式最后数学token后的中文句号/逗号，不误认cases条件分隔符。
EQ-CONT只对明确单条长等式延续行起始的重复关系/运算符定位；
多行独立左值定义、cases、约束行不报。无法区分推导链和延续时NEEDS-LLM覆盖说明。
合成完整单等式探针 A &= B + C \\ &= D；
合规续行 A = B + C = \\ D；不评价等式数学真伪。
EQ-CITE定位可见正文“上式/下式”；EQ-NOTE只对明确“式中/其中”解释段按源码约定判间隔/破折号，
顶格和破折号视觉对齐仍人工。禁把注释“其中”算正文。
所有5码各自正反例；不靠仅一个EQ-CONT用例证明整族。

## 5. Tables / captions (AC4)
复用各脚本现有caption花括号扫描，在现有函数局部扩展；支持普通caption与bicaption主中文参数，
保留嵌套宏/引用载荷；可选短题注和第二英文参数不参加中文标点检查。
只检查中文题注的可见正文，代码/数学/引用键中的标点不算；无法确认中文主参数则人工核读。
表身TB-SAMEAS排除题注/表注；TB-UNITHEAD要求简单tabular同列至少3个数值行
字面单位相同，且表头无该单位，作为迁移表头的候选，不换算单位。
multicolumn/multirow/嵌套表造成列归属不明时不自动合并；输出未覆盖说明。
表身空白和破折号不能推断测量事实，仅在table-guide保留人工核读语义。

## 6. Validation / rollback
AC1→§2；AC2→§3；AC3→§4；AC4→§5；AC5→文件边界和父design§4。
测试必须断言学院模式与generic对同一合成输入有预期差异；旧四模板文件hash/差异为空。
显式覆盖数学内%、℃、角度、分组方向、注释伪命中、include定位、双语题注。
style哈希更新本子已授权条目，不刷新冻结表其他值。
回退C2局部差异保留C1；C3接手references后按逆序回退，不整文件还原。
