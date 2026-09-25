# 中文学位论文引文位置、重复页码、著录提示与综述递进契约

## 1. Scope / Trigger

维护 `latex-thesis-zh` 的 `--author-cite`、`--repeat-cite`、`--college-details`、
`--progression-density`，或对应公开指南时适用。面向作者的规则由技能内
`references/modules/references.md`、`bibliography.md`、`literature.md`、
`references/citations/gb-standard.md` 与 `references/writing/literature-progression-zh.md` 拥有。
复制安装后的技能不得依赖本 spec 或私有论文语料。

## 2. Signatures

```text
uv run python scripts/check_references.py INPUT
    [--school yanshan-ee-2025|generic] [--author-cite] [--repeat-cite]
uv run python scripts/verify_bib.py FILE.bib
    [--standard default|gb7714|gb7714-2025] [--college-details]
uv run python scripts/analyze_literature.py INPUT
    [--section NAME] [--progression-density]
    [--intro-citations] [--current-year YEAR]
```

`--author-cite` 与 `--repeat-cite` 相互独立，也可与 `--school` 组合。
`--college-details` 只在 `--standard gb7714` 或 `gb7714-2025` 时合法。
`--progression-density` 可与 `--section` 组合，且与 `--intro-citations` 互斥。
省略新开关时不建立新扫描，旧 stdout、stderr 和退出码保持不变。`--help` 不属于旧输出基线。

## 3. Contracts

- 新候选为 `[Script]`、Info/P3、`Meaning-Check: NEEDS-LLM`。只报告文件、行、短片段、引用键或字段，不输出替换句，不改写引用键，不移动 cite。
- `--author-cite` 使用 assemble 顺序和源位置。支持 `\cite`、`\citep`、`\citet`、`\parencite`、`\textcite`、`\autocite`、`\footcite` 及其星号；命令与参数之间允许空白、注释和 0 到 2 个平衡可选参数。
- 明确的拉丁字母作者名（可含助词、连字符、重音）加报告谓词，且同句 cite 不紧跟作者短语时，给出 `RC-AUTHOR`。`\textcite` 与 `\citet` 不另报作者位置。
- 中文 1–4 字不是已确认姓氏。带「等/等人」或紧邻报告谓词时只给 `RC-AUTHOR-UNCERTAIN`，文案写明作者主语不确定。文献、已有研究和停用词不报。
- 不把 ASCII 点号缩写当成句号。不完整句和段落边界之外不猜测绑定。
- `--repeat-cite` 对每个受支持命令中的每个键计一次。单可选参数是 postnote；双可选参数中第二个才是 postnote；空白 postnote 为空。
- 同一键至少两次且至少一次缺少 postnote 时给出 `RC-REPEATPAGE`。两次都有逐键字面页码，或只有一次，不报。字面页码只包括整数、罗马数字和明确页段。
- 多键共享 postnote 即使非空也给一条 `RC-SHARED`。自然语言 postnote 给 `RC-POSTNOTE`，不能据此通过学院规则，也不发明页码。
- 题注中的可见引用计入。参考文献数据、注释、宏定义、verbatim 和 `\nocite` 不计。`\cites`、自定义宏传键和未展开参数未覆盖，模式会说明覆盖不足。
- `--school` 仍只负责非表浮动体中文题注。与本契约同时使用时，`CAP-PUNCT` 与本契约候选都保留，同一题注的 `CAP-PUNCT` 不重复。
- `--college-details` 不改变既有 standard 问题序列，只追加 info。`book`、`phdthesis`、`mastersthesis` 需要 `address` 或 `location`。这些类型缺少 `pages` 时作来源核验。`inproceedings` 缺少 `pages` 时指向学院第101项。`article` 不重复原有缺字段结果。
- 完整个人姓名、助词、连字符、重音和机构作者不作大小写违规，不生成缩写，不把 `LI G Z` 当作正确源 BibTeX。有作者数据时至多一条文件级 `BBL/PDF` 核读说明。缺传统页码或只有文章号时只列待核，不根据 PDF 总页数填写页码。
- `--progression-density` 复用既有 section 解析。可见正文排除题注、引用键、数学和代码。按出现次数计数：「进一步」严格多于 5，「针对」严格多于 7。未传 `--section` 时只用 `related`；找不到则保留原错误，不扫全文，不报告通过。阈值标 `UNVERIFIED`。脚本不轮换同义词。

## 4. Validation & Error Matrix

| 条件 | 必须行为 |
| --- | --- |
| 未传本契约的新开关 | 旧输出不变，且不调用新扫描 |
| `--college-details` 配合 `default`、省略 standard 或其它值 | 参数错误，非零退出，不打印通过，不猜测学校 |
| `--progression-density` 与 `--intro-citations` 同用 | 参数错误，非零退出，不打印文献综述通过 |
| 明确作者短语后 cite 紧跟该短语 | 不报 `RC-AUTHOR` |
| 同一键两次且都有逐键字面页码 | 不报 `RC-REPEATPAGE` |
| 章节缺失 | 保留原“未找到章节”错误，不改扫全文 |

## 5. Good / Base / Bad Cases

- Good：`Example 等人\cite{key}提出了路径。`；`\cite[12]{key}` 与 `\cite[iv--vi]{key}`；`location` 已填写的图书；指定章节内 5 次「进一步」。
- Base：不传新开关时，引用完整性、GB 校验和文献综述旧输出保持不变。
- Bad：把每个 2–4 字中文词当成姓名；因 postnote 非空就通过学院页码规则；把 `LI G Z` 写成正确源数据；用 PDF 总页数补 `pages`；缺失章节时扫全文并报告通过。

## 6. Tests Required

`tests/skills/latex_thesis_zh/test_citation_literature.py` 与
`tests/skills/latex_thesis_zh/test_verify_bib_scanner.py` 按路径加载 ZH 脚本，并恢复
`sys.path` 与 `sys.modules`。子进程设置 `PYTHONIOENCODING=utf-8`，解释器使用 `python -X utf8`。
覆盖作者位置、重复页码、著录字段、递进阈值、参数错误、默认基线和 C2 题注组合。
公开资源同步源文件、另一语言译文、同语言镜像和 manifest。

真实论文、PDF 页面、出版事实和五个宿主不由本契约的合成测试证明。

## 7. Wrong vs Correct

错误：在 `--school` 里追加引文规则，或让缺页码的脚本编造页码。

正确：引文位置、重复页码和著录提示只在各自的显式开关后出现；`--school` 仍只增加中文题注候选。
