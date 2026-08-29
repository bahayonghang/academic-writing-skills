# paper-audit 对应优化 (C4)

## Goal

把段落弧线纳入审稿侧的判据。审稿人对一篇稿子的"读得动 / 读不动"判断，
很大程度上落在"每段第一句能不能让我知道这段要说什么"上，
但当前 `Clarity` 维度的行为指标（`well-organized`、`notation consistent`）
没有落到段落粒度，评审 agent 也没有对应的观察点。

父任务：`08-29-writing-rhythm-arc`。依赖已归档的 C2 `af84e4a` / `401ee53` 与
C3 `e09675d` / `0bda6a1`（判据定型）。

## Evidence boundary

- 四项观察名及形态边界来自 C2 的中文学位论文契约与 C3 的英文 synthetic-only 契约；
  C3 没有目标 venue 的真实英文论文语料。
- 本任务只把可复核观察点写入审稿文档与 lane，不把它们写成审稿人行为的普适实证规律。
- 会议/期刊适用性、五档判据的跨 venue 稳定性和实际评分一致性均为 **UNVERIFIED**。

## Requirements

本任务需求 ID 与父任务的对应关系：

- R1：`Clarity` 行为指标落到段落粒度，`Presentation` 与九维权重不动（父任务 R3.1、R3.3）
- R2：`section_intro_related` lane 与 subagent 模板补段落弧线观察点及 DON'T（父任务 R3.2）
- R3：`REVIEWER_PSYCHOLOGY.md` 补节，术语与 C2/C3 四要素一致（父任务 R3.2）
- R4：段落弧线走文档与 lane，不新增脚本，deai trace 不流入 audit（既有判定）

### R1 Clarity / Presentation 判据落到段落粒度（父任务 R3.1、R3.3）

- R1.1 `references/quality_rubrics.md` 的 `Clarity`（13%，Source: Script）
      行为指标补入段落弧线维度。每档给出可判定的观察点，
      不是"写得好 / 写得差"这类无法复核的形容。
- R1.2 `Presentation`（8%）**不改**——它管的是版式、图表、格式，
      段落弧线属于 Clarity 而非 Presentation。避免同一现象两处扣分。
- R1.3 **不改任何维度权重**。ScholarEval 的 9 维权重已固定，本任务只改行为指标文字。

### R2 评审 lane 与 agent 提示（父任务 R3.2）

- R2.1 `references/REVIEW_LANE_GUIDE.md` 的 `section_intro_related` lane
      补段落弧线观察点——绪论与相关工作是弧线断裂最集中的位置。
- R2.2 `references/SUBAGENT_TEMPLATES.md` 对应 focus block 补 DO / DON'T：
      - DO：指出具体哪一段首句不承担论点、哪一段末句无去向
      - DON'T：不要因为段落没有显式过渡词就判为断裂
        （过渡词是手段之一，不是必要条件——这正是本次要修正的判断错误）
- R2.3 `agents/critical_reviewer_agent.md` 与 `agents/section_reviewer_agent.md`
      补一条观察点，措辞与 lane guide 一致。

### R3 REVIEWER_PSYCHOLOGY 对应（父任务 R3.2）

- R3.1 `references/REVIEWER_PSYCHOLOGY.md` 补一节：审稿人扫读时依赖段首句
      建立结构预期，段末句判断本段结论与去向。段落弧线缺失的代价是
      审稿人需要回读，回读会转化为负面印象。
- R3.2 该节需与 C2 的 `paragraph-arc-zh.md` / C3 的 `paragraph-arc.md`
      指向同一套四要素，不造第三套术语。

### R4 与 deai 的边界（既有判定，不重开）

- paper-audit 跑 deai 时**不传 `--analyze`**，deai trace **不流入** audit 评分。
  段落弧线在 audit 侧走**文档 + lane**，不走脚本 trace 通道。
- 因此本任务**不新增脚本**，不改 `audit.py` / `scholar_eval.py` / `scoring_model.py`。
- `pre_submission_readiness` lane 保持窄口径，不吸收段落弧线发现。

## 非目标

- 不改 ScholarEval 权重、不改 `scoring_model.py`。
- 不改 `Presentation` 维度。
- 不新增审稿 agent、不新增 lane。
- 不让 deai trace 流入 audit。
- 不改 4 维 NeurIPS 量表（`Quality` / `Clarity` / `Significance` / `Originality`）
  ——除非 C2/C3 定型后发现其 `Clarity` 描述与 9 维版本冲突，届时只做措辞对齐。

## Constraints

- `references/` 与 `agents/` 的现有契约分布在 `tests/skills/paper_audit/` 和
  `tests/contracts/`；需在现有所有权处扩展断言，不把锁误记为单一测试文件所有。
- 评审输出仍须匹配 `ISSUE_SCHEMA.md`。
- 不虚构审稿标准来源；C2 只提供中文学位论文局部复算证据，C3 只提供受控英文样本。
  新增说明须保留会议/期刊适用性 **UNVERIFIED**，不得声称 C3 已在 `ref/thesis` 实测。
- SKILL.md 只改 `last_updated`。
- 不改 `justfile`、`pyproject.toml`。

## Acceptance Criteria

- [x] AC1（R1） `quality_rubrics.md` 的 9 维 `Clarity` 五档各含至少一条段落粒度可判定
      观察点；4 维 `Clarity` 与 9 维 `Presentation` 未被改动。
- [x] AC2（R1、R4） ScholarEval 九维权重与 `scoring_model.py` 未被改动（diff 为空）。
- [x] AC3（R2） `REVIEW_LANE_GUIDE.md` 与 `SUBAGENT_TEMPLATES.md` 的段落弧线表述一致，
      且 DON'T 明确写出"缺过渡词不等于断裂"。
- [x] AC4（R3） `REVIEWER_PSYCHOLOGY.md` 新增节与 C2/C3 的四要素术语一致
      （可写成 contract 测试：三处文档的要素名集合相同）。
- [x] AC5（R4） `audit.py` / `scholar_eval.py` / `scoring_model.py` diff 为空。
- [x] AC6（R1、R2、R3） `just ci` 全绿；现有 paper-audit 与跨技能 contract 的所有权测试
      同步更新。
- [x] AC7（R1、R2、R3） docs/ 双语页面同步；manifest 散列更新。

## Verification record (2026-08-29)

- G1：作者已明确认可五档段落粒度观察点并批准继续。
- 独立 Phase 2.2 检查修复 lane 缺失的 missing-transition 边界，以及两处过宽/不完备的
  contract assertion；复查后无遗留 implementation finding。
- 聚焦 paragraph-arc audit 与调度测试：152 passed；paper-audit + contracts：595 passed。
- 单技能/全量资源同步通过（265 entries），双语 contract 与 docs build 通过。
- 完整 `just ci`：1641 passed；Pyright 0 errors、74 个既有 warnings。
- 目标会议/期刊适用性、跨 venue 稳定性、真实英文语料精度及实际审稿评分影响仍为
  **UNVERIFIED**。
