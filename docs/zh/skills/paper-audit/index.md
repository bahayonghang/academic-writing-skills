# `paper-audit`

统一支持 LaTeX、Typst 和 PDF 的学术论文审查技能。

## 适用场景

- 投稿前自查
- 结构化论文审阅
- 模拟评审
- 门禁式 pass/fail 判断
- 修改后的复审

## 模式

| 模式 | 适用场景 | 脚本 |
| --- | --- | --- |
| `self-check` | 做一次完整就绪性检查 | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode self-check` |
| `review` | 需要评审风格报告（脚本先给 Phase 0 自动审查） | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode review` |
| `gate` | 只想看阻塞性问题 | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode gate` |
| `polish` | 想做风格导向的后续润色 | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode polish` |
| `re-audit` | 想对照旧报告复检 | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode re-audit --previous-report report.md` |

## 支持输入

- `.tex`
- `.typ`
- `.pdf`
- 若要启用 venue 相关规则，可补充 `--journal` 或 `--venue`
- 使用 `re-audit` 时可补充 `--previous-report`

## 核心能力

- 图表与引用完整性检查
- IEEE 伪代码 gate 检查：浮动算法环境、caption/label/引用顺序，以及行号建议项
- PDF 视觉排版检查
- 严重级别与优先级报告
- 4 维度评分
- 文献综述质量评估（A1-A4：主题组织、批判性分析、研究空白推导、引用密度）
- 讨论深度与文献回溯（B3-B4）
- 结论完整性检查（B5：发现 + 启示 + 局限）
- 跨章节逻辑链闭合（C3：绪论声明在结论中回应）
- 可选 ScholarEval 风格评估
- 可选在线文献验证
- `review` 模式的多视角 agent 综合、`gate` 的 PASS/FAIL 门禁、`polish` 的预检查后润色，以及 `re-audit` 的差异复核

## 推荐提示词

```text
对 paper.tex 做一次 self-check 审查。
```

```text
判断 paper.pdf 是否已经达到投稿标准。
```

```text
基于上一次报告，对这篇论文做 re-audit。
```

```text
做一次 IEEE gate 检查，告诉我伪代码有没有浮动体或 caption 违规。
```

- 当前强化后的模式边界更明确：`review` 用于多视角综合审查，`gate` 适合 CI/投稿前门禁，`polish` 先过 precheck 再做表达打磨，`re-audit` 专门比较修订前后差异。
- 不同模式的输出不同：`self-check` 偏检查表与评分，`review` 偏综合评审包，`gate` 偏阻塞项结论，`re-audit` 偏问题状态与分数变化。
- IEEE 伪代码输出会显式区分硬性违规与建议项；缺少行号默认只记为建议，不直接阻断投稿。
