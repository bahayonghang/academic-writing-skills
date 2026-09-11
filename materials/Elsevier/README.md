# Elsevier 写法知识包

从本机 Zotero 按 Elsevier 元数据门 + 10 刊精确名过滤出的 **150** 篇论文，逐篇抽取可核验写法模式。本目录是知识包，不是 catalog skill。

与 Nature 蒸馏库、`materials/IEEE/` 分离。不要把 Nature 或 IEEE Transactions 句式当作这些 Elsevier 刊的规则。

## 目录

| 路径 | 内容 |
| --- | --- |
| `SKILL.md` | 触发与加载路由 |
| `corpus/inventory.json` | 150 条语料清单与 `status` |
| `corpus/FILTER.md` | 元数据门 + 刊单 |
| `observations/` | 逐篇证据；`_schema.md` 为字段说明 |
| `knowledge/*.tsv` | 可计数规则与统计表 |
| `knowledge/PROVENANCE.md` | 观察篇数、晋升门槛、隔离声明 |
| `references/` | 中文人读总结；无 core 行时保持占位 |
| `scripts/` | `next_pending.py`、`validate_knowledge.py` |

## 续跑

```powershell
python materials/Elsevier/scripts/next_pending.py
python materials/Elsevier/scripts/validate_knowledge.py --allow-pending
python materials/Elsevier/scripts/validate_knowledge.py
```

有 PDF 的条目写正文 observation，`status=complete`。无 PDF 的条目只写题录+摘要，`status=degraded`。

处理顺序：JPC → ESWA → EAAI → Applied Energy → AEI → Energy → CES → CEP → ISA Transactions → CACE。

当前覆盖：98 complete / 52 degraded / 0 pending。
