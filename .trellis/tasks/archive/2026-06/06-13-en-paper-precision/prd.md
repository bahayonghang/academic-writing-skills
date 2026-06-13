# latex-paper-en 检查器正确性与 venue 知识更新

> 父任务：`06-12-five-skills-optimization`（完整审计见其 `research/latex-paper-en-audit.md`
> E1-E29 + `research/latex-paper-en-venue-factcheck.md` 事实基线）
> 优先级：P0 · 依赖：`06-13-en-family-parsers`（E2/E4/E5 章节切分、E6 多文件装配、
> E9 clean_text 在 parsers 拷贝层修复，本任务消费其 API 并接线全部消费脚本）。
> 其余发现（E1/E3/E7-E29）不依赖地基，可并行。

## Goal

消除"检查器静默假通过/假阴性"这一最危险的缺陷类别（format 模块对任何输入都
PASS、deai 对未知章节 0 检出、--online 校验不可达），修复与自家 deai 准则互打的
建议引擎，并把 venue 知识层对齐 2026-06 事实（9 处错误）+ 补齐 AI 披露政策矩阵。

## Requirements

### R1 假通过/假阴性止血（E1/E3/E4/E8/E26 — P0）

- E1 check_format 解析重写：chktex 输出按五段式 `(.+?):(\d+):(\d+):(\d+):(.+)`
  解析 `-v0 -q` 实际格式；`--strict` 改用可解析的 verbosity；零解析命中但
  chktex 返回非空输出时报 internal error 而非 PASS。
  回归：含 3 条已知 chktex 警告的 fixture 必须检出 3 条。
- E26 CATEGORIES 编号区间分桶与 chktex 语义无关：按真实警告号映射重做或删除分类。
- E3 deai_check PyYAML：照抄 ZH 的 try/except 回落 DEFAULT_THRESHOLDS + stderr
  一行提示（`latex-thesis-zh/scripts/deai_check.py:109-117` 为范本）。
- E4 deai_check 未知 `--section` 显式报错并列出可用 keys（消费地基任务的
  resolve_section_keys），不再静默 "Density: 0.0%"。
- E8 verify_bib `--online`：含 DOI 的条目纳入送验使 `verify_doi`/`_cross_check`
  可达（现入口条件与 DOI 分支互斥，metadata_mismatch 是死代码）；
  online_bib_verify.py 在 bibliography 模块文档中给出入口。

### R2 检查器正确性（E7/E10-E18 — P1，依赖地基的项后做）

- E7 `\graphicspath{{figs/}}` 双层括号解析修复。回归：子目录图不再误报 MISSING。
- E14 check_references 编号缺口限定 `前缀:纯数字` 系列（fig:resnet18/50 不再当缺口）。
- E13 analyze_sentences 先按段落拼接再切句（80 列硬换行的真实 LaTeX 可检出长句）。
- E12 analyze_grammar 替换保留原大小写；SKILL.md/模块文档标注 MVP 规则集规模。
- E10 generate_table `--style` 实现 plain 分支或删除参数（文档同步）。
- E11 check_pseudocode `--venue` 收敛 choices 至实际生效集或文档说明仅 ieee 生效。
- E15 improve_expression 与 deai 词表对齐：删除 use→employ、show→demonstrate
  等被 deai/guide.md 列为反例的盲替换（与 typst T32 同类同修）。
- E16 optimize_title `--interactive` 加 `sys.stdin.isatty()` 防护；`--compare`
  解除 positional 文件强制。
- E17 deai EVIDENCE_MARKERS 改在 raw 行匹配（extract_visible_text 已剥 `\cite`，
  现 `\\cite\{` 分支死代码、引用密集段落误报低信息密度）。
- E18 compile.py `% !TEX program` 魔法注释优先于中文检测；`--recipe`+`--watch`
  组合给出警告而非静默忽略。
- E19 编码策略统一：17 处 `errors=ignore/replace` 与 2 处裸 utf-8 统一接入
  地基任务的 read_text_robust。
- E6 接线：全部消费脚本（verify_bib/check_references/check_figures/check_tables/
  deai/logic/literature/experiment/abstract）走 tex_loader 装配，诊断报
  `源文件:行号`。

### R3 venue 知识层（E20/E21/E29 — P1，纯文档可并行）

按 `research/latex-paper-en-venue-factcheck.md` 逐条修正：

- E20 事实错误：NeurIPS 9+1 页（现 "+0"）、删 NeurIPS lay summary（属 ICML/
  Position track）、样式文件按年命名、ICML "Impact Statement"（现 "Broader
  Impact Statement"）、AAAI camera-ready 付费加页（现 "+1"）、arXiv 摘要 1920
  字符（现 1500）、删 "LaTeX required for all venues"（ACL/AAAI 收 Word）、
  IEEE 摘要 ≤250 词（现 "150-200"）、iclr2026_conference.sty / colm2026_conference.sty
  精确名、acmart v2.18 + ACM 2026 全面 OA、templates/neurips.md 内部 8/9 页自相矛盾、
  ACL Limitations/Responsible NLP Checklist 补充。
- **catalog.md 与 templates/ 单源化**（学 ZH F14/F15 方案：一处权威定义，
  另一处只留索引或生成）。
- E21 新增 `references/venues/ai-disclosure.md`：12 venue/出版商 LLM 政策矩阵
  （润色是否允许、披露位置、desk-reject 风险——ICLR 专节/ACL checklist/
  Elsevier 声明段/IEEE 致谢/CVPR 虚构引用直接拒/arXiv CS 综述新政），
  deai 模块文档与 SKILL.md Safety Boundaries 交叉引用。
- E29 杂项：analyze_abstract 词数下限可配置（短摘要 venue）；verification.md
  semanticscholar 依赖示例修正；BibTeX 键大小写按 case-insensitive 比对；
  脚本 docstring 的 Typst 措辞与边界声明对齐。

### R4 可达性、契约与工程化（E22/E23/E24/E25/E27/E28 — P2）

- E22 check_references.py 纳入路由表（references 模块）；extract_prose、
  online_bib_verify 至少进 Reference Map 或显式移除。
- E27 SKILL.md 补 `$SKILL_DIR` 占位符解释；与 modules 的路径写法统一。
- E28 输出契约统一：`% MODULE (Line N) [Severity] [Priority]` 推广到
  check_format/check_figures/analyze_abstract/verify_bib/generate_table；
  deai `--analyze` 的 exit 1/2 密度分级语义在 SKILL.md 标注。
- E24 建 `evals/fixtures/paper-project/`：多文件 IEEE 风格工程，埋入本审计
  触发点（starred section、复数标题、graphicspath 子目录图、\input 引用、
  硬换行长句、含 chktex 警告的格式问题），evals.json 断言锚定脚本行为
  （仿 ZH thesis-project 的 README 埋点清单 + coverage 测试 + evals 联动模式）。
- E23 补 8 个零测试脚本的最小测试（analyze_grammar、analyze_sentences、
  improve_expression、check_format、check_references、online_bib_verify、
  deai_batch、extract_prose），E1/E12/E13 复现用例固化。
- E25 死代码清理：`width / 3.0`、永不生成的键、重复扫描、AUTHOR_ENUM_EN 双拷贝
  （与 analyze_literature 合并单源）、deai 模式三源收敛。

## Constraints

- parsers.py 拷贝改动一律走 `06-13-en-family-parsers`；EN 是规范拷贝，
  本任务的脚本层改动不得绕过哈希锁直接动 parsers。
- ZH 拷贝零改动（[[latex-thesis-zh-audit-2026-06]]：勿回同步有意分化）。
- deai 模块保持"可读性导向"定位，ai-disclosure.md 只描述政策事实，
  不提供规避检测建议。
- 不 bump version，只改 last_updated；SKILL.md 路由表改动注意
  [[skill-md-formatter-gotcha]]。

## Acceptance Criteria

- [ ] 含 3 条 chktex 警告的 fixture：check_format 检出 3 条（不再 PASS）。
- [ ] `--section methods` 经别名解析正常执行；未知章节名报错并列出可用 keys。
- [ ] 缺 PyYAML 环境（monkeypatch）deai_check 可运行。
- [ ] `\graphicspath{{figs/}}` + 子目录图零误报；fig:resnet18/50 无编号缺口误报。
- [ ] 4 行硬换行的 72 词句被 analyze_sentences 检出。
- [ ] verify_bib --online 对含 DOI 条目实际发起校验（mock 网络层断言调用）。
- [ ] improve_expression 不再输出 use→employ、show→demonstrate 替换。
- [ ] catalog.md 通过事实抽查：NeurIPS 9+1、ICML Impact Statement、AAAI 付费加页、
      arXiv 1920、IEEE ≤250 词、无 "LaTeX required for all venues"；
      同一 venue 事实在仓库内只有一处权威定义。
- [ ] `references/venues/ai-disclosure.md` 存在且被 deai 模块文档与
      SKILL.md 引用，无"规避检测"措辞。
- [ ] evals/fixtures/paper-project/ 落地，evals.json 至少 10 条绑定 fixture，
      E1/E2/E4/E7/E13/E14 有可执行回归断言。
- [ ] `just ci` 全绿。
