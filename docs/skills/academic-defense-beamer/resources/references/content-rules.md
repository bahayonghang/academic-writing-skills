# Content Rules

This file specifies how to write each text field of the defense deck, the sources of figures, tables, and numbers, and the order of steps for overflow. For the layouts and the fields, see [Layout Catalog](slide-layouts.md). For the page roles, see [Defense Deck Framework](defense-framework.md).

## Frame Titles and Subsection Bars

- Frame title (`section`): the thesis section number plus the section title, for example “3.2 方法设计” (3.2 method design). The section number comes from the thesis section tree. Do not number sections yourself.
- A page that maps to no section (for example, each page of the conclusion chapter) uses the chapter title as the frame title.
- Subsection bar (`subsection`): the subsection number plus the subsection title, for example “3.4.1 示例实验一” (3.4.1 example experiment 1). On the `intro` page of a research chapter, write “研究内容 i：章题” (research content i: chapter title).
- In the conclusion chapter, the subsection bars are “01　主要创新点” (01 main innovations) and “02　未来研究展望” (02 future research outlook).

## Takeaway Sentences

- Write one takeaway sentence (`takeaway`) on each content page, with 40 Chinese characters or fewer.
- The takeaway sentence states a verifiable mechanism or experimental judgment of the page, does not repeat the frame title, and avoids table-of-contents filler such as “本节介绍了……” or “本章分析了……”.
- When you read all takeaway sentences in page order, the sentences should retell the main line of the thesis. Before the build, output the takeaway sequence with the plan outline command, and ask the user to confirm the sequence.

## Bullets and Character Counts

- Each page has 5 bullets or fewer, and each bullet has 40 Chinese characters or fewer. Each layout has its own limits; see [Layout Catalog](slide-layouts.md).
- Prefer the two-part micro-typography `维度短签｜核心短句` (or `维度短签 :: 核心短句`): a 2–8 character prefix tag (2–4 characters recommended, such as “瓶颈问题” or “关键机制”) followed by a concise verb-object or noun phrase (12–28 characters recommended), which renders automatically as a tinted badge plus aligned body text; plain bullets without a separator remain backward-compatible.
- Avoid empty evaluative filler without comparison evidence (such as unsubstantiated “具有重要理论意义与实用价值”, “深入系统地研究了”, or “取得了显著效果”), and never leave untranslated foreign words (other than standard technical abbreviations) inside Chinese sentences. Keep concise accurate source phrasing as is rather than padding cards to hit a length target.
- Each content page has 180 visible body characters or fewer. This value is an initial threshold of the quality gate and is not calibrated.
- One page covers one idea. When the content is too much for one page, split the page.
- Text fields are plain text and are escaped verbatim at build time: characters such as `$`, `\`, and `%` appear as written. Do not write LaTeX commands or `$…$` inline math in text fields; when a symbol is needed, write its Chinese name (for example, 「观测集合」), or cite the thesis equation with the `equations-figure` layout.

## Font Sizes

- The default body size is `\small` (10 pt). A dense page can use `\footnotesize` (9 pt).
- No text is smaller than `\scriptsize` (8 pt, about 17 pt in pptx).
- For the font size levels, see [Visual Specification](visual-spec.md).

## Figures and Tables

- Use only figures and tables that are in the thesis. The figure files come from the extraction list. Do not generate new figures, and do not redraw data figures.
- Captions keep the thesis numbers, for example “图3-2” (Figure 3-2) and “表4-1” (Table 4-1). Subfigure captions keep the thesis letters (a), (b), and so on.
- When one figure appears on different pages, the figure number and the caption stay the same.

## Numbers

- Write only numbers that appear in the thesis.
- A performance number comes with its unit and its comparison baseline. For example, use “比基线方法降低 12.3%” (12.3% lower than the baseline method) only when the thesis gives both the unit and the baseline.
- Experiment, application, and chapter summary frames may highlight at most 3 key metric callouts in the optional `metrics` field (each with `label`, `value`, and `basis`); both the value and the comparison basis must come from the thesis text and are checked by `D-NUM-SRC`.
- Do not convert units, and do not recalculate percentages or means.

## Equations

- Copy the math source word for word by the thesis label, and keep the thesis numbers.
- Do not rewrite symbols, and do not merge or split equations.
- Put equations and table bodies in the `DefenseSource` environment.

## Emphasis

- Dual-layer restrained emphasis: in a text field, `**关键词**` renders as brick-red bold text (Beamer `\DefenseHighlight`, Touying `#key`) for core bottlenecks or breakthrough metrics, while `*结构术语*` renders as deep-navy bold text (Beamer `\DefenseTerm`, Touying `#hl`) for module names and structural concepts.
- Each page has at most 3 brick-red key emphasis spans (`**…**`); exceeding 3 is reported by the quality gate as `D-DENSITY` Minor.

## Terms and Abbreviations

- Terms are the same as in the thesis. One concept has only one name in the whole deck.
- At the first occurrence of an abbreviation, give the full name, in the same form as the thesis.

## Innovations and Outlook

- Innovation sentence pattern: “针对……问题，提出（或构建、设计）……，实现……” (for the … problem, propose (or construct, design) …, and achieve …).
- The innovation content comes from the matching contribution item in the conclusion chapter of the thesis, and gives the chapter number, for example “（第 3 章）” (chapter 3).
- The outlook comes from the outlook items in the conclusion chapter of the thesis. Do not add research directions that the thesis does not state.

## Overflow Handling Order

When the compile log reports an overflow or a page is too dense, apply these steps in this order:

1. Cut text.
2. Split the page into two pages.
3. Change to a different layout.
4. Reduce the figure width.

After these steps, no font size is smaller than `\scriptsize`.

## Academic Fact Protection

- Do not change `\cite`, `\ref`, `\label`, or math content.
- Do not invent references, authors, achievements, experiment results, or numbers.
- Do not generate new figures, and do not redraw data figures.
- The citation text in the “论文” (paper) box is a word-for-word copy from the thesis publication list.

## Sources and Attribution

This skill adopts mechanisms from two reference projects. This skill does not copy the source code or the original text of these projects:

| Project                   | License    | Adopted mechanisms                                                                                                                                                      |
| ------------------------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| claude-skill-academic-ppt | MIT        | Takeaway sequence reading, five-field speaker notes, question prediction, time budget, number check against the source text, one idea per page                          |
| thesis-defense-pptx-skill | Apache-2.0 | Allow list of thesis figures, template as the visual basis, text cuts before font reduction, page-by-page preview, placeholder scan, TOC consistent with the page order |
