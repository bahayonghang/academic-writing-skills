# typst-paper 路由对齐与真实工程适配

> 父任务：`06-12-five-skills-optimization`（完整审计报告见其 `research/typst-paper-audit.md`，发现 T1-T40）
> 优先级：P0 · 依赖：`06-13-en-family-parsers`（T6 多文件装配 / T7 模板工程提取 /
> T21 同名章节与块注释属 parsers.py 拷贝层，由地基任务统一修复后本任务消费其 API）。
> 其余发现（T1-T5、T8-T20、T22-T40）不依赖地基，可并行。

## Goal

消除两类系统性塌方：(a) 约半数模块文档描述的是 LaTeX 姊妹版脚本的 CLI 与行为，
照文档执行必报错；(b) 脚本层对真实 Typst 论文的两种主流形态（charged-ieee 类
模板工程、多文件工程）整体失效。让 SKILL.md 路由表的每条主命令按文档原样执行
即产生正确的非空诊断。

## Requirements

### R1 止血：路由表承诺成立（T1/T2/T3/T4/T5/T26 — P0）

- T3/T26 `--section` 取值：脚本侧加 `methods→method` 等别名表（仿
  analyze_experiment 的 SECTION_ALIASES，建议抽到共享处），SKILL.md:82,84、
  LOGIC.md:7、examples 同步校正。
- T2 analyze_experiment 给 experiment 章节加实际检查（至少把数字归因/
  讨论深度检查套用到 experiment 段），不许"永远 No issues detected"。
- T1 check_references：接受 `--bib`/自动解析 `#bibliography(...)` 找到键集，
  `@key` 命中 bib 键时不报 undefined；`REF_RE`/`LABEL_RE` 字符集加 `:`
  （支持 `<fig:example>`/`@fig:arch`）。
- T4 verify_bib 为 Hayagriva 建立独立必填字段表（`date`/`parent` 语义），
  不再把 BibTeX 表（journal/year）套在 .yml 上；Hayagriva 跳过 en-dash 页码建议。
- T5 verify_bib 引用正则改 `@([A-Za-z][\w:.-]*)`；删除前缀黑名单
  （fig/tab/eq/sec...），改为与 bib 键集合做交集判断。

### R2 真实工程形态适配（T6/T7/T8 — P0，依赖地基任务）

- T6/T7 由 `06-13-en-family-parsers` 提供：`#include` 装配（typ_loader）、
  模板形参提取（`xxx.with(title:..., abstract:...)`）、`= Abstract` 英文标题。
  本任务负责把全部脚本入口切换到新 API 并补集成测试。
- T8 check_format 检测到 `@preview/charged-ieee` 等模板 import 时跳过
  page/columns 类版式检查，输出一行 info"版式由模板托管"。

### R3 文档 Typst 事实修正（T9/T10/T11/T12/T13/T14/T15/T30/T31/T35/T36 — P0/P1，纯文档）

- T9 8 处 `column-gutter` 移出 `#set page(...)`（page 函数无此参数）：
  templates/ieee.md:24、acm.md:22、VENUES.md:79,138,259,290、TEMPLATES.md:42、
  TYPST_SYNTAX.md:312。
- T10 `style: "gb-7714-2015"` → `"gb-7714-2015-numeric"`（TYPST_SYNTAX.md:285、
  VENUES.md:356），并补一句"GB/T 7714-2025 尚无 hayagriva 内置样式"现状。
- T11 COMPILE.md typst CLI 改位置参数写法（无 `--output` flag）；补 PNG 多页
  `{p}` 模板说明。
- T12-T15 BIBLIOGRAPHY/CITATION_STYLES/TITLE/SENTENCES/ABSTRACT/TABLES 六个文档
  按本 skill 脚本的真实 `--help` 重写（现在描述的是 LaTeX 版 CLI：`--tex`、
  `--standard gb7714`、`--json`、`--style vancouver`、`--interactive`、
  `--compare`、`--threshold`、`main.tex` 全部不存在）。
- T30 charged-ieee 0.1.0 → 0.1.4（3 处）；测试 fixture 的包版本/API 改为真实
  可编译组合（algorithmic 1.0.7 API、lovelace 0.3.1 `pseudocode-list`）。
- T31 Typst 示例里的 Markdown 粗体修正：`**...**` → `*...*`（VENUES.md:475、
  EXPERIMENT.md:21、analyze_experiment.py:38-39 的指导文本）。
- T35 TYPST_SYNTAX.md：eq 编号示例补 `#set math.equation(numbering:)`；
  引用抑制示例改 `#cite(<key>, form: ...)`；修复 539-548 嵌套代码围栏。
- T36 NeurIPS 页数统一为 9（templates/neurips.md:13 现写 8，VENUES.md:419 正确）。

### R4 实现层缺陷（T16/T17/T18/T19/T20/T22/T23/T24/T25 — P1）

- T16 analyze_grammar/analyze_sentences/improve_expression 输出前缀改用
  `parser.get_comment_prefix()`（现在硬编码 `%`）；online_bib_verify 统一 `//`。
- T17 generate_table `--style` 空操作：实现 plain 分支或删除参数。
- T18 compile.py watch 分支传递 `--format`；PNG 多页自动加 `{p}`。
- T19 deai_check 未知 `--section` 显式报错退出（现静默 0 traces）。
- T20 em-dash 计数改互斥匹配 `len(re.findall(r"---|——|—", text))`
  （现 "——" 一处计 3，与 ZH F5 同病同修）。
- T22 optimize_title 无效词加 `\b` 词边界（现 "Renewable" 因含 "new" 被 Critical）。
- T23 deai_check 的 `import yaml` 移入 `yaml_path.exists()` 分支并 try/except
  降级 DEFAULT_THRESHOLDS（与 ZH F8 同修，verify_bib.py:122-130 是仓内正例）。
- T24/T25 check_format `#set page` 块先平衡括号截取再内部匹配；figure/caption
  正则支持嵌套括号与 `caption: "..."` 字符串形式；check_references 标签 span
  判定放宽到闭括号后一行。
- T14 analyze_sentences 中文支持：句切分加中文标点、长度以字符计——或从
  SENTENCES.md 移除中文宣传（二选一，倾向前者，skill 定位是双语）。
- T38 analyze_experiment 文件不存在时报错（prompt 生成模式改显式 `--prompt` 开关）。
- T39 analyze_grammar 替换保留原大小写。

### R5 可达性、测试与评测（T27/T28/T29 — P1）

- T29 check_references 修复后纳入 Module Router（新模块行或并入 format/tables）；
  deai_batch、online_bib_verify 至少进 Reference Map；generate_table 经修正后的
  TABLES.md 可达。
- T28 为 10 个零覆盖脚本补 root 测试（优先 check_references/check_tables/
  generate_table，以 T1/T17 复现用例固化）；conftest 的 SCRIPT_DIR_TYPST
  死常量删除或真正启用。
- T27 evals.json 绑定 fixture：建 charged-ieee 风格 + bare 风格两个迷你论文工程
  （含 .bib 与 .yml 双参考文献，正好回归 T4/T7/T8），断言锚定脚本行为；
  契约测试加 typst eval-fixture 绑定断言（仿 paper-audit 现有做法）。

### R6 一致性与瘦身（T32/T33/T34/T37/T40 — P2）

- T32 expression/deai 词表冲突消解：COMMON_ERRORS/EXPRESSION 删除 Notably/
  It is worth noting that/numerous 等与 deai 阈值表对打的建议，或加冲突对照注记；
  EXPERIMENT.md:31 的 "demonstrates robust performance" 示例更换。
- T33 孤儿文件处理：AI_TONE_TERMS/TERMINOLOGY/TRANSLATION_GUIDE 挂到对应模块
  See-also；BEST_PRACTICES/REVIEWER_PERSPECTIVE 评估后引用或删除；
  references/TEMPLATES.md 并入 templates/ 单源（已发生版本漂移）。
- T37 SKILL.md 补 `$SKILL_DIR` 占位符说明；模块文档路径写法统一。
- T34 14 处 `errors="ignore"/"replace"` 改为显式告警或 strict + 友好提示
  （与 ZH F22 同修）。
- T40 死代码清理：analyze_literature 永不存在的键、translate_academic 字面
  省略号、check_tables 重复扫描与 P3 越界。

## Constraints

- parsers.py 拷贝改动一律走 `06-13-en-family-parsers`，本任务不得单独漂移
  typst 拷贝（哈希锁 test_parsers_alignment 会拦截）。
- 输出契约保持 `// MODULE ...` + Severity/Priority + [Script]/[LLM] 不变。
- 不 bump version，只改 last_updated；SKILL.md 表格改动注意
  [[skill-md-formatter-gotcha]]（ROUTER_ROW_RE 契约测试）。

## Acceptance Criteria

- [ ] SKILL.md 路由表全部主命令对 fixture 工程按文档原样执行（仅替换
      $SKILL_DIR 与入口文件）产生非空、正确诊断；`--section methods` 不再报错。
- [ ] charged-ieee 模板 fixture：optimize_title/analyze_abstract 提取到
      title/abstract；check_format --venue ieee 零 Critical 误报。
- [ ] 正常带引用论文（2 cite + 1 `@fig:arch`）经 check_references 零误报。
- [ ] 合法 Hayagriva 条目（date/parent）经 verify_bib 零缺字段误报；
      连字符键不再误报 not found/unused。
- [ ] 六个模块文档中出现的每个 CLI flag 都能在对应脚本 `--help` 中找到
      （加契约测试覆盖 flag 与 --section 取值）。
- [ ] 2 处中文 "——" 不触发 em-dash 告警；"Renewable Energy" 标题零无效词误报。
- [ ] 缺 PyYAML 环境（monkeypatch）deai_check 可运行。
- [ ] evals.json 至少 8 条绑定 fixture 文件且断言验证脚本行为。
- [ ] `just ci` 全绿。
