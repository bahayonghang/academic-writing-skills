# 规范逐项检查清单（spec-check）联动约定

> 来源：07-08-spec-final-check 任务实现（2026-07-08）。latex-thesis-zh 的 spec-check
> 机制横跨 templates/*.md、check_spec.py、SKILL.md 三处，改任何一处先读本文。

---

## Convention: 逐项检查清单的五列格式与双向锁

**What**：`templates/<school>.md` 中的 `## 逐项检查清单` 段是机器可解析契约——五列表格
`ID | 检查项 | 规范依据 | 检查方式 | 适用`：

- `ID`：`^[A-Z]{2,4}-\d{2,3}$`，文件内唯一且前缀统一（yanshan=YS、thuthesis=THU、
  pkuthss=PKU、generic=GEN）；
- `规范依据`：规范原文章节号（如 `§1.5.3`），必须能在规范原文中找到出处，禁止编造；
- `检查方式`：`script:<checker>`（check_spec.py `CHECKERS` 注册表键）/ `module:<模块>`
  （SKILL.md 路由表模块名）/ `llm` / `manual`；
- `适用`：`通用` / `硕士` / `博士`。

**Why**：`tests/contracts/test_spec_checklists.py` 双向锁定：`script:` 引用必须存在于
CHECKERS，且 CHECKERS 每个 checker 必须被至少一个清单引用（防死代码）；`module:` 必须是
路由表真实模块。**加新 checker 而不在任何清单引用它、或删清单条目导致 checker 失联，
契约测试都会红。**

**How**：

- 新校清单（thuthesis/pkuthss/generic 已落地，2026-07-09）复用既有 checker 键；字数/数量类
  阈值加进 check_spec.py `TEMPLATE_THRESHOLDS[<template>]`——仅在有可追溯官方依据时；无依据则
  该条写 `llm`/`manual`，不得套用别校阈值。
- **阈值参数化边界**（2026-07-09 确立）：checker 行为差异一律走 TEMPLATE_THRESHOLDS 键
  （现有：`title_max`/`title_sub_max`/`kw_range`/`kw_sep`/`abstract`/`body`/`intro`/`bib_min`），
  checker 用 `.get(key, <原硬编码值>)` 读取——**键缺省时行为必须与 yanshan 原行为逐字节一致**；
  部分键缺失（如 pkuthss.master 无 `abstract`）降级 NEEDS-LLM 只报实测数。禁止为单校新增
  checker 函数。官方措辞无法界定判定区间（"600左右"、"≤5 无下限"）**不得发明边界值**，
  落 `llm` 并在检查项文本逐字引用原文。
- **负面证据以测试固化**：研究确认"该校无此规定"的检查器禁入该校清单（先例：清华/北大均无
  正文/绪论/结论字数、文献量、近五年、结论禁引、本章小结条款——七个 checker 由
  `test_check_spec.py::BANNED_NON_YS_METHODS` 断言在 THU/PKU/GEN 清单零出现）。新校接入时
  同样先收集负面证据再固化断言，防止燕山值静默外溢。
- 表格会被全局格式化 hook 重排对齐——解析基于单元格内容（`parse_checklist`），
  重排无害；但改完 SKILL.md 任何表格仍须跑 `tests/contracts/test_skill_contracts.py`。
- 阈值类检查器带 ±10% 缓冲带（落带内报 NEEDS-LLM），因规范多用“一般”措辞；
  时间敏感检查（近五年/近两年）必须用 `--year` 固定基准年，否则断言随墙钟漂移。

**联动清单**（改一处查其余）：

| 改动                            | 必须同步                                                                                                                                                                                                                                         |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 新增/删除 CHECKERS 键           | 至少一个 templates/*.md 清单引用它；`references/modules/spec-check.md` 内建检查器列表                                                                                                                                                            |
| TEMPLATE_THRESHOLDS 增模板/键   | 每个数值有 research 来源行；新键必须带缺省=原行为；yanshan fixture check_spec 输出回归对比；`test_check_spec.py` 补覆盖用例（含缺省回退）                                                                                                        |
| SKILL.md 路由表增删模块         | coverage 测试 `SMOKE_COMMANDS` 必须同步（`test_smoke_commands_cover_router_table` 强制）；`MODULE_COMMANDS` 键**仅当**有清单条目引用 `module:<模块>` 时才加——无引用时加键即死配置（先例：blind-review 只进 SMOKE_COMMANDS 未加 MODULE_COMMANDS） |
| templates/*.md 新增清单段       | `test_spec_checklists.py` 自动纳入（按 `## 逐项检查清单` 枚举，无需改测试）                                                                                                                                                                      |
| fixture thesis-project 内容变化 | `test_check_spec.py` 的天然违规断言（YS-18/24/26 FAIL 等）与 fixture README 埋点 #24                                                                                                                                                             |
