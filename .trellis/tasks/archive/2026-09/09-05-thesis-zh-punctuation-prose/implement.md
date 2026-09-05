# 实施计划

用户已于 2026-09-05 明确追加并授权实施；工程章完成公共资源交接后执行，随后进入题注子任务。

- [x] 读 context、prd/design 和既有标点/deai 规则，核对累积 diff。
- [x] 按唯一规则 owner 修改、同步入口和双语镜像，追加至少 3 个 output 与 1 个 trigger。
- [x] 保存实际响应与语义裁决，验证事实/引用/数学/源码保真。
- [x] 完成下列验证并记录结果；全量 CI 由父任务最后执行。

```powershell
uv run --extra dev python -m pytest tests/contracts/test_skill_contracts.py tests/contracts/test_trigger_evals.py tests/contracts/test_defensive_ai_rhetoric_contract.py tests/contracts/test_deai_pattern_cluster_contract.py tests/skills/latex_thesis_zh/test_check_style_zh.py -q
uv run python docs/scripts/check_resource_sync.py --write-manifest --inventory-only
uv run python docs/scripts/check_resource_sync.py --skill latex-thesis-zh
uv run --extra dev python -m pytest tests/contracts/test_docs_bilingual_resources.py -q
just doc-build
rtk git diff --check
```

执行前核对测试真实路径并更新。无运行时代码变化，不为文档写镜像实现的测试。
