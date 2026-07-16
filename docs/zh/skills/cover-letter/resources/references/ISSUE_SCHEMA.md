# 投稿信问题架构

`paper-audit/references/ISSUE_SCHEMA.md` 的简化、现场兼容变体。投稿信的发现可以通过稍后通过添加具有默认值的删除字段来通过纸质审核的深度审查整合来获取。

## 规范记录

```json
{
  "title": "short issue title",
  "quote": "exact quote from the cover letter",
  "explanation": "why this matters and what remains problematic",
  "comment_type": "claim_accuracy|journal_fit|declaration_missing|presentation|tone|disclosure_consistency",
  "severity": "major|moderate|minor",
  "source_kind": "script|llm",
  "confidence": "high|medium|low|unverified",
  "source_section": "header|opening|body|contributions|fit|declarations|closing",
  "char_offset": 128,
  "manuscript_section_anchor": "abstract|introduction|results|conclusion|none",
  "evidence_anchor": [
    {
      "type": "citation|figure_or_table|metric|section|analysis_artifact|missing",
      "text": "visible anchor in manuscript"
    }
  ],
  "claim_strength": "unsupported|observed|supported|strong",
  "missing_evidence": ["specific support that is absent or unverified"],
  "allowed_wording": "bounded wording that stays within the evidence",
  "forbidden_wording": [
    "unbounded wording that would require stronger evidence"
  ],
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

## 可选字段

- `confidence` — 高/中/低/未验证；当无法找到投稿信报价时，降级为 `unverified`。
- `source_section` — 问题位于信件的哪个逻辑部分；确定性声明映射会发出
  `header`、`opening`、`body` 或 `closing`，语义通道也可以使用
  `contributions`、`fit` 或 `declarations`。
- `char_offset` — 声明在所分析信件文本中的零基字符偏移量；无法定位句子时为 `-1`。
- `manuscript_section_anchor` — 主张应得到论文稿件的哪一部分的支持； `none` 当问题是关于信件本身（例如语气）而不是权利要求与论文稿件的对齐时。
- `evidence_anchor` / `claim_strength` / `missing_evidence` / `allowed_wording` / `forbidden_wording` - 当问题涉及声明准确性时添加。遵循 `CLAIM_EVIDENCE_CONTRACT.md` 合同。
- `quote_verified` — 由 `verify_letter_against_manuscript.py` 填充。

## 丢弃与纸质审核规范

v1 中故意缺少这些字段；在引入纸质审核时添加默认值：

| 已丢弃字段 | 摄取默认值 |
| ------------------ | -------------------------------------------------------- |
| `review_lane` | `"presubmission_readiness"` |
| `root_cause_key` | 源自 `comment_type + source_section + quote hash` |
| `gate_blocker` | `false`（投稿信在 v1 中没有门模式） |
| `related_sections` | 使用 `manuscript_section_anchor` 代替 |

## 评论类型语义

- `claim_accuracy` — 信件主张不受支持或相对于论文稿件证据存在过度主张。
- `journal_fit` — 音高与目标场地的范围或等级不匹配。
- `declaration_missing` — 缺少必需的声明（请参阅模板的 `required_declarations`）。
- `presentation` — 长度、段落形状、引文波形符或其他表面形式。
- `tone` — AI 语气词、禁止短语、营销语言或结构性 AI 跟踪信号（平行开头、统一句子长度、多样化的促销词汇）。
- `disclosure_consistency`——投稿信和论文稿件在生成AI 披露方面存在分歧（一个披露，另一个保持沉默，或者两者在极性上相互矛盾）。由 `align_check.py` 发出，它读取两个文档。

## 严重性指导

- `major` — 模板的 `required` 项的 declaration_missing；公开过度声明，其中 Claim_strength 为 `unsupported`；长度超出模板硬顶≥20%； Journal_fit 判定为低。
- `moderate` — 夸大其为 `observed`，但超出了观察范围；当稿件需要时缺少可选但推荐的声明；在负载最多的子轴上，journal_fit 的判定为 MEDIUM；信件和论文稿件之间的 AI 披露不一致 (`disclosure_consistency`)。
- `minor` — 段落长度警告； AI-tone词频；薄弱的话题开头；非必需的期刊特定短语。
