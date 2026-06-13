# paper-audit 审计报告（主会话内审计，2026-06-13）

> 审计对象：`academic-writing-skills/paper-audit/`（90 文件，脚本 11368 行，audit.py 单文件 116KB）。
> 方法：聚焦重点脚本全文细读（scoring_model/scholar_eval/literature_search/pdf_parser）+ 契约测试核对 +
> 临时实测 + 网络核实三项外部事实。references/ 与 audit.py 余量用定向 grep（116KB 未逐行通读——
> 见 §5 覆盖声明）。仓库零修改。
> 注：前任后台 agent 因网关 520/进程退出三次中断，本报告为主会话补做，预算所限聚焦高价值面。

## §1 外部核实结论（附来源）

1. **ScholarEval (arXiv:2510.16234) 真实存在，但被本 skill 严重误引**。论文标题
   *"ScholarEval: Research Idea Evaluation Grounded in Literature"*（2025-10-17 v1，
   2026-02-28 v2），是评估**研究构想（research idea）**的检索增强框架，只有**两个**
   评估维度：**soundness**（方法的经验有效性，靠文献检索类似应用判定）与
   **contribution**（相对前作的推进程度）。它**不是**论文评估框架，**没有**
   8/9 维度评分表。本 skill 的 `scholar_eval.py:5-6` 称"Based on ScholarEval
   (arXiv:2510.16234), provides an 8-dimension evaluation for academic papers"——
   这是把一个 2 维度的 idea 评估框架冒名为 8 维度论文评估表。真实的 8 维度
   （soundness/clarity/presentation/novelty/significance/reproducibility/ethics +
   overall）更接近 OpenReview/NeurIPS/ICLR 审稿表，与 ScholarEval 无对应关系。
   来源：https://arxiv.org/abs/2510.16234 、https://arxiv.org/html/2510.16234
2. **Tavily API 现行认证是 `Authorization: Bearer tvly-...` 请求头**，query 只放 payload；
   本 skill `literature_search.py:212-220` 用的是**已废弃的 payload `api_key` 字段**格式。
   Tavily 可能仍向后兼容，但这是 deprecated 写法，未来可能失效。
   来源：https://docs.tavily.com/documentation/api-reference/introduction 、
   https://github.com/tavily-ai/tavily-python
3. **Semantic Scholar API 现状**：本 skill `literature_search.py:65,82-89` 的实现
   （`/graph/v1/paper/search`，可选 `x-api-key` 头，429 退避重试，失败返回 `[]`）
   与 S2 现行 API 一致——无 key 走低限速、有 key 提速，**实现健康**。
   来源：https://api.semanticscholar.org/api-docs/

## §2 审计发现总表

### P0 — （无）

本 skill **未发现** EN/typst 那类"宣传功能对真实论文整体失效"或"检查器静默假通过"
的 P0 塌方。核心区别：依赖卫生与 evals 绑定显著优于姊妹 skill（见 §3）。

### P1 — 学术诚信/宣传与实现脱节

| # | 发现 | 位置(file:line) | 证据 |
|---|------|----------------|------|
| **A1** | **ScholarEval 误引（学术诚信问题）**：把 arXiv:2510.16234（2 维度 research-idea 评估框架：soundness + contribution）冒名为本 skill 的"8 维度论文评估"依据。skill 的实际维度表是 OpenReview 风格审稿表，与被引论文无对应。一个帮人审稿、强调"never fabricate"的工具自身错误归因学术来源，风险尤其讽刺 | `scripts/scholar_eval.py:5-6`；`references/SCHOLAR_EVAL_GUIDE.md`（同口径复述需核） | §1.1 论文实际只有 soundness/contribution 两维 |
| **A2** | **"Ridge 回归"名不副实——是手设系数冒充训练模型**：`models/scoring_model.json` 的 coefficients 与加权平均权重（soundness 0.18/clarity 0.13/...）**逐字节相同**，仅多了微小交互项（0.02/0.01）与惩罚项（critical -0.5、dims_below_5 -0.3）、intercept 0.5；`train()` 直接 `raise NotImplementedError`；CI 写死 `ci_width=0.5`。但 docstring 宣称"trained/trainable regression model""Requires numpy and scikit-learn"，`ScoringPrediction` 输出 `model_type="regression"` + `confidence_interval`（标称 95% CI）。`--regression` 实际产出 = 加权平均 + 固定惩罚，"回归"与"95% CI"暗示了不存在的统计学习 | `scripts/scoring_model.py:27-28,77-79,178-187`；`scripts/models/scoring_model.json` | 实读：coefficients==权重表；train 抛异常；CI 常量 |
| **A3** | **SKILL.md 版本标题陈旧，且契约测试把错误版本锁死**：frontmatter `version: "5.2.0"`（正确，对齐 pyproject）但 H1 标题 `# Paper Audit Skill v5.1`（:17 陈旧）；更糟的是 `tests/test_skill_contracts.py:438` 断言 `"# Paper Audit Skill v5.1" in skill_md`——测试主动把过时版本钉死，修标题会红测试 | `paper-audit/SKILL.md:11,17`；`tests/test_skill_contracts.py:438` | frontmatter 5.2.0 vs H1 v5.1 |

### P2 — 知识/文档/卫生

| # | 发现 | 位置(file:line) | 证据 |
|---|------|----------------|------|
| **A4** | **Tavily 用已废弃 payload `api_key` 格式**（现行为 `Authorization: Bearer`，§1.2）。失败静默返回 `[]`，用户得不到"是认证格式过时还是真无结果"的区分 | `scripts/literature_search.py:212-220` | §1.2 来源 |
| **A5** | **PDF 依赖未在 SKILL.md 声明**：description 宣传支持 `.pdf`，但 `.pdf` 路径需第三方 `pymupdf`/`pymupdf4llm`（非 stdlib、未必在用户环境）。lazy import + 友好 ImportError 是**正例**（优于 EN 的 PyYAML 裸崩），但 SKILL.md 未提"PDF 模式需 pip install pymupdf"，用户首次对 PDF 跑会撞 ImportError | `scripts/pdf_parser.py:80-85,123-128`；`SKILL.md:3`（仅 description 提 .pdf） | grep SKILL.md 无 pymupdf/pip install |
| **A6** | **audit.py 全程裸 `encoding="utf-8"` 读取，无鲁棒回退**：非 UTF-8（GBK/latin-1）论文在读取点会 UnicodeDecodeError。多数读取是 skill 自写的 workspace JSON（utf-8 安全），但用户论文首次摄入路径同样裸 utf-8。ZH 已有 `read_text_robust`，paper-audit 未跟进 | `scripts/audit.py:889,1678` 等（grep 全为 `encoding="utf-8"`，无 errors=/无 try 回退） | grep：0 处 errors=、0 处鲁棒回退 |
| **A7** | **"8-Dimension" 命名不一致**：`scholar_eval.py:5` docstring 称 "8-Dimension"，但 `SCHOLAR_EVAL_DIMENSIONS` 含 9 项（8 实质维 + overall computed），项目记忆称"9th dimension literature_grounding"。文档/常量/记忆三处对维度数说法不一 | `scripts/scholar_eval.py:5,29-39` | 常量 9 键 vs docstring "8" |
| **A8** | **parsers.py 拷贝与 EN 规范拷贝共享 split_sections 缺陷**（不深挖，已由 `06-13-en-family-parsers` 统一修复并经哈希锁同步本拷贝）。本任务只需在地基落地后确认 paper-audit 消费脚本接线正确 | `scripts/parsers.py`（哈希锁成员） | 见 en-family-parsers PRD |

## §3 确认健康、无需动的部分（显著优于 EN/typst）

- **依赖卫生优秀**：核心脚本纯 stdlib，**无 PyYAML/numpy/sklearn/requests 硬依赖**
  （与 EN/typst 的 deai_check PyYAML 裸崩形成鲜明对比）；唯一第三方依赖
  （pymupdf/pymupdf4llm）走 lazy import + 友好 ImportError，是仓内 import 降级的范本。
- **evals 已绑定真实 fixture 且受契约测试强制**：`test_skill_contracts.py:406-431`
  逐条锁定 9 个 eval 的 fixture 路径（quick_audit/gate_ieee/polish/deep_review/
  previous_* 等），`fixtures/` 目录真实存在——**EN/typst 的"evals 全空 files"模式
  在 paper-audit 不成立**，这是全套件最好的 evals 工程化。
- **literature_search.py 实现健康**：S2/arXiv/Tavily 三客户端均 stdlib urllib、
  429 指数退避、超时 15-20s、失败一律优雅返回 `[]`（不崩、不抛）；S2 与 arXiv
  端点/字段用法与现行 API 一致。
- **scoring 权重归一正确**：9 维权重和 = 1.00（含 overall 0.10）；fallback 加权平均
  排除 overall 后除以 0.90 归一正确；分数 clamp 到 [1,10]。
- **20 个 agent 文件全部被引用**（无孤儿）：editor_in_chief（5 处）、synthesis（3 处）
  为编排枢纽，committee_* 与 deep-review 小 reviewer（claims_evidence/
  evaluation_fairness/notation_consistency/section/self_consistency）各被引用。
- **i18n 集中化**：`i18n.py` 把全部用户可见字符串集中到 `t()` 查表，en/zh 双语切换
  不重复渲染逻辑——架构整洁。
- **CLI 契约受测**：`test_paper_audit_skill_argument_hint_matches_cli_contract` 校验
  SKILL.md argument-hint 与 audit.py `--help` 的 `--report-style/--focus/--format` 一致。
- **无 Gemini/google_web_search 残留**；`agents/openai.yaml` 在 v3.0 已移除
  （契约测试 `test_openai_yaml_shape` 对该缺失有显式豁免注释）。

## §4 建议修复分组

**组 A — 学术诚信与宣传校正（P1，优先）**
- A1：修正 ScholarEval 归因。两条路线择一：(a) 诚实降级措辞——"维度框架受
  ScholarEval 的 literature-grounding 理念**启发**，评分维度参考 OpenReview/NeurIPS
  审稿表"，并把 literature_grounding 维度（这才是真正呼应 ScholarEval 的部分）
  单独标注来源；(b) 若要保留"基于 ScholarEval"，必须如实说明只借鉴了
  soundness 与 literature-grounding 两点，其余维度是自构。同步改
  scholar_eval.py docstring 与 SCHOLAR_EVAL_GUIDE.md。
- A2：scoring_model.py 去"回归"包装。要么如实改名（"weighted scoring with
  interaction/penalty adjustments"，model_type 改 "weighted_plus"），删除
  "Requires numpy and scikit-learn"/95% CI 等暗示统计学习的措辞、把硬编码 CI
  标注为启发式区间；要么真正接训练数据（OpenReview/PeerRead）实现 train()。
  倾向前者（轻量、诚实）。

**组 B — 文档/契约同步（P2）**
- A3：SKILL.md H1 改 v5.2（或去掉版本号只留 frontmatter 单源），同步把
  test_skill_contracts.py:438 的断言改为 5.2 或改为校验 frontmatter version
  与 pyproject 一致（更稳健，避免再次锁死陈旧版本）。注意
  [[skill-version-repo-synced]]：单 skill 任务不 bump version，此处是修正
  H1 与 frontmatter 的**既有不一致**，非 bump。
- A5：SKILL.md 增一行"PDF 模式需 `pip install pymupdf`（enhanced 模式另需
  pymupdf4llm）"，与 Safety/Do-Not-Use 同区。
- A7：维度数表述统一为 9（8 评分维 + overall）或明确"8 实质维 + 1 计算维"。

**组 C — 健壮性（P2）**
- A4：Tavily 改 `Authorization: Bearer` 头格式（payload 去 api_key），保留失败
  降级；可在 meta 区分"认证失败"与"无结果"。
- A6：audit.py 用户论文摄入路径接入地基任务的 read_text_robust（utf-8→
  GB18030→replace），workspace 内部 JSON 读取可不动。

**组 D — 地基联动（依赖 06-13-en-family-parsers）**
- A8：地基任务落地后，确认 paper-audit 的 parsers 拷贝哈希同步、消费脚本接线，
  补多文件工程的集成测试。

**执行顺序**：A 组（诚信，纯文档+轻量代码，先做）→ B 组（文档/契约）→
C 组（健壮性）→ D 组（地基落地后收尾）。

## §5 覆盖声明（预算所限的未尽事项，留给实施任务复核）

- audit.py（116KB）只做了定向 grep（文件读取、regression 接线、editor/committee
  编排关键词），**未逐行通读**；report_generator.py（61KB）、i18n.py（26KB）、
  check_references.py（20KB）、pre_submission_check.py（18KB）只做结构性抽查。
  实施 paper-audit 子任务时应对 audit.py 的多 agent 编排主流程（prepare_review_
  workspace → committee → consolidate → synthesis → editor_in_chief）做一次
  端到端契约核对，确认每步输入/输出文件路径自洽、SKILL.md 文档的工作流可被
  Claude 无歧义执行。
- A6 的"用户论文首次摄入点"未精确定位到行（grep 显示的读取多为 workspace 文件），
  实施时需确认原始 .tex/.typ 读取处的编码处理。
- references/ 的评分维度/权重是否在 SCORING_SYSTEMS.md / quality_rubrics.md /
  SCHOLAR_EVAL_GUIDE.md 多处硬编码且与 scholar_eval.py 常量一致，未逐一比对
  （ZH 审计的"知识多源失同步"模式在此 skill 需专门一查）。
