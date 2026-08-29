# C4 contract ownership map

2026-08-29 使用 `rg` 核对后的测试所有权：

- `tests/skills/paper_audit/test_paper_audit_synthesis.py`：canonical lane focus blocks。
- `tests/skills/paper_audit/test_paper_audit_deep_review.py`：reviewer psychology、lane guide、
  critical reviewer agent 的现有契约。
- `tests/skills/paper_audit/test_paper_audit_topology_docs.py`：agent/template/lane topology。
- `tests/contracts/test_docs_bilingual_resources.py`：源资源、双语页面与 manifest。
- `tests/contracts/test_skill_contracts.py`：SKILL/frontmatter 等通用契约；当前没有独占本任务
  四份 reference 的逐字字符串锁。

本任务应在上述现有所有权处扩展断言，并可新增一个窄的 paragraph-arc audit contract
测试；不得把所有约束误塞进 `test_skill_contracts.py`。
