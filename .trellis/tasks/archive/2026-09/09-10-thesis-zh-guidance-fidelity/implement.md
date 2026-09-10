# C1 执行计划

依赖：父任务规划审阅通过且用户批准；先实施本子任务有助于 C2 使用一致的术语保真表述。
由 academic_writing_editor 实施，独立检查者只在本任务范围修复。

1. 保存本任务文件基线；复核父 gap-analysis G1–G3，按 design 运行8例旧规则采样。
2. 修正五个公开源文件，保持引用指针与规则 owner；不改脚本或学校阈值。
3. 同步五组双语资源；追加 fixture/定向 eval，既有前缀完整保留。
4. 执行8例修改后采样与独立保真核读；修复任何失败并仅复测受影响例。
5. 运行以下局部门禁，把全部 exit code/failed/skipped 与证据边界写 research/validation.md。
6. 通知父任务更新 manifest 后，执行单技能资源门禁；父任务最后完成全量 gates。
7. AC 全满足后交付评审，提交/归档遵循用户后续授权；不得自动推送。

局部命令（仓库根）：
```powershell
rtk uv run --no-sync python -m pytest tests/contracts/test_thesis_zh_guidance_fidelity.py tests/contracts/test_polish_contract_alignment.py tests/contracts/test_deai_pattern_cluster_contract.py tests/contracts/test_defensive_ai_rhetoric_contract.py tests/contracts/test_trigger_evals.py tests/contracts/test_skill_contracts.py -q
rtk uv run --no-sync python docs/scripts/check_resource_sync.py --skill latex-thesis-zh
```
新增测试文件只在实施后执行。资源门禁要在父任务更新 manifest 后运行；不可用 inventory-only 替代。
不运行新的付费 provider，不安装依赖；缺少能力如实报告。

回滚点：改源前、采样前分别记录本次文件 diff；用精确逆向补丁恢复本任务改动。
eval 追加按对象定位，不整文件覆盖用户新增；不使用 git reset/clean。
