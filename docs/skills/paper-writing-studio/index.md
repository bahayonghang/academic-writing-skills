# `paper-writing-studio`

Venue-aware academic writing polish with a neutral fallback. It polishes or translates academic prose with one explicit profile and keeps evidence-bearing tokens unchanged.

## Use It For

- Polish one section or a full manuscript in Nature, IEEE, or Elsevier style.
- Translate Chinese academic prose into English and keep the numbers and citations.
- Polish academic English with the neutral `unspecified` profile when no venue is known.
- Report venue conflicts and missing evidence instead of guessing a profile.

## Do Not Use It For

- LaTeX or Typst formatting, compilation, templates, or fonts; use `latex-paper-en`, `latex-thesis-zh`, or `typst-paper`.
- Bibliography format checks or citation search; use `bib-search-citation`.
- Reviewer-style critique or scoring; use `paper-audit`.
- Submission cover letters; use `cover-letter`.
- Zotero writes or file output that you did not authorize.

## Profile Router

| Profile       | Use when                                                                                  | Evidence status                                                                                                         |
| ------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `nature`      | Explicit venue `nature`, or a Nature domain key                                           | Loads the rows under `ref/nature-writing-studio/skill` when that path exists; otherwise the output is marked `degraded` |
| `ieee`        | Explicit venue `ieee`, a journal in the IEEE allowlist, or an IEEE domain key             | Routing metadata only; the output is marked `degraded`                                                                  |
| `elsevier`    | Explicit venue `elsevier`, a journal in the Elsevier allowlist, or an Elsevier domain key | Routing metadata only; the output is marked `degraded`                                                                  |
| `unspecified` | No venue signal, or no safe mapping                                                       | Neutral baseline; `missing_evidence` names the missing signal                                                           |

The profile precedence is explicit venue > journal allowlist > unambiguous domain > `unspecified`.

## Minimum Inputs

- `input_text`: the prose to polish or translate.
- `target`: the section, for example `abstract`, `introduction`, `methods`, `results`, or `discussion`.
- Optional `venue`, `journal`, and `domain` hints.

## Script Entry Points

| File              | Purpose                                                                                                       |
| ----------------- | ------------------------------------------------------------------------------------------------------------- |
| `scripts/core.py` | Internal module without a CLI: `select_profile`, `canonical_section`, `protected_tokens`, and `render_result` |
| `profiles/*.json` | Load plan, section routes, mechanisms, and evidence gate for each profile                                     |

## Output Artifacts

- Inline Markdown with `text`, `text_compact`, and `summary`. The skill writes no file unless you ask for one.
- `summary` records the venue, the profile version, the section, the applied rules, the evidence rows, the protected tokens, the conflicts, the missing evidence, and the `degraded` flag.

## Portable Execution

Frontmatter `allowed-tools` is Claude-compatible metadata. It is not a mandatory permission list on other platforms. Map the read and search needs onto this session's available capabilities.

## Public Resources

### Examples

- [Rewrite an introduction for IEEE Transactions](./resources/examples/ieee-introduction-rewrite.md)
- [Polish an abstract in Nature style](./resources/examples/nature-abstract-polish.md)
- [Neutral polish without a venue](./resources/examples/unspecified-neutral-polish.md)

## Common Requests

```text
Polish this abstract in Nature style and keep the numbers and citations.
```

```text
Rewrite this IEEE Transactions introduction and keep the evidence tokens.
```

```text
Rewrite this experiments paragraph for an Elsevier process-control journal. Do not use the Nature "Here we" opening.
```

```text
There is no target journal yet. Polish this paragraph in neutral academic English and list the missing venue evidence.
```
