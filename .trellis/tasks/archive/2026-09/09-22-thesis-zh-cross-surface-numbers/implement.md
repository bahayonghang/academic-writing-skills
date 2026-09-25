# C4 执行计划

## Entry / dependencies
C3完成后串行交付公共文件；不依赖C1配置。
仅在本版父子规划获后续明确实施授权、通过结构检查后，激活此子；父任务不直接写产品。
读取 implement.jsonl/check.jsonl 的既有规范与父研究，然后读本子prd/design/implement。
精确源码和测试白名单见本子design§1；父design§3规定公共文件时段所有权。

## Ordered steps and validation
1. 采集experiment默认和results-analysis基线；按design§2做简单表格/正文/小结原位抽取。
   先添加本子AC矩阵中的失败/反例测试；阶段验证用下面目标命令按对应test名称运行。
2. 按design§3唯一键绑定与缺表面规则，再做§4混用/互推候选与JSON词表；先写碰巧同数、单位不明等反例。
   对应本子design和AC逐条验收；检查报告位置、错误路径和无新flag旧输出。
3. 按本子design文件清单更新公开指南、路由、规范和合成eval；按父design§3同步公共入口。
   所有公开源同步本语言mirror、另一语言翻译、manifest；人工核对事实与链接。
   执行资源manifest重建后仍须完整检查，不能用inventory-only作为最终通过。
4. 运行下列目标测试与全量门禁；成功后记录命令、exit、AC证据、未覆盖范围。
   对应默认baseline命令保持路径/UTF-8/年份一致；不得靠改预期值掩盖默认行为变化。
5. 移交下一子前检查完整差异只落白名单；记录共享文件归属与局部回滚点。
   本计划不授权commit/archive/push；本轮规划结束不执行这些步骤。

## Commands during future implementation
rtk proxy uv run --extra dev python -m pytest -q tests/skills/latex_thesis_zh/test_cross_surface_numbers.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_coverage.py
rtk proxy uv run --extra dev python -m pytest -q tests/contracts/test_skill_contracts.py tests/contracts/test_thesis_zh_guidance_fidelity.py
rtk proxy uv run python docs/scripts/check_resource_sync.py --write-manifest --inventory-only
rtk proxy just ci
rtk proxy uv run python docs/scripts/check_resource_sync.py
rtk proxy just doc-build

新增测试文件在实施中创建；规划阶段不把文件不存在当测试失败，也不宣称已执行这些测试。
just ci包含版本、lint、typecheck、pytest四项。checks通过后不重复扩大测试，除非出现新改动/失败。

## Acceptance evidence / rollback
每个AC子句对照本子design矩阵，记录实际用例和结果；结构校验、合成测试、真实论文、PDF、
provider与五宿主运行分别报告，未跑的为UNVERIFIED。
按当前子局部差异回退源码、测试、资源与manifest；有后继子时逆序，不整文件覆盖共享改动。
