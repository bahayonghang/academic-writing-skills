# Elsevier 语料盘点（2026-09-11）

本地 Zotero SQLite 只读。脚本：`list_elsevier_items.py`。完整条目：`elsevier-inventory.json`。

## 检索门

Elsevier 元数据（publisher 含 Elsevier，或 DOI `10.1016/`，或 URL 含 sciencedirect.com / elsevier.com）共 275 条。本任务刊单是其中的领域子集，不是 275 条全做。

刊单（选项 A，精确 `publicationTitle`，`Computers and Chemical Engineering` 归一为 `Computers & Chemical Engineering`）：

- Journal of Process Control
- Expert Systems with Applications
- Engineering Applications of Artificial Intelligence
- Applied Energy
- Advanced Engineering Informatics
- Energy（精确匹配，不含 Energy Conversion and Management 等）
- Chemical Engineering Science
- Control Engineering Practice
- ISA Transactions
- Computers & Chemical Engineering

排除 Pattern Recognition、Construction and Building Materials、Cement and Concrete Research 等。

## 规模

领域刊单 **150** 条；**98** 有 PDF，**52** 无 PDF。

## 期刊分布（刊单内）

| 数量 | venue |
| --- | --- |
| 24 | Journal of Process Control |
| 24 | Expert Systems with Applications |
| 22 | Engineering Applications of Artificial Intelligence |
| 14 | Applied Energy |
| 13 | Advanced Engineering Informatics |
| 13 | Energy |
| 11 | Chemical Engineering Science |
| 10 | Control Engineering Practice |
| 10 | ISA Transactions |
| 9 | Computers & Chemical Engineering |

全文搜 Elsevier/ScienceDirect 会混入非 Elsevier 引用。本盘点只用元数据，再用刊名精确匹配。
