# Example: Revise the Deck from Quality-Gate Results

This example uses the 30-minute defense deck of the synthetic thesis `evals/fixtures/mini-thesis/` to show fixes for three common results:
D-DENSITY (too dense), D-NUM-SRC (number not in the thesis), and D-OVERFLOW-V (vertical overflow).

## User Request

> The deck check reported D-DENSITY, D-NUM-SRC, and D-OVERFLOW-V. Please fix them.

## 1. Check Results

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

Exit code 1 (Major present). Change only `slide_plan.yaml`; do not edit `defense.tex` directly.

## 2. Fix Item by Item

| Result | Cause | Change |
| --- | --- | --- |
| D-NUM-SRC `c3-experiment-2` | The takeaway says "RMSE is 25% lower than method A"; 25% is a self-computed percentage that the thesis does not contain | Review as NEEDS-LLM: go back to the source sentence of Table 3-2, use only thesis numbers, and change it to 「本章方法的 RMSE 与 MAE 均为三者最低」 (the method of this chapter has the lowest RMSE and MAE of the three) `[LLM]` |
| D-OVERFLOW-V and D-DENSITY `c5-problem` | `figure-bullets` holds 8 bullets and overflows the page by 80 pt | Apply step 1 of the overflow order, cut text: keep 2 bullets (「部署后数据分布发生**漂移**」「固定模型的误差随之增大」) and move the rest into the speaker notes |
| D-DENSITY `c3-problem` | 6 bullets; the layout limit is 4 | Cut to 1–2 core bullets |
| D-DENSITY `c4-problem` | 5 long bullets, 198 visible characters | Compress each bullet into a short phrase: 「时间粒度不一致」「空间覆盖不一致」「直接拼接会引入**噪声**」 |

When cutting text is still not enough, consider in order: split into two pages, change the layout, shrink the figure width; the font size stays at or above `\scriptsize`.

## 3. Rebuild and Recheck

```bash
uv run python -B $SKILL_DIR/scripts/build_deck.py --plan defense-work/slide_plan.yaml --inventory defense-work/inventory.json --out defense-work/deck --force --compile
uv run python -B $SKILL_DIR/scripts/check_deck.py --deck defense-work/deck/defense.tex --inventory defense-work/inventory.json --plan defense-work/slide_plan.yaml
```

```text
% 汇总：Critical 0，Major 0，Minor 0，Info 0；skipped：无
```

One round is enough here. The fix loop has at most 3 rounds; if Critical or Major results remain after round 3, list them and let the user decide.

## 4. Do Not Fix It This Way

- Do not replace 25% with another self-computed number, and do not put a percentage the thesis does not contain into the speaker notes.
- Do not switch to an image outside the thesis to clear D-FIG-ALLOW, and do not redraw data figures.
- Do not rewrite equation symbols or table bodies to clear D-EQ-SRC or D-TAB-SRC.
- Do not edit `defense.tex` directly: the next rebuild overwrites it, and the quality gate follows the plan.
