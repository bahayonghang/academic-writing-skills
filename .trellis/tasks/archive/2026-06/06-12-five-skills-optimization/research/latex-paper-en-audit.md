# latex-paper-en 审计报告（agent 原始产出，2026-06-12/13）

审计范围：`academic-writing-skills/latex-paper-en/` 全部 87 文件 + 仓库根 `tests/`、`conftest.py` 相关部分；对照姊妹 skill `latex-thesis-zh`（F1-F24 修复后版本）。所有可复现 bug 均在系统临时目录用 Python/chktex/latexmk（TeX Live 2025）实测取证，未改动仓库任何文件。
配套外部事实基线：见同目录 `latex-paper-en-venue-factcheck.md`。

## §1 外部环境调研结论（联网核查）

| # | 结论（2026-06 现状） | skill 现状判定 |
|---|---|---|
| 1 | IEEEtran 现行仍为 **v1.8b (2015)**，IEEE 无新模板/换字体；IEEE 摘要官方指引为**单段 ≤250 词**，无全局 "150-200 词" 规则 | `templates/ieee.md:17`、`catalog.md:58` 的 "Abstract: 150-200 words" **错误** |
| 2 | acmart 现行 **v2.18 (2026-05)**：八合一 Primary Article Template、新字体；ACM 2026-01-01 全面 OA；review 投稿 `[manuscript,review,anonymous]` | `templates/acm.md` 无错误事实但**严重过时/空洞**，未提 TAPS/OA/review 选项 |
| 3 | NeurIPS 2025/2026：正文 **9 页，camera-ready +1**；checklist 强制；样式按年命名；lay summary 仅 Position track | `catalog.md:162` "+0" **错误**；"lay summary" 归属 **错误**；"neurips.sty" 文件名不准 |
| 4 | ICML 2026：8 页（camera 9）；正式名 **"Impact Statement"**；camera-ready 需 lay summary + 财务 COI | `catalog.md:163`/`icml.md:23` "Broader Impact Statement" **名称错误** |
| 5 | ICLR 2026：9 页（rebuttal/camera 10）；LLM 重大使用须专节披露否则可 desk reject；互惠审稿 | `catalog.md:164` 方向对，样式精确名 `iclr2026_conference.sty` |
| 6 | ACL/ARR：long 8 页（camera 9）；**Limitations 节 long+short 均强制**；Responsible NLP Checklist 强制；提供官方 Word 模板 | `catalog.md:165` 基本正确，缺 checklist 事实 |
| 7 | AAAI 2026：7 页；camera-ready **无免费 +1 页**，只能购买（$300/页，≤2 页） | `catalog.md:166` "+1" **错误** |
| 8 | COLM：严格 9 页；2026 camera +1；样式精确名 `colm2026_conference.sty` | `catalog.md:167` 文件名不准 |
| 9 | CVPR 2026：8 页含图表；LLM 政策：虚构引用可**不经评审直接拒** | `catalog.md:128-142` 页数正确，LLM 政策缺失 |
| 10 | "references 不计页数" 成立；"LaTeX required for all venues" **不成立**（ACL、AAAI 接受 Word） | `catalog.md:173` **错误** |
| 11 | arXiv：摘要上限 **1920 字符**；2023-12 起自动 HTML；AI 不能署名；**2025-10-31 起 CS 类 review/survey/position 须同行评审证明** | `catalog.md:149` "1500 characters" **错误**；HTML/AI/survey 新政全部缺失 |
| 12 | LLM 润色政策矩阵：各 venue 均允许润色，披露要求各异（ACL checklist 强制；ICLR/COLM 专节；Elsevier 稿内声明段；IEEE 致谢节；ACM 纯写作辅助免披露） | skill 提供 deai 模块却**完全没有披露义务知识**，合规缺口 |

## §2 审计发现总表

### P0 — 宣传功能不存在或对真实论文失效

| # | 发现 | 位置(file:line) | 证据 |
|---|---|---|---|
| **E1** | `format` 模块永远输出 PASS：chktex 解析正则要求 `file:line:col: Warning N: msg`，但 chktex `-v0 -q` 实际输出 `file:line:col:num:msg`（无 "Warning"），`--strict` 的 `-v3` 是 lacheck 风格——两种模式都解析出 0 条 | `scripts/check_format.py:107`、`:70-72` | 实测：含 3 条 chktex 警告的文件 → "Status: PASS / Found 0 issues"。**静默假通过** |
| **E2** | `split_sections` 系统性失效（ZH 清单 #4 全中）：① `\\section*?{...}` 的 `*` 未转义（是 `n` 的量词）→ `\section*{X}` 完全不识别；② 关键词后紧跟 `}` → 复数标题 `Methods}`、`Experiments}`、`RELATED WORKS}` 全部不匹配；③ 不跳过 `%` 注释行；④ 同名 key 覆盖、首段范围丢失 | `scripts/parsers.py:48-57`、`:104-123` | 实测：`\section*{Introduction}`→`{}`；`\section{Methods}`→`{}`；`% \section{Related Work}` 被当真；`\sectio{Introduction}` 反而匹配（证明 `*` 未转义）。影响 deai/logic/grammar/sentences/expression/literature 全部 `--section` 与全文分析 |
| **E3** | PyYAML 硬依赖：`import yaml` 在存在性检查前无条件执行 → 安装到 ~/.claude/skills/ 无 PyYAML 必崩（ZH 同函数已改 try/except 回落） | `scripts/deai_check.py:89`、`:227` | 实测：屏蔽 yaml → `ImportError` |
| **E4** | `deai_check --section <未知名>` 静默 0 检出：回落全文范围但所有 checker 有 section 守卫 → "Density: 0.0%" 假阴性。叠加 E2，starred-section 论文 `--analyze` 输出空报告 exit 0 | `scripts/deai_check.py:312-315` vs `:268-270,:345,:451` | 实测对照：`--section methods` → 0.0%；`--section introduction` → 100.0% |
| **E5** | SKILL.md 路由命令照抄必报错：`analyze_logic.py main.tex --section methods` —— parser 键是 `method`，EN 无 ZH 的 `resolve_section_keys` 别名机制 | `SKILL.md:87`、`references/modules/logic.md:9` | 实测：`Section not found: methods` |
| **E6** | 全部脚本只读单文件、不解析 `\input`/`\include`（ZH 用 tex_loader.py 解决，EN 无对应物） | 所有 `scripts/*.py` | 实测：引用在 intro.tex → verify_bib 误报 "Unused BibTeX entries" |
| **E7** | `check_figures` 的 `\graphicspath` 解析必然失败：外层 lazy 正则在第一个 `}` 截断 → 标准双括号语法 `\graphicspath{{figs/}}` 100% 解析失败，图在子目录即误报 "Image not found" | `scripts/check_figures.py:51-53` | 实测：`graphics_paths=[.]`、状态 MISSING |
| **E8** | `verify_bib --online` 宣传的 DOI 校验不可达：只有"无 doi 且无 url"的条目进 `needs_online_check` → `verify_doi`/`_cross_check` 永不执行，`metadata_mismatch` 是死代码；唯一可达入口 online_bib_verify.py 未被任何 .md 引用 | `scripts/verify_bib.py:152`、`:170-219` | 代码链路：入口条件与 DOI 分支互斥 |

### P1 — 实现缺陷与契约错位

| # | 发现 | 位置 | 证据 |
|---|---|---|---|
| **E9** | `clean_text` 显示数学正则 `\\[^]]*\\]` 从任意反斜杠吃到 `\]`，吞掉中间全部正文 | `scripts/parsers.py:166` | 实测：`\emph{first}...\[L=x^2\]` → 正文被吞 |
| **E10** | `generate_table --style` 空操作：plain 与 booktabs 输出逐字节相同；模块文档照常宣传 | `scripts/generate_table.py:22-23`；`references/modules/tables.md:11-12` | 实测 `==` True |
| **E11** | `check_pseudocode --venue` 仅 ieee 生效：choices 含 acm/springer/neurips/icml 但全是空操作 | `scripts/check_pseudocode.py:261-264` vs `:108` | 代码链路 |
| **E12** | `analyze_grammar` 修订建议整行小写（BERT→bert）；仅 4 条 toy 规则未标 MVP | `scripts/analyze_grammar.py:46-50`；`SKILL.md:85` | 实测确认 |
| **E13** | `analyze_sentences` 对硬换行源文件失效：逐源文件行切句，跨行长句永远检不出（真实 LaTeX 普遍 80 列换行） | `scripts/analyze_sentences.py:57-64` | 实测：同一 72 词句，单行检出/4 行硬换行不检出 |
| **E14** | `check_references` 编号缺口检查必然误报：`fig:resnet18`/`fig:resnet50` 被当同系列 → 报 "fig:resnet19–49 missing" | `scripts/check_references.py:254-295` | 实测确认 |
| **E15** | `improve_expression` 与自家 deai 准则直接冲突：盲替换 use→employ、show→demonstrate（连名词 use 也换），而 deai/guide.md 把 "We use a 3-layer LSTM" 列为 ✅、"results demonstrate the effectiveness" 列为 ❌ | `scripts/improve_expression.py:18-23` vs `references/deai/guide.md:259,:280,:300,:318` | 两模块互相把对方"正确答案"改成"错误答案" |
| **E16** | `optimize_title --interactive` 用 `input()` 阻塞（agent 卡死）且被模块文档推荐；`--compare` 仍强制 positional 文件 | `scripts/optimize_title.py:277-302`；`references/modules/title.md:183` | 实测 rc=2 |
| **E17** | deai 低信息密度的 EVIDENCE_MARKERS 永远匹配不到 `\cite`：在 extract_visible_text 之后匹配而 `\cite{}` 已被剥除 → 引用密集段落照样误报，`\\cite\{` 分支死代码 | `scripts/deai_check.py:216` vs `parsers.py:60-73,125-153` | 代码链路 |
| **E18** | compile.py 中文检测优先级高于 `% !TEX program` 魔法注释（注释里一个汉字即强制 xelatex 覆盖显式指令）；`--recipe X --watch` 时 watch 被静默忽略 | `scripts/compile.py:104-114`、`:209-210` | 代码顺序 |
| **E19** | 编码三种互相矛盾策略并存：17 处 `errors="ignore"/"replace"`；check_pseudocode.py:56、deai_batch.py:191 裸 utf-8 直接 traceback；check_references.py:353-356 只捕 OSError。ZH 已统一 read_text_robust | 17 处详见原文 | 比对 |
| **E20** | venue 知识事实错误（对照 §1）：NeurIPS "+0"/"lay summary" 错；`templates/neurips.md:18` "8-page" 与同文件 :31 "9 pages" **自相矛盾**（icml.md:17 同病）；"Broader Impact Statement" 错；AAAI "+1" 错；arXiv "1500" 错；"LaTeX required for all venues" 错；IEEE "150-200 words" 错；样式文件名不准。catalog 与 templates 双源放大失同步（ZH F14 同病，ZH 已单源化） | `references/venues/catalog.md`、`templates/*.md` | §1 逐条比对 |
| **E21** | AIGC/LLM 披露政策缺位：deai 模块帮用户消除 AI 痕迹，但全 skill 无任何 venue 披露义务知识（ICLR 专节/desk-reject、ACL checklist、arXiv、Elsevier、IEEE、CVPR 虚构引用直接拒） | `references/venues/catalog.md:164`（仅 "LLM disclosure" 四字） | grep 无披露政策内容 |
| **E22** | 孤儿/不可达脚本：check_references.py（375 行质量不错）、extract_prose.py、online_bib_verify.py 不在路由表、无 .md 提及 | `SKILL.md:80-100` | grep 无入链 |
| **E23** | 测试盲区：8/21 脚本零测试（analyze_grammar、analyze_sentences、improve_expression、check_format、check_references、online_bib_verify、deai_batch、extract_prose）。E1/E12/E13 全在零测试脚本 | `tests/test_latex_paper_en_scripts.py:12-21` 等 | import 清单比对 |
| **E24** | evals 形同虚设：19 条全 `"files": []` 无 fixture，断言基本是"输出含模块名"。EN 无 evals/fixtures 目录（ZH 已建 thesis-project） | `evals/evals.json` | 文件本身 |

### P2 — 质量与维护性

| # | 发现 | 位置 | 证据 |
|---|---|---|---|
| **E25** | 死代码与知识多源：`width / 3.0` 计算即丢弃；`_find_section_bounds` 找永不生成的键；`_result()` 重复扫描；AUTHOR_ENUM_EN/GAP_KEYWORDS_EN 双份拷贝；deai 模式三源 | `check_figures.py:135`；`analyze_literature.py:69`；`check_tables.py:87`；`deai_batch.py:87-119` | 代码比对 |
| **E26** | check_format 的 CATEGORIES 按警告编号区间瞎分桶，与 chktex 实际语义无关 | `scripts/check_format.py:29-35` | chktex 手册 |
| **E27** | `$SKILL_DIR` 无解释；SKILL.md 与 modules 两套路径写法并存 | `SKILL.md:82-99` vs `references/modules/*.md` | grep |
| **E28** | 输出契约不统一：SKILL.md:126 规定的格式只有少数脚本遵守；`[Script]/[LLM]` 标注仅两三处；deai `--analyze` 用 exit 1/2 表达密度分级与 SKILL.md:113 "脚本失败须报 exit code" 语义冲突 | 多脚本 | 横向比对 |
| **E29** | 杂项：analyze_abstract 词数下限 150 写死（短摘要 venue 误报）；`when_to_use` 非标准字段；脚本 docstring 自称支持 Typst 与边界矛盾；verification.md:55 依赖未安装的 semanticscholar 包；BibTeX 键大小写按 exact-case 比对 | 见左 | 比对 |

## §3 确认健康、无需动的部分

- **SKILL.md 本体结构**：183 行，description 含正负向分流，Do Not Use 清晰，路由表+执行顺序+缺参追问完整。
- **安全边界好**：prompt-injection 防护、shell-escape 双确认（实测生效）、在线校验默认关闭。
- **渐进式加载**：薄入口 → modules → per-venue templates；>300 行参考文件均有 TOC。
- **compile.py 主体**：latexmk 默认 + recipe 对齐 + bibtex 非零容忍；实测 xelatex 出 PDF。
- **check_pseudocode.py 的 IEEE 事实**与 IEEEtran v1.8b 现状一致。
- **analyze_experiment.py**：唯一实现 SECTION_ALIASES + FALLBACK_SECTION_PATTERNS 的脚本，可作 E5 修复范本。
- **online_bib_verify.py 实现本身**健康（问题在不可达）。
- **trigger_eval.json**：34 条、6 类负例覆盖好。
- **无 Gemini 残留；无 rglob 问题；版本同步**；test_parsers_alignment 哈希锁设计合理（注意 `split_sections` 不在锁内，修复需手动同步 audit/cover-letter 拷贝）。
- **check_tables.py 规则面**与 IEEE 惯例一致。

## §4 建议修复分组

**组 A｜解析底座（P0，最先做）**
1. **A1 移植 ZH 章节解析**（修 E2/E4/E5）：`extract_headings` + `SECTION_TITLE_RULES` + `_split_sections_from_headings` + `resolve_section_keys` 移植到 EN parsers.py，规则表改英文（`\section*{}`、复数、ALL-CAPS、复合标题）；`--section` 未命中列出可用 keys。同步 paper-audit/cover-letter 拷贝并更新 ALIGNMENTS。
2. **A2 移植 tex_loader.py**（修 E6/E19）：read_text_robust + assemble() 接入全部消费脚本，诊断报 `源文件:行号`。
3. **A3 修 check_format**（修 E1/E26）：解析正则改五段式匹配 `-v0` 输出；CATEGORIES 重做或删除。
4. **A4 修 deai_check PyYAML**（修 E3）：照抄 ZH try/except 回落。

**组 B｜脚本正确性（P1，A1 后做）**
5. clean_text 显示数学改 `\\\[.*?\\\]`（E9）；graphicspath 双层提取（E7）；编号系列限定 `前缀:纯数字`（E14）；analyze_sentences 段落拼接再切句（E13）；analyze_grammar 保留大小写+标注 MVP（E12）。
6. verify_bib --online 把含 DOI 条目纳入送验（E8）；generate_table --style 实现或删除（E10）；check_pseudocode venue choices 收敛（E11）。
7. improve_expression 词表与 deai 对齐（E15）；optimize_title isatty 防护 + --compare 解除文件强制（E16）；compile.py 魔法注释优先（E18）；deai EVIDENCE_MARKERS 改 raw 行匹配（E17）。

**组 C｜知识层（P1，纯文档可并行）**
8. 按 §1 逐条修 venue 事实（E20）；**templates/ 与 catalog.md 单源化**（学 ZH F14/F15）。
9. 新增 `references/venues/ai-disclosure.md` 政策矩阵，deai 模块与 Safety Boundaries 交叉引用（E21）。

**组 D｜工程化（P2，最后）**
10. 建 `evals/fixtures/paper-project/`（多文件 IEEE 风格工程，埋入 starred section、复数标题、graphicspath、\input 引用等触发点），E1/E2/E4/E7/E13/E14 写成可执行断言（E24）；补 8 个零测试脚本（E23）。
11. 路由表补 references 模块挂 check_references.py 或移除孤儿（E22）；$SKILL_DIR 解释 + 路径统一（E27）；输出契约统一 + deai exit code 语义标注（E28）；清死代码（E25/E29）。

**执行顺序**：A1 → A2 →（A3/A4 并行）→ B → C（随时并行）→ D。
