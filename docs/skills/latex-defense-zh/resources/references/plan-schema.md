# Inventory and Plan Fields

This file specifies the fields, types, and values of the extraction inventory `inventory.json` and of the defense deck plan `slide_plan.yaml`. It also specifies the validation, escaping, and source-text transformation rules of the build script. For the layouts, see [Layout Catalog](slide-layouts.md). For how to write the text, see [Content Rules](content-rules.md). For the page counts and the seconds, see [Time Budget](time-budget.md).

## Pipeline

```bash
uv run python -B $SKILL_DIR/scripts/extract_thesis.py --thesis <THESIS_REPO> --out inventory.json [--main FILE] [--json]
uv run python -B $SKILL_DIR/scripts/plan_deck.py --inventory inventory.json --out slide_plan.yaml [--minutes 40] [--stage predefense|defense] [--theme yanshan|generic]
uv run python -B $SKILL_DIR/scripts/plan_deck.py --plan slide_plan.yaml --outline
uv run python -B $SKILL_DIR/scripts/build_deck.py --plan slide_plan.yaml --inventory inventory.json --out DIR [--logo PATH] [--force] [--compile]
```

1. `extract_thesis.py` reads the thesis repository in read-only mode and writes the inventory.
2. `plan_deck.py` makes the plan skeleton from the inventory. It writes a placeholder into each field to fill.
3. The LLM fills the placeholders as [Content Rules](content-rules.md) specifies. `--outline` prints the frame titles and the takeaway sentences in page order for user confirmation.
4. `build_deck.py` validates the plan and writes the defense deck, the speaker notes, and the theme files. With `--compile`, it compiles the deck with latexmk.

| Script              | Exit codes                                                                                                                                                                                 |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `extract_thesis.py` | 0: success, also when there are warnings; 2: the thesis directory does not exist, the main file is missing, or there are two or more main file candidates and the user did not specify one |
| `plan_deck.py`      | 0: success; 2: an argument error, an input file that the script cannot read, or minutes and chapter roles outside the scope of [Time Budget](time-budget.md)                               |
| `build_deck.py`     | 0: success; 2: an input error or a validation failure; 4: the output directory already contains an owned file and `--force` is absent; 5: latexmk is not found, or the compilation fails   |

## Inventory

The inventory is a UTF-8 JSON file. The inventory contains the absolute path of the thesis root directory. Keep the inventory in the user working directory. Do not commit it to a public repository.

The source location field `source` has the form “file path relative to the thesis root:line number”, for example `chapters/chapter3.tex:20`.

In this file, “plain text” is the result of these steps: remove `\label`, the citation commands, and `\footnote`; replace `\\` and `~` with a space; keep only the argument text of format commands (for example `\textbf`); remove all other command names and braces.

### Top-Level Fields

| Field          | Type            | Description                                                                      |
| -------------- | --------------- | -------------------------------------------------------------------------------- |
| `thesis_root`  | string          | Absolute path of the thesis root directory, with `/` separators                  |
| `main_tex`     | string          | Main file, relative to the thesis root                                           |
| `degree`       | string          | `doctor`, `master`, or `unknown`, from the document class options                |
| `meta`         | mapping         | Cover fields                                                                     |
| `logo`         | string or null  | School logo file, relative to the thesis root                                    |
| `graphicspath` | list of strings | Entries of `\graphicspath` in the main file, relative to the main file directory |
| `chapters`     | list            | Chapter tree                                                                     |
| `figures`      | list            | Figures                                                                          |
| `tables`       | list            | Tables                                                                           |
| `equations`    | list            | Numbered equations with labels                                                   |
| `algorithms`   | list            | Algorithms                                                                       |
| `publications` | list            | Achievements during the degree study                                             |
| `conclusion`   | mapping         | Contribution and outlook items of the conclusion chapter                         |
| `macros`       | list            | Macro definitions in the preamble                                                |
| `warnings`     | list            | Extraction warnings                                                              |

Main file selection: `--main` has priority. Otherwise, the candidates are the files in the thesis root directory that contain both `\documentclass` and `\begin{document}` and that have the extension `.tex`. If there are two or more candidates, the script removes each candidate whose file name contains `blind`, `anon`, `review` (case-insensitive), or “盲审” (blind review). If one candidate remains, the script selects it and writes the warning `W-MAIN`. Otherwise, the script exits with code 2.

The script expands `\input`, `\include`, and `\subfile` in the main file in document order. It removes comments before parsing.

### Cover Fields: meta

| Field                                 | Value rule                                                                                                                                                               |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `title_zh`, `title_en`                | The two arguments of `\title{中文题目}{英文题目}` (Chinese title, English title); with one argument, only `title_zh`                                                     |
| `author`, `school`, `subject`, `date` | The first argument of the command with the same name                                                                                                                     |
| `supervisor`, `supervisor_title`      | The first two arguments of `\supervisor`: the name and the academic title                                                                                                |
| `title_lines`                         | The lines of the definition body of the preamble macro whose name ends with `titlelines`, split at `\\`; if there is no such macro, a list that contains only `title_zh` |

The field values are plain text. When `title_zh`, `author`, `supervisor`, `school`, `subject`, or `date` is missing, the value is an empty string, and the script writes the warning `W-META`. The script does not parse the key-value settings of other document classes (for example `\thusetup{…}`). Fill the missing fields in the plan `meta`.

### Chapter Tree: chapters

| Field             | Type             | Description                                                                                                                           |
| ----------------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `number`          | integer          | Chapter number: the position of each unstarred `\chapter` in the main matter, from 1; the count stops at `\appendix` or `\backmatter` |
| `title`           | string           | Chapter title (long title)                                                                                                            |
| `short_title`     | string or null   | The short title (the bracket argument) in `\chapter[短题]{长题}`                                                                      |
| `source`          | string           | Source location                                                                                                                       |
| `role_suggestion` | string           | Suggested chapter role: `intro`, `foundation`, `research`, `application`, or `conclusion`                                             |
| `role_evidence`   | string           | Reason for the suggestion                                                                                                             |
| `role`            | string, optional | Chapter role that the user specifies; when present, `plan_deck.py` uses this value instead of `role_suggestion`                       |
| `sections`        | list             | Sections: `number` (`k.m`), `title`, `short_title`, `source`, `kind`, `subsections`                                                   |

For the chapter role hints, see [Defense Deck Framework](defense-framework.md). If a suggestion is wrong, add the `role` field to the chapter entry, and run `plan_deck.py` again.

The section type `kind` comes from the section title: “引言” (introduction) or “概述” (overview) gives `intro`; “问题描述”, “问题定义”, or “问题建模” (problem description, definition, or modeling) gives `problem`; “实验”, “仿真”, “案例”, or “结果” (experiment, simulation, case, or result) gives `experiment`; “小结” (summary) gives `summary`; all other titles give `method`. Each item of `subsections` contains `number` (`k.m.p`), `title`, `short_title`, and `source`.

### Figures: figures

| Field                   | Type           | Description                                                                                                                  |
| ----------------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `label`                 | string         | The first top-level `\label` in the environment; without a label, `auto:fig:<章号>-<序号>` (chapter number, sequence number) |
| `number`                | string         | Thesis figure number, for example `3-2`                                                                                      |
| `number_source`         | string         | `aux` or `computed`                                                                                                          |
| `caption`               | string         | Caption source text                                                                                                          |
| `chapter`               | integer        | Chapter number                                                                                                               |
| `section`, `subsection` | string or null | Section number and subsection number, for example `3.3`, `3.3.2`                                                             |
| `files`                 | list           | One item for each `\includegraphics`: `path`, `resolved`, `exists`                                                           |
| `subfigures`            | list           | Subfigures: `letter`, `caption`, `file`, `label`, `number`                                                                   |
| `source`                | string         | Source location                                                                                                              |

- Scope: figures with a caption in the `figure` and `figure*` environments.
- Number: when any `*.aux` file under the thesis root gives the label number in `\newlabel`, the script uses that number, and `number_source` is `aux`. When it reads aux files, the script skips directories whose names start with `.`. When two or more files contain the same label, the file at the shallowest directory level wins. Otherwise, the script calculates the number from the order of appearance in the chapter as “chapter number + separator + sequence number”, and `number_source` is `computed`. The separator is `-` or `.`, as the aux numbers use it; without aux files, it is `-`.
- Caption: from `\bicaption`, the Chinese argument; from `\caption`, the long title. The script removes `\label` and keeps all other source text.
- Image files: `path` is the original string in the source file. `resolved` is the file that the script finds, relative to the thesis root. The search order is each entry of `graphicspath`, then the main file directory. When the original path has no extension, the script tries `.pdf`, `.png`, `.jpg`, `.jpeg`, and `.eps` in this order. When the file does not exist, `exists` is `false`, and the script writes the warning `W-FIG-FILE`.
- Subfigures: from `\subcaptionbox` and the `subfigure` environment. The letters are a, b, c, and so on, in order of appearance. A subfigure from `\subcaptionbox*` has no letter. The subfigure number comes from aux first; otherwise, it is “figure number(letter)”. `file` is the original string of the first `\includegraphics` in the subfigure.

### Tables: tables

For tables, the rules for `label` (without a label, `auto:tab:<章号>-<序号>`), `number`, `number_source`, `caption`, `chapter`, `section`, `subsection`, and `source` are the same as for figures. Tables have one more field:

| Field            | Type           | Description                                                                                                                                                              |
| ---------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `tabular_source` | string or null | The original text of the first `tabular`, `tabular*`, `tabularx`, `xltabular`, or `longtable` environment in the table environment, from `\begin` to the matching `\end` |

Scope: tables with a caption in the `table` and `table*` environments. When the script finds no table body, `tabular_source` is null, and the script writes the warning `W-TABLE-BODY`.

### Equations: equations

Scope: unstarred `equation`, `align`, `gather`, `multline`, `flalign`, and `eqnarray` environments that have at least one numbered label.

| Field                              | Type   | Description                                                       |
| ---------------------------------- | ------ | ----------------------------------------------------------------- |
| `label`, `number`, `number_source` | string | Values of the first label                                         |
| `labels`                           | list   | All labels; each item contains `label`, `number`, `number_source` |
| `env`                              | string | Environment name                                                  |
| `tex`                              | string | The original text between `\begin{…}` and `\end{…}`               |

`chapter`, `section`, `subsection`, and `source` are the same as for figures.

The calculated numbers use a count in each chapter. `equation` and `multline` count as 1 number. The other environments split into rows at top-level `\\`, and each nonempty row counts as 1 number. A row with `\notag` or `\nonumber` has no number; the script records a label in such a row only when aux gives it a number. A row with `\tag{x}` has the number x and does not increase the count.

### Algorithms: algorithms

Scope: algorithms with a caption in the `algorithm` environment. The fields are `label` (without a label, `auto:alg:<章号>-<序号>`), `number`, `number_source`, `caption`, `chapter`, `section`, `subsection`, and `source`. The inventory does not record the algorithm body. This version has no algorithm layout.

### Publications: publications

| Field      | Type             | Description                                                                                    |
| ---------- | ---------------- | ---------------------------------------------------------------------------------------------- |
| `id`       | string           | `P1`, `P2`, and so on, in order of appearance                                                  |
| `category` | string           | Category: the plain text of the previous `\achievementcategory{…}` or `\section*{…}`           |
| `text`     | string           | Plain text of the reference entry, without the chapter mark                                    |
| `chapters` | list of integers | Chapter numbers from the chapter mark, in ascending order; an empty list when there is no mark |

- The script searches for the achievement block in this order and uses the first result: the argument of `\achievement{…}`; the `achievements` environment; a `\chapter` or `\chapter*` whose title contains “成果” (achievements) or “发表的学术论文” (published papers), up to the next `\chapter`. Each `\item` in the block gives one publication. When there is no publication, the script writes the warning `W-PUB`.
- Examples of the chapter mark: “对应论文第三、四章”, “对应第3-5章”, and “（对应本文第2章和第4章）” (corresponds to chapters 3 and 4, to chapters 3 to 5, and to chapters 2 and 4). The chapter numbers can be Arabic numerals or Chinese numerals (一 to 九十九, that is, 1 to 99). “至”, “-”, “~”, “—”, and “–” mark a range. “、”, “，”, “和”, “及”, and “与” separate two or more chapter numbers.

### Conclusion: conclusion

| Field           | Type            | Description                                                                      |
| --------------- | --------------- | -------------------------------------------------------------------------------- |
| `chapter`       | integer or null | Conclusion chapter number: the last chapter whose suggested role is `conclusion` |
| `contributions` | list of strings | Contribution items                                                               |
| `outlook`       | list of strings | Outlook items                                                                    |

The items come from the `\item` entries of top-level lists and from paragraphs that start with a number such as “（1）”, “(1)”, “1.”, or “1、”. Items after the first heading or paragraph that contains “展望” (outlook), “未来” (future), “今后” (from now on), or “下一步” (next step) go to `outlook`. Items before it go to `contributions`. The script removes the number at the start of each item. When there is no conclusion chapter, the script writes the warning `W-CONCLUSION`.

### Macros: macros

| Field        | Type   | Description                                                                                                                |
| ------------ | ------ | -------------------------------------------------------------------------------------------------------------------------- |
| `name`       | string | Macro name, without the backslash                                                                                          |
| `command`    | string | Definition command: `newcommand`, `renewcommand`, `providecommand`, `DeclareMathOperator` (with an optional `*`), or `def` |
| `definition` | string | Original text of the definition                                                                                            |
| `source`     | string | Source location                                                                                                            |

The scope is the preamble of the main file, including the files that the preamble expands.

### School Logo: logo

The script searches for the logo in each directory of `graphicspath`. Without `graphicspath`, it searches the main file directory. When exactly one image has a file name stem that contains `logo`, `badge` (case-insensitive), or “校徽” (school logo), `logo` is its path. Otherwise, the value is null, and the script writes the warning `W-LOGO`.

### Warnings: warnings

Each warning contains `code`, `message`, and `source` (can be null).

| Code           | Condition                                                                                                                   |
| -------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `W-MAIN`       | Two or more main file candidates; one remains after the script removes the blind-review versions, and the script selects it |
| `W-META`       | A cover field is missing                                                                                                    |
| `W-ENCODING`   | A source file is not UTF-8, and the script decoded it as GB18030; or some characters cannot be decoded                      |
| `W-INCLUDE`    | The target file of `\input`, `\include`, or `\subfile` does not exist                                                       |
| `W-FIG-FILE`   | An image file does not exist                                                                                                |
| `W-TABLE-BODY` | A table environment contains no table body environment                                                                      |
| `W-PUB`        | There is no achievement list, or the list has no items                                                                      |
| `W-CONCLUSION` | The script finds no conclusion chapter                                                                                      |
| `W-LOGO`       | The script finds no logo file, or finds two or more candidates                                                              |

## Plan

The plan is a UTF-8 YAML file. `plan_deck.py` makes the skeleton. The LLM fills the placeholders and, as necessary, changes the layouts, the selected figures and tables, and `meta`.

### Placeholder

The skeleton writes the placeholder `〔待填写〕` (to be filled) into each field to fill. On content pages, these fields are `takeaway`, each item of `bullets`, `notes.say`, `notes.key`, `notes.transition`, and each item of `notes.questions`. On the cover and the TOC frames, these fields are `notes.say` and `notes.transition`. On the thanks frame, `notes.say` has the preset text “汇报完毕，请各位老师批评指正。” (This concludes my presentation. Please give your comments.)

The last line of `--outline` gives the frame count, the content page count, and the placeholder count. `build_deck.py` does not check placeholders. The quality gate reports the remaining placeholders.

### Plan meta

| Field                                                                   | Type             | Description                                                     |
| ----------------------------------------------------------------------- | ---------------- | --------------------------------------------------------------- |
| `stage`                                                                 | string           | `predefense` (pre-defense) or `defense` (defense)               |
| `theme`                                                                 | string           | `yanshan` or `generic`                                          |
| `minutes`                                                               | positive integer | Presentation minutes; the default is 40                         |
| `title_lines`                                                           | list of strings  | Lines of the cover title                                        |
| `author`, `supervisor`, `supervisor_title`, `subject`, `school`, `date` | string           | Cover fields; the initial values come from the inventory `meta` |
| `logo`                                                                  | string or null   | School logo file, relative to the thesis root                   |
| `inventory_sha256`                                                      | string           | SHA-256 of the inventory file when the script made the skeleton |
| `extra_packages`                                                        | list of strings  | Names of additional packages                                    |
| `chapters`                                                              | list             | One item for each chapter: `number`, `title`, `role`            |

- `stage` and `minutes` set the page order and the seconds for each page when the script makes the skeleton. A change to these two fields after that does not add or remove frames. To change the stage or the duration, run `plan_deck.py` again. The `defense` stage adds the achievements page `achievements` after the outlook page. `stage` also sets the stage text on the cover.
- Each item of `extra_packages` must match `^[A-Za-z0-9-]+$`. The deck loads each item with `\usepackage` after the fixed packages. The fixed packages are amsmath, amssymb, mathtools, bm, booktabs, multirow, makecell, tabularx, array, threeparttable, siunitx, and adjustbox.
- In `chapters`, `title` uses the short title first. The build script makes the chapter list of the TOC pages from `chapters`.

### Frame Sequence and IDs

The frame sequence is: the cover `cover`; the overall TOC `toc`; the pages of chapter 1; for each chapter k (k ≥ 2), the chapter TOC `c<k>-toc` and the pages of chapter k; the thanks page `thanks`. A content page ID is `c<k>-<role>`. When one chapter has two or more pages with the same role, the ID is `c<k>-<role>-<i>`, where i starts at 1.

### Frame Fields

| Field        | Type             | Description                                                                                                                                                                                 |
| ------------ | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`         | string           | Frame ID; unique in the deck; matches `^[A-Za-z0-9][A-Za-z0-9_-]*$`                                                                                                                         |
| `role`       | string           | Page role; see [Defense Deck Framework](defense-framework.md)                                                                                                                               |
| `layout`     | string           | Layout name; see [Layout Catalog](slide-layouts.md)                                                                                                                                         |
| `chapter`    | integer or null  | Chapter number; null for the cover and the thanks page; 0 for the overall TOC                                                                                                               |
| `section`    | string           | Frame title                                                                                                                                                                                 |
| `subsection` | string           | Subsection bar; not shown when empty                                                                                                                                                        |
| `position`   | string           | Only for `figure-bullets`: `left` (default) or `top`                                                                                                                                        |
| `takeaway`   | string           | Takeaway sentence                                                                                                                                                                           |
| `bullets`    | list of strings  | Bullets; the `cards` layout shows one card for each bullet, and the `outlook` layout shows one item for each bullet                                                                         |
| `figures`    | list of mappings | Each item contains `label` and can contain `subfigures` (a list of subfigure letters) and `width` (the figure width as a fraction of the line width, greater than 0 and not greater than 1) |
| `equations`  | list of mappings | Each item contains `label`, which is any label of the equation                                                                                                                              |
| `table`      | string or null   | Table label                                                                                                                                                                                 |
| `paper`      | string or null   | Publication ID; shown as the “论文” (paper) box                                                                                                                                             |
| `notes`      | mapping          | Speaker notes: `say`, `key`, `seconds` (integer), `transition`, `questions` (list of strings)                                                                                               |
| `source`     | list of strings  | Source locations of the mapped sections and of the selected figures and tables; read-only, not rendered                                                                                     |
| `hints`      | list of strings  | Section titles, figure and table captions, research contents, conclusion items, or publication entries; read-only, not rendered                                                             |

Frames with the `cover`, `toc`, and `thanks` layouts use only `id`, `role`, `layout`, `chapter`, and `notes`. `width` has no effect in `figure-grid`.

### Skeleton Prefill Rules

| Field                           | Prefill rule                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `layout`                        | Selected from the page role and the candidate figures and tables; see the next table                                                                                                                                                                                                                                                                                                                                                  |
| `section`                       | “section number section title” of the first mapped section (short title first); the chapter title when no section maps to the page                                                                                                                                                                                                                                                                                                    |
| `subsection`                    | For the `intro` page of a research chapter, “研究内容 i：章题” (research content i: chapter title); for the `innovation`, `outlook`, and `achievements` pages, “01　主要创新点”, “02　未来研究展望”, and “03　攻读学位期间取得的成果” (main innovations, future research outlook, achievements during the degree study); “subsection number subsection title” when the page maps to exactly one subsection; otherwise an empty string |
| `figures`, `equations`, `table` | The first candidate in the mapped sections, in order of appearance, that no earlier page uses                                                                                                                                                                                                                                                                                                                                         |
| `bullets`                       | An empty list for the `figure`, `figure-grid`, and `table` layouts; for `challenges` and `innovation`, one item for each research chapter; for `outlook`, one item for each outlook item of the conclusion, 3 items at most, or 2 items when there are no outlook items; otherwise 1 item                                                                                                                                             |
| `paper`                         | For a `summary` page, the first publication whose chapter mark includes this chapter; the other publications of the same chapter go to `hints`                                                                                                                                                                                                                                                                                        |
| `notes.seconds`                 | The seconds for each page from the time budget                                                                                                                                                                                                                                                                                                                                                                                        |

| Page role                                | Default layout                                                                                                                                                                                             |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `challenges`, `innovation`               | `cards`                                                                                                                                                                                                    |
| `summary`                                | `paper-summary`                                                                                                                                                                                            |
| `outlook`                                | `outlook`                                                                                                                                                                                                  |
| `method`, `foundation`                   | `equations-figure` when there is an equation candidate; otherwise `figure-bullets` when there is a figure candidate; otherwise `bullets`                                                                   |
| `experiment`                             | `figure` when there is a figure candidate, and `figure-grid` when that figure has at least 2 subfigures with letters; `table` when there is a table candidate and no figure candidate; otherwise `bullets` |
| `application`                            | `figure` when there is a figure candidate; `table` when there is a table candidate and no figure candidate; otherwise `bullets`                                                                            |
| `status`, `organization`, `architecture` | `figure` when there is a figure candidate; otherwise `bullets`                                                                                                                                             |
| `background`, `problem`, `intro`         | `figure-bullets` when there is a figure candidate; otherwise `bullets`                                                                                                                                     |
| `achievements`                           | `bullets`                                                                                                                                                                                                  |

- Candidate conditions: a figure has at least one `\includegraphics`; the `tabular_source` of a table is not empty and is not a `longtable` or `xltabular` environment.
- `figure-grid` preselects the first 6 subfigure letters. On the `intro` page of a research chapter, `figure-bullets` gets `position: top`; on all other pages, it gets `left`.
- Introduction chapter: the `background`, `status`, `challenges`, and `organization` pages map to the first section whose title contains, respectively, “背景” or “意义” (background, significance); “现状”, “综述”, or “进展” (status, review, progress); “问题” or “挑战” (problem, challenge); “内容”, “安排”, or “组织” (content, arrangement, organization).
- Research chapter: the `intro`, `problem`, and `summary` pages map to the first section of the matching section type. The `method` and `experiment` pages spread over all sections of the matching section type.
- Foundation chapter: the `foundation` pages spread over the sections whose type is not `intro` or `summary`.
- Application chapter: the `intro` page maps to the section of type `intro`, or to the first section when there is none. The `architecture` page maps to the section whose title contains “架构”, “总体”, “框架”, or “结构” (architecture, overall, framework, structure). The `application` pages spread over the remaining sections, except sections of type `summary`.
- Conclusion chapter: the pages do not map to sections.
- Distribution rule: when the page count is not greater than the section count, adjacent sections share one page. The section counts of the pages differ by 1 at most, and the earlier pages get the extra sections. When the page count is greater than the section count, each section gets at least one page. When a section gets two or more pages, the same rule spreads these pages over the subsections of that section.

## Build Rules

### Validation

If any of these conditions is not true, `build_deck.py` lists all errors, exits with code 2, and writes no file:

- Plan: `meta` is a mapping; `meta.stage` and `meta.theme` have valid values; `meta.minutes` is a positive integer; `meta.title_lines` is a list; each item of `meta.chapters` is a mapping that contains `number` and `title`; each item of `meta.extra_packages` obeys the package name rule; `frames` is a nonempty list; each frame ID obeys the ID rule and is unique.
- Frame: `role` and `layout` are in the permitted sets; the `chapter` of a TOC frame is 0 or a chapter number; `notes` is a mapping, `notes.seconds` is an integer, and `notes.questions` is a list; `bullets` is a list.
- References: each item of `figures` is a mapping that contains `label`, and the label is in the inventory; each selected subfigure letter exists, and that subfigure has an image file; `width` is greater than 0 and not greater than 1; in layouts other than `figure-grid`, the figure has at least one image file; the labels or IDs that `equations`, `table`, and `paper` refer to are in the inventory.
- Layouts: `figure`, `figure-bullets`, and `figure-grid` have exactly 1 figure; `figure-grid` selects 2–6 subfigure letters; `equations-figure` has 1–4 equations and 1 figure at most; the `table` layout has the `table` field, the referenced table has a table body, and the table body is not a `longtable` or `xltabular` environment.
- Command line: the `--logo` file exists; `--out` is not an existing regular file.

In these cases, the script only writes a warning and continues the build: `meta.inventory_sha256` does not agree with the current inventory; a field does not show in the selected layout, for example, the `figure` layout does not show `bullets`; a figure has two or more image files, and the deck shows only the first; the logo file does not exist; the thesis repository and the output directory are on different drives. The script writes the warnings to standard output and to `build_manifest.json`.

### Text Escaping

Escaping applies to these plan fields: `section`, `subsection`, `takeaway`, `bullets`, the cover fields in `meta`, the chapter titles in `meta.chapters`, and the publication entry text. The rules apply in this order:

1. A sequence of whitespace (line breaks included) becomes one space.
2. `**词**` (word) becomes `\DefenseHighlight{词}`. An unpaired `**` stays as plain characters.
3. The other characters change as the next table shows.

| Character               | Output                     |
| ----------------------- | -------------------------- |
| `\`                     | `\textbackslash{}`         |
| `{`, `}`                | `\{`, `\}`                 |
| `$`, `&`, `#`, `%`, `_` | A `\` before the character |
| `~`                     | `\textasciitilde{}`        |
| `^`                     | `\textasciicircum{}`       |

A bullet that starts with `[` or `<` gets a `{}` prefix, so that `\item` does not read it as an optional argument or an overlay specification. A title line that starts with `[` or `*` gets a `{}` prefix. Text fields do not support inline math or LaTeX commands. Use the `equations` field for equations.

### Captions

A figure caption is `图<编号>\quad` (figure, number) followed by the caption source text in the `DefenseSource` environment. A table caption is `表<编号>\quad` (table, number) followed by the caption source text. A subfigure caption is `(<字母>)` (letter) followed by the subfigure caption source text. The script does not escape caption source text. In the `DefenseSource` environment, `\ref` and `\eqref` print the thesis number, and the citation commands print nothing.

### Equations

- The output is `\begin{<env>*}`, the transformed body, and `\end{<env>*}`, all in the `DefenseSource` environment.
- Transformed body: in the inventory `tex`, each `\label{x}` becomes `\tag*{(<x 的编号>)}` (number of x). All other characters stay the same.
- The script removes these labels and adds no `\tag*`: a label in a row that already has `\tag`; each label after the first in a row; a label without a number in the inventory; all labels of `eqnarray`. `eqnarray*` does not support `\tag`, so the numbers show below the equation, for example `(4-1)\quad (4-2)`.
- The rows are the same as in the inventory number calculation: `equation` and `multline` are one row; the other environments split into rows at top-level `\\`.
- When the script removed no label, change each `\tag*{(<编号>)}` (number) in the transformed body back to its `\label{x}`. The result is identical to the inventory `tex`, character by character.

Transformation example (the first block is the thesis environment that contains the inventory `tex`; the second block is the deck output):

```latex
\begin{align}
  \vect{h}_{t} &= \sigma\left(W_{x}\vect{x}_{t} + W_{h}\vect{h}_{t-1}\right) \label{eq:c4-hidden}\\
  \vect{z}_{t} &= \operatorname{concat}\left(\vect{h}_{t}, \vect{s}_{t}\right) \nonumber\\
  \hat{\vect{y}}_{t+1} &= W_{o}\vect{z}_{t} + b \label{eq:c4-output}
\end{align}
```

```latex
\begin{DefenseSource}
\begin{align*}
  \vect{h}_{t} &= \sigma\left(W_{x}\vect{x}_{t} + W_{h}\vect{h}_{t-1}\right) \tag*{(4-1)}\\
  \vect{z}_{t} &= \operatorname{concat}\left(\vect{h}_{t}, \vect{s}_{t}\right) \nonumber\\
  \hat{\vect{y}}_{t+1} &= W_{o}\vect{z}_{t} + b \tag*{(4-2)}
\end{align*}
\end{DefenseSource}
```

### Table Bodies

The original text of `tabular_source` stays the same. It goes in the `DefenseSource` environment, and then in `\adjustbox{max width=\textwidth,max totalheight=0.62\textheight}`. The table caption is above the table body. `longtable` and `xltabular` do not compile in `\adjustbox`. Thus `plan_deck.py` does not preselect such tables, and `build_deck.py` exits with code 2 when it finds one.

### Figure and Logo Paths

- The entries of `\graphicspath` are the `graphicspath` entries under the main file directory and the main file directory itself. Each entry is a path relative to the output directory, with `/` separators, and ends with `/`. When the output directory and the thesis repository are on different drives, the script writes an absolute path and a warning.
- For the file argument of `\DefenseFigure`, the script uses the first item of the inventory `files` and writes its original `path` string. The `figure-grid` layout uses the `file` of each selected subfigure.
- The logo path priority is `--logo`, then the plan `meta.logo`, then the inventory `logo`. The last two are relative to the thesis root. When the logo file does not exist, the script writes a warning, and the cover shows the text mark or no logo, as the theme specifies.

### Macros

`thesis-macros.tex` collects the thesis macros that the selected figure captions and subfigure captions, equations, table captions, and table bodies use. It also adds, recursively, the macros that the definitions of these macros use. The macros are in preamble order. Before each macro, a comment line gives the source location:

- The script changes `\newcommand`, `\renewcommand`, and `\providecommand` definitions to `\providecommand`.
- The script puts `\DeclareMathOperator` and `\def` definitions in `\ifdefined\<名>\else … \fi` (name).

### Labels and Numbers

The preamble of `defense.tex` has one line `\DefenseDefineLabel{<label>}{<编号>}` (label, number) for each figure, subfigure, table, algorithm, and equation label in the inventory. Synthetic labels that start with `auto:` are not included. In the `DefenseSource` environment, `\ref{<label>}` prints the thesis number, and `\eqref` adds parentheses. A label that is not registered prints `??`.

### Output Files

| File                                                                                    | Content                                                                                                                                            |
| --------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `defense.tex`                                                                           | Defense deck                                                                                                                                       |
| `thesis-macros.tex`                                                                     | Thesis macros                                                                                                                                      |
| `notes.md`                                                                              | Speaker notes; for the format, see [Speaker Notes Format](speaker-notes.md)                                                                        |
| `build_manifest.json`                                                                   | Skill version, theme, stage, frame count, SHA-256 of the plan and of the inventory, SHA-256 of the other six files, and the warnings; no timestamp |
| `beamerthemeYanshanDefense.sty`, `beamerthemeGenericDefense.sty`, `defense-layouts.sty` | Copies of the theme and layout packages                                                                                                            |

These seven files are the owned files of the build script. If an owned file exists and `--force` is absent, the build script exits with code 4 and writes no file. `--force` overwrites only the owned files. It does not delete other files in the output directory.

`defense.tex` has a frame marker on the line before each `\begin{frame}`. The quality gate uses the frame markers to map line numbers, page roles, and page order:

```latex
% defense-frame: id=<id> role=<role> chapter=<n|-> layout=<layout>
```

When `chapter` is null, the marker has `-`.

With `--compile`, the build script runs `latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error defense.tex` in the output directory, with a time limit of 600 seconds. When the compilation fails, the build script writes the last 40 lines of `defense.log` to standard error and exits with code 5.

## Known Limitations

- Text fields do not support inline math or LaTeX commands.
- When the thesis changes a standard command with `\renewcommand`, the deck keeps the standard definition, because `\providecommand` does not replace an existing definition.
- The script does not copy macros that the document class or a package of the thesis defines. When the compilation reports an undefined command, add the necessary package to `meta.extra_packages`, or select figures and tables that do not use that command.
- Tables with `longtable` or `xltabular` cannot use the `table` layout.
- A figure without `\includegraphics` (for example, a figure drawn with TikZ) cannot use a figure layout.
- The script extracts the conclusion items with the suggested roles. When the `role` field changes a chapter role, the script does not extract `conclusion` again.
- The script does not parse the key-value cover settings of other document classes (for example `\thusetup{…}`).
- File expansion processes only `\input`, `\include`, and `\subfile`.
