# 深入审查示例输出

输出示例：

```bash
uv run python -B "$SKILL_DIR/scripts/prepare_review_workspace.py" paper.tex --output-dir ./review_results
uv run python -B "$SKILL_DIR/scripts/audit.py" paper.tex --mode deep-review --scholar-eval
uv run python -B "$SKILL_DIR/scripts/consolidate_review_findings.py" ./review_results/paper
uv run python -B "$SKILL_DIR/scripts/verify_quotes.py" ./review_results/paper --write-back
uv run python -B "$SKILL_DIR/scripts/render_deep_review_report.py" ./review_results/paper
uv run python -B "$SKILL_DIR/scripts/render_deep_review_report.py" ./review_results/paper --style peer-review
```

---

# 深度审查报告

**纸**：`paper.tex` |**语言**：EN|**模式**：深度回顾

## 总体评价

该论文解决了一个重要问题，实证设置很重要，但核心贡献目前因三个问题而被削弱：摘要声称的收益比实验支持的更广泛，比较协议为所提出的方法提供了相对于基线的额外灵活性，并且一个附录表与标题改进数字不符。这些是可以修复的，但它们不是装饰性的。

- **专业**：3
- **中等**：2
- **次要**：2

## 主要问题

### M1：标题效率声称胜过证据
- **类型**：claim_accuracy
- **来源**：[LLM] 通过`claims_vs_evidence`
- **部分**：摘要
- **引用**：`Our method achieves state-of-the-art efficiency across long-document understanding tasks.`
- **说明**：结果表仅支持超过 8K token 的序列的此声明。对于较短的序列，最佳基线是可比较的。

### M2：比较协议不对称
- **类型**：方法论
- **来源**：[LLM] 通过`evaluation_fairness_and_reproducibility`
- **部分**：实验
- **引用**：`We tune our method over three retry runs while reporting each baseline once.`
- **解释**：这使得所提出的系统比基线有更多的成功机会，并削弱了标题比较的公平性。

## 中等问题

### O1：附录总数与标题改进不符
- **类型**：claim_accuracy
- **来源**：[LLM] 通过`notation_and_numeric_consistency`
- **部分**：附录
- **引用**：`Average gain: 12.4`
- **说明**：附录中列出的每个数据集的平均增益为不同的值。

## 修订路线图

### 优先级1
- [ ] 限定摘要和结论中的标题效率主张。
- [ ] 在对称评估条件下重新运行主要比较。

### 优先级2
- [ ] 将附录总计与标题指标进行核对。
- [ ] 添加有关该方法何时不主导基线的简短注释。
