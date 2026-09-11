# Implementation Plan

## Preconditions

当前仅授权规划。用户批准本规划摘要后，再 `task.py start`。实施前读 `prd.md`、`design.md`、`research/corpus.md`、`research/observation-schema.md`、`research/elsevier-inventory.json`。

只读对照：`materials/IEEE/`。不改 IEEE 包与 catalog。

Zotero：`zot --json doctor` 确认 SQLite 与 Pdfium。connector 不可达可继续。

## Ordered Work

1. **脚手架**。建立 `materials/Elsevier/`（与 IEEE 同构）。TSV 只写表头。拷贝 inventory，全部 `pending`。拷贝 `_schema.md`。写 `FILTER.md`、`PROVENANCE.md` 骨架、`SKILL.md`、中文 `README.md`。references 占位，不发明句式。
2. **脚本**。从 IEEE 复制 `validate_knowledge.py`、`next_pending.py`、`mark_observed.py`、`write_degraded.py`、`aggregate_counts.py`，改根路径、刊桶、`EXPECTED_COUNT=150`。`validate --allow-pending` 必须通过。
3. **无 PDF**。对 52 篇跑 `write_degraded.py`，inventory 标 `degraded`。
4. **Schema 首篇**。`next_pending.py` 的第一篇有 PDF 的 JPC 条目。写 complete observation，更新 TSV，不在此篇升 core。
5. **有 PDF 循环（98）**。按 R8 刊桶。可按 IEEE 收口经验：observation 只写 `observations/<KEY>.md`，禁止并行写同一 TSV；一批完成后再 `mark_observed` + 聚合。每 10 篇刷新 `n_observed`。每刊桶结束按 core 更新 references。
6. **收口**。150 篇 observation 齐。`aggregate_counts.py` 回计 core。重写 references。`validate_knowledge.py` 无 `--allow-pending` 退出 0。抽 10 条非刊单 Elsevier 条目核 AC1。`git diff -- academic-writing-skills materials/IEEE` 为空。

跨会话：从 `next_pending.py` 续跑。不要重做已 complete/degraded 的 key。

## Validation Commands

```powershell
python .trellis/tasks/09-11-elsevier-writing-materials/research/list_elsevier_items.py
python materials/Elsevier/scripts/next_pending.py
python materials/Elsevier/scripts/validate_knowledge.py --allow-pending
python materials/Elsevier/scripts/validate_knowledge.py
zot --json doctor
git diff -- academic-writing-skills materials/IEEE
```

| Gate | 证据 |
| --- | --- |
| AC1 | inventory 150 key 与 research JSON 一致；10 条非刊单 key 不在 inventory |
| AC2 | observation 150；complete=98；degraded=52 |
| AC3 | core 行 paper_count 与 top_papers 抽查 |
| AC4 | references 主张有 ID |
| AC5 | core 行无 Nature 禁运模板；IEEE/catalog diff 空 |
| AC6 | validate 退出 0 |

## Risky files / rollback

- `materials/Elsevier/knowledge/*.tsv` 同一时间只一个会话写
- `Energy` 刊名必须精确匹配
- 不要改 `materials/IEEE/`

## Completion Boundary

150 篇全部 observed 才算 AC2 完成。中途可提交脚手架与部分 observation。改写 skill 与 catalog 安装保持未做。
