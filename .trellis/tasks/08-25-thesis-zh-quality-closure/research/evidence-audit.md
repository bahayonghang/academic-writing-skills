# 手册主张的本仓库取证结果（2026-08-25）

来源手册：`ref/latex-thesis-zh-skill-optimization-plan.md`（审计对象为论文仓库副本
`.agents/skills/latex-thesis-zh/`）。本文件把手册每条主张在**本仓库副本**
`academic-writing-skills/latex-thesis-zh/` 上重新取证，供六个子任务直接引用，不要重复调研。

## 0. 两副本关系

手册的 `path:line` 锚点逐条命中本仓库副本（见下表），但聚合数字对不上：

| 指标                             | 手册（论文仓库副本） | 本仓库副本实测 |
| -------------------------------- | -------------------- | -------------- |
| 文件数                           | 100                  | 98             |
| Markdown 行数                    | 4911                 | 6497           |
| Python 行数                      | 13375                | 15238          |
| `evals/evals.json` case 数       | 31                   | 31             |
| `evals/trigger_eval.json` 查询数 | 39                   | 39             |

结论：两副本已分叉，行号仍对齐。**手册的聚合数字不得写入任何验收标准**；
子任务需要规模数字时现场测量。

## 1. 已实跑复现的缺陷（可直接作为验收依据）

### V1 特殊章角色错选（对应手册 P0-3 / E2）

`analyze_logic.py:1932-1960` 的 `_process_chapter_range()` 在无 `--section` 时取
「绪论后首个非豁免 chapter」。两份豁免表都不含符号表/缩略语章：

- `analyze_logic.py:162-171` `LEAD_EXEMPT_TITLES_ZH` = 摘要 / abstract / 参考文献 /
  bibliography / 致谢 / 附录 / 目录 / contents
- `analyze_logic.py:282-288` `CHAPTER_INTRO_EXEMPT_TITLES_ZH` = 绪论 / 引言 / 结论 /
  总结 / 展望

实跑复现（临时工程，include 顺序：符号表 → 绪论 → 工艺章 → 方法章）：

```
% 过程分析章（chapters/nomenclature.tex:1）[Severity: Info] [Priority: P3]:
  [Script] 第“符号和缩略语说明”章未见过程分析章特征……
```

目标工艺章 `chapters/process.tex` 同时具备过程信号（工艺流程分析）与框架信号
（总体框架），双信号预判本应命中，但因定位阶段已选错章而未被检查。

状态：**validated**。

### V2 词频阈值未按篇幅归一（对应手册 P1-4）

`deai_check.py:888-921` `_check_term_threshold()` 对全文可见文本做 substring 计数，
与 `references/deai/tone-thresholds.yaml` 的固定 cap 直接比较，无可见字数分母。

实跑复现（同一段 4 行内容按 1 / 2 / 4 倍重复，词密度不变）：

| 篇幅 | 结果                              |
| ---- | --------------------------------- |
| 1 倍 | 静默                              |
| 2 倍 | 静默                              |
| 4 倍 | `「因此」全文出现 8 次（上限 6）` |

同密度内容因篇幅增长产生假阳性。状态：**validated**。

### V3 生成表格与公式内容进入文档级词频计数（修正手册 E1）

手册 E1 称控制行、跨行公式、figure 环境会被「报为平行句式或标点候选」。
**该症状未复现**：构造含 `\clearpage`、`\newpage`、跨行 `equation`、`figure` 环境、
带生成注释的 `table` 的工程，`deai_check.py --analyze` 输出零 finding。

实际泄漏窄得多且确实存在：表格单元格与公式 `\text{}` 内的中文进入文档级词频计数。
构造 7 次「首先」全部位于 `tabular` 行与 `equation` 的 `\text{}` 内：

```
第10行 [term_threshold] (result) 「首先」全文出现 7 次（上限 4）
```

机制：`_iter_visible_lines()`（`deai_check.py:880-884`）逐行调用
`parser.extract_visible_text()`。`PRESERVE_PATTERNS`（`parsers.py:191-204`）是
**单行**正则，`\begin{tabular}` 与 `\end{tabular}` 分列不同行时环境体不被剥离。

**E1 的验收标准必须按本条重写**，不能按手册原文写「控制行被报为平行句式」——
那条断言在当前代码上恒为真（本来就不报），起不到回归防护作用。

状态：**validated**（症状与手册描述不同）。

### V4 CLI 中文帮助乱码（对应手册 P1-4）

26 个脚本无一处 `sys.stdout.reconfigure` / `PYTHONIOENCODING` 自设
（`grep -rln "reconfigure|PYTHONIOENCODING" scripts/` 空集）。

实跑：`PYTHONUTF8=0` 且不设 `PYTHONIOENCODING` 时，`deai_check.py --help` 的
中文描述以 GBK 输出，UTF-8 终端读取为乱码（ASCII 部分正常）。设
`PYTHONIOENCODING=utf-8` 后正常。状态：**validated**。

### V5 逐行可见文本解析，16 个消费者各自处理

`parsers.py:242-268` `extract_visible_text(self, line: str)` 以单行为单位。

`tex_loader` 消费者（16 个，均已统一走 `assemble()`，这是 V5 的**有利事实**）：
`analyze_abstract` `analyze_conclusion` `analyze_experiment` `analyze_literature`
`analyze_logic` `blind_review` `check_consistency` `check_format` `check_references`
`check_spec` `check_style_zh` `check_tables` `deai_batch` `deai_check`
`map_structure` `optimize_title`（另 `compile.py` `verify_bib.py` 也引用）。

其中直接调用 `extract_visible_text` 的有 10 个：`analyze_conclusion`
`analyze_experiment` `analyze_literature` `analyze_logic` `blind_review`
`check_format` `check_spec` `check_style_zh` `deai_batch` `deai_check`。

状态：**validated**。source layer 已单一（`tex_loader.assemble`），缺的只是
node 层 IR，不需要另起 include resolver。

### V6 mode 维度缺失

`SKILL.md:105-121` Rewrite Contract 适用范围只有 `expression`；
`references/modules/routing-rules.md:16-18` 把其余 16 个模块列为纯诊断。
无 `diagnose / plan / revise / re-audit / gate` 正交维度。状态：**validated**。

### V7 通用写作规则无适用条件

`references/writing/writing-philosophy-zh.md:90-111`：

- 分章节指南表把篇幅写成无条件要求（摘要 300-500 字、绪论 3-5 页、
  文献综述 5-10 页、总结与展望 1-2 页）
- 「文献综述」行要求「逐篇讨论每篇文献的贡献与局限」
- 「实验必须包含」列出误差分析、超参数搜索范围、计算资源（GPU 型号、总时长）

无 `must / should / may` 分级、无学科/学校适用条件、无冲突裁决。

附带发现一处**跨文件规则冲突**（手册未提，需在本任务处理）：
`writing-philosophy-zh.md:49` 把「基于上述分析，本文提出…」列为✅推荐句式，
`academic-style-zh.md:87` 也把「基于上述分析」列入因果连接词推荐表；而
`references/deai/tone-thresholds.yaml:49-60` 的 throat_clearing 段首正则、
`references/deai/tone-terms-zh.md:76-77`、`references/deai/guide.md:185-187`
把同族段首套语（综上所述 / 由此可见 / 值得注意的是 / 首先，/ 然而，）判为 AI 痕迹。
「基于上述分析」本身未被 deai 词表收录，但与被收录的「由此可见」「综上所述」
同属一类，推荐与禁止并存构成读者可察的规则矛盾。

状态：**validated**。

### V8 因果门禁过粗

`references/writing/over-claim-guard.md:41-42`：「仅以下情况可用因果表述：受控干预
（消融、随机分组、A/B 对比）、工具变量设计、或复现了已确立的机制。」
`:112-116` 反向校准段：「受控干预（消融 / 随机对照 / A-B）得到因果结果 → 用『证明』」。

即实验类型标签（是否叫「消融」）直接决定因果资格，无训练预算可比性、
唯一变化因素、随机性重复、替代解释检查。状态：**validated**。

### V9 eval 只验触发与关键词

`evals/evals.json` 31 个 case，键集恒为
`{id, prompt, expected_output, files, assertions}`，无 `baseline_output`、
`with_skill_output`、`human_notes`。断言类型只有 `contains` / `not_contains` /
`regex`。多条断言形如 `[一-鿿]{5,}`（「有中文输出」）。
状态：**validated**。

## 2. 本仓库集成面（手册完全未覆盖，改动必踩）

手册假定外部仓库结构未知（§10.4 只给了 `rg` 搜索建议）。实测本仓库有六处硬约束：

| #   | 约束                                                                                                                 | 位置                                                                              | 对本任务的含义                                                                                                                                            |
| --- | -------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| C1  | `parsers.py` 成员以 md5 跨 5 副本锁定，含 `LatexParser.PRESERVE_PATTERNS`（en/zh/audit/cover_letter 四副本必须一致） | `tests/contracts/test_parsers_alignment.py:75-116`                                | **已定决策**：新增 `visible_prose.py`，不动被锁成员。ZH 侧 `extract_visible_text` 未被锁（`:87` 只锁 en/audit/cover_letter），但 `PRESERVE_PATTERNS` 被锁 |
| C2  | `evals.json` 必须保留 `{id, prompt, expected_output, files}` 四键与最小 case 数                                      | `tests/contracts/test_skill_contracts.py:352-362`                                 | output eval 升级只能**加字段**，不能换 schema                                                                                                             |
| C3  | 路由表每条命令实跑 `--help`，断言命令中每个 `--flag` 在 help 文本内                                                  | `tests/contracts/test_skill_contracts.py:490-513`、`:519`                         | 新增 flag 必须同步进 argparse；改路由表命令必然跑到该测试                                                                                                 |
| C4  | `docs/resource-manifest.json` 带 sha256，镜像 108 个 thesis-zh 双语文件                                              | `docs/resource-manifest.json`、`tests/contracts/test_docs_bilingual_resources.py` | 每个改 references 的子任务在**自己的提交内**重建 manifest + 双语页面                                                                                      |
| C5  | 全部 SKILL.md `version` 必须等于 pyproject `6.0.0`                                                                   | `tests/contracts/test_skill_versions.py`、`just check-versions`                   | 子任务只改 `last_updated`，不 bump version                                                                                                                |
| C6  | 测试目录是 `tests/skills/latex_thesis_zh/`（现有 19 文件），root `conftest.py` 已把 ZH scripts 追加进 `sys.path`     | `tests/conftest.py:28-30`、`tests/support/paths.py`                               | 手册写的 `tests/latex_thesis_zh/` 路径**错误**，新测试放 `tests/skills/latex_thesis_zh/`                                                                  |

补充：`agents/` 下只有 `openai.yaml`，被 `test_openai_yaml_shape`
（`test_skill_contracts.py:472-480`）要求含 `interface:` / `display_name:` /
`short_description:` / `default_prompt:` 四键。本仓库无 per-skill `README.md`
（人类入口在 `docs/skills/<skill>/index.md` 双语），skill 包内无 `reports/` 先例。

### C7 — `deai_check.py` 第四套锁（AST 逻辑锁 + typst 值锁）

`tests/contracts/test_deai_alignment.py`。改 deai 前必读——它决定「调阈值」
这类方案能落在哪里。

| 成员 | 锁 | 位置 | 可改？ |
| --- | --- | --- | --- |
| `_TIER_FACTORS` | 三副本 md5 | `ALIGNMENTS:136` | 否 |
| `_apply_tier` | 三副本 AST | `LOGIC_ALIGNMENTS:159` | 否 |
| `Checker._iter_visible_lines` | 三副本 AST | `LOGIC_ALIGNMENTS:162` | 否 |
| `Checker._iter_section_paragraphs` | 三副本 AST | `LOGIC_ALIGNMENTS:161` | 否 |
| `Checker._check_overclaim` | 三副本 AST | `LOGIC_ALIGNMENTS:160` | 否 |
| `Checker._check_throat_clearing` | 三副本 md5 | `ALIGNMENTS:144` | 否 |
| `Checker.calculate_density_score` | 三副本 md5 | `ALIGNMENTS:145` | 否 |
| `DEFAULT_THRESHOLDS` 的 `overclaim` / `punctuation` / `sentence_length` / `tense` | 三副本值相等 | `THRESHOLD_ALIGNMENTS:171-175` | 否 |
| `term_thresholds` 的 11 个 CJK 词（全面3 关键5 其次4 因此6 显然3 显著5 核心4 深入3 然而5 重要5 首先4） | ZH 与 typst 同词同值 | `test_term_thresholds_relationships:291-303` | **值不可改** |
| `term_thresholds` 的 14 个 ZH-only 词（此外 另外 进而 而且 通常 一般 尤其 大量 众多 基本 主要 最为 极为 尤为） | 无锁 | — | 可改 |
| `throat_clearing.patterns` 的 CJK 项 | typst 子集须源自 ZH | `test_throat_clearing_relationships:305-313` | 删除会波及 typst |
| `burstiness.consecutive_paragraphs` | 三副本各自 pin（en=2 zh=4 typst=8） | `test_burstiness_config_pinned:228-241` | 改需同步改断言 |
| `_check_term_threshold` `_check_punctuation` `_check_tense` `_check_sentence_length_variance` `_check_low_information_density` `_get_instruction` `_is_false_positive` `check_section` `generate_report` `_load_thresholds` `main` | 文件头 docstring 登记为 intentionally divergent | `test_deai_alignment.py:22-26` | **可改** |

含义：任何「调 deai 阈值」的方案必须落在已登记 divergent 的成员上，
且**不改 cap 值本身**。改判定式或改输入节点集合是安全路径；
改 `term_thresholds` 的 11 个值或 `_iter_visible_lines` 会打断跨 skill 锁。

`.trellis/spec/academic-writing-skills/index.md` 已记录前三套锁的背景速览，
可作为交叉参考。

## 3. paper-audit 可适配面（比手册估计的多）

手册 §7.2 说「从 paper-audit 适配轻量 issue schema」。实测 paper-audit 已有的、
可直接借用而非新造的部分：

`academic-writing-skills/paper-audit/references/ISSUE_SCHEMA.md` 已含
`title` `quote` `comment_type` `severity` `confidence`（high|medium|low|unverified）
`source_kind`（script|llm）`source_section` `related_sections` `root_cause_key`
`review_lane` `evidence_anchor` `claim_strength`（unsupported|observed|supported|strong）
`missing_evidence`。

已有脚本：`consolidate_review_findings.py`（根因合并）、`diff_review_issues.py`
（「Diff two deep-review issue bundles for re-audit style comparisons」）、
`build_claim_map.py`、`verify_quotes.py`、`render_revision_trajectory.py`。
参考：`CONSOLIDATION_RULES.md`、`MODE_GUIDE.md`。

含义：手册 §7.2 的 finding schema 与 §10.2 的 `artifacts.py` / `re_audit.py` 有
现成模式可循，字段名应与 paper-audit 对齐（便于日后交叉消费），但**不复制**
投稿评分、多评审委员会、desk-reject gate、大工作区布局。

## 4. 未取证项（保持 missing evidence）

以下手册 §13.4 列出的项在本任务范围内**不执行**，报告中一律标 missing evidence：

1. skills.sh / SkillsMP / GitHub 外部 prior-art 检索（未获授权，且会触发远程请求）
2. 任何 provider/model 的 baseline vs with-skill 对照
3. 隔离答案的人工盲 A/B 与胜率
4. visible-prose IR 的真实 precision / recall / false-positive rate
5. macOS / Linux / VS Code 等平台兼容
6. 外部仓库 clean install / PR / release / discovery
7. 任何「团队就绪」「公开就绪」或普遍质量提升结论

用户已决定不纳入 Qiaomu Library 仪式性产物（README / interface.yaml / reports/），
沿用本仓库既有约定。因此 §10.2 的 `reports/*` 与 §12 Phase 5-6 的 provider A/B、
盲评、发布流程均不在本任务树内。
