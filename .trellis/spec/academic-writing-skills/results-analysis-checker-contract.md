# 结果分析检查器契约

## 1. Scope / Trigger

修改 `latex-thesis-zh/scripts/analyze_experiment.py` 的 `--results-analysis`、RA-* 词表或
判据，或者修改其 fixtures、evals、SKILL 路由和公开结果分析资源时，必须遵守本文。
详细写作判据以 `references/writing/results-analysis-guide-zh.md` 为运行时权威；本文只锁定
开发接口和防回归边界。

## 2. Signatures

```text
uv run python scripts/analyze_experiment.py INPUT
  [--section SECTION] [--per-chapter] [--results-analysis] [--generate]
```

```python
analyze(
    file_path: Path,
    section: str | None = None,
    per_chapter: bool = False,
    results_analysis: bool = False,
) -> list[str]

_collect_results_intervals(
    lines: list[str], content: str, parser, section: str | None = None
) -> list[dict]
```

区间 payload 固定包含 `start`、`end`、`chapter_start`、`chapter_end`、`source`、`key`、
`chapter_has_summary`、`visible_lines`；段落 payload 固定为
`{start_line, raw_text, visible_text}`。每个 RA checker 的调用签名统一为
`(paragraphs, interval, chapter_window_raw, chapter_window_visible) -> list[str]`。

## 3. Contracts

- RA-* 只在 `--results-analysis` 下运行；默认模式与单独 `--per-chapter` 不得出现 RA 输出。
  两旗标同时存在时先保留 E-* 逐章检查，再附加 RA-*。
- 无 `--section` 时，区间为逐章 `EXP_SEC_RE` 通道与全局
  `^(discussion|result)(_\d+)?$` 通道的并集；重叠区间只保留带章上下文的逐章版本。
- 有 `--section X` 时，X 先经 `SECTION_KEY_ALIASES` 归一化，只选
  `^X(_\d+)?$` 后缀族，不回退到逐章通道。
- 全局区间的证据窗口只能是区间自身。所属章是否存在“小结”可作为 RA-TRANSITION 的
  布尔所有权元数据，但不得扩大 RA-CAUSAL、RA-EQUIV 或 RA-STAGE 的证据窗口。
- 段落按 raw 空行切分；`\ref{fig:` / `\ref{tab:` 只查 raw，语言词面与指标词只查
  visible。数学等价、一致性谓词、归因名词和规范性阶段声明只排除所在陈述句，不能屏蔽
  同段另一句的候选。
- RA-CAUSAL 的局部窗口为命中段前后各一段：局部组件证据静默，只有章级证据时 Minor，
  两级均无时 Major。多机制堆叠与末句撤回仍是 defensive-ai-rhetoric 的 `llm-only` 判据。
- RA-SECONDBEST 的对比、最优、次优和表引用只从当前区间读取。RA-STAGE 只使用
  `选定集|筛选后` 与 `生成样本|原始候选|合成样本` 两组对象词，并要求窗口内至少出现
  两种 KS/W1/MMD/SWD/C2ST/ACF/PSD 指标。
- 运行时检查族固定为 RA-EQUIV、RA-CAUSAL、RA-SECONDBEST、RA-SHALLOW、
  RA-DISTVOCAB、RA-UNIVERSAL、RA-STAGE、RA-TRANSITION。标定裁掉的候选不得留在脚本、
  SKILL、routing-rules、guide 或双语公开资源中；裁决证据只保留在任务标定报告。
- 所有 finding 使用 `[Script] RA-XXX（启发式线索，须 LLM 按证据阶梯复核）`，不得把
  脚本静默写成 R-* 语义清单通过；真实效果保持 `UNVERIFIED / missing evidence`。

## 4. Validation & Error Matrix

| 条件 | 必须行为 |
| --- | --- |
| 未传 `--results-analysis` | 默认与单独 `--per-chapter` 输出不含 `RA-` |
| 同时传 `--per-chapter --results-analysis` | E-* 与 RA-* 均运行；`--section` 只过滤 RA 区间 |
| `--section X` 有 `_N` 重复节 | 只返回归一化后的 `X` 与 `X_N`，全部为 global source |
| `--section X` 无匹配 | 输出 Info/P3 `RA-STRUCT`，不得回退逐章扫描 |
| 逐章与全局区间重叠 | 同一物理 finding 只报告一次，并保留逐章上下文 |
| 全局区间所属章有“小结” | RA-TRANSITION 静默；其他 RA 证据窗口仍限当前区间 |
| RA-CAUSAL 局部/章级/无证据 | 分别静默 / Minor-P2 / Major-P1 |
| 当前节无次优词、同章其他节有 | RA-SECONDBEST 仍按当前节报告，不借用其他节词面 |
| 公开资源残留已裁候选或散列过期 | focused contract 或 resource-sync 必须失败 |
| 未执行 provider-backed eval | 只能报告 `UNVERIFIED / missing evidence` |

```powershell
uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/test_results_analysis.py -q
uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/ tests/contracts/ -q
uv run python docs/scripts/check_resource_sync.py --skill latex-thesis-zh
just ci
```

## 5. Good / Base / Bad Cases

- Good：`--per-chapter --results-analysis --section result_2` 保留全章 E-*，RA 只扫描
  `result_2` 族；多文件 finding 输出真实 `源文件:行号`。
- Base：只传 `--results-analysis`，合并逐章结果节与全局 discussion/result 族，重叠项去重。
- Bad：让 `--section result` 回退到所有实验节，或用章内无关段落的“次优”压掉当前节
  RA-SECONDBEST；这会破坏区间所有权。

## 6. Tests Required

- zh 脚本按 `testing-and-tooling.md` 的 importlib 模式加载；断言 `__file__` 指向 zh 副本。
- 断言 result/discussion `_N` 后缀族、别名、精确 `--section`、重叠去重与旗标组合。
- 每个运行时 RA 检查至少一正一反；单独锁定 RA-CAUSAL 三档、RA-STAGE 同物理行两句、
  当前区间隔离、局部比较排除、章小结避让、raw/visible 分探针和多文件行号。
- 十条防误报红线不得只由实现推断；聚合静默 fixture 要覆盖未被单项边界覆盖的红线。
- evals 只追加、ID 唯一并绑定真实 fixture；防御性契约继续显式锁定 zh eval id 29。
- SKILL、routing、guide 或双语资源变化必须跑 contracts、单技能 resource sync 和 docs build。
- 产品回归测试若读取 Trellis 标定证据，必须指向已提交的 canonical archive 路径；
  禁止依赖会被 `task.py archive` 移走的 `.trellis/tasks/<active-task>/` 路径。

## 7. Wrong vs Correct

### Wrong

```python
# 章内任意证据都压掉当前因果论断，并让 --section 借用整章窗口。
if RA_COMPONENT_EVIDENCE_RE.search(chapter_visible):
    return []
interval["chapter_start"], interval["chapter_end"] = chapter_start, chapter_end
```

### Correct

```python
# 局部证据才静默；章级证据仅降档。global/--section 的证据窗口保持当前区间。
if RA_COMPONENT_EVIDENCE_RE.search(local_visible):
    return []
severity = "Minor" if chapter_has_evidence else "Major"
interval["chapter_start"], interval["chapter_end"] = start, end
interval["chapter_has_summary"] = owning_chapter_has_summary(start)
```

### Wrong: 归档前路径

```python
report = (
    REPO_ROOT
    / ".trellis"
    / "tasks"
    / "08-10-results-checker-zh"
    / "research"
    / "calibration-report.md"
)
```

### Correct: 规范归档路径

```python
report = (
    REPO_ROOT
    / ".trellis"
    / "tasks"
    / "archive"
    / "2026-08"
    / "08-10-results-checker-zh"
    / "research"
    / "calibration-report.md"
)
```
