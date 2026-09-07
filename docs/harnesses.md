# Harnesses

Snapshot date: **2026-09-07** (Asia/Shanghai). The capability table below follows
official documentation captured on that date. A local CLI install is not runtime
verification. Unrun items stay **UNVERIFIED**.

Applicable tools: Claude Code, Codex, Grok Build, Kimi Code, and OMP (Oh My Pi).

## Two paths {#two-paths}

Keep these paths separate.

| Path | Who | Tracked entry | Do not mix in |
| --- | --- | --- | --- |
| Maintain this development repository | Project maintainers | Root `AGENTS.md`; Claude Code also loads `CLAUDE.md` | Paper-project skill copy steps, manuscript-only `SKILL.md` workflows |
| Install skills into a manuscript project | Paper skill users | Each skill `SKILL.md` plus that skill's `references/` | This repository's Trellis lifecycle, ignored harness adapter dirs, maintainer agents and hooks |

Skill packages must stay usable after copy into a manuscript repository. Do not
depend on this development repository's private absolute paths or a local global
tool config.

## Common explicit read {#explicit-read}

A new clone can load shared rules without ignored harness directories, private
absolute paths, or implied global hooks.

**Maintainer clone**

1. Open tracked `AGENTS.md`.
2. Claude Code: open tracked `CLAUDE.md`. The first line is `@AGENTS.md`. Claude
   Code does not natively read `AGENTS.md`.
3. Other tools: load `AGENTS.md` through native discovery, or open `AGENTS.md` in
   the session. Do not treat the Claude `@AGENTS.md` import syntax as universal.
4. For a skill change, open that skill's `SKILL.md`, then the routed file under
   `references/`.

**Paper skill user**

1. Open the installed skill `SKILL.md`.
2. Open the routed file under that skill's `references/` (and `templates/`,
   `examples/`, Markdown `agents/` when the skill points there).
3. If the tool does not auto-load the skill, keep the same explicit read.

Do not depend on `.claude/`, `.codex/`, `.agents/`, `.cursor/`, `.grok/`,
`.kimi-code/`, or `.omp/`. Git ignores `.claude/`, `.codex/`, `.agents/`, and
`.cursor/`. Those directories have no tracked files. `.grok/`, `.kimi-code/`, and
`.omp/` are not present in this repository.

Markdown `allowed-tools` in `SKILL.md` frontmatter is guidance for some
Claude-compatible loaders. Treat that list as a sandbox only when the current
platform enforces it.

## Evidence status {#evidence}

This round closes **static rules and isolation-script delivery**. This round
does not close **five-platform runtime verification**. Unrun runtime stays
**UNVERIFIED**.

| Check | Status on 2026-09-07 |
| --- | --- |
| `grok inspect` on the current working copy | Verified discovery of root `Agents.md` / `Claude.md` and project Trellis skills/agents. Claude-compatible hooks were disabled. The grok inspect row is not a fresh-clone check. Fresh-clone discovery stays **UNVERIFIED**. |
| Isolation CLI (`paper-audit` sibling vs standalone) | Verified locally. Full sibling layout: missing=0, RUN=11. Standalone: missing=8, RUN=3 (limited coverage). This row is not a five-tool runtime pass. |
| Claude Code new session `/context` | UNVERIFIED |
| Codex new session `AGENTS.md` chain, skills, agents, hooks | UNVERIFIED |
| Kimi Code project `AGENTS.md`, skills, agents, delegation | UNVERIFIED |
| OMP interactive `AGENTS.md`, `skill://`, `.omp` agents, Trellis extension | UNVERIFIED |
| `npx skills add` copy or symlink layout on the five tools | UNVERIFIED |
| Five-tool runtime (fresh session, delegation, hooks trust) | UNVERIFIED |
| Hosted GitHub Actions Windows/Ubuntu × Python 3.10/3.13 on the current SHA | UNVERIFIED |

Local CLI versions recorded on 2026-09-07: Claude Code 2.1.263, Codex 0.153.4,
Grok Build 1.0.22, Kimi Code 0.41.0, OMP (Oh My Pi) 18.1.12. Those versions
describe the research machine. They are not a runtime pass for this repository.

## Access matrix {#access-matrix}

| Tool | Maintainer entry | Paper-skill entry | Load method | Delegation | Permissions |
| --- | --- | --- | --- | --- | --- |
| Claude Code | Tracked `CLAUDE.md` with `@AGENTS.md` | Installed `SKILL.md`; optional project `.claude/skills/<name>/SKILL.md` | Native `CLAUDE.md`; skill body on demand | Project `.claude/agents/*.md`; `SubagentStart` / `PreToolUse` can inject context | `CLAUDE.md` is guidance. Blocking needs settings or a `PreToolUse` hook. Project hooks need trust. |
| Codex | Tracked root `AGENTS.md` (global → project → cwd chain) | Installed `SKILL.md`; project `.agents/skills` name/description first | `AGENTS.md` chain each run | `.codex/agents/*.toml`; `SubagentStart` additionalContext | Sandbox and approval come from runtime and agent config. Project hooks may need a user-level enable plus review. |
| Grok Build | `AGENTS.md` family and `CLAUDE.md` family | Installed `SKILL.md`; native `.grok/skills`; Claude skills/plugins also compatible | Official docs: both rule families | Built-in general-purpose / explore / plan plus `.grok/agents`; project hooks exist | Mode, project permission, and sandbox are layered. Project hooks need `/hooks-trust`. |
| Kimi Code | `AGENTS.md` as reference context (agent system prompt is a separate layer) | Installed `SKILL.md`; `.kimi-code/skills` and `.agents/skills` (Project > User > Extra > Built-in) | Reference context plus explicit `SKILL.md` read | Built-in coder / explore / plan; `.kimi-code/agents` and `.agents/agents`; child context | Dispatch usually needs approval unless an allow rule or Ask When Needed applies. Agent `tools` / `disallowedTools` can limit tools. |
| OMP (Oh My Pi) | Tracked standalone `AGENTS.md` / `CLAUDE.md`; official also documents `.omp/AGENTS.md` | Installed `SKILL.md`; `.omp/skills` first; `agents` provider also reads `.agents/skills` | Startup metadata; body via `skill://` | `task` tool; project `.omp/agents/*.md`; model / effort / spawns / prewalk | `--approval-mode`, agent tool list, spawn depth, and model role are layered. |

OMP here is **Oh My Pi** (`https://omp.sh/`, repository `can1357/oh-my-pi`).

## Claude Code {#claude-code}

- Maintainer: commit `CLAUDE.md`. Keep `@AGENTS.md` as the first line.
- Paper user: open the installed skill `SKILL.md`. Claude Code project skills use
  `.claude/skills/<skill>/`. That path is gitignored in this development
  repository.
- New-session check `/context` stays UNVERIFIED.
- Official sources (2026-09-07):
  [Memory / CLAUDE.md / AGENTS.md](https://code.claude.com/docs/en/memory),
  [Skills](https://code.claude.com/docs/en/skills),
  [Subagents](https://code.claude.com/docs/en/sub-agents),
  [Hooks](https://code.claude.com/docs/en/hooks).

## Codex {#codex}

- Maintainer: commit root `AGENTS.md`. Codex builds a global → project → cwd
  instruction chain.
- Paper user: open the installed skill `SKILL.md`. Project skills use
  `.agents/skills` when that tree exists. This repository gitignores `.agents/`.
- Fresh-session chain, skill discovery, and hook trigger stay UNVERIFIED.
- Official sources (2026-09-07):
  [AGENTS.md](https://developers.openai.com/codex/guides/agents-md),
  [Skills](https://developers.openai.com/codex/skills),
  [Subagents](https://developers.openai.com/codex/subagents),
  [Config reference](https://developers.openai.com/codex/config-reference).

## Grok Build {#grok-build}

- Maintainer: open `AGENTS.md`. Grok Build may also read `CLAUDE.md`.
- Paper user: open the installed skill `SKILL.md`. Native project skills use
  `.grok/skills`. That directory is absent here.
- `grok inspect` on 2026-09-07 discovered the working-copy root rule files and
  Trellis skills/agents through compatibility paths. Claude-compatible hooks
  were disabled. Fresh-clone and hook-trust checks stay UNVERIFIED.
- Official sources (page dates in docs: skills/plugins 2026-08-11, subagents
  2026-07-21; research snapshot 2026-09-07):
  [Skills, plugins, marketplaces](https://docs.x.ai/build/features/skills-plugins-marketplaces),
  [Subagents](https://docs.x.ai/build/features/subagents),
  [Permissions](https://docs.x.ai/build/features/permissions).

## Kimi Code {#kimi-code}

- Maintainer: open `AGENTS.md` as reference context.
- Paper user: open the installed skill `SKILL.md`. Project skills use
  `.kimi-code/skills` and `.agents/skills`. `.kimi-code/` is absent here.
  `.agents/` is gitignored.
- Project discovery and Agent/AgentSwarm delegation stay UNVERIFIED.
- Official sources (2026-09-07):
  [Skills](https://moonshotai.github.io/kimi-code/en/customization/skills),
  [Agents and sub-agents](https://moonshotai.github.io/kimi-code/en/customization/agents),
  [Configuration](https://moonshotai.github.io/kimi-code/en/configuration/config-files).

## OMP (Oh My Pi) {#omp}

- Maintainer: open standalone `AGENTS.md`. Official docs also describe
  `.omp/AGENTS.md`. `.omp/` is absent here.
- Paper user: open the installed skill `SKILL.md`. Startup may inject metadata
  only; read the body through `skill://` or by opening the file.
- A 2026-09-07 standalone `read` probe returned no skills. That probe is not an
  interactive-session result. Interactive discovery and Trellis extension stay
  UNVERIFIED.
- Official sources (2026-09-07):
  [Context files](https://github.com/can1357/oh-my-pi/blob/main/docs/context-files.md),
  [Skills](https://github.com/can1357/oh-my-pi/blob/main/docs/skills.md),
  [Task agent discovery](https://github.com/can1357/oh-my-pi/blob/main/docs/task-agent-discovery.md),
  [Task tool](https://github.com/can1357/oh-my-pi/blob/main/docs/tools/task.md),
  [Oh My Pi repository](https://github.com/can1357/oh-my-pi),
  [omp.sh](https://omp.sh/).

## Related pages

- [Installation](/installation) — maintainer clone versus manuscript skill install,
  including the `paper-audit` sibling layout
- [Usage](/usage) — cross-skill routing after install
