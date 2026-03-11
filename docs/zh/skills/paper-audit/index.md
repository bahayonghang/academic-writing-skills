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
| `review` | 需要评审风格报告 | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode review` |
| `gate` | 只想看阻塞性问题 | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode gate` |
| `polish` | 想做风格导向的后续润色 | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode polish` |
| `re-audit` | 想对照旧报告复检 | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode re-audit --previous-report report.md` |

## 支持输入

- `.tex`
- `.typ`
- `.pdf`

## 核心能力

- 图表与引用完整性检查
- PDF 视觉排版检查
- 严重级别与优先级报告
- 4 维度评分
- 可选 ScholarEval 风格评估
- 可选在线文献验证

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
