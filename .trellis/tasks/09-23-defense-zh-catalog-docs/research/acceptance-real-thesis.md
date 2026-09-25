# C4 验收证据（含 AC11 状态）

记录日期：2026-09-25。宿主：Claude Code（云端会话容器）。本文件不记录论文题目、姓名、正文、数字与本机路径。

## AC11 真实论文验收：PENDING

本会话运行在云端容器中，容器内没有用户的真实论文仓库，用户也未在会话中给出论文路径；按 design §5，不能以本仓库或 fixture 代替。
AC11 保持 **PENDING**，需要用户在本机（或把论文仓库接入会话后）按父 `implement.md`「AC11 流程」执行一次，
并把结果补记到本文件。其他四个宿主（Codex、Grok Build、Kimi Code、OMP）运行状态为 **UNVERIFIED**。

## 替代演练：合成论文 + LLM 真实填写（非 AC11 证据）

为在交付前暴露流程问题，在会话 scratchpad 中对 C2 fixture（合成论文）完整走了一遍技能流程，规划由 LLM 按
`references/content-rules.md` 逐帧填写（不是 `fill_plan` 的合成占位文本）。输出目录类型：会话 scratchpad。

| 步骤 | 命令（`$SKILL_DIR`、`$WORK` 同 C2 证据） | 退出码 | 结果 |
| ---- | ---- | ------ | ---- |
| 提取 | `extract_thesis.py --thesis $WORK/mini-thesis --out $WORK/inventory.json` | 0 | 同 C3 证据 |
| 规划 | `plan_deck.py … --minutes 30 --stage defense --theme yanshan` | 0 | 帧数 45，内容页数 36，占位符 226 |
| LLM 填写 + 串读 | `plan_deck.py --plan $WORK/slide_plan.yaml --outline` | 0 | 占位符 0；结论句串读复述论文主线 |
| 构建（第 1 轮） | `build_deck.py … --out $WORK/deck --compile` | 0 | 帧数 45；PDF 45 页 |
| 检查（第 1 轮） | `check_deck.py … --plan $WORK/slide_plan.yaml` | 0 | Critical 0，Major 0，Minor 36（全部 D-NOTES：讲稿偏短） |
| 修复第 2 轮 | 补写讲稿后 `build_deck.py --force --compile`；`check_deck.py` | 0 / 0 | Minor 16（D-NOTES） |
| 修复第 3 轮 | 补写讲稿后重建与检查 | 0 / 1 | **Critical 1（D-COMPILE：PDF 早于 tex）**——见缺陷 2 |
| 修复缺陷后复查 | 重建与检查 | 0 / 0 | Critical 0，Major 0，Minor 0，Info 0；`Overfull` 0 |
| 预览 | `render_preview.py --pdf $WORK/deck/defense.pdf --out $WORK/deck/preview` | 0 | 45 张逐页 PNG 与总览图 |

目视总览图时发现缺陷 1（第 17 页子图网格空白）。修复后复查：全部 45 页版面正常，章前目录高亮当前章，三子图网格显示，论文框、创新点卡片、展望与成果页正确。

另用同一规划注入三类缺陷（论文外百分比、过密要点、8 条要点的 figure-bullets）生成 `examples/fix-after-check.md` 中的真实输出：
check 退出 1，D-NUM-SRC Major 1、D-OVERFLOW-V Major 1、D-DENSITY Minor 3；按示例修复后一轮归零。

## 演练发现并已修复的缺陷

1. **figure-grid 子图不显示**：帧没有小节条时，`templates/jinja/frames/figure-grid.tex.j2` 的 `{\centering …}` 紧跟
   `\begin{frame}{<title>}`，被 Beamer 当作帧副标题吞掉。改为 `\begingroup … \endgroup`；同步 `slide-layouts.md` 骨架与说明（含双语页）、
   `demo-deck.tex`；新增 `test_no_brace_group_follows_frame_title`（修复前失败）。
2. **只改讲稿后误报 D-COMPILE Critical**：`build_deck.py --force` 重写内容相同的 `defense.tex`，latexmk 按内容哈希跳过重编，
   PDF 的 mtime 早于答辩稿。改为内容未变的自有文件不重写；`plan-schema.md`（含双语页）写明；新增
   `test_force_keeps_unchanged_files`（修复前失败）。
3. **文字字段写 `$…$` 原样显示为 `\$G\$`**：属于规划写法问题，质量门不报。在 `content-rules.md`（含双语页）写明文字字段不写 LaTeX 或行内数学。
4. **测试隔离**：PyMuPDF 首次导入绑定 `sys.stdout`；首次导入发生在 `capsys` 用例内时，后续编译用例写入已关闭的流。`conftest.py` 在收集阶段预导入。
5. **docs 清单排序依赖平台**：`check_resource_sync.py` 用 `sorted(Path)`，Windows 不区分大小写、Linux 区分，Linux 重建清单会整体重排。
   改为按路径分段小写排序（与既有清单一致，Linux 重建零差异）；新增 `test_manifest_order_is_platform_independent`。

## 质量门

| 命令 | 结果 |
| ---- | ---- |
| `uv run --extra dev python -m pytest -q tests/contracts` | 326 passed |
| `DEFENSE_ZH_COMPILE=1 uv run --extra dev python -m pytest -q tests/skills/latex_defense_zh` | 152 passed |
| `uv run python docs/scripts/check_resource_sync.py` | resource contract passed（301 条） |
| `just skills-install --list` | 列出 8 个技能 |
| `just ci` | 通过：2515 passed，8 skipped；pyright 0 errors |
| `just doc-build` | build complete |

pyright 警告数在本容器为 104（基线 86）。增量全部来自容器 venv 装了 PyMuPDF 后 paper-audit `pdf_parser.py`、`visual_check.py` 与
`render_preview.py` 的第三方类型推断；未装 PyMuPDF 的 CI 环境不受影响，本任务未新增代码警告。

## 验收对照

| AC | 状态 | 证据 |
| --- | --- | --- |
| AC1 | PASS | 五个契约测试文件覆盖 latex-defense-zh，含路由命令 `--help` 核对与命令卫生 |
| AC2 | PASS | `just skills-install --list` 8 个技能 |
| AC3 | PASS | 完整资源检查与 `just doc-build` 通过；侧栏含「中文答辩稿 (latex-defense-zh)」组 |
| AC4 | PASS | `just ci` 通过 |
| AC5 | PASS | 技能目录、docs 新页、spec 与测试 grep 无本机绝对路径；技能目录无图片文件；内容均为合成 fixture |
| AC6 | PENDING | 见上文 AC11 |
| AC7 | PASS（有说明） | 除 design §2 与技能目录外，另改 `docs/scripts/check_resource_sync.py`、C2/C3 文件（`build_deck.py`、`figure-grid.tex.j2`、`demo-deck.tex`、三份 references 及其双语页）与 `tests/skills/latex_defense_zh/conftest.py`、`test_defense_build.py`，均为上文缺陷修复 |
