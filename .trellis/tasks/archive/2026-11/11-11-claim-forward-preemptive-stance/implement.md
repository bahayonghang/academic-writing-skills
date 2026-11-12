# 执行计划

## 进入条件

- `prd.md` 的 D1–D5 已评审定稿；与建议不同的决策已回写 `design.md`。
- 已执行 `task.py start`。在此之前不写任何产品文件。
- 先读 `implement.jsonl` 列出的 spec 与本任务 `research/`，再读 `prd.md`、`design.md`。
- 写入范围以 `design.md` §1 的三张表为准。出现白名单外的文件、新接口或脚本改动即停下回到规划。

## 步骤

### P1 改写侧立场保真

1. 核对前提：在 `academic-writing-skills/` 的 `*.py` 中搜索 `invented-claim` 与 `terminology-drift`，
   确认没有脚本内嵌完整枚举。有命中则停。
2. 先改两份契约测试：`RISK_FLAGS` 加 `understatement`，新增"三方文档含双向强度规则"的断言。
   运行并确认失败。
3. 改三个 SKILL.md 的 `Risk-Flags` 行与强度规则，再改 `design.md` §1 P1 表中的模块文档与三份模式簇文档。
4. 更新 `polish-rewrite-contract.md`。
5. 验证：P1 目标测试通过；`[Script]` 可置集合断言未改动。
6. 提交点 P1。

### P2 claim-forward 指南

1. 先在 `test_claim_forward_contract.py` 与 `test_thesis_zh_guidance_fidelity.py` 新增独立断言
   （四类处置小节存在、EN 三类处置存在、"不得删除让步句"与"不新增观察码"两句存在）。确认失败。
2. 中文指南：在三类处置之后写四类处置、修复顺序说明和去重规则。既有保护句一字不动。
3. 英文指南：先补三类处置，再写四类处置。示例为英文论文语境的合成短例。
4. 两份模块文档、两份 deai 模块文档的边界句、两份 over-claim-guard 的补充段。
5. 更新 `claim-forward-contract.md` §3.1。
6. 验证：P2 目标测试通过；`CF_CODE_RE` 在两份脚本与 paper-audit 文档中的集合不变。
7. 提交点 P2。

### P3 路由、eval、示例与镜像

1. 写两份合成 fixture（八个样例，见 `design.md` §5）。逐个核对：数字自洽，无真实人名、机构与论文原句。
2. 用 Python 追加 `evals.json`（EN 25、ZH 61、Typst 17）与 `trigger_eval.json` 条目，保持原换行与缩进。
3. 改 EN/ZH 的 SKILL.md 路由行、路由说明与 `last_updated`；Typst 只改 `last_updated`。
   核对三份描述长度不超过 400 字符。
4. 写两份示例文档。
5. 重建 manifest，同步同语言镜像，完成另一语言译文，更新 `docs/usage.md` 与 `docs/zh/usage.md`。
6. 验证：全量门禁。
7. 提交点 P3。

## 验证命令

```bash
uv run --extra dev python -m pytest -q tests/contracts/test_polish_contract_alignment.py tests/contracts/test_deai_pattern_cluster_contract.py
uv run --extra dev python -m pytest -q tests/contracts/test_claim_forward_contract.py tests/contracts/test_thesis_zh_guidance_fidelity.py tests/contracts/test_defensive_ai_rhetoric_contract.py
uv run --extra dev python -m pytest -q tests/contracts/test_trigger_evals.py tests/contracts/test_skill_contracts.py tests/contracts/test_docs_bilingual_resources.py
uv run python docs/scripts/check_resource_sync.py --write-manifest --inventory-only
just ci
uv run python docs/scripts/check_resource_sync.py
just doc-build
git diff --stat -- academic-writing-skills/*/scripts academic-writing-skills/paper-audit
```

最后一条的期望输出为空。`just ci` 含版本检查、lint、typecheck、pytest 四步。
manifest 重建后必须再跑不带 `--inventory-only` 的完整检查。

## 评审门

- P1 后：`Risk-Flags` 三方一致，`[Script]` 层未扩权。
- P2 后：逐条对照 AC1–AC3；人工通读两份指南，确认没有任何一句允许删除限制或抬高未证实断言。
- P3 后：逐条对照 AC4–AC9；用 `trellis-check` 做全范围复核。

## 交付说明要求

- 每条 AC 写明实际运行的命令与结果。
- 分别报告结构检查、合成 eval、真实模型运行、真实论文评估；未做的写 UNVERIFIED。
- 不执行 push；提交按 `git-commit` 规范，中文摘要，按阶段拆分。

## 回滚

按 P3 → P2 → P1 逆序按提交回退。P1 的枚举改动必须整组回退，不得只回退部分文件。
