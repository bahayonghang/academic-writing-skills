# Implementation Plan: C1 共享润色契约

## Phase 0: Review Gate

- [ ] `design.md` 的三轴命名、字段名、`Risk-Flags` 闭集、适用范围三分法经评审冻结。
- [ ] 确认本任务**不改任何脚本**——`git diff --stat -- '*/scripts/'` 全程应为空。
- [ ] 确认 `deai_check.py` 三副本零改动的判定（其输出为指令非替换文本）被接受。
- [ ] PRD + design 评审通过前保持 planning，不进实现。

## Phase 1: 三方 SKILL.md 契约段

- [ ] `latex-paper-en/SKILL.md` Output Contract 段追加四字段定义 + 两层分层规则表 +
      适用/仅LLM/排除三分清单。
- [ ] `latex-thesis-zh/SKILL.md` 同上（字段标识符保持英文，说明文本中文）。
- [ ] `typst-paper/SKILL.md` 同上。
- [ ] 三方 Required Inputs 追加 `--goal` / `--strength` 说明，注明默认 `grammar` / `minimal`。
- [ ] 三方 `last_updated` → 今日；`version` 保持 `6.0.0` 不动。

## Phase 2: routing-rules 与模块文档

- [ ] 三方 routing-rules 写入：
  - 契约适用范围三分法（含**排除清单逐项列出**，不靠默认）。
  - 追问边界：编辑目标/幅度/作者原意**只在确实影响本次编辑时**追问，不得变成固定问卷；
    与既有「自动推断模块，不默认追问」规则的关系写清。
  - 「改写不得升高措辞强度，升高即置 `overstatement`」。
  - deai 例外：其 `-> Suggestion:` / `-> 建议:` 是行为指令，LLM 据此产出的改写走 `[LLM]` 层。
- [ ] EN `references/modules/expression.md` / `grammar.md` / `sentences.md`：加 over-claim
      指针（`../evidence/over-claim-guard.md`）+ 契约段输出示例。
- [ ] Typst `references/modules/EXPRESSION.md` / `GRAMMAR.md` / `SENTENCES.md`：同上，指针为
      `../OVER_CLAIM_GUARD.md`。
- [ ] 为 ZH `references/modules/expression.md` 准备指针文案（文件由 C3 创建，C1 只交付文案，
      写在本任务 notes 里供 C3 取用）。
- [ ] 确认 over-claim-guard **未**被加入任何 SKILL.md 顶层 Reference Map。

## Phase 3: 契约测试

- [ ] 新建 `tests/contracts/test_polish_contract_alignment.py`：
  - 路径常量从 `tests.support.paths` 导入（不手写相对路径）。
  - 断言三方 SKILL.md 均含四个字段名，且字面一致。
  - 断言 `Risk-Flags` 闭集在三方文档中取值集合相同。
  - 断言 `[Script]` 层禁止 `PRESERVED` 的规则在三方均有表述。
  - 断言排除清单在三方 routing-rules 中存在且非空。
- [ ] 断言 `--tier` 语义未被挪用：grep 三方文档确认 `--tier` 仅出现在 deai 语境。

## Phase 4: Validation

- [ ] `git diff --stat -- '*/scripts/'` 为空（C1 零脚本改动）。
- [ ] `git diff -- '*/scripts/deai_check.py'` 为空。
- [ ] `uv run --extra dev python -m pytest tests/contracts/ -q` 全绿（含 `ROUTER_ROW_RE`）。
- [ ] `just ci` 全绿，passed ≥ 1338，pyright error = 0。
- [ ] 人工核对：三方 SKILL.md 的四字段块逐字比对无差异。

## Review Gate（交付冻结）

- [ ] 向 C2/C3 交付冻结清单：`--goal` / `--strength` 参数名与取值、四个字段名、
      `Risk-Flags` 闭集、`[Script]` 禁 `PRESERVED` 规则、适用范围三分法。
- [ ] 冻结后若 C2/C3 提出契约需要变更，**回到 C1 改** 再同步，不允许子任务各自变形。

## Rollback Points

- Phase 1-2 是纯文档改动，可整体 `git revert` 无副作用。
- Phase 3 的契约测试若在 C2/C3 落地前就断言脚本输出，会导致红——**测试只断言文档**，
  脚本输出的断言归 C2/C3。这是本任务最容易踩错的边界。
