# C2 rebuttal response：定位、渲染与 R-* 质量门

## Goal

新增 `scripts/rebuttal_build.py` 与 `scripts/rebuttal_check.py`。build 从台账渲染修改计划与 responses（纯文本等价 Markdown），
用修改后 aux 解析修改位置的编号与页码；check 按父 `design.md` §7 输出 R-* 结果。契约见父 `design.md` §3–§8、§10。

前置：C1 已完成，`rebuttal_common.py`、`rebuttal_state.json` 与 `concerns.yaml` 格式已固定。

## Requirements

- B1 台账校验：`schema` 字段、条目必填字段与枚举值（父 design §4）；不合法时列出全部错误并退出码 2。`--plan-only` 只要求 `action`、`plan`、`owner`。
- B2 `--plan-only`：只写 `workspace/revision_plan.md`（父 design §5 末条）；不写 responses。
- B3 完整渲染：写 `responses/review-result.md`、`responses/response-all.md`、`responses/response-R<n>.md`、`workspace/anchors.json`、
  `workspace/revision_plan.md`；结构按父 design §5；只渲染 `status=done` 的条目，其余条目渲染为「〔待填写〕」并由 check 报告。
- B4 位置解析：`label` 查当前 aux 得编号与页码；与 `base_number` 不同时写原编号与新编号；文献用 `\bibcite` 序号；无 `--thesis` 时只写台账给出的文字位置。
- B5 手改保护：responses 当前 sha256 与 `rebuttal_state.json.rendered` 不同时退出码 4，`--force` 覆盖；渲染后更新 `rendered`。
- B6 check：实现父 design §7 全部 16 个码；依赖论文的码在无 `--thesis` 或非 git 时写入 `skipped`；结果写 `workspace/check.json`。
- B7 只读：不写评阅书目录与论文仓库；git 只用 `diff --name-only`、`ls-files`、`rev-parse`。
- B8 R-NUM-SRC 的论文可见文本：用 `tex_loader` 加载 include 树，去掉注释与命令后取数字集合（与 `check_deck.py` 的 D-NUM-SRC 相同口径，复用其函数时不改 `check_deck.py`）。

## Acceptance Criteria

- [ ] 两个脚本 `--help` 列出父 design §8 的全部选项。
- [ ] 干净 fixture（全部 `done`、证据齐全、修改后 aux 新于 tex）：build 写出 5 类文件；check Critical 与 Major 为 0，退出码 0。
- [ ] responses 每条含「意见 / 回复 / 修改位置」；编号变化锚点写「原图2-1，现图2-2（第13页）」形式；页码来自修改后 aux。
- [ ] 每个 R-* 码一个负例测试，断言码名、严重度与 concern 编号。
- [ ] R-COMMIT 路径过滤：仓库其他文件有改动而声明文件无改动时报 Critical；`responses/`、`workspace/`、评阅书目录下的改动不计入。
- [ ] 手改 responses 后 build 退出码 4；`--force` 后覆盖并更新 `rendered`。
- [ ] responses 原文与「去 Markdown 渲染」后的文本逐行一致（测试内实现一个最小渲染：去行首标记与行内强调后比较，二者应相同）。
- [ ] `--plan-only` 在条目只有 `action`/`plan`/`owner` 时成功，且不创建 responses 文件。
- [ ] 论文副本与评阅书目录 sha256 集合运行前后一致。
- [ ] `rtk proxy uv run --extra dev python -m pytest -q tests/skills/latex_defense_zh`、`rtk proxy just lint`、`rtk proxy just typecheck` 通过。
