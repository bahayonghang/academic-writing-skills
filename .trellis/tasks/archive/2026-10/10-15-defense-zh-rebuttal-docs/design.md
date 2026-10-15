# C3 设计

父 `design.md` 是契约来源。本文件只写 C3 的文件清单、登记点与写作要点。

## 1. 新增文件

- `academic-writing-skills/latex-defense-zh/references/rebuttal-workflow.md`
- `academic-writing-skills/latex-defense-zh/references/rebuttal-writing.md`
- `academic-writing-skills/latex-defense-zh/references/rebuttal-gate.md`
- `academic-writing-skills/latex-defense-zh/examples/review-response.md`
- 双语资源页：`docs/skills/latex-defense-zh/resources/references/rebuttal-{workflow,writing,gate}.md`、
  `docs/zh/skills/latex-defense-zh/resources/references/rebuttal-{workflow,writing,gate}.md`、
  `docs/skills/latex-defense-zh/resources/examples/review-response.md`、`docs/zh/skills/latex-defense-zh/resources/examples/review-response.md`
- `.trellis/spec/academic-writing-skills/defense-rebuttal-contract.md`

## 2. 修改登记点

| 文件                                                                                | 改动                                                                  |
| ----------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| `academic-writing-skills/latex-defense-zh/SKILL.md`                                 | prd D1                                                                |
| `academic-writing-skills/latex-defense-zh/agents/openai.yaml`                       | `short_description`                                                   |
| `academic-writing-skills/latex-defense-zh/evals/evals.json`                         | 新增 eval（用 Bash 下的 Python 写入，避免 JSON 格式化 hook 压平数组） |
| `academic-writing-skills/latex-defense-zh/evals/trigger_eval.json`                  | 新增触发条目（同上）                                                  |
| `tests/skills/latex_defense_zh/test_defense_skill_entry.py`                         | `MODULES`                                                             |
| `docs/skills/latex-defense-zh/index.md`、`docs/zh/skills/latex-defense-zh/index.md` | 模块表三行、rebuttal 流程、输出                                       |
| `docs/resource-manifest.json`                                                       | `check_resource_sync.py --write-manifest --inventory-only` 重建       |
| `README.md:55`、`README_CN.md:47`                                                   | 技能行描述                                                            |
| `docs/CHANGELOG.md`                                                                 | 顶部新增条目，历史条目不动                                            |
| `.trellis/spec/academic-writing-skills/index.md`                                    | 新契约一行                                                            |
| `.trellis/spec/academic-writing-skills/defense-deck-contract.md`                    | 「五脚本」处加指向新契约的一句                                        |

不改：技能登记硬编码列表（技能数不变）、`docs/.vitepress/config.ts`（侧栏由 `resourceItems` 按 manifest 生成）、版本号。

## 3. SKILL.md 要点

- description 草案（实施时本地计数，须 ≤400）：
  `Chinese thesis defense helper for existing XeLaTeX PhD or master thesis repositories: builds a Beamer pre-defense or defense deck with speaker notes and a fidelity gate, and drafts point-by-point responses to thesis review reports as paste-ready Markdown with a coverage and evidence gate. Not for .pptx, journal rebuttals, or English defenses.`
- SKILL.md 正文已有 13.3 KB；rebuttal 细节放 references，SKILL.md 只增加路由行、一段工作流（≤10 行）与必要的输入输出说明。
- 先前记忆：全局格式化 hook 会对齐 SKILL.md 表格，可能触发 `ROUTER_ROW_RE` 契约测试；改完立即运行入口测试与 `test_skill_contracts.py`。

## 4. references 写作要点

- `rebuttal-writing.md` 的规则来自父 `research/prior-art.md` §3：先总体说明再逐条；一条意见一条回复；回复首句写处理动作与具体内容，不只写「已修改」；
  修改位置写章节、图表号与页码，页码指修改稿；不采纳给学术理由，不以时间、经费为理由；感谢只在总体说明出现一次；遵守中文去 AI 腔规则（无「值得注意的是」等提示语）。
- 示例全部合成（虚构题目与数字），每则示例给出台账条目与渲染后的三段文本。
- `rebuttal-workflow.md` 写明：评阅人提出补实验而答辩前无法完成时，处理方式为 `future_work`，可在论文局限与展望中补充讨论并作为修改位置；不得写成已完成。
- 公开资源中出现的命令选项须与 `--help` 一致（父 design §8）。

## 5. 真实评阅书验收（AC9）

步骤：询问用户评阅书目录、论文仓库与是否接受写入同级目录 → intake → 记录等级、条数、锚点计数与 warnings →
不进行 LLM 拆分与 build（属于用户使用阶段，不属于本任务交付）→ 写 `research/acceptance-real-reviews.md`。
若用户希望顺带完成本轮修改说明，另行作为使用任务，不并入 C3。
