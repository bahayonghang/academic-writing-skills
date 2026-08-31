# 问题架构

规范模式`deep-review`发现。

```json
{
  "title": "short issue title",
  "quote": "exact quote from paper",
  "explanation": "reasoned explanation",
  "comment_type": "methodology|claim_accuracy|presentation|missing_information",
  "severity": "major|moderate|minor",
  "confidence": "high|medium|low|unverified",
  "source_kind": "script|llm",
  "source_section": "methods",
  "subsection_id": "2.1.1",
  "context_sides": ["current", "prev.tail"],
  "related_sections": ["results", "appendix"],
  "root_cause_key": "normalized-shared-key",
  "review_lane": "claims_vs_evidence",
  "evidence_anchor": [
    {"type": "citation|figure_or_table|metric|section|analysis_artifact", "text": "visible anchor"}
  ],
  "claim_strength": "unsupported|observed|supported|strong",
  "missing_evidence": ["specific support that is absent or unverified"],
  "allowed_wording": "bounded wording that stays within the evidence",
  "forbidden_wording": ["unbounded wording that would require stronger evidence"],
  "gate_blocker": false,
  "quote_verified": true
}
```

## 必填字段

- `title`
- `quote`
- `explanation`
- `comment_type`
- `severity`
- `source_kind`

## 指导

- `root_cause_key`当相同问题持续存在时，应在重新审核中保持稳定。
- `gate_blocker`仅适用于无法通过提交门的问题。
- `quote_verified`应该在运行后添加`verify_quotes.py`.
- `evidence_anchor`, `claim_strength`, `missing_evidence`, `allowed_wording`， 和
  `forbidden_wording`是可选的声明证据字段。出现问题时添加它们
与声明准确性、引文支持、图形/表格证据或数据有关
可用性。在下游消费者明确之前不要将它们设置为必需的
版本化模式。
- `confidence`遵循有序的梯子`high > medium > low > unverified`.
  `unverified`保留用于无法找到锚点引用的结果
在源中。跑步`verify_quotes.py --write-back`将降级任何问题
和`quote_verified=false`到`confidence: unverified`所以下游
合并和报告可以将其视为证据不足，而不是
默默地保留着最初的自信标签。
- `subsection_id` 与 `context_sides` 是可选的小节上下文字段。
  没有 depth-3 单元时省略 `subsection_id`。`context_sides` 是列表，取值来自
  `current`、`prev.tail`、`next.head` 与 `parent_lead`；不要使用旧的单值
  `context_side`。每条 S-CTX issue 使用 `source_kind: "llm"` 与
  `severity: "minor"`；只有汇总的 `S-CTX-IN+OUT` issue 使用 `severity: "moderate"`。

## 可选的捆绑包装

`final_issues.json`通常是上述记录的顶级列表
（遗留模式，仍然是默认生成的`consolidate_review_findings.py`).
对于重新审核分数跟踪，它可能是包含相同列表的字典
以及可选的轮级元数据：

```json
{
  "issues": [ /* records as defined above */ ],
  "round_scores": {
    "quality": 78,
    "clarity": 73,
    "significance": 70,
    "originality": 75
  }
}
```

- `issues`使用dict形式时需要；消费者又回到了
如果不存在则为空列表。
- `round_scores`是可选的。键是自由格式的维度名称（
4 维摘要或 9 维 ScholarEval 层都可以工作）。
值必须是数字。
- `scripts/diff_review_issues.py`和`scripts/render_revision_trajectory.py`
自动检测 dict 形式。当两个包都没有暴露时
  `round_scores`，轨迹渲染被默默地跳过而不是出错。
