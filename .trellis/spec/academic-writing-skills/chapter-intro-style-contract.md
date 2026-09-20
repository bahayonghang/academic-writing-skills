# 中文学位论文章引言段式与要件观察契约

## 1. Scope / Trigger

修改 `latex-thesis-zh/scripts/analyze_logic.py` 的 `--chapter-intro-style`、CI-* 判据、
`chapter-intro-style-terms.yaml`、相关 fixture 或公开正文章引言资源时，必须遵守本文。
面向写作者的语义说明以 `references/writing/thesis-writing-guide.md` 为权威；本文锁定开发接口、
三码契约、豁免、默认行为变化声明、私有标定边界和防回归门禁。

## 2. 术语分离

- **位置形态**（`intro_form`）：`lead`（章后导语）与 `numbered`（编号引言节），两者均合规。
- **段式**（`style`）：`one`（一段式，1段）、`two`（两段式，2段）、`multi`（多段式，$\ge 3$段），位置形态与段式正交。
- **核心要件**（`moves`）：问题、承上（第 2 章不适用）、方案、收束或路线。要件固定、段数灵活。

## 3. Signatures and Constants

```text
uv run python scripts/analyze_logic.py INPUT [--section SECTION] [--first-chapter N] [--chapter-intro-style]
```

```python
analyze(file_path: Path, ..., chapter_intro_style: bool = False) -> list[str]

CI_ONE_PARA_MAX_HAN = 600  # 未标定 / UNVERIFIED
```

阈值常量在指南、spec 和 YAML 注释三处标注为**未标定 / UNVERIFIED**。
术语表固定包含 `problem_markers`、`solution_markers`、`closing_markers` 三个字段。
运行时逐字段读取 YAML；缺失、类型错误或非法值只回退该字段，内置默认与 YAML 及两个 neutral docs 副本必须相等。

## 4. Contracts

- `--chapter-intro-style` 是可选附加开关，默认关闭；未传 flag 时输出必须逐字节不变（除默认行为变化的误报/建议修复外）。
- 所有 finding 均为 `[Script]` 观察，默认 `[Severity: Info] [Priority: P3]`，块内必须含 `Meaning-Check: NEEDS-LLM`。
  不得输出 `Meaning-Check: PRESERVED`，不得复制完整原句，不得给 `logic` 增加自动改写契约。
- `--method-narrative` 在未指定 `--section` 时的提前返回路径保持不变；在该路径下 `--chapter-intro-style` 不运行。
- 三码判定与豁免契约：
  1. `CI-STYLE`：正文章引言块非空时恒报一条。报告段式标签（一段式/两段式/多段式）、位置形态（编号引言节/章后导语）、约汉字数、段数与句数，以及四个核心要件的覆盖向量（问题:✓/✗ 承上:✓/✗/不适用 方案:✓/✗ 收束或路线:✓/✗）。第 2 章（概述式引言）承上标“不适用”。引言块为空时豁免。
  2. `CI-MOVES`：正文章引言块核心要件（问题、方案、收束或路线）任一缺失时报告。若方案未命中且默认检查已报“缺启下”，为避免重复不在此处报告方案缺失。引言块为空或 `--section` 区间外豁免。
  3. `CI-LONG`：一段式引言（`style == "one"`）单段汉字数 $> 600$ 且 $\le$ 默认篇幅上限（导语 900、编号引言节 1600）时报告，建议在方案宣告处拆为两段。汉字数超过默认上限时由默认检查覆盖（零重叠）；两段式与多段式豁免。
- 架构单源承诺：章引言行区间由 `_chapter_intro_span` 单源提供，`_chapter_intro_block` 改为调用它；抽取后默认输出与 `baseline-before.txt` 逐字节相等。

## 5. 默认行为变化声明

本任务包含两处经过批准的默认行为变化（属于 spec 允许的误报与误导修复例外）：
1. `CHAPTER_DEP_REF_RE` 扩展为支持顿号、逗号、波浪号、连字符及“至和与及”连接的章号列举（如“第 3、4、5 章”“第 3～5 章”），清除承上句因列举而被误判为缺承上的假阳性。
2. `_check_chapter_intro` 的四处建议文案（`bridge_suggest`、`preview_suggest`、过简建议、过长建议）改为段式中立表述，不再写死“第一段/第二段/两段”，避免误导一段式写作者拆段。observe 行与理由行字面保持不变。

## 6. Private Calibration Boundary

私有论文或内部语料仅可用于统计研究，不得成为常规 CI 的隐式前置条件。
常规测试与 CI 仅使用已提交的合成 fixture；公开测试和样例中不得出现真实私有论文语句、作者信息或本机绝对路径。
阈值常量未经全量跨学科跨校抽样标定前，始终标为 `UNVERIFIED`，不宣称误报率或漏报率。

## 7. Tests Required

- zh 脚本按 `testing-and-tooling.md` 的 importlib 模式加载并锁定 `__file__` 为 zh 副本。
- 锁定章号列举承上不再误报、单章“第 2 章”仍匹配、建议行不含“第一段/第二段/两段式/扩展为承上启下两段/保留承上启下两段”。
- 锁定三码正反例：第 2 章 `CI-STYLE` 承上标不适用；`CI-LONG` 与默认过长零重叠；`--section method` 作用域；`--first-chapter` 章号声明。
- 锁定 finding 格式包含 `[Script] CI-`、`[Severity: Info] [Priority: P3]`、`Meaning-Check: NEEDS-LLM`，且报告中不出现 fixture 整句。
- 锁定 YAML 字段与内置默认等价，以及逐字段降级回退能力。
- 锁定 `SMOKE_COMMANDS` 包含 `--chapter-intro-style`，且默认输出基线 `baseline-before.txt` 逐字节不变。
- 改 `analyze_logic.py` 后必须同步更新 `tests/skills/latex_thesis_zh/test_polish_unit_zh.py` 的 `FROZEN_HASHES["analyze_logic.py"]`（LF 规范化 sha256）。
- 锁定公开资源同步、双语镜像相等以及 VitePress 构建。
