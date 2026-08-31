# Paragraph Arcs in Chinese Theses

This guide turns whether a paragraph has an opening, a close, and an interface into reviewable
surface observations. The script only locates first sentences, last sentences, adjacent-paragraph
interfaces, and internal development. It does not judge whether a claim is true or rewrite prose.

## Entry Point

```bash
uv run python scripts/analyze_logic.py main.tex --paragraph-arc
uv run python scripts/analyze_logic.py main.tex --paragraph-arc --section introduction
```

`--paragraph-arc` is additive; default `logic` output stays unchanged when it is absent. `--section`
only narrows the existing section scope, while `--first-chapter` continues to serve chapter-number
semantics and does not locate paragraph arcs.

Every finding is a `[Script]` observation, defaults to Info/P3, and carries
`Meaning-Check: NEEDS-LLM`. Only three consecutive eligible paragraphs that lack both an opening
lead and a closing signal in the introduction or related work add one Minor/P2 summary observation;
the individual findings are not upgraded.

## Checking Boundary

- A paragraph must contain at least 40 Chinese characters. The first lead-in after a heading, list
  items, and paragraphs ending at a protected environment are excluded.
- Equations, figures, tables, algorithms, code, and lists are hard boundaries; `P-ARC-LINK` never
  reconnects paragraphs across a heading or one of these environments.
- `abstract`, `conclusion`, `acknowledgment`, `appendix`, `organization`, and `summary` do not enter
  paragraph-arc checking.
- The report does not copy a complete source sentence or change `\cite{}`, `\ref{}`, `\label{}`, or
  a mathematics environment.
- [`paragraph-arc-terms.yaml`](paragraph-arc-terms.yaml) is the term source of truth. If YAML is
  absent or a field is invalid, the script falls back to the equal built-in table for that field.

## Four Surface Observations

| Code | Recomputable signal | Human review question |
| --- | --- | --- |
| `P-ARC-LEAD` | The first sentence is short without a judgment predicate, an empty transition, nearly citation-only, or only values/units | Does the first sentence identify the paragraph's object, problem, or judgment? |
| `P-ARC-CLOSE` | The last sentence matches neither a retrospective nor a prospective marker | Does the last sentence close the point or establish the next interface? |
| `P-ARC-LINK` | The next paragraph has no explicit link and endpoint token Jaccard rounded to four places is `< 0.0200` | Is the relation progression, contrast, cause, or parallelism? |
| `P-ARC-FLAT` | A one-sentence paragraph, or every sentence is an author/year enumeration | Does the paragraph need comparison, explanation, or decomposition? |

`P-ARC-LINK` uses a strict comparison: `score == 0.0200` passes and only `score < 0.0200` is
reported. Jaccard is `0.0` when either token set is empty; endpoints shorter than 15 Chinese
characters use only the explicit-link test. A1 remains the owner of author enumeration in related
work, so `P-ARC-FLAT` does not duplicate that shape there.

## Three Paragraph Patterns

Paragraphs do not follow a fixed sentence-count template. The lead-development-close pattern below
describes argumentative roles; authors may adjust sentence count to the available evidence.

| Paragraph role | First-sentence task | Development task | Last-sentence task |
| --- | --- | --- | --- |
| Background | Define the research object and operating context | Present facts, constraints, or established understanding | Narrow to a condition relevant to this study |
| Problem | State a phenomenon, bottleneck, or unresolved relation | Explain its scope and the boundary of existing approaches | Derive the question to be answered |
| Solution | State the mechanism or analysis object used here | Explain input, processing, and output relations | Return to the design basis or connect the next module |

Do not turn the pattern into a first-next-final layout list. The opening should carry a judgment,
development sentences should provide evidence or explanation, and the close should complete the
paragraph's role in the thesis argument.

## Retrospective and Prospective Closes

A retrospective close answers what this paragraph showed, with forms such as therefore, hence, in
summary, or indicates. A prospective close answers what later work this result enables, such as
providing input for later parameter identification. Neither is a mandatory phrase list: a missing
marker creates a human-review prompt and cannot prove that a paragraph is incomplete.

Prefer a semantic relation over a mechanical connector at paragraph interfaces:

- Retrospective reference: `上述`, `该`, `这一`, `前述`;
- Progressive or parallel route: `在此基础上`, `另一条路线`, `另一组`, `另一方面`;
- Problem to solution: `针对上述`, `基于此`;
- Multi-chain synthesis: `综合`.

## Relationship to AXES

AXES describes Assertion, eXample, Explanation, and Significance roles inside a paragraph. P-ARC
describes their visible entry, exit, and adjacent-paragraph interfaces. They are not one-to-one:

Cross-heading subsection inheritance, handoff, and parent-section roles belong to `S-CTX-*`; its
eligibility rule intentionally keeps the first paragraph after a heading.

| AXES role | P-ARC observation surface | Boundary |
| --- | --- | --- |
| Assertion | `P-ARC-LEAD` provides a first-sentence review entry | The script does not judge whether the assertion is correct |
| eXample / Explanation | `P-ARC-FLAT` notes possibly thin development | A one-sentence paragraph can be valid; inspect its purpose |
| Significance | `P-ARC-CLOSE` observes retrospective or prospective shape | No fixed marker does not imply no significance |
| Paragraph relation | `P-ARC-LINK` observes an explicit link or lexical overlap | Low overlap cannot prove semantic disconnection |

## Original Abstract Examples

**Background**: Delayed observation of online quality variables is a basic constraint on continuous
operating decisions. Multiple sensors provide high-frequency process records, but their sampling
rhythms and label feedback are asynchronous. Hence the state representation must retain both dynamic
information and temporal correspondence.

**Problem**: Existing offline estimators depend on fixed sampling windows and struggle to cover
distribution changes after operating-mode switches. Window statistics describe local variation but
do not explain how sparse labels constrain a continuous state. This gap yields the representation
learning problem under asynchronous conditions.

**Solution**: To address this constraint, the section constructs a conditional state encoder. It
takes multiple records as input, creates a continuous representation on a unified time index, and
passes label conditions to the estimator. The representation provides input for later quality
prediction and error analysis.

These examples show roles and interfaces only; they carry no facts, data, method contributions, or
citations from a specific thesis.
