# 中文学位论文审阅准则

适用范围：`--venue thesis-zh` 或 `lang == "zh"` 的学位论文（大论文）。不适用于英文会议/期刊小论文。

方法章叙述质量不在自动审计链内，走 `latex-thesis-zh --method-narrative --section`（与 `SKILL.md` 声明一致）。

本 agent / 本文件**不产出**评阅等级（优/良/中/差）或“同意答辩”结论。`paper-audit` 已有 `gate` PASS/FAIL 与 ScholarEval 分数；再加一套等级会产生互相冲突的结论面。

中文伪代码规范不在下表。C1 判定 `check_pseudocode.py` 非语言中性，已在 zh 下抑制；本地化属范围外后续项。

## 三个集合（不得混用）

| 集合 | 数量 | 来源 | 性质 |
|---|---|---|---|
| 运行时基础评分维度 | 8 | `scripts/scoring_model.py` 的 `soundness` / `clarity` / `presentation` / `novelty` / `significance` / `reproducibility` / `ethics` / `literature_grounding` | 参与加权评分 |
| 派生总分 | 1 | `overall_base`（由前 8 维计算） | 不是独立评阅维度。`FEATURE_NAMES` 上方“9 base dimensions”注释不准 |
| 中文审阅指标行 | 15 | 下表 | 文档层指标，映射到基础维度，不参与权重 |

权重取自 `quality_rubrics.md`，不复制其分档文字，不新建评分体系。

## 15 行中文审阅指标

| # | 中文审阅指标行 | 基础评分维度 | 档位 | 承载 |
|---|---|---|---|---|
| 1 | 选题意义与前沿性 | `significance` (13%) | `[LLM]` | reviewer 判断 |
| 2 | 文献综述质量（评述而非罗列） | `literature_grounding` (12%) | `[Script]` + `[LLM]` | `analyze_literature.py`（module `LITERATURE`）+ reviewer |
| 3 | 理论基础扎实度 | `soundness` (18%) | `[LLM]` | reviewer 判断 |
| 4 | 研究方法与技术路线 | `soundness` (18%) | `[Script]` + `[LLM]` | `analyze_logic.py` / `analyze_experiment.py` + reviewer |
| 5 | 工作量与难度 | `significance` (13%) | `[LLM]` | reviewer 判断；不得用篇幅、图表数、公式数、参考文献数代理 |
| 6 | 创新性（硕士 / 博士标准分档） | `novelty` (13%) | `[LLM]` | reviewer 判断 |
| 7 | 结论可靠性 | `soundness` (18%) | `[Script]` + `[LLM]` | `analyze_conclusion.py`（module `CONCLUSION`）+ reviewer |
| 8 | 章节结构完备性 | `presentation` (8%) | `[Script]` | `check_spec.py`（module `SPEC`） |
| 9 | 摘要与关键词规范 | `clarity` (13%) | `[Script]` | `analyze_abstract.py`（module `ABSTRACT`） |
| 10 | 三线表规范 | `presentation` (8%) | `[Script]` | `check_tables.py`（module `TABLES`） |
| 11 | 图片质量与编号 | `presentation` (8%) | `[Script]` | `check_figures.py`（module `FIGURES`，语言中性复用） |
| 12 | 参考文献 GB/T 7714 | `presentation` (8%) | `[Script]` | `verify_bib.py --standard gb7714`（module `BIB`，仅 `.tex`） |
| 13 | 语言表达规范 | `clarity` (13%) | `[Script]` | `check_style_zh.py`（经 `sentences` 键覆盖，module `SENTENCES`） |
| 14 | 学术规范与原创性 | `ethics` (5%) | `[LLM]` | reviewer 判断；不做查重 |
| 15 | 盲审可识别信息 | `ethics` (5%) | `[Script]` | `blind_review.py --check`（module `BLIND`） |

可复现性（`reproducibility` 8%）由既有链路承担，不新增中文指标行。

## 档位纪律

第 1、3、5、6、14 行是 `[LLM]`。不得为其新增正则或词表检查器。工作量与创新性尤其不能用篇幅、图表数、公式数、参考文献数代理判定。

每个 `[Script]` 承载只归属一个 module，不重复计分。

## 硕士 / 博士差异（reviewer 判断依据）

- 硕士：创新可以是应用、集成或工程改进，但须说清相对最接近工作的增量。
- 博士：创新须有可独立陈述的知识贡献（方法、理论或系统），并在结论中可核验。
- 工作量：看问题难度、实现完整度与证据强度，不看页数。
- 学位级别以学校模板 / `latex-thesis-zh --degree` 为准；`paper-audit` 不复制该 CLI 轴。

## 学位论文评阅人阅读路径

期刊审稿人常先看贡献与实验（见 `REVIEWER_PSYCHOLOGY.md`）。学位论文评阅人应先看结构完备性与工作量是否支撑答辩，再看创新性是否达到学位档，最后看表达与规范。

## 与既有参考的边界

| 既有文件 | 职能 | 本文档的关系 |
|---|---|---|
| `DEEP_REVIEW_CRITERIA.md` | 16 类问题分类 | 不新增问题类别 |
| `REVIEW_CRITERIA.md` | 顶层评分映射 | 不改映射 |
| `quality_rubrics.md` | 分档描述 | 只引用权重 |
| `CHECKLIST.md` | 机械清单 | 勾选项留在清单 |
| `VENUE_RULES.md` | venue 硬约束 | 页数/字数硬约束指向它 |
| `REVIEWER_PSYCHOLOGY.md` | 阅读路径 | 本文补学位论文路径差异 |
