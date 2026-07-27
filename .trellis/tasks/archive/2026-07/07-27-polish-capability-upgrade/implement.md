# Implementation Plan: EN/ZH/Typst 润色能力升级（父任务）

父任务不写代码。本文件持有**执行顺序、模块所有权矩阵、集成 gate**，子任务各自的执行清单在
各自 `implement.md`。

## Phase 0: Review Gate

- [ ] 父 `prd.md` 的 D1-D5 五项 Scope Decision 已确认，无歧义。
- [ ] 下方所有权矩阵无悬空模块（每个产出改写的模块恰有一个 owner）。
- [ ] C1 `design.md` 评审通过——它是 C2/C3 的前置契约，未定稿前两者不得 `task.py start`。
- [ ] 基线已实测记录：`just ci` **1338 passed / exit 0 / pyright 0 errors**（2026-07-27）。

## 模块所有权矩阵

判定「是否纳入契约」的唯一标准：**该模块是否产出可直接替换原文的具体文本**。产出的若只是
"该怎么改"的指令，则改写行为发生在 LLM 侧，由 SKILL.md 的 `[LLM]` 层契约覆盖，脚本不动。

| Skill | 模块              | 脚本                    | 当前输出字段                                              | 产出具体改写？ | 契约落点            | Owner       |
| ----- | ----------------- | ----------------------- | --------------------------------------------------------- | -------------- | ------------------- | ----------- |
| EN    | `expression`      | `improve_expression.py` | `Original:` / `Revised:` / `Rationale:`                    | 是             | Script + LLM        | C2          |
| EN    | `grammar`         | `analyze_grammar.py`    | `Original:` / `Revised:` / `Rationale:`                    | 是             | Script + LLM        | C2          |
| EN    | `sentences`       | `analyze_sentences.py`  | `Original:` / **`Suggested:`** / `Rationale:`              | 是             | Script + LLM        | C2          |
| EN    | `translation`     | `translate_academic.py` | Markdown 报告：`### Translation Draft` + `% ORIGINAL:` / `% TRANSLATION:` + `### Notes` | 是（异形） | Script + LLM        | C2          |
| EN    | `deai`            | `deai_check.py`         | `-> Suggestion: <指令>`                                    | **否**（仅指令）| **仅 LLM 层**       | C1（只改文档）|
| EN    | `section-writing` / `caption` / `adapt` | 无脚本  | LLM 自由格式                                               | 是             | **仅 LLM 层**       | C1（只改文档）|
| ZH    | `expression`（新）| `check_style_zh.py`（新）| —                                                          | 部分（见 C3 design 分级）| Script + LLM | C3          |
| ZH    | `deai`            | `deai_check.py`         | `-> 建议: <指令>`                                          | **否**（仅指令）| **仅 LLM 层**       | C1（只改文档）|
| Typst | `expression` / `grammar` / `sentences` | 三脚本（TIER1 字节锁） | 同 EN                                    | 是             | Script + LLM        | C2（逐字节镜像）|
| Typst | `translation`     | `translate_academic.py` | 与 EN **不同**（未入 TIER1 锁，可独立演进）                | 是             | Script + LLM        | C2          |
| Typst | `deai`            | `deai_check.py`         | 同 EN                                                      | 否             | 仅 LLM 层           | C1（只改文档）|
| 三方  | 纯诊断模块        | compile / format / bibliography / references / tables / figures / pseudocode / spec-check / blind-review / abstract / conclusion / logic / literature / experiment / title | 挑错格式 | 否 | **不纳入契约** | — |

**deai 所有权结论**：`deai_check.py` 三个副本**均不修改**。它的 `-> Suggestion:` /`-> 建议:`
是行为指令（如"长短句交替，打破机械均匀的句长节奏"），不是替换文本；且 `deai_check.py` 受
`test_deai_alignment` 的 strict/logic 双层哈希锁保护，无必要改动不应触碰。C1 只在三个 SKILL.md
里写明：LLM 依据 deai 指令产出的改写，适用 `[LLM]` 层契约。

## Phase 1: C1 契约定稿（阻塞其余全部）

- [ ] `07-27-polish-contract-shared` 完成 `design.md` → 评审 → `task.py start` → 实现 → check。
- [ ] **交付物冻结**：字段名、取值枚举、两层分工规则、`revision_goal` / `edit_strength` 的
      参数名与取值。冻结后 C2/C3 一字不差复用。
- [ ] 契约测试落地：同时断言 EN/ZH/Typst 三方字段一致（这是父任务 AC 的核心可执行项）。

## Phase 2: C2 与 C3 并行

- [ ] `07-27-polish-en-expression-fix`（EN + Typst 镜像）
- [ ] `07-27-polish-zh-expression-module`（ZH）
- 两者都改 SKILL.md 路由表/契约段，**合并时必跑** `test_skill_contracts`（`ROUTER_ROW_RE`）。
- C2 每次改 `analyze_grammar.py` / `analyze_sentences.py` / `improve_expression.py` 都必须
  **同 commit** 镜像 typst 副本，否则 TIER1 字节锁红。

## Phase 3: 集成复审（父任务自身工作）

- [ ] 跨子任务字段一致性人工核对：EN / ZH / Typst 三方各跑一次改写类模块，比对输出契约段。
- [ ] 三把对齐锁全绿：`test_writing_modules_alignment`、`test_parsers_alignment`、
      `test_deai_alignment`。
- [ ] 轴命名扫描：全仓 grep 确认 `revision_goal` / `edit_strength` / `--tier` 三者无语义混用，
      且 `deai --tier` 行为未变（`_apply_tier` 的 `_TIER_FACTORS` 未被改动）。
- [ ] `just ci` 全绿，passed 数 ≥ 1338，pyright error 数 = 0。
- [ ] 回读父 `prd.md` 的「规划期已纠正的错误」5 条，确认无一复发。

## Validation

```bash
# 基线与终检
just ci

# 三把对齐锁单独确认
uv run --extra dev python -m pytest tests/contracts/test_writing_modules_alignment.py \
  tests/test_parsers_alignment.py tests/test_deai_alignment.py -q

# SKILL.md 路由表契约
uv run --extra dev python -m pytest tests/contracts/ -q

# deai 行为未被改动
git diff --stat -- '*/scripts/deai_check.py'   # 期望：空
```

## Rollback Points

- C1 完成后是一个安全回滚点：此时只有文档与契约测试变化，无脚本行为改动。
- C2 的 typst 镜像必须与 EN 改动**同 commit**；若需回滚 C2，两边一起回滚，否则字节锁红。
- C3 全部为新增文件 + SKILL.md 增行，回滚面独立，不影响 C1/C2。

## Known Non-Issues（勿重开）

- `pyproject.toml` 6.0.0 已于 `dd01dcb` 提交，工作区干净——**不是**遗留 P0。
- `parsers.py` 各副本差异由 `ALIGNMENTS` 锁定，属有意分歧。
- deai 阈值固定 2、burstiness 2/4/8、不移植 throat-clearing 均为已判定取舍。
- `\bmake\b` 不匹配 `makes`——不要再写 `makes it possible` 的回归用例。
