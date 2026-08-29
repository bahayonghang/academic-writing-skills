# Paper-audit 段落弧线审稿契约

## 1. Scope / Trigger

修改 `paper-audit` 的 9 维 `Clarity` 五档、`section_intro_related` lane、subagent focus、
critical/section reviewer agent、`REVIEWER_PSYCHOLOGY.md` 或对应双语公开资源时，必须遵守
本文。该能力是审稿文档与 lane 的人工观察契约，不是新的脚本 finding、评分维度或
`pre_submission_readiness` 输入。

## 2. Signatures

唯一观察集合：

```python
ARC_CODES = {
    "P-ARC-LEAD",   # topic lead / opening
    "P-ARC-CLOSE",  # wrap-up / closing
    "P-ARC-LINK",   # adjacent-paragraph interface
    "P-ARC-FLAT",   # body expansion
}
```

资源同步与验证入口：

```powershell
uv run python docs/scripts/check_resource_sync.py --skill paper-audit
uv run python docs/scripts/check_resource_sync.py
uv run --extra dev python -m pytest tests/contracts/test_paragraph_arc_audit_contract.py -q
```

## 3. Contracts

- 仅 9 维 ScholarEval `Clarity` 的五档增加段落粒度观察。每档必须能从段首、段末、相邻段
  接口或段内展开直接复核；不得只写“组织较好/较差”。
- 4 维 `Clarity`、9 维 `Presentation`、全部 ScholarEval 权重及评分边界保持不变。
- `REVIEW_LANE_GUIDE.md`、`SUBAGENT_TEMPLATES.md`、critical reviewer 与 section reviewer
  必须共享上面的四项集合，并明确“缺少显式过渡词本身不等于逻辑断裂”。
- 段落弧线只进入 `section_intro_related` 等人工审稿说明；不得进入
  `pre_submission_readiness`，不得给 `audit.py`、`scholar_eval.py` 或
  `scoring_model.py` 增加 P-ARC 路由。
- Related Work 作者/年份罗列继续由 A1 所有；审稿侧不得用 `P-ARC-FLAT` 重复扣分。
- `REVIEWER_PSYCHOLOGY.md` 只能把“回读成本”写成 audit heuristic。证据必须区分：C2 是
  一个中文学位论文章节的局部复算，C3 是受控英文 fixture；目标会议/期刊适用性、跨 venue
  稳定性及实际评分影响保持 **UNVERIFIED**。
- 六个公开源资源变化时，英文 source-faithful 页面、中文译文和 manifest 哈希必须同步。

## 4. Validation & Error Matrix

| Condition | Required behavior |
| --- | --- |
| 五档只写抽象形容词 | contract test 失败；补可定位的段首/段末/接口/展开观察 |
| lane、template 或任一 reviewer agent 缺少四项之一 | exact code-set/wording contract 失败 |
| 仅因没有过渡词就判为断裂 | contract 失败；改为核对命题关系是否可恢复 |
| 4 维 Clarity 或 9 维 Presentation 变化 | snapshot contract 失败 |
| ScholarEval 权重或评分脚本变化 | protected-path/weight contract 失败 |
| P-ARC 进入 pre-submission lane | narrow-lane contract 失败 |
| 英文/中文 docs 或 manifest 漂移 | resource-sync / bilingual contract 失败 |
| 把 C3 写成真实英文论文验证 | evidence-boundary contract 失败 |

## 5. Good / Base / Bad Cases

- Good：指出具体段落的首句未表明本段对象、末句未给出收束或去向，或相邻命题关系需要
  回读；同时保留人工语义复核。
- Base：段落没有显式过渡词，但前后命题的递进、转折、因果或引用关系可恢复，不产生
  逻辑断裂 finding。
- Bad：把单个 `however/therefore` 当作充分或必要条件，把段落弧线扣分放进
  `Presentation`/pre-submission，或宣称受控 fixture 已证明真实 venue 效果。

## 6. Tests Required

- `tests/contracts/test_paragraph_arc_audit_contract.py`：五档只在 9 维 Clarity 块内匹配；
  4 维 Clarity 与 9 维 Presentation 精确快照；权重表精确关系锁。
- 同一测试必须从 C2、C3 与 audit psychology 提取所有 `P-ARC-*` 代码，再与四项集合
  精确比较；不能用只会识别四个合法代码的正则掩盖新增代码。
- lane、template 和两类 reviewer agent 都要锁定四项观察与 missing-transition 边界；
  `pre_submission_readiness` 必须保持无 P-ARC。
- `tests/skills/paper_audit/` 锁定 `section_intro_related` 调度仍会加载 focus block。
- 最终运行 paper-audit + contracts、单技能/全量资源同步、双语 contract、docs build、
  lint、typecheck 与 `just ci`，并用 `git diff --exit-code -- <protected paths>` 确认禁改面。

## 7. Wrong vs Correct

### Wrong

```text
This paragraph has no transition word, so P-ARC-LINK is broken and Clarity must lose points.
```

### Correct

```text
No explicit transition is present. Check whether the propositions still make the adjacent
relation recoverable; report a break only when the interface itself cannot be established.
```
