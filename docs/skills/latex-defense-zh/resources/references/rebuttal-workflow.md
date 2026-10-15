# Review Response Workflow

This file specifies the use of the three review response (rebuttal) scripts, the directory layout, the fields of the concern ledger, the rules to split compound concerns, the selection of the handling action, the checkpoints, the evidence requirements, and the fix loop. For how to write the reply text, see [Response Writing](rebuttal-writing.md). For the R-* codes, see [Response Quality Gate](rebuttal-gate.md).

Scope: after the review reports of a thesis pre-review, blind review, final review, or pre-defense return, write the reply to each concern in the 「博士生修改说明」 (revision statement) or the 「评阅意见修改审查表」 (review revision form), and check that the thesis really changed. Rebuttal letters for journals or conferences are out of scope.

## Usage

```bash
uv run python -B $SKILL_DIR/scripts/rebuttal_intake.py --reviews $REVIEWS --thesis $THESIS --main document.tex --stage pre-review --json
uv run python -B $SKILL_DIR/scripts/rebuttal_build.py --workspace $ROOT/workspace --thesis $THESIS --plan-only
uv run python -B $SKILL_DIR/scripts/rebuttal_build.py --workspace $ROOT/workspace --thesis $THESIS --json
uv run python -B $SKILL_DIR/scripts/rebuttal_check.py --workspace $ROOT/workspace --thesis $THESIS --json
```

`$REVIEWS` is the review directory. `$THESIS` is the root directory of the thesis repository. `$ROOT` is the parent directory of `$REVIEWS` (when intake gets `--root`, it is that directory).

| Script               | Options                                                                                                                                                                                                                                       |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `rebuttal_intake.py` | `--reviews DIR` (required), `--thesis DIR`, `--main FILE`, `--root DIR`, `--stage pre-review\|final-review\|predefense\|other` (default `pre-review`), `--form-title TEXT`, `--order FILE,FILE,...`, `--base-commit SHA`, `--force`, `--json` |
| `rebuttal_build.py`  | `--workspace DIR` (required), `--thesis DIR`, `--plan-only`, `--force`, `--json`                                                                                                                                                              |
| `rebuttal_check.py`  | `--workspace DIR` (required), `--thesis DIR`, `--json`                                                                                                                                                                                        |

| Script               | Exit codes                                                                                                                                                                                                                                                                                                       |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `rebuttal_intake.py` | 0: success (warnings are possible); 2: input error (the directory does not exist, there is no review report, a `.docx`/`.doc`/image file, or the review directory and an output directory are nested); 3: a PDF is present and PyMuPDF is not installed; 4: `workspace/reviews/` exists and `--force` is not set |
| `rebuttal_build.py`  | 0: success; 2: the ledger or the workspace fails validation; 4: a file in responses was edited by hand after the last build and `--force` is not set                                                                                                                                                             |
| `rebuttal_check.py`  | 0: no Critical or Major finding; 1: at least one Critical or Major finding; 2: input error                                                                                                                                                                                                                       |

- `--thesis` is optional. Without it, intake does not map anchors to labels and does not record the base commit; the build locations have no current number and page; check skips the checks that need the thesis (see [Response Quality Gate](rebuttal-gate.md)).
- To read a PDF, PyMuPDF is necessary (`uv pip install pymupdf`). A scanned PDF without a text layer gives an empty skeleton and W-NO-TEXT. Then the user supplies a TXT file, or the LLM reads the page images and fills in the ledger.

## Directory layout

```text
$ROOT/
  <评阅书目录>/                 输入，只读
  responses/                    粘贴用文本，由 rebuttal_build.py 生成
    review-result.md            预评审结果行：总体评价 1（A）；总体评价 2（B）
    response-all.md             「博士生修改说明」全文
    response-R1.md …            单个评阅人的修改说明
  workspace/                    中间产物
    rebuttal_state.json         状态文件
    reviews/R1.md …             归一化评阅原文（脚本生成，不手改）
    concerns.yaml               意见台账（唯一事实源）
    revision_plan.md            修改计划（按负责方分组的表格）
    anchors.json                build 解析出的锚点
    check.json                  最近一次 check 结果
```

- The three scripts write only `responses/` and `workspace/`. The review directory and the thesis repository are read only. In the thesis repository, the scripts read only `*.aux`, the include tree of the main file, and read-only git commands.
- `$ROOT` can be inside the thesis repository (for example `<论文仓库>/rebuttal/pre-review/`). Then check excludes the paths under `$ROOT` and the review directory when it checks the git evidence.
- The review directory must not be `responses/` or `workspace/` and must not be inside them. Otherwise intake exits with code 2.

### State file `rebuttal_state.json`

| Field                | Meaning                                                                                                                                                                                  |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `schema`             | `"rebuttal-state/1"`                                                                                                                                                                     |
| `stage`              | `pre-review`, `final-review`, `predefense`, `other`                                                                                                                                      |
| `form_title`         | Title of the revision form. The default comes from `--stage`, and `--form-title` overrides it. Use it to compare with the title of the Word form; responses do not contain it            |
| `reviews_dir`        | Path of the review directory relative to `$ROOT`                                                                                                                                         |
| `reviews[]`          | `{id, file, sha256, pages, text_layer}`; `id` is `R1`, `R2`, …, sorted by the Arabic number in the file name, or by the file name when there is no number; `--order` overrides the order |
| `thesis`             | `{given, base_commit, aux_labels, main}`; `base_commit` is the `HEAD` of the thesis repository at intake time; `--base-commit` overrides it                                              |
| `rendered`           | `{<responses 相对路径>: sha256}`; build writes it to detect hand edits                                                                                                                   |
| `created`, `updated` | ISO dates                                                                                                                                                                                |

## Intake: read the review reports

1. Get the text of each page. `.txt` and `.md` files are split into pages at form feeds; without a form feed, the file is one page.
2. Remove watermarks and page headers: lines that repeat on at least `max(2, ceil(2/3 × 页数))` pages (页数 is the page count). Remove 「第 N 页」 lines and page number lines that contain only 1–3 digits. A digit line immediately after 「总分」 (total score) stays as the total score.
3. Split the 「学术评语」 (academic comments) and the 「不足之处和建议」 (shortcomings and suggestions) at their headings. Then split the concerns at the line-start numbers (`1.`, `1、`, `（1）`, `(1)`). The numbers must increase from 1. A line whose number does not increase joins the previous item.
4. Line joining: Chinese characters join directly; English words and digits get one space between them.
5. Parse the total score, the overall grade (A–E), and the defense decision.
6. Find anchors: `图a-b`, `表a-b`, `式(a-b)`, `公式(a-b)`, `算法a-b`, `第N章`, `第N章至第M章`, `a.b节`, `文献[n]`, `文献[n,m]`, `文献[n-m]`. With `--thesis`, look up the labels in the aux files of the submitted version and write `label`, `base_number`, and `base_page`.
7. Write `workspace/reviews/R<n>.md` and the state file. Write the ledger skeleton `concerns.yaml` only when it does not exist.

| warning            | Meaning and action                                                                                                                                      |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| W-SKIP-FILE        | A file in the directory that is not a review report was ignored; of files with the same name, intake reads one in the order `.md`, `.txt`, `.pdf` and ignores the others |
| W-NO-TEXT          | The PDF has no text layer; supply a TXT file, or let the LLM read the page images and fill in the ledger                                                |
| W-NO-SCORE         | The total score, the overall grade, or the defense decision was not parsed; compare with the original and fill it in under `reviewers` in the ledger    |
| W-NO-SECTION       | No heading of the 「不足之处和建议」 type was found, and the full text is one section; the LLM checks the split                                         |
| W-NO-NUMBER        | The shortcomings have no numbers, and the full section is item 1; the LLM splits it into sub-items                                                      |
| W-UNNUMBERED       | The text before item 1 is not in the ledger; check whether it contains a concern                                                                        |
| W-ANCHOR-AMBIGUOUS | One anchor matches more than one label, and the first one is used; check `label`                                                                        |
| W-ANCHOR-MISSING   | An anchor has no label in the aux files of the submitted version (for example the middle chapters of 「第3章至第5章」); the next steps are not affected |
| W-NO-AUX           | The thesis repository has no aux files; compile the submitted version, then run intake again                                                            |
| W-NO-GIT           | The thesis repository is not a git repository; the modification evidence can only be `user_confirmed`                                                   |
| W-LEDGER           | The existing ledger cannot be read; correct the YAML syntax                                                                                             |
| W-LEDGER-MISSING   | After a rerun with `--force`, there are items that the ledger does not have; the LLM merges them into the ledger                                        |

`--force` rewrites only `workspace/reviews/` and the state file. It never overwrites an existing ledger.

Base commit: the `base_commit` that intake records must be the submitted version. If modifications were committed after the submission, set it with `--base-commit <送审版本的提交>` (the commit of the submitted version). Otherwise check cannot see these modifications.

## Concern ledger `concerns.yaml`

The ledger is the only source of facts for responses. To change text in responses, change only the ledger, then build again.

```yaml
schema: rebuttal-ledger/1
reviewers:
  - id: R1
    total_score: 88 # 解析失败为 null
    grade: A # A–E 或 null
    agree_defense: 同意答辩
    praise: "<学术评语全文>" # 只读引用，不回复
concerns:
  - id: R1-3b # 评阅人-条号[小写字母子项]
    reviewer: R1
    item: 3 # 评阅书中的条号
    quote: "<评阅原文的逐字子串>"
    quote_short: null # quote 超过 160 字时给出首尾摘录，以「……」相连
    category: figure
    severity: Minor # Critical|Major|Minor|Info
    priority: P2 # P0|P1|P2|P3
    shared_with: [] # 与其他评阅人重叠的条目 id
    anchors: [] # intake 生成，不手改
    action: revise # revise|add|clarify|partial|future_work|decline
    status: done # open|planned|done|needs_user_input
    owner: drawio # latex-thesis-zh|drawio|manual|none
    plan: "<修改计划>"
    response: "<回复正文>"
    locations:
      - label: fig:c2-profile # 优先：LaTeX 标签或 bib 键
      - file: chapters/chapter2.tex # 无标签时：文件 + 节号
        section: "2.3"
    evidence:
      kind: git_diff # git_diff|user_confirmed|none
      files: [chapters/chapter2.tex]
      note: ""
    source: "[LLM]" # intake 生成为 "[Script]"，LLM 改写后为 "[LLM]"
```

| Field                   | Values                                                                                                                                                                                                            |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `category`              | `writing` (wording, abbreviations, symbols), `figure`, `table`, `reference`, `structure`, `experiment`, `generalization`, `theory`, `complexity`, `deployment`, `application`, `innovation`, `other`              |
| `severity` / `priority` | Critical / P0, Major / P1, Minor / P2, Info / P3; set them by the effect of the concern on the conclusions of the thesis                                                                                          |
| `owner`                 | `latex-thesis-zh` (body text changes), `drawio` (figures), `manual` (the user makes the change, for example the bib file or an experiment), `none` (the thesis does not change)                                   |
| `status`                | `open`: written by intake; `planned`: the user approved the handling action; `done`: the reply, the locations, and the evidence are complete; `needs_user_input`: the LLM cannot decide, and the user must answer |
| `locations[]`           | Each item must have `label` (a LaTeX label or a bib key) or `file` (a path relative to the thesis repository; `section` is optional)                                                                              |
| `evidence.files`        | Paths relative to the thesis repository                                                                                                                                                                           |

Numbers, conclusions, and locations in the ledger come only from the review text, the thesis, or a user confirmation. The LLM does not write experimental results that the thesis does not contain.

## Split compound concerns

When one numbered concern contains more than one independent modification request, split it into the sub-items `R<n>-<条号>a`, `b`, `c`, … (条号 is the item number), and remove the original full item.

1. Criterion: each sub-item can have its own handling action and its own modification location. Do not split several statements of the same request (「图2-1文字过于密集，图注也过长」, figure text too dense and caption too long).
2. The `quote` of each sub-item is a verbatim substring of the original text, without the lead-in phrase (「写作规范方面：」) and the separator punctuation.
3. Give the sub-items letters in the order of the original text. In the output, the sub-items of one item number share one 「意见N：」 original text, followed by 「（1）回复：」 and 「（1）修改位置：」.
4. A sub-item keeps the `reviewer` and `item` of the original item and the part of `anchors` that belongs to the sub-item.
5. Do not merge the same problem from different reviewers into one item: keep one item for each reviewer, link them with `shared_with`, and write the full reply in each.

## Select the handling action

| action        | Meaning                                               | Required                                                                                                               | Completion words in the reply  |
| ------------- | ----------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| `revise`      | Change existing content                               | `locations`, `evidence.kind≠none`                                                                                      | Allowed                        |
| `add`         | Add new content                                       | `locations`, `evidence.kind≠none`                                                                                      | Allowed                        |
| `clarify`     | Explain in the reply only; the thesis does not change | `response` gives the reason                                                                                            | Not allowed                    |
| `partial`     | Partly accept                                         | `locations`, `evidence.kind≠none`; `response` gives the reason for the part that is not accepted                       | Only for the changed part      |
| `future_work` | List as future work                                   | `response`; if a discussion was added to the limitations or the outlook of the thesis, also `locations` and `evidence` | Only for the added thesis text |
| `decline`     | Do not accept                                         | `response` gives an academic reason                                                                                    | Not allowed                    |

Order of selection:

1. The error or gap that the concern identifies exists in the thesis, and the change can be completed before the defense: `revise` or `add`.
2. The concern comes from a different reading, and the thesis already has the content: `clarify`; the reply gives the location of the original text. If that wording is really easy to misread, use `revise` and rewrite the wording.
3. The additional experiment, new data, or new platform that the concern requests cannot be completed before the defense: `future_work`. A discussion can be added to the 「局限与展望」 (limitations and outlook) section of the thesis, and that section becomes the modification location. The reply must not say that the experiment is complete.
4. The concern conflicts with the problem scope or the research assumptions of the thesis: `decline`; the reason is academic (problem scope, assumptions, the practice of existing literature), not time, funding, or workload.
5. Only part of the concern can be accepted: `partial`; give the changed part and the reason for the part that is not accepted.
6. It is not possible to decide whether to accept, or the user must supply experimental data: `status: needs_user_input`; write the question for the user in `plan`.

## Checkpoints

| Checkpoint | When                                                                                                                             | Content                                                                                                                                                                                                                                                                                                                           |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| R1         | After intake                                                                                                                     | Report to the user the total score, the grade, the concern count, the anchor count, and the warnings of each reviewer. Ask the user to confirm the reviewer order (R1 and R2 agree with the numbers of the originals) and the base commit (the submitted version). If the order is wrong, run again with `--order` and `--force`. |
| R2         | After the LLM splits the concerns and fills in `action`, `owner`, `plan`, and `status: planned`                                  | Run `rebuttal_build.py --plan-only`, and give `workspace/revision_plan.md` to the user to approve the handling actions. Explain the reason of each `decline` and `future_work` item. Do not write replies before the user approves.                                                                                               |
| R3         | After the thesis is changed and compiled again, the replies and the evidence are filled in with `status: done`, and check passes | Deliver the file list of `responses/`, the quality gate counts, and the open items. The user pastes the text into the Word form.                                                                                                                                                                                                  |

Between R2 and R3, the user or `latex-thesis-zh` changes the thesis, and a tool of the `drawio` type changes the figures. This module does not change the thesis source files and does not compile the thesis. After the changes, commit them to git and fully compile the revised thesis (the aux files must be newer than the tex files). Then write the replies.

## Evidence requirements

- `git_diff`: at least one of the files from `evidence.files` or `locations` changed after the base commit (committed and uncommitted changes both count). Use it only when the thesis repository is a git repository.
- `user_confirmed`: the user confirms the change in the conversation, and `note` records what the user confirmed (for example 「图由导师在 Visio 中重绘，PNG 已替换」, the supervisor redrew the figure in Visio and the PNG was replaced). check does not check git.
- `none`: the thesis did not change. Allowed only for `clarify`, `decline`, and `future_work` without locations.

The evidence and location checks apply only to items with `status: done`.

## Fix loop

1. Run `rebuttal_build.py`, then run `rebuttal_check.py --json`.
2. Change the ledger as [Response Quality Gate](rebuttal-gate.md) specifies (or change the thesis and compile it again), then build and check again.
3. At most 3 rounds. If Critical or Major findings remain after 3 rounds, stop and report the remaining findings and their causes to the user.
4. For each NEEDS-LLM finding (R-NUM-SRC, R-TONE), go back to the thesis sentence or the review text, and write the result of the review in the delivery note.

After a hand edit of a file in responses, build exits with code 4 and check reports R-SYNC. Action: write the hand edits back into the ledger, then run `rebuttal_build.py --force`.
