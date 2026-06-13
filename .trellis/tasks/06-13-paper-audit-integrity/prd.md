# paper-audit 学术诚信校正与编排核对

> 父任务：`06-12-five-skills-optimization`（完整审计见其 `research/paper-audit-audit.md` A1-A8）
> 优先级：P1 · 依赖：`06-13-en-family-parsers`（A8 parsers 拷贝层，本任务消费其 API）。
> A1-A7 不依赖地基，可并行。

## Goal

paper-audit 的依赖卫生与 evals 工程化是全套件最好的（无 P0 塌方），但存在一个
**学术诚信问题**（把 2 维度的 ScholarEval idea 评估框架冒名为 8 维度论文评估
依据）和一个**伪科学包装**（手设系数冒充"Ridge 回归 + 95% CI"）。本任务校正
这两项宣传与实现的脱节，修文档/契约陈旧，并对多 agent 编排主流程做一次端到端
契约核对。

## Requirements

### R1 ScholarEval 归因校正（A1 — P1，学术诚信优先）

- arXiv:2510.16234 实为评估**研究构想**的**两维度**框架（soundness + contribution），
  非 8 维度论文评估表。校正 `scripts/scholar_eval.py:5-6` docstring 与
  `references/SCHOLAR_EVAL_GUIDE.md`（及任何复述处）：
  - 诚实降级措辞——"评分维度参考 OpenReview/NeurIPS 审稿表；literature_grounding
    维度受 ScholarEval (arXiv:2510.16234) 的文献接地理念启发"；
  - 不再声称整个 8/9 维度框架"based on ScholarEval"。
- 一个强调 "never fabricate sources" 的审稿工具，自身来源归因必须准确。

### R2 scoring_model 去伪回归包装（A2 — P1）

- 现状：`models/scoring_model.json` 系数 == 加权平均权重 + 微小交互/惩罚项；
  `train()` 抛 NotImplementedError；CI 写死 0.5；却宣称"trained/trainable
  regression model""Requires numpy and scikit-learn""95% CI"、model_type="regression"。
- 择一：
  - (a)【推荐】如实改名：docstring 去"regression/trained/sklearn"措辞，
    `model_type` 改 "weighted_plus"（加权平均 + 交互/惩罚调整），CI 标注为
    启发式区间而非统计 95% CI；保留现有数值行为（向后兼容）。
  - (b) 真正实现 train()（接 OpenReview/PeerRead 标注数据）——成本高，非本任务范围。
- `--regression` flag 的帮助文本同步改为"加权评分 + 交互/惩罚调整"。

### R3 版本与契约同步（A3/A7 — P2）

- SKILL.md H1 `# Paper Audit Skill v5.1`（:17）改为 v5.2 或删版本号（frontmatter
  `version: 5.2.0` 为单源）；**这是修正既有 H1 与 frontmatter 不一致，非 bump**
  （[[skill-version-repo-synced]]）。
- `tests/test_skill_contracts.py:438` 的 `assert "# Paper Audit Skill v5.1"` 改为
  与 frontmatter version 一致校验（或直接断言 frontmatter version == pyproject），
  避免再次把陈旧版本锁死。
- 维度数表述统一：scholar_eval.py docstring "8-Dimension" 与 9 键常量
  （8 评分维 + overall）对齐为"8 评分维 + 1 计算维"或统称 9 维。

### R4 健壮性与依赖声明（A4/A5/A6 — P2）

- A5 SKILL.md 增一行 PDF 依赖声明："PDF 模式需 `pip install pymupdf`
  （enhanced 模式另需 pymupdf4llm）"。lazy import 友好提示已是正例，保留。
- A4 Tavily 改现行 `Authorization: Bearer tvly-...` 请求头（payload 去
  `api_key` 字段）；保留失败降级，meta 区分"认证失败"与"无结果"。
- A6 audit.py 用户论文首次摄入路径接入地基任务的 read_text_robust
  （utf-8→GB18030→replace）；workspace 内部 JSON 读取（utf-8 安全）不动。

### R5 多 agent 编排端到端契约核对（A8 + §5 覆盖缺口）

- 对 audit.py 主流程（prepare_review_workspace → committee/reviewer agents →
  consolidate_review_findings → synthesis → editor_in_chief）做一次端到端核对：
  每步的输入/输出文件路径自洽，SKILL.md 与 MODE_GUIDE 描述的工作流可被 Claude
  无歧义执行（哪个 agent 读哪个 workspace 文件、产出存哪、下一步如何消费）。
- 核查 references/ 的评分维度/权重是否在 SCORING_SYSTEMS.md / quality_rubrics.md /
  SCHOLAR_EVAL_GUIDE.md 多处硬编码且与 scholar_eval.py 常量一致（ZH"知识多源
  失同步"模式专查）；不一致则单源化。
- A8：地基任务落地后确认 paper-audit parsers 拷贝哈希同步、消费脚本接线，
  补多文件工程集成测试。

## Constraints

- 不改变 evals fixture 绑定（已受契约测试强制，是健康资产）。
- 不引入第三方硬依赖（pymupdf 保持 lazy + 可选）。
- parsers.py 改动一律走地基任务。
- 不 bump version（R3 是修正既有不一致）；安全边界与 never-fabricate 文案不削弱。

## Acceptance Criteria

- [ ] scholar_eval.py 与 SCHOLAR_EVAL_GUIDE.md 不再声称 8/9 维度框架"based on
      ScholarEval"；归因措辞与 arXiv:2510.16234 实际内容（2 维度 idea 评估）相符。
- [ ] scoring_model.py 去除"regression/trained/sklearn/95% CI"误导措辞，
      model_type 与帮助文本如实描述；数值行为向后兼容（现有测试不破）。
- [ ] SKILL.md H1 与 frontmatter version 一致；契约测试不再锁死陈旧版本。
- [ ] SKILL.md 声明 PDF 模式的 pymupdf 依赖。
- [ ] Tavily 用 Bearer 头；缺 pymupdf 环境对 .pdf 输入给友好提示（不裸崩）。
- [ ] 评分维度/权重在仓库内单源（多文档一致或一处权威定义）。
- [ ] 多 agent 编排主流程端到端契约核对通过（文档工作流可执行）。
- [ ] `just ci` 全绿。
