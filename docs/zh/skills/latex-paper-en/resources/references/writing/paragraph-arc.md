# 英文论文的段落弧线复核

当复核问题涉及段落开头、段落结尾、相邻段接口或段内展开不足时，使用这一可选诊断：

```bash
uv run python -B scripts/analyze_logic.py main.tex --paragraph-arc
uv run python -B scripts/analyze_logic.py main.tex --paragraph-arc --section introduction
```

`--paragraph-arc` 是附加开关；不传时，既有 `logic` 输出逐字节不变。输出仅用于诊断：
每条 finding 都带 `[Script] P-ARC-*` 与 `Meaning-Check: NEEDS-LLM`，检查器不会生成
替换正文。

## 作用域与边界

- 候选段落至少含 40 个可见英文词；parser 排除受保护标记后，按
  `\b[A-Za-z][A-Za-z'-]*\b` 计数。
- 标题开启新的 prose segment；标题后的首段仍然参与检查。
- 公式、图、表、算法、代码和列表环境是硬边界。过滤后不得重新连接边界两侧段落。
- 摘要、结论、致谢和附录内容豁免。
- `--section` 复用既有章节解析器，不创建第二套章节模型。

## Findings

| 代码 | 可观察形态 | 人工复核问题 |
| --- | --- | --- |
| `P-ARC-LEAD` | 无判断谓词的短首句、空过渡壳、近乎纯引用首句或数值/符号首句 | 首句是否给出本段的论点、对象或问题？ |
| `P-ARC-CLOSE` | 末句未命中配置的回指或前瞻信号 | 该段是否收束论点，或建立下一段接口？ |
| `P-ARC-LINK` | 无显式承接，且端点 token Jaccard 四舍五入到 4 位后 `< 0.0200` | 两段关系是递进、转折、因果还是回指？ |
| `P-ARC-FLAT` | 单个可见句成段，或在相关工作之外仅作作者/年份罗列 | 是否需要比较、分解或解释？ |

`P-ARC-LINK` 使用严格边界：`score == 0.0200` 通过，仅 `score < 0.0200` 报告。
任一端点少于 8 个可见词时，只检查显式承接并把接口标为待复核。相关工作中的作者/年份
罗列继续由 A1 负责。

在 Introduction 与 Related Work 中，连续两个原始相邻合格段都缺少 lead 与 close 形态时，
追加一条 Minor/P2 组 finding。各单项仍为 Info/P3；任一标题、短段、豁免段、环境、列表项
或章节变化都会复位连续 run。

## 证据边界

[`paragraph-arc-terms.yaml`](paragraph-arc-terms.yaml) 中的默认词表、`N=2` 与
`tau=0.0200` 只由受控合成样例固化。仓库没有 5–10 篇目标 venue 论文语料。真实论文上的
查准率、召回率、venue 迁移能力及数值外部有效性仍为 **UNVERIFIED**。后续复审应使用作者
确认的论文，并把证据声明与 runtime 契约分开。

AXES 描述段内可能存在的角色；P-ARC 只提供复核位置。topic lead 可对应 Assertion，非平坦
段内展开可包含 eXample 或 Explanation，close 可支持 Significance，但任何形态命中都不能
证明相应语义角色真实存在。
