@AGENTS.md

# CLAUDE.md

Claude Code loads this file. Shared maintainer facts live in `AGENTS.md` through the import above.

## Claude Code load differences

- Install Claude Code project skills under `~/.claude/skills/<skill>/`.
- Claude Code does not natively read `AGENTS.md`. Keep the `@AGENTS.md` import as the first line of this file.
- In a new Claude Code session, run `/context` to confirm that this file and the imported `AGENTS.md` loaded. A loaded file is not a five-tool runtime verification.
- Other harnesses discover `AGENTS.md` natively or through an explicit read path. Do not treat the Claude `@AGENTS.md` import syntax as universal.

Parser copies, tests, gates, six skills, version 6.0.0, academic-use terms, and academic fact-protection rules are in `AGENTS.md`.
