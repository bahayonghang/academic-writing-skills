# Implementation Plan: C3 ZH expression 模块

## Phase 0: Review Gate

- [ ] C1 `design.md` 已冻结；本任务复用其四字段 / `Risk-Flags` 闭集 / `--goal` / `--strength`。
- [ ] `design.md` §2 的九个检查器档位经评审确认，尤其 `E-INCOMP` / `E-PUNCT` / `E-UNITFONT`
      三个**不能 auto** 的判定。
- [ ] 确认本模块**不实现人称检查**（归 `abstract` 的 T-VOICE / T-OPEN）。
- [ ] 确认新脚本**不加入** `TIER1_HASH_GROUPS`。

## Phase 1: 写作参考（指导层，先做）

- [ ] 新建 `references/formatting/number-unit-guide-zh.md`：
  - GB/T 15834（标点）、GB/T 15835（数字）、GB 3100 / GB/T 3101 / GB/T 3102（量和单位）
  - 中文特有规则：概数用汉字、序数用中文、数值与单位空格、单位正体
  - **标准优先级声明**：学校模板 > 通用国标；冲突以 `templates/<template>.md` 为准
- [ ] 新建 `references/modules/expression.md`：
  - 指向 `../writing/academic-style-zh.md` 为规则真相源
  - 嵌入 design §1 的边界表（人称 / over-claim / YS-36 / deai D1 / logic 各自 owner）
  - 加 C1 供的 over-claim 指针文案（`../writing/over-claim-guard.md`）
  - 九个检查器 ID 与档位对照表

## Phase 2: 脚本实现

- [ ] 新建 `scripts/check_style_zh.py`，按 design §2 逐检查器实现：
  - [ ] A 档：`E-COLLOQ`、`E-COLLOC`、`E-NUMSPACE`
  - [ ] B 档：`E-ABSOLUTE`、`E-INCOMP`、`E-PUNCT`、`E-NUMSTYLE`、`E-LONGSENT`
  - [ ] B 档特例：`E-UNITFONT`（只读数学环境，永不给替换，输出须说明红线原因）
- [ ] 每个检查器实现其 design 声明的**排除条件**——排除条件不是可选项，是契约的一部分。
- [ ] 接入 `tex_loader.assemble` + `doc.lineref`，多文件工程定位为 `源文件:行号`。
- [ ] 追加 C1 四字段；`[Script]` 层 `Meaning-Check` 恒 `NEEDS-LLM`。
- [ ] 加 `--goal` / `--strength`，默认 `grammar` / `minimal`。
- [ ] 中文断句在本脚本内独立实现，**不复用** `deai_check.py` 的断句逻辑。

## Phase 3: SKILL.md 接线

- [ ] 路由表新增 `expression` 行（Use when / Primary command / Read next）。
- [ ] Reference Map 加 `references/writing/academic-style-zh.md`（**关闭 P1-1**）与
      `references/formatting/number-unit-guide-zh.md`。
- [ ] 路由规则串行序列插入 `expression`（第 2/3 层，见 `writing-philosophy-zh.md:124-133`）。
- [ ] `references/modules/routing-rules.md` 写入五条边界：
  - vs `abstract`（人称走 T-VOICE / T-OPEN）
  - vs `over-claim-guard`（强度分级不在此）
  - vs `spec-check` YS-36（模板专属数字规范不在此，双向指路）
  - vs `deai` D1（可读性长度 ≠ 均匀度 CV，不重复报同一句）
  - vs `logic`（段落与论证不在此）
- [ ] `last_updated` → 今日；`version` 保持 6.0.0。

## Phase 4: 测试

- [ ] 新建 `tests/skills/latex_thesis_zh/test_check_style_zh.py`：
  - 路径常量从 `tests.support.paths` 取；ZH 副本走 **importlib 按路径加载** + 守卫断言
    （bare import 会拿到 EN 副本）。
- [ ] 每检查器**正例 + 反例**各至少一条；反例须覆盖 design 声明的排除条件：
  - [ ] `E-PUNCT` 反例：括号内全英文用英文标点 → 不报
  - [ ] `E-INCOMP` 反例：承前省略主语的合法句 → 只出候选不出断言
  - [ ] `E-UNITFONT` 断言：输出中**无**替换文本，且含数学环境说明
  - [ ] `E-NUMSTYLE` 反例：图表编号/公式编号 → 不报
  - [ ] `E-LONGSENT` 反例：公式行/列举项 → 不报
- [ ] 无人称检查器的负向断言（确保没有人后来顺手加上）。
- [ ] 契约字段测试：输出含四字段，`Meaning-Check` 恒 `NEEDS-LLM`。
- [ ] 多文件工程定位测试：`源文件:行号` 形态正确。
- [ ] `evals/trigger_eval.json` 新增 `expression` 触发用例——**走 Bash python 写入**。

## Phase 5: Validation

```bash
uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/test_check_style_zh.py -q
uv run --extra dev python -m pytest tests/contracts/ -q
git diff --stat -- '*/latex-paper-en/' '*/typst-paper/'    # 期望空
git diff --stat -- '*/scripts/deai_check.py' '*/scripts/analyze_abstract.py' '*/scripts/check_spec.py'  # 期望空
just ci
```

- [ ] `just ci` 全绿，passed ≥ 1338，pyright error = 0。
- [ ] 端到端：对 `evals/fixtures/thesis-project/` 跑一次 `check_style_zh.py`，人工核对输出无
      明显误报，且未报出应由其他模块负责的问题。

## Rollback Points

- Phase 1 纯新增参考文档，可独立回滚。
- Phase 2 新增脚本，未接线前不影响任何现有行为。
- Phase 3 是**唯一有外部可见影响**的阶段（路由表变化）；回滚它即可让 skill 回到当前行为。
- Phase 4 与 Phase 2/3 同 commit。

## 已知陷阱

- bare import 拿到的是 EN 副本 —— ZH 测试必须 importlib 按路径加载 + 守卫断言。
- `evals.json` / `trigger_eval.json` 走 Bash python 写入，不用 Edit/Write。
- 不给 pytest 加 `PYTHONIOENCODING=utf-8`；Windows 重定向 JSON 时才加，且不 export 全局。
- 新脚本不要加进 `TIER1_HASH_GROUPS`。
- 只改 `last_updated`，不 bump `version`。
