# Typst Touying Backend

This file explains the installation, layout mapping, speaker notes, fidelity limits, and exit codes of the Touying backend, and how to maintain the deck by hand after the final version. From the same thesis inventory and plan, the Touying backend makes the Typst defense deck `defense.typ`, using the Typst theme package simply-ysu-touying. For the plan fields, see [Inventory and Plan Fields](plan-schema.md); for the Beamer layouts, see [Layout Catalog](slide-layouts.md); for the checks, see [Quality Gate](quality-gate.md); for presenting, see [Presenting and Speaker Notes](presenting.md).

## Scope

- The input is still the LaTeX repository of a Chinese thesis; Typst is used only for the defense deck. A thesis written in Typst is out of scope for this skill; for paper formatting, use `typst-paper`.
- Only the `yanshan` theme is supported. The theme package brings its own colors, positions, and school logo; this skill does not define Touying colors and copies neither the theme source nor the logo bitmaps.
- The only source of the backend is `deck.backend` of the plan. `plan_deck.py --backend touying` writes it when the plan is made; `build_deck.py` has no backend option.

```bash
uv run python -B $SKILL_DIR/scripts/plan_deck.py --inventory inventory.json --out slide_plan.yaml --backend touying [--minutes 40] [--stage predefense|defense]
uv run python -B $SKILL_DIR/scripts/build_deck.py --plan slide_plan.yaml --inventory inventory.json --out DIR [--force] [--compile] [--no-notes-pdf] [--typst-package SPEC] [--typst-package-path DIR] [--font-path DIR]
uv run python -B $SKILL_DIR/scripts/check_deck.py --deck DIR/defense.typ --inventory inventory.json [--plan slide_plan.yaml] [--json]
```

## Installation

### Typst and Package Versions

| Dependency         | Version or spec                          | Notes                                                      |
| ------------------ | ---------------------------------------- | ---------------------------------------------------------- |
| Typst              | 0.15.1 or later                          | When `typst --version` is older than 0.15.1, `build_deck.py --compile` exits with 5 |
| Theme package      | `@preview/simply-ysu-touying:0.2.0`      | The default; `--typst-package` can change it to another spec, for example `@local/simply-ysu-touying:0.2.0` |
| Touying            | `@preview/touying:0.8.0`                 | A dependency of the theme package; the version is fixed    |
| mitex              | `@preview/mitex:0.2.6`                   | Renders the LaTeX equations of the thesis; the version is fixed |

`build_deck.py` does not download Typst packages. `--compile` first looks for the three packages above on this machine; when any is missing, it lists the missing packages and exits with 6 without calling `typst compile`.

### Default Method: Cache from Typst Universe

simply-ysu-touying 0.2.0 is published on Typst Universe. On a machine with network access, let typst download it once outside the pipeline. For example, create `probe.typ` in any empty directory:

```typst
#import "@preview/simply-ysu-touying:0.2.0": *
#import "@preview/mitex:0.2.6": mitex
```

Then run `typst compile probe.typ`. typst downloads the theme package, the `touying:0.8.0` it depends on, and `mitex` into the package cache directory. After that, `build_deck.py --compile` can run offline. Other ways, such as `typst init @preview/simply-ysu-touying:0.2.0`, also trigger the download, but `mitex` still has to be imported once on its own.

### Alternative Method: `@local` Installation

Offline, or with a modified theme, copy the theme package directory (with its `typst.toml`, version 0.2.0) into the Typst local package directory:

```text
<data>/typst/packages/local/simply-ysu-touying/0.2.0/typst.toml
```

Then name it at build time:

```bash
uv run python -B $SKILL_DIR/scripts/build_deck.py … --compile --typst-package @local/simply-ysu-touying:0.2.0
```

The theme package imports `@preview/touying:0.8.0` internally, so `touying` and `mitex` must still be on this machine: in the package cache directory, or under `preview/<name>/<version>/` of the local package directory.

### Package Lookup Order

The build script uses the same directories as typst and looks for `<namespace>/<name>/<version>/typst.toml`:

1. The local package directory: `--typst-package-path`; without it, the environment variable `TYPST_PACKAGE_PATH`; without both, `<data>/typst/packages`.
2. `@preview` packages only: the package cache directory, that is, the environment variable `TYPST_PACKAGE_CACHE_PATH`, or `<cache>/typst/packages` when it is not set.

| System  | `<data>`                             | `<cache>`                          |
| ------- | ------------------------------------ | ---------------------------------- |
| Windows | `%APPDATA%`                          | `%LOCALAPPDATA%`                   |
| Linux   | `$XDG_DATA_HOME` or `~/.local/share` | `$XDG_CACHE_HOME` or `~/.cache`    |
| macOS   | `~/Library/Application Support`      | `~/Library/Caches`                 |

`--typst-package-path` and `--font-path` pass unchanged to `typst compile --package-path` and `--font-path`.

### Fonts

The theme package has its own font fallback chain: Source Han Sans SC (思源黑体) and its fallbacks for Chinese, and Arial for Latin text. When this machine lacks these fonts, typst uses other fonts and prints a warning, and the layout can change. When the fonts are in a non-system directory, pass it with `--font-path DIR`. The deck passes no `icon:` parameter, so no icon font such as Font Awesome is needed.

## Outputs

| File                  | Description                                                                              |
| --------------------- | ---------------------------------------------------------------------------------------- |
| `defense.typ`         | The defense deck; a frame marker on the line before each frame, and one note per frame  |
| `notes.md`            | The speaker notes, in the same format as the Beamer backend; see [Speaker Notes Format](speaker-notes.md) |
| `build_manifest.json` | `backend: "touying"`, `notes_pdf`, `typst_package`, `typst_version`, `copied_images`, the file hashes, and the warnings |
| `img/`                | Copies of the thesis images that the plan uses, with the relative paths of the inventory, for example `img/fig/chapter3/network.png` |
| `defense.pdf`         | The slide build, one page per frame (after compilation)                                  |
| `defense-notes.pdf`   | The presenter build, a `notes:N` notes page after each frame (after compilation; not compiled with `--no-notes-pdf`) |
| `defense.log`         | The standard error of the two `typst compile` runs; cleared at the start of each `--compile` |

- `defense.typ`, `notes.md`, `build_manifest.json`, and `img/` are owned files. When any of them exists and `--force` is absent, the script exits with 4.
- Files and images with unchanged content are not rewritten and keep their modification times. `--force` deletes only images that the previous build wrote and this build no longer uses, according to the old `build_manifest.json` and its `copied_images`; other files in `img/` stay.
- The Typst `--root` is the output directory, and the deck cannot use files outside it, so the images are first copied into `img/`. Copying keeps the bytes: no format conversion and no redrawing.
- The school logo comes from the theme package. The Touying backend ignores `--logo` and prints a notice.

Compile commands:

```text
typst compile --root DIR [--package-path P] [--font-path F] DIR/defense.typ DIR/defense.pdf
typst compile --root DIR [--package-path P] [--font-path F] --input notes=on DIR/defense.typ DIR/defense-notes.pdf
```

## Layout Mapping

The line before each frame holds the frame marker `// defense-frame: id=<id> role=<role> chapter=<n|-> layout=<layout>`, with the same fields as the Beamer backend. The frame head of a content layout is, in order: `== #"帧标题"` (frame title), `#note[…]`, `#sub("小节")` (subsection; when `subsection` is not empty), and `#takeaway("结论句")` (takeaway; when `takeaway` is not empty).

| Layout             | Touying output                                                                                                                                       |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `cover`            | `#title-slide(note: […])`; the title, author, supervisor, subject, school, date, and stage go into `config-info` in the preamble                     |
| `toc` (overview)   | `#outline-slide(groups: ((from: 3, to: 5), ), note: […])`; each run of consecutive `research` chapters is one group, counted by chapter heading number; without research chapters, `groups` is not passed |
| `toc` (chapter contents) | `= #"章题"` (chapter title), `#note[…]`, `#chapter-opener(…)`; the frame's `takeaway` becomes `question:`, its first 3 `bullets` become `keywords:`, and without both no argument is passed |
| `bullets`          | The frame head plus `#points(…)`                                                                                                                     |
| `figure`           | The frame head plus `#figure-box(caption: […])[#image("img/…", height: 4.2cm)]`                                                                       |
| `figure-bullets`   | `position: left`: `#grid(columns: (1.25fr, 1fr))`, the left cell a `figure-box` (3.2 cm high) and the right cell `points`; `position: top`: the `figure-box` (2.3 cm high) above and `points` below |
| `figure-grid`      | The frame head plus `#grid(columns: n)` (n subfigures per row), one subfigure `figure-box` per cell (2.9 cm or 1.35 cm high), followed by `#fig-caption(…)` as the overall caption |
| `equations-figure` | One `#eq-block(number: "(3-1)")[#mitex(…)]` per equation, followed by `points`; with a figure, wrapped in `#grid(columns: (1.15fr, 1fr))` with the figure in the right cell (2.9 cm high) |
| `table`            | The frame head plus `#fig-caption(…)` (table caption above the table), then `#result-table(header: (…), rows: (…))`                                   |
| `cards`            | One `#side-card(label: "问题一")[…]` per bullet; on the `innovation` page the labels are “创新点 1” (innovation 1) and so on                          |
| `paper-summary`    | `points` plus `#paper-box[…]`                                                                                                                        |
| `outlook`          | One `#label-row(label: "其一")[…]` per item                                                                                                          |
| `thanks`           | `#ending-slide(recap: (…), note: […])`; when the `innovation` frame has 1–3 bullets, `recap` lists “创新点 k” (innovation k) with that bullet, otherwise it is not passed |

- When the plan gives `width`, the image is written with `width: N%` (N is `width` times 100), otherwise with the height in the table above.
- The frame title corresponds to the Touying page heading `== 页` (page), the subsection bar to `sub`, and the takeaway to `takeaway`. The Touying theme shows the takeaway at the main title position of the page header, while the Beamer theme shows it at the page bottom; the meaning is the same, and the length rules are in [Content Rules](content-rules.md).
- Each chapter has one level-1 heading `=`, so that the outline, the footer navigation, and the chapter opener numbers follow the thesis chapter numbers. From chapter 2 on, the chapter contents frame writes `= 章题`; chapter 1, chapters whose first frame is not a chapter contents frame, and chapters with no frame in the plan (added before the thanks frame) are written as `= #"章题" <touying:skip>`, which only registers the chapter and makes no chapter opener.
- Backup pages follow the thanks frame and also carry frame markers and notes.

### Footer Navigation `nav_label`

The footer navigation bar gets the short name of each chapter explicitly through `ysu-theme.with(nav-labels: (…))`; the source is `meta.chapters[].nav_label` of the plan.

- Default rule: `plan_deck.py --backend touying` writes `nav_label` for each chapter. When the chapter title has 6 characters or fewer, it is the title; otherwise it is “第k章” (Chapter k), and a hint in `hints` of the chapter's first frame asks for a short name of 6 characters or fewer.
- Reason: 6 full chapter titles (16–24 characters) make the footer overlap and wrap and push out the author and stage field; short names of 5 characters or fewer line up neatly.
- When the plan lacks `nav_label`, `build_deck.py` adds it by the same rule. The Beamer backend ignores the field.

## Speaker Notes

### Writing

- Each frame has exactly one note, with the same content as the Beamer backend: key point (bold), what to say, transition, and the seconds of the page at the end of the line. “可能提问” (possible questions) does not go into the PDF; it stays in `notes.md`. For the rules, see [Presenting and Speaker Notes](presenting.md).
- On a content page the note goes after the `== 标题` (title) line, as `#note[…]`. `#note[…]` can appear several times, and the parts on one page join as paragraphs; the build script writes one part per frame.
- Structure pages (cover, overview, thanks) use the `note:` parameter of their function, for example `#title-slide(note: […])`.
- The note of a chapter opener goes after `= 章名` (chapter name) and before `#chapter-opener`, and belongs to that chapter opener.
- The note text is also a string literal; `**关键词**` (keyword) is only bold in the note (`#strong`), with no color. The placeholder “〔待填写〕” (to be filled) appears on the notes page as is.

### Presenter Build

With `typst compile --input notes=on`, the theme inserts a notes page after each frame:

- The notes page has the width of the slide and a height of 13.5/16 of the width (slides 16 cm × 9 cm, notes pages 16 cm × 13.5 cm), on a dark background.
- Page labels: a content page is `N` and a notes page is `notes:N`, where `N` is exactly the label of the preceding content page. FerroStage and pympress pair pages by this convention, so no split layout needs to be chosen.
- The slide build `defense.pdf` writes no page labels.
- The sub-pages that `#pause` makes share one label `N`, and the notes page follows only the last sub-page. The build script writes no `#pause`.
- A frame without note content still has an empty notes page, so the pairing is not affected.
- When a frame overflows, the theme continues it on extra pages automatically: each continuation page takes its own numeric label, and the notes page follows only the last continuation page (for example `6, 7, 8, 9, notes:9`). The total page count of the presenter build is then not 2 × frames, and the quality gate reports D-OVERFLOW-V.

### Exporting Note Records

The theme writes the note of each frame as `<ysu-note>` metadata, with the fields `frame`, `page` (first page of the frame), `kind`, `title`, `sub`, `chapter-no`, `chapter`, and `text` (plain text). Typst 0.15.1 exports them with `typst eval`:

```bash
typst eval 'query(<ysu-note>).map(it => it.value)' --root DIR --in DIR/defense.typ
```

The older form `typst query --root DIR DIR/defense.typ "<ysu-note>" --field value` is deprecated in Typst 0.15 but still works. D-OVERFLOW-V of the quality gate tries the former first and the latter on failure.

## Text Safety

- All text fields of the plan are written as Typst string literals `"…"`; only `\` becomes `\\` and `"` becomes `\"`. Runs of whitespace merge into one space.
- The text never enters Typst markup mode, so `#`, `$`, `*`, `_`, `@`, `<`, `` ` ``, `//`, `=`, and `]` all show as written. `$…$` in a text field does not render as math.
- `**关键词**` (keyword) splits into `[#"前"#hl("关键词")#"后"]` (before, keyword, after); an unpaired `**` is output as ordinary characters.
- Captions and table cells come from the LaTeX source of the thesis and convert by these rules: `\ref` and `\eqref` output the thesis number (`??` for an unknown label); citation commands output nothing; `\textbf` and `\emph`, `\textit` keep their emphasis; `$…$` goes to mitex for inline rendering; `~` becomes a no-break space (U+00A0); `--` and `---` become an en dash and an em dash; commands that cannot be converted show as written, with a warning.

## Fidelity Limits

### Figures

- PDF, PNG, JPG (JPEG), and SVG are supported. PDF figures are embedded as vectors with their original fonts; Chinese text in SVG falls back along the `font-family` list.
- EPS is not supported: Typst cannot read it. `plan_deck.py` gives a hint in `hints`, and `build_deck.py` lists all EPS figures and exits with 2. Change the thesis figure to PDF, PNG, JPG, or SVG, or use the Beamer backend.
- When an image file that the plan uses does not exist, `build_deck.py` exits with 2 (in the Beamer backend only the quality gate reports D-FIG-MISSING in that case).

### Equations

- The equation source is the LaTeX text in the inventory. After `\label` is removed, it goes as a raw block into `#mitex(…)`, and all other characters stay unchanged; `eq-block(number:)` shows the number, which corresponds to `\tag*` in the Beamer backend.
- The macros of the thesis preamble are selected by the equations, captions, and table cells that use them (recursively), translated into the `\newcommand` form that mitex reads, and prepended as `thesis-macros`. The translation changes only the form of the definition, not the equation body:

| Thesis definition                                | Translation                                         |
| ------------------------------------------------ | --------------------------------------------------- |
| `\newcommand`, `\renewcommand`, `\providecommand` | Changed to `\newcommand`; the body stays unchanged |
| `\def\X{…}` (no parameters)                      | `\newcommand{\X}{…}`                                |
| `\DeclareMathOperator{\X}{t}`                    | `\newcommand{\X}{\operatorname{t}}`                 |
| `\DeclareMathOperator*{\X}{t}`                   | `\newcommand{\X}{\operatorname*{t}}`                |

- A `\def` with parameters or delimiters (for example `\def\X#1{…}`), an incomplete definition, and other definition commands are not translated: `plan_deck.py` gives a hint in `hints`, and `build_deck.py` exits with 2 and suggests the Beamer backend.
- Other commands that mitex cannot render fail at compile time, and D-COMPILE reports them.

### Tables

- Only simple tables are supported: one `tabular`, `tabular*`, or `tabularx` environment whose content is only `\hline`, `\toprule`, `\midrule`, `\bottomrule`, `\cline`, `\cmidrule`, `\addlinespace`, `&`, `\\`, and cell text; a cell can contain `$…$`, `\textbf`, `\emph`, `\ref`, and citation commands.
- A table with `\multirow`, `\multicolumn`, `\makecell`, a nested environment, or a command in a cell that cannot be converted is a complex table; `longtable` and `xltabular` are not supported either. `plan_deck.py` gives a hint, and `build_deck.py` exits with 2. For a complex table, use a thesis figure that shows the same result, or use the Beamer backend.
- The first row becomes the `result-table` field `header` and the other rows become `rows`; rows with fewer columns get empty cells at the end.

### Source Regions

Thesis source text (captions, equations, tables) sits between the two comment lines `// defense-source-begin` and `// defense-source-end`. The quality gate compares only the equations and tables inside source regions with the inventory; text inside source regions does not count as visible characters and does not take part in D-NUM-SRC.

## Exit Codes

| Script          | Exit codes                                                                                                                                                                                |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `plan_deck.py`  | 0: success; 2: an argument or input error, including `--backend touying` with a theme other than `yanshan`                                                                                |
| `build_deck.py` | 0: success; 2: plan validation fails, the theme is not `yanshan`, `--typst-package` is not `@namespace/name:x.y.z`, an EPS or unsupported image format, a missing image file, a complex table, or a macro that cannot be translated; 4: an owned file exists and `--force` is absent; 5: typst is not found, typst is older than 0.15.1, or either compilation fails or times out (the error message names which one); 6: the theme package, `touying`, or `mitex` is not installed on this machine |
| `check_deck.py` | 0: no Critical or Major; 1: one or more; 2: an input error, including a `--deck` suffix that is not `.tex` or `.typ`, or a suffix that does not match the `build_manifest.json` field `backend` |

After exit 6, install the missing packages as in the “Installation” section of this file and run `build_deck.py --compile` again; no change other than `--force` is needed.

## Advanced: Manual Maintenance After the Final Version

After the plan is final and the quality gate passes, you can leave the pipeline and edit `defense.typ` directly for fine layout work.

1. Copy the output directory as the working directory for manual maintenance, and do not run `build_deck.py --force` on it afterward: a rebuild overwrites `defense.typ`, `notes.md`, and the copies in `img/`.
2. Keep the `// defense-frame:` marker before each frame. Write markers for new frames too; the quality gate uses them to map frames, page roles, and page order.
3. Keep thesis source text between `// defense-source-begin` and `// defense-source-end`, and do not change the equations or tables.
4. Put custom layouts in a separate file, for example `lib/layouts.typ`, imported by `defense.typ`; these files use only the public components of the theme package.
5. After the thesis figures change, copy them into `img/` again (keeping the relative paths of the inventory); do not edit figures in the deck directory.
6. You can record common commands with a task runner such as `just`, for example compiling the two PDFs and exporting the note records.
7. The quality gate still runs: `check_deck.py --deck <工作目录>/defense.typ --inventory inventory.json`. When the notes in `defense.typ` become the source of the speech, `notes.md` is no longer synchronized automatically, and the notes findings of D-NOTES need manual judgment.
