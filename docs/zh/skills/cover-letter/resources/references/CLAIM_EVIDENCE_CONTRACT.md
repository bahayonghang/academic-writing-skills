# 声明-证据合同

该参考定义了当写作或审计流程需要判断论文稿件声明是否得到可见证据支持时使用的轻量级合约。这是一份咨询合同，而不是发明缺失证据的许可。

此文件的内容故意与 `paper-audit/references/CLAIM_EVIDENCE_CONTRACT.md` 和 `latex-paper-en/references/CLAIM_EVIDENCE_CONTRACT.md` 相同。保持三个副本同步可以让每个技能提供完整的合同参考，而无需交叉导入。

## 索取候选人记录

发出声明证据图时使用此形状：

```json
{
  "claim": "exact manuscript claim or proposed claim",
  "section_key": "abstract|introduction|results|discussion|conclusion|...",
  "evidence_anchor": [
    {
      "type": "citation|figure_or_table|metric|section|analysis_artifact|missing",
      "text": "visible anchor"
    }
  ],
  "claim_strength": "unsupported|observed|supported|strong",
  "missing_evidence": ["specific missing support or verification action"],
  "allowed_wording": "bounded wording that does not outrun the evidence",
  "forbidden_wording": ["wording family that requires stronger evidence"]
}
```

## 力量阶梯

| 强度 | 含义 | 安全操作 |
| ------------- | ------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| `unsupported` | 没有可见的引文、指标、图形/表格、章节或工件锚点支持该声明。        | 软化、标记缺失的证据或移除。             |
| `observed` | 局部观察或指标可见，但交叉检查或比较支持不完整。 | 保持在观察到的设置范围内。                 |
| `supported` | 至少存在一个可见锚点，但来源仍需要声明级验证。          | 仅将声明保留在锚点的范围内。        |
| `strong` | 公制加上图形/表格/工件支持可见且边界明确。                | 保留，同时保留数据集/方法/设置限制。 |

## 证据锚规则

- 引用键仅证明参考文献被引用。在检查声明支持之前，它不能证明被引用的论文支持论文稿件句子。
- 图形支持模式和比较；表格支持精确值。除非该值可读或单独制表，否则请勿使用仅包含数字的锚点来表示精确的数字声明。
- 没有数据集、基线或分析单位的指标应保留 `observed`，而不是 `strong`。
- 仅当目标部分实际包含承诺的方法、证明、数据或限制时，部分或附录引用才有用。

## 输出规则

- 报告问题时保留作者的原始声明文本。
- 切勿发明基线、p 值、消融、样本量、引文、图表或数据集。
- 当证据缺失时，明确写出缺失的证据，而不是填补空白。
- 与普遍的主张相比，更喜欢有限制的措辞，例如“在报告的环境中”或“所呈现的结果表明”。

## 投稿信专业化

对于投稿信对齐检查，声明来源是_信件_，证据来源是_论文稿件_。信中的声明必须：

1. 引用-逐字匹配论文稿件中的句子或作为紧凑的释义，**和**
2. 由该论文稿件句子附近的证据锚点（图/表/度量/部分）支持。

如果只有(1)成立而没有(2)，则分类为`observed`；如果 (1) 失败，则声明应为 `unsupported`，无论字母措辞有多强硬。
