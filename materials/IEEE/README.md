# IEEE 写法知识包

从本机 Zotero 库按元数据过滤出的 **353** 篇 IEEE 论文，逐篇抽取可核验写法模式。本目录是知识包，不是 catalog skill，不会被 `just skills-install` 安装。

与 Nature 蒸馏库、通用 `latex-paper-en` 写法指南分离。不要把 Nature 句式当作 IEEE Transactions 规则。

## 目录

| 路径 | 内容 |
| --- | --- |
| `SKILL.md` | 触发与加载路由 |
| `corpus/inventory.json` | 353 条语料清单与 `status` |
| `corpus/FILTER.md` | 元数据过滤门（全文检索不是语料） |
| `observations/` | 逐篇证据；`_schema.md` 为字段说明 |
| `knowledge/*.tsv` | 可计数规则与统计表 |
| `knowledge/PROVENANCE.md` | 观察篇数、晋升门槛、隔离声明 |
| `references/` | 中文人读总结；无 core 行时保持占位 |
| `scripts/` | `next_pending.py`、`validate_knowledge.py` |

## 续跑

跨会话指针是 `corpus/inventory.json` 里每条的 `status`（`pending` / `complete` / `degraded`）。不要重做已完成的 key。

下一篇 pending：

```powershell
python materials/IEEE/scripts/next_pending.py
```

中期校验（允许尚未写 observation 的 pending）：

```powershell
python materials/IEEE/scripts/validate_knowledge.py --allow-pending
```

353 篇全部 observed 后去掉 `--allow-pending`：

```powershell
python materials/IEEE/scripts/validate_knowledge.py
```

当前覆盖：261 complete / 92 degraded / 0 pending。`next_pending.py` 在无 pending 时退出码 1。

有 PDF 的条目写正文 observation（结构 + 至少 3 条带原文观察），`status=complete`。无 PDF 的条目只写题录+摘要，`status=degraded`。

处理顺序：TII → TIM → TNNLS → 其余 Transactions → 其他期刊 → 会议 → preprint → early-access。同一桶内有 PDF 优先。
