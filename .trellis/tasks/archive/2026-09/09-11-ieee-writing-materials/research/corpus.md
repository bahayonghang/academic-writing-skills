# IEEE 语料盘点（2026-09-11）

来源：本地 Zotero SQLite 只读查询（`C:\Users\lyh\Zotero\zotero.sqlite`，schema 129）。脚本：`list_ieee_items.py`。完整条目：`ieee-inventory.json`。

## 检索门

`zot library search IEEE` 命中 1298 条。全文索引 `fts5-sidecar` 会把 PDF/摘要/参考文献里出现 IEEE 的非 IEEE 论文算进去（例：ACM KDD `ZZZJXXK9` Merlin）。

本任务的 IEEE 论文定义为元数据命中，条件为任一成立：

- `publicationTitle` / `proceedingsTitle` / `conferenceName` / `publisher` / `journalAbbreviation` 含 `IEEE`
- DOI 以 `10.1109` 开头
- URL 含 `ieeexplore.ieee.org` 或 `ieee.org`

排除 `attachment` / `note` / `annotation` 与 `deletedItems`。

## 规模

| 指标 | 数量 |
| --- | --- |
| IEEE 条目 | 353 |
| journalArticle | 337 |
| conferencePaper | 15 |
| preprint | 1 |
| 有 PDF | 262 |
| 无 venue 字段（多为 IEEE Xplore 提前在线，URL 仍是 ieeexplore） | 51 |

库总量 1767。无名为 IEEE 的 collection，也无 IEEE 标签。Zotero connector 本轮不可达；本地 SQLite 与 Pdfium 可读。抽样 `ZVIVPYR4`（TII, DOI `10.1109/TII.2025.3567401`）`item pdf --pages 1` 成功，outline 为空。

## 期刊/会议分布（前 16）

| 数量 | venue |
| --- | --- |
| 82 | IEEE Transactions on Industrial Informatics |
| 51 | (no venue) |
| 37 | IEEE Transactions on Instrumentation and Measurement |
| 26 | IEEE Transactions on Neural Networks and Learning Systems |
| 21 | IEEE Sensors Journal |
| 15 | IEEE Transactions on Automation Science and Engineering |
| 15 | IEEE Transactions on Cybernetics |
| 13 | IEEE Transactions on Fuzzy Systems |
| 10 | IEEE Transactions on Evolutionary Computation |
| 10 | IEEE Transactions on Systems, Man, and Cybernetics: Systems |
| 9 | IEEE Transactions on Pattern Analysis and Machine Intelligence |
| 8 | IEEE Transactions on Industrial Electronics |
| 8 | IEEE Transactions on Knowledge and Data Engineering |
| 7 | IEEE/CAA Journal of Automatica Sinica |
| 6 | IEEE Access |
| 4 | IEEE Internet of Things Journal |

其余为单篇或两篇会议/期刊，含 IEEE/CVF CVPR、ICDE。

## 抽样观察（TII `ZVIVPYR4` 第 1 页）

- 栏式：`IEEE TRANSACTIONS ON INDUSTRIAL INFORMATICS`
- 摘要：`Abstract—` 一段
- 关键词：`Index Terms—`
- 章节：罗马数字 `I. INTRODUCTION`
- 自称：`This study introduces`，未见 Nature 的 `Here we`
- 页脚：IEEE copyright / Xplore 授权行

## 对规划的含义

1. 语料是工程/控制/工业信息学为主的 IEEE Transactions，不是 Nature 生命科学语料。
2. 逐篇分析以有 PDF 的 262 篇为正文证据；其余 91 篇只吃标题、摘要、venue，observation 标 `degraded`。
3. 处理顺序建议：TII → TIM → TNNLS → 其余 Transactions → Access/会议 → 无 venue 提前在线。
