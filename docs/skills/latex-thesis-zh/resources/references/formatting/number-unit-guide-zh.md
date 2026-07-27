# Numbers and Units (Chinese Degree Thesis)

Used by the `expression` module for its `E-NUMSPACE` / `E-NUMSTYLE` / `E-UNITFONT` checkers. Rule sources: `../writing/academic-style-zh.md` §6 plus the national standards below.

## Standard precedence

**University template rules > general national standards.** When the two conflict, the `templates/<template>.md` snapshot wins — template snapshots are the single authoritative source for template facts in this repository. Known references: `templates/yanshan.md` (GB 3100 / GB/T 3101 / GB/T 3102 / GB/T 15835 citations, the numeric-usage item, and YS-36).

The standards involved:

| Standard | Coverage |
| --- | --- |
| GB/T 15835 | Numeric usage in publications |
| GB/T 15834 | Punctuation usage |
| GB 3100 | The International System of Units and its application |
| GB/T 3101 | General principles for quantities, units and symbols |
| GB/T 3102 | Quantities and units by field |

## 1. Numeric usage (GB/T 15835)

| Situation | Form | Example |
| --- | --- | --- |
| Exact values, measurements, statistics | Arabic numerals | 3.2 kg, 12 samples, 92.1% |
| Approximations | Chinese numerals | 数十次, 几百个, 十余年 |
| Ordinals in narrative prose | Chinese | 第一, 第二 (not 1st, 2nd) |
| Fixed phrases, idioms, abbreviations | Chinese numerals | 三大类, 四化, 一系列 |
| Numbering (figure/table/equation/chapter/section/reference) | Arabic numerals | 图 3-1, 表 2, 式（4-5）, 第 3 章 |

**Do not report numbering as an approximation**: `图 3`, `第 1 章`, `式 (2)`, and `文献 [12]` are all numbering. `expression`’s `E-NUMSTYLE` excludes them by their leading character (图/表/式/章/节/条/页/卷/册/第).

**Division of labour with `spec-check`**: `expression` covers only generally decidable items; the complete template-specific numeric review belongs to YS-36 in `spec-check` (decided as `llm`). The two never report the same problem twice — item-by-item final checks before submission go to `spec-check`.

## 2. Space between value and unit (GB 3100 / GB/T 3101)

- Put **one space** between the value and the unit symbol: `3.2 kg`, `25 MPa`, `50 Hz`. In LaTeX the thin space `3.2\,kg` is more correct.
- **No space** for: percent `92.1%`, per-mille `‰`, degrees `30°`, arcminutes `′`, arcseconds `″`, and Celsius `25℃` (the `25 °C` spelling does take a space).

`E-NUMSPACE` is tier A: on a hit it proposes inserting `\,`, with `Risk-Flags: whitespace-normalized`.

## 3. Units are upright (GB/T 3101)

Quantity symbols are **italic** (`m`, `v`, `E`); unit symbols are **upright** (`kg`, `m/s`, `J`). In LaTeX, `$3.2 kg$` typesets `kg` in italics; the correct forms are:

```latex
$3.2\,\mathrm{kg}$
% 或使用 siunitx
\SI{3.2}{\kilogram}
```

**Red line**: the problem sits inside a math environment, and "never modify math environments" is red line one for this skill. So `E-UNITFONT` is **read-only, report-only, and never offers replacement text**; its output states explicitly that the author must adjust it inside the math environment by hand. It is the only one of the nine checkers where detection is reliable yet the tier still cannot be auto — **the tier follows the red line, not the decision capability**, so do not mistake it for something that can be promoted to A.

## 4. Common errors

| Wrong | Right | Basis |
| --- | --- | --- |
| `3.2kg` | `3.2\,kg` | GB 3100, one space between value and unit |
| `92.1 %` | `92.1%` | Percent takes no space |
| `实验重复了 10 几次` | `实验重复了十几次` | GB/T 15835, approximations use Chinese numerals |
| `参见第 1st 章` | `参见第一章` | GB/T 15835, ordinals use Chinese |
| `$3.2 kg$` | `$3.2\,\mathrm{kg}$` | GB/T 3101, units are upright |

## Related

- Chinese academic writing rules: [academic-style-zh.md](../writing/academic-style-zh.md)
- Module entry point and tier table: [expression.md](../modules/expression.md)
- Template-specific final review: [spec-check.md](../modules/spec-check.md)
