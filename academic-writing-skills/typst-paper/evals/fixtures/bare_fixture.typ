// Bare (non-template) typst-paper fixture for evals.
// Exercises: heading-based abstract (= Abstract), explicit #set page layout
// (T8 non-template path), Hayagriva (.yml) bibliography (T4), multi-section
// routing, and check_references on colon labels.
#set page(
  paper: "us-letter",
  margin: 1in,
  columns: 2,
)
// column-gutter is not a #set page parameter; use #columns(2, gutter: 0.33in)[..]

#set text(font: "Times New Roman", size: 10pt, lang: "en")
#set heading(numbering: "1.1")

#align(center)[
  #text(size: 16pt, weight: "bold")[A Bare Typst Paper on Fault Detection]
]

= Abstract
We study fault detection in industrial systems. We propose a detector and show
that it improves recall on a benchmark while keeping false alarms low.

= Introduction
Fault detection is critical for safe operation @rowling2003.

= Method
The detector thresholds reconstruction error because anomalies inflate it,
which explains the improved recall relative to prior work.

= Experiment
We report 92.1% recall and 3.2% false-alarm rate over 8 runs.
Compared with the baseline at 85.0% recall, the gain is consistent.

#figure(
  table(
    columns: 3,
    stroke: none,
    table.hline(stroke: 0.8pt),
    [*Method*], [*Recall*], [*FAR*],
    table.hline(stroke: 0.5pt),
    [Baseline], [85.0], [3.5],
    [Ours], [92.1], [3.2],
    table.hline(stroke: 0.8pt),
  ),
  caption: [Detection results.],
) <tab:results>

See @tab:results.

= Conclusion
We have shown improved detection. This enables safer monitoring. A limitation is
the single-benchmark evaluation, and future work will broaden it.

#bibliography("refs.yml")
