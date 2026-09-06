# 跨子任务一致性核对

核对日期 2026-09-06。由独立 subagent 只读核对，改动作者不自评。

## 范围

| 子任务 | 被核对文件 |
| --- | --- |
| intake-gating | `references/MODE_GUIDE.md`（`Input Resolution`、`Auto-Detection at Intake`） |
| delivery-tiers | `SKILL.md`（`Delivery Boundary`、deep-review Phase 1）、`references/workflow-detail.md`、`references/output-layout.md` |
| verify | `docs/skills/paper-audit/index.md`、`docs/zh/skills/paper-audit/index.md` |

只核对三类问题：同一概念两处定义不同；同一动作两处归属不同级别；
en/zh 两页事实不一致。不报风格偏好，不报三个子任务未触碰的段落。

## 发现与处置

共 3 项，全部为本次改动引入或本次改动应当覆盖的项，均已修正。

### C1 — 同一概念两处定义不同（提问触发条件）

`MODE_GUIDE.md` 规定用户已给定模式时"Do not offer a mode choice"，
唯一例外是实质冲突，而实质冲突当时只定义了 Scope 与 Result 两个触发条件。
`workflow-detail.md` 同时要求 `deep-review` 在 `T3` 下"offer `quick-audit` or `gate`"。
用户同时给定 `deep-review` 与 `T3` 时两条规则相撞：
交付级别冲突既不改范围也不改结果，按 `MODE_GUIDE.md` 原文属于被禁止的提问。

处置：回退到 intake-gating 的 `MODE_GUIDE.md`，在实质冲突定义中增加第三个触发条件
**Delivery level**，指向 `SKILL.md` 的 `Delivery Boundary`。zh 镜像同步翻译。

### C2 — 同一动作两处归属不同级别（`--output` / `-o`）

`SKILL.md` 与 `workflow-detail.md` 都把 `--output` / `-o` 的禁止限定在 `T3`，
`T2` 允许写到两个仓库之外的用户指定目录。
两份 index.md 写成"Avoid both at `T2` and `T3`"／"`T2` 与 `T3` 下两者都要避开"，
把 `T2` 的允许动作误禁。成因是把 `--output` 与 `PYTHONDONTWRITEBYTECODE`
两条不同级别的规则并进了同一个"两者都要避开"从句。

处置：在 verify 子任务内改两份 index.md，把两条规则拆开分别限定级别。
同时补上 `T2` 下 `polish` 与 `deep-review` 的限定条件——
两页原本只给出"低于 `T3` 即可用"的印象，读者据此会误跑 all-in-one 路径。

### C3 — 覆盖确认 flag 与命令错配（既有缺陷，本次修正）

`SKILL.md` deep-review Phase 1 把 `--overwrite` 与 `--overwrite-workspace`
并列挂在 `prepare_review_workspace.py` 步骤下。实际归属：
`--overwrite` 定义在 `scripts/prepare_review_workspace.py:956`，
`--overwrite-workspace` 定义在 `scripts/audit.py:3487`。
`prepare_review_workspace.py` 没有 `--overwrite-workspace` 这个 flag。
`workflow-detail.md` 与 `output-layout.md` 的表述正确，与代码一致。

该错配在本次改动之前即存在，但落在 delivery-tiers 已改写的同一行上，
故按同一行的事实错误处理：明写 `--overwrite` 属本步骤，
`--overwrite-workspace` 属 all-in-one 的 `audit.py --mode deep-review` 路径。

## 核对通过项

- **en/zh 事实一致**：`Delivery Levels` 与 `交付级别` 逐条对应，
  三行表格、级别触发语、逐模式可用性、模式无关写入、`T3` 两组上报规则、
  禁止冒充脚本检查、以及指向 `Delivery Boundary` 的出口，两页齐全，无一方多出或缺失。
- **逐模式级别归属**：`SKILL.md`、`workflow-detail.md`、两份 index.md 四处一致。
- **实测来源声明**：`SKILL.md` 与 `workflow-detail.md` 给出相同日期 2026-09-06、
  相同的四个实测模式、相同的"deep-review 一行来自读码未实跑"声明。
- **`PYTHONDONTWRITEBYTECODE` 条款**：四处规则与级别范围一致，
  `SKILL.md` 与 `workflow-detail.md` 给出相同成因（`audit.py` 启动子进程不带 `-B`）。
- **两组拆分**：`SKILL.md` 声明规则并指向 `workflow-detail.md` 的两份清单；
  两页 index.md 与之一致；`quick-audit`/`gate` 在 `T3` 下仍产出真实 `[Script]` 的
  后续规则四处一致。

## 观察项（未改）

- `workflow-detail.md` 落盘表第三列表头是 `T3`，但 `re-audit` 单元格答的是三级
  （"`T1` plain; `T2`/`T3` need `--no-trajectory`"）。内容与 `SKILL.md` 一致，
  只是列名窄于单元格内容。不属三类问题，未改。
- `SKILL.md` 的 `T3` 触发语有两条（`"don't leave any files"`、`"conversation only"`），
  两页 index.md 只列第一条。两语言等量省略，不构成 en/zh 不一致。
