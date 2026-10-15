# C1 rebuttal intake：评阅书提取与意见台账

## Goal

新增 `scripts/rebuttal_intake.py` 与共享模块 `scripts/rebuttal_common.py`：给定评阅书目录，在其同级创建 `responses/` 与 `workspace/`，
把评阅书归一化为 `workspace/reviews/R<n>.md`，解析评分，生成 `workspace/concerns.yaml` 台账骨架与 `workspace/rebuttal_state.json`。
契约见父任务 `design.md` §1–§4、§6、§8–§10。

## Requirements

- I1 目录：`$ROOT` 默认为 `--reviews` 的父目录，`--root` 覆盖；创建 `responses/`、`workspace/`、`workspace/reviews/`。
  评阅书目录与 `responses/`、`workspace/` 相同或嵌套时退出码 2。
- I2 输入：`.pdf`（PyMuPDF 懒加载，缺失时退出码 3）、`.txt`、`.md`；`.docx`/`.doc`/图片退出码 2；目录中无可用文件退出码 2。
  其他扩展名忽略并列入 warnings。
- I3 归一化：父 design §9 第 1–6 条。
- I4 评分：解析总分、总体评价等级（A–E）、是否同意答辩；解析失败字段为 null 并 warning。
- I5 台账骨架：每条编号意见一条 `R<n>-<item>`（父 design §4 规则第 1 条）；`reviewers[].praise` 写入学术评语全文；
  每条意见的 `anchors` 由 `find_anchors` 检出，给出 `--thesis` 时用基线 aux 与 `\bibcite` 填 `label`、`base_number`、`base_page`。
- I6 状态文件：父 design §3 表格全部字段；`base_commit` 为 `git rev-parse HEAD`（非 git 仓库为 null 并 warning），`--base-commit` 覆盖。
- I7 不覆盖：`workspace/reviews/` 已存在且无 `--force` 时退出码 4；`concerns.yaml` 已存在时永不覆盖，并列出台账中缺少的条号。
- I8 只读：不写评阅书目录与论文仓库；不修改 `tex_loader.py`、`extract_thesis.py` 与 `mini-thesis/` fixture。
- I9 `--json` 输出父 design §8 所列字段；非 JSON 模式输出中文摘要（评阅人数、各自等级与条数、锚点数、warnings）。

## Acceptance Criteria

- [ ] `rebuttal_intake.py --help` 列出父 design §8 的全部选项，退出码 0。
- [ ] txt fixture：水印与页脚行全部删除；跨行意见合并为一条；条数、等级、总分、同意答辩正确。
- [ ] PDF（测试中由 PyMuPDF 生成，三页、每页重复水印、`1、` 编号）：同上；无 PyMuPDF 时该测试 skip。
- [ ] 锚点：`图2-1`、`式(2-1)`、`第3章至第5章`、`2.3节`、`文献[3]`、`文献[1,2]` 被识别；在 mini-thesis 副本上 `图2-1` 映射到 `fig:c2-profile`、页码 12。
- [ ] 退出码：缺目录 2、`.docx` 2、嵌套目录 2、模拟缺 PyMuPDF 3、重复运行无 `--force` 4；`--force` 后 `concerns.yaml` 内容不变。
- [ ] 无 `--thesis`：台账生成，锚点 `label` 为 null，退出码 0。
- [ ] 只读：评阅书目录与论文副本运行前后 sha256 集合一致。
- [ ] `rtk proxy uv run --extra dev python -m pytest -q tests/skills/latex_defense_zh` 与 `rtk proxy just lint`、`rtk proxy just typecheck` 通过。
