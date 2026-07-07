# 整理 tests 测试目录结构

## Goal

把根目录 `tests/` 下已经膨胀成一层平铺的 Python 测试文件，整理成按测试归属可浏览、可维护的目录结构，同时保持现有测试行为、pytest 发现规则、脚本导入语义和开发命令不变。

这次任务只重组测试目录与相关路径引用，不改变被测业务逻辑。

## Confirmed Facts

- 当前 `tests/` 根目录有 41 个顶层 `test_*.py` 文件，另有 `conftest.py` 与 `fixtures/`。
- `uv run --extra dev python -m pytest --collect-only -q` 当前可收集 890 个测试。
- `pyproject.toml` 的 pytest 配置是 `testpaths = ["tests"]` 与 `python_files = ["test_*.py"]`，递归子目录仍会被发现；`just test` 也显式运行 `tests/ academic-writing-skills/*/tests/`。
- `just check-versions` 目前硬编码运行 `tests/test_skill_versions.py -q`，如果移动该文件必须同步更新。
- 多个测试文件使用 `Path(__file__).parent.parent` 推导仓库根目录；移动到二级目录后会指向 `tests/` 而不是仓库根，需要统一替换为稳定路径入口。
- 多个测试文件 `from conftest import SCRIPT_DIR_*`；移动后不应继续把 `conftest.py` 当通用路径模块使用。
- `.trellis/spec/academic-writing-skills/testing-and-tooling.md` 明确要求 zh/typst 等非 EN/AUDIT 副本脚本测试使用 `importlib.util.spec_from_file_location` 按路径加载，并完整恢复 `sys.path` / `sys.modules`。本次整理不能破坏这些加载守卫。
- `tests/conftest.py` 的 sys.path 顺序是测试契约的一部分：EN 与 AUDIT 脚本目录前置，ZH / cover-letter 追加，由具体测试的 importlib loader 临时抢占。

## Requirements

- R1. 将根目录平铺测试改为目录化结构，根目录保留 `conftest.py`、`fixtures/`、测试支持模块，不再直接堆放大量 `test_*.py`。
- R2. 目录结构应以维护者最容易定位为准：单技能测试放到对应 skill 组，跨技能约束放到 contracts 组，共享脚本行为放到 shared 组。
- R3. 新增一个稳定的测试支持入口承载 `REPO_ROOT`、`SKILLS_ROOT`、`SCRIPT_DIR_*` 等路径常量；`conftest.py` 负责 pytest 配置和 sys.path 副作用，测试文件不再依赖 `conftest.py` 作为普通模块。
- R4. 移动测试文件后，所有 `Path(__file__)` 推导、显式测试路径、文档里的常用单测路径、脚本注释中的测试引用都要同步更新。
- R5. 不拆分大型测试文件、不重写测试断言、不改变被测脚本功能；本次只做结构重组和必要的路径适配。
- R6. 保留 `academic-writing-skills/bib-search-citation/tests/test_bib_search.py` 的技能内测试位置，因为 `just test` 已覆盖 `academic-writing-skills/*/tests/`，本任务不强行搬迁技能内测试。

## Proposed Directory Taxonomy

```text
tests/
  conftest.py
  fixtures/
  support/
    __init__.py
    paths.py
  skills/
    cover_letter/
    latex_paper_en/
    latex_thesis_zh/
    paper_audit/
    typst_paper/
  contracts/
  shared/
```

`bib-search-citation` 当前没有需要从根 `tests/` 移入的测试文件；它已有技能内测试目录。

## Acceptance Criteria

- [ ] 根 `tests/` 下不再直接放置 41 个平铺的 `test_*.py`；测试文件按 `skills/`、`contracts/`、`shared/` 归类。
- [ ] `tests/support/paths.py` 提供稳定路径常量，`conftest.py` 与移动后的测试文件都从该入口取路径。
- [ ] 所有移动后的测试文件不再因 `Path(__file__).parent.parent` 或 `from conftest import ...` 指向错误位置。
- [ ] `justfile`、`CLAUDE.md`、脚本注释、fixture README 中的旧测试路径引用已更新或改为目录级命令。
- [ ] `uv run --extra dev python -m pytest --collect-only -q` 仍可收集 890 个测试，或仅因显式、可解释的测试发现变更而变化。
- [ ] `just check-versions` 使用移动后的 `test_skill_versions.py` 路径并通过。
- [ ] `just test` 通过。
- [ ] `just lint` 与 `just typecheck` 通过；如果最终跑 `just ci`，则它必须通过。
- [ ] `git diff --check` 通过。

## Out Of Scope

- 拆分 `test_paper_audit.py`、`test_latex_paper_en_scripts.py`、`test_latex_thesis_zh_scripts.py` 等大型测试文件。
- 重新设计脚本加载器或把各 skill 的脚本副本抽成共享包。
- 修改 `academic-writing-skills/*/scripts/` 的运行逻辑。
- 搬迁 `academic-writing-skills/bib-search-citation/tests/` 这类已在技能目录内的测试。

## Notes

- User request: 当前 `tests` 目录下测试 py 文件结构混乱，需要深入分析并创建合适文件夹进行优化整理，且需要创建 Trellis 任务。
- Recommended decision: 使用上面的 `skills/ + contracts/ + shared/ + support/` 结构，并在用户确认后进入实现。
