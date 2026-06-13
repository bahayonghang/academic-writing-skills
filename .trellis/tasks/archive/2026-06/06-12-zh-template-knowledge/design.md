# Design: 模板知识单源化 + 事实更新

## R1 知识源收敛

- 删除 `references/university-templates/`（与 templates/ 三对逐字节重复）；
  `yanshan.md` 内容有规范获取指引价值 → 迁为 `templates/yanshan.md`
  （无公开 documentclass，文件头注明为规范指引而非 LaTeX 模板事实）。
- `detect_template.py`：`_reference_dir()` → `templates/`；映射改
  thuthesis.md/pkuthss.md/generic.md；ustcthesis/fduthesis 注释说明暂落 generic。
- `map_structure.py` TEMPLATES 删除 `figure_format` 字段（事实单源于
  templates/\*.md）；detect_template 输出相应去掉 Figure format 行。

## R2 事实更新（事实核查日期 2026-06）

- thuthesis.md：BibTeX 样式 `thuthesis-numeric.bst`/`thuthesis-author-year.bst`
  （natbib），删除 thubib.bst；版本基线 v7.6.0（2025-03-28）+ CTAN 指引。
- pkuthss.md：原仓库 Gitea 2024-08 归档 → codeberg.org/CasperVector/pkuthss
  （最后实质更新 2024-04）；社区分支提示；以学校最新格式审核为准。

## 测试与契约同步

- `test_skill_contracts.REFERENCE_LAYOUTS` 移除 `university-templates`。
- `test_venue_templates_layout`：byte-for-byte 测试替换为单源断言
  （university-templates 不存在 + thubib 不再出现 + thuthesis-numeric 存在）。
- SKILL.md Reference Map：删 legacy 行，templates/ 行加 yanshan.md。

## docs 同步

- docs 镜像 `resources/university-templates/` → `resources/templates/`
  （generic/thuthesis/pkuthss/yanshan）；config.ts 侧边栏改链；
  gb-standard.md / format.md 镜像中的 `../university-templates/...` 链接改
  `../templates/...` 并重新同步。
