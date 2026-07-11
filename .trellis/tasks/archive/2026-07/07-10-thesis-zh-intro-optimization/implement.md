# implement.md — 执行清单

前置：本任务经 `task.py start` 激活后才可实施。每步完成即跑对应验证，最后一步全量 `just ci`。

## 顺序清单

1. **合成 fixture**
   - 制作脱敏等价样本 `tests/fixtures/`（或按现有 zh 测试 fixture 目录惯例）：绪论 tex（含堆引、同前缀扎堆、名词短语科学问题表、无对比表的综述小节、非漏斗首段）+ 迷你 bib（年份分布故意偏旧）。
   - 验证：肉眼比对问题模式与 prd 表格一一对应；不含用户论文原文。

2. **analyze_literature.py：A4~A8 + `--intro-citations`**
   - 键前缀归一函数独立可测；`--bib` 缺省降级为 Info。
   - 验证：`uv run --extra dev python -m pytest tests/... /test_intro_citations.py`。

3. **analyze_logic.py：L-SCI / L-MAP / L-FUN / L-DOM + `--intro-mainline`**
   - 验证：`test_intro_mainline.py` 双形态用例通过。

4. **references 四件**
   - 新建 `references/writing/introduction-guide-zh.md`（阈值全部注出处 + "以本校规范为准"）；
   - 追加 `modules/literature.md`、`modules/logic.md` 的新 flag 说明；
   - `thesis-writing-guide.md` 加指针一行。
   - 验证：文档内命令与脚本实际 flag 名一致（复制执行一遍）。

5. **SKILL.md 最小改动**
   - literature/logic 两行 Use when 补触发词；Reference Map 加一行；last_updated=实施日；version 不动。
   - 验证：`uv run --extra dev python -m pytest tests/contracts/`（ROUTER_ROW_RE 与字符串锁）。注意：表格改动别被全局格式化 hook 重排（memory: skill-md-formatter-gotcha）。

6. **evals 追加 case**
   - 用 Bash python 写入 evals.json（JSON hook 陷阱），跑 evals 相关 contract 测试。

7. **全量验证 + 真实样本回归**
   - `just ci` 全绿（看 pyright error 数）。
   - 对真实 chapter1.tex 跑两个新 flag，人工核对：128 唯一键、15 处堆引、zhao* 扎堆、表 1-2 科学问题名词短语均被命中 → 结果记入任务 journal（不提交论文本体）。

## 回滚点

- 每步独立 commit（fixture / literature / logic / references / SKILL.md / evals），任一步 revert 不影响其余。
- 新功能全部在新 flag 后，默认路径零行为变化。

## Review gates

- 步骤 2、3 完成后：自查诊断输出格式符合 Output Contract（`% MODULE (L##) [Severity] [Priority]`，`[Script]`/`[LLM]` 标注）。
- 步骤 5 完成后：确认 SKILL.md 未超 07-09 瘦身后的体量基线。
