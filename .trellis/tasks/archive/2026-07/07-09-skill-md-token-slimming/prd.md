# PRD: 六技能 SKILL.md 精简优化（token 瘦身）

## 背景

`academic-writing-skills/` 六个技能的 SKILL.md 合计约 104 KB：

| Skill | SKILL.md 字节 | 行数 | 全目录 KB | md 文件数 |
|---|---|---|---|---|
| latex-thesis-zh | 24,158 | 200 | 841 | 43 |
| latex-paper-en | 19,060 | 189 | 787 | 65 |
| paper-audit | 18,534 | 372 | 916 | 55 |
| typst-paper | 15,893 | 173 | 703 | 49 |
| cover-letter | 13,535 | 140 | 370 | 29 |
| bib-search-citation | 13,131 | 269 | 146 | 5 |

Token 成本分两层：
1. **常驻层（每次会话必付）**：六条 frontmatter `description` 注入系统提示。latex-thesis-zh 的 description 显著超长（约 260 汉字 + 触发短语列举）。
2. **激活层（触发时付）**：整个 SKILL.md 读入。paper-audit（372 行）与 bib-search-citation（269 行）为最大项。

## 分析发现（精简候选）

### A. description 常驻层
- A1. latex-thesis-zh description 过长：触发短语枚举（"公式编号挤到下一行""每章最多 5 节"等）可压缩为类别词；预计可减 40-50%。
- A2. 其余五条 description 长度合理（280-420 字符），仅微调。

### B. SKILL.md 激活层（结构性冗余，六技能同构）
- B1. `Capability Summary` 与 `Triggering` 与 description 三处重叠——Capability Summary 可并入 Router 表或删除。
- B2. `Example Requests` 每技能 10-20 行，与 Triggering 重复；可删或缩至 3 例。
- B3. `Safety Boundaries` 各技能重复仓库级 Critical Rules（cite/ref/label 保护、不造假等）；可缩为一行引用 + 技能特有条目。
- B4. `Workflow` 与 `Module Router` 部分重叠（router 已表达阶段顺序）。
- B5. paper-audit 372 行为最大单体：`Workflow`（88 行）、`Review Standard`、`Reviewer Lanes` 细节可下沉 `references/`，SKILL.md 只留路由 + 契约。
- B6. bib-search-citation 269 行但 references 仅 5 个 md：`Search Planning`（29 行）、`Known Limitations`、`Error Handling` 可下沉 references/。

### C. 不动项（约束）
- 不改 Module Router 表结构（`tests/contracts` 的 ROUTER_ROW_RE 锁定，且全局格式化 hook 会重排表格——见 memory: skill-md-formatter-gotcha）。
- 不 bump SKILL.md version（须与 pyproject 同步，本任务只改 last_updated）。
- 不改 references/、scripts/ 的实质内容（本任务只下沉/移动，不删知识）。
- description 属路由边界修改，改后需跑 trigger 评测（evals）验证触发不回归。

## 目标与验收标准

- [ ] 六个 SKILL.md 合计体积从 ~104 KB 降至 ≤ 70 KB（-30%以上），单个不超过 200 行。
- [ ] latex-thesis-zh description 压缩至 ≤ 现有 60%，其余 description 不劣化触发覆盖。
- [ ] 下沉内容全部落入对应 `references/`，无知识丢失（diff 可追溯）。
- [ ] `just ci` 全绿（含 contract 测试 test_router_contract / test_parsers_alignment）。
- [ ] 若存在 evals：description/触发相关 evals 通过（evals.json 修改须走 Bash python 写入，避免 JSON hook 压平）。

## 范围外

- 不改 scripts/ Python 代码、agents/、docs 站点。
- 不合并技能、不改技能数量与命名。
- references/ 自身的去重瘦身（可另立任务）。
