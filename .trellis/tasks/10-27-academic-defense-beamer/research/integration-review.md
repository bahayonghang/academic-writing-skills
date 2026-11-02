# 集成复核（2026-11-01）

子任务提交：
- `10-27-defense-rename`：`051ffd1`
- `10-27-defense-beamer-notes`：`195037d`
- `10-27-defense-typst-backend`：`70118f1`

| 跨子任务验收 | 结果 |
| --- | --- |
| 旧名清理 | 通过：`rg` 只在两处迁移说明（README / README_CN「旧安装目录可删除」）命中，属允许例外 |
| `just ci` + 资源同步 | 通过：2933 passed, 25 skipped；resource contract 308 项通过 |
| 同一 fixture 双后端构建 + 备注 PDF 校验 | 通过：`DEFENSE_COMPILE=1 DEFENSE_TYPST_COMPILE=1 uv run --with pymupdf pytest tests/skills/academic_defense_beamer` 256 passed, 0 skipped。Beamer（XeLaTeX，TeX Live 2025）投屏版 + second-screen 备注版通过 D-NOTES-PDF；Touying 54 帧，投屏版 54 页，备注版 108 页 `N` / `notes:N` 交替，D-NOTES-PDF 零结果 |
| FerroStage 人工核对 | **UNVERIFIED**：两份备注版均未在 FerroStage 实机截图 |
| SKILL.md / 双语页 / README / docs 一致 | 通过（子任务 3 trellis-check 复核）；SKILL.md 正文 153 → 164 行，细节在 `references/` |
| 学术事实保护 | 通过：图按字节复制、公式只去 `\label` 与改写宏定义语法、表体只取自 `tabular_source`；Touying 保真规则写入 `references/quality-gate.md` 与 `touying-backend.md` |

决策更新：D3 中「0.2.0 尚未上架 Typst Universe」已过时——2026-11-01 用户确认 0.2.0 已上架；默认 `@preview/simply-ysu-touying:0.2.0` 不变，`@local` 降为离线 / 改主题时的备选。

遗留：
- FerroStage 实机核对（人工）。
- 仓库 fixture 不含图片文件，直接以 Touying 构建会因缺图退出 2；测试用自建图片覆盖。
- 主题 0.2.0 小问题：溢出续页页脚计数不连续（`6/11, 6/11, 7/11, 8/11` 后跳到 `10/11`），可反馈主题仓库。
