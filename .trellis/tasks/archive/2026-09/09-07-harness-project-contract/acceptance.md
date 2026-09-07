# C1 acceptance notes

Date: 2026-09-07. Implementer self-check only. No commit, archive, or remote workflow.

## Pre-task README diffs (out of scope)

Recorded before rewrite. These fragments stay outside C1 intended edits and remain in the working tree.

README.md:

```diff
-> Recommended models: **Claude Opus 4.6/fable5 · GPT 5.6 Sol Max/Xhigh · Gemini 3.1 PRO**
+> Recommended models: **Claude Opus 4.6 · Fable 5.1 · GPT 6 Astra · Gemini 3.8 Flash · Kimi K3 · DeepSeek V4 Pro**
```

README_CN.md line 14 (two trailing spaces kept):

```diff
-> 推荐模型：**Claude Opus 4.6/fable5 · GPT 5.6 Sol Max/Xhigh · Gemini 3.1 PRO**  
+> 推荐模型：**Claude Opus 4.6 · Fable 5.1 · GPT 6 Astra · Gemini 3.8 Flash · Kimi K3 · DeepSeek V4 Pro**  
```

Python check after C1: `README_CN.md:14` still ends with two spaces before newline.

## Command results

From repo root. Outer shell may wrap with RTK; command text is the original.

| Command | Exit | Notes |
| --- | --- | --- |
| `uv run --extra dev python -m pytest tests/contracts/test_skill_versions.py tests/contracts/test_skill_contracts.py -q` | 0 | 24 passed in 13.99s. uv rebuilt the local package after `pyproject.toml` description/classifier edit. `version = "6.0.0"` unchanged. |
| Human search `v3.0.0`, `MIT`, `pdfplumber`, `Academic Use`, `商业` in AGENTS.md, CLAUDE.md, README.md, README_CN.md, pyproject.toml | n/a | `rg` not used; equivalent search. Hits below. |
| `git diff --check` | 2 (Git) / 1 (RTK wrapper) | Expected baseline. Python scan of C1 files: only `README_CN.md:14` has trailing whitespace. `git diff --check -- AGENTS.md CLAUDE.md README.md pyproject.toml` exit 0. |

## Human search hits (allowed files)

Current claims, not stale license/version/PDF strings:

- `AGENTS.md:7` — `Academic Use Only — Not for commercial use.` (kept direction)
- `README.md:162` — `Academic Use Only — Not for commercial use.` (kept)
- `pyproject.toml:4` — description includes `Academic Use Only — Not for commercial use.` (kept direction; no license ID added)
- `README_CN.md:146` — `仅限学术用途 — 不得用于商业用途。` (kept)

Zero hits in those five files for `v3.0.0`, `MIT`, `pdfplumber`, `Antigravity`, `MIT License`.

## License decision

User direction kept: academic use, not for commercial use. MIT classifier removed. No new SPDX/license identifier and no extra legal clauses.

## UNVERIFIED

Five-tool runtime, fresh-session load, and `npx skills add` install layout were not run in this implement pass. Applicable tools are named. Those runtime checks stay UNVERIFIED.
