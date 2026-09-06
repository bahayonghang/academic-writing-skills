# 交付说明与证据分层

对应 `implement.md` 步骤 8、本子任务 R5/AC6、父任务 R8/AC12。
汇总日期 2026-09-06。覆盖 `09-06-paper-audit-intake-delivery` 整棵任务树。

档位定义（沿用 `design.md`）：

- **validated advantage** —— 有实跑、实测响应或自动化测试支撑。
- **design advantage** —— 仅由文档结构或静态读码支撑，未实跑。
- **hypothesis** —— 预期效果，本轮未取得任何直接证据。

## 逐条改进

### R1 意图门控（intake-gating）

| 改进 | 档位 | 证据 |
| --- | --- | --- |
| 已指定模式 + 存在旧报告时只陈述不提问 | validated advantage | 独立 subagent 场景 S1 实际响应，规则溯源可核对（`research/behavior-check.md`，intake-gating） |
| 未指定模式时四类检测仍提问 | validated advantage | 场景 S2 实际响应；`tests/skills/paper_audit/test_paper_audit_synthesis.py:106` 的 `Auto-Detection at Intake` 与 `revision_coach_agent` dispatch 两项断言仍通过（本轮 `just ci` 1756 passed） |
| 审稿信构成实质冲突、仍提问 | validated advantage | 场景 S3 实际响应，含"增加审查范围"的显式理由 |
| `--previous-report` 唯一候选时自行解析并陈述 | validated advantage | 场景 S4 实际响应 |
| `--previous-report` 零候选／多候选的停问分支 | design advantage | 仅有文档规则，本轮场景未覆盖 |
| 修订标记检测与长文 polish 阈值的"已指定模式"分支 | design advantage | 仅有文档规则，未实测 |

### R3–R7 交付形态分级（delivery-tiers）

| 改进 | 档位 | 证据 |
| --- | --- | --- |
| `quick-audit`／`gate`／`re-audit` 不落盘 | validated advantage | 四模式落盘行为实跑（`research/write-behavior.md`，delivery-tiers） |
| `polish` 落盘到论文文件旁的 `.polish-state/`，故 `T2` 即被挡 | validated advantage | 实跑推翻了原先"polish 不建工作区"的静态推断；`scripts/audit.py:2509` |
| `deep-review` 必然落盘、`T3` 下不可用 | **design advantage** | 仅静态读码（`audit.py:2704`、`audit.py:1961-1968`、`prepare_review_workspace.py:952`），**未实跑** |
| check 子进程往仓库写 `__pycache__`，`T2`/`T3` 需 `PYTHONDONTWRITEBYTECODE=1` | validated advantage | 决定性实测：运行前无 `__pycache__`、运行后出现于 `scripts/__pycache__`；成因 `scripts/audit.py:681` 启动子进程不带 `-B` |
| `T3` 不建 `review_results`、按名列出不可用脚本 | validated advantage | 行为场景 D1 实际响应，四脚本逐项列出 |
| 已授权落盘时先陈述目标目录、不静默覆盖 | validated advantage | 行为场景 D2、D4 实际响应（给出展开后的绝对路径并要求确认） |
| `T2` 下 polish 不可用并给出替代路径 | validated advantage | 行为场景 D3 实际响应 |
| 三级边界互不重叠、覆盖完整 | design advantage | 文档结构自证，无行为实验 |
| `[Script]`／`[LLM]` provenance 按脚本是否实际运行判定 | validated advantage | 对抗核查项 A 修复后复核；复用既有标记体系，未新造 |
| 12 项对抗发现全部修复 | validated advantage | 四轮独立 subagent 对抗核查，逐项 path:line 复核（`research/write-behavior.md`） |
| R7 不扩大权限 | validated advantage | diff 中 `allowed-tools`／`argument-hint` 未改、未新增依赖、未改 `pyproject.toml`／lockfile（本次 `git diff` 仅涉 15 个 md/json 文件） |

### R8 同步与验收（本子任务）

| 改进 | 档位 | 证据 |
| --- | --- | --- |
| 2 条 trigger query（门控、禁止落盘） | validated advantage | 结构实测 20 条／13 正／7 负，`tests/contracts/test_trigger_evals.py` 全通过 |
| 2 条行为 eval（eval 24 门控、eval 25 `T3` 落盘） | design advantage | 形状与内容契约由 `just ci` 保证；**断言未在真实模型输出上跑过**（仓库内无执行器，见 `research/eval-runner-notes.md`） |
| `evals.json` 未被格式化 hook 压平 | validated advantage | `git diff` 显示 23 行纯新增、既有条目零 diff |
| docs 双语说明页新增"交付级别"节 | validated advantage | en/zh 两页各 18 行新增、逐条对应；`just doc-build` 通过 |
| 跨子任务一致性 | validated advantage | 独立 subagent 只读核对，3 项发现（C1 提问触发条件、C2 `--output` 级别归属、C3 覆盖 flag 错配）已回退到 owning 子任务修正（`research/consistency-check.md`） |
| manifest 散列与镜像一致 | validated advantage | `uv run python docs/scripts/check_resource_sync.py` → `resource contract passed: all resources (271 manifest entries)` |
| 全量 CI 绿 | validated advantage | `just ci` → `1756 passed in 117.28s`，exit 0 |

### 效果类

| 论断 | 档位 |
| --- | --- |
| 减少已指定模式时的复问次数 | hypothesis |
| 减少真实使用中的误落盘 | hypothesis |
| 提升审查效率 | hypothesis |

## 集成验收命令与结果

| 命令 | 结果 |
| --- | --- |
| `just ci` | exit 0，`1756 passed in 117.28s` |
| `uv run python docs/scripts/check_resource_sync.py` | exit 0，`all resources (271 manifest entries)` |
| `just doc-build` | exit 0，`build complete in 14.91s` |

三条均在**最终工作树状态**上复跑过一次（`docs/skills/paper-audit/index.md`
回退表格对齐噪声之后重跑 `doc-build` 与 `check_resource_sync`）。

## missing evidence

本轮未取得、不得当作已验证的项：

1. **真实论文盲评** —— 未在真实论文上跑过任何模式的完整审查，
   也未验证改动对真实审稿质量的影响。父任务 Out of Scope 已明确不作此宣称。
2. **跨平台安装** —— 仅在 win32 / PowerShell 下验证。
   未在 Linux / macOS 上跑过 `just ci` 或落盘行为实测。
3. **独立第三方复核** —— 核查由本会话派出的 subagent 完成，
   非项目外第三方；行为验收全部为文档驱动的响应模拟，非端到端产品运行。
4. **`deep-review` 落盘行为实跑** —— 该模式的落盘判定至今只有静态读码证据。
5. **eval 断言的真实执行** —— `evals.json` 的断言在本仓库内无执行器；
   跑它需要 skill-creator 侧流程与 `ANTHROPIC_API_KEY`，明确不进 `just ci`。
6. **部署副本同步** —— 论文仓库副本
   `thesis/.agents/skills/paper-audit/` 未更新（用户 2026-09-06 选择"仅本仓库"），
   由用户自行重装同步。

## 据实上报的既有问题（未修）

核查发现、早于本次改动、超出任务范围，未在本轮修改：

1. `references/output-layout.md` 工件图缺 `artifacts/data/subsection_index.json`
   与 `artifacts/windows/`（`scripts/prepare_review_workspace.py:691-738` 无条件产出）。
2. `SKILL.md` deep-review Phase 3 写 `committee/consensus.md`，实际是
   `artifacts/committee/consensus.md`。
3. 同源代码缺陷：`scripts/audit.py:1689` 的
   `_register_artifact_if_present(review_dir, "committee/consensus.md")` 路径过时，
   导致 `consensus.md` 永不登记进 checkpoint 的 `generated_files`。
4. `references/workflow-detail.md` 落盘表第三列表头为 `T3`，
   但 `re-audit` 单元格答的是三级；内容正确，列名窄于单元格内容。
5. `evals.json` 的 `id` 序列缺 14（既有断号，本轮未整理）。
