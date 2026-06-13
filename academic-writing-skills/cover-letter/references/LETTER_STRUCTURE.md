# Letter Structure

Five-segment canonical structure for an academic submission cover letter. Used by `generate` mode as the scaffold and by `optimize` mode as the diagnostic checklist.

## 1. Header

- Date.
- Editor's name and title (when known) or "Editor-in-Chief" + journal title.
- Salutation: "Dear Dr. [Last Name]" (preferred) or "Dear Editor-in-Chief."

If editor information is not available from the user, output `[Editor name to be confirmed]` as a placeholder rather than guessing.

## 2. Opening (1 sentence)

- Manuscript title and article type.
- Target journal title.
- One-clause statement of the central finding or contribution.

Avoid:

- "We are pleased to submit..."
- "Enclosed please find..."
- "Please find attached..."

Prefer:

- "We submit [title], an [article type] reporting [one-clause headline]."
- "We present [title], which [verb] [contribution]."

## 3. Contribution claim (2-4 sentences)

- What was done: 1 sentence.
- Headline quantitative result: 1 sentence with a number that also appears in the manuscript.
- Why this matters: 1 sentence on what now becomes possible or what previously open question is resolved.
- Optional: 1 sentence acknowledging the comparison frame (the prior work this extends).

**Constraint**: every numeric value, comparator name, or claim of "first," "best," "outperforms" must trace to a specific section of the manuscript. This is what `align-check` verifies.

## 4. Journal fit (2-3 sentences)

- Why this venue is the right home.
- Reference the journal's specific scope or recent paper this work connects to.
- Avoid generic "broad readership" framing — be specific.

## 5. Declarations (template-driven)

Order:

1. Originality / dual-submission ("This manuscript has not been published elsewhere and is not under concurrent consideration.")
2. Authorship ("All authors have approved the submission.")
3. Competing interests (explicit, even when "none").
4. AI-use disclosure (required by Nature / Science / Cell and ICMJE Jan 2026 Section V when generative AI assisted the manuscript or letter; IEEE / ACM disclose this inside the manuscript instead). Name the tool and how it was used; pure grammar/spell-check is exempt.
5. Data availability (if applicable to venue; top journals route this through the submission system rather than the letter).
6. Ethics / IRB / IACUC (if applicable).
7. Conference extension disclosure (if applicable — IEEE / ACM journals).
8. Funding sources (if applicable).

## 6. Closing

- Brief thank-you statement (one sentence).
- Corresponding author block: name, affiliation, email, ORCID (optional).

## Length budget by section

| Section      | Top journal   | Mid journal   | Conference    |
| ------------ | ------------- | ------------- | ------------- |
| Opening      | 1-2 sentences | 1-2 sentences | 1 sentence    |
| Contribution | 3-4 sentences | 3-5 sentences | 3 sentences   |
| Journal fit  | 2-3 sentences | 2-3 sentences | 2 sentences   |
| Declarations | 3-5 sentences | 3-5 sentences | 2-3 sentences |
| Closing      | 1 sentence    | 1 sentence    | 1 sentence    |
| **Total**    | ≤350 words    | 400-500 words | ≤400 words    |
