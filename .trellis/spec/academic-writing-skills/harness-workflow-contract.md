# Harness workflow contract

> Source: `09-07-five-harness-evergreen-audit` C1–C6 (2026-09-07).
> Applicable tools: Claude Code, Codex, Grok Build, Kimi Code, and OMP (Oh My Pi).
> Write approved experience here. Do not default to global Basic Memory.

## 1. Scope / Trigger

Read this spec before changing any of:

- the AGENTS / CLAUDE load chain
- pytest discovery or `just test` / `just ci`
- `paper-audit` `_run_check_script` encoding
- paper-audit install layout (sibling vs standalone)
- portable skill execution or native-vs-sequential labels
- the five-tool evidence ledger or public harness status rows

This spec is the maintainer contract. Public pages explain the same facts to
users. Skill `SKILL.md` plus `references/` remain the paper-project rule source.

## 2. Two completion states

Do not mix these labels.

| Label | Pass condition | This round (2026-09-07) |
| --- | --- | --- |
| 静态规则与隔离脚本交付 | C1–C5 product/docs/tests land; C6 ledger is complete and honest; shared gates owned by the main session | Static and isolation delivery may close after main-session `just ci` / resource sync / docs build. Completeness of the ledger is the C6 pass. |
| 五平台运行验证完成 | Each of the five tools has a captured new-session, delegation, and permissions handshake | **Not closed.** Unrun runtime stays **UNVERIFIED**. |

A local CLI install is not runtime verification. Naming a tool in AGENTS.md is
not a runtime pass.

## 3. Evidence classes

Keep three classes independent. A pass in one class does not fill another.

| Class | What counts | What does not count |
| --- | --- | --- |
| Static rules | Tracked text, workflow YAML, pytest config, skill notes, contract tests | CLI `--version`, working-copy inspect, pytest green |
| Isolation CLI | Real `audit.py` (or equivalent shipped script) on a temp layout; record exit, RUN, missing | Mocked checker maps; `npx skills add`; symlink installer |
| New session | Fresh process on that tool: load, discover, delegate, hooks trust | Current session; docs; `grok inspect` on a dirty working copy |

Unrun items stay **UNVERIFIED**. Do not mark UNVERIFIED as failed. Do not mark
UNVERIFIED as passed.

## 4. Encoding protocol (checker subprocess)

**What**: `paper-audit/scripts/audit.py` `_run_check_script` copies
`os.environ`, sets child `PYTHONIOENCODING=utf-8`, and runs `subprocess` with
`encoding="utf-8"`. Timeout 120s maps to returncode `-1`. Do not use `text=True`
with the locale codec. Do not replace decode failure with empty stdout.

**Why**: Windows PYTHONIOENCODING=utf-8 on the child without a matching parent
decode produced `UnicodeDecodeError` (GBK) then `AttributeError` on
`stdout.strip()`. Pre-fix collector (`isolated-audit-output.txt`):
checkout-stream-utf8 **exit 1**. Post-fix parent probe files (main session):
checkout-stream-utf8 wrote a complete JSON report with empty STDERR, matching
checkout-default and checkout-utf8-mode. C6 did not re-run the probe.

**Applicable tools**: all five. The protocol is in this repository's Python
checker boundary. It is not a harness setting and not a user global encoding
change.

**Exceptions**: Do not set `PYTHONIOENCODING=utf-8` on pytest itself (see
`testing-and-tooling.md`). Manuscript ingest uses `read_text_robust`, not this
pair. Do not treat `errors="replace"` on file reads as a substitute for the
subprocess pair.

**Tests**: `tests/skills/paper_audit/test_paper_audit_integration.py` must call
the shipped `_run_check_script`. Windows cases use PYTHONUTF8=0 plus
PYTHONIOENCODING=utf-8. Non-Windows cases cover the same Unicode payload.

## 5. Pytest single config / `just test` / `just ci`

**What**: `[tool.pytest.ini_options] testpaths = ["tests", "academic-writing-skills"]`
is the only discovery source. `just test` is `uv run --extra dev python -m pytest`.
`just ci` is four steps: `just check-versions`, `just lint`, `just typecheck`,
`just test`. Resource sync and VitePress build are not `just ci`.

**Why**: A root-only pytest run missed `bib-search-citation` package tests (42
items). C2 aligned default collect with `just test` at 1756, including those 42.

**Applicable tools**: all five when maintainers run gates. Hosted matrix is
written in `.github/workflows/ci.yml` (PR/push, Windows/Ubuntu, Python 3.10/3.13,
no `continue-on-error`). Hosted same-SHA matrix stays **UNVERIFIED** until a
GitHub Actions run on the current SHA exists.

**Exceptions**: Docs resource gate:
`uv run --extra dev python docs/scripts/check_resource_sync.py`.
Pyright warnings (75 on 2026-09-07) are a baseline. Do not batch-clean them.
`git diff --check` on the whole tree still reports `README_CN.md:14` trailing
spaces on the pre-existing model-recommendation line. Keep that line. Report
the baseline. Do not rewrite it to force a green diff-check.

## 6. Install sibling layout vs limited coverage

**What**: Full `.tex`/`.typ` script-backed paper-audit checks resolve sibling
writing skills from the parent of `paper-audit/`. Recommended layout keeps all
six skill directories as siblings. A paper-audit-only copy is **limited
coverage**: missing sibling scripts SKIP; existing exit/gate semantics stay.

Recorded isolation CLI (fixture `tests/fixtures/paper_audit/sample_paper.tex`,
`quick-audit --lang en --format json`):

| Layout | exit | RUN | missing |
| --- | --- | --- | --- |
| Full sibling copy of all six skill dirs | 0 | 11 | 0 |
| paper-audit only | 0 | 3 | 8 |

**Applicable tools**: all five after a manuscript install. Isolation CLI is a
shared product check, not a per-harness handshake.

**Exceptions**: `npx skills add` copy vs symlink stays **UNVERIFIED**. Do not
copy sibling scripts into `paper-audit/`. Do not change standalone exit/gate
into a new failure solely because coverage dropped.

**Tests**: `tests/skills/paper_audit/test_installed_layout.py` drives shipped
`audit.py` on temp copies.

## 7. Portable read / search / exec / delegate

**What**: Map those four needs onto the current session's tools. Claude
`allowed-tools` in `SKILL.md` frontmatter is Claude-compatible metadata. That
list is not a permission grant on Codex, Grok Build, Kimi Code, or OMP.

**Applicable tools**:

| Tool | Static rule | Runtime |
| --- | --- | --- |
| Claude Code | Frontmatter may constrain some Claude loaders | UNVERIFIED whether the session enforces the list |
| Codex, Grok Build, Kimi Code, OMP | Do not treat Claude tool names as the API | UNVERIFIED |

**Exceptions**: Script and semantic contracts must not depend on the literal
names `Read`, `Glob`, `Grep`, `Bash`, or `Task`.

## 8. Native delegated vs sequential single-agent

**What**: Use native delegated children only when the current tool actually
spawned independent children with exclusive scopes. Otherwise run the same
perspectives sequentially in one agent. Label that path `sequential single-agent`.
Do not call that path an independent panel.

`review_report.md` and `overall_assessment.txt` must state `native delegated`
or `sequential single-agent`. Sequential `CONSENSUS` is cross-perspective
agreement in this session. Deterministic script fallback must not claim that
other models or reviewer agents were called.

**Applicable tools**: all five. Live five-tool delegation stays **UNVERIFIED**.

**Exceptions**: `paper-audit/references/MODE_GUIDE.md` still says “dispatch”
without restating native vs sequential. That leftover is a follow-up. Do not
expand a closeout into a MODE_GUIDE rewrite. Until that rewrite, SKILL.md
Portable Execution and `workflow-detail.md` own the labels.

## 9. Knowledge write-back

Approved, evidenced rules go in `.trellis/spec/academic-writing-skills/`.
Public user facts go in `docs/harnesses.md` and `docs/zh/harnesses.md`.
Do not write this ledger into global Basic Memory by default.

## 10. Five-tool evidence ledger (2026-09-07)

Research-machine CLI versions (not a runtime pass): Claude Code 2.1.263,
Codex 0.153.4, Grok Build 1.0.22, Kimi Code 0.41.0, OMP (Oh My Pi) 18.1.12.

Completeness of this table is the C6 AC2 pass. Runtime greens are not required.

| Tool | Static rules | Isolation CLI | New session | Delegation | Permissions |
| --- | --- | --- | --- | --- | --- |
| Claude Code | Verified locally: `CLAUDE.md` first line `@AGENTS.md`; AGENTS.md is the shared source; six skills; version 6.0.0; academic-use kept; no current v3.0.0 / MIT / pdfplumber claims | Shared product CLI verified locally: sibling missing=0 RUN=11; standalone missing=8 RUN=3. Not a Claude install handshake. `npx`/symlink **UNVERIFIED** | **UNVERIFIED** (`/context` in a fresh Claude session) | **UNVERIFIED** | Documented 2026-09-07. `CLAUDE.md` is guidance. Blocking needs settings or a `PreToolUse` hook. Project hooks need trust. Trust handshake **UNVERIFIED** |
| Codex | Same shared AGENTS.md source. Codex loads AGENTS.md through the global → project → cwd chain (docs). Claude `@AGENTS.md` syntax is not universal | Same isolation CLI row as Claude Code | **UNVERIFIED** (fresh AGENTS chain, skills, agents, hooks) | **UNVERIFIED** | Documented 2026-09-07. Sandbox and approval come from runtime and agent config. Project hooks may need a user-level enable plus review. Handshake **UNVERIFIED** |
| Grok Build | Same shared AGENTS.md / CLAUDE.md families (docs). `grok inspect` on the **current working copy** discovered root `Agents.md` / `Claude.md` and project Trellis skills/agents. Claude-compatible hooks were disabled. That inspect is not a fresh-clone check | Same isolation CLI row as Claude Code | **UNVERIFIED** (fresh clone / fresh session). Working-copy `grok inspect` is recorded under Static rules; it does not fill this column | **UNVERIFIED** | Documented 2026-09-07. Mode, project permission, and sandbox are layered. Project hooks need `/hooks-trust`. Trust handshake **UNVERIFIED** |
| Kimi Code | Same shared AGENTS.md as reference context (docs). Agent system prompt is a separate layer | Same isolation CLI row as Claude Code | **UNVERIFIED** (project AGENTS.md, skills, agents) | **UNVERIFIED** | Documented 2026-09-07. Dispatch usually needs approval unless an allow rule or Ask When Needed applies. Handshake **UNVERIFIED** |
| OMP (Oh My Pi) | Same standalone AGENTS.md / CLAUDE.md (docs). Official also documents `.omp/AGENTS.md`. `.omp/` is absent here | Same isolation CLI row as Claude Code | A 2026-09-07 standalone `read` probe returned no skills. That probe is not an interactive session. Interactive `AGENTS.md` / `skill://` / `.omp` agents / Trellis extension **UNVERIFIED** | **UNVERIFIED** | Documented 2026-09-07. `--approval-mode`, agent tool list, spawn depth, and model role are layered. Handshake **UNVERIFIED** |

### Shared checks (not per-tool)

| Check | Status on 2026-09-07 |
| --- | --- |
| C1 project rules | Verified locally. AGENTS.md shared source; CLAUDE.md `@AGENTS.md`; academic-use kept; MIT classifier removed; version 6.0.0; six skills including cover-letter |
| C2 pytest + ci.yml | Verified locally as written. Default collect includes bib 42. Hosted same-SHA Windows/Ubuntu × 3.10/3.13 **UNVERIFIED** (no remote workflow this round) |
| C3 UTF-8 pair | Verified locally. Tests drive shipped `_run_check_script`. Pre-fix collector: checkout-stream-utf8 exit 1. Post-fix parent probe files (main session): stream-utf8 complete JSON, empty STDERR, matching default and utf8-mode. C6 did not re-run the probe |
| C4 isolation CLI | Verified locally (table in §6). `npx`/symlink **UNVERIFIED** |
| C5 portable notes | Verified as static skill text. Live five-tool delegation **UNVERIFIED** |
| Final `just ci` / resource sync / docs build | Owned by the main session after this spec write. C6 implementer does not treat those as already run |
| Paid new sessions | **UNVERIFIED** |

### UNVERIFIED list (must stay UNVERIFIED until a captured run exists)

- Claude Code / Codex / Grok Build / Kimi Code / OMP fresh session load
- Native delegation on those five tools
- Hooks trust on those five tools
- `npx skills add` copy vs symlink
- Hosted GitHub Actions Windows/Ubuntu × 3.10/3.13 on the current SHA
- Paid new sessions

## 11. Validation & Error Matrix

| Condition | Required behavior |
| --- | --- |
| Child checker emits UTF-8; parent pipe is locale/GBK | Fail closed before the C3 pair; after the pair, stdout is `str` and keeps Unicode |
| Decode failure in `_run_check_script` | Do not treat missing stdout as empty success |
| Default pytest collect misses bib-search-citation tests | Fail; `testpaths` must include `academic-writing-skills` |
| Full sibling layout missing > 0 on sample_paper quick-audit | Fail isolation smoke |
| Standalone missing ≠ 8 on that fixture | Fail the recorded limited-coverage lock; do not “fix” by changing gate semantics |
| Sequential review labeled `independent panel` | Invalid. Use `sequential single-agent` |
| Deterministic fallback claims other models were called | Invalid |
| Static or isolation pass used as five-tool runtime pass | Invalid. Keep UNVERIFIED |
| Ledger row with no run marked passed | Invalid. Write UNVERIFIED |
| Closeout writes global Basic Memory by default | Invalid. Write this spec |
| `README_CN.md:14` trailing spaces “fixed” in closeout | Invalid. That line is a baseline |

## 12. Tests required

- `tests/skills/paper_audit/test_paper_audit_integration.py`: Unicode protocol through shipped `_run_check_script`; timeout still `-1`
- `tests/skills/paper_audit/test_installed_layout.py`: full vs standalone RUN/missing locks
- `tests/contracts/test_skill_versions.py` / `test_skill_contracts.py`: version 6.0.0 and skill list
- Baseline suite must not shrink. New C3/C4 tests must keep calling shipped functions, not kwargs-only mocks
- Final `just ci`, resource sync, and `just doc-build` are the parent shared gates (main session)

## 13. Follow-ups (out of this closeout)

- Restate native vs sequential in `paper-audit/references/MODE_GUIDE.md` (C5 leftover)
- Hosted GitHub Actions matrix on the current SHA
- `npx skills add` copy vs symlink on the five tools
- Fresh-session load, native delegation, and hooks trust on the five tools
- Paid new sessions
- ZIP reproducibility, release-tag check binding, deploy-job permission split (parent non-goals)
- 75 Pyright warnings: baseline; do not batch-clean

## 14. Wrong vs Correct

```python
# Wrong: locale text pipe; UTF-8 child output can become stdout=None
result = subprocess.run(cmd, capture_output=True, text=True)

# Correct: pair child UTF-8 output with UTF-8 decode
env = dict(os.environ)
env["PYTHONIOENCODING"] = "utf-8"
result = subprocess.run(cmd, capture_output=True, encoding="utf-8", env=env, timeout=120)
```

```text
# Wrong: just test glob that diverges from pytest.ini
# Correct: just test -> uv run --extra dev python -m pytest
#          testpaths = tests, academic-writing-skills
```

```text
# Wrong: sequential same-session review called "independent panel"
# Correct: sequential single-agent; CONSENSUS is same-session agreement
```

```text
# Wrong: "五平台运行验证完成" because just ci passed
# Correct: "静态规则与隔离脚本交付"; runtime rows stay UNVERIFIED
```
