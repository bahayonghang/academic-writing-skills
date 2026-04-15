# Example: Explicit Intake Locking

## User Prompt

`Create a literature-map in Simplified Chinese on edge AI for smart manufacturing from 2023-2025, and stop if the evidence is too thin.`

## Expected Intake Resolution

- Lock `Simplified Chinese` as the report language.
- Lock `literature-map` as the deliverable mode.
- Lock the time window to the absolute span `2023-2025`.
- Lock the emphasis to `CPS and edge AI` or `smart manufacturing and process optimization`, whichever better matches the phrasing.
- Do **not** re-ask the full four-question intake because the prompt already resolves it.

## Expected Search Note

- State the chosen venue buckets before synthesis.
- Mention the exact year span used.
- If the evidence is sparse, say so directly and stop with a thin-evidence note rather than padding the report.

## Good Output Shape

- Locked intake choices up front
- Venue buckets and recency policy
- Shortlisted papers with explicit preprint labels
- Literature-map synthesis or thin-evidence stop note
