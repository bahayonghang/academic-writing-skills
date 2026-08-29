# 英文论文段落弧线与密度换算契约

## 1. Scope / Trigger

修改 `latex-paper-en/scripts/analyze_logic.py --paragraph-arc`、英文 P-ARC 术语表、
`deai_check.py` 英文密度数据、序列词匹配或稳定 fixture 时，必须遵守本文。共享段落切分、
原始邻接、章节所有权和报告边界继承 `paragraph-arc-contract.md`；本文只记录英文差异。

## 2. Density conversion

英文可见词唯一口径是 parser 排除受保护结构后使用
`\b[A-Za-z][A-Za-z'-]*\b`。旧每篇绝对上限 `A` 转为 `2A`/万词：

```text
allowance(words) = ceil(2A * max(words, 1500) / 10000)
```

只有 5000 个可见词时 allowance 恰为 `A`；1500 和 10000 词的 allowance 分别为
`ceil(0.3A)` 和 `2A`，属于有意密度缩放。不得称为语料标定。`throat_clearing` 同理取
2.0/万词、最低额度 1。`section_factors.organization=6.6` 借用中文初值，英文有效性
保持 **UNVERIFIED**。

序列词为 `first/second/then/finally/next`。仅小写独立词计数；`FIRST`、`First` 和
`first-order` 不计。该匹配属于 EN/Typst 字节锁与 EN/ZH/Typst AST 锁；Typst 阈值数据
仍保留 `per_document`，不得随 EN 换算。

## 3. English P-ARC differences

```python
PARAGRAPH_ARC_MIN_WORDS = 40
PARAGRAPH_ARC_LINK_THRESHOLD = 0.0200
PARAGRAPH_ARC_DOUBLE_MISSING_RUN = 2
```

- 标题结束 segment，但标题后首段参与检查；不采用中文 S1 标题导语豁免。
- 专用豁免范围只有 abstract/conclusion/acknowledgment/appendix。公式、图表、算法、
  代码、列表与 item 是硬边界。
- LEAD 观察 8 词首句、过渡剥离后 6 词、引用剥离后 5 词及数值/单位形态；CLOSE、LINK、
  FLAT 的形态与公共 contract 一致。
- LINK 端点各至少 8 词时先四舍五入到 4 位再严格 `<0.0200` 报告；等于通过。短端点
  只检查显式承接并标为待人工复核。
- Related Work 作者/年份罗列继续由 A1 负责；P-ARC-FLAT 不双报。
- Introduction/Related Work 中 N=2 的原始相邻双缺失 run 才追加 Minor/P2；各单项仍为
  Info/P3。任一短段、标题、环境、豁免段、item 或 section 变化都复位。

## 4. Output and evidence

每条 finding 必须含 `[Script] P-ARC-*` 与 `Meaning-Check: NEEDS-LLM`，不得复制完整段落、
自动改写或给 `logic` 增加 rewrite contract。flag 默认关闭；
`tests/fixtures/paragraph_arc_en/baseline-before.txt` 用 `.gitattributes -text -diff` 锁定。

N、tau 与术语表只由受控 synthetic fixture 固化 runtime。没有 5-10 篇目标 venue 论文时，
真实论文查准率、召回率、跨 venue 代表性及阈值外部有效性一律 **UNVERIFIED**。

## 5. Tests and gates

- allowance truth table 覆盖每个旧 A 在 1500/5000/10000 词的数值，以及 `A` 不报、
  `A+1` 报；测试不得宣称任意长度旧行为等价。
- canonical word regex 覆盖连字符词、撇号词、缩写、公式和结构命令。
- 三副本锁覆盖小写独立序列词，显式证明 uppercase 与连字符复合词不计。
- P-ARC 覆盖四类 finding、默认基线、章节所有权、所有硬边界、原始邻接、N=2 复位、
  LINK 显式/重叠/空集/等于/小于边界及 FLAT 正反例。
- 公开资源变化后运行单技能/全量 resource sync、双语 contract、docs build、lint、
  typecheck 与 pytest。G2 只可报告 synthetic-only 人工核读，真实论文精度不升级。
