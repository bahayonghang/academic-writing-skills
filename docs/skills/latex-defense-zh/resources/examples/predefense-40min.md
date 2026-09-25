# Example: 40-Minute Pre-Defense Deck (One Full Round)

This example uses the synthetic thesis `evals/fixtures/mini-thesis/` (traffic flow prediction, 7 chapters). The thesis title, names, and numbers are all synthetic.

## User Request

> My PhD thesis repository is in `mini-thesis/`. Make a 40-minute pre-defense Beamer deck with the Yanshan theme. Put the output in `defense-work/`.

## 1. Extraction and Checkpoint 1

```bash
uv run python -B $SKILL_DIR/scripts/extract_thesis.py --thesis mini-thesis --out defense-work/inventory.json --json
```

Output summary (exit code 0): 7 chapters, 17 figures, 5 tables, 7 equations, 1 algorithm, 4 publications, 3 contributions, 2 outlook items; warning `W-MAIN`:
there are two main-file candidates, `document.tex` and `document_blind.tex`, and the formal version `document.tex` is selected.

Confirm with the user:

| Chapter | Chapter title (excerpt)                               | Suggested role |
| ------- | ----------------------------------------------------- | -------------- |
| 1       | Introduction                                          | `intro`        |
| 2       | ... theoretical basis and problem framework           | `foundation`   |
| 3–5     | Three research chapters                               | `research`     |
| 6       | Design and application of the traffic flow platform   | `application`  |
| 7       | Conclusion and outlook                                | `conclusion`   |

> Chapter roles as above, pre-defense stage, 40 minutes, Yanshan theme, output directory `defense-work/`. After you confirm, I generate the plan skeleton.

## 2. Plan Skeleton and Filling

```bash
uv run python -B $SKILL_DIR/scripts/plan_deck.py --inventory defense-work/inventory.json --out defense-work/slide_plan.yaml --minutes 40 --stage predefense --theme yanshan
```

Output: 54 frames, 45 content pages, 279 placeholders. Following `references/content-rules.md`, the LLM fills every `〔待填写〕` frame by frame. One frame after filling:

```yaml
- id: c3-problem
  role: problem
  layout: figure-bullets
  chapter: 3
  section: 3.2 问题描述
  takeaway: 缺失观测在时间和空间上都不规则
  bullets:
    - 缺失位置不固定，传统插值难以利用**空间相关性**
  figures:
    - label: fig:c3-missing
  notes:
    say: 图3-2给出了示例检测器的缺失模式。缺失在时间和空间上都不规则……（150–250 字）
    key: 缺失模式不规则
    transition: 下面介绍时空图构建。
    questions:
      - 缺失率多高时方法失效？
```

Filling points: the takeaway has 40 Chinese characters or fewer and does not repeat the frame title; numbers are copied from the thesis only; text fields contain no `$…$` or LaTeX commands;
each innovation is taken item by item from the conclusion chapter with its chapter number.

## 3. Outline Reading and Checkpoint 2

```bash
uv run python -B $SKILL_DIR/scripts/plan_deck.py --plan defense-work/slide_plan.yaml --outline
```

```text
13  c3-intro  3.1 引言 | 本章通过时空图卷积补全稀疏观测
14  c3-problem  3.2 问题描述 | 缺失观测在时间和空间上都不规则
15  c3-method-1  3.3 时空图卷积补全模型 | 以距离高斯核构建时空图的邻接矩阵
……
帧数 54，内容页数 45，占位符 0
```

> Please read the takeaways in page order and confirm the storyline before I build.

## 4. Build, Check, and Fix

```bash
uv run python -B $SKILL_DIR/scripts/build_deck.py --plan defense-work/slide_plan.yaml --inventory defense-work/inventory.json --out defense-work/deck --compile
uv run python -B $SKILL_DIR/scripts/check_deck.py --deck defense-work/deck/defense.tex --inventory defense-work/inventory.json --plan defense-work/slide_plan.yaml
```

A common result of the first check is speaker notes that are too short (output excerpt; line numbers and counts vary with the plan):

```text
% D-NOTES (frame=c3-intro, notes.md:<行>) [Severity: Minor] [Priority: P2]: [Script] 「说什么」115 字，内容页应为 150–250 字
% 汇总：Critical 0，Major 0，Minor <n>，Info 0；skipped：无
```

Extend the notes (with thesis facts only), rebuild with `build_deck.py --force --compile`, and check again until Critical and Major are 0; at most 3 rounds.

## 5. Preview and Checkpoint 3

```bash
uv run python -B $SKILL_DIR/scripts/render_preview.py --pdf defense-work/deck/defense.pdf --out defense-work/deck/preview
```

Look through `contact-sheet.png` page by page: each chapter TOC highlights the current chapter; all three subfigures in the subfigure grid appear; each page has at most 3 emphasis highlights; the footer does not cover the body.

Example delivery note:

> The deck has 54 pages and compiles; quality gate Critical 0, Major 0, Minor 0. Please confirm: the supervisor title and the defense date on the cover;
> the numbers on the Chapter 6 application-effect page match Table 6-1 of the thesis. The speaker notes are in `defense-work/deck/notes.md`.
