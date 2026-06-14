# Skill-Creator Evaluation Notes

The user explicitly requested `$skill-creator`, so implementation must follow the skill-creator loop instead of only editing Markdown.

## Required Evaluation Shape

1. Snapshot old skill before editing:
   - Suggested path: `latex-thesis-zh-workspace/skill-snapshot/`
2. Add or update eval prompts:
   - Main file: `academic-writing-skills/latex-thesis-zh/evals/evals.json`
   - Include at least one prompt using the user's actual issue wording.
3. Add or update objective assertions:
   - Expected markers: `对象`, `问题`, `方法`, `最多 5`, `小节`, `扣合`, or equivalent diagnostic labels.
   - Include a negative/no-fabrication assertion if rewrite suggestions are generated.
4. Run comparison:
   - Preferred: with updated skill vs old skill snapshot.
   - If independent subagents are unavailable in Codex inline mode, run the adapted inline workflow and save outputs under the same workspace structure.
5. Grade and aggregate:
   - Use `grading.json` with `text`, `passed`, and `evidence` fields.
   - Use `python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name latex-thesis-zh` from the skill-creator directory if the workspace shape supports it.
6. Generate human review:
   - Use `C:\Users\lyh\.skillsmanage\skills\skill-creator\eval-viewer\generate_review.py`.
   - If no browser/display is available, pass `--static <html_path>`.
7. Revise based on feedback:
   - If feedback is empty or accepted, record that explicitly.
   - If feedback identifies title suggestions as too generic or overfit, update the skill guidance and rerun the targeted eval.

## Trigger Description Optimization

After the functional heading-architecture behavior is accepted, consider running the `skill-creator` description optimization loop for `latex-thesis-zh` because the frontmatter description is the primary trigger surface.

The trigger eval corpus already exists at:

- `academic-writing-skills/latex-thesis-zh/evals/trigger_eval.json`

This task should add title-architecture coverage before any trigger optimization run.
