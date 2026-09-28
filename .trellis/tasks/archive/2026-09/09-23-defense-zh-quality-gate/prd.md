# C3 答辩稿质量门与预览

## Goal

为 latex-defense-zh 提供确定性质量门 `check_deck.py`（D-* 码）与 PDF 预览 `render_preview.py`，
并在 `references/quality-gate.md` 写明各码的含义、阈值、严重度与处置方法，供 LLM 修规划与用户验收使用。

## Parent / Dependencies

父任务 `09-23-latex-defense-zh`，对应父 R7、R8，以及 R1 的 scripts 与 quality-gate 参考部分。
前置：C2 已完成并通过其质量门。本子任务读取 C2 的帧标记、清单与规划格式、`scripts/defense_budget.py`、
`tests/skills/latex_defense_zh/conftest.py` 的共享 fixture；不改 C1、C2 文件。发现 C2 缺陷时停下上报。

## Requirements

- C3-R1 `scripts/check_deck.py`：按父 design §3 CLI 与 §4 结果格式输出 D-* 结果；文本与 `--json` 两种输出；
  缺少可选输入（log、plan、notes）时对应码记入 `skipped`，不报错。
- C3-R2 D-* 码集合：D-COMPILE、D-OVERFLOW-V、D-OVERFLOW-H、D-FIG-ALLOW、D-FIG-MISSING、D-FIG-NUMBER、D-FIG-ASPECT、
  D-NUM-SRC、D-EQ-SRC、D-TAB-SRC、D-PLACEHOLDER、D-TOC、D-CHAIN、D-COVERAGE、D-DENSITY、D-BUDGET、D-NOTES、D-META、
  D-STAGE、D-PAPER、D-MARKER。判据、阈值、严重度与优先级见 design §3。
- C3-R3 学术事实保护：清单外图片、清单外数字、改写公式、改写表体、清单外成果分别由 D-FIG-ALLOW、D-NUM-SRC、D-EQ-SRC、
  D-TAB-SRC、D-PAPER 报告；D-NUM-SRC 同时标 NEEDS-LLM，由 LLM 与用户复核该数字能否由论文原文直接支持。
- C3-R4 `scripts/render_preview.py`：PyMuPDF 懒加载；逐页 PNG 与带页码的总览图；缺 PyMuPDF 时给出安装提示并退出 3。
- C3-R5 `references/quality-gate.md`：码表（含义、判据、阈值、严重度、优先级、处置）、阈值未标定说明、修复循环规则
  （≤3 轮，按 C1 content-rules 的溢出处置顺序）、NEEDS-LLM 项的人工复核方法、预览目视清单；同步双语资源页与 manifest。
- C3-R6 只读：check 与 preview 不改答辩稿、规划、清单与论文仓库；preview 只写 `--out` 目录下自有的 PNG 文件。

## Acceptance Criteria

- [ ] AC1: 每个 D-* 码至少一个正例（基线稿不报该码）与一个反例（注入缺陷后报该码，严重度与优先级符合 design §3）。
- [ ] AC2: 父 AC8 三个反例（论文外数字、论文外图片、改写公式）分别报 D-NUM-SRC、D-FIG-ALLOW、D-EQ-SRC。
- [ ] AC3: 文本行格式与 `--json` 字段稳定（字段集合断言）；有 Critical/Major 时退出 1，否则 0；输入文件缺失退出 2。
- [ ] AC4: 无 log 时 D-COMPILE、D-OVERFLOW-V、D-OVERFLOW-H 出现在 `skipped`；无 notes.md 时报 D-NOTES（Major）。
- [ ] AC5: preview 在 PyMuPDF 缺失时（monkeypatch 导入失败）退出 3，stderr 含安装命令；PyMuPDF 可用时对合成 PDF 生成
  逐页 PNG 与总览图，旧的多余 `page-NNN.png` 被清除；不可用时该用例 skip。
- [ ] AC6: check 与 preview 运行前后，基线稿目录与清单文件 SHA-256 不变（preview 输出目录除外）。
- [ ] AC7: `check_resource_sync.py --skill latex-defense-zh` 通过；`just ci` 通过。
