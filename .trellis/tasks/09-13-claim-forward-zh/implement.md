# C2 执行计划

前置：C1 归档；`claim-forward-contract.md` 与 `test_claim_forward_contract.py` 存在；`task.py start 09-13-claim-forward-zh` 后开始。

## 顺序

1. spec：`claim-forward-contract.md` 增 "ZH 实现" 节（词表差异、`subject_gate` / `cite_exempt`、承接句豁免、`tex_loader` 展开）。
2. terms YAML：`references/writing/claim-forward-terms-zh.yaml`。
3. 脚本：`scripts/check_claim_forward.py`（ZH）；`--help` 列出 `--section` `--json`。
4. fixture：`evals/fixtures/claim_forward_cases_zh.tex`（5 正例；反例：裸"仅为 0.018"、"尚未"痛点句、引用句"未能"、结论承接句 + 展望、"不足与展望"小节）。
5. 测试：`tests/skills/latex_thesis_zh/test_claim_forward_zh.py`；`test_claim_forward_contract.py` 增 ZH 用例（含 `analyze_conclusion.py` / `check_style_zh.py` 哈希不变断言）；`SKILLS` dict；`SMOKE_COMMANDS`。
6. 文档：`references/modules/claim-forward.md`、`references/writing/claim-forward-zh.md`、`over-claim-guard.md` 向上校准节、`routing-rules.md`、`expression.md` / `deai.md` / `conclusion.md` 各一行。
7. SKILL.md：路由行、路由规则、Rewrite Contract 纳入范围、description、`last_updated`；跑 `test_skill_contracts.py`。
8. evals：Bash python 追加 id 49（CRLF round-trip）；`trigger_eval.json` 追加。
9. docs：`docs/zh/` 与 `docs/` 镜像页、usage token、manifest 重生成。
10. 私有语料复核（不进仓库）：对 `ref/thesis/decrypted/` 5 篇跑脚本，记录每码命中数到本任务 `research/zh-baseline-run.md`（只记数字，不贴原文）。

## 验证命令

```bash
uv run python academic-writing-skills/latex-thesis-zh/scripts/check_claim_forward.py academic-writing-skills/latex-thesis-zh/evals/fixtures/claim_forward_cases_zh.tex
uv run python academic-writing-skills/latex-thesis-zh/scripts/check_claim_forward.py academic-writing-skills/latex-thesis-zh/evals/fixtures/claim_forward_cases_zh.tex --json
uv run pytest tests/contracts/test_claim_forward_contract.py tests/skills/latex_thesis_zh/test_claim_forward_zh.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_coverage.py -q
uv run pytest tests/contracts/test_skill_contracts.py tests/contracts/test_deai_alignment.py tests/contracts/test_trigger_evals.py tests/contracts/test_docs_bilingual_resources.py -q
uv run python docs/scripts/check_resource_sync.py
just ci
just doc-build
```

Windows 下 `--json` 重定向需 `PYTHONIOENCODING=utf-8`（命令内联，不 export 全局）。

## 评审门

- 门 1（步骤 4 后）：fixture 5 正例命中、反例 0 误报；`git diff --stat` 不含 `analyze_conclusion.py` / `check_style_zh.py` / `deai_check.py`。
- 门 2（步骤 7 后）：`test_skill_contracts.py` + `test_latex_thesis_zh_coverage.py` 绿。
- 门 3（步骤 10 后）：`just ci` / `check_resource_sync.py` / `just doc-build` 绿；基线复核数字记录在案。

## 回滚点

- 每门一个 commit；`git revert`。
