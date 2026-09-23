# C3 实施证据

解释器：`uv run --extra dev python -X utf8`。子进程环境：`PYTHONIOENCODING=utf-8`。
未传 `--author-cite`、`--repeat-cite`、`--college-details`、`--progression-density`。
`--current-year 2026` 是既有年份钉，不是新开关。基线在第一处 C3 产品改动前写入
`.trellis/tasks/09-22-thesis-zh-citation-literature/research/baseline/`。
实施后用同一解释器、同一路径重跑，与保存文件逐字节比较。没有为通过而改基线。

## 默认命令与逐字节比较

| 命令 | 保存退出码 | 实施后 raw stdout/stderr/exit |
| --- | --- | --- |
| `check_references.py` thesis-project `main.tex` | 1 | 与本子基线及 C2 `references-default.*` 均一致 |
| `verify_bib.py` thesis-project `references.bib` | 0 | 一致 |
| 同上 `--standard gb7714` | 1 | 一致 |
| 同上 `--standard gb7714-2025` | 1 | 一致 |
| `analyze_literature.py` `main.tex --current-year 2026` | 0 | 一致 |
| 同上 `--intro-citations --current-year 2026` | 0 | 一致 |

未使用 `--online` 或 `--online-check`。`numeric-equation-table-contract.md` 未改。
`--school` 仍不增加引文位置、页码或著录规则；这三项只在 C3 自己的开关后出现。

## 门禁退出码

| 命令 | 退出码 | 结果 |
| --- | --- | --- |
| `uv run python docs/scripts/check_resource_sync.py --write-manifest --inventory-only` | 0 | 284 条。新指南 `sourceLocale=zh`。已改中文源的 locale 仍为 `zh`。此命令不是最终通过 |
| `just ci` | 0 | 版本 1 passed；Ruff format/check 通过；Pyright 无新增 error（日志中的 warning 在既有 EN 脚本）；pytest 2289 passed, 2 skipped |
| `uv run python docs/scripts/check_resource_sync.py` | 0 | 284 条全量资源通过。CI 之后再跑一次，退出码仍为 0 |
| `just doc-build` | 0 | VitePress 1.6.4，14.62s |

措辞修正前，目标 pytest 曾因「建议页数」子串误伤「不根据 PDF 建议页数」而退出 1。
脚本改为「不根据 PDF 总页数填写页码」后，`test_citation_literature.py` 与
`test_verify_bib_scanner.py` 退出 0（28 passed）。随后的 `just ci` 覆盖全部目标测试。

## AC 映射

| AC | 测试 |
| --- | --- |
| AC1 | `test_clear_author_plus_deng_hits_until_cite_moves`；`test_clear_names_cover_accent_hyphen_particle_and_predicate`；`test_fact_sentence_and_non_author_subjects_do_not_hit`；`test_uncertain_chinese_name_does_not_claim_an_author_fact`；`test_textcite_and_citet_do_not_add_an_author_position_hint`；`test_dotted_abbreviation_does_not_split_the_sentence`；`test_incomplete_sentence_and_paragraph_boundary_are_not_guessed` |
| AC2 | `test_repeat_page_counts_keys_postnotes_and_dedup`；`test_shared_and_natural_language_postnotes_do_not_pass`；`test_repeat_mode_skips_non_visible_cites_and_states_incomplete_coverage`；`test_caption_cites_count_and_school_caption_is_not_duplicated`；`test_repeat_cite_uses_assemble_order_across_files`；`test_author_and_repeat_flags_are_independent`；`test_flags_off_do_not_assemble_or_emit_citation_codes` |
| AC3 | `test_college_details_appends_info_without_changing_standard_issues`；`test_college_details_without_author_data_skips_the_style_note`；`test_college_details_rejects_non_gb_standards` |
| AC4 | `test_progression_thresholds_count_occurrences_inside_the_section`；`test_missing_section_does_not_scan_the_whole_file`；`test_progression_and_intro_citations_are_mutually_exclusive`；`test_progression_without_section_uses_related_only` |
| AC5 | `test_default_commands_match_saved_baselines`；`test_public_docs_keep_c1_c2_and_state_c3_flags`；`test_citation_literature_flags_are_opt_in_on_help`；`test_loader_reads_zh_citation_scripts`；上表门禁 |

中文 1–4 字只出 `RC-AUTHOR-UNCERTAIN` 或 `RC-AUTHOR-COVERAGE`，文案写明作者主语不确定。
明确拉丁字母姓名加「等/等人」或报告谓词才出 `RC-AUTHOR`。

## 共享文件中由 C3 拥有的部分

- `SKILL.md`：C2 学院句之后新增的一条路由句。C1、C2 原句保留。
- `evals/evals.json`：只追加 id 55。id 1–54 未重排。
- `.trellis/spec/academic-writing-skills/index.md`：新增 `citation-placement-contract.md` 一行。
- `docs/resource-manifest.json`：C3 源文件散列，以及新指南一条 `sourceLocale=zh`。
- `README.md`、`README_CN.md`、`docs/usage.md`、`docs/zh/usage.md`、两份技能索引：C2 句之后的 C3 句。索引另加综述递进密度链接。
- `check_references.py`：仅 `--author-cite` / `--repeat-cite` 路径。C2 `CAP-PUNCT` 仍只在 `--school yanshan-ee-2025` 运行一次。
- `routing-rules.md` 及其英/中镜像：文末新增一节。前面的 C1、C2 节保留。

## MANUAL / NEEDS-LLM 边界

新候选均为 `[Script]`、Info/P3、`Meaning-Check: NEEDS-LLM`。不输出替换句，不改写键，不移动 cite。
`RC-REPEATPAGE` 只标位置供人工核页，不证明该页支持当前句，不发明页码。
多键共享 postnote 为 `RC-SHARED`。自然语言 postnote 为 `RC-POSTNOTE`，不能据此通过学院规则。
`\cites`、自定义宏传键和未展开参数记为覆盖不足。
中文姓名不确定时不宣称识别出作者。`\textcite` / `\citet` 的渲染作者不另报位置。
`--college-details` 不改既有 GB 问题序列。`inproceedings` 缺页指向学院第101项人工核实。
作者显示只给一条文件级说明：核最终 BBL/PDF 的姓在前、大写和首字母。不生成缩写，不把 `LI G Z` 当作正确源 BibTeX。
缺传统页码或只有文章号只列待核，不根据 PDF 总页数填写页码。`article` 不重复原有缺字段。
「进一步」>5、「针对」>7 的阈值标 `UNVERIFIED`。脚本不轮换同义词。六类方向和四种组织只在指南中用合成片段说明。

## UNVERIFIED

真实论文、PDF 页面、出版社事实、学校是否接受，以及五个宿主的运行，均未由本次合成测试证明。
未做在线查证。未改 `bib_scan.py`。未新增持久引用索引。

## Check revision

`--college-details` 的新增候选原先只有 `[Script]` 与 `Meaning-Check: NEEDS-LLM`，报告行没有 Priority P3。
`verify_bib.py` 现为这些 info 候选写入 `priority=P3`，并在报告中显示 `[Priority: P3]`。
无 priority 的既有问题行格式不变。默认六条命令仍由 `test_default_commands_match_saved_baselines` 比对通过。
本次检查重跑目标 pytest（116 passed）、`just lint` 与 `just typecheck`（exit 0；Pyright 仅有既有 EN warning）。
未重跑 `just ci`、资源全量检查和 `just doc-build`。公开资源未改。
