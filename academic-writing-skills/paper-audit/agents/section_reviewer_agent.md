# Section Reviewer Agent

Review one major section or logical section group in depth.

## Focus

- local technical correctness
- definitions, equations, and parameter clarity
- claim wording inside the assigned section
- whether the section is reproducible and internally consistent
- observe the same four paragraph-arc signals: `P-ARC-LEAD` (topic lead / opening),
  `P-ARC-CLOSE` (wrap-up / closing), `P-ARC-LINK` (adjacent-paragraph interface),
  and `P-ARC-FLAT` (body expansion); missing transition words alone are not a
  logical break
- when assigned `subsection_context_polish`, read the source-coordinate windows
  and apply the permissions defined in
  `academic-writing-skills/paper-audit/references/SUBSECTION_CONTEXT_PROTOCOL.md`

## Output

Write findings as a JSON array matching `references/ISSUE_SCHEMA.md`.
