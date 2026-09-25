# 版式目录

本文件列出答辩稿的十二个版式。每个版式给出适用页角色、规划字段、内容上限和调用的宏。宏在 `templates/beamer/defense-layouts.sty` 中定义，两个主题共用。页角色见 [答辩稿框架](defense-framework.md)，文字规则见 [内容规范](content-rules.md)。

## 版式总表

| 版式               | 适用页角色                                                            | 规划字段                                                                       | 内容上限                     | 调用的宏                                                   |
| ------------------ | --------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ---------------------------- | ---------------------------------------------------------- |
| `cover`            | `cover`                                                               | `meta`                                                                         | 题目不超过 3 行              | `\DefenseCoverFrame`                                       |
| `toc`              | `toc`                                                                 | `chapter`                                                                      | 无                           | `\DefenseTocFrame`                                         |
| `bullets`          | `background`、`status`、`achievements`、`problem`                     | `subsection`、`bullets`、`takeaway`                                            | 要点不超过 5 条              | `\DefenseSubsection`、`\DefenseTakeaway`                   |
| `figure`           | `status`、`organization`、`architecture`、`application`、`experiment` | `figures`（1 幅）、`takeaway`                                                  | 图高不超过 `0.62\textheight` | `\DefenseFigure`、`\DefenseTakeaway`                       |
| `figure-bullets`   | `intro`、`background`、`problem`、`method`、`foundation`              | `figures`（1 幅）、`bullets`、`position`（`left` 或 `top`）                    | 要点不超过 4 条              | `\DefenseSubsection`、`\DefenseFigure`、`\DefenseTakeaway` |
| `figure-grid`      | `experiment`                                                          | `figures`（1 幅，含 2–6 个子图）、`takeaway`                                   | 子图不超过 6 个              | `\DefenseFigure`、`\DefenseCaption`、`\DefenseTakeaway`    |
| `equations-figure` | `method`、`foundation`                                                | `equations`（不超过 4 个）、`figures`（不超过 1 幅）、`bullets`（不超过 3 条） | 公式不超过 4 个              | `DefenseSource`、`\DefenseFigure`、`\DefenseTakeaway`      |
| `table`            | `experiment`、`application`                                           | `table`、`takeaway`                                                            | 表体逐字复制                 | `\DefenseCaption`、`DefenseSource`、`\DefenseTakeaway`     |
| `cards`            | `challenges`、`innovation`                                            | `bullets`（每条一张卡片）                                                      | 卡片不超过 5 张              | `\DefenseSubsection`、`\DefenseCard`                       |
| `paper-summary`    | `summary`                                                             | `bullets`、`paper`                                                             | 要点不超过 4 条              | `\DefensePaperBox`、`\DefenseTakeaway`                     |
| `outlook`          | `outlook`                                                             | `bullets`                                                                      | 条目不超过 3 条              | `\DefenseSubsection`、`\DefenseBoxTitle`                   |
| `thanks`           | `thanks`                                                              | `meta`                                                                         | 无                           | `\DefenseThanksFrame`                                      |

除 `cover`、`toc`、`thanks` 外，每个版式的帧标题取 `section` 字段。`subsection` 字段为空时不输出小节条。`takeaway` 字段在各内容版式中都可用，渲染为页底的结论句框。

构建脚本在每个 `\begin{frame}` 前一行写帧标记。下文骨架中尖括号内的名称是规划字段的值。

## 导言区

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

- 主题取 `YanshanDefense` 或 `GenericDefense`。
- `\DefenseAddChapter` 每章一行，供目录页使用。
- `\DefenseDefineLabel` 每个论文标签一行，供 `DefenseSource` 环境输出论文编号。

## cover

```latex
% defense-frame: id=cover role=cover chapter=- layout=cover
\begin{frame}[plain]
\DefenseCoverFrame
\end{frame}
```

封面显示校徽、阶段字样、题目题带、汇报人、专业、导师、学院和日期。题目在 `\title` 中用 `\\` 分行。

## toc

```latex
% defense-frame: id=<id> role=toc chapter=<n> layout=toc
\begin{frame}[plain]
\DefenseTocFrame{<chapter>}
\end{frame}
```

总目录的 `chapter` 为 0。第 k 章的章前目录的 `chapter` 为 k。

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

`<caption>` 为论文编号加题注，例如「图3-2　示例对比结果」。`\DefenseFigure` 的默认尺寸为宽不超过行宽、高不超过 `0.62\textheight`，保持宽高比。

## figure-bullets

`position` 为 `left`（默认）时，图在左栏，要点在右栏：

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

`position` 为 `top` 时，图在上方，要点在下方：

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

| 子图数 | 每行子图数 | 小页宽度         | 小页间距         | 子图高度          |
| ------ | ---------- | ---------------- | ---------------- | ----------------- |
| 2      | 2          | `0.32\linewidth` | `0.08\linewidth` | `0.45\textheight` |
| 3      | 3          | `0.3\linewidth`  | `0.03\linewidth` | `0.45\textheight` |
| 4      | 2          | `0.32\linewidth` | `0.08\linewidth` | `0.21\textheight` |
| 5 或 6 | 3          | `0.3\linewidth`  | `0.03\linewidth` | `0.21\textheight` |

每行结束处写 `\par`，两行之间加 `\vspace{2pt}`。子图题的字母与论文一致。

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

- 公式环境取论文原环境名加星号。论文中每个 `\label{<label>}` 换为 `\tag*{(<number>)}`，其余字符不变。
- `eqnarray` 不支持 `\tag`：输出 `eqnarray*`，并在公式下方列出编号。
- 没有图时不用 `columns`，公式与要点占整行宽度。

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

- 表题在表上方，沿用论文编号，例如「表3-1　示例方法指标对比」。
- 表体从 `\begin{tabular}` 到 `\end{tabular}` 逐字复制。`\adjustbox` 只缩小，不放大。
- `\par` 放在 `DefenseSource` 环境内，使 `\centering` 生效。
- 表体缩小后文字小于 `\scriptsize` 时，换用论文中展示同一结果的图，或在讲稿中引用该表。

## cards

```latex
% defense-frame: id=<id> role=<role> chapter=<n> layout=cards
\begin{frame}{<section>}
\DefenseSubsection{<subsection>}
\DefenseCard{<label>}{<text>}
\DefenseCard{<label>}{<text>}
\end{frame}
```

- `challenges` 页：卡片标签依次为「问题一」「问题二」等，卡片数等于研究章数。
- `innovation` 页：小节条为「01　主要创新点」，卡片标签依次为「创新点 1」「创新点 2」等，卡片数等于研究章数。

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

`paper` 字段为空时不输出 `\DefensePaperBox`。

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

第三条的标签为「其三」。

## thanks

```latex
% defense-frame: id=thanks role=thanks chapter=- layout=thanks
\begin{frame}[plain]
\DefenseThanksFrame
\end{frame}
```

致谢页沿用封面版面，题带文字为「敬请各位老师批评和指正！」。

## 宏一览

| 宏或环境                                                           | 作用                                                                           |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| `\DefenseSetup{logo=…,stage=…,logo-text=…}`                        | 设置校徽路径、阶段（`predefense` 或 `defense`）和无校徽时的文字标识            |
| `\DefenseStage{…}`                                                 | 设置阶段，与 `stage` 键相同                                                    |
| `\DefenseSupervisor{…}`、`\DefenseSubject{…}`、`\DefenseSchool{…}` | 设置封面的导师、专业和学院                                                     |
| `\DefenseAddChapter{n}{章题}`                                      | 在目录中登记一章                                                               |
| `\DefenseDefineLabel{label}{编号}`                                 | 登记论文标签对应的论文编号                                                     |
| `\DefenseCoverFrame`、`\DefenseTocFrame{k}`、`\DefenseThanksFrame` | 输出封面、目录页和致谢页的帧内版面                                             |
| `\DefenseSubsection{…}`                                            | 小节条                                                                         |
| `\DefenseTakeaway{…}`                                              | 页底结论句框                                                                   |
| `\DefenseHighlight{…}`                                             | 红色粗体强调                                                                   |
| `\DefenseBoxTitle{…}`                                              | 填充底色的框标题                                                               |
| `\DefenseFigure[选项]{文件}{题注}`                                 | 论文图与题注；选项追加到 `\includegraphics` 的默认选项之后                     |
| `\DefenseCaption{…}`                                               | 题注行，用于子图组总题注与表题                                                 |
| `\DefensePaperBox{…}`                                              | 「论文」框                                                                     |
| `\DefenseCard{标签}{正文}`                                         | 带标签与箭头的卡片                                                             |
| `DefenseSource`                                                    | 包住逐字复制的公式与表体；环境内 `\ref`、`\eqref` 输出论文编号，引文命令不输出 |
