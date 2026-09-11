# Design

## Ownership

`materials/Elsevier/` 拥有 Elsevier 领域刊写法知识包。Zotero 只读。`materials/IEEE/` 与 `academic-writing-skills/` 只读。

| Requirement | Mechanism | Acceptance |
| --- | --- | --- |
| R1 | D1 刊单 inventory | AC1 |
| R3,R6,R8 | D2 逐篇 observation | AC2 |
| R3,R5 | D3 TSV 与晋升 | AC3 |
| R2,R7 | D4 references | AC4 |
| R2,R4,R5 | D5 隔离 | AC5 |
| R2 | D6 校验脚本 | AC6 |

## D1 — 语料

过滤实现：`research/list_elsevier_items.py`。实施时拷贝 `research/elsevier-inventory.json` 为 `materials/Elsevier/corpus/inventory.json`，每条加 `status=pending`、`observation=null`。

`corpus/FILTER.md` 写死：Elsevier 元数据门 + 10 刊精确名。`Energy` 不得用子串匹配。

处理序：R8 刊桶 → `has_pdf` 真者优先 → `date` 降序 → `key`。

## D2 — Observation

`materials/Elsevier/observations/<KEY>.md`，schema 见 `research/observation-schema.md`，实施时拷到 `_schema.md`。

读取链与 IEEE 相同：`zot --json item get/children/pdf`。

节枚举：`abstract` | `introduction` | `related_work` | `method` | `experiments` | `conclusion` | `appendix`。Elsevier 期刊通常无 `Index Terms`；若 PDF 有 keywords 行，记入 Structure，不强行进 opener 统计。

故事骨架（非 core，观察中填写）：

- `SP-ELS-001`：独立 Related Work
- `SP-ELS-002`：Related Work 并入 Introduction

首篇：`next_pending.py` 给出的第一篇有 PDF 的 JPC 条目，用来钉 schema。

## D3 — TSV

表头与 `materials/IEEE/knowledge/` 对齐（含 `status` 列）。初始只有表头。禁止从 Nature 或 IEEE 拷数据行。

晋升：`writing_rules` / `phrase_bank` 在 `paper_count >= 3` 升 core。`In this paper` / `this paper proposes` 进 phrase_bank，不进 `anti_ai_patterns`。

Nature 禁运：摘要必含 `Here we`；methods-last；Extended Data。

`top_papers` 存 Zotero key，最多 5 个。

## D4 — References 与路由

与 IEEE 相同的文件集。`SKILL.md` 触发：Elsevier 过程控制 / 化工 / 工业 AI 英文学术写法（JPC、CACE、EAAI、ESWA 等）。Do not use：IEEE Transactions、Nature、中文大论文。

每 10 篇刷新 `PROVENANCE.md` 的 `n_observed`。每完成一个刊桶或每 30 篇，按已有 core 更新 references。

收口时可用对照 IEEE 的 `aggregate_counts.py` 从 complete observation 回计 core 行。

## D5 — 隔离

可写：`materials/Elsevier/**`、本任务规划文件。

只读：`materials/IEEE/**`、`academic-writing-skills/**`、`ref/nature-writing-studio/**`、Zotero sqlite。

## D6 — 脚本

从 `materials/IEEE/scripts/` 复制并改根路径与 `EXPECTED_COUNT=150`：

- `validate_knowledge.py`（含 `--allow-pending`）
- `next_pending.py`（R8 刊桶）
- `mark_observed.py`
- `write_degraded.py`（52 篇无 PDF）
- `aggregate_counts.py`

不新增 Python 依赖。不把 materials 纳入 `just ci`。

## Data flow

```
Zotero sqlite / Pdfium
  -> inventory.json (150)
  -> next_pending.py
  -> zot item get/pdf
  -> observations/<KEY>.md
  -> knowledge/*.tsv
  -> references/*.md
  -> validate_knowledge.py
```

## Rollback

按 git 路径回退 `materials/Elsevier/`。单篇：删 observation，inventory 改回 pending，从 TSV 计数扣回。
