# Design: GB/T 7714 真实校验 + 2025 过渡

## verify_bib.py

1. `--standard` choices: `default | gb7714 | gb7714-2025`；`gb7714*` 共享国标增量检查。
2. 必填字段双层表：`REQUIRED_FIELDS`（default，原样不动）+ `GB_REQUIRED_FIELDS`
   （gb 模式生效）：phdthesis/mastersthesis(school,year)、techreport(institution,year)、
   patent(number,year)、standard(number)、online/electronic/webpage(url)。
3. `_verify_entry_gb(entry)`（仅 gb 模式追加）：
   - article 缺 volume/pages → warning（卷(期):页码）；
   - online/electronic/webpage 缺 urldate → warning；
   - 2015 专属：非 online 类型但带 url → info 建议补 urldate；2025 取消该提示（非网络文献不再要求访问日期）；
   - author 含字面 "et al."/"等"：语种不匹配 → warning；匹配 → info（建议 .bib 保留全部作者交给样式截断）；
   - 文件级 info（各最多 1 条）：≥4 作者未截断条目数提示；中文条目缺 langid 计数提示；
     2015 模式附 2026-07-01 实施过渡提示；2025 模式附差异要点 + arXiv 预印本条目识别提示。
4. severity 增加 `info`：status 仅由 error→FAIL / warning→WARNING 决定，info 不降级
   （default 模式不产生 info，回归不变）。
5. L265 `google_web_search` → `WebSearch 工具`。

## 文档

- `gb-standard.md`：删除第五（图表编号）、第六（章节标题）节 → 指针指向
  `templates/generic.md`（校级排版约定）；新增"五、GB/T 7714-2025 要点与过渡期建议"。
- `templates/generic.md`：接收迁移的图表编号/标题字体内容，标注"常见校级约定，非国标强制"。
- `modules/format.md`：指针改链 `../../templates/generic.md`。
- `modules/bibliography.md`：补 `--standard gb7714-2025` 一行 + 过渡提示。

## 测试

新建 `tests/test_latex_thesis_zh_gb7714.py`：fixture .bib（@phdthesis 缺 school、
@online 缺 urldate、@techreport 缺 institution、@article 正常/缺卷页、混用 等/et al.）。
断言 gb7714 全部报出、default 与现状一致、gb7714-2025 差异符合规则、输出无 google_web_search。
