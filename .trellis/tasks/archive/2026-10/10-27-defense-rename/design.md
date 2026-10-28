# 设计：改名迁移

## 原则

- 机械替换，分三类处理，避免盲目全局替换误伤：
  1. **标识符**：`latex-defense-zh`（目录、技能名、列表项、URL 路径）→ `academic-defense-beamer`；`latex_defense_zh`（测试包名）→ `academic_defense_beamer`。
  2. **环境变量**：`DEFENSE_ZH_COMPILE` → `DEFENSE_COMPILE`。子任务 3 另加 `DEFENSE_TYPST_COMPILE`，此处不加。
  3. **展示名**：VitePress 侧栏 “中文答辩稿 (latex-defense-zh)” → “学位论文答辩稿 (academic-defense-beamer)”，英文 “Thesis Defense Decks (academic-defense-beamer)”；
     `openai.yaml` `display_name` → `Academic Defense Beamer`。
- 保持不变：`\Defense*` 宏、`DefenseSource` 环境、主题文件名、D-* 码、`% defense-frame:` 标记、`defense.tex` 等产物名、`tests.support.paths` 中与路径无关的常量名。

## 文件处理表

| 文件 | 处理 |
| --- | --- |
| `academic-writing-skills/latex-defense-zh/**` | `git mv` 整目录；内部文本按上面三类替换 |
| `tests/skills/latex_defense_zh/**` | `git mv`；`conftest.py` 的路径常量与环境变量；测试中的技能名断言 |
| `tests/support/paths.py` | 若有该技能路径常量则更新（当前未定义，测试在 conftest 自建路径；实施时再确认） |
| `tests/contracts/test_skill_contracts.py` | 模块表键名、`SKILL.md` 路径、router help 测试函数名改为 `test_academic_defense_beamer_module_router_commands_match_script_help` |
| `tests/contracts/test_{skill_versions,skills_install,trigger_evals,tex_loader_alignment,docs_bilingual_resources}.py`、`tests/shared/test_tex_loader_security.py`、`tests/skills/latex_thesis_zh/test_thesis_rebuttal_installed.py` | 列表中的技能名 |
| `scripts/skills_install.py` | 目录列表 |
| `academic-writing-skills/latex-thesis-zh/SKILL.md`、`evals/trigger_eval.json` | 路由边界中的技能名；description 长度若有上限需复核 |
| `AGENTS.md` | 技能目录列表、parser copies 段、测试段（含环境变量）；`CLAUDE.md` 只引用 AGENTS.md，无需改 |
| `.trellis/spec/academic-writing-skills/defense-deck-contract.md` | 标题与正文路径；文件名保留（内容与后端无关的契约将在子任务 3 扩展） |
| `.trellis/spec/academic-writing-skills/{index,thesis-rebuttal-contract,include-boundary-contract}.md` | 引用 |
| `docs/skills/latex-defense-zh/`、`docs/zh/skills/latex-defense-zh/` | `git mv` 到 `academic-defense-beamer/` |
| `docs/.vitepress/config.ts` | `skillItems(prefix, "academic-defense-beamer")` 与侧栏标题 |
| `docs/{index,installation,quick-start,usage,CHANGELOG}.md`、`docs/zh/*`、`docs/skills/index.md`、`docs/zh/skills/index.md`、`docs/skills/latex-thesis-zh/index.md`、`docs/zh/skills/latex-thesis-zh/index.md`、`README.md`、`README_CN.md` | 名称与链接 |
| `docs/resource-manifest.json` | 只用 `check_resource_sync.py --write-manifest` 重生成 |

## 风险

- 资源页 `docs/skills/<skill>/resources/` 由资源同步脚本按技能目录生成并校验散列：先移动技能目录再重生成清单，顺序反了会出现成对的“缺失 + 多余”。
- `latex-thesis-zh` 的 description 中出现技能名，替换后长度增加 6 个字符；若契约测试限制 description 长度，需要缩写周边措辞而不是删掉路由提示。
- Windows 上 `git mv` 大小写或长路径问题：本改名不涉及大小写变化，风险低。
