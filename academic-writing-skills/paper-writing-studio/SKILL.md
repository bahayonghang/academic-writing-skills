---
name: paper-writing-studio
description: >-
  Use this academic writing skill to polish or translate academic writing with an explicit Nature, IEEE, Elsevier,
  or neutral profile. Selects a profile by explicit venue, journal allowlist,
  then unambiguous domain; reports uncertainty instead of guessing.
version: 0.1.0
---

# Paper Writing Studio

Use `scripts/core.py` for selection and the output contract. Profile
manifests under `profiles/` are isolated load plans: load only the selected
profile's section reference and evidence rows. The core never loads or merges
venue TSV files. If no safe mapping exists, use `unspecified`.

Profiles: `nature.json`, `ieee.json`, and `elsevier.json`. Their `source_path`,
`provenance`, `load_order`, section routes, and evidence gates are part of the
trace; candidate or degraded rows must remain explicit in `summary`.

Inputs: `input_text`, `target`, optional `venue`, `journal`, and `domain`.
Outputs: inline Markdown with `text`, `text_compact`, and a traceable `summary`.
