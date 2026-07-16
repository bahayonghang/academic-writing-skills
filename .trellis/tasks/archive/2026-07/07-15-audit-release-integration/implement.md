# 发布集成与文档收尾 — 执行清单

前提：七个行为修复子任务全部归档（07-14 docs 树已于 2026-07-15 全部归档，无额外等待）。每步验证通过才进下一步。**全程不做 git commit——所有变更作为拟提交分组留到 Phase 3.4 统一展示确认**（仓库流程 workflow.md）。

## Step 1 — 基线确认

- [x] `python ./.trellis/scripts/task.py list --mine` 确认 07-15 树 7/8 done。
- [x] 记录进入本任务前的已知基线（2026-07-16 实时复核）：bib-search 技能测试
      `42 passed`，`just lint` 通过，Pyright `0 errors`；`just test` / `just ci` 为
      `1336 passed, 2 failed`。两项失败仅为 bib-search 的
      `references/limitations-and-errors.md` 与 `references/query-syntax.md` 已改、但
      `docs/resource-manifest.json` 的 `sourceSha256` 尚未同步，失败用例为
      `test_manifest_matches_live_public_inventory` 与 `test_inventory_only_cli_passes`。
      该已知漂移明确由本任务 Step 5 / R4a 消解；除此之外不得有基线失败。

## Step 2 — 跨子任务集成复查（R3）

- [x] `uv run --extra dev python -m pytest tests/contracts -q` 全绿（parsers/deai/writing-modules/版本四类锁）。
- [x] 按各子任务 design.md 的锁行声明抽查：en（extract_title/_strip_balanced_commands +1 行、writing 四脚本 en/typst 字节一致）、typst（TypstParser.clean_text 新锁行、PRESERVE `//.*` 条目删除）、zh（`_extract_balanced_block` 锁列表 +zh）。
- [x] `uv run --extra dev python -m pytest tests/ academic-writing-skills/*/tests/ -q` 全量绿。
- [x] 发现行为缺陷 → 停止，回开对应子任务（R5），本任务不修代码。

## Step 3 — last_updated（R1，拟提交分组 ①）

- [x] 六个 SKILL.md `last_updated` 改为执行日；只动这一个字段。
- [x] 验证：`git diff -- 'academic-writing-skills/*/SKILL.md'` 恰六行；`just ci` 仍绿（字符串锁防线）。

## Step 4 — CHANGELOG 6.0.0 段（R2，拟提交分组 ②）

- [x] 从 `task.py list-archive` + 各子任务 commit 汇总实际落地项，按 A-* ID 归纳成段写入 `docs/CHANGELOG.md`。
- [x] 逐条核对：每条对应真实 commit，无未落地项。

## Step 5 — 文档同步与一致性（R4，拟提交分组 ③）

- [x] R4b **概览一致性复查**（先于 checker——checker 捕获不了概览漂移）：逐技能对照最终 SKILL.md 路由表/能力文案与 docs **EN + zh 两侧** usage/概览页，更新漂移处（契约明文：router 变化必须同步双语 usage.md）。重点核对本树改过 SKILL 文案的技能（至少 paper-audit 的 Reviewer Lanes 段、latex-thesis-zh 的 bibliography 路由 gb7714-2025 提示；以各子任务最终 diff 为准）。
- [x] R4a 按 `.trellis/spec/academic-writing-skills/docs-bilingual-resources.md` 契约跑资源同步检查器，通过。
- [x] R4c `just doc-build` 成功。

## Step 6 — 收尾

- [x] 父任务 PRD 验收清单逐项核对勾选。
- [x] Phase 3.4：展示三个拟提交分组（① last_updated ② CHANGELOG ③ docs 一致性+同步），征得确认后提交。
- [x] `/trellis:finish-work` 归档本任务与父任务。

## 回滚点

每个拟提交分组独立可弃（scoped restore，禁用 reset）：既有文件 `git checkout -- <该分组修改文件>`；本任务如新建文件（CHANGELOG 段为编辑既有文件，通常无新建）按分组登记单列 `rm`。Step 2 失败时本任务归零成本退出。
