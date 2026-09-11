# Design

## Ownership

`materials/IEEE/` 拥有 IEEE 写法知识包。Zotero 只读。`academic-writing-skills/` 只读。`ref/nature-writing-studio/` 只读参考。

| Requirement | Mechanism | Acceptance |
| --- | --- | --- |
| R1 | D1 元数据语料 + inventory | AC1 |
| R2,R6,R9 | D2 逐篇 observation 循环 | AC2 |
| R2,R3,R7 | D3 TSV 聚合与晋升 | AC3 |
| R3,R8 | D4 人读 references 由 core 综合 | AC4 |
| R4,R5 | D5 隔离与原句保真 | AC5 |
| R3 | D6 校验脚本 | AC6 |

## D1 — 语料与 inventory

过滤条件与 `research/corpus.md` 相同，实现已在 `research/list_ieee_items.py`。实施时把 `research/ieee-inventory.json` 拷入 `materials/IEEE/corpus/inventory.json`，并为每条增加：

```json
{
  "key": "ZVIVPYR4",
  "status": "pending",
  "observation": null
}
```

`status`：`pending` → `complete` | `degraded`。`corpus/FILTER.md` 写死过滤字段，避免后人改回全文搜索。

处理键序（稳定排序）：venue 桶（R9）→ `has_pdf` 真者优先 → `date` 降序 → `key`。`scripts/next_pending.py` 输出下一条 `pending`。

## D2 — Observation 循环

文件：`materials/IEEE/observations/<KEY>.md`，字段以 `research/observation-schema.md` 为准。实施开始时把该 schema 拷到 `observations/_schema.md`。

读取链：`zot --json item get` → `item children` → 有 PDF 则 `item pdf --pages`。connector 不可达时继续 SQLite/Pdfium。

IEEE 节枚举（写入 TSV 的 `section` 列）：

`abstract` | `index_terms` | `introduction` | `related_work` | `method` | `experiments` | `conclusion` | `appendix`

Related Work 若并入 Introduction，Structure 记 `related_work=inlined`，opener 仍算 `introduction`。

首篇校验用已抽样的 `ZVIVPYR4`，确认 schema 可填后再按 R9 顺序推进。

## D3 — Knowledge TSV

表头对齐 nature-writing-studio，节名换成 D2 枚举。初始只有表头，零数据行。禁止从 Nature 文件复制数据行。

| 文件 | 用途 | 晋升 |
| --- | --- | --- |
| writing_rules.tsv | 可执行写法规则 | candidate → core（`paper_count >= 3`） |
| phrase_bank.tsv | 句槽模板 | 同上 |
| opener_distribution.tsv | 节首 3-gram | 统计，无 core 标记 |
| gap_transitions.tsv | 节内转折 | 统计 |
| hedge_verbs.tsv | 动词证据强度 | 统计；tier 仅 causal / associative / speculative |
| cross_section_linkers.tsv | 跨节衔接 | 统计 |
| section_openers.tsv | 各节段首模板（IEEE 对应 Nature 的 results_discussion_openers） | 统计 |
| paper_story_patterns.tsv | 节序模板 | 观察到完整节序后再建 ID |
| domain_register.tsv | venue 映射的领域 | 按 venue 计数 |
| anti_ai_patterns.tsv | 仅 IEEE 语料里证实的 LLM 套话 | 默认空表；`In this paper` 不进此表 |
| cross_section_rules.tsv | 跨节硬规则 | 与 writing_rules 相同晋升 |

`writing_rules` 增加列 `status`：`candidate` | `core`。`phrase_bank` 同样。统计表不设 status。

`top_papers` 存 Zotero key，最多 5 个，便于回指 observation 文件。

预置故事骨架（可在观察中改名，不可预先当 core）：

- `SP-IEEE-001`：abstract → introduction → related_work → method → experiments → conclusion
- `SP-IEEE-002`：abstract → introduction（related inlined）→ method → experiments → conclusion
- `SP-IEEE-003`：abstract → introduction → method → experiments → conclusion（会议短文）

Nature 禁运进 core 的模板：摘要必含 `Here we`；methods-last；Extended Data Fig.；Nature Letter 节序。

IEEE 自称（`This paper proposes` / `This study introduces` / `In this paper`）进 `phrase_bank` slot=`abstract` 或 `introduction`，证据够 3 篇再 core。

## D4 — References 与路由

`references/style-guide.md`：时态、语态、自称、hedge 梯。只引用 core 行与高频 opener。

`references/writing/`：`index.md`、`abstract.md`、`introduction.md`、`related-work.md`、`method.md`、`experiments.md`、`conclusion.md`。每节先给节目标，再给已晋升句式，主张末尾写 `R00x` / `P00x`。

`SKILL.md`：YAML `description` 写触发（IEEE Transactions 写法、工业信息学/控制/仪表）；When to use / Do not use；加载顺序（style-guide → 一节 writing 文件 → 对应 TSV）。默认不加载全部 TSV。

`README.md`：中文说明知识包用途、语料规模、如何续跑 `next_pending.py`。

更新频率：每完成 10 篇刷新 TSV 计数与 `PROVENANCE.md` 的 `n_observed`；每完成一个 venue 桶或每 30 篇，重写 references 中已有证据的段落。未晋升的 candidate 不写进 references。

## D5 — 隔离与保真

白名单（可写）：

- `materials/IEEE/**`
- 本任务 `prd.md` / `design.md` / `implement.md` / `research/` / jsonl / `task.json`

只读：`academic-writing-skills/**`、`ref/nature-writing-studio/**`、Zotero sqlite、`docs/**`。

exemplar 必须能在对应 observation 的 Quotes 节找到。无 PDF 条目不得冒充正文 opener。

## D6 — 脚本

`scripts/validate_knowledge.py`：

- 十个 TSV 表头存在
- inventory 353 key = observation 文件名集合（实施中期允许 pending 无文件；任务完成时相等）
- complete/degraded 计数与 inventory 一致
- core 行 `paper_count >= 3`
- core `writing_rules` 不含禁运模板子串

`scripts/next_pending.py`：打印下一条 pending key、venue、has_pdf。

不新增 Python 依赖。不加入 `just ci` 产品测试，除非后续单独授权。完成本任务时本地运行这两个脚本。

## Data flow

```
Zotero sqlite / Pdfium
  -> inventory.json (353)
  -> next_pending.py
  -> zot item get/pdf
  -> observations/<KEY>.md
  -> increment knowledge/*.tsv
  -> (every 10) PROVENANCE.md
  -> (every venue or 30) references/*.md
  -> validate_knowledge.py
```

## Rollback

知识包可按 git 路径整目录回退。单篇写坏则删该 observation、把 inventory `status` 改回 `pending`，并按该 key 从 TSV 的 `top_papers` / 计数回滚（若该行 `paper_count` 回到 0 则删行）。不回滚 catalog skill。
