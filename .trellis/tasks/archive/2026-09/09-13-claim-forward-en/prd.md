# latex-paper-en 主张前置检查与改写 (C1)

父任务：`.trellis/tasks/09-13-claim-forward-integration/`（需求源、术语、S1–S24 判定均在父任务 `research/`）。

## Goal

在 `latex-paper-en` 新增路由模块 `claim-forward`：脚本检出自我削弱 / 主张后置的句子并给出候选，`[LLM]` 层按参考文档做最小改写；同时建立三子任务共用的 spec 与契约测试骨架。

## Requirements

### R1 脚本 `scripts/check_claim_forward.py`

- 输入 `main.tex`，可选 `--section <key>`（键集合同 `parsers.split_sections`），`--json`。
- 5 个 `[Script]` 观察码：`CF-DISCLAIM`、`CF-SELFWEAK`、`CF-CAVEAT-POS`、`CF-HEDGE-STACK`、`CF-CLOSE-NEG`（定义见父任务 `research/delta-matrix.md` 采纳汇总）。
- 输出格式与 `improve_expression.py` 同族：`% CLAIM-FORWARD (Line N) [Severity: Info|Minor] [Priority: P3|P2]: [Script] CF-… <说明>`，随后 `% Original:`、`% Candidate:`、`% Meaning-Check: NEEDS-LLM`；文件末尾汇总行。exit 0（无 finding、section 缺失时打 `ERROR` 行仍 exit 0，与 expression 一致）。
- 豁免：含 `\cite{}` 的句子及紧邻的 prior work / previous studies / existing methods 上下文；数学环境；Limitations 段（`\section*{Limitations}` 或 `\paragraph{Limitations}`）内的限制句。
- 裸 `only` / `limited` / `not` 不报；只报搭配（terms YAML 定义）。
- 词表与句式表外置 `references/writing/claim-forward-terms.yaml`，脚本内置等值 fallback（P-ARC `paragraph-arc-terms.yaml` 先例），YAML 缺失或解析失败时静默用 fallback。

### R2 文档

- `references/modules/claim-forward.md`：命令、5 码说明、豁免、与 deai / over-claim-guard / abstract / expression 的边界（交叉引用而非重复）。
- `references/writing/claim-forward.md`：改写规则（主张前置 5 步、preferred / discouraged 句式、`CF-LOSS-FRAME` 过程编年判断、自查四问）、来源归属（两仓库 URL + MIT）、否决说明（不删不利对比、不删非主线结果、不把技术缺陷改写为范围局限）。
- `references/evidence/over-claim-guard.md` 新增 "Upward calibration (claim-forward)" 节：over-claim 阶梯为上限，hedge 降到证据已支撑档，不删 caveat 本体。
- `references/modules/routing-rules.md`：三分列表把 `claim-forward` 加入 "`[LLM]` layer only" 组；执行顺序放在 `deai` 之后、`logic` 之前。
- `references/modules/expression.md` 与 `deai.md` 各加一行指路 `claim-forward`。

### R3 SKILL.md

- 路由表新增 `claim-forward` 行（Use when / Primary command / Read next）。
- Reference Map 加入新参考文档。
- `description` 加 claim-forward / self-weakening 触发词，总长 ≤400。
- `last_updated` 改为提交日；`version` 不动。

### R4 spec 与测试

- 新建 `.trellis/spec/academic-writing-skills/claim-forward-contract.md`（术语、5 码语义、输出格式、豁免、禁改清单、paper-audit 码集合占位）；`index.md` 加索引行。
- 新建 `tests/contracts/test_claim_forward_contract.py`（EN 部分：脚本存在、5 码常量、输出前缀、exit 0、`--help` 含 `--section --json`、SKILL.md 路由行、routing-rules 分组、deai 三副本与 TIER1 哈希不变）。
- 新建 `tests/skills/latex_paper_en/test_claim_forward.py`（importlib 加载；每码正例 1 + 反例 1；引用豁免；Limitations 段豁免；YAML 缺失 fallback）。
- `tests/contracts/test_skill_contracts.py` 中 `SKILLS["latex-paper-en"]["modules"]` 加 `claim-forward`。
- `tests/contracts/test_writing_modules_alignment.py` 中 `EXPECTED_ABSENCES["check_claim_forward.py"] = ["typst"]`。

### R5 evals 与 docs

- `evals/evals.json` 追加 id 24（fixture `evals/fixtures/claim_forward_cases.tex`，5 正例 + 3 边界反例）；`evals/trigger_eval.json` 追加 ≥2 条 positive、≥1 条 negative（"reduce hedging" 类不应路由到 deai 的边界）。
- `docs/` 英文页 + `docs/zh/` 中文页各加模块段落；`docs/usage.md` 与 `docs/zh/usage.md` 路由 token 加 `claim-forward`；重生成 `resource-manifest.json`。

## Acceptance Criteria

- [ ] `check_claim_forward.py <fixture> --section introduction` 输出 5 码正例且反例不报，exit 0。
- [ ] `--json` 输出含 `code`、`line`、`severity`、`priority`、`original`、`candidate` 字段。
- [ ] `test_claim_forward_contract.py`、`test_claim_forward.py`、`test_skill_contracts.py`、`test_writing_modules_alignment.py`、`test_deai_alignment.py`、`test_trigger_evals.py`、`test_docs_bilingual_resources.py` 全绿。
- [ ] `deai_check.py`、TIER1 四模块、`parsers.py` 字节不变（哈希测试证明）。
- [ ] `uv run python docs/scripts/check_resource_sync.py` 绿；`just ci` 绿；`just doc-build` 绿。
- [ ] 参考文档含来源归属与否决说明；无 "defensive" 命名的新模块/代码。

## Constraints

- 不改 `improve_expression.py`、`analyze_abstract.py`、`analyze_logic.py`、`deai_check.py`。
- `--strength` / `--tier` 不新增语义；脚本不接受这两个 flag。
- typst-paper 不在范围。
- 词表基线：EN 无私有语料，词表精度标 UNVERIFIED，fixture 自建。

## 依赖

- 无前置；本任务先行，C2/C3 依赖本任务创建的 spec 与契约测试文件。
