# Module: Experiment Review

**Trigger**: experiment, evaluation, baseline, ablation, significance, efficiency comparison

**Purpose**: Review an existing experiment or evaluation section and emit reviewer-style findings without drafting a replacement paragraph.

## Commands

```bash
uv run python -B scripts/analyze_experiment.py main.tex --section experiments
uv run python -B scripts/analyze_experiment.py main.tex --section results
```

## Review Focus

- baseline/comparator specificity
- metric and numeric evidence
- overclaiming or promotional wording
- missing ablation evidence
- missing statistical significance or variance reporting
- missing efficiency comparison
- conclusions that go beyond the evidence shown

## Raw Script Output

```latex
% EXPERIMENT (Line 42) [Severity: Major] [Priority: P1]: Comparison claim names only generic baselines; cite or name the exact comparator.
% EXPERIMENT (Line 42) [Severity: Major] [Priority: P1]: Performance claim is not tied to a concrete metric or numeric result.
```

## Skill-Layer Response

- Keep the final response in LaTeX-friendly review comment style.
- Do not rewrite the experiment section unless the user explicitly asks for revised prose.
- Never invent baselines, metrics, significance claims, or efficiency numbers.
