# 规范逐项检查清单（spec-check）联动约定

> 来源：07-08-spec-final-check 任务实现（2026-07-08）。latex-thesis-zh 的 spec-check
> 机制横跨 templates/*.md、check_spec.py、SKILL.md 三处，改任何一处先读本文。

---

## Convention: 逐项检查清单的五列格式与双向锁

**What**：`templates/<school>.md` 中的 `## 逐项检查清单` 段是机器可解析契约——五列表格
`ID | 检查项 | 规范依据 | 检查方式 | 适用`：

- `ID`：`^[A-Z]{2,4}-\d{2,3}$`，文件内唯一且前缀统一（yanshan=YS，规划中 THU/PKU/GEN）；
- `规范依据`：规范原文章节号（如 `§1.5.3`），必须能在规范原文中找到出处，禁止编造；
- `检查方式`：`script:<checker>`（check_spec.py `CHECKERS` 注册表键）/ `module:<模块>`
  （SKILL.md 路由表模块名）/ `llm` / `manual`；
- `适用`：`通用` / `硕士` / `博士`。

**Why**：`tests/contracts/test_spec_checklists.py` 双向锁定：`script:` 引用必须存在于
CHECKERS，且 CHECKERS 每个 checker 必须被至少一个清单引用（防死代码）；`module:` 必须是
路由表真实模块。**加新 checker 而不在任何清单引用它、或删清单条目导致 checker 失联，
契约测试都会红。**

**How**：

- 新校清单（如 thuthesis/pkuthss/generic）复用既有 checker 键；字数/数量类阈值加进
  check_spec.py `TEMPLATE_THRESHOLDS[<template>]`——仅在有可追溯官方依据时；无依据则该条
  写 `llm`/`manual`，不得套用别校阈值。
- 表格会被全局格式化 hook 重排对齐——解析基于单元格内容（`parse_checklist`），
  重排无害；但改完 SKILL.md 任何表格仍须跑 `tests/contracts/test_skill_contracts.py`。
- 阈值类检查器带 ±10% 缓冲带（落带内报 NEEDS-LLM），因规范多用“一般”措辞；
  时间敏感检查（近五年/近两年）必须用 `--year` 固定基准年，否则断言随墙钟漂移。

**联动清单**（改一处查其余）：

| 改动                            | 必须同步                                                                                                                         |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| 新增/删除 CHECKERS 键           | 至少一个 templates/*.md 清单引用它；`references/modules/spec-check.md` 内建检查器列表                                            |
| SKILL.md 路由表增删模块         | 清单 `module:` 引用、`MODULE_COMMANDS` 提示命令、coverage 测试 `SMOKE_COMMANDS`（`test_smoke_commands_cover_router_table` 强制） |
| templates/*.md 新增清单段       | `test_spec_checklists.py` 自动纳入（按 `## 逐项检查清单` 枚举，无需改测试）                                                      |
| fixture thesis-project 内容变化 | `test_check_spec.py` 的天然违规断言（YS-18/24/26 FAIL 等）与 fixture README 埋点 #24                                             |
