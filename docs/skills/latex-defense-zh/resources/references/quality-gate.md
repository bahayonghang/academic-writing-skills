# Quality Gate

This file specifies the D-* codes, criteria, thresholds, severities, and fixes of the defense deck quality gate `check_deck.py`. It also specifies the use of the preview script `render_preview.py` and the visual checklist. For the page roles, see [Defense Deck Framework](defense-framework.md). For the layouts, see [Layout Catalog](slide-layouts.md). For how to write the text, see [Content Rules](content-rules.md). For the page counts and the seconds, see [Time Budget](time-budget.md). For the notes format, see [Speaker Notes Format](speaker-notes.md). For the plan fields, see [Inventory and Plan Fields](plan-schema.md).

## Usage

```bash
uv run python -B $SKILL_DIR/scripts/check_deck.py --deck DIR/defense.tex --inventory inventory.json [--plan slide_plan.yaml] [--log DIR/defense.log] [--minutes 40] [--json]
uv run python -B $SKILL_DIR/scripts/render_preview.py --pdf DIR/defense.pdf --out DIR/preview [--dpi 110] [--cols 4]
```

- `check_deck.py` reads the defense deck, the `notes.md` and the `defense.log` in the same directory, the inventory, and the thesis source files. It does not write files.
- When `--log` is absent, the script uses the `defense.log` in the deck directory. When that file does not exist, D-COMPILE, D-OVERFLOW-V, and D-OVERFLOW-H go into `skipped`.
- With `--plan`, the chapter roles and the stage come from the plan. Without a plan, the script infers the chapter roles from the page roles in the frame markers. The minutes come from `--minutes`, then from the plan `meta.minutes`, then from the default 40.
- When the script cannot read the thesis repository, D-NUM-SRC goes into `skipped`. When the script cannot find the role of each chapter, it does not do the content frame count check of D-BUDGET, and D-BUDGET goes into `skipped`. The check of the total notes seconds runs in all cases.

| Script              | Exit codes                                                                                                                                                                                                                                     |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `check_deck.py`     | 0: no Critical or Major finding; 1: one or more Critical or Major findings; 2: the deck does not exist, the script cannot read the inventory or the plan, the file that `--log` gives does not exist, or `--minutes` is not in the range 15–90 |
| `render_preview.py` | 0: success; 2: the PDF does not exist or the script cannot open it, or `--dpi` or `--cols` is not a positive integer; 3: PyMuPDF is not installed                                                                                              |

## Output Format

In text mode, each finding is one line. The last line is the summary:

```text
% D-NUM-SRC (frame=c3-experiment-2, defense.tex:271) [Severity: Major] [Priority: P1]: [Script] Meaning-Check: NEEDS-LLM：数字 37.25 在论文全文中没有同形数字；回到论文原句核对
% 汇总：Critical 0，Major 1，Minor 0，Info 0；skipped：D-COMPILE、D-OVERFLOW-V、D-OVERFLOW-H
```

- `frame` is the id in the frame marker. For a frame without a marker, the value is `#` and the frame index, for example `#17`. For preamble fields, whole-deck counts, and log lines that do not map to a frame, the value is `-`.
- The location has the form “file:line”. A finding in the speaker notes gives `notes.md`. A log finding that does not map to a deck line gives `defense.log`. A missing or old PDF gives `defense.pdf`. When there is no line number, the line is `-`.
- A log finding that maps to a frame gives the log line number at the end of the message, for example “（defense.log:1234）”.
- A NEEDS-LLM finding has `Meaning-Check: NEEDS-LLM：` before the message.
- The findings are in frame order, and the findings with `frame=-` come first. In one frame, the order is by code, file, and line.

`--json` gives the structure below. The `source_kind` of each finding is always `script`. The `meaning_check` is `NEEDS-LLM` or an empty string.

```json
{
  "deck": "defense.tex",
  "findings": [
    {
      "code": "D-NUM-SRC",
      "severity": "Major",
      "priority": "P1",
      "source_kind": "script",
      "frame": "c3-experiment-2",
      "line": 271,
      "file": "defense.tex",
      "message": "数字 37.25 在论文全文中没有同形数字；回到论文原句核对",
      "meaning_check": "NEEDS-LLM"
    }
  ],
  "summary": { "Critical": 0, "Major": 1, "Minor": 0, "Info": 0 },
  "skipped": ["D-COMPILE", "D-OVERFLOW-V", "D-OVERFLOW-H"]
}
```

## Severities

| Severity | Priority | Action                                                                                   |
| -------- | -------- | ---------------------------------------------------------------------------------------- |
| Critical | P0       | An academic fact error or a compilation failure. Fix it before delivery                  |
| Major    | P1       | Fix it before delivery. If the finding is not correct, tell the user the reason          |
| Minor    | P2       | A fix is recommended. If the finding stays after the fix loop, tell the user at delivery |
| Info     | P3       | Information only. The deck does not need a change                                        |

## Code Table

In this section, “visible characters” are the characters that stay in a frame after the script removes comments, `DefenseSource` environments, the frame title, figure file arguments, and environment arguments, and then deletes command names and braces. Whitespace does not count. A “content frame” is a frame whose page role is not cover, toc, thanks, or backup.

### Structure

| Code          | Meaning                                            | Criterion                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Severity   | Fix                                                                                                                                            |
| ------------- | -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| D-MARKER      | Frame marker                                       | The last non-blank line before the frame is not a frame marker                                                                                                                                                                                                                                                                                                                                                                                                          | Minor / P2 | The build script makes the deck. Run `build_deck.py` again. Do not edit `defense.tex` by hand                                                  |
| D-MARKER      | Frame marker                                       | The role of the marker is not a page role, the layout is not a layout name, or the chapter is not an integer or `-`; or the id is the same as the id of an earlier frame                                                                                                                                                                                                                                                                                                | Major / P1 | Change the fields of the frame in the plan, then build again                                                                                   |
| D-COVERAGE    | Complete framework                                 | The first frame (backup pages excluded) is not cover, or the last frame is not thanks; the introduction chapter does not have one of background, status, challenges, organization; the foundation chapter does not have foundation; a research chapter does not have one of intro, problem, method, experiment, summary; the application chapter does not have one of intro, architecture, application; the conclusion chapter does not have one of innovation, outlook | Major / P1 | Add the missing page roles in the plan                                                                                                         |
| D-TOC         | Table of contents                                  | The second frame is not `\DefenseTocFrame{0}`; from chapter 2 on, a chapter has no chapter TOC, the argument of the chapter TOC is not the chapter number, or the chapter TOC is not immediately before the first frame of the chapter                                                                                                                                                                                                                                  | Major / P1 | Put the toc frame of the chapter back into the plan, immediately before the first frame of the chapter                                         |
| D-CHAIN       | Problems, research chapters, and innovations match | The card count of the challenges frame or of the innovation frame is not equal to the count of research chapter intro frames; the subsection bar of a research chapter intro frame is not “研究内容 i：章题” (research item i: chapter title), where i is the position of the chapter among the research chapters                                                                                                                                                       | Major / P1 | Make the problem cards, the research chapters, and the innovation cards match one to one; change the subsection bars in research chapter order |
| D-PLACEHOLDER | Placeholders                                       | The deck or the notes contain `〔待填写〕`, `TODO`, `TBD`, or `XXX`                                                                                                                                                                                                                                                                                                                                                                                                     | Major / P1 | Fill the field in the plan, then build again                                                                                                   |

### Figures

| Code          | Meaning                  | Criterion                                                                                                                                                                                                | Severity      | Fix                                                                                                       |
| ------------- | ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | --------------------------------------------------------------------------------------------------------- |
| D-FIG-ALLOW   | Only thesis figures      | The file of `\includegraphics` or `\DefenseFigure` is not an image file of the inventory `figures` (`files[].path`, `files[].resolved`, `subfigures[].file`) and is not the logo file                    | Critical / P0 | Use a figure from the inventory. Do not make new figures. Do not redraw data plots                        |
| D-FIG-MISSING | Figure file exists       | For a permitted image, the search in the deck directory, in `\graphicspath`, and with the extension fallback finds no file                                                                               | Major / P1    | Check the figure files in the thesis repository; after a figure file changes, extract the inventory again |
| D-FIG-NUMBER  | Figure and table numbers | A “图 k-m” (figure k-m) or “表 k-m” (table k-m) in the visible text or in the notes is not an inventory number; or the caption number belongs to a different figure in the inventory                     | Major / P1    | Use the thesis numbers. Change the caption or the notes in the plan                                       |
| D-FIG-ASPECT  | Figure proportions       | A PNG or JPEG bitmap has a height-to-width ratio of more than 1.6 in the figure, figure-grid, or equations-figure layout; or a width-to-height ratio of more than 3 in the left column of figure-bullets | Minor / P2    | Use a different layout or figure position; see [Layout Catalog](slide-layouts.md)                         |

### Source Text

| Code      | Meaning                 | Criterion                                                                                                                                                                               | Severity      | Fix                                                                                                                                    |
| --------- | ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| D-EQ-SRC  | Verbatim equations      | A math environment in `DefenseSource`, after the removal of `\label`, `\tag`, `\notag`, `\nonumber`, and all whitespace, is not equal to an inventory equation                          | Critical / P0 | Build again with the inventory equation. Do not rewrite symbols. Do not merge or split equations                                       |
| D-EQ-SRC  | Verbatim equations      | Outside `DefenseSource`, the deck has a math environment, `\[`, `\(`, `$$`, or an unescaped `$`                                                                                         | Major / P1    | Do not write math in the text fields of the plan. For an equation, use the equations-figure layout with an inventory equation          |
| D-TAB-SRC | Verbatim table bodies   | A table environment in `DefenseSource`, after the removal of all whitespace, is not equal to an inventory table body `tabular_source`                                                   | Critical / P0 | Build again with the inventory table body. Do not change cells                                                                         |
| D-TAB-SRC | Verbatim table bodies   | Outside `DefenseSource`, the deck has a table environment                                                                                                                               | Major / P1    | Show tables only through the table layout with an inventory table                                                                      |
| D-NUM-SRC | Numbers from the thesis | A number in the visible text or in the notes fields “说什么”, “要点”, “过渡”, and “可能提问” has no number of the same form in the full thesis text; the finding has the NEEDS-LLM mark | Major / P1    | Examine each number as the section “NEEDS-LLM Review” specifies                                                                        |
| D-PAPER   | “论文” (paper) box      | The text of `\DefensePaperBox`, after the removal of all whitespace, is not equal to an entry of the inventory publication list                                                         | Critical / P0 | Copy the citation text word for word from the publication list. Do not invent publications                                             |
| D-PAPER   | “论文” box              | The chapters of the publication in the publication list do not include the chapter of the frame                                                                                         | Major / P1    | Use a publication of this chapter                                                                                                      |
| D-PAPER   | “论文” box              | A research chapter has a publication in the publication list, but the summary page of the chapter has no “论文” box                                                                     | Minor / P2    | Add the publication to the summary page                                                                                                |
| D-META    | Cover fields            | A cover field (title, author, supervisor, school, subject, date) is empty; or the title or the author is different from the inventory `meta.title_zh` or `meta.author`                  | Major / P1    | Change the cover fields in the plan `meta`, then build again                                                                           |
| D-META    | Cover fields            | The inventory `meta.title_zh` or `meta.author` is empty, so the script cannot compare                                                                                                   | Info / P3     | Examine the cover title and author manually                                                                                            |
| D-STAGE   | Defense stage           | The stage is not predefense or defense; the stage is different from the plan `meta.stage`; or the defense stage has no achievements frame                                               | Major / P1    | If the deck and the plan do not agree, build again from the plan; to change the stage, make the plan again with `plan_deck.py --stage` |
| D-STAGE   | Defense stage           | The predefense stage has an achievements frame                                                                                                                                          | Minor / P2    | Remove the achievements frame from the plan, or use the defense stage                                                                  |

### Density, Time, and Notes

| Code      | Meaning       | Criterion                                                                                                                                                                                           | Severity   | Fix                                                                                                                                                   |
| --------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| D-DENSITY | Page density  | A content frame has more than 260 visible characters                                                                                                                                                | Major / P1 | Use the overflow handling order in [Content Rules](content-rules.md)                                                                                  |
| D-DENSITY | Page density  | A content frame has 181–260 visible characters; the count of bullets, cards, outlook items, subfigures, or equations is more than the layout limit; a takeaway sentence has more than 40 characters | Minor / P2 | The same. For the layout limits, see [Layout Catalog](slide-layouts.md)                                                                               |
| D-BUDGET  | Page budget   | The content frame count is not in the page range of the time budget                                                                                                                                 | Major / P1 | Add or remove content frames as [Time Budget](time-budget.md) specifies; when the duration changes, make the plan again with `plan_deck.py --minutes` |
| D-BUDGET  | Page budget   | The total of the “时长” (duration) fields in the notes (backup pages excluded) is different from 60 × minutes by more than 10%                                                                      | Minor / P2 | Adjust `notes.seconds` of the frames in the plan                                                                                                      |
| D-NOTES   | Speaker notes | The deck directory has no `notes.md`                                                                                                                                                                | Major / P1 | Run `build_deck.py` again                                                                                                                             |
| D-NOTES   | Speaker notes | A frame has no notes section, or its notes section does not have one of the five fields; the “说什么” field of a content frame is not 150–250 characters                                            | Minor / P2 | Complete the `notes` fields of the frame in the plan                                                                                                  |

### Compilation

| Code         | Meaning             | Criterion                                                                                                                                                                          | Severity      | Fix                                                                                                                             |
| ------------ | ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| D-COMPILE    | Compilation         | The log has an error line (a line that starts with `! `, or with “file:line:”), `Emergency stop`, or `Fatal error`; or `defense.pdf` does not exist or is older than `defense.tex` | Critical / P0 | Find the cause from the log line. For frequent causes, see the known limitations in [Inventory and Plan Fields](plan-schema.md) |
| D-COMPILE    | Compilation         | The log has an undefined cross-reference or citation (`Reference … undefined`, `Citation … undefined`)                                                                             | Major / P1    | Make sure that the label is in the inventory; build again, then compile again                                                   |
| D-OVERFLOW-V | Vertical overflow   | The log has `Overfull \vbox`                                                                                                                                                       | Major / P1    | Use the overflow handling order in [Content Rules](content-rules.md)                                                            |
| D-OVERFLOW-H | Horizontal overflow | The log has `Overfull \hbox` with an overflow of more than 20pt                                                                                                                    | Major / P1    | The same                                                                                                                        |
| D-OVERFLOW-H | Horizontal overflow | The overflow is more than 5pt and not more than 20pt. The script does not report an overflow of 5pt or less                                                                        | Minor / P2    | The same                                                                                                                        |

The script maps a log finding to a frame with these line numbers: the `l.` line number or the “file:line” of an error line, the line number after `detected at line` and `at lines`, and the `on input line` number of an undefined reference. When the line number is in no frame, the finding has `frame=-`.

Exclusions and matching rules of D-NUM-SRC:

- The script does not compare structural numbers: numbers with a separator after “图”, “表”, or “式” (figure, table, equation), “第 k 章” (chapter k), “研究内容 k” (research item k), “k 节” (section k), the section number at the start of a subsection bar, and integers of 10 or less.
- Years are not excluded. A year must occur in the thesis.
- The script splits the text into the longest “digits.digits” strings. Before the comparison, it changes full-width digits to ASCII digits and removes thousands commas between digits. Numbers with different decimal places (for example 12.3 and 12.30) do not match, and the script reports them. The review decides.

## Thresholds

| Threshold                                     | Value     | Code         |
| --------------------------------------------- | --------- | ------------ |
| Visible characters of a content frame (Minor) | 180       | D-DENSITY    |
| Visible characters of a content frame (Major) | 260       | D-DENSITY    |
| Characters of a takeaway sentence             | 40        | D-DENSITY    |
| Characters of “说什么” in a content frame     | 150–250   | D-NOTES      |
| Tolerance of the total notes seconds          | ±10%      | D-BUDGET     |
| Horizontal overflow (Minor, Major)            | 5pt, 20pt | D-OVERFLOW-H |
| Bitmap height-to-width ratio                  | 1.6       | D-FIG-ASPECT |
| Bitmap width-to-height ratio                  | 3         | D-FIG-ASPECT |

The thresholds above are initial values and are not calibrated. The values 180 and 260 and the range 150–250 did not come from a calibration on a corpus of defense decks. Do not adjust the thresholds for one thesis. The layout limits come from [Layout Catalog](slide-layouts.md).

## Fix Loop

1. Run `check_deck.py`.
2. Change `slide_plan.yaml` as each code specifies. Do not edit `defense.tex` directly.
3. Build the deck again with `build_deck.py --force --compile`.
4. Run `check_deck.py` again.

Do a maximum of 3 rounds. If Critical or Major findings stay after round 3, list the remaining findings and let the user decide.

- For D-DENSITY, D-OVERFLOW-V, and D-OVERFLOW-H, use the overflow handling order in [Content Rules](content-rules.md): cut the text, split the page into two pages, use a different layout, and then make the figure narrower.
- For D-FIG-ALLOW, D-EQ-SRC, D-TAB-SRC, D-PAPER, and D-NUM-SRC, use only content from the inventory and from the thesis text. Do not rewrite numbers, equations, table bodies, or publication entries.

## NEEDS-LLM Review

D-NUM-SRC compares only the written form of numbers. It does not examine what a number means. For each finding, do these steps:

1. Find the sentence in the thesis that contains the number.
2. Make sure that the number, the unit, and the comparison baseline agree with that sentence.
3. If the number comes from a conversion, a rounding, or a new calculation, use the number in the thesis text.
4. If the thesis writes the same value in a different form (for example 12.30 and 12.3), use the form in the thesis text.
5. If you cannot decide, list the number and the thesis sentence, and let the user decide.

The script does not report a number that occurs in the thesis. When the same number means a different quantity in the thesis, the script cannot find the error. Before delivery, compare all numbers with the thesis sentences in page order.

## Preview and Visual Check

`render_preview.py` needs PyMuPDF. If PyMuPDF is not installed, the script prints “缺少 PyMuPDF：运行 `uv pip install pymupdf` 后重试” (PyMuPDF is missing; run the install command and try again) and exits with code 3.

- The page images start at `page-001.png`. `--dpi` sets the resolution; the default is 110. Before the script writes, it deletes the old `page-NNN.png` files in the output directory. It does not delete other files.
- The contact sheet is `contact-sheet.png`. Each page thumbnail is 480 pixels wide, there are `--cols` columns (default 4), the page number is below each thumbnail, and the background is white.

Examine these items on each page:

1. The positions of the frame title and the page number agree with the template.
2. The figures are clear, not blurred or stretched.
3. Each page has 3 or fewer emphasis marks (red bold text).
4. The footer does not cover body text or figures.
5. The chapter TOC highlights the current chapter.

## Known Limitations

- The script reads overflow line numbers as lines of `defense.tex`. An overflow in a package or in `thesis-macros.tex` can map to the wrong frame.
- D-FIG-ASPECT reads only PNG and JPEG bitmaps. It does not examine PDF figures, EPS figures, or image files that it cannot read.
- Image calls in `DefenseSource` are not part of D-FIG-ALLOW. D-EQ-SRC and D-TAB-SRC compare the equations and the table bodies word for word with the inventory.
- Frame splitting uses the lines that contain `\begin{frame}` and `\end{frame}`. When one line has more than one frame, the split is not correct.
- A frame without a frame marker gets its notes section by frame index.
- The visible character count does not expand macro definitions. It deletes the macro name and keeps the argument text.
