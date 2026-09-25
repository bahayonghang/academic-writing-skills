# C1 设计

## 1. Files
skill根=academic-writing-skills/latex-thesis-zh。
改 scripts/check_consistency.py、scripts/check_style_zh.py；
references/modules/consistency.md、expression.md、routing-rules.md；
references/writing/academic-style-zh.md；examples/structure-and-consistency.md；SKILL.md。
新增 tests/skills/latex_thesis_zh/test_term_governance.py；
扩展 test_consistency_semantics.py、test_check_style_zh.py、test_polish_unit_zh.py；
合成 fixture 放 skill/evals/fixtures/term-governance/。
实施时新增 .trellis/spec/academic-writing-skills/term-governance-contract.md 并登记索引。
双语镜像/manifest/公开入口/evals 边界沿用父 design §3。

## 2. Governance input (AC1)
采用现有 JSON 文件扩展，无第二份配置：
{"zh":[["合成甲","合成乙"]],"en":[],"banned":{"旧称":{"candidates":[{"text":"候选甲","slot":"过程"},{"text":"候选乙","slot":"对象"}]}},"locked":{"标准名":["旧别名"]},"exempt":{"environments":["localterms"]}}

字段均可缺省；banned 每词至少一条非空候选；slot 可省略；locked 的数组是禁用变体。
exempt 只增加环境名，不能取消固定保护。一次读取/验证于治理入口，不在各检查器重复验证。
显式 --governance 无 --custom-terms 属参数错误。旧 zh/en 加载逻辑不因治理开关改语义。

新路径使用 assemble 的内容和 origin；局部扫描器保留位置，屏蔽注释、前导区、数学、
cite/ref/label载荷、路径、verbatim/lstlisting/minted、thebibliography、用户指定环境。
缩略词表仅对明确的 abbreviation/abbreviations/acronym 环境和标题为“缩略词表/缩略词对照表”的范围豁免，
不能按整个普通 table 豁免。未知自定义宏声明覆盖不完整，不宣称无问题。
不扫描外置 .bib，不把题名带入治理候选。
中文按字面词匹配；ASCII 词使用词边界。每命中一条词位，给词、位置、所有候选和 slot，
而不是按候选数复制 finding。locked 不从词频推导规范名。

## 3. Abbreviation style (AC2)
新模式在受保护片段屏蔽后的装配文本按位置前后顺序查找完整括注，
登记“中文名称 + （英文全称，缩写）”；中英文逗号作为识别输入但报告项目约定的全角形式。
只接受句内可明确界定的名称短语，边界不清只给 NEEDS-LLM 覆盖说明。
缩写支持大小写混合、数字与内部连字符，如合成 ZX/AbX/X-2，不复制论文专名。
同一已登记中文名/缩写对之后出现“中文名（缩写）”或“中文名 缩写”发候选；
首次只有“中文名（缩写）”不能推出已有合格展开，因此不发“二次”结论。
Title Case 只作为完整括注中的候选，不自动改专名大小写；保留作者确认权。
含数学的括注与“X 为中文名”的符号解释不作为 XOR 问题。
与旧 --terms/--abbreviations 合用时去重同位置同类候选，不替换旧定义识别器。
JSON 新结果字段仅新模式出现；旧 report 与 key 集合保持。

## 4. Degree wording (AC3)
ChineseStyleChecker 新增显式模式参数，默认 False。运行旧绝对词检查时仅在新模式按命中跨度
跳过列明合法搭配，不能因句中一处合法搭配跳过整句。
程度词扫描可见中文句子，Info/P3，[Script]，Meaning-Check: NEEDS-LLM；
“完全忽略”已有“完全”候选时保留一个位置的候选，不重复；若从句、证据强弱留给 LLM。
继续沿用原文保护与 section 分流，不新增自动替换模板。

## 5. Verification / traceability (AC4–AC5)
| AC | 正例 | 反例/边界 |
| --- | --- | --- |
| AC1 | 两slot、locked变体、多文件定位 | 数学/cite/bib表/自定义环境；损坏JSON/错误字段 |
| AC2 | 三种问题，主入口跨文件顺序 | 四类豁免；无定义；混合大小写缩写；重复输入 |
| AC3 | 极易、句内第二个绝对 | 合法搭配、旧模式、引用他人观点 |
| AC4 | 文档schema与CLI完全对应 | 不引用私有路径；合成词不含论文注册表 |
| AC5 | 默认文本/JSON/stdout/stderr/exit回归 | style哈希更新；其余冻结不变 |

默认基线按父 design §4；单元测试按路径加载 ZH 并恢复 sys.path/sys.modules。
新功能各有独立 CLI 调用，--help 不作为旧输出基线。
回滚此子源码+测试+资源差异；C2开始后不得直接整文件覆盖 style。
