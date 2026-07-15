# 模块：参考书目

**触发**：参考书目、参考书目、参考文献、引文、参考格式、引文风格

## 命令

```bash
uv run python -B $SKILL_DIR/scripts/verify_bib.py references.bib
uv run python -B $SKILL_DIR/scripts/verify_bib.py references.yml          # Hayagriva
uv run python -B $SKILL_DIR/scripts/verify_bib.py references.bib --typ main.typ
uv run python -B $SKILL_DIR/scripts/verify_bib.py references.bib --style apa
uv run python -B $SKILL_DIR/scripts/verify_bib.py references.bib --style gb-7714-2015-numeric
uv run python -B $SKILL_DIR/scripts/verify_bib.py references.bib --online --email you@example.com
```

## 细节

检查：必填字段、重复键、缺少引用、未使用的条目
（什么时候`--typ`已给出）。接受`.bib`（BibTeX）和`.yml`/`.yaml`（马头明王）；
Hayagriva 参赛作品根据他们自己的现场合同进行验证（`title` /
`author`, `date`/`parent`语义），而不是 BibTeX 表。

特定于风格的检查（通过`--style`，其中之一`ieee`, `apa`, `mla`, `chicago`,
`gb-7714-2015-numeric`)：作者计数 vs 等人。阈值、页面格式（破折号、
仅 BibTeX）、DOI 要求。

在线验证（`--online`， 选修的`--email`对于 CrossRef 有礼貌
池，`--online-timeout`）根据 CrossRef / 语义交叉检查条目
学者。

该脚本打印一份人类可读的报告；技能层转换发现
呈现它们时进入 `// BIBLIOGRAPHY ...` 注释协议行。

另请参阅：[CITATION_VERIFICATION.md](../CITATION_VERIFICATION.md) 了解基于 API 的验证。
另请参阅：[CITATION_STYLES.md](../CITATION_STYLES.md) 了解 IEEE/APA/中文格式规则。
另请参阅：[JOURNAL_ABBREVIATIONS.md](../JOURNAL_ABBREVIATIONS.md) 了解 ISO 4 期刊名称缩写。
