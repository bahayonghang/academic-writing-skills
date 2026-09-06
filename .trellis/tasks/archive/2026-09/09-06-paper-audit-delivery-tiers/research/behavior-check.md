# 交付形态行为验收与对抗核查记录

验收日期 2026-09-06。

## 方法

四轮独立 subagent 核查，改动作者不自评。
第一轮做行为验收（D1-D4 场景 + 自审四问）；
第二至四轮做对抗式事实核查，把文档claim 逐条对照 `scripts/` 源码验证，
要求给出 path:line 并明确 VERIFIED / WRONG / UNSUPPORTED。

## 行为验收（第一轮）

| 场景 | 输入 | 期望 | 实际 | 判定 |
| --- | --- | --- | --- | --- |
| D1 | "审查论文，但不要在磁盘上留下任何文件" | 不建 review_results，列缺失证据 | 明确不建 review_results / .polish-state / 报告文件；四脚本逐项列出 | 通过 |
| D2 | "deep-review thesis.tex"，无约束 | T1，写前陈述目标目录 | 给出展开后的绝对路径并要求确认 | 通过 |
| D3 | "polish，但别写进仓库" | T2 下 polish 不可用 | 判定不可用并给出三条替代路径 | 通过 |
| D4 | "gate，报告存到仓库外" | 陈述解析后的目标目录 | 给出绝对目录与文件名，要求确认后才写 | 通过 |

## 对抗核查发现与处置

第一轮 subagent 在完成 D1-D4 后主动指出一处矛盾，第二至四轮共发现 12 项。
全部为本次改动引入或本次改动应当覆盖的项，均已修复并重新核查通过。

| 编号 | 问题 | 处置 |
| --- | --- | --- |
| A | "T3 下一切发现都是 `[LLM]`" 与事实冲突：`quick-audit`/`gate` 的检查器确实运行 | 改为按脚本是否实际运行判定 provenance |
| F1 | T2 两步法把 `--output-dir` 值当作 `--review-dir`，而工作区是其 slug 子目录 | 改为传 `WORKSPACE:` 打印出的路径 |
| F2 | 未说明 `--output` / `-o` 在所有模式下都写文件 | 补入模式无关的写入说明 |
| F3 | `re-audit` 记为不落盘，但 `diff_review_issues.py` 会写 `revision_trajectory.md` | 补条件与 `--no-trajectory` 规避 |
| F4 | 两个渲染器被当作"检查"标 `missing evidence`，误导证据缺失 | 拆成"丢失证据"与"仅未产出"两组 |
| N1 | `SKILL.md` 仍要求把全部不可用脚本标 `missing evidence`，与拆组矛盾 | 同步拆组表述 |
| N2 | `output-layout.md` 把 `--output-dir` 父目录与工作区混为一谈 | 说明覆盖保护判定的是工作区 |
| N3 | "the first four" 无先行词；`workflow-detail.md` 声称实测覆盖全部模式 | 点名四个实测模式，声明 deep-review 未实测 |
| N4 | 轨迹写出被写成无条件 | 补"至少一个数值型 round score"条件 |
| N5 | `re-audit` 标为三级全可用，缺 T2 限定 | 改为 T1 直接可用，T2/T3 需 `--no-trajectory` |
| P1 | "Name every script" 与两组清单不完整（缺 workspace 准备脚本） | 补 `prepare_review_workspace.py`、`build_claim_map.py` |
| P2 | check 子进程往仓库写 `__pycache__` | 实测确认后补 `PYTHONDONTWRITEBYTECODE=1` 要求 |

## P2 的实测

`scripts/audit.py:681` 以 `[sys.executable, script, file]` 启动子进程，不带 `-B`；
父进程的 `-B` 不传递，`uv run` 也不设置 `PYTHONDONTWRITEBYTECODE`（实测该变量为 `None`）。

决定性实测：按同样方式单独运行 `pre_submission_check.py`，
运行前 `academic-writing-skills/` 下无 `__pycache__`，
运行后出现 `academic-writing-skills/paper-audit/scripts/__pycache__`。
测试产生的目录已删除，验收后复查为空。

该写入落在本仓库内，因此 `T2` 与 `T3` 均需显式设置 `PYTHONDONTWRITEBYTECODE=1`。
仓库自身的测试也这么做（`tests/conftest.py:18`、`tests/contracts/test_skill_contracts.py:457`）。

## 未修复的既有问题（超出本任务范围，据实上报）

以下三项由核查发现，属于本次改动之前就存在的问题，未在本任务中修改：

1. `academic-writing-skills/paper-audit/references/output-layout.md` 的工件图不完整，
   缺 `artifacts/data/subsection_index.json` 与 `artifacts/windows/`
   （`scripts/prepare_review_workspace.py:691-738` 无条件产出）。
2. `academic-writing-skills/paper-audit/SKILL.md` deep-review Phase 3 写
   `committee/consensus.md`，实际路径是 `artifacts/committee/consensus.md`。
3. 与第 2 项同源的代码缺陷：`scripts/audit.py:1689`
   `_register_artifact_if_present(review_dir, "committee/consensus.md")`
   路径同样过时，导致 `consensus.md` 永远不会登记进 checkpoint 的 `generated_files`。

## 证据档位

- validated advantage：四个模式的落盘行为、`__pycache__` 写入、D1-D4 行为响应、
  12 项对抗发现的修复后复核、`just ci` 相关测试与资源同步检查。
- design advantage：`deep-review` 的落盘判定（仅静态证据，未实跑）、
  三级边界的完整性与互斥性。
- hypothesis：本改动能减少真实使用中的误落盘（未在真实论文上验证）。

missing evidence：真实论文场景、跨平台安装、独立第三方复核，本轮均未运行。
