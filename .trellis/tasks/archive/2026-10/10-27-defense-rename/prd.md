# 更名 latex-defense-zh → academic-defense-beamer 并迁移全仓引用

父任务：`.trellis/tasks/10-27-academic-defense-beamer`（需求总集与决策 D1、D2 见其 prd.md）。
波及清单见父任务 `research/source-analysis.md` 第 1 节。

## 目标

技能目录、技能名与全部引用改为 `academic-defense-beamer`，**行为不变**：五个模块的 CLI、参数、退出码、产物、D-* 码与输出格式与改名前逐字一致。
本子任务不引入 Typst 或备注 PDF 能力，只为子任务 2、3 腾出正确的名称与路径。

## 需求

1. `git mv academic-writing-skills/latex-defense-zh academic-writing-skills/academic-defense-beamer`，保留历史。
2. `SKILL.md` frontmatter `name: academic-defense-beamer`；`$SKILL_DIR` 示例路径改为 `~/.claude/skills/academic-defense-beamer`；
   `agents/openai.yaml` 的 `display_name` 改为 `Academic Defense Beamer`。description 与 when_to_use 的能力描述本子任务不扩写（Typst 由子任务 3 加）。
3. 测试目录 `tests/skills/latex_defense_zh/` → `tests/skills/academic_defense_beamer/`；编译开关 `DEFENSE_ZH_COMPILE` → `DEFENSE_COMPILE`（不保留旧名别名）。
4. 契约测试、安装器、相邻技能（`latex-thesis-zh` 的路由边界与 trigger eval）、`AGENTS.md`、`.trellis/spec/academic-writing-skills/` 中的引用全部更新。
5. 文档：`docs/skills/latex-defense-zh/` 与 `docs/zh/skills/latex-defense-zh/` 移到 `academic-defense-beamer/`，VitePress 侧栏、首页、安装、快速开始、
   用法、README、README_CN 更新；`docs/resource-manifest.json` 用 `check_resource_sync.py --write-manifest` 重新生成，不手改散列。
6. `docs/CHANGELOG.md` 的 `[Unreleased]` 中涉及该技能的条目改用新名称（D2：未发版，不另写改名条目）；
   `docs/installation.md` 与中文镜像各加一句：旧的本地安装目录 `latex-defense-zh` 可删除。
7. 生成的 Beamer 产物里出现的旧名（主题 `.sty` 与 `deck.tex.j2` 的头注释）一并改为新名；主题宏名 `\Defense*` 与文件名 `beamerthemeYanshanDefense.sty` 不变。

## 不做

- 改任何脚本逻辑、CLI、D-* 码或模板版式。
- 改 `tex_loader.py` 的函数体（AST 对齐测试锁定）；只允许改模块 docstring 中的技能名。
- 改 `.trellis/tasks/archive/**` 与 `.trellis/workspace/**` 中的历史记录。

## 验收

- [ ] `rg -n "latex-defense-zh|latex_defense_zh|DEFENSE_ZH_COMPILE" --glob "!.trellis/tasks/**" --glob "!.trellis/workspace/**"` 只命中迁移说明句。
- [ ] `just ci` 四步通过；`uv run python docs/scripts/check_resource_sync.py` 通过。
- [ ] `DEFENSE_COMPILE=1 uv run pytest tests/skills/academic_defense_beamer` 在有 XeLaTeX 的机器上通过（无 XeLaTeX 时记为 UNVERIFIED）。
- [ ] `uv run python scripts/skills_install.py --help`（或其列表输出）出现 `academic-defense-beamer`，不出现旧名。
- [ ] `just doc-build` 成功，新路径页面可访问，旧路径不再生成。
- [ ] 改名前后对同一 fixture 运行 `build_deck.py`，`defense.tex` 除头注释外字节一致。
