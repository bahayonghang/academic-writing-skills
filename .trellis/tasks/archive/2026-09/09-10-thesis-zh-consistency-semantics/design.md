# C2 设计

## 数据流和唯一顺序来源
输入入口 → 既有 tex_loader.assemble → 有序文本/行来源 → 定义与使用位置 → 检查结果。
`academic-writing-skills/latex-thesis-zh/scripts/tex_loader.py:171` 的 assemble 与
第 132 行 origin 已提供实际 include 展开和定位。复用它们，不重新实现 include 解析。
“首次”指装配全文的首次有效使用与首次定义，不在每章重置。
逐章重引是允许/建议的写法，不新增“每章必须重新定义”的检查；因此无需新建章状态或
解析标题来判断是否重复定义。不能用文件名排序替代真实阅读顺序。

check_consistency 内部在有主文件时接收该入口（允许增加仅内部的 keyword-only
entry_file 参数，不新增 CLI 选项），只装配一次，在同一表示上收集定义和使用。
原始 list-of-files API/目录/--all-files 模式无入口时分别按文件分析，
报告明确“文件内顺序已检查，跨文件顺序未验证”。不能把文件列表首项猜成主入口。
读取失败或装配缺失信息沿用 loader 可见警告，不以空内容伪造全局覆盖。

## 术语与缩写判定（R1–R3）
- 删除不成立的默认等价配对；复核本次现有 DEFAULT_TERM_GROUPS 中每组，不能补新词典。
- 内置组只能提示可能的用词不一致，不按最高词频给确定性“统一成 X”建议。
  custom-terms 仍表示用户显式分组，但顺序/频次不隐含“首项为规范名”的新合同。
- 全称/缩写的合法切换不因计数超过3而被断言为语义错误；若保留风格提示，
  明确它是可选一致性候选，不能要求全部全称改成缩写。
- 定义只在同一物理行的“全称（缩写）/全称 (缩写)”附近取有界文本，
  不跨换行、句末或结构命令；同一采集函数供 terms/abbreviations 使用。
  提取结果是可见全称候选片段，不声称自动获得唯一规范全称；可靠边界缺失时标注 NEEDS-LLM。
- 内部用字符位置比较定义与使用，避免同一行先用后定义被行号相等掩盖。
  定义括号内缩写不是一次“未定义使用”。
- 每章首次使用允许重新定义；后章也可直接复用全文此前已定义的缩写。
  同章/跨章重复同一明确释义不报冲突。
  不同可见释义只生成可定位候选供 LLM 判断（例如中英文全称可能等价），不硬编码语言别名。
- 无任何定义的缩写继续沿用现有 ABBREV_MIN_USES 与停用词规则；有定义但首用在前
  则报告顺序问题。缺少可靠全称边界时说明需人工核对，不猜完整术语。
- 对外沿用现有结果字典与报告入口，复用既有 issue 分类表达候选和信息；
  不新增配置 schema、评分状态机或兼容迁移。出现的源路径须能区分同名不同目录文件。

## 文件所有权
C2 owner：agent_skill_architect（Python checker）；语义复核由 academic_writing_editor。
其他人可能并行修改仓库，不撤销他人改动。
- academic-writing-skills/latex-thesis-zh/scripts/check_consistency.py
- academic-writing-skills/latex-thesis-zh/references/modules/consistency.md
- docs/skills/latex-thesis-zh/resources/references/modules/consistency.md
- docs/zh/skills/latex-thesis-zh/resources/references/modules/consistency.md
- tests/skills/latex_thesis_zh/test_consistency_semantics.py（新增）
- tests/skills/latex_thesis_zh/test_latex_thesis_zh_checker_precision.py（仅错误的旧术语正例及本次 full_after_abbrev 可选风格语义断言）
- tests/skills/latex_thesis_zh/test_latex_thesis_zh_scripts.py（仅 TestCheckConsistency）
- 本子任务 research/ 证据。
与 C3 共用 scripts 测试文件，C2 完成并交接后 C3 才编辑该文件；不得并发 whole-file 写入。
共享 parser/loader 仅消费，不编辑。manifest 与新增 maintainer spec 由父任务拥有。

## 验收与回滚
AC1→分组/候选规则；AC2→装配全文顺序、位置采集与 origin；
AC3→重复释义合并与不同释义候选；AC4→无入口降级说明；
AC5→调用 shipped ConsistencyChecker/main 的独立预期用例；
AC6→公开边界及父任务资源集成。
默认结果变化属于误报/假绿修复，记录具体旧/新行为，不宣称全输出向后不变。
仅逆向撤本任务函数、测试段和对应镜像；不恢复整份累积测试文件。
