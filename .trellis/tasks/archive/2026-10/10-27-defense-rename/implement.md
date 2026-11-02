# 执行计划：改名迁移

前置：无。在 `dev` 分支工作，工作区干净。

## 步骤

1. 基线：`just ci` 记录当前结果；对 `evals/fixtures/mini-thesis` 跑 extract → plan → build（不编译），保存 `defense.tex` 到 scratchpad 作对照。
2. `git mv academic-writing-skills/latex-defense-zh academic-writing-skills/academic-defense-beamer`。
3. `git mv tests/skills/latex_defense_zh tests/skills/academic_defense_beamer`。
4. `git mv docs/skills/latex-defense-zh docs/skills/academic-defense-beamer`；`git mv docs/zh/skills/latex-defense-zh docs/zh/skills/academic-defense-beamer`。
5. 按 design.md 文件处理表逐文件替换（标识符 → 环境变量 → 展示名）。替换后执行：
   `rg -n "latex-defense-zh|latex_defense_zh|DEFENSE_ZH_COMPILE" --glob "!.trellis/tasks/**" --glob "!.trellis/workspace/**"`，逐条确认剩余命中只在迁移说明。
6. 在 `docs/installation.md` 与 `docs/zh/installation.md` 加旧安装目录清理说明。
7. `uv run python docs/scripts/check_resource_sync.py --write-manifest`，再不带参数运行确认通过。
8. 验证：
   ```bash
   just ci
   uv run python docs/scripts/check_resource_sync.py
   just doc-build
   ```
   有 XeLaTeX 时再跑 `DEFENSE_COMPILE=1 uv run pytest tests/skills/academic_defense_beamer`（PowerShell：`$env:DEFENSE_COMPILE='1'`）。
9. 重跑步骤 1 的 build，与对照 `defense.tex` 比较，差异只允许在头注释。
10. trellis-check；提交：`refactor(academic-defense-beamer): 将 latex-defense-zh 更名为 academic-defense-beamer`。

## 回滚点

- 步骤 2–7 任一步失败：`git reset --hard HEAD` 回到基线（工作区起点干净）。
- 提交后：`git revert`。

## 审查门

- 改名提交中不得出现脚本逻辑变化：`git diff --stat -M` 中脚本文件应显示为 rename 且相似度 ≥ 98%。
