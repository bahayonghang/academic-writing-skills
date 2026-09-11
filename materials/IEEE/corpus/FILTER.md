# IEEE 语料过滤门

语料是 Zotero 元数据命中，不是全文检索。`zot library search IEEE` 的全文命中（含 PDF / 摘要 / 参考文献里出现 IEEE 字样的非 IEEE 论文）不是本包的语料。

条目来源：`.trellis/tasks/09-11-ieee-writing-materials/research/ieee-inventory.json`（2026-09-11 从本地 SQLite 只读导出，353 条）。

## 命中条件（任一成立）

- `publicationTitle` 含 `IEEE`
- `proceedingsTitle` 含 `IEEE`
- `conferenceName` 含 `IEEE`
- `publisher` 含 `IEEE`
- `journalAbbreviation` 含 `IEEE`
- DOI 以 `10.1109` 开头
- URL 含 `ieeexplore.ieee.org` 或 `ieee.org`

## 排除

- `attachment` / `note` / `annotation`
- `deletedItems`

## 规模（导出当时）

- 353 条 IEEE 条目
- 337 `journalArticle` / 15 `conferencePaper` / 1 `preprint`
- 262 有 PDF；91 无 PDF（observation 标 `degraded`）
- 51 条无 venue 字段（多为 IEEE Xplore 提前在线，URL 仍是 ieeexplore；venue 记 `early-access` / `(no venue)`）

## 处理顺序（R9）

1. IEEE Transactions on Industrial Informatics
2. IEEE Transactions on Instrumentation and Measurement
3. IEEE Transactions on Neural Networks and Learning Systems
4. 其余 venue 名含 `IEEE Transactions`
5. 其他 `journalArticle`（IEEE Access、Sensors 等）
6. `conferencePaper`
7. `preprint`
8. venue 为 `(no venue)` 或缺失（early-access）

同一桶内：有 PDF 优先，然后 `date` 降序，然后 `key`。
