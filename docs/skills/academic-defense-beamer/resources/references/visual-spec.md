# Visual Specification

This file gives the colors, positions, font size levels, font fallback, and logo rules of the two themes `yanshan` and `generic`. The `yanshan` theme uses a modern deep-navy, muted brick-red, and soft surface-tint palette aligned with the Touying backend (`simply-ysu-touying`); the `generic` theme uses the same positions with neutral academic colors and shows no logo. The theme files are `templates/beamer/beamerthemeYanshanDefense.sty` and `templates/beamer/beamerthemeGenericDefense.sty`, and the shared package is `templates/beamer/defense-layouts.sty`.

## Page

- Document class: `\documentclass[aspectratio=169,11pt]{ctexbeamer}`, with a 16 cm × 9 cm page.
- The left and right text margins are 1 cm each; the footer reserves 0.3 cm; frame content aligns to the top.
- No Beamer navigation symbols are shown; body text uses restrained dark ink (`black!88!defenseNavy`), and plain list items use small rounded-square bullets.

## Colors

| Color name       | `yanshan` | `generic` | Use                                                                                                 |
| ---------------- | --------- | --------- | --------------------------------------------------------------------------------------------------- |
| `defenseNavy`    | `#1F296A` | `#1F3A5F` | Cover plinth and title plaque top bar, frame titles, structural term bolding, KPI metric top bar    |
| `defenseBlue`    | `#2F5597` | `#2E5E8C` | End color of the page number parallelogram gradient                                                 |
| `defenseAccent`  | `#2F5597` | `#2E5E8C` | Subsection vertical bar, list bullets, single-column card left bar, cover plinth top trim           |
| `defenseBoxHead` | `#1F296A` | `#1F3A5F` | Box title background, header bar background of single-column and multi-column cards                 |
| `defensePaper`   | `#162052` | `#182D4A` | Left label background of the “论文” (paper) box, end color of the cover plinth gradient             |
| `defenseRed`     | `#B42318` | `#A93226` | Key conclusion emphasis (`**…**`), header anchor bar, left accent bar of the takeaway banner        |
| `defenseTint`    | `#F2F4F9` | `#F4F6F9` | Tinted surface of cards, takeaway banners, dimension lead tags, KPI blocks, and the “论文” box      |
| `defenseLine`    | `#D9DCE5` | `#D5DCE4` | Header divider hairline, figure mat frame, soft thin borders of cards and takeaway banners          |
| `defenseMuted`   | `#5A6072` | `#5D6773` | Figure and table captions, TOC index badges, KPI metric labels and comparison basis text            |

Current chapter on the TOC: both themes highlight the active chapter with a `defenseTint` bar, a left `defenseRed` bar, and bold `defenseNavy` text.

## Conversion and Minimum Font Size

The page is 16 cm wide (corresponding to a 16:9 widescreen pptx of 33.867 cm × 19.05 cm, scale factor 0.4724). Beamer body text at 11 pt corresponds to 23.3 pt in pptx. This skill sets the Beamer text minimum to 8 pt (`\scriptsize`) and recommends `\small` (10 pt) for body text.

## Positions

The coordinate origin is the top-left corner of the page, in cm. The content area aligns strictly to the 1.0 cm left and right grid (x = 1.0 cm to 15.0 cm).

| Element                         | Beamer implementation                                                                  | Font size                                    |
| ------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------- |
| Frame title                     | Left-aligned at (1.0, 0.42), height 0.80                                               | `\Large` bold `defenseNavy`                  |
| Header divider and red bar      | Hairline (1.0, 0.77)–(15.0, 0.77), left red bar 0.95 wide                              | None                                         |
| Content page logo               | Right-aligned at (14.12, 0.42), height 0.52                                            | None                                         |
| Page number parallelogram       | (14.30, 0.21)–(15.00, 0.63), deep-navy gradient                                        | Page number in `\scriptsize` bold white text |
| Subsection bar                  | At the left margin on the first body line, rounded vertical bar 0.12 × 0.36            | `\normalsize` bold                           |
| Cover stage capsule             | Right-aligned at (15.0, 0.92), `defenseTint` surface                                   | `\small` bold                                |
| Cover logo                      | (1.0, 0.48), height 0.92                                                               | None                                         |
| Cover floating title plaque     | (1.0, 1.70)–(15.0, 5.00), white framed card with subtle shadow and two-tone top bar    | `\huge` bold `defenseNavy`                   |
| Cover deep-navy plinth          | (0, 5.75)–(16.0, 9.00), straddled at the boundary by a white “汇报人” capsule          | Info table in `\small`                       |
| TOC page                        | Left 0.32 wide deep-navy strip, “目录 / CONTENTS” header, two-digit chapter badges     | `\normalsize`                                |

- The frame title area has a total height of 0.80 cm and a maximum title width of about 11.5 cm; when a section title is longer, prefer the short title from the thesis TOC.

## Font Size Levels

| Level                                                    | Beamer implementation    |
| -------------------------------------------------------- | ------------------------ |
| TOC main heading                                         | `\Huge` bold (24.88 pt)  |
| Cover title plaque, main sentence on the thanks page     | `\huge` bold (20.74 pt)  |
| Frame title                                              | `\Large` bold (14.4 pt)  |
| Subsection bar, TOC lines, straddling presenter capsule  | `\normalsize` (10.95 pt) |
| Body text, bullets, single-column cards, takeaway banner | `\small` (10 pt)         |
| Dimension lead tags, multi-column grid cards, captions   | `\footnotesize` (9 pt)   |
| KPI comparison basis, text minimum                       | `\scriptsize` (8 pt)     |

Dual-layer emphasis rules: `**关键结论词**` renders as bold `defenseRed` (`\DefenseHighlight`, at most 3 per page); `*结构术语*` renders as bold `defenseNavy` (`\DefenseTerm`).

## Font Fallback

| Category | Try in this order                                |
| -------- | ------------------------------------------------ |
| Chinese  | Microsoft YaHei → Source Han Sans SC → FandolHei |
| Latin    | Arial → TeX Gyre Heros                           |

The package uses `\IfFontExistsTF` to select the first available font in this order. TeX Live includes FandolHei and TeX Gyre Heros.

## Logo

- The logo file comes from the thesis repository. Write the logo path in `\DefenseSetup{logo=<path>}`. The skill package contains no logo file.
- The logo is 0.52 cm high on content pages and 0.92 cm high on the cover and the thanks page, preserving the source aspect ratio.
- `yanshan` theme: when the logo path is empty or the file does not exist, the deck shows a text mark. The default text mark is “燕山大学” (Yanshan University), in bold and in `defenseNavy`. `\DefenseSetup{logo-text=<文字>}` changes the text mark.
- `generic` theme: the deck shows no logo and no text mark.

## Touying Backend

- In the Touying backend, the colors, positions, font sizes, font fallback, and school logo all come from the installed theme package simply-ysu-touying. This skill does not define them and copies neither the theme source nor its logo bitmaps. The positions above apply only to the Beamer themes, while the color hierarchy and dual-layer emphasis semantics align with simply-ysu-touying.
- The page is 16:9 (16 cm × 9 cm); a notes page of the presenter build is 16 cm × 13.5 cm, see [Presenting and Speaker Notes](presenting.md).
- The build script sets only `aspect-ratio: "16-9"`, `nav-labels`, and `config-info`, and passes no color, font, or `icon:` parameter. For the default figure heights, see the layout mapping in [Typst Touying Backend](touying-backend.md).
- There is only one theme, `yanshan`; the `generic` theme is only for the Beamer backend.
