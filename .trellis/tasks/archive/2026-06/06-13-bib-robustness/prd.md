# bib-search-citation 解析器与检索正确性修复

> 父任务：`06-12-five-skills-optimization`（完整审计报告见其 `research/bib-search-citation-audit.md`，发现 B1-B26）
> 优先级：P0 · 依赖：无（本 skill 纯 stdlib、不依赖 parsers.py 拷贝，可独立先行）

## Goal

让"检索 → 引用"主链路在 fixture 之外的真实文献库（出版社导出、Zotero/JabRef 导出、
含 @string 的 IEEE/ACM 官方 .bib）上可信：消除三类静默丢数据、三类检索失真、
CLI 错误契约违约，并清理文档/测试卫生债。

## Requirements

### R1 解析器鲁棒性（B1/B2/B10 — P0）

- B1 引号状态机重写：brace 定界值内的 `"` 视为普通字符（只有 `field = "..."`
  形式才进入引号定界模式）。回归用例：`title = {Floppy disks of 3" form factor}`
  后跟 2 个合法条目须解析出 3 条。
- B2 resync 与告警：某条目花括号深度永不归零时，resync 到下一个行首 `@` 重扫；
  `meta` 增加 `parse_warnings`（含跳过的行号范围），使 SKILL.md:201"report that
  entries may have been skipped"的承诺有数据可依。
- B10 `@string/@comment/@preamble` 显式识别：不再产生幻影条目、不计入
  `total_entries`、不参与检索；@string 进宏表（供 R2 的 B7 使用）。
- 把审计取证的三个 fixture（quote_trap / broken / phantom）收编为回归测试。

### R2 检索正确性（B3/B6/B7/B8/B9 — P0/P1）

- B3 recency 泄漏：recency 加分仅对文本匹配得正分的条目生效（或挪到排序
  tie-break）。回归：对无关查询返回 0 条。
- B6 LaTeX 重音映射：`normalize_text` 增加常见重音转义表（`{\"u}`→ü 等），
  并同时产出 ASCII 折叠形式参与匹配。回归：`author:Müller` 与 `author:Muller`
  都命中 `G{\"u}nther M{\"u}ller`。
- B9 `derive_venue` 候选列表插入 `journaltitle`（biblatex/Better BibLaTeX 默认字段，
  一行修复收益最大）。
- B7 @string 宏展开 + `#` 串接拼接（依赖 R1 宏表）。
- B8 crossref 两遍解析：子条目继承父条目 year/booktitle 等缺失字段。

### R3 CLI 与错误契约（B4/B5/B11/B12/B17/B24 — P1）

- B4 文件读取纳入 main 的 JSON 错误契约（stderr JSON + exit 2）；utf-8 失败
  回退 latin-1 并在 meta 标注 `encoding_fallback`。
- B5 Windows 控制台：脚本开头 `sys.stdout.reconfigure(encoding="utf-8")`
  （两个脚本都加）。回归：结果含 `Łukasz` 在 cp936 环境不崩（CI 用
  monkeypatch 模拟低能力 stdout）。
- B11 CLI override（--claim/--include-raw-bib/--citation-mode/--sort/--limit/
  --recent-window/--return-fields）统一应用于 query/spec-json/spec-file 三种
  输入模式；做不到的组合显式报 SpecError，不许静默忽略。
- B12 未知 filter 键报错（SpecError 列出合法键）；generic field filter 对
  不存在的字段名在 meta 输出 warning。
- B17 `limit` 边界校验：0 与负数显式报错或文档化语义。
- B24 SKILL.md `argument-hint` 改为 `--bib library.bib --query QUERY`。

### R4 文档与测试卫生（B13/B14/B15/B16/B18/B19/B20/B21/B22/B23/B25/B26 — P2）

- B13 删除 SKILL.md 的 RTK 工作流段（维护者私有工具，分发后必失效），或把
  allowed-tools 与正文统一为通用工具措辞。
- B20 删除根 `tests/test_bib_search_citation.py`（skill 内 10 用例的过期子集，
  双重收集）。
- B21 在 `tests/test_skill_contracts.py` 为本 skill 启用 `router_help: True`。
- B22 同步 `docs/skills/bib-search-citation/resources/query-syntax.md`（EN+ZH）
  到 v5.2 内容（补 claim/recency）。
- B14 文档化作者匹配限制（姓-名顺序、无 von 处理），修正 query-syntax.md:273
  把 `author:chen` 匹配 Cheng 当优点的误导表述。
- B15/B16/B25/B26 在 SKILL.md / query-syntax.md 记录已知限制：matched 计数语义、
  CJK 多关键词需连续子串、多文件库需逐个调用、1800s 年份不识别（或顺手修
  `entry_year` 正则为 `\b1[5-9]\d{2}|20\d{2}\b` 级别的宽化）。
- B19 清死代码：`kind == "free"` 不可达分支、FIELD_ALIASES 恒等映射。
- B23 evals.json 断言加强：替换恒真断言（`not_contains: fabricated` 等）为
  锚定具体行为的断言。

## Constraints

- 保持零第三方依赖（纯 stdlib 是本 skill 的健康资产）。
- 保持既有 JSON 输出 schema 向后兼容（新增 meta 字段可以，改名/删除不行）。
- 安全边界文案（不可信数据、claim_support "NOT proof"）不得削弱。
- 不 bump version，只改 last_updated（[[skill-version-repo-synced]]）。

## Acceptance Criteria

- [ ] 三个审计 fixture（quote_trap/broken/phantom）全部正确解析并产出 parse_warnings。
- [ ] 无关查询（`quantum cryptography blockchain consensus` 对预测类文献库）返回 0 条。
- [ ] `author:Müller` / `author:Muller` / `venue:NeurIPS`（经 @string 展开）/
      biblatex `journaltitle` 库的 venue 过滤全部命中。
- [ ] `--spec-json '{"query":"mamba"}' --claim "..."` 输出含 claim_support
      （或显式 SpecError），不再静默忽略。
- [ ] `{"filters":{"venue_contains":[...]}}` 报 SpecError 而非返回全集。
- [ ] cp936 模拟环境输出含 `Ł` 的结果不崩溃。
- [ ] 根目录重复测试文件已删除，`just test` collect 数量无双重收集。
- [ ] docs 站 query-syntax 两语言版与 skill 内版本一致（claim/recency 在场）。
- [ ] `just ci` 全绿。
