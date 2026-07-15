# Example: Joint Mainline Logic and Experiment Review

User request:
First check whether the thesis mainline closes from the introduction through the conclusion, then determine whether the experiment chapters read more like a project report than a thesis discussion.

Recommended module order:
1. `logic`
2. `experiment`

Commands:
```bash
uv run python $SKILL_DIR/scripts/analyze_logic.py main.tex
uv run python $SKILL_DIR/scripts/analyze_experiment.py main.tex
```

Note: full-document mode in `analyze_logic.py` includes the introduction funnel, chapter mainline,
and C3 introduction-conclusion closure by default. Add `--section 绪论` to focus on one chapter
(both Chinese chapter names and English keys are accepted).

Expected output:
- First identify any misalignment among the introduction, contribution origins, and conclusion.
- Then identify missing comparison, mechanism explanation, limitation discussion, and future work in experiment chapters.
- Report the two issue classes through their respective modules instead of merging them into generic “expression optimization.”
