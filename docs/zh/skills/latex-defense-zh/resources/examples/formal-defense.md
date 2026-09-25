# 示例：30 分钟正式答辩稿与提问准备

本示例以合成论文 `evals/fixtures/mini-thesis/` 为对象，演示 `--stage defense`、成果页与答辩提问准备。

## 用户请求

> 正式答辩只有 30 分钟，要加上攻读学位期间的成果页，再帮我准备评委可能问的问题。

## 1. 生成规划

```bash
uv run python -B $SKILL_DIR/scripts/extract_thesis.py --thesis mini-thesis --out defense-work/inventory.json
uv run python -B $SKILL_DIR/scripts/plan_deck.py --inventory defense-work/inventory.json --out defense-work/slide_plan.yaml --minutes 30 --stage defense --theme yanshan
```

输出：帧数 45，内容页数 36。与 40 分钟预答辩相比：

- 每个研究章从 10 页减为 7 页（`method` × 2、`experiment` × 2）。
- 结论章在展望页之后多一页 `c7-achievements`（「03　攻读学位期间取得的成果」），`hints` 列出清单中的四条成果。
- 封面阶段字样为「博士学位论文答辩」（预答辩为「博士学位论文预答辩」）。

`stage` 与 `minutes` 在生成骨架时决定页序；之后要改，重新运行 `plan_deck.py`，不要手工增删帧。

## 2. 成果页与创新点页

```yaml
- id: c7-achievements
  role: achievements
  layout: bullets
  takeaway: 攻读学位期间发表论文 3 篇、申请专利 1 项
  bullets:
    - 发表学术论文 3 篇，分别对应第 3、4、5 章
    - 申请发明专利 1 项
- id: c7-innovation
  role: innovation
  layout: cards
  bullets:
    - 针对观测稀疏导致空间相关性难以刻画的问题，提出基于时空图卷积的流量补全方法（第 3 章）
    - ……（其余两条同样逐条取自结论章）
```

成果条数与章对应只取自论文成果列表；研究章小结页的「论文」框由规划的 `paper` 字段给出，著录文本逐字取自清单。

## 3. 构建与检查

```bash
uv run python -B $SKILL_DIR/scripts/build_deck.py --plan defense-work/slide_plan.yaml --inventory defense-work/inventory.json --out defense-work/deck --compile
uv run python -B $SKILL_DIR/scripts/check_deck.py --deck defense-work/deck/defense.tex --inventory defense-work/inventory.json --plan defense-work/slide_plan.yaml --json
```

`--json` 的 `summary` 为 `{"Critical": 0, "Major": 0, "Minor": 0, "Info": 0}` 后进入预览。
D-STAGE 检查答辩稿阶段与规划一致、defense 阶段含成果页；D-PAPER 检查「论文」框著录文本来自清单。

## 4. 答辩提问准备

按 `agents/qa-committee-agent.md`，以清单与规划为输入，为每个研究章准备 3–5 问。第 3 章的一条：

```text
问题：补全误差会如何影响后续预测？
类别：章间逻辑
结论：第3章的补全结果是第4章融合预测的输入，补全精度直接影响预测输入质量。
依据：3.4 节；表3-2（本章方法 RMSE 0.39、MAE 0.30）；4.1 节技术路线。
边界：论文未单独量化补全误差向预测误差的传递。
备用页：无需新页，可回到表3-2。
```

把每页最可能的 1–2 问写入规划的 `notes.questions`，重建后出现在 `notes.md` 的「可能提问」栏。

## 5. 不在本技能范围

正式答辩常需「预答辩/盲审意见修改说明」页。本版不生成该页，需要时由用户另行准备。
