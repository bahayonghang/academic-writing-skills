# implement — 08-10-nature-writing-zh

前置:确认 08-10-nature-writing-en 已合入(manifest 串行依赖);读父任务三份工件 + 本任务 design.md。

## 执行清单(有序)

1. [ ] 预检:`grep -rn "B-NAT" academic-writing-skills/latex-thesis-zh tests/` 确认 ID 无冲突;确认 EN 任务的 article-architecture.md N3 节措辞(文案对齐来源)
2. [ ] analyze_abstract.py `_run_bilingual()` 追加 B-NAT 提示项(design §1;english_found 门控)
3. [ ] 测试:bilingual 正例(含 B-NAT)+ 反例(无英文摘要不含)两条
4. [ ] abstract-structure.md 检查项表加 B-NAT 行
5. [ ] **验证点 A**:`pytest -k "abstract or bilingual"` 全绿 + fixture 手跑 `--bilingual --json`(PYTHONIOENCODING=utf-8)确认 schema 不变
6. [ ] conclusion-guide-zh.md 新节(design §2 四要素)
7. [ ] D-ZH-3 核对 results-analysis-guide-zh.md,按 design §3 判定标准落档或补节
8. [ ] 重建 manifest → 双语页面 → 侧栏(design §4)
9. [ ] **验证点 B**:`--skill latex-thesis-zh` 单项 + 全量资源校验 + `just doc-build`
10. [ ] SKILL.md 改 last_updated(仅此字段)
11. [ ] 行为 eval 记录到 verification.md:正反 fixture 输出对比;未跑 provider-backed 项标 UNVERIFIED
12. [ ] 终检:`just ci` + scripts 目录 diff 仅含 analyze_abstract.py + 收尾报告落档"已覆盖不改"清单

## 回滚点

- 验证点 A 失败:回退步骤 2-4,检查追加位置与 schema
- 验证点 B 失败:manifest 重建,双语页面按 spec 补齐

## 审查门

- 完成后走 2.2 质量检查再报告;父任务终检等两子任务归档后执行
