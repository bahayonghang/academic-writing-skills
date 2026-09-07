# 现有测试与证据基线

日期：2026-09-07（Asia/Shanghai）。仓库分支 `dev`，HEAD `f32fa909971b6975820dc4ad5565c278d5496b62`。执行前只有 README.md、README_CN.md 两处推荐模型文本的未提交修改；本轮未改动它们。

## 命令与结果

命令在仓库根执行，外层用 `rtk proxy` 保留原始输出。日志下列 `.txt` 副本可纳入版本控制，`.log` 被全局忽略模式排除。

| 检查 | 命令 | 结果 | 证据 |
|---|---|---|---|
| 项目完整门禁 | `just ci` | PASS，退出 0 | [完整输出](just-ci-output.txt) |
| 版本一致性 | `just ci` 内 `just check-versions` | 1 passed，0.07s | 完整输出第 5–9 行 |
| Ruff format/check | `just ci` 内 `just lint` | 200 files already formatted；All checks passed | 完整输出第 11–16 行 |
| Pyright | `just ci` 内 `just typecheck` | 0 errors，75 warnings，退出 0 | 完整输出第 18–193 行 |
| Pytest | `just ci` 内 `just test` | **1756 passed，0 failed，0 skipped，161.44s** | 完整输出末尾；包括 bib-search-citation 内置 42 项测试 |
| 双语公开资源 | `uv run --extra dev python docs/scripts/check_resource_sync.py` | PASS，271 manifest entries，退出 0 | [输出](resource-sync-output.txt) |
| 文档构建 | `just doc-build` | PASS，VitePress 1.6.4，18.90s，退出 0 | [输出](docs-build-output.txt) |
| 工作树空白检查 | `git diff --check` | FAIL，退出 2（Git本身；RTK外层返回1），仅 README_CN.md:14 原有行末双空格 | 用户进入任务前已有的推荐模型行；本轮保留 |

环境：Windows，Python 3.13.14，pytest 9.0.2，just 1.58.0，uv 0.12.10，Node v26.7.0。使用现有 `.venv` 和 `docs/node_modules`，没有执行安装或新增依赖。远端 Pages 使用 Node 20，因此本地构建不能代替远端环境的复现。

## 失败和警告的分类

本轮现有本地门禁没有失败，不能为了满足“追踪失败”而编造失败用例。历史远端失败另见 CI 审查证据；必须同时给出 run SHA、触发事件和失败日志是否仍可取得。

补充：这里“门禁没有失败”特指 just ci / 资源同步 / 文档构建。最终 git diff --check 报 README_CN.md:14 的原有 Markdown 行末双空格；该行属于用户已有改动，本轮不修。后续按任务新增 diff 的空白结果验收，并单独列出保留的既有失败，不能声称整个工作树 diff check 通过。

75 条 Pyright warning 是既有配置允许的警告，不是此次引入的失败。`pyproject.toml` 将多项类型诊断降为 warning；其中包含 compile.py 的可选 key、deai_check.py 的容器类型推断等。仅在后续批准项实际触及这些代码或能证明运行错误时做针对性修复；本计划不扩展为全面类型重构。

## 不能从通过结果推出的结论

- `tests/contracts/test_trigger_evals.py:1-9` 明确语料结构测试不运行真实模型 trigger eval；1756 passed 不证明五工具真实触发准确率。
- 本机配置目录存在不证明 Git 克隆后可得，也不证明 hooks 获授权并执行。
- 没有在 Claude Code、Grok Build、Kimi Code、OMP 中启动新的模型会话；Codex 当前会话和子代理工具可用，也不等于项目配置的新会话验收。
- 没有触发 GitHub 工作流或部署；没有验证真实论文质量、PDF 全部可选依赖、跨平台安装和各模型相对费用。

## 后续复验原则

执行批准的最小改造后先跑对应子任务门禁，最终只跑一次 `just ci`、资源同步、文档构建。仅在新修改、失败或未决风险时增加验证，不重复全量运行来制造证据数量。
