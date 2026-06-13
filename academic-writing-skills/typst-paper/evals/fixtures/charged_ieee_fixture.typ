// charged-ieee template-style fixture for typst-paper evals.
// Exercises: template title/abstract extraction (T7), template-managed layout
// (T8), @cite vs @label reconciliation (T1), three-line table, pseudocode.
#import "@preview/charged-ieee:0.1.4": ieee

#show: ieee.with(
  title: [Renewable Energy Forecasting With Graph Attention Networks],
  abstract: [
    Accurate short-term load forecasting remains challenging because demand is
    driven by weather and human behavior. We propose a graph attention model and
    evaluate it on three public datasets. The method improves forecasting
    accuracy over strong baselines while keeping inference latency low.
  ],
  index-terms: ("Forecasting", "Graph Neural Networks"),
  bibliography: bibliography("refs.bib", style: "ieee"),
)

= Introduction
Short-term forecasting is important for grid operation @hochreiter1997. However,
existing approaches struggle with spatial correlations @vaswani2017.

= Method
We propose a graph attention network. The model aggregates neighbor features
because spatial locality drives demand, which suggests that attention over the
adjacency graph captures the relevant structure.

= Experiment
We report 4.2% MAPE on dataset A, compared with 5.1% for the baseline.
On dataset B the method reaches 3.8% MAPE relative to 4.6% prior work.
Ablation over 12 runs shows the attention module contributes most of the gain.

#figure(
  image("arch.png", width: 80%),
  caption: [Graph attention architecture.],
) <fig:arch>

See @fig:arch for the architecture.

= Conclusion
We have shown that graph attention improves forecasting. The approach enables
better grid planning. A limitation is the reliance on a known adjacency graph,
and future work will relax this assumption.
