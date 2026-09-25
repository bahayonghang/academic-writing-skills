# Review progression density

The optional `--progression-density` switch counts only the visible prose of a located section. The threshold is marked `UNVERIFIED`. The script does not rotate synonyms and does not emit a replacement sentence.

## Count boundary

When 「进一步」 occurs strictly more than 5 times, or 「针对」 occurs strictly more than 7 times, emit an `[Script]`, Info/P3, `Meaning-Check: NEEDS-LLM` candidate.
Counts of 5 and 7 do not fire. Counts of 6 and 8 do.
Captions, citation keys, mathematics, and code are excluded. Occurrences outside the section are excluded.
When `--section` is omitted, use only the existing `related` range. If that section is missing, keep the original error, do not scan the whole file, and do not report a pass.
`--progression-density` and `--intro-citations` cannot be used together. There is no YAML override.

## Six rewrite directions

These directions are for a human rewrite. The script does not rotate words from them.

1. Direction 1: write a checkable action.
2. Direction 2: write the object, condition, or scope.
3. Direction 3: write stage order.
4. Direction 4: write the given evidence and its boundary.
5. Direction 5: write a disagreement or difference.
6. Direction 6: merge repeated progression and keep one real turn.

## Four paragraph organizations

1. Organization 1: topic sentence, then evidence, then boundary.
2. Organization 2: consensus, then disagreement, then an open problem.
3. Organization 3: method assumption, then applicable condition, then limitation.
4. Organization 4: time stage, then turn, then the current gap.

## Synthetic fragments

```text
进一步分析条件 A。进一步比较方法 B。
```

This fragment only shows what 「进一步」 counts. It is not a sentence from a thesis.

```text
本节先写条件 A 的范围，再写该范围不覆盖的部分。
```

This fragment shows the order of organization 1. It supplies no synonym table and invents no measurement.
