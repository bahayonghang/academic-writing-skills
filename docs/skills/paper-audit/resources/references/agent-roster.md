# Agent Roster

Full list of reviewer agents under `agents/`. `SKILL.md` keeps a one-line
summary; this file is the authoritative roster.

## Committee agents (deep-review default)

- `committee_editor_agent.md`
- `committee_theory_agent.md`
- `committee_literature_agent.md`
- `committee_methodology_agent.md`
- `committee_logic_agent.md`

## Default deep-review lanes

- `section_reviewer_agent.md`
- `claims_evidence_reviewer_agent.md`
- `notation_consistency_reviewer_agent.md`
- `evaluation_fairness_reviewer_agent.md`
- `self_consistency_reviewer_agent.md`
- `prior_art_reviewer_agent.md`
- `synthesis_agent.md`
- `editor_in_chief_agent.md` — EIC desk-reject screener (used in `gate` mode)
- `revision_coach_agent.md` — parse free-form reviewer letters into a
  structured roadmap (used in `re-audit` mode)
- `revision_suggestion_agent.md` — convert each Major/Moderate issue into
  an original/suggested text pair plus additional actions; produces
  `artifacts/data/revision_suggestions.json`

## Reference reviewer playbooks (not auto-dispatched)

These files preserve detailed criteria reused by the committee and lane
prompts; they are not automatically dispatched by the current workflow. Their
A5-A7, B6-B10, and C3-C5 criteria remain linked from the live review criteria.
Full dispatch wiring belongs to the follow-up task
`paper-audit-specialized-reviewer-wiring`.

- `critical_reviewer_agent.md` — devil's advocate with C3-C5 checks
- `domain_reviewer_agent.md` — domain expertise with A1-A7 assessments
- `methodology_reviewer_agent.md` — methodology rigor with B3-B10 checks
- `literature_reviewer_agent.md` — evidence-based literature verification
  (optional, `--literature-search`)
