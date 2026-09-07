# 实施计划

## 前置

C1 完成（避免同时修改 pyproject.toml）；用户批准。

批准后先读 prd/design 与父任务 implement.md，再检查真实文件锚点是否漂移。没有明确实施批准不得运行 task.py start。

## 步骤

1. 用默认收集输出与当前 just test 实际路径做 node-id 集合基线。
2. 将 pytest testpaths 指向 tests 与 academic-writing-skills；简化 just test 为复用配置的 python -m pytest。
3. 新增 ci.yml：沿用 checkout@v4；用 actions/setup-python@v7 选择 matrix 的3.10/3.13，astral-sh/setup-uv@v10.0.1 安装 uv 0.12.10，extractions/setup-just@v4 安装 just 1.58.0。UV_PYTHON 必须指向当前 matrix Python，UV_FROZEN=1；先打印 python/uv/just 版本，再 uv sync --frozen --extra dev 和 just ci。文档 job 显式准备 Python3.13/uv 和 Node20，运行完整资源检查、npm ci 和docs build；不依赖 runner 碰巧预装工具。
4. 核验 workflow 的事件、权限、matrix、命令退出传递和 path；不触发远程 workflow。
5. 本地执行门禁；后续获准提交/推送时再记录 GitHub run URL/SHA，未运行时保持 UNVERIFIED。

## 必须通过的检查

以下从仓库根运行；外层按本机 RTK 规则使用 rtk proxy，命令内容保持原义。新文件标为“新增”的测试在实施时创建。

```text
uv run --extra dev python -m pytest --collect-only -q
just test
just ci
uv run --extra dev python docs/scripts/check_resource_sync.py
npm --prefix docs run docs:build
git diff --check
```

## 审查与完成

上述 Actions 版本在2026-09-07已打开作者仓库核对：[setup-python](https://github.com/actions/setup-python)、[setup-uv](https://github.com/astral-sh/setup-uv)、[setup-just](https://github.com/extractions/setup-just)。实施时核对标签仍可解析；这里是CI工具供给，不新增产品Python/Node依赖。保留同SHA hosted运行缺证边界。

在独立取证中解析 YAML/对照当前命令即可，不新增锁字符串的 CI 测试框架。node-id 对比必须包含 bib-search-citation/tests 的42项。完整 just ci 与 just test 不需要重复运行：最终 just ci 的 test 结果可复用。

记录每条命令退出码、失败/跳过原因和适用工具，不能仅写“测试完成”。本轮只创建计划，以上验收默认未执行；父任务的审查基线不是改造后的验收结果。
