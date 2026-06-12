# Implementation Plan: latex-thesis-zh 章引言承上启下

## Phase 0: Review Gate

- [ ] 确认范围：扩展现有 `logic` 模块 + 写作参考 + 测试，**不新增模块**。
- [ ] 确认章引言检查显式排除绪论（由 `_check_introduction_funnel` 负责），零重叠。
- [ ] PRD 与 design 评审通过前，任务保持 planning，不进实现。

## Phase 1: 写作参考（指导层）

- [ ] `references/writing/thesis-writing-guide.md` 新增《正文章引言（承上启下两段式）》节：
  - 两段角色定义（承上 / 启下）、篇幅约定（1~2 段 / 约 300~500 字）。
  - 一个可套用模板（"第X章……解决了……仍存在……；针对……，本章提出……，核心思想是……，相比……优势在于……。本章组织如下：……"）。
  - 一组正反例（规范两段 vs 章后直接 \section / 单句 / 相对指代）。
- [ ] `references/writing/structure-guide.md` 导语规范处补一句章引言约定。
- [ ] `references/modules/logic.md` 补一句章引言专项检查说明。

## Phase 2: 脚本检查（诊断层）

- [ ] `scripts/analyze_logic.py` 新增常量：`CHAPTER_PREVIEW_KEYWORDS_ZH`、`RELATIVE_REF_PATTERNS_ZH`、`CHAPTER_NUM_REF_RE`。
- [ ] 扩展章引言检查（在 `_check_chapter_mainline` 内或新增 `_check_chapter_intro`，由 `analyze()` 默认调用）：
  - 取章引言块（`\chapter` → 首个 `\section`）。
  - 承上缺失 / 启下缺失 → Major/P1。
  - 篇幅过短 / 过长 → Minor/P2。
  - 相对指代 → Minor/P2（建议章节号）。
  - 疑似与绪论重复 → LLM 备注。
  - 排除绪论/引言/结论/总结/展望/致谢/附录；第一个正文章对"承上"放宽。
- [ ] 保留 `_check_chapter_mainline` 既有"多章缺桥接"可观察行为。

## Phase 3: SKILL.md 接线

- [ ] 路由规则 / Reference Map 增加一句章引言指引（最小措辞）。
- [ ] 递增 `metadata.version`，更新 `last_updated`。

## Phase 4: 测试

- [ ] 新增 3 个 fixture：① 规范两段章引言（全过）② 章后直接 \section（报承上+启下缺失）③ "上一章"相对指代+单句（报相对指代+篇幅过短）。
- [ ] 为四类检查写断言。

## Phase 5: Validation

```bash
uv run --extra dev python -m pytest tests/test_skill_contracts.py tests/test_skill_versions.py
uv run --extra dev python -m pytest tests/ academic-writing-skills/latex-thesis-zh
just lint
git diff --check
```

- [ ] 规范 fixture 零 P1 误报。
- [ ] 既有 logic 检查（S1、绪论漏斗、C3、--motivation-thread）无回归。

## Rollback Points

- 若章引言检查对正常论文误报过多 → 收紧启发式（提高承上/启下信号阈值，或对首个正文章进一步放宽）。
- 若与 `_check_introduction_funnel` 输出重叠 → 收紧绪论排除名单。
- 若篇幅"过长"阈值争议大 → 先只保留"过短"提示，过长降级为可选。
