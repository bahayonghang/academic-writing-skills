# 实施计划

## 顺序与授权

收尾执行；等待写作、工程章及用户追加的标点任务完成公共资源交接。先红测后修复，最后父任务集成。
用户已批准整棵任务实施；进入本子任务时 start，核对 dirty 并只改 design 白名单。

- [x] 读父任务研究、design 与 context，核对当前文件并落实正反例。
- [x] 按 design 修改最小目标；共同文件由本子任务单写，不覆盖前序内容。
- [x] 运行下列目标测试，按 design 保存实际输出/视觉证据。
- [x] 同步源语言/译文及 manifest，完成公开入口和说明检查。
- [x] 逐项填写 AC 证据，明确通过/失败/未运行/missing evidence，再交接。

## 未来实施检查

```powershell
uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/test_caption_commands.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_multifile.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_scripts.py tests/contracts/test_parsers_alignment.py -q
uv run --extra dev python -m pytest tests/contracts/test_skill_contracts.py tests/contracts/test_trigger_evals.py -q
uv run python docs/scripts/check_resource_sync.py --write-manifest --inventory-only
uv run python docs/scripts/check_resource_sync.py --skill latex-thesis-zh
uv run --extra dev python -m pytest tests/contracts/test_docs_bilingual_resources.py -q
just doc-build
rtk git diff --check
```

write-manifest 只在实施资源修改后运行，并审查 sourceLocale 与译文；用户已批准本轮实施。
完整 just ci 与全量资源检查由父任务最后统一执行。
JSON语料静态检查不是模型输出通过；编译/图片存在不是视觉验收。
缺工具/付费模型时不自动安装或调用，记录缺证据并保留对应未完成 AC。
若失败，先核实是否本任务造成，仅回退本任务确切 diff，不 reset/clean 工作树。
