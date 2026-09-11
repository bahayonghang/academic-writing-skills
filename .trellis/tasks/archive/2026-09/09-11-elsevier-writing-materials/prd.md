# Elsevier 顶刊写法蒸馏到 materials

## Goal

从本机 Zotero 库中过程控制 / 化工 / 工业 AI 的 Elsevier 期刊论文逐篇抽取可核验写法模式，写入 `materials/Elsevier/` 知识包。该包与 `materials/IEEE/`、Nature 蒸馏库分离。

## Confirmed Facts

| 事实 | 证据 | 意义 |
| --- | --- | --- |
| IEEE 知识包可对照 | `materials/IEEE/`；提交 `8320fd3` | 复用目录、observation 字段、校验脚本 |
| Elsevier 元数据上限 275 | `research/corpus.md` | 全文检索作废 |
| 领域刊单 150 篇，98 有 PDF | `research/elsevier-inventory.json` | 逐篇范围 = 这 150 条 |
| 刊量：JPC 24、ESWA 24、EAAI 22、Applied Energy 14、AEI 13、Energy 13、CES 11、CEP 10、ISA 10、CACE 9 | 同上 | 处理顺序按此桶 |
| 用户选定领域刊单 A | 2026-09-11 回复 `A` | 不做 275 全库，不做控制三刊 |
| 知识包形态已定 | IEEE 任务选项 A | 无改写 skill、无 catalog 安装 |

## Requirements

- R1 语料：集合 = `research/elsevier-inventory.json` 的 150 个 key。先过 Elsevier 元数据门，再按刊单精确匹配 `publicationTitle`。`Energy` 只接受精确刊名。禁止把全文命中 Elsevier 字样的非 Elsevier 论文写入语料。
- R2 产物：`materials/Elsevier/` 镜像 `materials/IEEE/`：`SKILL.md`、`observations/`、`knowledge/*.tsv`、`references/`、`corpus/`、`scripts/`。不建 `prompts/`。不安装 catalog。不改 `academic-writing-skills/` 与 `materials/IEEE/`。
- R3 逐篇：先 `observations/<KEY>.md`，再更新 TSV。`writing_rules` / `phrase_bank` 在 `paper_count >= 3` 后升 `core`。
- R4 证据：exemplar 来自该篇 PDF 或 Zotero 摘要原句。禁止编造。PDF 只拼回断词。
- R5 隔离：不拷 Nature 或 IEEE 的 TSV 数据行。IEEE 只作目录与脚本对照。
- R6 覆盖：98 篇有 PDF 的条目 complete（结构 + 至少 3 条带原文观察）。52 篇无 PDF 的条目 degraded。
- R7 语言：`references/` 与 README 用中文；TSV 的 phrase / exemplar 保持英文原句。
- R8 顺序：JPC → ESWA → EAAI → Applied Energy → AEI → Energy → CES → CEP → ISA Transactions → CACE。同桶有 PDF 优先，然后日期降序、key。

## Acceptance Criteria

- [ ] AC1 (R1): `materials/Elsevier/corpus/inventory.json` 与 `research/elsevier-inventory.json` 的 150 个 item key 一致；抽至少 10 条非刊单 Elsevier 元数据条目（如 Pattern Recognition）确认不在 inventory。
- [ ] AC2 (R3,R6,R8): `observations/` 下 150 个 `<KEY>.md`；complete=98 且含 Structure 与至少 3 条带原文观察；degraded=52；inventory `status` 与文件一致。
- [ ] AC3 (R3,R5): core 的 `writing_rules` / `phrase_bank` 行 `paper_count >= 3`，`top_papers` 能在 `observations/` 找到文件；`PROVENANCE.md` 给出已观察篇数。
- [ ] AC4 (R2,R7): `references/writing/` 覆盖 abstract、introduction、related-work、method、experiments、conclusion；主张指向 core ID。
- [ ] AC5 (R2,R5): core 行不含 Nature 强制模板（摘要必含 `Here we`、methods-last、Extended Data）；`git diff -- academic-writing-skills materials/IEEE` 为空。
- [ ] AC6 (R2): `scripts/validate_knowledge.py` 对表头、inventory↔observation、core 门槛退出码 0。

## Out of Scope

- 改写器、catalog 安装、docs 镜像
- 修改 `materials/IEEE/` 或六技能源码
- 写入 Zotero、下载缺失 PDF
- 275 条 Elsevier 全库；Pattern Recognition、建材、水泥等刊
- 把 IEEE TSV 行改名后当作 Elsevier 规则

## Technical Notes

刊单、过滤与 PDF 数见 `research/corpus.md`。observation 字段见 `research/observation-schema.md`。脚本与目录见 `design.md`。批次顺序见 `implement.md`。
