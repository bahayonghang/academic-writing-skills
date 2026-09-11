# Elsevier 领域刊语料过滤门

语料是 Zotero 元数据命中后再按刊名精确匹配，不是全文检索。

条目来源：`.trellis/tasks/09-11-elsevier-writing-materials/research/elsevier-inventory.json`（2026-09-11 只读导出，150 条）。

## Elsevier 元数据门（任一成立）

- `publisher` 含 `Elsevier`
- DOI 以 `10.1016/` 开头
- URL 含 `sciencedirect.com` 或 `elsevier.com`

## 刊单（精确 `publicationTitle`）

- Journal of Process Control
- Expert Systems with Applications
- Engineering Applications of Artificial Intelligence
- Applied Energy
- Advanced Engineering Informatics
- Energy（精确匹配，不含 Energy Conversion and Management 等）
- Chemical Engineering Science
- Control Engineering Practice
- ISA Transactions
- Computers & Chemical Engineering（`Computers and Chemical Engineering` 归一为此名）

## 排除

- `attachment` / `note` / `annotation` / `deletedItems`
- Pattern Recognition、Construction and Building Materials、Cement and Concrete Research 等非刊单
- 275 条 Elsevier 元数据中未列入刊单的条目

## 规模（导出当时）

- 150 条
- 98 有 PDF；52 无 PDF（observation 标 `degraded`）

## 处理顺序（R8）

1. Journal of Process Control
2. Expert Systems with Applications
3. Engineering Applications of Artificial Intelligence
4. Applied Energy
5. Advanced Engineering Informatics
6. Energy
7. Chemical Engineering Science
8. Control Engineering Practice
9. ISA Transactions
10. Computers & Chemical Engineering

同一桶内：有 PDF 优先，然后 `date` 降序，然后 `key`。
