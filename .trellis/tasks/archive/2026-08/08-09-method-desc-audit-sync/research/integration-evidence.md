# C3 方法叙述接线集成证据

日期：2026-08-09

## 病例与干净对照

端到端 fixture：

- `tests/fixtures/paper_audit/method_narrative_case.tex`
- `tests/fixtures/paper_audit/method_narrative_clean.tex`
- `tests/fixtures/paper_audit/method_narrative_case.typ`
- `tests/fixtures/paper_audit/method_narrative_clean.typ`
- `tests/fixtures/paper_audit/method_narrative_case_zh.tex`
- `tests/fixtures/paper_audit/method_narrative_clean_zh.tex`

EN LaTeX、Typst 与 zh 显式选章工作流的病例均解析出恰好三条 M-* issue：

| Code | Severity | Priority | 评分语义 |
| --- | --- | --- | --- |
| `M-HEADING` | Minor | P2 | soundness 扣 0.5 |
| `M-SEQWORD` | Info | P3 | 显式过滤，不扣分 |
| `M-EQUATION` | Minor | P2 | soundness 扣 0.5 |

对应干净 fixture 均为零条 M-* issue。`M-EDGETABLE` 仍由三个写作技能输出为 LLM 工作表，
但 paper-audit 解析器从不把其标记或表格行转成 issue。结构化 finding 的
Current/Suggested/Rationale/Meaning-Check 续行同样不再膨胀 issue 数量。仅活动 finding 块内的
这些续行会被抑制；混合输出中独立出现的裸诊断行仍按既有 Minor/P2 兜底语义保留，任意非续行
都会关闭活动块。

paper-audit Phase 0 对英文 `.tex` 和所有 `.typ` 输入各保留一次 `--cross-section` 调用，并各追加
一次 `--section methods` 调用；zh `.tex` 与 PDF 不追加方法节调用。zh fixture 只通过
`latex-thesis-zh --method-narrative --section <章名>` 的显式选章工作流验证。

## 评分链

病例与干净版经 `run_audit(..., scholar_eval=True)` 对照：

- soundness 分差为 `1.0`；
- 分差只来自两条 Minor finding，每条沿用既有 `0.5` 权重；
- `M-SEQWORD` 的 Info finding 保留在报告上下文，但不进入 ScholarEval；
- quick-audit 输出显式显示 Info/P3，Phase 0 上下文摘要计入 Info，模块表保留 Info/P3；
- 其余 script score 维度逐项相等。

`MODULE_DIMENSION_MAP`、九维权重、Critical/Major/Minor 权重及 paper-audit `version` 均未修改。

## 红线负例

三类合法行内标题继续由各技能 fixture 锁定为不报 M-HEADING：

- EN/Typst Related Work 分组标题：
  `tests/skills/latex_paper_en/test_latex_method_narrative.py` 与
  `tests/skills/typst_paper/test_typst_method_narrative.py`；
- Typst 实验分析段 lead-in：
  `test_typst_experiment_lead_ins_do_not_enter_method_scope`；
- zh `\paragraph{核心结论概括}`：
  `tests/skills/latex_thesis_zh/test_method_narrative.py`。

新增 diff 的措辞扫描未命中 `writing quality`、`写作质量` 或 `叙述质量`。Critical Reviewer
中既有的 DON'T wording 未被本任务修改，不属于新增红线命中。

## 验证记录

- `rtk uv run --extra dev ruff format --check tests/skills/paper_audit/test_method_narrative_audit_integration.py`
  - 通过，1 file already formatted。
- `rtk uv run --extra dev ruff check tests/skills/paper_audit/test_method_narrative_audit_integration.py`
  - 通过。
- `rtk uv run --extra dev python -m pytest tests/skills/paper_audit/test_method_narrative_audit_integration.py -q`
  - `3 passed`。
- `rtk uv run --extra dev python -m pytest tests/skills/paper_audit/ tests/contracts/ -q`
  - `568 passed`。
- 三技能方法叙述测试加 `tests/contracts/test_method_narrative_alignment.py`
  - `33 passed`。
- `rtk uv run python docs/scripts/check_resource_sync.py --skill <skill>`
  - `latex-thesis-zh`、`latex-paper-en`、`typst-paper`、`paper-audit` 均通过，manifest 为
    `256 entries`。
- `rtk uv run python docs/scripts/check_resource_sync.py`
  - 全量资源检查通过，`256 entries`。
- `rtk just doc-build`
  - VitePress 构建通过。
- `rtk just ci`
  - Ruff 通过；Pyright `0 errors, 72 warnings`；pytest `1465 passed`。

## 证据边界

方法叙述候选检查的 hypothesis 仅由合成病例、干净对照和合法标题负例支持。真实论文语料的
查准率与召回率仍为 **UNVERIFIED**，不得由上述自动化结果外推为真实论文精度结论。该边界需由
主会话写入父任务 journal；C3 实施代理不执行 parent journal、commit 或 archive。
