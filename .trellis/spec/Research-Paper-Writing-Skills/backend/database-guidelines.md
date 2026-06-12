# Reference Corpus And State

There is no database. The persistent assets here are the skill metadata and the
reference corpus used by the writing workflow.

State and source-of-truth files:

- `research-paper-writing/SKILL.md` stores the workflow, global principles, and
  output contract.
- `research-paper-writing/references/*.md` stores the section-specific guidance.
- `research-paper-writing/references/examples/*.md` stores reusable writing
  patterns.
- `research-paper-writing/agents/openai.yaml` stores the agent-facing package
  metadata.
- The README files carry installation and attribution context.

Local pattern:

- Keep attribution and credits in the README, not scattered across individual
  example files.
- Keep section guides focused on writing logic, not repository history.
- Keep example files concrete and local to the section they support.

Reference files:

- `ref/Research-Paper-Writing-Skills/README.md`
- `ref/Research-Paper-Writing-Skills/research-paper-writing/SKILL.md`
- `ref/Research-Paper-Writing-Skills/research-paper-writing/references/examples/index.md`

Avoid:

- Treating the example corpus like mutable runtime state.
- Adding hidden state files that future agents would need to discover.
- Diluting attribution or credits across the section guide files.
