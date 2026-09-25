# Example: Polish an Abstract in Nature Style

User request:
Polish this abstract in Nature style. Keep the numbers and the citations.

Inputs:

- `input_text`: the synthetic abstract fragment below.
- `target`: `abstract`.
- `venue`: `nature` (the user gives it explicitly).

Profile selection and loading:

1. The user gives the venue explicitly, so `selection_source` is `explicit venue`. The request has no journal and no domain, so `conflicts` is empty.
2. Read only `profiles/nature.json`. Its `load_order` loads the system prompt, the style guide, the `abstract` section prompt, and the writing-rule TSV files.
3. `source_path` is `ref/nature-writing-studio/skill`. This example runs in a copy that is installed in a paper project, and that path is absent. Thus `degraded` is `true`,
   the missing source goes into `missing_evidence`, `rules_applied` and `evidence_rows` stay empty, and the skill does not use the IEEE or Elsevier rules.

Synthetic input:

```text
In this paper, we propose a novel graph model which achieves 12.5% lower error than the baseline [3], and it is very robust (see \ref{tab:main}).
```

Output example:

`text`:

```text
Here we present a graph model that lowers the error by 12.5% relative to the baseline [3] and remains robust (\ref{tab:main}).
```

`text_compact` (`render_result` takes the first 65% of the characters of the normalized text; the cut can fall inside a word):

```text
Here we present a graph model that lowers the error by 12.5% relative to the base
```

`summary`:

```json
{
  "venue": "nature",
  "profile_version": "2.0.1",
  "section": "abstract",
  "domain": null,
  "rules_applied": [],
  "patterns_used": [],
  "evidence_rows": [],
  "ai_tells_avoided": ["novel", "very"],
  "untraceable_tokens": [],
  "degraded": true,
  "selection_source": "explicit venue",
  "conflicts": [],
  "missing_evidence": ["source_path ref/nature-writing-studio/skill"],
  "protected_tokens": ["12.5%", "[3]", "\\ref{tab:main}"]
}
```

Key points:

- `12.5%`, `[3]`, and `\ref{tab:main}` stay unchanged in the output. The output adds no numbers, citations, or results.
- `ai_tells_avoided` records the removed intensifiers. This example loads no anti-AI rows, so it gives no row IDs, and `rules_applied` is empty.
- In this development repository, if `ref/nature-writing-studio/skill` exists and all required rows load, `rules_applied` and `evidence_rows` list the rows that were loaded,
  and `degraded` is `false`.
