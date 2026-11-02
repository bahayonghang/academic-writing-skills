# Time Budget

This file specifies the conversion from the presentation minutes to the page count and to the seconds for each page. The default presentation duration is 40 minutes (2400 seconds). The planning script and the quality gate use the same formula. For the page roles, see [Defense Deck Framework](defense-framework.md).

## Definitions

- Content page: a page that is not `cover`, the overall TOC, a chapter TOC, `thanks`, or `backup`.
- Total frame count = content page count + chapter count + 2 (the cover, the overall TOC, the chapter TOC pages, and the thanks page).
- Scope: 15–90 minutes; at least one `research` chapter; chapter 1 is `intro`, and the last chapter is `conclusion`.

## Allocation at 40 Minutes

The page roles fall into two groups:

- Roles with a fixed count of 1 page: `challenges`, `organization`, the `intro`, `problem`, and `summary` of a research chapter, the `intro` of an application chapter, `innovation`, `outlook`, and `achievements`.
- Roles that scale with the duration (the 40-minute base count is in parentheses): `background` (2), `status` (2), `foundation` (3), `architecture` (1), and `application` (2).

| Segment               | Page role × page count × seconds per page (40 minutes)                                   | Subtotal (seconds)           |
| --------------------- | ---------------------------------------------------------------------------------------- | ---------------------------- |
| Fixed segment         | `cover` 1 × 30; overall TOC 1 × 20; chapter TOC (chapter count − 1) × 8; `thanks` 1 × 10 | 108 (7 chapters), not scaled |
| `intro` chapter       | `background` 2 × 50; `status` 2 × 50; `challenges` 1 × 50; `organization` 1 × 50         | 300                          |
| `foundation` chapter  | `foundation` 3 × 50                                                                      | 150                          |
| `application` chapter | `intro` 1 × 40; `architecture` 1 × 50; `application` 2 × 45                              | 180                          |
| `conclusion` chapter  | `innovation` 1 × 90; `outlook` 1 × 45; the defense stage adds `achievements` 1 × 45      | 135 (defense stage: 180)     |
| `research` chapter    | Each research chapter gets an equal part of the remainder R; see the formula below       | 1527 (3 research chapters)   |

## Formula

Let M be the presentation duration in minutes, k = M / 40, and r(x) = ⌊x + 0.5⌋ (round half up).

1. Page count of a scaled role = max(1, r(base count × k)).
2. Seconds of each of the `intro`, `foundation`, `application`, and `conclusion` segments = the 40-minute subtotal of that segment × k. The fixed segment does not scale.
3. Remainder R = 60M − fixed segment seconds − the sum of the segment seconds from step 2.
4. Duration of each research chapter T = R / research chapter count; page count n = max(6, r(T / 53)).
5. In a research chapter, `intro`, `problem`, and `summary` have 1 page each; `method` page count = max(2, r((n − 3) × 3 / 7)); `experiment` page count = max(1, n − 3 − `method` page count).
6. Seconds per page: for a segment that is not a research chapter, r(segment seconds / segment page count); for a research chapter, r(T / n); for the pages of the fixed segment, the values in the table above.
7. When the content page count is N, the quality gate accepts a content page range of [r(0.85N), r(1.15N)].

The sum of the page seconds should be close to 60M. The quality gate gives a notice when the deviation is more than 10%.

## Reference Values

Chapter structure: `intro`, `foundation`, three `research` chapters, `application`, and `conclusion` (7 chapters in total); the stage is predefense.

| Duration M (minutes) | Pages per research chapter n (method/experiment) | Content page count N | Content page range | Total frame count |
| -------------------- | ------------------------------------------------ | -------------------- | ------------------ | ----------------- |
| 30                   | 7 (2/2)                                          | 35                   | [30, 40]           | 44                |
| 40                   | 10 (3/4)                                         | 45                   | [38, 52]           | 54                |
| 60                   | 15 (5/7)                                         | 66                   | [56, 76]           | 75                |

Values at 40 minutes for two other cases:

- 4 research chapters and no foundation chapter (7 chapters in total): 8 pages for each research chapter, N = 44.
- Default 7-chapter structure in the defense stage: 9 pages for each research chapter, N = 43.

## Calculation Example

40 minutes, default 7-chapter structure, predefense stage:

1. k = 1. The fixed segment is 108 seconds. The `intro` chapter is 300 seconds, the `foundation` chapter is 150 seconds, the `application` chapter is 180 seconds, and the `conclusion` chapter is 135 seconds, 765 seconds in total.
2. R = 2400 − 108 − 765 = 1527 seconds; T = 1527 / 3 = 509 seconds; n = max(6, r(509 / 53)) = r(9.60) = 10.
3. `method` = max(2, r(7 × 3 / 7)) = 3; `experiment` = 10 − 3 − 3 = 4. Each page of a research chapter gets r(509 / 10) = 51 seconds.
4. N = 6 (`intro` chapter) + 3 (`foundation` chapter) + 30 (research chapters) + 4 (`application` chapter) + 2 (`conclusion` chapter) = 45; range [38, 52]; total frame count = 45 + 7 + 2 = 54.
