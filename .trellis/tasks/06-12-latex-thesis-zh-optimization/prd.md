# PRD: latex-thesis-zh skill 审计与优化（父任务）

> 审计日期：2026-06-12 · 审计范围：`academic-writing-skills/latex-thesis-zh/`（v5.2.0，63 文件，~11280 行）
> 方法：全量脚本代码审读 + 内容文件审计 + 网络调研（GB/T 7714 修订、thuthesis/pkuthss 生态、高校 AIGC 检测政策）

## 1. 背景与动机

latex-thesis-zh 是六技能套件中体量最大的 skill（19 个脚本、13 个路由模块、40+ 参考文件）。
本次审计确认其整体架构（Module Router + 渐进式加载 + 只读建议输出）是健康的，
但存在**三类系统性问题**：宣传功能与实现脱节、对真实多文件论文工程失效、知识源过时且冗余。

### 外部环境变化（网络调研结论）

1. **GB/T 7714-2025 已于 2025-12-02 发布，2026-07-01 实施，全面代替 GB/T 7714-2015**。
   新增预印本/数据集著录类型，统一著录符号，取消非网络文献访问日期，修改个人责任者规则。
   biblatex 社区已有 gb7714-2025 实现。本 skill 的 description、gb-standard.md、verify_bib.py
   全部锚定 2015 版，三周后即过时。
2. **thuthesis 现行 v7.6.0（2025-03-28）+ 2026-05 CTAN 更新**：BibTeX 样式为
   `thuthesis-numeric.bst` / `thuthesis-author-year.bst`（natbib，源自 gbt7714 v2.1.6+）。
   skill 中 `thubib.bst` 的说法是老版本残留，属事实错误。
3. **pkuthss 原仓库已归档**（GitLab/Gitea archived，迁至 Codeberg，最后实质更新 2024-04），
   活跃的是社区分支（iofu728 等）与 Typst 移植版。skill 未提示此状态。
4. **高校 AIGC 检测政策已成型**（2025 届起）：知网 AIGC 检测通道普及，阈值集中在
   15%–40% 区间（川大文 20/理 15，民航大 30，海大 40 等），且误判争议大（公式/法条被判 AI）。
   deai 模块定位正确，但缺少与校级阈值、误判风险的对接说明。

## 2. 审计发现总表

### P0 — 宣传功能不存在或对真实论文失效

| # | 发现 | 位置 | 证据 |
|---|------|------|------|
| F1 | `--standard gb7714` 是空操作：`self.standard` 从未被读取，`GB7714_RECOMMENDED` 定义后未引用。SKILL.md bibliography 模块主命令宣传的国标校验实际不存在 | `scripts/verify_bib.py:33,28` | 全文无 `self.standard` 消费点 |
| F2 | 必填字段表仅 article/inproceedings/book 三类；GB/T 7714 高频类型 学位论文[D]、标准[S]、专利[P]、电子文献[EB/OL]、报告[R] 完全未校验 | `scripts/verify_bib.py:22-27` | |
| F3 | 所有分析脚本只读单文件，不解析 `\input/\include`。真实学位论文（thuthesis/pkuthss 均如此）主文件只有 include 骨架 → `analyze_logic.py main.tex` 等文档命令静默输出"未检测到问题" | `analyze_logic.py:1040`、`deai_check.py:243`、`analyze_abstract.py`、`analyze_experiment.py:242`、`analyze_literature.py:140`、`check_tables.py:50`、`check_format.py:122`、`optimize_title.py` | `map_structure.py:78-140` 与 `check_references.py:346-369` 已有可复用的 include 解析实现 |
| F4 | `parsers.LatexParser.split_sections` 三连缺陷：(a) 同类章节区间互相覆盖（两章都含"方法"时前一章从 dict 中丢失，所有章节级检查静默跳过该章）；(b) 不跳过 `%` 注释行（注释掉的 `\chapter{结论}` 仍被当真）；(c) 不匹配 `\chapter*{摘要}`、`绪\quad 论`、含空格标题等常见写法 | `scripts/parsers.py:81-99` | Typst 分支反而跳过了注释（parsers.py:192） |

### P1 — 实现缺陷与契约错位

| # | 发现 | 位置 |
|---|------|------|
| F5 | 破折号三倍计数：`text.count("——") + text.count("—")`，一个"——"计 3 处，两处"——"即误报超限 | `deai_check.py:658` |
| F6 | `--analyze` 仅扫描 SECTION_PATTERNS 命中的章节；标题不含关键字的正文章（如"多模态情感识别模型研究"）完全不进入章节级检查 | `deai_check.py:699-700` + `parsers.py:51-61` |
| F7 | `_is_false_positive` 中 `text[max(0, start-20):start]` 计算后丢弃（死代码，前向上下文判断从未生效） | `deai_check.py:263` |
| F8 | PyYAML 是仓库依赖，但 skill 安装到 `~/.claude/skills/` 后用户环境通常没有 → `deai_check.py` 构造函数即崩溃 | `deai_check.py:99-109`、`pyproject.toml` |
| F9 | SKILL.md 路由命令 `analyze_logic.py main.tex --section related` 会静默关闭全部章节级检查（导语/主线/章引言/漏斗/三方对齐都在 `if not section` 分支）；`--cross-section`（C3 闭合）从未在 SKILL.md 文档化，按文档操作永远跑不到 | `analyze_logic.py:1096-1118` vs `SKILL.md:83,97` |
| F10 | `check_references.py`（质量最好的多文件脚本）不在 Module Router 的 13 个模块中，从 SKILL.md 不可达 | `SKILL.md:71-87` |
| F11 | `--section` 仅接受英文键（introduction/related），用户传"绪论"报错且不提示可用值 | `analyze_logic.py:1044-1047`、`deai_check.py` |
| F12 | `verify_bib.py:265` 输出 "Use 'google_web_search'"——Gemini CLI 工具名残留，Claude Code 无此工具 | `verify_bib.py:265` |
| F13 | `$SKILL_DIR` 在 Claude Code 中不是预定义环境变量，SKILL.md 未说明替换约定，照抄命令会展开为空 | `SKILL.md:75-87` |
| F14 | 模板知识三源并存且失同步：`templates/` 与 `references/university-templates/` 三对文件逐字节相同（~270 行纯冗余）；`detect_template.py:23-29` 仍接旧目录且无 yanshan 映射；`map_structure.py:22-48` 又硬编码一份 TEMPLATES 事实 | 见左 |
| F15 | thubib.bst 过时（现行 thuthesis-numeric.bst）；pkuthss 归档状态未提示（见 §1） | `templates/thuthesis.md:15`、`templates/pkuthss.md` |
| F16 | `check_consistency.py` 把"全称+缩写并用"判为不一致并建议"统一使用 CNN"——与国标"首次全称（缩写），后文用缩写"惯例直接冲突，对规范论文必然误报 | `check_consistency.py:22-32,117-126` |
| F17 | `check_consistency.find_tex_files` 用 `rglob("*.tex")` 扫全目录，未被 include 的废稿/备份一并计入统计 | `check_consistency.py:237-254` |
| F18 | `gb-standard.md` 第五、六节把校级排版规定（黑体三号章标题、宋体五号图题）包装成 GB/T 7714 国标内容，且 `modules/format.md` 原样复读；这些是各校自定的，应归入模板层并标注来源 | `references/citations/gb-standard.md:117-141`、`references/modules/format.md` |

### P2 — 质量与维护性

| # | 发现 | 位置 |
|---|------|------|
| F19 | evals.json 19 条用例全部 `"files": []`，无任何 fixture 论文工程，端到端无法真实执行；断言只验"输出提到模块名" | `evals/evals.json` |
| F20 | 孤儿文件：`references/formatting/caption-guide.md`、`references/university-templates/yanshan.md`、`references/writing/writing-philosophy-zh.md` 无任何入链 | 见左 |
| F21 | 未测脚本：check_format、check_references、online_bib_verify、deai_batch、generate_table（test_latex_thesis_zh_scripts.py 覆盖 11 个模块，其余缺位） | `tests/` |
| F22 | 全部脚本 `errors="ignore"/"replace"` 读文件：GBK 编码论文被静默打成乱码后"检查通过" | 各脚本 read_text |
| F23 | `check_format.py` 的 oral_expression 把"我们"全量标记且无 visible-text 过滤；`optimize_title.py --interactive` 交互模式不适配 agent 执行 | `check_format.py:35`、`optimize_title.py:328` |
| F24 | deai 模块未与 2025-2026 高校 AIGC 检测现实对接：tier 阈值与校级 15%-40% 红线无映射，未提示检测误判风险（公式/法条误报）与"辅助可、代写禁"的政策边界 | `references/deai/guide.md`、`tone-thresholds.yaml` |

### 确认健康、无需动的部分

- parsers.py 五份拷贝的"有意分化"已由 `tests/test_parsers_alignment.py` 哈希锁定（ZH 缺 clean_text 是文档化设计）；
- `agents/openai.yaml` 为全仓库统一惯例；
- SKILL.md 167 行，渐进式加载结构良好；Safety Boundaries / Output Contract 清晰；
- trigger_eval.json 27 条且负例为高质量近邻（EN/Typst/audit/bib-search 边界）；
- compile.py 配方设计、online_bib_verify.py 纯标准库实现均合格。

## 3. 子任务映射

| 子任务 | 优先级 | 覆盖发现 |
|--------|--------|----------|
| `06-12-zh-parsers-multifile` | P0 | F3, F4, F11, F22 |
| `06-12-zh-gb7714-validation` | P0 | F1, F2, F12, F18(国标部分), §1.1 新国标 |
| `06-12-zh-router-cli-alignment` | P1 | F9, F10, F13, SKILL.md 修订 |
| `06-12-zh-template-knowledge` | P1 | F14, F15, F18(校级排版迁移), F20(yanshan) |
| `06-12-zh-checker-precision` | P1 | F5, F6, F7, F8, F16, F17, F23, F24 |
| `06-12-zh-fixtures-evals` | P2 | F19, F21, F20(孤儿清理) |

执行顺序建议：parsers-multifile → gb7714-validation / checker-precision（并行）→
router-cli-alignment → template-knowledge → fixtures-evals（验收层，最后做）。
parsers 改动是其他任务的地基（章节切分 API 变更会影响所有 analyzer），必须先行。

## 4. 跨子任务验收标准（父任务集成验收）

1. 用 fixtures 中的多文件 thuthesis 风格工程跑 SKILL.md 路由表全部 13 条主命令：
   每条命令按文档原样执行（仅替换 `$SKILL_DIR` 与入口文件）即产生非空、正确的诊断输出。
2. `verify_bib.py references.bib --standard gb7714` 对含 [D]/[S]/[P]/[EB/OL] 缺字段的
   fixture .bib 至少产出对应类型的缺字段告警，并提供 2025 新国标过渡期提示。
3. `just ci` 全绿；SKILL.md version 与 pyproject 同步规则不破坏（单 skill 任务不 bump version，只改 last_updated）。
4. 模板事实单一来源：同一事实（如 thuthesis bst 名）在仓库内只出现一处权威定义。
5. 三个孤儿文件被引用或被删除，无新增孤儿。

## 5. 范围外（明确不做）

- 不新增"从零写论文"能力（Do Not Use 边界保持）；
- 不把 deai 做成针对特定检测平台的对抗工具（仅可读性导向 + 政策风险提示）；
- 不动 paper-audit / latex-paper-en 等兄弟 skill（除非 parsers 对齐测试要求镜像修改）；
- 不引入新的第三方运行时依赖（PyYAML 问题通过降级为可选依赖解决，而非加依赖）。

## 6. 调研来源

- GB/T 7714-2025 发布公告与解读：openstd.samr.gov.cn（hcno=C6CE52E55AC09B9C79A20AEA77CEDD14）、
  沈阳药科大学期刊编辑部 pd.syphu.edu.cn/info/1021/2608.htm、LaTeX 工作室 biblatex-gb7714-2025 实现测试
- thuthesis：CTAN（ctan.org/pkg/thuthesis，v7.6.0 2025/03/28）、github.com/tuna/thuthesis
- pkuthss：gitea.com/CasperVector/pkuthss（2024-08-28 archived）→ codeberg.org/CasperVector/pkuthss
- 高校 AIGC 政策：教育部"允许辅助、禁止代写"定调；川大/民航大/海大/华师大等 2025 届通知；
  南京大学"检测结果仅作辅助参考"声明
