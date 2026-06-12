# Directory Structure

This repository is a single skill package:

- `research-paper-writing/SKILL.md`: core workflow and output contract.
- `research-paper-writing/references/`: section guides and example bank.
- `research-paper-writing/agents/openai.yaml`: agent metadata.
- `README.md` and `README_zh.md`: repository-level install and attribution docs.

Local pattern:

- Keep the section guides under `references/` and the example bank under
  `references/examples/`.
- Keep the skill entrypoint short and route detailed guidance into the section
  files.
- Keep repository-level install guidance in the README, not in the skill body.

Reference files:

- `ref/Research-Paper-Writing-Skills/README.md`
- `ref/Research-Paper-Writing-Skills/research-paper-writing/SKILL.md`
- `ref/Research-Paper-Writing-Skills/research-paper-writing/references/examples/index.md`

Avoid:

- Introducing extra runtime directories that do not belong to the single-skill
  package.
- Mixing reference examples into the top-level README.
- Moving section-specific guidance out of `references/`.
