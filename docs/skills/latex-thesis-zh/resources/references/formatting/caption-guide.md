# Guide to Generating and Optimizing Figure/Table Captions

Follow these rules when the user asks for an English or bilingual Chinese-English caption. Whether
to use bilingual captions, their language order, capitalization, and list entries depends on the
university's latest rules and the actual template macro. Do not infer that every Chinese thesis must
switch to `\bicaption` from one university's example.

## 1. English Formatting Rules

- First follow the university rules and actual template consistently for **Title Case** or
  **Sentence case**. Only when neither specifies a style may the project optionally standardize noun
  phrases in Title Case and complete sentences in Sentence case.
- Final punctuation likewise follows the university rules, template, and the thesis's established
  convention. The examples below use Sentence case and do not establish a universal requirement.

## 2. Writing Style (Concise and Non-Generic)

- Describe the figure/table directly. Remove redundant openings such as “The figure shows” or “This diagram illustrates.” Start directly with `Architecture of...`, `Performance comparison of...`, or `Visualization of...`.
- For tables, prefer standard academic forms such as `Comparison with...`, `Ablation study on...`, and `Results on...`.
- Avoid unnecessarily ornate words such as showcase and depict; use show, compare, or present directly.

## 3. Bilingual Output (\bicaption)

Chinese degree theses commonly use the `bicaption` package or a similar mechanism for bilingual captions. Tell the user to place the result in this form only when the actual template supports it:

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth]{figures/example.pdf}
  \bicaption{中文标题}{English Title in Title Case or Sentence Case}
  \label{fig:example}
\end{figure}
```

Observe LaTeX escaping rules: special characters such as `%`, `_`, and `&` must be escaped. Keep mathematical expressions inside `$` delimiters.

## 4. Output Example

**User input:**
Generate a bilingual caption for this figure: it compares the accuracy of different models on three datasets.

**Agent response:**
```latex
% 图表标题 [Severity: Minor] [Priority: P2]: 建议使用双语 caption
% 中文标题：不同模型在三个数据集上的准确率对比
% English Title：Accuracy comparison of different models across three datasets
%
% 示例用法：
% \bicaption{不同模型在三个数据集上的准确率对比}{Accuracy comparison of different models across three datasets}
```

## 5. Caption Commands and Template Boundary

- The presence checks in `check_references.py` and `check_tables.py` recognize `\caption` and
  `\bicaption`, including valid optional short titles and whitespace or line breaks after the command.
- A presence check proves only that a real caption command occurs; it does not validate bilingual
  content, typeface, list entries, or rendered template layout. `\captionsetup`, captions in comments,
  and similarly named custom commands are not captions.
- When the university class provides a dedicated caption macro, first inspect its documentation and
  the thesis's existing usage. Do not replace every template with `\bicaption` for stylistic
  uniformity or add arbitrary macro-alias configuration.

## 6. Continued Figures and List of Figures

Use `\ContinuedFloat`, an empty-list caption, or a template-specific continuation macro only when
the actual template or a loaded package supports it. After a local change, check:

1. whether the continued page keeps the expected number and continuation marker;
2. whether `.aux` and the list of figures contain only the entries required by the template and use
   the intended short title;
3. whether captions, headers/footers, and prose are displaced on the previous, continued, or next page.

A successful build or an existing list-of-figures file does not replace viewing those pages. If the
template has no matching continuation semantics, preserve the current source and report the required
template evidence instead of applying another university's macro.

## 7. Avoiding Duplicate Subcaptions

First establish how `subcaption`, `subfig`, or the university macro creates the main caption,
subcaptions, and English list entries. Remove text locally only when the main and subcaption layers
really duplicate the same information. Avoid treating deduplication as a universal rule that makes
all subcaptions monolingual or deleting English captions without understanding template semantics.
Inspect the reading order of the main figure, every subfigure label, and both caption languages.

## 8. Effective Image Resolution and Editable Sources

Image metadata that says “300 DPI” does not establish sufficient effective resolution in the thesis.
Effective ppi depends on pixel dimensions and final layout width; for example, horizontal effective
ppi equals horizontal pixel count divided by final width in inches. Use the university or publisher's
target. Without the final layout size, do not declare that image clarity passes.

- Prefer editing an available vector or original source and export the PDF/PNG used by the thesis;
  avoid repeatedly scaling a low-resolution screenshot.
- Inspect the editable source, exported image, and compiled page together. A source file does not
  prove a correct export, and an existing PNG does not prove that the final page is clear, unclipped,
  or readable.
- On Windows, copy to a task-owned ASCII temporary name only when a tool actually fails on a
  non-ASCII path. This is a compatibility step, not the default, and does not change source ownership.

## 9. Visual Acceptance Boundary

Compile figure/table layout changes through the existing `compile.py` wrapper using the thesis's
actual entry and recipe, then view the affected page and adjacent pages. Check caption order,
continuation numbers and list entries, clipping, blank regions, and text readability.

Compilation success, an `.aux` entry, or an existing PNG/PDF is only intermediate evidence. If the
page was not actually viewed, report `missing evidence`; do not announce that layout passes. This
workflow does not authorize deleting or compressing the original PDF, installing system tools, or
controlling a desktop UI.
