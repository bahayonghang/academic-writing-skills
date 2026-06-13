# LLM / AI-Assistance Disclosure Policies (2026-06)

> Factual reference for where and whether AI assistance must be disclosed at
> major venues. This file describes **disclosure obligations only**. It does not
> provide any advice on evading AI-detection — the `deai` module is a
> readability/clarity aid, not a detector-evasion tool. When a paper used an LLM
> in any non-trivial way, disclose it per the target venue's policy below.

All listed venues **permit** language polishing. They differ on what must be
disclosed and where. "Polishing" = grammar/spelling/wording; "generative use" =
drafting text, generating code, or producing analysis.

| Venue / publisher | Polishing | Generative use disclosure | Where | Desk-reject risk |
|-------------------|-----------|---------------------------|-------|------------------|
| NeurIPS 2025/2026 | exempt | declare in the paper checklist when an LLM is a core method component | checklist | checklist required; LLMs cannot be authors |
| ICML 2026 | exempt | author fully responsible; prompt injection forbidden | n/a | prompt injection = desk reject |
| ICLR 2026 | exempt | significant ideation/writing role must be described | dedicated LLM-usage section (may be appendix) | undisclosed significant use → desk reject |
| COLM 2026 | exempt (light aid) | significant role must be disclosed | dedicated section (ICLR-style) | undisclosed significant use → desk reject |
| ACL / ARR | exempt | generative writing/code **must** be declared | Responsible NLP Checklist + Acknowledgements | wrong/misleading checklist → desk reject |
| CVPR | n/a (no mechanism) | author fully responsible | n/a | fabricated citations / factual errors → reject without review |
| IEEE | "suggested, not required" | AI-**generated** content (text/figures/code) must be disclosed | Acknowledgments section (name system + affected sections) | — |
| ACM | exempt after revision | generated content disclosed prominently | within the Work (e.g. Acknowledgements) | LLMs cannot be authors |
| Springer Nature | "AI-assisted copy editing" exempt | generative use recorded | Methods | AI-generated images forbidden; LLM not an author |
| Elsevier | grammar/spelling exempt | all other generative use declared | a "Declaration of Generative AI…" statement before the references | published with the paper |
| Science | — | AI use disclosed | cover letter **and** in the paper | undisclosed use can be misconduct |
| ICMJE journals (medical) | — | AI use disclosed | cover letter **and** manuscript (Section V, 2026-01) | undisclosed use can constitute misconduct |

## Practical guidance

- arXiv: generative AI cannot be listed as an author; significant use should be
  disclosed per field convention. Since 2025-10-31, arXiv CS review/survey/position
  articles need proof of peer review at a journal/conference (workshops do not count).
- A cover letter is the right place for disclosure at medical/ICMJE journals,
  Science, and many Elsevier titles; ML conferences use checklists or a dedicated
  section instead. See `cover-letter` skill for the letter-side declaration.
- When in doubt, disclose. Disclosure is never penalized; undisclosed significant
  use is, at several venues, grounds for desk rejection or a misconduct finding.

> Sources: per-venue 2026 author guides and CFPs; ICMJE 2026-01 Recommendations;
> IEEE / ACM / Springer Nature / Elsevier AI policy pages; arXiv help/blog.
> See the parent audit's `latex-paper-en-venue-factcheck.md` for the full citation list.
