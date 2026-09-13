# C3 执行计划

前置：C1、C2 归档；`task.py start 09-13-claim-forward-audit` 后开始。

## 顺序

1. 基线哈希：记录 `audit.py`、`scholar_eval.py`、`zh_check_adapters.py`、`quality_rubrics.md`、`ISSUE_SCHEMA.md` 的 sha256，写入契约测试常量。
2. spec：`claim-forward-contract.md` 填 "paper-audit 观察码集合" 与 "禁改清单"。
3. 契约测试：`test_claim_forward_contract.py` 增 audit 用例（码集合闭合、OVER_CLAIM_GUARD 节标题与红线句、`section_discussion_conclusion` block 存在、哈希不变、ZH criteria 15 行）。先跑一次确认红（TDD）。
4. 参考文档：`OVER_CLAIM_GUARD.md` -> `CLAIM_EVIDENCE_CONTRACT.md` -> `SUBAGENT_TEMPLATES.md` -> `REVIEW_LANE_GUIDE.md` -> `REVIEWER_PSYCHOLOGY.md` -> `ZH_THESIS_REVIEW_CRITERIA.md`（条件改）。
5. agents：5 个文件各一行。
6. `tests/skills/paper_audit/test_paper_audit_topology_docs.py`：若锁 block 名集合，加 `section_discussion_conclusion`。
7. evals：fixture `evals/fixtures/claim_forward_cases.tex`；Bash python 追加 id 26（紧凑格式）；`trigger_eval.json` 追加。
8. SKILL.md：description、`last_updated`；跑 `test_skill_contracts.py`（含 paper-audit eval fixture 存在性规则）。
9. docs：`docs/` 与 `docs/zh/` paper-audit 页各加一段；manifest 重生成。

## 验证命令

```bash
uv run pytest tests/contracts/test_claim_forward_contract.py tests/skills/paper_audit/test_paper_audit_topology_docs.py -q
uv run pytest tests/contracts/test_skill_contracts.py tests/contracts/test_trigger_evals.py tests/contracts/test_docs_bilingual_resources.py tests/contracts/test_paragraph_arc_audit_contract.py tests/contracts/test_defensive_ai_rhetoric_contract.py -q
uv run python docs/scripts/check_resource_sync.py
just ci
just doc-build
```

## 评审门

- 门 1（步骤 5 后）：契约测试绿；`git diff --stat` 只含 references / agents / spec / tests。
- 门 2（步骤 8 后）：`test_skill_contracts.py` 绿；description ≤400。
- 门 3（步骤 9 后）：`just ci` / `check_resource_sync.py` / `just doc-build` 绿。

## 父任务集成复查（C3 归档后，在父任务执行）

- 三 skill 术语一致性 grep：`defensive` 不出现在新增模块名 / 码 / 文件名中。
- `CF-` 码在 EN / ZH / audit 三处定义一致（契约测试已覆盖，复查只核对文档措辞）。
- 更新 `.trellis/spec/academic-writing-skills/index.md` 描述行；父任务归档。

## 回滚点

- 每门一个 commit；`git revert`。
