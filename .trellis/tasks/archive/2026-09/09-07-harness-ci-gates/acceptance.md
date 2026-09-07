# C2 本地验收记录

日期：2026-09-07。实施者只改产品范围内的 pytest 配置、`just test` 与新增 `ci.yml`。未触发 GitHub workflow，未把本地结果写成 hosted 同 SHA 通过。

## Node-id 集合

| 收集命令 | 改造前 | 改造后 |
|---|---|---|
| `uv run --extra dev python -m pytest --collect-only -q` | 1714 | 1756 |
| 原 `just test` glob：`tests` + `academic-writing-skills/*/tests` | 1756 | 不再单独枚举 |
| 简化后 `just test`（`python -m pytest`，复用同一配置） | — | 1756 collected；`just test` 执行 1756 passed，0 failed，0 skipped，286.16s |

改造后默认 collect 与 `just test` 的 node-id 集合一致。改造前 just-glob 的 1756 项全部保留。`academic-writing-skills/bib-search-citation/tests` 的 42 项均在默认收集中。新增项只允许增加；本轮计数等于 1756，没有下降。

`just test` 输出确认 `testpaths: tests, academic-writing-skills`，并在末尾执行 `academic-writing-skills/bib-search-citation/tests/test_bib_search.py`。

## Workflow 本地核验

`.github/workflows/ci.yml` 原文含：`pull_request` 与 `push`；`permissions.contents: read`；无 `release`、无 `pages: write`、无 `continue-on-error`。矩阵为 `ubuntu-latest` / `windows-latest` 与 Python `"3.10"` / `"3.13"`。`UV_PYTHON` 绑定 `${{ matrix.python-version }}`，`UV_FROZEN: "1"`。供给步骤为 `actions/checkout@v4`、`actions/setup-python@v7`、`astral-sh/setup-uv@v10.0.1`（uv 0.12.10）、`extractions/setup-just@v4`（just 1.58.0）；先打印 python/uv/just 版本，再 `uv sync --frozen --extra dev` 与 `just ci`。文档 job 在 Ubuntu 上设置 Python 3.13/uv、Node 20（`docs/package-lock.json`）、`npm ci --prefix docs`、资源同步与 `npm --prefix docs run docs:build`。

`.github/workflows/deploy.yml` 未修改。release-only 触发与生产 Pages 权限保持原状。

未执行 `gh workflow run`、未 push、未 dispatch。Windows/Ubuntu × Python 3.10/3.13 的 hosted 同 SHA 矩阵：**UNVERIFIED**。

## 命令退出码

| 检查 | 退出码 | 说明 |
|---|---|---|
| 改造前默认 `--collect-only -q` | 0 | 1714 项 |
| 改造前 just-glob `--collect-only -q` | 0 | 1756 项；多出的 42 项全部来自 bib-search-citation/tests |
| 改造后默认 `--collect-only -q` | 0 | 1756 项；含 bib 42 项 |
| `just --show test` | 0 | `uv run --extra dev python -m pytest` |
| `just test` | 0 | 1756 passed |
| `git diff --check -- justfile pyproject.toml` | 0 | 无新增行末空白 |
| `ci.yml` 原文事件/权限/矩阵检查 | 0 | 见上；PyYAML 1.1 会把键 `on` 读成布尔，不以该解析作为 GitHub 事件结论 |
| `just ci` | 未跑 | 本轮已跑 `just test`；完整四段门禁交主会话 |
| 资源同步 / docs build | 未跑 | 文档 job 只写入 workflow；本地未当作 hosted 证据 |
| hosted GitHub 矩阵 | UNVERIFIED | 未触发远端运行 |

不能从本次本地结果推出 hosted runner 已安装 uv/just、Linux 矩阵已通过，或当前 SHA 已有 Actions 成功记录。
