# design.md — latex-thesis-zh 绪论优化技术设计

## 设计原则

1. **不新增 Module Router 行**：五项能力全部挂载到现有 `literature` 与 `logic` 两个模块，避免 SKILL.md 路由表改动触发 contract 锁与 trigger 评测成本。
2. **脚本管量化、LLM 管判断**：数量/占比/堆引/名词短语等可确定性计算的走 `[Script]`；主线连贯、比较句质量、图表设计建议走 `[LLM]`（读 references 后给提案）。
3. **细节下沉 references**：SKILL.md 仅在 literature/logic 行的 Use when 里补触发词（"绪论引用不足""研究现状扎堆"），正文不加新段。

## 改动清单

### 脚本（academic-writing-skills/latex-thesis-zh/scripts/）

**analyze_literature.py** — 新增绪论引用诊断（R1/R2）：

- 新 flag：`--intro-citations [--bib PATH] [--min N] [--max N]`（默认 min=120, max=160，博士档；硕士档降半）。
- 检查项（沿用现有 A1~A3 编号续排）：
  - `A4 citation-count`：绪论范围唯一键计数，低于 min 报 Major，位于区间报 Info。
  - `A5 stacked-citation`：单个 `\cite` ≥3 键定位（Info/Minor，提示拆为比较分述）。
  - `A6 author-clustering`：键名作者前缀归一（小写去年份），同前缀 ≥3 键且集中出现在同一段落 → Minor，点名前缀与行号。
  - `A7 year-distribution`（需 `--bib`）：解析 year 字段（复用 verify_bib.py 已有的 bib 解析函数，如不可直接 import 则提取最小解析逻辑），报告近三年/近五年占比 vs 阈值；无 `--bib` 时输出一条 Info 提示，不报错。
  - `A8 visual-summary`：综述 section 内无 `\ref{tab:...}`/`\ref{fig:...}` 指向对比表/演进图，或有图表但小节末尾缺"总-分-总"收束段 → Minor。
- 键→作者前缀归一规则：`^([a-zA-Z]+?)(?=[A-Z0-9])`，中文拼音键（如 `ChaiTianYou...`）取前两个大写驼峰段；写成独立函数便于测试。

**analyze_logic.py** — 新增绪论主线检查（R4/R5）：

- 新 flag：`--intro-mainline`。
- 检查项：
  - `L-SCI science-problem-form`：定位"科学问题"表格列/枚举环境，判别每项是否为纯名词短语（无谓语动词、无对象限定、无方法要素 → Major）。启发式：项文本 <15 字且不含"针对/研究/如何/能否/拟"任一 → 命中。
  - `L-MAP four-way-closure`：抽取创新点数、科学问题数、研究内容条数、章节安排章数，数目或关键词映射断裂 → Major（如 4 创新点 vs 5 研究内容且无"工程验证"声明）。
  - `L-FUN funnel-first-para`：绪论首段是否含领域词→瓶颈词→"本文/本章"三层推进（缺层 → Minor）。
  - `L-DOM domestic-foreign`：标题含"国内外"但正文未出现国内/国外分述标记，且无按主题混排的显式声明 → Info。

### references/

- **新文件 `references/writing/introduction-guide-zh.md`**（绪论专章，约 200~300 行）：
  - 六节漏斗骨架 + 各节字数配比（绪论总量 ≈1 万字 / ≤20 页）。
  - 引用配额表：总量 120~160+、近三年 ≥30%、近五年 ≥50%、外文 ≥1/2，每阈值注出处并标"以本校规范为准"。
  - 选文配比策略（每主题簇：奠基 1~2 + 近三年 2~3 + 中外均衡；同一团队多篇拆开比较着写）。
  - 研究演进时间线图规范（年代轴、阶段分期命名、代表文献锚点）与文献对比矩阵模板（方法/假设/适用范围/局限四列）。
  - 科学问题三要素句式模板 + 科学问题/技术问题/工程任务判别表 + 正反例（反例直接用 fixture 的名词短语形态）。
  - 四方闭合清单（创新点↔科学问题↔研究内容↔章节）。
- **`references/modules/literature.md`**：追加 A4~A8 检查说明与新 flag 用法。
- **`references/modules/logic.md`**：追加 `--intro-mainline` 检查说明。
- **`references/writing/thesis-writing-guide.md`**：绪论节末尾加一行指针到 introduction-guide-zh.md，不搬内容。

### SKILL.md

- literature 行 Use when 追加"绪论引用数量/年份分布/扎堆"；logic 行追加"科学问题三要素/绪论主线"。Reference Map 加 introduction-guide-zh.md 一行。last_updated 改 2026-07-10，version 不动。

### tests/

- `tests/skills/latex_thesis_zh/`（或现有 zh 测试目录）新增：
  - `test_intro_citations.py`：合成 fixture（脱敏 chapter1 等价样本，~40 行 tex + 迷你 bib）覆盖 A4~A8 各一正一反。
  - `test_intro_mainline.py`：覆盖 L-SCI 表格/枚举双形态、L-MAP 断裂、L-FUN、L-DOM。
- 键前缀归一函数单测（拼音驼峰键、英文键、数字年份键）。

### evals/

- 追加 1 条绪论诊断 eval case（走 Bash python 写入，避免 JSON hook 压平）。

## 关键取舍

- **不做**：自动改写绪论 prose（保持 literature 模块"默认只给诊断与蓝图"的既有契约）；自动生成演进图（只给规范与 TikZ/表格骨架建议）；联网补文献（安全边界禁止未确认外发）。
- **年份解析放 analyze_literature 而非 verify_bib**：verify_bib 的职责是条目合规（GB/T 7714），分布统计是综述质量问题，归 literature。
- **fixture 脱敏**：问题模式保留（121 键规模可缩样为少量键 + 等比例阈值注入测试参数），内容替换为通用领域词，绝不提交用户论文原文。

## 兼容与回滚

- 新检查全部藏在新 flag 后，默认行为零变化 → 存量用户无感。
- 每个脚本改动独立 commit（literature / logic / references / tests / evals），可单独 revert。
