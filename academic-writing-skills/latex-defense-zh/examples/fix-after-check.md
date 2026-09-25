# 示例：按质量门结果修改答辩稿

本示例以合成论文 `evals/fixtures/mini-thesis/` 的 30 分钟答辩稿为对象，演示三类常见结果的修复：
D-DENSITY（过密）、D-NUM-SRC（论文外数字）、D-OVERFLOW-V（纵向溢出）。

## 用户请求

> 答辩稿检查报了 D-DENSITY、D-NUM-SRC 和 D-OVERFLOW-V，帮我修。

## 1. 检查结果

```bash
uv run python -B $SKILL_DIR/scripts/check_deck.py --deck defense-work/deck/defense.tex --inventory defense-work/inventory.json --plan defense-work/slide_plan.yaml
```

```text
% D-DENSITY (frame=c3-problem, defense.tex:186) [Severity: Minor] [Priority: P2]: [Script] 版式 figure-bullets 的要点 6 个，上限 4 个
% D-NUM-SRC (frame=c3-experiment-2, defense.tex:271) [Severity: Major] [Priority: P1]: [Script] Meaning-Check: NEEDS-LLM：数字 25 在论文全文中没有同形数字；回到论文原句核对
% D-DENSITY (frame=c4-problem, defense.tex:300) [Severity: Minor] [Priority: P2]: [Script] 可见字符 198 个，超过 180 个
% D-DENSITY (frame=c5-problem, defense.tex:394) [Severity: Minor] [Priority: P2]: [Script] 版式 figure-bullets 的要点 8 个，上限 4 个
% D-OVERFLOW-V (frame=c5-problem, defense.tex:411) [Severity: Major] [Priority: P1]: [Script] Overfull \vbox，超出 80.61697pt（defense.log:1619）
% 汇总：Critical 0，Major 2，Minor 3，Info 0；skipped：无
```

退出码 1（有 Major）。只改 `slide_plan.yaml`，不直接改 `defense.tex`。

## 2. 逐条修复

| 结果 | 原因 | 修改 |
| --- | --- | --- |
| D-NUM-SRC `c3-experiment-2` | 结论句写「RMSE 比方法 A 降低 25%」，25% 是自行计算的百分比，论文没有 | 按 NEEDS-LLM 复核：回到表3-2 原句，只用论文数字，改为「本章方法的 RMSE 与 MAE 均为三者最低」 `[LLM]` |
| D-OVERFLOW-V 与 D-DENSITY `c5-problem` | `figure-bullets` 放了 8 条要点，超出页面 80 pt | 按溢出处置顺序第 1 步删减文字：保留 2 条（「部署后数据分布发生**漂移**」「固定模型的误差随之增大」），其余移入讲稿 |
| D-DENSITY `c3-problem` | 6 条要点，版式上限 4 条 | 删减为 1–2 条核心要点 |
| D-DENSITY `c4-problem` | 5 条长要点，可见字符 198 个 | 每条压缩为一个短句：「时间粒度不一致」「空间覆盖不一致」「直接拼接会引入**噪声**」 |

删减文字仍放不下时，再依次考虑拆为两页、换版式、缩小图宽；字号不低于 `\scriptsize`。

## 3. 重建与复查

```bash
uv run python -B $SKILL_DIR/scripts/build_deck.py --plan defense-work/slide_plan.yaml --inventory defense-work/inventory.json --out defense-work/deck --force --compile
uv run python -B $SKILL_DIR/scripts/check_deck.py --deck defense-work/deck/defense.tex --inventory defense-work/inventory.json --plan defense-work/slide_plan.yaml
```

```text
% 汇总：Critical 0，Major 0，Minor 0，Info 0；skipped：无
```

一轮完成。修复循环最多 3 轮；第 3 轮后仍有 Critical 或 Major 时，列出剩余结果交用户决定。

## 4. 不能这样修

- 不把 25% 改成另一个自己算出的数字，也不把论文里没有的百分比写进讲稿。
- 不为消除 D-FIG-ALLOW 而换用论文外的图片，不重画数据图。
- 不为消除 D-EQ-SRC 或 D-TAB-SRC 而改写公式符号或表体。
- 不直接编辑 `defense.tex`：下次重建会覆盖，质量门也会以规划为准。
