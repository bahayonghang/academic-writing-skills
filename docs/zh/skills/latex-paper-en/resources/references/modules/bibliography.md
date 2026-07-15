# 模块：参考书目

**触发**：参考书目、参考书目、参考文献、引文、参考格式、引文风格

## 命令

```bash
uv run python -B scripts/verify_bib.py references.bib
uv run python -B scripts/verify_bib.py references.bib --tex main.tex
uv run python -B scripts/verify_bib.py references.bib --standard gb7714
uv run python -B scripts/verify_bib.py references.bib --tex main.tex --json
uv run python -B scripts/verify_bib.py references.bib --style apa
uv run python -B scripts/verify_bib.py references.bib --style vancouver --tex main.tex
uv run python -B scripts/verify_bib.py references.bib --style nature
```

## 细节
检查：必填字段、重复键、缺少引用、未使用的条目。
特定风格的检查（通过 `--style`）：作者计数 vs 等人。阈值、页面格式（破折号）、DOI 要求、特定于样式的必填字段。
关键输出字段：`missing_in_bib`, `unused_in_tex`.
技能层响应：将原始验证结果转换为 `% BIBLIOGRAPHY ...` 样式的结果呈现给用户。

另请参阅：[verification.md](../citations/verification.md) 基于 API 的验证。
另请参阅：[styles.md](../citations/styles.md) 了解 IEEE/APA/Vancouver/Nature 格式规则。
另请参阅：[journal-abbreviations.md](../citations/journal-abbreviations.md) 了解 ISO 4 期刊名称缩写。

