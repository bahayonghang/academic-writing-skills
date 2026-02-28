---
name: paper-audit
version: 1.0.0
category: academic-writing
tags:
  - audit
  - review
  - paper
  - pdf
  - latex
  - typst
  - chinese
  - english
  - scoring
  - checklist
description: |
  Unified paper audit skill supporting Chinese & English academic papers.
  Supports LaTeX (.tex), Typst (.typ), and PDF (.pdf) input formats.
  Three modes: self-check (pre-submission), review (peer review simulation),
  gate (quality gate pass/fail).
  Use when user mentions: audit, review, check paper, paper quality,
  pre-submission check, score paper, or any paper auditing task,
  polish paper, deep polish, adversarial review, refine writing,
  caption audit, 图表标题审查.
argument-hint: "[paper.tex|paper.typ|paper.pdf] [--mode self-check|review|gate|polish] [--pdf-mode basic|enhanced] [--style A|B|C] [--journal <venue>] [--skip-logic] [--online] [--scholar-eval]"
allowed-tools: Read, Glob, Grep, Bash(python *), Task
references:
  - resources/references/REVIEW_CRITERIA.md
  - resources/references/CHECKLIST.md
  - resources/references/AUDIT_GUIDE.md
  - resources/references/POLISH_GUIDE.md
  - resources/references/SCHOLAR_EVAL_GUIDE.md
scripts:
  - scripts/audit.py
  - scripts/pdf_parser.py
  - scripts/detect_language.py
  - scripts/report_generator.py
  - scripts/parsers.py
  - scripts/visual_check.py
  - scripts/check_references.py
  - scripts/scholar_eval.py
---

# Paper Audit Skill (论文审核)

Unified academic paper auditing across formats and languages.

## Critical Rules

1. NEVER modify `\cite{}`, `\ref{}`, `\label{}`, math environments in LaTeX
2. NEVER modify `@cite`, `#cite()`, `#ref()`, `<label>` in Typst
3. NEVER fabricate bibliography entries — only verify existing `.bib`/`.yml` files
4. NEVER change domain terminology without user confirmation
5. Check `FORBIDDEN_TERMS` lists before suggesting any terminology changes
6. For PDF input, clearly flag sections where extraction quality is uncertain
7. Always distinguish between automated findings and LLM-judgment scores

## Audit Modes

### Mode: `self-check` (Pre-submission Self-Check)

**Trigger keywords**: audit, check, self-check, pre-submission, score, review my paper

**What it does**: Runs all automated checks and generates a structured report with:
- Per-dimension scores (Quality, Clarity, Significance, Originality) on 1-6 scale
- Issue list sorted by severity (Critical > Major > Minor)
- Improvement suggestions per section
- Pre-submission checklist results

**CLI**: `python scripts/audit.py paper.tex --mode self-check`

#### Online Bibliography Verification

Add `--online` to enable CrossRef/Semantic Scholar metadata verification:
```
python scripts/audit.py paper.tex --mode self-check --online --email user@example.com
```

#### ScholarEval 8-Dimension Assessment

Add `--scholar-eval` to enable the 8-dimension evaluation framework:
```
python scripts/audit.py paper.tex --mode self-check --scholar-eval
```

Script-evaluable dimensions (Soundness, Clarity, Presentation, partial Reproducibility) are scored automatically. For complete assessment, supplement with LLM evaluation of Novelty, Significance, Ethics, and Reproducibility. See `SCHOLAR_EVAL_GUIDE.md`.

**ScholarEval LLM Assessment Prompt** (for `review` mode):

Read the full paper and provide 1-10 scores with evidence in JSON format:

```json
{
  "novelty": {
    "score": "<1-10>",
    "evidence": "<Describe originality and distinction from prior work>"
  },
  "significance": {
    "score": "<1-10>",
    "evidence": "<Describe potential impact on the field>"
  },
  "reproducibility_llm": {
    "score": "<1-10>",
    "evidence": "<Assess experimental description completeness, code/data availability>"
  },
  "ethics": {
    "score": "<1-10>",
    "evidence": "<Assess ethical considerations, conflicts of interest, data privacy>"
  }
}
```

### Mode: `review` (Peer Review Simulation)

**Trigger keywords**: simulate review, peer review, reviewer perspective, what would reviewers say

**What it does**: Everything in self-check PLUS:
- Paper summary from reviewer perspective
- Strengths analysis
- Weaknesses analysis with severity
- Questions a reviewer would ask
- Accept/reject recommendation with confidence

**CLI**: `python scripts/audit.py paper.tex --mode review`

### Mode: `gate` (Quality Gate)

**Trigger keywords**: quality gate, pass/fail, can I submit, ready to submit, advisor check

**What it does**: Fast mandatory checks only:
- Format validation
- Bibliography integrity
- Figure/table references
- Pre-submission checklist
- Binary PASS/FAIL verdict with blocking issues

**CLI**: `python scripts/audit.py paper.tex --mode gate`

### Mode: `polish` (Adversarial Dual-Agent Deep Polish)

**Trigger keywords**: polish, deep polish, adversarial review, refine writing,
  improve writing, paragraph polish

**What it does**:
- Phase 1 (Python): Fast rule-based precheck → .polish-state/precheck.json
- Phase 2 (Critic Agent): LLM adversarial review → per-section logic/expression scores
- Phase 3 (Mentor Agent × N): Per-section polish suggestions → Original vs Revised table
- Outputs: Structured polish report with diff-comment suggestions

**Style options** (`--style`):
- `A` Plain Precise (default): Short sentences, active voice, technical precision
- `B` Narrative Fluent: Story-driven, transitions, accessible prose
- `C` Formal Academic: Passive voice acceptable, formal register, hedge words

**Skip logic**: `--skip-logic` bypasses Critic logic scoring; Mentor runs
  expression-only polish. Equivalent to `/polish` quick command.

**CLI**: `python scripts/audit.py paper.tex --mode polish --style A --journal neurips`

## Supported Formats

| Format | Parser | Notes |
|--------|--------|-------|
| LaTeX (.tex) | `LatexParser` | Full support — all checks available |
| Typst (.typ) | `TypstParser` | Full support — all checks available |
| PDF (.pdf) basic | `PdfParser` (pymupdf) | Text extraction with font-size heading detection |
| PDF (.pdf) enhanced | `PdfParser` (pymupdf4llm) | Structured Markdown with table/header preservation |

**PDF Limitations**: Math formulas may be lost; some checks (format, figures) skip for PDF. Recommend providing source files (.tex/.typ) for maximum accuracy.

## Language Support

| Language | Detection | Extra Checks |
|----------|-----------|-------------|
| English | Auto (default) | Standard suite |
| Chinese | Auto (CJK ratio > 30%) | + consistency check, + GB/T 7714 compliance |

Force with `--lang en` or `--lang zh`.

## Check Modules

| Module | Script Source | Dimensions Affected | Applicable Formats |
|--------|-------------|--------------------|--------------------|
| Format Check | `check_format.py` | Clarity | .tex, .typ |
| Grammar Analysis | `analyze_grammar.py` | Clarity | .tex, .typ, .pdf |
| Logic & Coherence | `analyze_logic.py` | Quality, Significance | .tex, .typ, .pdf |
| Sentence Complexity | `analyze_sentences.py` | Clarity | .tex, .typ, .pdf |
| De-AI Detection | `deai_check.py` | Clarity, Originality | .tex, .typ, .pdf |
| Bibliography | `verify_bib.py` | Quality | .tex, .typ |
| Figure/Table Refs & Captions | `check_figures.py` | Clarity | .tex |
| Reference Integrity | `check_references.py` | Clarity, Quality | .tex, .typ |
| Visual Layout | `visual_check.py` | Clarity | .pdf |
| Consistency (ZH) | `check_consistency.py` | Clarity | .tex (Chinese only) |
| GB/T 7714 (ZH) | `verify_bib.py` (GB mode) | Quality | .tex (Chinese only) |
| Pre-submission Checklist | Built-in | All | All formats |

## Scoring System

Based on REVIEWER_PERSPECTIVE.md criteria:

### Four Dimensions
- **Quality** (30%): Technical soundness, well-supported claims
- **Clarity** (30%): Clear writing, reproducible, good organization
- **Significance** (20%): Community impact, advances understanding
- **Originality** (20%): New insights, not obvious extensions

### Six-Point Scale (NeurIPS standard)
| Score | Rating | Meaning |
|-------|--------|---------|
| 5.5-6.0 | Strong Accept | Groundbreaking, technically flawless |
| 4.5-5.4 | Accept | Technically solid, high impact |
| 3.5-4.4 | Borderline Accept | Solid but limited evaluation/novelty |
| 2.5-3.4 | Borderline Reject | Merits but weaknesses outweigh |
| 1.5-2.4 | Reject | Technical flaws, insufficient evaluation |
| 1.0-1.4 | Strong Reject | Fundamental errors or known results |

## Output Protocol

All issues follow the unified format:

```
[MODULE] (Line N) [Severity: Critical|Major|Minor] [Priority: P0|P1|P2]: Issue description
  Original: ...
  Revised:  ...
  Rationale: ...
```

- **Severity**: Critical (must fix), Major (should fix), Minor (nice to fix)
- **Priority**: P0 (blocking), P1 (important), P2 (low priority)

## Workflow

When a user requests a paper audit:

1. **Identify the file** — locate the .tex, .typ, or .pdf file
2. **Determine mode** — self-check (default), review, or gate based on user intent
3. **Run the orchestrator** — `python scripts/audit.py <file> --mode <mode>`
4. **Present the report** — show the Markdown report to the user
5. **Discuss findings** — help the user address Critical and Major issues first
6. **Re-audit if needed** — run again after fixes to verify improvements

For `review` mode, supplement the automated report with LLM analysis of:
- Overall paper strengths (what works well)
- Key weaknesses (what reviewers would criticize)
- Questions a reviewer would ask
- Missing related work or baselines

### Polish Mode Workflow

1. **Run Python precheck**
   ```
   python scripts/audit.py <file> --mode polish [--style A|B|C] [--journal <name>] [--skip-logic]
   ```
   Read `.polish-state/precheck.json` from the paper's directory.

2. **Check hard blockers**
   If `precheck.json["blockers"]` is non-empty, display them and STOP.
   Say: "Fix these Critical issues before polish can proceed:" + list.
   Do NOT spawn any agent until user confirms fixes.

3. **Handle non-IMRaD structure** (if `precheck.json["non_imrad"] == true`)
   Show detected sections, ask user: "Proceed with polish on these sections?"

4. **Spawn Critic Agent** via Task:

   Subagent type: `general-purpose`
   Prompt template:
   ```
   You are an adversarial academic reviewer.
   Paper: {file_path}  |  Language: {lang}  |  Journal: {journal}  |  Style: {style}

   Step 1: Read the paper using the Read tool (file: {file_path}).
   Step 2: The rule-based precheck found these issues: {precheck_issues_summary}
   Step 3: Produce a CRITIC REPORT as valid JSON (no markdown fencing):
   {
     "global_verdict": "ready_to_polish" | "needs_revision_first" | "major_restructure_needed",
     "global_rationale": "2-3 sentences",
     "section_verdicts": [
       {
         "section": "<name>",
         "logic_score": 1-5,
         "expression_score": 1-5,
         "blocks_mentor": false,
         "blocking_reason": "",
         "top_issues": [{"type": "logic|expression|argument", "description": "..."}]
       }
     ],
     "cross_section_issues": ["..."]
   }
   blocks_mentor = true ONLY when logic_score <= 2 or section is structurally absent.
   ```
   Save the Critic's JSON output to `.polish-state/critic_report.json` using Bash:
   ```
   python -c "import pathlib; pathlib.Path('.polish-state/critic_report.json').write_text('<critic_json_here>', encoding='utf-8')"
   ```

5. **Display Critic Dashboard and gate**
   Render the Critic report as a markdown table (see dashboard format).
   Show blocked sections. Ask:
   "How to proceed?
    [1] Polish all sections (override blocks)
    [2] Skip blocked sections, polish the rest
    [3] Stop and revise blocked sections first"
   Wait for response.

6. **Spawn Mentor Agents per section** (sequential, one at a time):
   For each approved section in IMRaD order:

   Subagent type: `general-purpose`
   Prompt template:
   ```
   You are a writing mentor specializing in academic polish.

   CRITICAL RULES (NEVER VIOLATE):
   - Never modify \cite{}, \ref{}, \label{}, \eqref{} in LaTeX
   - Never modify @cite, #cite(), #ref(), <label> in Typst
   - Never modify math environments: $...$, \begin{equation}..., \begin{align}...
   - Never add/remove citations
   - Mark any domain terminology changes as [TERM CHANGE: confirm?]

   Section: {section_name} (lines {start}-{end})
   Target style: {style} ({style_description from POLISH_GUIDE.md})
   Critic scores — Logic: {logic_score}/5, Expression: {expression_score}/5
   Critic top issues: {top_issues}
   Pre-check expression issues in this section: {filtered_expression_issues}

   Read lines {start}-{end} of {file_path}:
     Use Read tool with offset={start-1} and limit={end-start+1}.

   Produce MENTOR REPORT in this format:

   ## Section: {section_name}

   ### Polish Suggestions
   [MENTOR] (Line N) [Severity: Major|Minor] [Priority: P1|P2]: description
     Original: <exact original text>
     Revised:  <revised text preserving all LaTeX/Typst commands>
     Rationale: <one sentence>

   ### Section Summary
   <2-3 sentences on overall quality and key improvements>
   ```

   After each Mentor completes:
   - Display its output
   - Ask: "Section {name} polish done. Accept and continue to next section?"
   - Wait for confirmation before spawning next Mentor.

7. **Final status dashboard** (after all sections done):
   See dashboard format below.

### Polish Status Dashboard Format

Print at end of each phase and at completion:

```
╭─ 🔴🔵 paper-audit Polish Mode ──────────────────────────╮
│ 📄 File: {filename} | Style: {A/B/C} | Journal: {venue} │
│ ⚔️  Critic: {global_verdict}                             │
│                                                           │
│ Section      │ Logic │ Expr │ Mentor      │ Suggestions  │
│ abstract     │  4/5  │ 3/5  │ ✅ Done     │      3       │
│ introduction │  3/5  │ 2/5  │ ✅ Done     │      7       │
│ method       │ BLOCK │ 2/5  │ ⏭️  Skipped  │      0       │
│ experiment   │  4/5  │ 4/5  │ ✅ Done     │      2       │
│ conclusion   │  5/5  │ 3/5  │ ✅ Done     │      4       │
│                                                           │
│ 👉 Next: {明确的下一步指示}                               │
╰───────────────────────────────────────────────────────────╯
```
