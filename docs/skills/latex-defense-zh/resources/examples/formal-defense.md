# Example: 30-Minute Formal Defense Deck and Question Preparation

This example uses the synthetic thesis `evals/fixtures/mini-thesis/` to show `--stage defense`, the achievements page, and defense question preparation.

## User Request

> The formal defense has only 30 minutes. Add the page of achievements obtained during the degree study, and help me prepare the questions the committee may ask.

## 1. Generate the Plan

```bash
uv run python -B $SKILL_DIR/scripts/extract_thesis.py --thesis mini-thesis --out defense-work/inventory.json
uv run python -B $SKILL_DIR/scripts/plan_deck.py --inventory defense-work/inventory.json --out defense-work/slide_plan.yaml --minutes 30 --stage defense --theme yanshan
```

Output: 45 frames, 36 content pages. Compared with the 40-minute pre-defense:

- Each research chapter goes from 10 pages to 7 pages (`method` × 2, `experiment` × 2).
- The conclusion chapter has one more page after the outlook page, `c7-achievements` ("03　攻读学位期间取得的成果", achievements during the degree study); its `hints` list the four publications in the inventory.
- The stage text on the cover is 「博士学位论文答辩」 (doctoral thesis defense); for the pre-defense it is 「博士学位论文预答辩」.

`stage` and `minutes` decide the page order when the skeleton is generated; to change them later, rerun `plan_deck.py` instead of adding or deleting frames by hand.

## 2. Achievements Page and Innovation Page

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

The number of achievements and their chapter mapping come only from the thesis publication list; the "论文" (paper) box on each research-chapter summary page comes from the plan field `paper`, and its bibliographic text is copied verbatim from the inventory.

## 3. Build and Check

```bash
uv run python -B $SKILL_DIR/scripts/build_deck.py --plan defense-work/slide_plan.yaml --inventory defense-work/inventory.json --out defense-work/deck --compile
uv run python -B $SKILL_DIR/scripts/check_deck.py --deck defense-work/deck/defense.tex --inventory defense-work/inventory.json --plan defense-work/slide_plan.yaml --json
```

Move on to the preview when the `--json` field `summary` is `{"Critical": 0, "Major": 0, "Minor": 0, "Info": 0}`.
D-STAGE checks that the deck stage matches the plan and that the defense stage has an achievements page; D-PAPER checks that the bibliographic text in the "论文" box comes from the inventory.

## 4. Defense Question Preparation

Following `agents/qa-committee-agent.md`, take the inventory and the plan as input and prepare 3–5 questions for each research chapter. One question for Chapter 3:

```text
问题：补全误差会如何影响后续预测？
类别：章间逻辑
结论：第3章的补全结果是第4章融合预测的输入，补全精度直接影响预测输入质量。
依据：3.4 节；表3-2（本章方法 RMSE 0.39、MAE 0.30）；4.1 节技术路线。
边界：论文未单独量化补全误差向预测误差的传递。
备用页：无需新页，可回到表3-2。
```

Write the 1–2 most likely questions of each page into `notes.questions` of the plan; after the rebuild they appear in the "可能提问" (possible questions) field of `notes.md`.

## 5. Out of Scope for This Skill

A formal defense often needs a page explaining the revisions made after the pre-defense and blind-review comments. This version does not generate that page; the user prepares it separately when needed.
