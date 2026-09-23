# Bibliography Module Reference

Purpose: Validate references against GB/T 7714 and check BibTeX/BibLaTeX configuration.

> 版本提示：GB/T 7714-2025 已于 2025-12-02 发布、**2026-07-01 实施**（代替 2015 版）。
> `verify_bib.py --standard gb7714` 按 2015 版检查；`--standard gb7714-2025` 按新国标
> 差异点检查（预印本/数据集类型、非网络文献不再要求访问日期）。过渡期建议见
> [`../citations/gb-standard.md`](../citations/gb-standard.md) 第五节。

## Document Type Identifiers

| Type | Code | Example Format |
|------|------|---------------|
| Book | M | 作者. 书名[M]. 出版地: 出版社, 年份. |
| Journal | J | 作者. 题名[J]. 刊名, 年, 卷(期): 页码. |
| Thesis | D | 作者. 题名[D]. 城市: 学校, 年份. |
| Conference | C | 作者. 题名[C]//会议名. 城市, 年: 页码. |
| Patent | P | 发明人. 专利名[P]. 国别: 专利号, 日期. |
| Electronic | EB/OL | 作者. 题名[EB/OL]. (发布日期)[引用日期]. URL. |

## BibLaTeX Configuration (Recommended)

```latex
\usepackage[backend=biber,style=gb7714-2015]{biblatex}
\addbibresource{refs.bib}
\printbibliography[title=参考文献]
```

## BibTeX Alternative

```latex
\bibliographystyle{gbt7714-numerical}  % or gbt7714-author-year
\bibliography{refs}
```

## Common Issues

- **Author names**: Chinese surname first; English: Surname, Initials.
- **Multiple authors**: 3 or fewer: list all; 4+: first 3 + "等"/"et al."
- **DOI**: Must include when available (`doi = {10.xxxx/xxxxx}`)
- **Page numbers**: Use double dash `1--15` (not single dash or tilde)

> Full details: see [`../citations/gb-standard.md`](../citations/gb-standard.md) (sections 一–四)

## 可选学院著录提示（`--college-details`）

只与 `--standard gb7714` 或 `--standard gb7714-2025` 同时使用。其它组合，包括 `--standard default` 和省略 `--standard`，都是参数错误，非零退出，不表示通过，也不猜测学校。

该开关不改变既有 standard 问题的顺序，只在末尾追加 Info 候选。`book`、`phdthesis` 和 `mastersthesis` 需要 `address` 或 `location` 至少其一。这些类型缺少 `pages` 时列为来源核验。`inproceedings` 缺少 `pages` 时还要人工核实学院第101项。`article` 沿用原有缺字段结果，不重复报告。

正常完整个人姓名不是大小写违规。助词、连字符、重音和机构作者保持原样。不生成缩写姓名，也不把 `LI G Z` 当作正确的源 BibTeX。有作者数据时至多一条文件级说明：核最终 `BBL/PDF` 是否姓在前、姓大写、名用首字母。缺少传统页码或只有文章号时只列待核，不根据 PDF 总页数填写页码。

候选为 `[Script]`、Info/P3、`Meaning-Check: NEEDS-LLM`。
