# Implementation Plan

## 1. Baseline

- [x] 保存目标语义在当前 references/tests/spec 中无直接覆盖的检索证据，以及四份相关 eval 基线。
- [x] 运行 `uv run --extra dev python -m pytest tests/contracts/test_trigger_evals.py tests/contracts/test_deai_alignment.py tests/contracts/test_docs_bilingual_resources.py -q`。
- [x] 记录四份 `evals.json` 的现有顺序、最大 ID 与 fixture 绑定；新增项只追加，不重排或复用空洞 ID。

## 2. Runtime Judgment Guidance

- [x] EN：更新 `latex-paper-en/references/deai/guide.md`、`references/modules/deai.md`、`references/modules/experiment.md`。
- [x] ZH：更新 `latex-thesis-zh/references/deai/guide.md`（zh）、`references/modules/deai.md`（en）、`references/modules/experiment.md`（zh）；严格保持 manifest 所定 source locale。
- [x] Typst：更新 `typst-paper/references/DEAI_GUIDE.md`（en）、`references/modules/DEAI.md`（zh）、`references/modules/EXPERIMENT.md`（en）。
- [x] 三套 de-AI 指南都修订现有 stance-less 段：证据足够才选择较可信解释，否则明确机制未定。
- [x] 三套 de-AI/module 指南都声明：脚本的 `hedge` / `hedge_application` 建议仍然有效，但 `may/could/可能` 不替代逐机制证据。
- [x] Paper audit：更新 `references/CLAIM_EVIDENCE_CONTRACT.md`、`references/OVER_CLAIM_GUARD.md`、`references/SUBAGENT_TEMPLATES.md` 与 `agents/claims_evidence_reviewer_agent.md`。
- [x] 在 `SUBAGENT_TEMPLATES.md` 明确目标模式是 `unsupported extrapolation` 的子型，并写入 max-8 排序、重复位置合并和局部风格让位规则。

## 3. Bilingual Resource Synchronization

- [x] 对第 2 节的 13 个 source，按 manifest target 同步 26 个页面：同语言页除必要链接重写外忠实于 source，另一语言页完整翻译并保持 heading/code/inline-code/table/link shape。
- [x] 运行 `uv run python docs/scripts/check_resource_sync.py --write-manifest --inventory-only` 重建散列，并审查 13 条 `sourceLocale` 没有漂移。
- [x] 不新增公开 resource 文件，因此无需新增 sidebar 手工项；文件系统发现与既有 manifest 路径保持不变。

## 4. Regression Fixtures And Output Evals

- [x] 为 EN `.tex`、ZH `.tex`、Typst `.typ` 与 paper-audit `.tex` 各新增一个组合 fixture；每个 fixture 包含 design 矩阵的一个正例和四个边界反例。
- [x] 四份 `evals/evals.json` 各追加一个新用例，使用当前最大 ID + 1；不重排既有项，不填补 paper-audit 的缺号。
- [x] 四条新 eval 都以 `files` 绑定新 fixture。paper-audit 的非空/存在性是硬契约；其余三套按本任务更强的本地回归约束执行。
- [x] output assertions 检查逐机制 evidence mapping、`undetermined` fallback、保留有证据的强/弱措辞、禁止 invented evidence/overstatement；不得只匹配 `AI` 或 `hedge`。
- [x] 按 `testing-and-tooling.md` 用 Python 文本写入 eval JSON：EN/ZH/Typst 保持各自既有风格，paper-audit 在结尾数组前文本级 splice 紧凑条目；完成后用 JSON parser 校验，diff 必须为纯增量。

## 5. Contract Tests

- [x] 新增 `tests/contracts/test_defensive_ai_rhetoric_contract.py`：检查 13 个 source 的核心语义、三处 stance-less 安全分支、脚本 hedge 边界、paper-audit max-8 规则和四份组合 eval。
- [x] 通过唯一 fixture 路径和 prompt 语义定位新 eval，断言 ID 唯一且新增项位于列表尾部；不以具体整数 ID 锁长期行为。
- [x] 复用 `tests/contracts/test_deai_alignment.py` 验证现有脚本镜像；不再新增一套扫描 `deai_check.py` 的重复 contract assertion。

## 6. Trellis Spec Closeout

- [x] 在 Phase 3.3 新建 `.trellis/spec/academic-writing-skills/defensive-ai-rhetoric-contract.md`，使用 `## Contract:` / `## Convention:` 段式，并包含 `**Tests Required**` 或 `**Validation**`。
- [x] 写入最终组合判据、C 档边界、脚本 hedge 建议边界、stance-less 修复分支、paper-audit lane 饱和规则、正反例与验证命令。
- [x] 更新 `.trellis/spec/academic-writing-skills/index.md` 的“文档 / 内容 / 何时读”三列表，并核对 spec 与 runtime references 无语义冲突。

## 7. Validation

- [x] `uv run --extra dev python -m pytest tests/contracts/test_defensive_ai_rhetoric_contract.py tests/contracts/test_trigger_evals.py tests/contracts/test_deai_alignment.py tests/contracts/test_skill_contracts.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_coverage.py -q`
- [x] `uv run --extra dev python -m pytest tests/contracts -q`
- [x] `uv run python docs/scripts/check_resource_sync.py --skill latex-paper-en`
- [x] `uv run python docs/scripts/check_resource_sync.py --skill latex-thesis-zh`
- [x] `uv run python docs/scripts/check_resource_sync.py --skill typst-paper`
- [x] `uv run python docs/scripts/check_resource_sync.py --skill paper-audit`
- [x] `uv run python docs/scripts/check_resource_sync.py`
- [x] `just doc-build`
- [x] `just ci`
- [x] 解析四份 `evals/evals.json`，确认 JSON 有效、ID 唯一、既有顺序未变、新 fixture 全部存在。
- [x] 检查 `git diff -- academic-writing-skills/latex-paper-en/scripts/deai_check.py academic-writing-skills/latex-thesis-zh/scripts/deai_check.py academic-writing-skills/typst-paper/scripts/deai_check.py` 为空。
- [x] 有 provider 凭据且成本获授权时运行四条目标 output eval；否则在 check evidence 中写 `missing evidence`。
- [x] 检查最终 diff 只包含任务规划、13 个 source、26 个 docs targets、manifest、四组 eval/fixture、目标 test 与 spec/index；不得夹带当前工作树中的既有 Trellis 改动。

## Check Evidence

- Targeted implementation suite: `151 passed`; final focused eval/contract rerun: `113 passed`.
- Contract suite: `208 passed`.
- Full resource checker: 254 manifest entries passed; all four affected skill checks passed.
- Documentation: `just doc-build` passed.
- Final CI: Ruff passed, Pyright reported 0 errors, and pytest reported `1413 passed`.
- Scoped diff: four eval JSON files are pure additions; 13 `sourceLocale` values are unchanged;
  the three `deai_check.py` files and their threshold files have no diff.
- Provider-backed output eval: `missing evidence` (no credential/cost authorization was provided).

## Rollback Points

- Runtime/docs：每个 source 与两个 docs target 成组回滚，避免 manifest 指向过期页面。
- Eval：fixture 与对应 JSON entry 成对回滚，避免悬空路径。
- Contract：先回滚 test，再回滚 spec/index；最后重建或回滚 manifest。脚本本就不在变更范围。
