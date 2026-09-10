# C2 执行计划

依赖：父任务审批；建议 C1 后执行。C3 修改共用测试文件前必须等本任务交接。
1. 复跑父任务 G4/G5 探针，保存本次基线。
2. 新测试按 tests.support.paths + importlib 加载 ZH 副本并断言 __file__；
   先写用户可观察的错误反例，确认现行实现失败。
3. 在 check_consistency 内实现 design 的分组、全文首次顺序与重复释义候选；
   复用现有 assemble/origin，不新增章状态或修改共享模块。
4. 修正旧测试的错误概念正例；增加 CLI --terms/--abbreviations/完整模式、
   custom-terms、入口/目录/--all-files、同名多目录、多行及同一行定位的测试。
5. 同步一致性模块的双语说明；记录哪些是脚本结果，哪些需要 LLM。
6. 运行局部门禁；交接共用测试文件给 C3，父任务再完成 manifest/全量资源门禁。
7. 提交和归档只在后续授权时执行，明确“默认行为变化：误报/假绿修复”。

```powershell
rtk uv run --no-sync python -m pytest tests/skills/latex_thesis_zh/test_consistency_semantics.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_checker_precision.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_scripts.py -q
rtk uv run --no-sync python -m pytest tests/contracts/test_parsers_alignment.py tests/contracts/test_skill_contracts.py -q
```
新增测试在实施后运行。CLI subprocess 使用子输出 UTF-8 与父 encoding=utf-8 成对协议。
夹具由测试 tmp_path 合成；不依赖私人论文或活动 Trellis 目录。
API/CLI 的断言使用独立预期位置与判定，不只复算实现的中间列表。

若实现发现必须更改 shared parser 或新增命令接口，回到规划，不默默扩 scope。
回滚用精确逆向 diff，保留同文件中 C3 和用户新增的其他测试。
