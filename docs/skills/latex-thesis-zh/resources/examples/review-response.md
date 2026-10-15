# Example: Point-by-Point Replies to Pre-Review Comments

This example uses the synthetic review reports `evals/fixtures/rebuttal/reviews/` and the synthetic thesis `evals/fixtures/rebuttal/mini-thesis/` to show the full process from reading the review reports to delivering the paste text. The completed ledger is `evals/fixtures/rebuttal/concerns-done.yaml`. The title, the concerns, and the page numbers are invented.

Scenario: the thesis repository is `$THESIS`, and the submitted version is committed to git. The user put the two review reports in `$THESIS/rebuttal/pre-review/review_results/` and must fill in the 「博士生修改说明」 (revision statement).

## User request

> The two pre-review reports are back, in rebuttal/pre-review/review_results. Sort the concerns one by one and decide how to handle each. After I change the thesis, generate replies that I can paste directly into the Word revision statement.

## 1. Read the review reports

```bash
uv run python -B $SKILL_DIR/scripts/rebuttal_intake.py --reviews $THESIS/rebuttal/pre-review/review_results --thesis $THESIS --main document.tex --stage pre-review --json
```

Output summary:

```json
{
  "reviewers": [
    {
      "id": "R1",
      "file": "评阅书1.txt",
      "grade": "A",
      "total_score": 88,
      "items": 3,
      "anchors": 6
    },
    {
      "id": "R2",
      "file": "评阅书2.txt",
      "grade": "B",
      "total_score": 85,
      "items": 2,
      "anchors": 6
    }
  ],
  "warnings": [
    {
      "code": "W-ANCHOR-MISSING",
      "message": "第3章至第5章（chapter 4） 在论文 aux 中找不到对应标签",
      "source": "评阅书2.txt"
    },
    {
      "code": "W-ANCHOR-MISSING",
      "message": "第3章至第5章（chapter 5） 在论文 aux 中找不到对应标签",
      "source": "评阅书2.txt"
    }
  ],
  "ledger_written": true
}
```

Under `$THESIS/rebuttal/pre-review/`, the script creates `responses/` (empty) and `workspace/` (`rebuttal_state.json`, `reviews/R1.md`, `reviews/R2.md`, `concerns.yaml`). The watermark lines, the footers, and the page number lines are removed, and the concerns that span more than one line are joined.

**Checkpoint R1**:

> Reviewer 1: total score 88, grade A, agrees to the defense, 3 concerns. Reviewer 2: total score 85, grade B, agrees to the defense, 2 concerns. The two W-ANCHOR-MISSING warnings occur because chapters 4 and 5, between 「第3章至第5章」 (chapters 3 to 5), have no chapter labels in the synthetic thesis. They do not affect the next steps.
> Please confirm: the order of R1 and R2 agrees with the numbers of the original review reports, and the base commit is the submitted version.

The user confirms.

## 2. Split the concerns and decide the handling actions

Item 3 of reviewer 1 contains four independent requests. By the split rules in [Response Workflow](../references/rebuttal-workflow.md), the item becomes `R1-3a` (abbreviations), `R1-3b` (figure 2-1), `R1-3c` (reference [3]), and `R1-3d` (link between chapters). Each `quote` is a verbatim substring of the original text. `R1-3a` and `R2-2` both concern section 2.3, so `shared_with` links them.

| Item                           | Handling action | Reason                                                              |
| ------------------------------ | --------------- | ------------------------------------------------------------------- |
| R1-1 cross-network transfer    | future_work     | There is no data from a second network of the same type             |
| R1-2 symbols of equation (2-1) | add             | Add the symbol definitions                                          |
| R1-3a abbreviations            | revise          | Reduce the abbreviations and give the full name at the first use    |
| R1-3b figure 2-1               | revise          | Redraw the figure                                                   |
| R1-3c reference [3]            | revise          | Complete the bibliographic data                                     |
| R1-3d link between chapters    | clarify         | The introduction of chapter 3 already explains the link             |
| R2-1 complexity                | decline         | Cost measurement on hardware platforms is outside the problem scope |
| R2-2 data split                | add             | Add the difference from the split method of the compared references |

After `action`, `owner`, and `plan` are written for all items, set them to `status: planned`:

```bash
uv run python -B $SKILL_DIR/scripts/rebuttal_build.py --workspace $THESIS/rebuttal/pre-review/workspace --thesis $THESIS --plan-only
```

`workspace/revision_plan.md` groups the items by owner (drawio, latex-thesis-zh, manual, none), and `R1-3a` and `R2-2` share one row.

**Checkpoint R2**: give the revision plan to the user, and explain the reasons of `R1-1` (future_work) and `R2-1` (decline). The user approves.

## 3. Change the thesis

The user uses `latex-thesis-zh` to change the body text of chapter 2, redraws the figure, adds a detector layout figure before it, completes `references.bib`, compiles the full thesis, and commits. The new figure changes the original figure 2-1 to figure 2-2, and the later pages move by one.

As [Response Writing](../references/rebuttal-writing.md) specifies, the LLM writes the `response`, `locations`, and `evidence` of each item and sets `status: done` (the result is `evals/fixtures/rebuttal/concerns-done.yaml`).

## 4. Generate and check

```bash
uv run python -B $SKILL_DIR/scripts/rebuttal_build.py --workspace $THESIS/rebuttal/pre-review/workspace --thesis $THESIS
uv run python -B $SKILL_DIR/scripts/rebuttal_check.py --workspace $THESIS/rebuttal/pre-review/workspace --thesis $THESIS
```

```text
锚点：已解析 6 个，未解析 0 个
% 汇总：Critical 0，Major 0，Minor 0，Info 0；skipped：无
```

Excerpt of `responses/response-all.md`:

```text
意见3：写作规范方面：自定义缩写较多，影响可读性；图2-1文字过于密集；文献[3]著录信息不完整；第2章与第3章衔接不足。

（1）回复：已删除不常用的自定义缩写，其余缩写在首次出现处给出中文全称。（与评阅人2意见2一并修改）

（1）修改位置：第2.3节

（2）回复：已重绘该图，删去图中重复的说明文字并放大坐标轴标注。

（2）修改位置：原图2-1，现图2-2（第13页）

（3）回复：已补全该文献的卷号、期号与起止页码。

（3）修改位置：参考文献[3]
```

`responses/review-result.md`:

```text
总体评价 1（A）；总体评价 2（B）
```

## 5. Delivery

**Checkpoint R3**:

> Generated `responses/review-result.md`, `responses/response-all.md`, `responses/response-R1.md`, and `responses/response-R2.md`. Quality gate: Critical 0, Major 0, Minor 0, Info 0.
> How to paste: copy all of `response-all.md` into the 「博士生修改说明」 field. When the form has one field for each reviewer, copy `response-R1.md` and `response-R2.md` separately. The page numbers refer to the revised thesis. After the thesis is compiled again, run build and check again.
