# 实施计划

## 开始条件

intake-gating 与 delivery-tiers 两个子任务均已完成并各自验证通过。
本子任务不改那两个子任务拥有的源文件。

## 顺序

1. 读 eval runner，确认 `assertions` 支持的类型与是否支持否定断言，
   结果记入 `research/eval-runner-notes.md`。
2. 改 `trigger_eval.json`，新增门控与交付形态两类 query。
3. 用 Bash python 读—改—写 `evals.json`，新增两条行为用例。
4. `git diff` 核对 `evals.json` 中未改动条目零 diff、数组未被压平。
5. 两份 index.md 各补一节三级交付形态说明。
6. 做跨子任务一致性核对，写 `research/consistency-check.md`。
7. 跑集成检查。
8. 写交付说明，逐条标注证据档位与 missing evidence。

## 验证命令

```bash
uv run --extra dev python -m pytest tests/skills/paper_audit tests/contracts -q
uv run python docs/scripts/check_resource_sync.py
just ci
just doc-build
```

`evals.json` 的写入用如下形态，不用 Edit/Write：

```bash
uv run python -c "import json,pathlib; p=pathlib.Path('academic-writing-skills/paper-audit/evals/evals.json'); d=json.loads(p.read_text(encoding='utf-8')); d['evals'].append({}); p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')"
```

## 审查门

- 步骤 1 未完成不得写断言——否定断言是否可用决定用例写法。
- 步骤 4 发现格式被压平则回退 `evals.json` 重做。
- 步骤 6 发现冲突则停止，回退到对应子任务修正后再继续步骤 7。

## 回退点

步骤 2、3、5 各自独立可回退。步骤 7 失败区分本任务引入与既有问题，
缺工具时不补装、不假报通过。
