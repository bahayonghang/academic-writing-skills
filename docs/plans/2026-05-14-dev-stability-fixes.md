# Dev 分支稳定性优化计划

> 基于 2026-05-14 skill-creator 分析结果，按优先级排列
> **状态: ✅ 全部完成 (2026-05-14)**

## 背景

dev 分支 (v3.1.0, 15 commits ahead of main) 已通过全部 530 tests、lint、format 检查。
以下优化项均为"技术债"级别，不阻塞合并，但应在合并后尽快处理。

---

## Task 1: 契约测试补齐新增模块

**优先级**: 中 | **影响**: 测试覆盖缺口  
**文件**: `tests/test_skill_contracts.py`

### 目标

将 `tables`、`abstract`、`adapt` 模块加入各写作技能的契约测试 modules 列表。

### 步骤

1. `latex-paper-en` modules 列表末尾追加 `"tables"`, `"abstract"`, `"adapt"`
2. `latex-thesis-zh` modules 列表末尾追加 `"tables"`, `"abstract"`
3. `typst-paper` modules 列表末尾追加 `"tables"`, `"abstract"`, `"adapt"`
4. 运行 `just test` 确认通过

### 验证

```bash
uv run python -m pytest tests/test_skill_contracts.py -v -k "module_router"
```

---

## Task 2: paper-audit 契约测试迁移到规范模式名

**优先级**: 中 | **影响**: legacy alias 移除时测试断裂  
**文件**: `tests/test_skill_contracts.py`

### 目标

将 `paper-audit` 的 modules 列表从旧名更新为 SKILL.md v4.5 规范名。

### 步骤

1. 将 `"self-check"` 改为 `"quick-audit"`
2. 将 `"review"` 改为 `"deep-review"`
3. 保留 `"gate"`, `"polish"`, `"re-audit"` 不变
4. 运行 `just test` 确认通过

### 验证

```bash
uv run python -m pytest tests/test_skill_contracts.py -v -k "paper_audit"
```

---

## Task 3: pyright typeCheckingMode 升级为 basic

**优先级**: 中 | **影响**: 类型错误无法被 CI 捕获  
**文件**: `pyproject.toml`

### 目标

启用最低级别类型检查，逐步修复类型标注。

### 步骤

1. 将 `typeCheckingMode = "off"` 改为 `typeCheckingMode = "basic"`
2. 运行 `uv run pyright`，记录报错数量
3. 如果报错 < 20，直接修复后提交
4. 如果报错 > 20，先提交 `typeCheckingMode = "basic"` + 在 pyproject.toml 中添加必要的 `reportXxx = false` 抑制项，后续逐步修复
5. 运行 `just ci` 确认全链路通过

### 验证

```bash
uv run pyright
just ci
```

---

## Task 4: latex-thesis-zh Reference Map 消歧

**优先级**: 低 | **影响**: LLM 运行时可能读错文件  
**文件**: `academic-writing-skills/latex-thesis-zh/SKILL.md`

### 目标

在 Reference Map 中明确 `COMPILATION.md` 与 `modules/COMPILE.md` 的分工。

### 步骤

1. 在 Reference Map 的 `references/COMPILATION.md` 条目后追加说明：`（顶层编译策略概述；模块执行时读 modules/COMPILE.md）`
2. 确认 Module Router 的 compile 行 "Read next" 仍指向 `references/modules/COMPILE.md`

### 验证

目视检查 SKILL.md 中两处引用不冲突。

---

## Task 5: industrial-ai-research 无脚本说明

**优先级**: 低 | **影响**: 结构一致性  
**文件**: `academic-writing-skills/industrial-ai-research/SKILL.md`

### 目标

在 SKILL.md 中明确说明本技能为纯 LLM 驱动，不包含可执行脚本。

### 步骤

1. 在 `## Workflow` 之前或 `## Module Router` 表格下方加一行说明：

   > This skill is LLM-driven and does not include executable scripts. All phases are executed through web search, synthesis, and structured prompting.

2. 可选：创建 `scripts/README.md` 说明设计意图

### 验证

无功能变更，目视确认即可。

---

## Task 6: 确认 docs/node_modules 不在版本控制中

**优先级**: 低 | **影响**: 仓库体积  
**文件**: `.gitignore`

### 步骤

1. 运行 `git ls-files docs/node_modules | head -5`
2. 如果有输出，说明 node_modules 被跟踪：
   - 在 `.gitignore` 中添加 `docs/node_modules/`
   - 运行 `git rm -r --cached docs/node_modules`
   - 提交
3. 同时确认 `docs/.vitepress/dist/` 是否有意保留（用于 GitHub Pages 部署）

### 验证

```bash
git ls-files docs/node_modules | wc -l  # 应为 0
```

---

## 执行顺序建议

```
Task 1 + Task 2 (同一文件，一次提交)
  → verify: just test
Task 3 (独立提交)
  → verify: just ci
Task 4 + Task 5 (文档类，一次提交)
  → verify: 目视
Task 6 (仓库清理，独立提交)
  → verify: git ls-files
```

预计总工作量：30-60 分钟。
