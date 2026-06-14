# 优化 latex-thesis-zh 章节标题结构指导

## Goal

优化 `academic-writing-skills/latex-thesis-zh` 对中文学位论文“大标题/小标题”问题的识别与修改指导，使 skill 能针对既有 LaTeX 论文工程审阅：

- 章标题是否体现“研究对象 + 问题/任务 + 方法/路径”。
- 每章直属小节数是否过多，默认建议最多 5 节。
- 小节标题是否扣合章标题，而不是泛泛使用“模型建立”“实验分析”“结果讨论”等孤立标题。
- 标题诊断是否能落到真实 `.tex` 源文件与行号，并给出不破坏 LaTeX 引用、标签、公式和模板命令的重命名建议。

## User Value

当前用户的论文问题不是单纯排版错误，而是学位论文的章节组织和论证主线问题。优化后，`latex-thesis-zh` 应能从章节标题本身判断“大论文结构是否像博士/硕士学位论文”，并输出可执行的调整方案，帮助用户把“章节堆叠”改成“对象、问题、方法递进”的目录结构。

## Confirmed Facts

- 用户明确要求结合 `$skill-creator` 创建完整 Trellis 优化任务，而不是立即实现。
- 用户指出的核心约束包括：
  - 大章节的小标题数目太多，应限制到最多 5 节。
  - 大标题和小标题题目都不对。
  - 大标题需要体现“对象、问题、方法”。
  - 小标题必须和上面的章标题扣合。
- 已阅读 `skill-creator`：后续实施不能只改提示词，必须包含 eval 用例、旧版/新版或适配后的对比、人审 viewer、反馈迭代与描述优化评估。
- `latex-thesis-zh` 已有 `title`、`structure`、`logic` 模块；已有逻辑检查覆盖标题后导语、章引言、绪论漏斗、章节主线闭合，但尚未把“章标题对象-问题-方法”和“每章小节最多 5 节”作为明确 contract。
- 当前 `academic-writing-skills/latex-thesis-zh/evals/evals.json` 有标题和结构相关用例，但缺少“章标题/小节标题结构架构”专项 eval。
- 两篇参考中文博士论文目录已抽取为 research 证据：
  - `复杂非平稳工业过程异常监测与诊断_张志鹏_学位论文.pdf`
  - `水泥粉磨过程关键指标预测模型与运行优化算法研究.pdf`

## Requirements

1. Skill 行为
   - 当用户提到“大标题”“小标题”“章标题”“小节标题”“目录结构”“章节标题不扣题”“小节太多”等请求时，`latex-thesis-zh` 应路由到标题/结构相关检查，而不是只做普通润色。
   - 输出必须区分“诊断”和“建议改名/合并方案”，避免直接改源文件。
   - 默认保留 `\cite{}`、`\ref{}`、`\label{}`、数学环境、参考文献键和模板宏命令。

2. 章节标题规则
   - 主体方法/应用章标题应尽量包含或可推断出：
     - 研究对象，例如“非平稳工业过程”“水泥粉磨过程”“比表面积”“单位电耗”。
     - 问题/任务，例如“异常监测”“根因诊断”“关键指标预测”“运行优化”。
     - 方法/路径，例如“自适应方法”“异构数据融合模型”“多步优化算法”。
   - 绪论、结论、参考文献、致谢、附录等惯例标题不强制套用对象-问题-方法。

3. 小节结构规则
   - 每章直属 `\section` 默认最多 5 节；超过时应输出 P1/P2 级结构风险，并建议合并策略。
   - 小节标题应围绕章标题展开，优先形成“引言/问题描述/模型或算法/实验或应用/本章小结”的闭环。
   - 泛化小节标题可以保留，但必须能通过上下文扣合章标题；否则应给出带章标题关键词的改名建议。

4. 参考资料与文档
   - 更新 skill 内部参考文件，并同步 docs 英文路径与 docs/zh 路径的镜像内容。
   - 参考论文目录证据必须保存在本任务 `research/` 中，作为后续实现依据。

5. 可测性
   - 添加或更新 pytest 回归测试，覆盖：
     - 过多直属小节被检出。
     - 主体章标题缺少对象/问题/方法任一维度时被检出。
     - 小节标题与章标题脱节时被检出。
     - 绪论/结论等惯例标题不被误报为必须对象-问题-方法。
   - 添加或更新 `evals/evals.json` 中的真实用户式评测 prompt，并绑定 fixture 或临时测试论文。
   - 添加或更新 `trigger_eval.json`，覆盖“标题结构专项”正例和邻近负例。

6. Skill-creator 评测循环
   - 实施前快照旧版 skill。
   - 按 `skill-creator` 要求创建/更新 evals JSON 和 eval metadata。
   - 尽量执行 with-skill vs old-skill/baseline 对比；若当前 Codex 环境缺少独立子代理，采用 skill-creator 的 inline fallback，但仍要保存输出。
   - 生成断言、grading/benchmark，并使用 `C:\Users\lyh\.skillsmanage\skills\skill-creator\eval-viewer\generate_review.py` 生成人审页面；无浏览器环境时使用 `--static`。
   - 根据人审反馈进行至少一轮修订或明确记录无需修订的理由。

## Acceptance Criteria

- [ ] `latex-thesis-zh` 能对“章标题/小节标题结构”请求给出明确路由和输出契约。
- [ ] 标题结构规则覆盖对象-问题-方法、每章最多 5 个直属小节、小节扣合章标题三类问题。
- [ ] 参考文件和 docs 镜像保持一致，无孤儿 reference 文件。
- [ ] `evals/evals.json` 至少新增 1 个标题结构专项用例，且断言能区分本次改动是否生效。
- [ ] `trigger_eval.json` 包含标题结构专项正例和邻近负例，仍通过触发语料健康测试。
- [ ] pytest 至少覆盖 `tests/test_latex_thesis_zh_scripts.py`、`tests/test_latex_thesis_zh_coverage.py`、`tests/test_skill_contracts.py`、`tests/test_trigger_evals.py` 中与本任务相关的门禁。
- [ ] 运行 `skill-creator` 评测工作流，生成可供用户审阅的 review artifact，并将路径记录在任务或最终汇报中。
- [ ] 不启动实现前，`prd.md`、`design.md`、`implement.md` 和 `research/` 均已完成并经用户确认。

## Out Of Scope

- 不直接修改用户个人 thesis 仓库中的 `.tex` 正文。
- 不新增外部文献或手工改写 `ref.bib`。
- 不从零生成学位论文目录。
- 不将英文会议论文 section-writing 模型直接照搬为中文学位论文结构规则。
- 不把所有标题问题强制自动改源文件；本任务以诊断和建议为主。

## Open Questions

- 后续实施时，是否允许 `optimize_title.py` 增加新 CLI 参数（推荐：允许增加 `--headings` 或等价参数），还是只通过现有 `logic` 检查输出标题结构诊断。

推荐答案：允许在 `title` 模块中增加标题结构专项参数，并让 SKILL.md 路由“大标题/小标题”请求时串联 `title` 与 `structure`。这样职责清晰，且不会把标题命名问题混入普通逻辑衔接检查。
