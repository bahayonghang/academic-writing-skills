# 整合模板知识源并更新 thuthesis/pkuthss 事实

> 父任务：`06-12-latex-thesis-zh-optimization`（见其 prd.md §1 调研 2/3、§2 发现 F14/F15/F18/F20）
> 优先级：P1

## Goal

模板知识收敛为**单一权威来源**并更新到 2026 年现实：消除 templates/ 与
university-templates/ 的逐字节重复，修正 thuthesis 过时事实，标注 pkuthss 维护状态，
并把"校级排版规定"从国标文档中迁出归位。

## Requirements

### R1 知识源收敛（F14）

- `templates/{generic,thuthesis,pkuthss}.md` 与
  `references/university-templates/{generic,tsinghua,pku}.md` 三对文件当前逐字节相同。
  保留 `templates/` 为唯一权威（SKILL.md Reference Map 已宣布 university-templates 为
  legacy），university-templates 目录处理方式在 design 阶段定夺：
  直接删除并改写脚本引用（倾向），或保留 1 行重定向占位。
- `detect_template.py` 的 `TEMPLATE_REFERENCE_FILES` 与 `_reference_dir()` 改指
  `templates/`；补 ustcthesis/fduthesis 的映射说明（暂落 generic）。
- `map_structure.py:22-48` 硬编码的 TEMPLATES 字典（figure_format 等事实）与
  templates/*.md 二选一：事实只在一处定义（建议脚本仅保留 documentclass 检测
  pattern，展示性事实从 md 读取或删除）。
- `yanshan.md`（孤儿，20 行）：并入 templates/ 体系并接入 detect_template 映射，
  或确认无用后删除（git 历史可追溯）。

### R2 事实更新（F15，基于 2026-06 调研）

- `templates/thuthesis.md`：
  - BibTeX 样式改为 `thuthesis-numeric.bst` / `thuthesis-author-year.bst`
    （natbib `\usepackage[sort]{natbib}` + `\bibliographystyle{thuthesis-numeric}`），
    删除 `thubib.bst`（v4 时代残留）；
  - 标注现行版本基线 v7.6.0（2025-03-28，含本科生 2025 规范更新）与
    "从 CTAN/GitHub releases 获取最新版"的指引。
- `templates/pkuthss.md`：
  - 标注原仓库已归档（Gitea 2024-08 archived，现迁 codeberg.org/CasperVector/pkuthss，
    最后实质更新 2024-04）；
  - 提示社区活跃分支（如 iofu728 Overleaf 版符合 2022 研究生格式审核）与
    "以学校最新格式审核要求为准"的注意事项。
- 两文件标注"事实核查日期：2026-06"，便于后续保鲜。

### R3 校级排版内容归位（F18 迁移部分）

- 接收 zh-gb7714-validation 任务从 `gb-standard.md` 第五、六节迁出的
  图表编号/标题字体内容：落入 `templates/generic.md`（标注"常见校级约定，
  非国标强制，以本校规范为准"），thuthesis/pkuthss 文件中写各自模板的实际行为。
- `references/modules/format.md` 同步改链，不再复读"黑体三号"表格为普适规则。

## Constraints

- 删除/移动文件时全仓 grep 入链（SKILL.md、modules/*.md、detect_template.py、
  docs/ 站点），不得产生死链；docs 站点若引用旧路径需同步。
- 模板事实必须有来源可查（CTAN/官方仓库），禁止凭印象编写具体版本号或命令。
- 不 bump version，只改 last_updated。

## Acceptance Criteria

- [ ] 全仓库中 thuthesis bst 名称、figure_format 等同一事实只有一处权威定义。
- [ ] `detect_template.py main.tex` 对 thuthesis fixture 输出的 reference 路径
      指向 templates/，key_requirements 非空。
- [ ] 仓库内不再存在逐字节相同的模板文件对；无死链（grep 验证）。
- [ ] thubib.bst 字样从仓库消失；pkuthss 归档状态与 thuthesis v7.6.0 基线可见。
- [ ] `just ci` 全绿。
