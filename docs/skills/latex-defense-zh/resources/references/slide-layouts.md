# Layout Catalog

This file lists the twelve layouts of the defense deck. For each layout, this file gives the page roles, the plan fields, the content limit, and the macros that the layout calls. The file `templates/beamer/defense-layouts.sty` defines the macros, and both themes use these macros. For the page roles, see [Defense Deck Framework](defense-framework.md). For the text rules, see [Content Rules](content-rules.md).

## Layout Table

| Layout             | Page roles                                                            | Plan fields                                                              | Content limit                              | Macros called                                              |
| ------------------ | --------------------------------------------------------------------- | ------------------------------------------------------------------------ | ------------------------------------------ | ---------------------------------------------------------- |
| `cover`            | `cover`                                                               | `meta`                                                                   | Title of 3 lines or fewer                  | `\DefenseCoverFrame`                                       |
| `toc`              | `toc`                                                                 | `chapter`                                                                | None                                       | `\DefenseTocFrame`                                         |
| `bullets`          | `background`, `status`, `achievements`, `problem`                     | `subsection`, `bullets`, `takeaway`                                      | 5 bullets or fewer                         | `\DefenseSubsection`, `\DefenseTakeaway`                   |
| `figure`           | `status`, `organization`, `architecture`, `application`, `experiment` | `figures` (1 figure), `takeaway`                                         | Figure height of `0.62\textheight` or less | `\DefenseFigure`, `\DefenseTakeaway`                       |
| `figure-bullets`   | `intro`, `background`, `problem`, `method`, `foundation`              | `figures` (1 figure), `bullets`, `position` (`left` or `top`)            | 4 bullets or fewer                         | `\DefenseSubsection`, `\DefenseFigure`, `\DefenseTakeaway` |
| `figure-grid`      | `experiment`                                                          | `figures` (1 figure with 2–6 subfigures), `takeaway`                     | 6 subfigures or fewer                      | `\DefenseFigure`, `\DefenseCaption`, `\DefenseTakeaway`    |
| `equations-figure` | `method`, `foundation`                                                | `equations` (4 or fewer), `figures` (1 or fewer), `bullets` (3 or fewer) | 4 equations or fewer                       | `DefenseSource`, `\DefenseFigure`, `\DefenseTakeaway`      |
| `table`            | `experiment`, `application`                                           | `table`, `takeaway`                                                      | Word-for-word copy of the table body       | `\DefenseCaption`, `DefenseSource`, `\DefenseTakeaway`     |
| `cards`            | `challenges`, `innovation`                                            | `bullets` (one card for each bullet)                                     | 5 cards or fewer                           | `\DefenseSubsection`, `\DefenseCard`                       |
| `paper-summary`    | `summary`                                                             | `bullets`, `paper`                                                       | 4 bullets or fewer                         | `\DefensePaperBox`, `\DefenseTakeaway`                     |
| `outlook`          | `outlook`                                                             | `bullets`                                                                | 3 items or fewer                           | `\DefenseSubsection`, `\DefenseBoxTitle`                   |
| `thanks`           | `thanks`                                                              | `meta`                                                                   | None                                       | `\DefenseThanksFrame`                                      |

Except for `cover`, `toc`, and `thanks`, the frame title of each layout comes from the `section` field. When the `subsection` field is empty, the frame has no subsection bar. All content layouts accept the `takeaway` field. The deck shows the field as the takeaway box at the page bottom.

The build script writes a frame marker on the line before each `\begin{frame}`. In the skeletons below, the names in angle brackets are the values of plan fields.

## Preamble

```latex
\documentclass[aspectratio=169,11pt]{ctexbeamer}
\usetheme{YanshanDefense}
\DefenseSetup{logo=<logo>,stage=<stage>}
\title{<title line 1>\\<title line 2>}
\author{<author>}
\DefenseSupervisor{<supervisor>}
\DefenseSubject{<subject>}
\DefenseSchool{<school>}
\date{<date>}
\DefenseAddChapter{<n>}{<chapter title>}
\DefenseDefineLabel{<label>}{<thesis number>}
```

- The theme is `YanshanDefense` or `GenericDefense`.
- Write one `\DefenseAddChapter` line for each chapter. The TOC pages use these lines.
- Write one `\DefenseDefineLabel` line for each thesis label. The `DefenseSource` environment uses these lines to print the thesis numbers.

## cover

```latex
% defense-frame: id=cover role=cover chapter=- layout=cover
\begin{frame}[plain]
\DefenseCoverFrame
\end{frame}
```

The cover shows the school logo, the stage text, the title band, the presenter, the major, the supervisor, the school, and the date. In `\title`, use `\\` to break the title into lines.

## toc

```latex
% defense-frame: id=<id> role=toc chapter=<n> layout=toc
\begin{frame}[plain]
\DefenseTocFrame{<chapter>}
\end{frame}
```

On the overall TOC, `chapter` is 0. On the chapter TOC of chapter k, `chapter` is k.

## bullets

```latex
% defense-frame: id=<id> role=<role> chapter=<n> layout=bullets
\begin{frame}{<section>}
\DefenseSubsection{<subsection>}
\begin{itemize}
  \item <bullet>
\end{itemize}
\DefenseTakeaway{<takeaway>}
\end{frame}
```

## figure

```latex
% defense-frame: id=<id> role=<role> chapter=<n> layout=figure
\begin{frame}{<section>}
\DefenseSubsection{<subsection>}
\DefenseFigure{<file>}{<caption>}
\DefenseTakeaway{<takeaway>}
\end{frame}
```

`<caption>` is the thesis number plus the caption text, for example “图3-2　示例对比结果”. By default, `\DefenseFigure` limits the width to the line width and the height to `0.62\textheight`, and keeps the aspect ratio.

## figure-bullets

When `position` is `left` (the default), the figure is in the left column and the bullets are in the right column:

```latex
% defense-frame: id=<id> role=<role> chapter=<n> layout=figure-bullets
\begin{frame}{<section>}
\DefenseSubsection{<subsection>}
\begin{columns}[T,onlytextwidth]
  \column{0.54\textwidth}
  \DefenseFigure[height=0.5\textheight]{<file>}{<caption>}
  \column{0.42\textwidth}
  \begin{itemize}
    \item <bullet>
  \end{itemize}
\end{columns}
\DefenseTakeaway{<takeaway>}
\end{frame}
```

When `position` is `top`, the figure is at the top and the bullets are below the figure:

```latex
% defense-frame: id=<id> role=<role> chapter=<n> layout=figure-bullets
\begin{frame}{<section>}
\DefenseSubsection{<subsection>}
\DefenseFigure[height=0.36\textheight]{<file>}{<caption>}
\begin{itemize}
  \item <bullet>
\end{itemize}
\DefenseTakeaway{<takeaway>}
\end{frame}
```

## figure-grid

```latex
% defense-frame: id=<id> role=experiment chapter=<n> layout=figure-grid
\begin{frame}{<section>}
\DefenseSubsection{<subsection>}
{\centering
\begin{minipage}[t]{0.32\linewidth}
  \DefenseFigure[height=0.21\textheight]{<file a>}{(a) <subcaption a>}
\end{minipage}\hspace{0.08\linewidth}%
\begin{minipage}[t]{0.32\linewidth}
  \DefenseFigure[height=0.21\textheight]{<file b>}{(b) <subcaption b>}
\end{minipage}\par}
\DefenseCaption{<caption>}
\DefenseTakeaway{<takeaway>}
\end{frame}
```

| Subfigure count | Subfigures per row | Minipage width   | Minipage spacing | Subfigure height  |
| --------------- | ------------------ | ---------------- | ---------------- | ----------------- |
| 2               | 2                  | `0.32\linewidth` | `0.08\linewidth` | `0.45\textheight` |
| 3               | 3                  | `0.3\linewidth`  | `0.03\linewidth` | `0.45\textheight` |
| 4               | 2                  | `0.32\linewidth` | `0.08\linewidth` | `0.21\textheight` |
| 5 or 6          | 3                  | `0.3\linewidth`  | `0.03\linewidth` | `0.21\textheight` |

Write `\par` at the end of each row, and add `\vspace{2pt}` between two rows. The subfigure letters are the same as in the thesis.

## equations-figure

```latex
% defense-frame: id=<id> role=<role> chapter=<n> layout=equations-figure
\begin{frame}{<section>}
\DefenseSubsection{<subsection>}
\begin{columns}[T,onlytextwidth]
  \column{0.52\textwidth}
  \begin{DefenseSource}
  \begin{align*}
    <thesis line 1> \tag*{(<number 1>)}\\
    <thesis line 2> \tag*{(<number 2>)}
  \end{align*}
  \end{DefenseSource}
  \begin{itemize}
    \item <bullet>
  \end{itemize}
  \column{0.44\textwidth}
  \DefenseFigure[height=0.45\textheight]{<file>}{<caption>}
\end{columns}
\DefenseTakeaway{<takeaway>}
\end{frame}
```

- The equation environment is the environment name from the thesis plus an asterisk. Replace each `\label{<label>}` from the thesis with `\tag*{(<number>)}`, and keep all other characters.
- `eqnarray` does not support `\tag`: output `eqnarray*`, and list the numbers below the equations.
- When there is no figure, do not use `columns`. The equations and the bullets use the full line width.

## table

```latex
% defense-frame: id=<id> role=<role> chapter=<n> layout=table
\begin{frame}{<section>}
\DefenseSubsection{<subsection>}
\DefenseCaption{<caption>}
\begin{DefenseSource}
\centering
\adjustbox{max width=\textwidth,max totalheight=0.62\textheight}{%
<thesis tabular>}\par
\end{DefenseSource}
\DefenseTakeaway{<takeaway>}
\end{frame}
```

- The table caption is above the table and keeps the thesis number, for example “表3-1　示例方法指标对比”.
- Copy the table body word for word, from `\begin{tabular}` to `\end{tabular}`. `\adjustbox` only shrinks the table and never enlarges the table.
- Put `\par` inside the `DefenseSource` environment, so that `\centering` takes effect.
- When the shrunk table body has text smaller than `\scriptsize`, use a thesis figure that shows the same result, or cite the table in the speaker notes.

## cards

```latex
% defense-frame: id=<id> role=<role> chapter=<n> layout=cards
\begin{frame}{<section>}
\DefenseSubsection{<subsection>}
\DefenseCard{<label>}{<text>}
\DefenseCard{<label>}{<text>}
\end{frame}
```

- `challenges` page: the card labels are “问题一” (problem 1), “问题二” (problem 2), and so on. The card count equals the research chapter count.
- `innovation` page: the subsection bar is “01　主要创新点” (01 main innovations), and the card labels are “创新点 1” (innovation 1), “创新点 2” (innovation 2), and so on. The card count equals the research chapter count.

## paper-summary

```latex
% defense-frame: id=<id> role=summary chapter=<n> layout=paper-summary
\begin{frame}{<section>}
\begin{itemize}
  \item <bullet>
\end{itemize}
\DefensePaperBox{<publication text>}
\DefenseTakeaway{<takeaway>}
\end{frame}
```

When the `paper` field is empty, the frame has no `\DefensePaperBox`.

## outlook

```latex
% defense-frame: id=<id> role=outlook chapter=<n> layout=outlook
\begin{frame}{<section>}
\DefenseSubsection{02\quad 未来研究展望}
\DefenseBoxTitle{其一}\quad <outlook 1>

\vspace{0.3cm}
\DefenseBoxTitle{其二}\quad <outlook 2>
\end{frame}
```

The label of the third item is “其三” (third).

## thanks

```latex
% defense-frame: id=thanks role=thanks chapter=- layout=thanks
\begin{frame}[plain]
\DefenseThanksFrame
\end{frame}
```

The thanks page uses the cover layout. The band text is “敬请各位老师批评和指正！” (please give your comments and corrections).

## Macro Reference

| Macro or environment                                               | Purpose                                                                                                                                                                   |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `\DefenseSetup{logo=…,stage=…,logo-text=…}`                        | Sets the logo path, the stage (`predefense` or `defense`), and the text mark for a deck without a logo                                                                    |
| `\DefenseStage{…}`                                                 | Sets the stage; same as the `stage` key                                                                                                                                   |
| `\DefenseSupervisor{…}`, `\DefenseSubject{…}`, `\DefenseSchool{…}` | Set the supervisor, the major, and the school on the cover                                                                                                                |
| `\DefenseAddChapter{n}{章题}`                                      | Registers one chapter in the TOC (章题: chapter title)                                                                                                                    |
| `\DefenseDefineLabel{label}{编号}`                                 | Registers the thesis number of a thesis label (编号: number)                                                                                                              |
| `\DefenseCoverFrame`, `\DefenseTocFrame{k}`, `\DefenseThanksFrame` | Output the in-frame layout of the cover, the TOC pages, and the thanks page                                                                                               |
| `\DefenseSubsection{…}`                                            | Subsection bar                                                                                                                                                            |
| `\DefenseTakeaway{…}`                                              | Takeaway box at the page bottom                                                                                                                                           |
| `\DefenseHighlight{…}`                                             | Red bold emphasis                                                                                                                                                         |
| `\DefenseBoxTitle{…}`                                              | Box title with a filled background                                                                                                                                        |
| `\DefenseFigure[选项]{文件}{题注}`                                 | Thesis figure and caption (选项: options; 文件: file; 题注: caption); the options come after the default options of `\includegraphics`                                    |
| `\DefenseCaption{…}`                                               | Caption line for the overall caption of a subfigure group and for a table caption                                                                                         |
| `\DefensePaperBox{…}`                                              | “论文” (paper) box                                                                                                                                                        |
| `\DefenseCard{标签}{正文}`                                         | Card with a label and an arrow (标签: label; 正文: body text)                                                                                                             |
| `DefenseSource`                                                    | Wraps the equations and table bodies that are word-for-word copies; in the environment, `\ref` and `\eqref` print the thesis numbers, and citation commands print nothing |
