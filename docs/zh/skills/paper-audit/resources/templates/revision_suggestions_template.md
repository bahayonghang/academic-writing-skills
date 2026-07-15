# 修订路线图模板

根据审计结果和审查评估生成优先行动计划。

---

## 模板

```markdown
# Revision Roadmap

**Paper**: `{file_path}` | **Date**: {timestamp}
**Based on**: {mode} audit {+ multi-perspective review if applicable}
**Overall Score**: {overall}/6.0 ({score_label})

---

## Priority 1 — Must Address (Blocking)

Issues that must be resolved before submission. Correspond to Critical severity findings.

| # | Task | Source | Section | Est. Effort |
|---|------|--------|---------|-------------|
| R1 | {Specific revision task} | {Module or Reviewer} | {Section X.X} | {hours/days} |
| R2 | {Specific revision task} | {Module or Reviewer} | {Section X.X} | {hours/days} |

### R1: {Task title}
- **Problem**: {What is wrong}
- **Source**: {Which check or reviewer identified this}
- **Requirement**: {What needs to change}
- **Acceptance criteria**: {How to verify it is fixed}

### R2: {Task title}
- **Problem**: {description}
- **Source**: {source}
- **Requirement**: {what to do}
- **Acceptance criteria**: {verification}

---

## Priority 2 — Strongly Recommended

Issues that significantly improve paper quality. Correspond to Major severity findings.

| # | Task | Source | Section | Est. Effort |
|---|------|--------|---------|-------------|
| S1 | {Specific revision task} | {Module or Reviewer} | {Section X.X} | {hours/days} |
| S2 | {Specific revision task} | {Module or Reviewer} | {Section X.X} | {hours/days} |

---

## Priority 3 — Optional Improvements

Style, formatting, and minor issues. Correspond to Minor severity findings.

- [ ] {Minor task — from GRAMMAR, SENTENCES, FORMAT, etc.}
- [ ] {Minor task}
- [ ] {Minor task}

---

## Revision Checklist

### Priority 1 (Must Fix)
- [ ] R1: {task}
- [ ] R2: {task}

### Priority 2 (Should Fix)
- [ ] S1: {task}
- [ ] S2: {task}

### Priority 3 (Nice to Fix)
- [ ] {task}
- [ ] {task}

---

## Estimated Total Effort

| Priority | Items | Est. Time |
|----------|-------|-----------|
| Priority 1 | {count} | ~{X} hours |
| Priority 2 | {count} | ~{Y} hours |
| Priority 3 | {count} | ~{Z} hours |
| **Total** | **{total}** | **~{sum} hours** |

---

## Revision Deadline Guidance

- **Minor Revision scope** (P1 only): 1-2 weeks
- **Major Revision scope** (P1 + P2): 4-6 weeks
- **Full Revision scope** (P1 + P2 + P3): 6-8 weeks

---

## Re-Audit Instructions

After completing revisions, run:
```bash
pythonaudit.py {文件路径}--mode重新审核--previous-report{这个报告路径}
```

This will verify each item against the revised paper and report:
- FULLY_ADDRESSED / PARTIALLY_ADDRESSED / NOT_ADDRESSED per item
- Any new issues introduced during revision
- Updated scores for comparison
```

---

## 设计原则

1. **可操作性**：每一项都是具体的任务，而不是模糊的评论
2. **可追溯性**：每个项目都链接回来源检查或审阅者
3. **优先级**：P1 > P2 > P3，反映对论文质量的影响
4. **时间估算**：帮助作者计划修订时间表
5. **可验证性**：每个 P1 项目都有验收标准
6. **兼容性**：格式作为重新审核模式验证的输入
