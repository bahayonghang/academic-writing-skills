# Visual Specification

This file gives the colors, positions, font size levels, font fallback, and logo rules of the two themes `yanshan` and `generic`. The `yanshan` theme copies the measured values of the reference predefense pptx. The `generic` theme uses the same positions with neutral colors and shows no logo. The theme files are `templates/beamer/beamerthemeYanshanDefense.sty` and `templates/beamer/beamerthemeGenericDefense.sty`. The shared package is `templates/beamer/defense-layouts.sty`.

## Page

- Document class: `\documentclass[aspectratio=169,11pt]{ctexbeamer}`; the page is 16 cm × 9 cm.
- The left and right text margins are 1 cm each. The footer reserves 0.3 cm. Frame content aligns to the top.
- The deck shows no Beamer navigation symbols.

## Colors

| Color name       | `yanshan` | `generic` | Use                                                                                                           |
| ---------------- | --------- | --------- | ------------------------------------------------------------------------------------------------------------- |
| `defenseNavy`    | `#1F296A` | `#1F3A5F` | Title band of the cover and the thanks page, double lines of the frame title, text mark when there is no logo |
| `defenseBlue`    | `#2F5597` | `#2E5E8C` | TOC ellipse, end color of the page number gradient, current chapter on the `generic` TOC                      |
| `defenseAccent`  | `#4472C4` | `#2E5E8C` | Subsection bar text and dot, bullet symbols, card borders, start color of the page number gradient            |
| `defenseBoxHead` | `#376092` | `#4A6A8A` | Box title background, card label background                                                                   |
| `defensePaper`   | `#002060` | `#1F3A5F` | Border and label of the “论文” (paper) box                                                                    |
| `defenseRed`     | `#FF0000` | `#C0392B` | Emphasized words, border of the takeaway box                                                                  |

Current chapter on the TOC: `yanshan` uses black bold text; `generic` uses bold text in `defenseBlue`.

## Conversion

The reference pptx page is 33.867 cm × 19.05 cm. The Beamer page is 16 cm wide, so the scale factor is 16 / 33.867 = 0.4724. Multiply positions, sizes, and font sizes by this factor.

Beamer body text at 11 pt on a 16 cm wide page is equivalent to 23.3 pt in pptx. The pptx body text minimum of 16 pt corresponds to 7.6 pt in Beamer. This skill uses 8 pt (`\scriptsize`) as the Beamer text minimum and recommends `\small` (10 pt) for body text.

## Positions

The coordinate origin is the top-left corner of the page. The unit is cm. (x, y) is the top-left corner of the element.

| Element                             | pptx measurement                               | Beamer implementation                                                                                    | Font size                                    |
| ----------------------------------- | ---------------------------------------------- | -------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| Content page logo                   | (0.6, 0.1), 5.4 × 1.6                          | (0.28, 0.05), height 0.76                                                                                | None                                         |
| Frame title                         | Centered horizontally, y 1.0, height 1.4       | Center (8.0, 0.80)                                                                                       | 28 pt → 13.2 pt                              |
| Double lines beside the frame title | y 1.8 and 1.9                                  | y 0.85 and 0.90, line width 0.6 pt                                                                       | None                                         |
| Page number parallelogram           | (32.0, 0.5), 1.2 × 1.0                         | (15.12, 0.24), 0.57 × 0.47                                                                               | Page number in `\scriptsize` bold white text |
| Subsection bar                      | (2.1, 2.3), height 1.3, round icon on the left | At the left margin, on the first body line, dot diameter 0.42                                            | 24 pt → 11.3 pt                              |
| Cover title band                    | (0, 4.9), 33.9 × 6.8                           | (0, 2.31), 16 × 3.21                                                                                     | 48 pt → 22.7 pt                              |
| Cover stage text                    | (18.2, 1.1)                                    | (8.6, 0.52)                                                                                              | 32 pt → 15.1 pt                              |
| Cover logo                          | (0.5, 0.5), 8.9 × 2.6                          | (0.24, 0.24), height 1.23                                                                                | None                                         |
| Cover info table                    | (8.2, 12.9), 18.0 × 4.6                        | Top edge at y 6.09, centered horizontally                                                                | 24 pt → 11.3 pt                              |
| Cover date                          | Below the info table                           | Top edge at y 8.33, centered horizontally                                                                | 24 pt → 11.3 pt                              |
| TOC ellipse                         | (14.8, 0.3), 6.8 × 2.8                         | Center (8.0, 0.80), 3.21 × 1.32                                                                          | 54 pt → 25.5 pt                              |
| TOC lines                           | Centered horizontally, line spacing 2.1        | Left-aligned lines in a block that is centered horizontally, line spacing min(0.99, 6.9 / chapter count) | 24 pt → 11.3 pt                              |

- The frame title area is 0.8 cm high. The frame title is at most about 9.4 cm wide, which is about 18 Chinese characters in `\Large` bold. For a longer section title, use the short title from the thesis TOC.
- The converted position of the TOC ellipse is (6.99, 0.14). The TOC ellipse in the reference pptx looks centered, so the implementation centers the ellipse horizontally.
- The TOC lines are centered vertically in the range from y 1.9 to y 8.8.

## Font Size Levels

| Level                                              | pptx size | Converted value | Beamer implementation    |
| -------------------------------------------------- | --------- | --------------- | ------------------------ |
| TOC ellipse text                                   | 54 pt     | 25.5 pt         | `\Huge` bold (24.88 pt)  |
| Cover title band, main sentence on the thanks page | 48 pt     | 22.7 pt         | `\huge` bold (20.74 pt)  |
| Cover stage text                                   | 32 pt     | 15.1 pt         | `\Large` bold (14.4 pt)  |
| Frame title                                        | 28 pt     | 13.2 pt         | `\Large` bold (14.4 pt)  |
| Subsection bar, TOC lines, cover info table        | 24 pt     | 11.3 pt         | `\normalsize` (10.95 pt) |
| Body text, bullets, box titles, cards              | 16–18 pt  | 7.6–8.5 pt      | `\small` (10 pt)         |
| Captions, citation text in the “论文” (paper) box  | None      | None            | `\footnotesize` (9 pt)   |
| Text minimum                                       | 16.9 pt   | 8 pt            | `\scriptsize` (8 pt)     |

Subsection bars and emphasized words are bold. The color of emphasized words is `defenseRed`.

## Font Fallback

| Category | Try in this order                                |
| -------- | ------------------------------------------------ |
| Chinese  | Microsoft YaHei → Source Han Sans SC → FandolHei |
| Latin    | Arial → TeX Gyre Heros                           |

The package uses `\IfFontExistsTF` to select the first available font in this order. TeX Live includes FandolHei and TeX Gyre Heros.

## Logo

- The logo file comes from the thesis repository. Write the logo path in `\DefenseSetup{logo=<path>}`. The skill package contains no logo file.
- The logo is 0.76 cm high on content pages and 1.23 cm high on the cover and the thanks page. The width keeps the aspect ratio of the source image.
- `yanshan` theme: when the logo path is empty or the file does not exist, the deck shows a text mark. The default text mark is “燕山大学” (Yanshan University), in bold and in the color `defenseNavy`. `\DefenseSetup{logo-text=<文字>}` changes the text mark.
- `generic` theme: the deck shows no logo and no text mark.
