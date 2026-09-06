# Literature Review Rewrite

## User Request

> Rewrite this literature review section from an author-year list into a thematic synthesis, but do not add citations or change formulas and labels.

## Expected Routing

- Enter the `literature` module first
- Add `logic` if the user is also concerned about the introduction funnel or chapter closure

## Expected Output

- A1/A2/A3 diagnosis
- A rewrite blueprint following `共识 -> 分歧 -> 局限 -> 空白 -> 本文切入点`
- Use the “theme cluster -> representative-study attribution -> cluster-end comparison” interface, and explain that author/method/object/result roles apply only when checking an individual study that needs detail
- Paragraph-level rewrite proposals only when the user explicitly requests them

## Synthetic Reconstruction Example

The source says, in three consecutive sentences, “Study A proposed Method Alpha and obtained Result One;
Study B proposed Method Beta and obtained Result Two; Study C proposed Method Gamma and obtained Result
Three.” Even with four roles in every sentence, this remains an author list. Reconstruct it by first stating
the theme shared by all three studies, then expanding Study B's object, method, and existing result because
it supports the key difference, and finally comparing the three studies' applicability before identifying the
unresolved problem. If the input omits Study B's author or result, mark `missing evidence` instead of guessing
from a citekey. Preserve the existing `\cite{ref_a,ref_b,ref_c}`, formulas, and labels.
