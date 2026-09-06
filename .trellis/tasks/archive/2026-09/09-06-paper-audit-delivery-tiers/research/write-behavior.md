# 各模式落盘行为实跑记录

实跑日期 2026-09-06。

## 方法

每个模式在独立空目录中运行一次，目录内只放 fixture。
fixture 为 `academic-writing-skills/paper-audit/evals/fixtures/quick_audit_fixture.tex`，
复制为 `probe.tex`；re-audit 另放 `previous_review_report.md` 复制为 `prev.md`。
运行前后各 `find . | sort` 一次，差集即该模式的落盘产物。
`o` 与 `e` 是本次实跑自己的 stdout/stderr 重定向文件，不计入产物。

命令形态：

```bash
uv run python -B "$SRC/scripts/audit.py" probe.tex --mode <MODE>
```

## 结果

| 模式 | 落盘产物 | 退出码 | T3 可用 |
| --- | --- | --- | --- |
| `quick-audit` | 无 | 1 | 是 |
| `gate` | 无 | 1 | 是 |
| `re-audit` | 无 | 1 | 是 |
| `polish` | `.polish-state/precheck.json`、`.polish-state/artifacts/data/subsection_index.json`、`.polish-state/artifacts/windows/` | 0 | 否 |
| `deep-review` | 未实跑 | — | 否（见下） |

退出码 1 出现在有 blocker 的模式上，是正常返回，不是运行失败——
四次运行的 stderr 均为空，stdout 均含完整报告。

## 与静态推断的差异

父任务 [codex-findings.md](../09-06-paper-audit-intake-delivery/research/codex-findings.md)
依据 `scripts/audit.py:2704` 与 `audit.py:1961-1968` 推断
"quick-audit / gate / polish / re-audit 不建工作区"。

实跑推翻了其中 polish 一项。`polish` 不走 `run_deep_review`，
但另有独立写入路径：

- `scripts/audit.py:2509`：`state_dir = paper_path.parent / ".polish-state"`
- `scripts/audit.py:2526`：docstring 写明 "Writes .polish-state/precheck.json next to the paper file"
- `scripts/audit.py:2605`：`WorkspaceLayout(path.parent / ".polish-state")`

关键点：写入位置是 **论文文件所在目录**，不是当前工作目录。
因此 polish 在 T2（不得写入仓库）就已被挡住——
论文通常在仓库工作树内，`.polish-state/` 会落在仓库里。
polish 不是仅在 T3 不可用，而是 T2 与 T3 均不可用。

## deep-review 未实跑的理由

`deep-review` 会 dispatch 委员会与 lane agent，运行代价与副作用远大于本次取证需要。
其落盘行为有两条无歧义的静态证据：

- `scripts/audit.py:2704`：`canonical_mode == "deep-review"` 是唯一进入 `run_deep_review` 的分支。
- `scripts/audit.py:1961-1968`：`run_deep_review` 在 `review_dir is None` 时无条件调用 `prepare_workspace`。
- `scripts/prepare_review_workspace.py:952`：`--output-dir` 默认 `./review_results`。

三条合起来足以判定 deep-review 必然落盘，因此列为 T3 不可用。
"deep-review 在 T3 下不可用"是 design advantage 级证据（静态），
不标为 validated advantage。

## 结论（供 T3 清单定稿）

T3 可用模式：`quick-audit`、`gate`、`re-audit`——三项均有实跑证据。
T2 额外排除：`polish`（写入论文目录）。
T3 额外排除：`polish`、`deep-review`。
