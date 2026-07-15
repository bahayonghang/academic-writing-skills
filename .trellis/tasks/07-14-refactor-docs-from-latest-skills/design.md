# 双语文档重构设计

## 1. Design Summary

文档站采用统一、可推导的资源路径，将技能包中的 250 个公开资源映射成 500 个
英文/中文资源文件。人工维护技能概览与译文；自动工具维护资源清单并检查源文件、
路径、双语结构和不可翻译 token 的一致性。父任务不直接批量翻译，子任务按共享
契约逐技能交付。

## 2. Source Boundary

对每个 `academic-writing-skills/<skill>/`：

- `references/**/*.{md,yaml,yml}` -> public resources
- `templates/**/*.md` -> public resources
- `examples/**/*.md` -> public resources
- `agents/**/*.md` -> public only when it is a human-readable agent contract
- `SKILL.md` -> source for the hand-authored skill overview, not copied as a resource
- `scripts/`, `evals/`, tests, fixtures, `agents/openai.yaml` -> excluded

Current inventory:

| Skill | References | Templates | Examples | Agent Markdown | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| `bib-search-citation` | 3 | 0 | 3 | 0 | 6 |
| `cover-letter` | 8 | 10 | 4 | 2 | 24 |
| `latex-paper-en` | 53 | 5 | 7 | 0 | 65 |
| `latex-thesis-zh` | 39 | 4 | 5 | 0 | 48 |
| `paper-audit` | 31 | 3 | 4 | 19 | 57 |
| `typst-paper` | 42 | 3 | 5 | 0 | 50 |
| **Total** | **176** | **25** | **28** | **21** | **250** |

Inventory is computed at implementation time; these counts are planning evidence, not constants to
hard-code in the checker.

## 3. Target Information Architecture

```text
docs/
├─ skills/<skill>/
│  ├─ index.md
│  └─ resources/
│     ├─ references/<source-relative-path>
│     ├─ templates/<source-relative-path>
│     ├─ examples/<source-relative-path>
│     └─ agents/<source-relative-path>
├─ zh/skills/<skill>/
│  ├─ index.md
│  └─ resources/{references,templates,examples,agents}/...
├─ resource-manifest.json
└─ scripts/check_resource_sync.py
```

The source-relative filename and case are preserved. Existing non-uniform resource paths are
removed. No redirect or compatibility copy is retained.

## 4. Manifest Contract

`docs/resource-manifest.json` records one row per source resource:

```json
{
  "skill": "latex-thesis-zh",
  "kind": "references",
  "source": "academic-writing-skills/latex-thesis-zh/references/writing/conclusion-guide-zh.md",
  "sourceLocale": "zh",
  "sourceSha256": "...",
  "en": "docs/skills/latex-thesis-zh/resources/references/writing/conclusion-guide-zh.md",
  "zh": "docs/zh/skills/latex-thesis-zh/resources/references/writing/conclusion-guide-zh.md"
}
```

`sourceLocale` is assigned per file, not per skill, because several resources are bilingual or use
a language different from the skill's primary language. Language-neutral YAML is marked `neutral`.

The checker derives the expected source inventory independently, so deleting a manifest row cannot
hide a newly added public source file.

## 5. Localization Contract

- For `sourceLocale=en`, the English page remains source-faithful and the Chinese page is translated.
- For `sourceLocale=zh`, the Chinese page remains source-faithful and the English page is translated.
- For `sourceLocale=neutral`, both copies are byte-identical to the source.
- Mixed-language files are normalized for the target locale while preserving quoted source text when
  the quote's language is semantically relevant.
- Markdown heading levels, list nesting, table column counts, admonitions and section order stay aligned.
- Fenced code, commands, paths, filenames, CLI flags, formulas, citation keys, identifiers, standard
  numbers and frontmatter keys stay unchanged.
- Link labels are translated; relative targets are rewritten only as required by the uniform mirrored
  tree and must resolve within the same locale.
- Translation must not weaken MUST/禁止/required constraints or invent capabilities, evidence or policy.

## 6. Overview And Core Pages

Skill `index.md` pages remain curated rather than generated. Each follows the same shape:

1. use it for / do not use it for;
2. module or mode router;
3. minimum inputs;
4. first commands and script entry points;
5. output artifacts;
6. public resource groups;
7. common requests and adjacent-skill handoffs.

Home, installation, quick-start, usage and skill-index pages are reviewed against all six current
`SKILL.md` contracts. They link only to the new resource hierarchy.

## 7. Navigation

`docs/.vitepress/config.ts` keeps manually curated top-level skill groups and overview labels, but
resource subtrees are discovered from each locale's filesystem. The generator:

- groups by `references`, `templates`, `examples` and `agents`;
- recursively nests directories;
- uses the translated page H1 as the item label with a filename fallback;
- excludes YAML and other non-page assets from page links while leaving them downloadable;
- sorts deterministically and preserves exact filename case;
- emits collapsed groups so the large inventory remains usable.

This removes the current 100+ manual resource links and makes newly synced pages visible by default.

## 8. Automated Verification

`docs/scripts/check_resource_sync.py` and focused tests verify:

1. source inventory equals manifest inventory;
2. every manifest source hash matches the live source;
3. both locale paths exist at the canonical location and no legacy resource page remains;
4. source-faithful/neutral copies meet their exact-content rule;
5. translated pairs preserve heading-level sequence, fenced code, protected inline-code tokens,
   relative link targets and table shape;
6. prose-bearing translated pages are not byte-identical across locales;
7. every Markdown resource is reachable through generated navigation;
8. all local links and VitePress routes build successfully.

Semantic translation quality remains a review responsibility. Each child task performs targeted
side-by-side sampling of normative, procedural and example-heavy pages.

## 9. Execution And Compatibility

Execution order is core contract -> smallest English-to-Chinese pilot -> Chinese-to-English pilot ->
remaining skills -> parent integration:

1. `docs-bilingual-core`
2. `docs-bib-search-citation`
3. `docs-latex-thesis-zh`
4. `docs-cover-letter`
5. `docs-paper-audit`
6. `docs-latex-paper-en`
7. `docs-typst-paper`
8. parent full-scope verification

The URL migration is intentionally breaking. Release notes and redirects are outside this task unless
the user later broadens scope.

## 10. Rollback

Each child owns only one skill subtree plus its manifest rows and navigation output. If a child fails
review, revert that child before starting the next. The core task must land first; reverting it requires
reverting all children because their paths depend on the canonical hierarchy.
