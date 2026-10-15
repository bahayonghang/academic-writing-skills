# Response Quality Gate

This file specifies the R-* codes of `rebuttal_check.py`, their criteria, severities, and fixes, the skip rules, and the NEEDS-LLM review. For the workflow and the ledger fields, see [Response Workflow](rebuttal-workflow.md). For how to write the replies, see [Response Writing](rebuttal-writing.md).

## Usage

```bash
uv run python -B $SKILL_DIR/scripts/rebuttal_check.py --workspace $ROOT/workspace --thesis $THESIS --json
```

- The script reads `workspace/concerns.yaml`, `workspace/rebuttal_state.json`, `workspace/reviews/R<n>.md`, `responses/*.md`, and the review directory. In the thesis repository, it reads the aux files and the include tree of the main file, and runs read-only git commands.
- It writes only `workspace/check.json` (the same content as the `--json` output). It does not write the thesis repository, the review directory, or responses.
- Exit codes: 0 no Critical or Major finding; 1 at least one Critical or Major finding; 2 input error (the workspace has no state file or ledger, the ledger cannot be parsed, or `--thesis` does not exist).

## Output format

In text mode, each finding is one line, and the last line is the summary:

```text
% R-COMMIT (concern=R1-3b, workspace/concerns.yaml:88) [Severity: Critical] [Priority: P0]: [Script] 声明的修改文件自基线提交以来没有改动：chapters/chapter2.tex
% R-MD-SYNTAX (concern=-, responses/response-R1.md:9) [Severity: Major] [Priority: P1]: [Script] Markdown 语法会改变粘贴结果：行首标记
% 汇总：Critical 1，Major 1，Minor 0，Info 0；skipped：无
```

- `concern=` is the id of the ledger item. A finding for a full file has `-`; a finding for a reviewer has `R<n>`.
- The location is the line of the `id:` of the item in the ledger, or a line in responses or in the review text.
- `--json` outputs `{findings[], summary{Critical, Major, Minor, Info}, skipped[]}`.
- Severity and priority: Critical = P0, Major = P1, Minor = P2, Info = P3.

## R-* code table

| Code             | Severity | Criterion                                                                                                                                                                                                                                                 | Fix                                                                                                            |
| ---------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| R-COVER          | Critical | A numbered concern of the review text has no matching `item` in the ledger; or an item with `status: done` has an empty `response`                                                                                                                        | Add the item or the reply. When you split sub-items, keep every item number                                    |
| R-STATUS         | Major    | There are `open`, `planned`, or `needs_user_input` items                                                                                                                                                                                                  | Complete the reply and the evidence, then set `done`; for `needs_user_input`, ask the user first               |
| R-QUOTE          | Major    | The item number does not exist in the review text; `quote` without whitespace is not a substring of the original item; or one part of `quote_short` split at 「……」 is not a substring                                                                    | Copy the original text verbatim from `workspace/reviews/R<n>.md`                                               |
| R-COMMIT         | Critical | An item with `status: done` that needs a location (`revise`, `add`, `partial`, or, when `locations` is set, `future_work`): `evidence.kind` is `none`; or, for `git_diff`, none of `evidence.files` and the files from the locations changed since the base commit | Change the thesis and commit; or check the paths in `evidence.files`; or use `user_confirmed` and write `note` |
| R-COMMIT         | Minor    | `user_confirmed` evidence has an empty `note`                                                                                                                                                                                                          | Record what the user confirmed                                                                                 |
| R-COMMIT         | Info     | Without `--thesis`, with a thesis repository that is not a git repository, or without a base commit, `git_diff` evidence cannot be checked                                                                                                                | Ask the user to confirm, or give `--thesis`                                                                    |
| R-CLAIM          | Critical | A `clarify` or `decline` item, or an item whose `status` is not `done`, has a `response` that contains a completion word (已修改, 已补充, 已增加, 已删除, 已调整, 已完善, 已重绘, 已修正, 已更正, 已统一)                                                  | Remove the completion word; if the thesis really changed, set `action` to `revise` or `add` and add evidence   |
| R-LOC            | Major    | An item with `status: done` that needs a location has empty `locations`; a `label` is not in the revised aux files or the bib keys; a `file` does not exist in the thesis repository; or a `.tex` file of a location has no matching aux file             | Add the location, or correct the label or the path; fully compile the revised thesis                           |
| R-PAGE-STALE     | Major    | A `.tex` file among the evidence files or the location files is newer than its aux file (when there is no chapter aux file, the aux file of the main file)                                                                                                | Fully compile the revised thesis, then run build                                                               |
| R-RENUM          | Minor    | The current number of an anchor differs from the submitted version, and `response` has only the original number (the anchor is not in `locations`)                                                                                                        | Write the revised number in the reply, or add the label to `locations`                                         |
| R-MD-SYNTAX      | Major    | A line in responses breaks the plain-text-equivalent rules: a line-start marker, `**`, `__`, a backtick, a link, an HTML tag, a table pipe, `$`, a backslash, a footnote, or hard-break spaces at the end of the line                                     | Change the text in `response` of the ledger, then build again                                                  |
| R-PLACEHOLDER    | Critical | responses or a `response` of the ledger contains `〔待填写〕`, `TODO`, `TBD`, `XX`, `??`, or `？？`                                                                                                                                                       | Fill in the content; keep an incomplete item at a status other than `done` and report it to the user           |
| R-NUM-SRC        | Major    | A number with a decimal point or a percent sign in a reply is not in the visible text of the thesis and not in the review text (NEEDS-LLM)                                                                                                                | Check the thesis sentence; if the number is wrong, change the reply                                            |
| R-NUM-SRC        | Info     | The number is not in the thesis but occurs in the text of that reviewer (NEEDS-LLM)                                                                                                                                                                       | Confirm that the reply quotes the number from the review text                                                  |
| R-REVIEW-CHANGED | Major    | A review file does not exist, or its sha256 differs from the value at intake time                                                                                                                                                                         | Confirm the origin of the file, run `rebuttal_intake.py --force`, then merge the ledger                        |
| R-SHARED         | Minor    | `shared_with` points to an item that does not exist; or, of two linked items, one changes the thesis (`revise`, `add`, `partial`) and the other is `clarify`, `decline`, or `future_work`                                                                 | Make the handling actions agree, or give the reason for the different handling in the reply                    |
| R-RESULT         | Major    | The `grade` of a reviewer in the ledger is empty; `review-result.md` was not generated; or its grade differs from the ledger                                                                                                                              | Compare with the original, fill in `grade`, and build again                                                    |
| R-SYNC           | Minor    | A file in responses was edited by hand after the last build, or was deleted                                                                                                                                                                               | Write the changes back into the ledger, then run `rebuttal_build.py --force`                                   |
| R-TONE           | Info     | The first 12 characters of 3 or more replies are the same; the reason of a `decline` or `future_work` item contains 「时间」 (time), 「经费」 (funding), or 「工作量」 (workload); a reply contains words that can disparage the reviewer (NEEDS-LLM)     | Rewrite as [Response Writing](rebuttal-writing.md) specifies                                                   |

The evidence and location checks (R-COMMIT, R-LOC) apply only to items with `status: done`. R-STATUS reports the incomplete items.

## Git evidence convention

- Base: `thesis.base_commit` in the state file (intake records it; `--base-commit` can override it).
- Changed files = `git diff --name-only <基线> HEAD` (committed changes; 基线 is the base) together with `git status --porcelain` (uncommitted and untracked changes). A rename entry counts only its new path.
- All git commands have `--no-optional-locks` and do not write `.git/index`.
- When `$ROOT` and the review directory are inside the thesis repository, the paths under them are not changed files.
- The tex file of a location label comes from its aux file (`chapters/chapter2.aux` → `chapters/chapter2.tex`).

## Skip rules

Without `--thesis`, these checks go into `skipped`:

| skipped name    | Content                                                                     |
| --------------- | --------------------------------------------------------------------------- |
| `R-COMMIT(git)` | Check of the git evidence; `git_diff` items get an additional R-COMMIT Info |
| `R-LOC(aux)`    | Existence of labels and files; the check for empty `locations` still runs   |
| `R-PAGE-STALE`  | Time comparison of tex and aux files                                        |
| `R-RENUM`       | Check of number changes                                                     |
| `R-NUM-SRC`     | Check of number sources                                                     |

With `--thesis`, when the thesis repository is not a git repository or the state file has no base commit, only `R-COMMIT(git)` is skipped.

## NEEDS-LLM review

R-NUM-SRC and R-TONE are candidate findings. The LLM reviews each one:

1. R-NUM-SRC: open the matching paragraph, table, or caption in the revised thesis, and confirm the number and the unit. When the number comes from the review text, confirm that the quote is correct. After the review, write 「已核对」 (checked) or the correction in the delivery note.
2. R-TONE: replace a repeated opening with the handling content; replace a resource reason with an academic reason; remove disparaging words.
3. Write the review results in the delivery note, not in responses.

## Fix loop

1. `rebuttal_build.py` → `rebuttal_check.py --json`.
2. Fix Critical findings first, then Major findings; list Minor and Info findings in the delivery note.
3. After a ledger change, build again; after a thesis change, compile the thesis again, then build.
4. At most 3 rounds. If Critical or Major findings remain after 3 rounds, stop and report.
