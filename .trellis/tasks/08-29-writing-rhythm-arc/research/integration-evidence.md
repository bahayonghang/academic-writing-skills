# Writing rhythm arc parent integration evidence

## Child closeout map

| Child | Work commit | Archive commit | Parent AC |
| --- | --- | --- | --- |
| C1 density/budget | `4b37ddf` | `62f74a0` | AC1, AC2, AC3, AC5, AC7 |
| C2 thesis-zh P-ARC | `af84e4a` | `401ee53` | AC4, AC6 |
| C3 paper-en P-ARC | `e09675d` | `0bda6a1` | AC4, AC5, AC6 |
| C4 paper-audit P-ARC | `a56b74c` | `e63a627` | AC6, AC8 |

Historical metadata note: C1's archived `task.json` retains `base_branch: main`, but Git ancestry
shows `4b37ddf` is based directly on `fc9fdd9` (`origin/dev` at audit time). The archived child was
left unchanged.

## Final gates

- `just ci`: 1641 passed; Ruff clean; Pyright 0 errors and 74 warnings.
- C4 focused contract and scheduling tests: 152 passed.
- `docs/scripts/check_resource_sync.py --skill paper-audit`: passed, 265 manifest entries.
- full resource sync: passed, 265 manifest entries.
- VitePress docs build: passed.
- C4 independent `trellis-check`: no remaining implementation defects after two contract fixes.
- C1-C4 child tasks are all archived under `.trellis/tasks/archive/2026-08/`.

## Evidence boundary

- C1 is a five-paper Chinese density recomputation. Against the 25 legacy absolute caps at
  `fc9fdd9`, the papers triggered 17/15/14/17/15 terms; the new calibrated density table triggers
  0/0/1/2/0 terms in the checked-in full-corpus snapshot.
- C2 is a local product-helper rerun over one private Chinese thesis chapter. It is not evidence of
  cross-chapter, cross-template, or cross-disciplinary representativeness.
- C3 converts each legacy allowance at the 5000-visible-word baseline and exercises P-ARC only on
  a controlled synthetic English fixture. It is not English corpus calibration.
- C4 is an audit-only rubric/lane/agent heuristic protected by contract tests. It does not validate
  reviewer behavior or scoring effects.

English real-paper precision/recall, target-venue transfer, cross-disciplinary representativeness,
threshold external validity, and effects on actual reviewer scores remain **UNVERIFIED**.
