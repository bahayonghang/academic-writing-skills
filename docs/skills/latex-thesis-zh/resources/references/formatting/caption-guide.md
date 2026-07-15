# Guide to Generating and Optimizing Figure/Table Captions

Follow these rules when the user asks for an English or bilingual Chinese-English caption.
Chinese degree-thesis templates based on national standards, including thuthesis and pkuthss,
usually require **bilingual Chinese-English** captions, so the English text must be precise and
follow the specified format.

## 1. English Formatting Rules

- If the translation is a noun phrase, use **Title Case**: capitalize all content words and omit the final period.
- If the translation is a complete sentence, use **Sentence case**: capitalize only the first word and proper nouns, and end with a period.

## 2. Writing Style (Concise and Non-Generic)

- Describe the figure/table directly. Remove redundant openings such as “The figure shows” or “This diagram illustrates.” Start directly with `Architecture of...`, `Performance comparison of...`, or `Visualization of...`.
- For tables, prefer standard academic forms such as `Comparison with...`, `Ablation study on...`, and `Results on...`.
- Avoid unnecessarily ornate words such as showcase and depict; use show, compare, or present directly.

## 3. Bilingual Output (\bicaption)

Chinese degree theses commonly use the `bicaption` package or a similar mechanism for bilingual captions. Tell the user to place the result in this form:

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
