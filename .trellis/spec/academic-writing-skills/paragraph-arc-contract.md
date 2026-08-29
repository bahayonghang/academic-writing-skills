# 中文学位论文段落弧线检查器契约

## 1. Scope / Trigger

修改 `latex-thesis-zh/scripts/analyze_logic.py` 的 `--paragraph-arc`、P-ARC-* 判据、
`paragraph-arc-terms.yaml`、稳定 fixture、标定证据或公开段落弧线资源时，必须遵守本文。
面向写作者的语义说明以 `references/writing/paragraph-arc-zh.md` 为权威；本文锁定开发接口、
章节所有权、硬边界和防回归门禁。

## 2. Signatures and Constants

```text
uv run python scripts/analyze_logic.py INPUT [--section SECTION] [--paragraph-arc]
```

```python
analyze(file_path: Path, ..., paragraph_arc: bool = False) -> list[str]

PARAGRAPH_ARC_MIN_HAN = 40
PARAGRAPH_ARC_LINK_THRESHOLD = 0.0200
PARAGRAPH_ARC_DOUBLE_MISSING_RUN = 3
```

术语表固定包含 `judgment_predicates`、`empty_transitions`、
`retrospective_markers`、`prospective_patterns`、`explicit_link_markers`。运行时逐字段读取
YAML；缺失、类型错误或非法正则只回退该字段，内置默认与 YAML 及两个 neutral docs 副本
必须相等。

## 3. Contracts

- P-ARC 只在 `--paragraph-arc` 下运行；未传 flag 时稳定 fixture 输出必须逐字节不变。
  `baseline-before.txt` 是精确字节快照，须由 `.gitattributes` 标记为 `-text -diff`，避免
  Windows 换行归一化或末尾合法空行破坏基线。
- 段落按空行、纯注释、`\par`、标题和受保护环境边界切分。标题与公式、图表、算法、
  代码、列表环境会结束 `prose_segment`；LINK 不得删除豁免段后重新拼接邻接关系。
- 段落定位使用首个和末个有可见正文或引用的源行；独立 `\label{}` / `\ref{}` 行不得
  把 LEAD/CLOSE 位置偏到结构命令行。
- 章节所有权先取最具体的已识别子节；该子节结束后必须回退到所属章。不得因
  `split_sections` 关闭了 `organization` / `summary` 等子区间而把后续绪论段落归为 `None`。
- 少于 40 个汉字、标题导语、列表项、以受保护环境收尾的段落，以及
  `abstract/conclusion/acknowledgment/appendix/organization/summary` 不参与检查。
- `P-ARC-LEAD`、`P-ARC-CLOSE`、`P-ARC-LINK`、`P-ARC-FLAT` 均为 Info/P3。
  仅 `introduction` / `related` 中连续 3 个原始相邻合格段同时缺 LEAD+CLOSE 时，按每个
  连续 run 追加一条 Minor/P2 汇总；短段、标题、环境、章节与任一豁免段都重置 run。
- LINK 先检查显式标记，再检查端点长度与 token Jaccard。任一 token 集为空时为 0.0；
  先四舍五入到 4 位，严格 `score < 0.0200` 报告，等于阈值通过。
- 相关工作中的作者/年份罗列由 A1 负责；P-ARC-FLAT 不重复报告该形态。
- 每个 finding 头必须含 `[Script] P-ARC-*`，块内必须含
  `Meaning-Check: NEEDS-LLM`；不得复制完整原句、产出改写或给 `logic` 增加改写契约。

## 4. Private Calibration Boundary

私有论文只读用于 G1/G2。仓库只保存源 SHA-256、行号、句子散列、人工标签与聚合统计，
不得保存正文或让产品测试依赖本机路径。G2 必须直接调用产品段落切分、豁免、术语加载和
LINK 判定复算人工正接口；平行实现只能辅助阈值研究，不能单独证明产品门禁。单章不能证明
跨模板或跨学科代表性，始终标记 `UNVERIFIED`。

## 5. Tests Required

- zh 脚本按 `testing-and-tooling.md` 的 importlib 模式加载并锁定 `__file__`。
- 锁定 LEAD/CLOSE 独立定位、结构命令行避让、四类 finding 输出字段及默认输出字节基线。
- 锁定标题、公式、图、表、算法、代码、列表、短段和专用章节豁免；LINK 与 N=3 run 都要
  覆盖边界复位，不能只测单个正常路径。
- 锁定显式标记、重叠通过、空 token、四位舍入等于/小于阈值，以及 FLAT 单句/罗列正反例。
- 公开资源变化后运行单技能与全量 resource sync、双语 contract、docs build 和 `just ci`。

## 6. Quality Check

```powershell
uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/test_paragraph_arc.py -q
uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/ tests/contracts/ -q
uv run python -X utf8 docs/scripts/check_resource_sync.py --skill latex-thesis-zh
uv run python -X utf8 docs/scripts/check_resource_sync.py
just doc-build
just ci
```

复核时还必须执行私有 G2 复算（若语料可用）、`git diff --check` 与任务校验，并确认
测试/公开资源没有本机私有路径依赖。
