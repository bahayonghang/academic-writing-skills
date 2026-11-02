# 父任务执行计划（集成）

父任务不直接改代码。按顺序启动子任务，每个子任务通过自己的检查与提交后再启动下一个。

## 顺序

1. `python ./.trellis/scripts/task.py start .trellis/tasks/10-27-defense-rename` → 实施 → trellis-check → 提交 → 归档。
2. `10-27-defense-beamer-notes`：前置条件为子任务 1 已提交。
3. `10-27-defense-typst-backend`：前置条件为子任务 1、2 已提交；开工前先完成其 implement.md 中的 spike 并把结论写回其 design.md。

## 集成复核（三个子任务都归档后）

```bash
just ci
uv run python docs/scripts/check_resource_sync.py
rg -n "latex-defense-zh|latex_defense_zh|DEFENSE_ZH_COMPILE" --glob "!.trellis/tasks/archive/**" --glob "!.trellis/workspace/**"
```

- 用 `academic-defense-beamer/evals/fixtures/mini-thesis` 各跑一遍 Beamer 与 Touying 全流程（extract → plan → 填写 → build --compile → check → preview），
  记录页数、D-* 计数与两份备注版的 D-NOTES-PDF 结果。编译用例需 `DEFENSE_COMPILE=1` / `DEFENSE_TYPST_COMPILE=1`。
- 人工证据：在 FerroStage 打开两份 `defense-notes.pdf`，截图演讲者窗口。未执行则在交付说明标 UNVERIFIED。
- 对照父 prd.md 的“跨子任务验收”逐条勾选；任何一条失败回到对应子任务。
- 规格：`.trellis/spec/academic-writing-skills/` 中的答辩稿契约与本文件第 2–6 节一致（由子任务 3 收尾时更新，父任务复核）。

## 回滚点

- 子任务 1 提交前：`git restore` 即可。
- 任一子任务提交后发现问题：`git revert <该子任务提交>`，其余子任务的提交保持不动；子任务 3 回退后 Beamer 路径不受影响。
