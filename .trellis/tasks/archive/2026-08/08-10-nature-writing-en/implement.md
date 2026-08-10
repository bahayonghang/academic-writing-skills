# implement — 08-10-nature-writing-en

前置:读父任务 prd.md + research/source-basis.md + research/delta-matrix.md + 本任务 design.md。

## 执行清单(有序)

1. [ ] 预检:`grep -rn "routing" tests/contracts tests/skills` 确认 routing-rules.md 的锁定格式;`grep -rn "article-architecture" .` 确认无命名冲突
2. [ ] 写 `references/writing/article-architecture.md`(design §1 结构;归属声明措辞抄 source-basis.md;N3 措辞抄 delta-matrix 共享契约)
3. [ ] 路由接入三处(design §2);每处最小 diff
4. [ ] translation-guide.md 加两节 + modules/translation.md 加索引(design §3)
5. [ ] title.md / tables.md 微补(design §4)
6. [ ] **验证点 A**:`uv run --extra dev python -m pytest tests/contracts/ tests/skills/ -q` — 契约与字符串锁全绿再继续
7. [ ] 重建 manifest → 校正 sourceLocale → 写 EN/zh 双语页面 → 侧栏注册(design §5)
8. [ ] **验证点 B**:`--skill latex-paper-en` 单项 + 全量资源校验 + `just doc-build`
9. [ ] SKILL.md 改 last_updated(仅此字段)
10. [ ] 行为 eval 并记录:
    - 正例:"把我的 Results 改成期刊式叙事" → 应路由到 article-architecture.md
    - 反例:"润色我的 NeurIPS 摘要语法" → 不应加载 article-architecture.md
    - 记录方式:任务目录 `verification.md`,未跑 provider-backed 的项标 UNVERIFIED
11. [ ] 终检:`just ci` + `git diff --stat -- '**/scripts/'` 为空 + 收尾报告落档 D-EN-4 "已覆盖不改"清单

## 回滚点

- 步骤 6 失败:回退步骤 2-5 的文档改动,修正格式后重做
- 步骤 8 失败:manifest 可重建,双语页面按 spec Good case 补齐

## 审查门

- 实现全程不做 `task.py start` 以外的状态变更;完成后走 2.2 质量检查再报告
