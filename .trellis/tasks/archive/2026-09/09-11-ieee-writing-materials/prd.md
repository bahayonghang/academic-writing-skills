# IEEE 论文写法蒸馏到 materials

## Goal

从本机 Zotero 库的 IEEE 论文逐篇抽取可核验写法模式，迭代写入 `materials/IEEE/` 知识包，供后续 IEEE 英文学术写作消费。该包与 Nature 蒸馏库、通用 `latex-paper-en` 写法指南分离，避免把 Nature 句式套到工业信息学 Transactions 上。

## Confirmed Facts

| 事实 | 证据 | 意义 |
| --- | --- | --- |
| 全文搜 `IEEE` 会混入非 IEEE 条目 | `zot library search IEEE` `meta.total=1298`；首条 `ZZZJXXK9` 为 ACM KDD | 语料必须用元数据过滤 |
| 元数据 IEEE 条目 353 | `research/ieee-inventory.json`；`research/corpus.md` | 逐篇范围 = 这 353 条 |
| 337 期刊 / 15 会议 / 1 preprint；262 有 PDF | 同上 | 无 PDF 的 91 篇只吃题录+摘要 |
| 最大 venue：TII 82、TIM 37、TNNLS 26 | `research/corpus.md` | 处理顺序从 TII 开始 |
| 51 条无 publicationTitle，URL 仍是 IEEE Xplore | `research/corpus.md` no_venue_samples | 计入语料，venue=`early-access` |
| 本地 SQLite + Pdfium 可读；connector 不可达 | `zot doctor`：`local_sqlite_read.available=true`，`connector-unreachable` | 只读路径不依赖 Zotero UI |
| Nature 库是 TSV 蒸馏 + 逐篇 observation | `ref/nature-writing-studio/skill/SKILL.md`；`knowledge/PROVENANCE.md` | 复用表结构，不复用 Nature 规则行 |
| 现有 IEEE 模板只覆盖版式 | `academic-writing-skills/latex-paper-en/templates/ieee.md` | 本任务只补写法知识包 |
| catalog 安装只扫 `academic-writing-skills/` | `scripts/skills_install.py` | `materials/IEEE/SKILL.md` 不会被 `just skills-install` 装走 |
| `materials/` 目前为空 | 仓库根 `materials/` | 新产品目录 |
| TII 抽样第 1 页为 `Abstract—` + `Index Terms—` + `I. INTRODUCTION` + `This study introduces` | `zot item pdf ZVIVPYR4 --pages 1` | IEEE 节序和自称与 Nature 不同 |
| 交付形态已定为知识包 A | 用户 2026-09-11 回复 `A` | 无改写 prompts，无 catalog 发布 |

## Requirements

- R1 语料：IEEE 集合等于 `research/ieee-inventory.json` 的 key 集合。过滤条件见 `research/corpus.md`。每条 observation 记录 Zotero item key、venue、DOI、PDF 是否可读。禁止把全文命中 IEEE 字样的非 IEEE 论文写入语料。
- R2 逐篇迭代：先写 `observations/<KEY>.md`，再更新 `knowledge/*.tsv` 的计数、exemplar 与 `paper_count`。`writing_rules` / `phrase_bank` 在 `paper_count >= 3` 且类别稳定后升 `core`；1–2 篇保持 `candidate`。
- R3 架构：`materials/IEEE/` 为知识包。根 `SKILL.md` 只做触发与加载路由；可执行模式在 `knowledge/*.tsv`；人读总结在 `references/`；逐篇证据在 `observations/`；语料清单在 `corpus/`；确定性校验在 `scripts/`。不建 `prompts/`、`evals/`、`agents/`。
- R4 证据保真：exemplar 必须来自该篇 PDF 或 Zotero 摘要原句。禁止编造例句、作者、venue、实验结果。PDF 摘录按字面保存，仅拼回断词。
- R5 隔离：不把 Nature 先验行拷进 IEEE TSV。不修改 `academic-writing-skills/` 下任何 catalog skill。不把本目录加入 `just skills-install`。
- R6 覆盖：有 PDF 的条目完成正文 observation（章节结构 + 至少 3 条带原文的写法观察）。无 PDF 的条目完成题录+摘要 observation，并标记 `degraded`。
- R7 出处：`knowledge/PROVENANCE.md` 记录论文数、日期、过滤规则、晋升门槛与脚本。
- R8 语言：`references/` 与 README 用中文；TSV 的 phrase / exemplar_quote 保持英文原句；rule `description` 可用中文（与 nature-writing-studio 的 description 列一致）。
- R9 处理顺序：TII → TIM → TNNLS → 其余 Transactions → 其他期刊（含 Access）→ 会议 → preprint → `early-access`。`corpus/inventory.json` 记录 `status`，支持跨会话续跑。

## Acceptance Criteria

- [ ] AC1 (R1): `materials/IEEE/corpus/inventory.json` 与 `research/ieee-inventory.json` 的 353 个 item key 集合一致；从 `zot library search IEEE` 的非 IEEE 命中中抽至少 10 条，确认不在 inventory。
- [ ] AC2 (R2,R6,R9): `observations/` 下 353 个 `<KEY>.md`；有 PDF 的 262 篇 `status=complete` 且含 Structure 与至少 3 条带原文观察；无 PDF 的 91 篇 `status=degraded` 且含摘要观察；inventory 的 `status` 与文件一致。
- [ ] AC3 (R2,R3,R7): `knowledge/` 中 `core` 的 `writing_rules` / `phrase_bank` 行 `paper_count >= 3`，且 `top_papers` 能在 `observations/` 找到对应文件；`PROVENANCE.md` 给出当时已观察篇数。
- [ ] AC4 (R3,R8): `references/writing/` 覆盖 abstract、introduction、related-work、method、experiments、conclusion；每条主张指向 `core` rule/phrase ID 或该节 `paper_count >= 5` 的 opener。
- [ ] AC5 (R4,R5): `knowledge/writing_rules.tsv` 的 `core` 行不含 Nature 强制模板（`Here we` 作为摘要必含句、methods-last、Extended Data）；`git diff -- academic-writing-skills` 为空。
- [ ] AC6 (R3): `scripts/validate_knowledge.py` 对 TSV 表头、inventory↔observation 对齐、core 门槛退出码 0。

## Out of Scope

- 新 catalog skill、docs 站点镜像、`just skills-install` 目标扩展
- `prompts/` 改写器与 IEEE 润色运行时
- 修改 `latex-paper-en` / `typst-paper` / `paper-audit` / `cover-letter` / `bib-search-citation`
- 写入 Zotero（tag、note、collection、connector import）
- 付费或自动下载缺失 PDF
- 把 1298 条全文命中当作 IEEE 语料
- 复制 Nature `writing_rules.tsv` / `phrase_bank.tsv` 的 prior 行

## Technical Notes

晋升、节枚举、TSV 清单、observation 字段与校验命令见 `design.md`。跨会话续跑与批次顺序见 `implement.md`。过滤与 venue 分布见 `research/corpus.md`。observation 字段见 `research/observation-schema.md`。
