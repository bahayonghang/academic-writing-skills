# 技术设计 (C2)

## 落点与作用域

主入口为 `academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py`。复用
`_zh_loc`、`_thread_tokens`、`_section_visible_lines`、`LatexParser.extract_visible_text`
和 parser 的章节类型。新增 `paragraph_arc: bool = False` 参数及 `--paragraph-arc`；
关闭时不调用任何新逻辑。

全文模式按 parser 已识别的章节范围运行。`--section` 仅缩小到显式选择的章节；
`--first-chapter` 继续只服务既有章号语义，不参与段落弧线定位。

## 段落与 prose segment

段落边界：空行、纯注释行、`\par`、标题命令、受保护环境开闭。受保护环境包括公式、
图表、表格、算法、代码和列表。段落可见文本由 parser 提取；少于 40 个汉字不进入弧线检查。

标题或受保护环境同时结束当前 `prose_segment`。LINK 只比较同一 segment 中原始相邻的
合格段；不得删除豁免段后再 zip，避免跨标题、表格或公式形成伪相邻关系。

段落记录至少包含：`start`、`end`、`visible`、`sentences`、`section`、`segment_id`、
`is_heading_lead`、`in_item`、`ends_with_env`。

## 判据与术语表

新增 `references/writing/paragraph-arc-terms.yaml`，包含：

- `judgment_predicates`
- `empty_transitions`
- `retrospective_markers`
- `prospective_patterns`
- `explicit_link_markers`

脚本读取 YAML，缺失或无效时使用同值内置默认。`另一条路线`、`另一组`、`另一方面`、
`综合`属于显式承接标记。测试锁定 YAML 与默认值一致。

### LEAD

首句命中任一条件即报告：少于 20 汉字且无判断谓词；空过渡词剥离后少于 15 汉字；
剥离引用后少于 10 汉字且原句包含引用；去除数字、单位和标点后无汉字。

### CLOSE

末句同时缺少回指标记和前瞻模式，且段落不以受保护环境结束时报告。

### LINK

接口成立条件：后段首句包含显式标记，或
`round(jaccard(_thread_tokens(left_last), _thread_tokens(right_first)), 4) >= τ`。
任一 token 集为空时 Jaccard 为 0.0；短于 15 汉字的端点只检查显式标记。比较采用严格
`score < τ` 报告，`score == τ` 通过。

标定标签位于 `research/arc-link-labels.json`，不含正文。阈值候选为人工标签中出现的
四位小数 score；选择“正接口误报不超过预算时的最大阈值”，同阈值再以负控命中数优先。
G1 已冻结 `τ=0.0200`：正接口误报 2/11，负控命中 4/8。

### FLAT

句数为 1 时报告；全部句子命中既有作者罗列形态时报告，但 `related` 章交给 A1，避免双报。

## 豁免与严重度

以下段落不参与 P-ARC：`is_heading_lead`、`in_item`、`ends_with_env`、可见文本不足 40 汉字，
或章节类型属于 `abstract/conclusion/acknowledgment/appendix/organization/summary`。

单项 finding 默认为 Info/P3。仅 `introduction`/`related` 内连续 N 个原始相邻合格段同时
命中 LEAD+CLOSE 时追加一条 Minor/P2 汇总 finding；单项观察仍保持 Info。跨 segment、
章节边界或豁免段会重置连续计数。G1 已冻结 N=3。

## 输出契约

每条 finding 使用统一块结构，例如：

```latex
% 段落弧线（第120-134行）[Severity: Info] [Priority: P3]: [Script] P-ARC-CLOSE 末句未见收束信号
% Current: 末句位于第134行；未命中回指或前瞻标记。
% Suggested: 请人工确认本段是否需要回扣论点或建立下一段接口。
% Rationale: 该规则只观察形态信号，不判断语义完整性。
% Meaning-Check: NEEDS-LLM
```

不复制完整原句到报告，避免把私有正文扩散到日志。`logic` 模块不增加改写契约。

## 基线、标定与回滚

- 激活前在任务 research 保存受控样本与改造前输出；激活后先复制到稳定的
  `tests/fixtures/paragraph_arc/`，产品测试只读稳定 fixture。
- 私有章节只用于本地 G1/G2，提交匿名统计与散列，不提交正文。
- 回滚只需移除 `--paragraph-arc` 参数、检查调用和新增资源；默认路径无迁移。
