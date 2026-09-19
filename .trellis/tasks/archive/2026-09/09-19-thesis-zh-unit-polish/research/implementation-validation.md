# Implementation and validation — 2026-09-19

User approved the revised plan and D1–D5. `task.py start` changed this task to
`in_progress`; implementation and documentation are now written. No commit, push,
or archive has been performed.

## Delivered behavior

- `polish_unit_zh.py --plan` lists bounded subsection/paragraph coordinates and
  read-only neighbors. Large subsections expose their paragraph units; template
  scaffolding is excluded without discarding English or numeric prose.
- `--verify` compares an original unit/file with a revision, reports the eleven
  `UP-*` checks, blocks deterministic red-line drift, and keeps semantic review
  `NEEDS-LLM`. It does not generate replacement text.
- The skill router, public protocol/module/example, synthetic fixture, eval and
  trigger entries, test registries, README pair, bilingual docs and manifest are
  synchronized. Version remains `6.0.0`; description is 226 characters.

## Initial implementation validation

| Check | Result |
| --- | --- |
| New core test module | 105 passed |
| Focused routing/resource/eval/coverage tests | 93 passed |
| `just ci` | Passed all four stages; 2,095 tests passed, 2 platform skips in 165.58 seconds |
| `check_resource_sync.py --skill latex-thesis-zh` | Passed; 280 manifest entries |
| `just doc-build` | Passed; VitePress build completed in 13.33 seconds |
| Task context validation | Passed; 12 implement entries, 6 check entries |
| `git diff --check` | Passed |
| Compliant synthetic revision | Exit 0, zero findings, `PASS-SCRIPT`, `NEEDS-LLM` |
| Drift synthetic revision | Exit 1; `UP-SCOPE`, `UP-CITE`, `UP-NUM`, `UP-STRENGTH` |
| Local private sample | Exit 0, zero findings; only code/count results retained in `verify-baseline.md` |

The sandbox denied pytest temporary-directory access (`WinError 5`) and esbuild
subprocess creation (`spawn EPERM`). The same authorized checks ran with escalation;
no dependency, sandbox-policy or product workaround was introduced.

The first full test pass found one stale subsection-contract assertion expecting
the old ZH `last_updated`. It was updated to the required implementation date;
paper-audit's date and behavior remain unchanged. Ruff formatting was applied to
the three changed test registries. No unrelated failures were repaired.

## Initial independent review

A read-only `trellis-check` agent reviewed the task scope and independently
reproduced and rechecked three fixes: legal whitespace around math-environment
commands, numeric unit superscripts, and percent-comment recognition after an
even number of backslashes. Each has a regression test. Final review found no
unresolved material issue.

The review also verified six frozen script hashes against HEAD with LF
normalization, unchanged historical eval/trigger prefixes (49/53 entries), faithful
Chinese mirrors and English translations, and absence of private paths in changed
public files. New eval/trigger changes are append-only: 57 and 15 lines.

## Fable review refinements — 2026-09-19

The user supplied Fable's review and authorized further implementation. The initial
green checks above did not cover the newly identified citation/reference gaps. This
follow-up preserves the task scope and updates R2.7/R2.8/R5.6, design and spec.

| Review item | Implemented response |
| --- | --- |
| Missing biblatex citation protection | Shared citation scanner for key extraction and visible-text masking; handles the documented single/multiple citation families, optional notes, stars and initial capitals. Key drift blocks with `UP-CITE`. |
| Missing capitalized cross-references | Capital counterparts, including `Cref`, use the same protected target check and payload masking. |
| Lexical strength false positives | Explicit `--terms` spans are excluded only from strength counting; term-frequency and other checks stay active. Candidates include local context and an explicit terminology/ordinary-use caveat. Unconfigured ordinary uses can still warn. |
| Sparse CLI help | Every argument now explains its purpose, with required/exclusive inputs identified. |
| Disconnected public lists | Reference Map, routing criteria and both docs indexes keep related entries together in continuous lists. |
| Registry/smoke order | `polish` follows `claim-forward`, matching the router. |
| Python-list text differences | A-tier text renders `cite{...}` / `ref{...}` / `label{...}` or quoted values; an empty side says `无差异项`. JSON arrays remain unchanged. |
| Verification footer on plan | Text plans end with unit instructions, with no verification or semantic verdict; the JSON structure stays unchanged. |
| Ineffective hedge-loader test | A distinct YAML sentinel proves actual resource loading; missing resource/PyYAML and invalid YAML exercise fallback. |

The citation families are bounded by local biblatex declarations. Custom citation
macros and general TeX expansion are not newly supported. The strict heading
comparison and existing template-macro visibility boundary remain as designed.
No exception dictionary or new NLP dependency was added to suppress lexical cases.

| Follow-up check | Result |
| --- | --- |
| Core regression suite | 179 passed in 19.77 seconds after the independent-review fix below |
| Focused contracts, resources and smoke tests | 86 passed in 24.94 seconds |
| Owned Ruff checks | Passed |
| Core script/test Pyright | 0 errors, 0 warnings |
| Resource sync | Passed; 280 entries |
| Task context validation | Passed; 12 implement entries, 6 check entries |
| Docs build | Passed in 19.24 seconds |
| Local private sample recheck | Exit 0, `PASS-SCRIPT`, zero findings; no sample text persisted |
| Independent follow-up review | Passed after the tracked star-whitespace fix; no remaining code/docs findings |
| Full CI after all fixes | All four stages passed; 2,169 tests passed, 2 platform skips in 207.71 seconds; Pyright 0 errors / 75 existing warnings |
| Final diff whitespace check | Passed using the repository's normal line-ending settings |

The independent reviewer reproduced an additional syntax gap: LaTeX's star lookahead
skips whitespace, but the citation and reference patterns initially required an
adjacent star. The minimal fix allows whitespace before the optional star in both
patterns. Fifteen regressions failed before that fix and passed afterward. Twelve
separate review probes then confirmed correct blocking and payload masking across
single/multiple cites and capital references with spaces, newlines and comments.
The final full CI was rerun because the earlier 2,154-test run did not cover this fix.
It passed on the stable final source; no product files changed afterward. Task,
design and spec records now include the reviewed behavior and regression boundary.

## Acceptance mapping

| Criteria | Evidence |
| --- | --- |
| AC-01 / AC-02 | Nine expected subsection IDs; paragraph fallback; coordinate-only plans |
| AC-03 / AC-05 | No-op invariants, heading preservation/change tests and read-only neighbor tests |
| AC-04 / AC-06 | Executable drift fixture and opt-in term-count CLI tests |
| AC-07 | Six normalized frozen hashes plus independent HEAD comparison |
| AC-08 / AC-10 | Full CI and resource/build gates recorded above |
| AC-09 | Skill version/date/description checks |
| AC-11 / AC-12 | Attribution, private-data boundary, reference layout/link tests and resource gate |

## Evidence limits and local delivery

Both the initial and final runs' two platform-specific pytest skips are the non-Windows Unicode subprocess
tests on this Windows host. Pyright reports 0 errors and 75 warnings; warnings
were not batch-cleaned. Script checks and one local sample do not establish a
false-positive rate or independently prove semantic fidelity. Five-platform runtime
and human author acceptance remain unverified.

Fable's follow-up implementation and all required validation are complete. The
feature's source, routing, tests and resource inventory form one coupled
deliverable. Proposed local commit group: `feat(latex-thesis-zh): add unit polish verification`,
including all task-owned changes under the ZH skill, its tests/docs, the README
pair, the new spec/index entry, and this task directory. There are no unrelated
dirty paths in the inspected working tree. Files remain unstaged pending the
Phase 3.4 commit-plan confirmation; archive and journal closeout follow separately.
