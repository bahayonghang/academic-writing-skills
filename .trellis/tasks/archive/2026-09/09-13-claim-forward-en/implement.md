# C1 执行计划

前置：父任务 `research/` 两文件已读；`task.py start 09-13-claim-forward-en` 后开始。

## 顺序

1. spec 先行：写 `.trellis/spec/academic-writing-skills/claim-forward-contract.md`（术语、5 码、输出格式、豁免、禁改清单、"paper-audit 观察码集合：待 C3 填 5 码" 占位）；`index.md` 加行。
2. terms YAML：`references/writing/claim-forward-terms.yaml`。
3. 脚本：`scripts/check_claim_forward.py`（`_DEFAULT_TERMS` 与 YAML 等值；argparse：`file`、`--section`、`--json`）。`--help` 必须列出两个 flag（ROUTER_ROW_RE 测试会跑 `--help`）。
4. fixture：`evals/fixtures/claim_forward_cases.tex`（Case A–E 各对应一码正例；Case F 引用豁免；Case G Limitations 段；Case H 裸 only/limited 反例）。
5. 测试：`tests/skills/latex_paper_en/test_claim_forward.py`；`tests/contracts/test_claim_forward_contract.py`；`SKILLS` dict、`EXPECTED_ABSENCES` 两处改动。
6. 文档：`references/modules/claim-forward.md`、`references/writing/claim-forward.md`、over-claim-guard 新节、routing-rules 三分列表 + 执行顺序、expression.md / deai.md 各一行。
7. SKILL.md：路由行、Reference Map、description、`last_updated`。全局 markdown hook 会对齐表格；提交前跑 `test_skill_contracts.py` 确认 ROUTER_ROW_RE 仍匹配。
8. evals：用 Bash python 写 `evals/evals.json`（读取 -> append id 24 -> `json.dumps(indent=2, ensure_ascii=False)` + 换行 -> 保持 CRLF）；`trigger_eval.json` 同法追加。
9. docs：EN 页与 ZH 镜像页各加模块段（实际路径以 `docs-bilingual-resources.md` 为准）；`docs/usage.md` / `docs/zh/usage.md` 加 token；`uv run python docs/scripts/check_resource_sync.py --write-manifest --inventory-only`。

## 验证命令

```bash
uv run python -B academic-writing-skills/latex-paper-en/scripts/check_claim_forward.py academic-writing-skills/latex-paper-en/evals/fixtures/claim_forward_cases.tex
uv run python -B academic-writing-skills/latex-paper-en/scripts/check_claim_forward.py academic-writing-skills/latex-paper-en/evals/fixtures/claim_forward_cases.tex --json
uv run pytest tests/contracts/test_claim_forward_contract.py tests/skills/latex_paper_en/test_claim_forward.py -q
uv run pytest tests/contracts/test_skill_contracts.py tests/contracts/test_writing_modules_alignment.py tests/contracts/test_deai_alignment.py tests/contracts/test_trigger_evals.py tests/contracts/test_docs_bilingual_resources.py -q
uv run python docs/scripts/check_resource_sync.py
just ci
just doc-build
```

## 评审门

- 门 1（步骤 3 后）：脚本对 fixture 输出 5 正例、0 反例误报；`git diff --stat` 不含 `deai_check.py` / TIER1 模块。
- 门 2（步骤 7 后）：`test_skill_contracts.py` 绿；description ≤400。
- 门 3（步骤 9 后）：`just ci` + `check_resource_sync.py` + `just doc-build` 全绿。

## 回滚点

- 每门一个 commit；回滚 = `git revert` 该 commit。新文件为主，冲突面小。
