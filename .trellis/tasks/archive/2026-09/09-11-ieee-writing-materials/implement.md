# Implementation Plan

## Preconditions

当前仅授权规划。用户明确批准本规划摘要后，再 `task.py start`。实施前读 `prd.md`、`design.md`、`research/corpus.md`、`research/observation-schema.md`、`research/architecture-notes.md`。工作树保持 `academic-writing-skills/` 无本任务 diff。

Zotero：`zot --json doctor` 确认 `local_sqlite_read.available` 与 `pdf_backend.available`。connector 不可达可继续。

## Ordered Work

1. **脚手架**。建立 `materials/IEEE/` 目录树（design D3/D4/D6）。TSV 只写表头。拷贝 inventory，所有 `status=pending`。拷贝 `_schema.md`。写 `FILTER.md`、空 `PROVENANCE.md` 骨架、路由 `SKILL.md`、中文 `README.md`。`references/writing/` 先放 index 与各节占位，占位中只写「待 core 行填充」，不发明句式。
2. **校验脚本**。实现 `validate_knowledge.py` 与 `next_pending.py`。脚手架阶段允许 353 个 pending 无 observation；完成态才要求文件集合相等。脚本需支持 `--allow-pending`。
3. **Schema 首篇**。处理 `ZVIVPYR4`（TII，已抽样第 1 页）。补全 PDF 后续页，写 observation，更新 TSV。用这一篇钉死字段，不在此篇晋升 core。
4. **TII 循环（82）**。`next_pending.py` 取下一 TII key。一篇：get/children/pdf → observation → TSV。每 10 篇更新 `PROVENANCE.md` 的 `n_observed`。TII 桶结束后按已有 core/高频 opener 写第一版 `references/`（无 core 则保持占位）。
5. **其余 venue 桶**。TIM → TNNLS → 其他 Transactions → 其他期刊 → 会议 → preprint → early-access。规则同步骤 4。无 PDF 标 `degraded`。
6. **收口**。353 篇 observation 齐。重写 references，删除仍无 core 的臆测句。`validate_knowledge.py` 无 `--allow-pending` 退出 0。抽 10 条非 IEEE 全文命中核对 AC1。确认 `git diff -- academic-writing-skills` 为空。

跨会话：从 `next_pending.py` 继续，不重做已 `complete`/`degraded` 的 key。单次会话以完成当前篇并落 TSV 为最小提交单元；不要只读 PDF 不写文件。

## Validation Commands

```powershell
python .trellis/tasks/09-11-ieee-writing-materials/research/list_ieee_items.py
python materials/IEEE/scripts/next_pending.py
python materials/IEEE/scripts/validate_knowledge.py --allow-pending
python materials/IEEE/scripts/validate_knowledge.py
zot --json doctor
zot --json item get ZVIVPYR4
git diff --check -- materials/IEEE
git diff -- academic-writing-skills
```

| Gate | 证据 |
| --- | --- |
| AC1 | inventory key 集合差集为空；10 条非 IEEE 全文命中的 key 列表 |
| AC2 | observation 文件数 353；complete=262；degraded=91 |
| AC3 | core 行 paper_count 与 top_papers 抽查 |
| AC4 | references 中每条主张的 ID 能在 TSV 找到 |
| AC5 | 对 writing_rules core 行搜禁运子串；catalog diff 空 |
| AC6 | validate 退出码 0 |

`just ci` 四步应保持原状通过。本任务不把 materials 纳入 pytest，除非校验脚本在实施中被证明需要锁。

## Risky files / rollback

- `materials/IEEE/knowledge/*.tsv`：并发改同一 TSV 会丢行。同一时间只一个会话写。
- `corpus/inventory.json`：status 与 observation 必须同一次改。
- 回滚单篇：见 design D5/Rollback。

## Completion Boundary

353 篇全部 observed 才算 AC2 完成。中途会话可以提交脚手架与部分 observation，任务状态仍为未完成。改写 skill、catalog 安装、docs 镜像保持未做。真实投稿收益 UNVERIFIED。
