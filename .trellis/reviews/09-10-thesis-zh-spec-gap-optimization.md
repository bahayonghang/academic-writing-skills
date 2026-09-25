---
skill: trellis-plan-review
version: 0.5.0
task_dir: D:/Documents/Code/Agents/academic-writing-skills/.trellis/tasks/09-10-thesis-zh-spec-gap-optimization
task_name: 09-10-thesis-zh-spec-gap-optimization
task_status: planning
review_scope: task-tree
task_count: 4
task_members:
  - 09-10-thesis-zh-spec-gap-optimization
  - 09-10-thesis-zh-guidance-fidelity
  - 09-10-thesis-zh-consistency-semantics
  - 09-10-thesis-zh-compile-outdir
task_statuses:
  09-10-thesis-zh-spec-gap-optimization: planning
  09-10-thesis-zh-guidance-fidelity: planning
  09-10-thesis-zh-consistency-semantics: planning
  09-10-thesis-zh-compile-outdir: planning
verdict: 可执行
blocking: 0
should_fix: 0
notes: 0
generated_at: 2026-09-10T12:30:41Z
---

# Trellis 规划审阅报告

## 审阅范围

- 根任务：`09-10-thesis-zh-spec-gap-optimization`
- 模式：`task-tree`
- 任务数量：4
- 有序成员（根优先；顺序不代表依赖）：
  - `09-10-thesis-zh-spec-gap-optimization` — planning
  - `09-10-thesis-zh-guidance-fidelity` — planning
  - `09-10-thesis-zh-consistency-semantics` — planning
  - `09-10-thesis-zh-compile-outdir` — planning

审阅逐一读取四个成员的 task.json、prd.md、design.md、implement.md 和两份 JSONL。
核对范围包括 G1–G6 源码/指南证据、24 个 AC 的各项义务、真实调用路径、文件所有权、
执行顺序、验证命令和回滚边界。所有成员尚未开始，Pass 7 实现漂移不适用。
本文只允许交付规划质量结论，不构成实施授权。

下文以 P、C1、C2、C3 分别表示上述四个成员；任务证据均可在
`.trellis/tasks/<成员名>/` 下定位。

## 结论

可执行 — 阻断 0 / 应修 0 / 提示 0

最终版本没有发现必须返回规划的问题。三个交付物可以在当前文件边界内实施；
仍须由后续明确的实施请求授权，再遵循 Trellis 启动流程。
产品修复和效果验收尚未完成。

## 问题清单

无。

## 未能核实

- **新实现及新测试结果：UNVERIFIED。** 当前全部任务为 planning，新增三个测试文件和
  产品修复尚不存在；不能将需求/机制闭环视为 AC 已通过。
- **C1 八场景的 before/after 实际响应与独立核读：UNVERIFIED。** 本次核对了原生委派能力
  和不继承上下文的采样设计，没有执行后续实施阶段的输出采样。C1 design.md:44 明确
  保存两轮原始回答，design.md:52 明确缺原生能力时不得宣布 AC5 通过。
- **本轮真实 TeX 构建：UNVERIFIED。** 本次只运行内存/Mock 探针，没有运行 TeX。
  09-05 归档 implementation-check.md:33 的 outdir 历史记录已读取，但不升级为本轮验收。
  C3 design.md:46 的现成工具条件、临时目录及 wrapper smoke 必须在实施时履行或报告缺口。
- **105 项基线未由本审阅代理重复执行。** 已读取 P research/validation.md:3 的本轮主会话
  执行记录及精确命令；本审阅代理独立复跑的是 G4/G5/G6 探针。重复运行未变化的产品
  基线不能增加本次规划审阅的独立证明力。
- **外部候选的当前上游版本、人气、安全与实际写作效果未独立核实。** P
  reports/prior-art-research.md 已将这些项与本地文档可读性区分；本次没有外部操作。
- **五宿主 fresh session、provider A/B、人工盲评、跨学科准确率、真实学校 class、
  真实论文质量及印刷/视觉效果：missing evidence。** 任务明确排除这些效果承诺；
  静态资源检查、合成案例、Python 回归和目标 PDF 存在性不能代替这些证据。

## 可靠部分

### 机械预检与数量复算

在局部条款同步后重新运行：

```text
python -B -X utf8 <本会话已解析的 trellis-plan-review 技能目录>/scripts/plan_precheck.py .trellis/tasks/09-10-thesis-zh-spec-gap-optimization --include-descendants
```

结果为 exit 0，4 个 planning 成员、3 条父子边、无 legacy fallback、
无树完整性/占位符/引用阻塞；根报告目标被 Git 忽略。
没有运行 task.py start、finish 或 archive。

独立读取 P research/spec-inventory.json 并重算当前文件：
58 个 Markdown 文件、3,787 行，所有 SHA-256 与行数匹配；
16 份本库规范 + 3 份通用 guides + 三个参考目录各 13 份 = 58。
P research/spec-coverage.md 的适用性清单覆盖所有成员；
本审阅没有把主会话/参考审阅者的逐行阅读记录冒充为本审阅者重新逐行阅读全部参考项目。
当前 evals.json 为 47 条，trigger_eval.json 为 49 条，与 C1 前缀保留条件一致。

### G1–G6 的现行依据

| 缺口 | 现场证据与结论 |
| --- | --- |
| G1 | `academic-writing-skills/latex-thesis-zh/references/writing/writing-philosophy-zh.md:64` 和 :86 无给定数字却示范替入 3.2%/12.3%；`references/modules/logic.md:11` 至 :14 用孤立 95% 推出提升及长程依赖机制。C1 的条件化示例直接覆盖这些点。 |
| G2 | `academic-writing-skills/latex-thesis-zh/references/writing/over-claim-guard.md:14`、:41、:114 仍以方法标签作为强因果捷径，:48、:104、:121 以 hedge 保留未核实首次；`references/writing/results-analysis-guide-zh.md:219` 至 :239 明确区分组件贡献与因果归因。让措辞表回指既有证据规则可以消除冲突。 |
| G3 | `academic-writing-skills/latex-thesis-zh/references/writing/writing-philosophy-zh.md:92` 至 :110 的固定篇幅、逐篇综述及 GPU 条款，与 `references/writing/abstract-structure.md:94`、`references/modules/literature.md:54` 的适用边界不一致。C1 同时处理摘要上部旧表，并保留现有学校阈值。 |
| G4 | `academic-writing-skills/latex-thesis-zh/scripts/check_consistency.py:58`、:61、:70 混淆概念，:202 按频率取统一目标；`tests/skills/latex_thesis_zh/test_latex_thesis_zh_checker_precision.py:146` 固化错误正例。内存探针独立复跑仍得到统一成“深度学习”的错误建议。 |
| G5 | `academic-writing-skills/latex-thesis-zh/scripts/check_consistency.py:243` 的定义正则跨行，:276 不比较定义顺序，:290 把任意重复定义都报告。独立探针复现先用后定义 PASS、合法跨章重引 multiple_definitions 和章标题被吞入释义。 |
| G6 | `academic-writing-skills/latex-thesis-zh/scripts/compile.py:278`/ :290 转交 outdir，:330 却查源目录；:203 至 :242 的显式 compiler 不转交 outdir 且不检查 PDF 存在。独立 Mock 复现只有目标 PDF 返回 1、只有源目录旧 PDF 返回 0。 |

G4/G5/G6 的独立执行命令：

```text
python -B -X utf8 .trellis/tasks/09-10-thesis-zh-spec-gap-optimization/research/reproduce_probes.py
```

结果与 P research/probe-results.json 的五项观察一致。
探针只注入内存文本和 Mock 外部进程/存在性，没有创建论文文件或运行 TeX。

### 逐项 AC 追溯

表内按独立可观察义务展开，所有项均能回到要求与机制；这里只说明规划有验收办法。

| 成员 / AC | 已拆分的义务 | Requirement 与机制位置 |
| --- | --- | --- |
| P AC1 | 58 份覆盖；行数/散列；16+3+39 适用性分类 | R1；P design.md:16，research/spec-inventory.json，research/spec-coverage.md。已独立重算。 |
| P AC2 | C1 全部验收；旧冲突消除；8 类实际响应独立核读 | R2；P design.md:17；C1 design.md:34、:44、:54。 |
| P AC3 | C2 全部验收；不同概念、定义顺序、逐章重引反例 | R3；P design.md:18；C2 design.md:3、:17、:50。 |
| P AC4 | C3 全部验收；目录、退出码、支持组合调用真实 wrapper | R4；P design.md:19；C3 design.md:3、:19、:38。 |
| P AC5 | 源/双语/manifest；just ci；完整资源检查；docs build；逐类证据缺口 | R5；P design.md:28、:43；implement.md:14 至 :28 的独立门禁与记录。 |
| P AC6 | 仅列明文件；无新配置/依赖/路由/跨技能实现；保留用户改动；不外推运行/论文效果 | R6；P design.md:23、:40、:43、:51；各子文件所有权与精确逆向 diff。 |
| C1 AC1 | 无证据时不补数字/提升幅度/机制；强证据下保留范围内强结论 | R1；C1 design.md:4、:35、:36、:39、:54。 |
| C1 AC2 | 不等预算不获因果资格；组件贡献与区分性因果分开；未检索首次移除/待核 | R1；C1 design.md:4、:37、:38、:40。 |
| C1 AC3 | 学校要求控制博士摘要；非 GPU 工程/理论不补超参数/实验/GPU；主题综合保留多引 | R2；C1 design.md:9、:12、:41、:42。 |
| C1 AC4 | 段主题/章目标/证据/处置可定位；只审阅不改正文；仅 current 可建议改写 | R3；C1 design.md:14 至 :17 引用现有 P-ARC/S-CTX；现行 logic.md:137 明确只读窗口边界。 |
| C1 AC5 | 8 场景真实回答与逐项核读；expected/输入隔离；历史47/49前缀不重排 | R4；C1 design.md:34 至 :55；implement.md:6 至 :9；fork_turns="none" 明确阻止主线程答案污染。 |
| C1 AC6 | 双语/manifest；必要新锚点；静态/实际响应/论文证据分开 | R4；C1 design.md:19、:44、:60；implement.md:11、:16；父任务资源与构建门禁，已注入 docs-bilingual-resources 契约。 |
| C2 AC1 | 不合并三组不同概念；显式 custom-terms 真变体可报告 | R1/R4；C2 design.md:18 至 :20；implement.md:9 的 custom-terms 回归。 |
| C2 AC2 | 同行/多行先用后定义；include 前后顺序；后章不强制再定义；不吞前章标题 | R2；C2 design.md:3 至 :15、:23 至 :28；复用 assemble/origin 并按字符位置比较。 |
| C2 AC3 | 跨章重引/同章同义重复/正常全称缩写无语义冲突；不同释义可定位 NEEDS-LLM | R3；C2 design.md:21 至 :32；候选不冒充唯一规范全称，不自动判断中英等价。 |
| C2 AC4 | 目录/--all-files 文件内顺序；说明跨文件未核；默认 include 图排除草稿 | R2/R4；C2 design.md:11 至 :15；现行 check_consistency.py:343 的默认可达图入口及 implement.md:9。 |
| C2 AC5 | 真实 API/CLI；注释/引用键/停用词/一次性/定义后/多文件；替换错误旧正例 | R4；C2 design.md:31、:39 至 :45、:53；implement.md:5 至 :10、:19 至 :21。 |
| C2 AC6 | 公开脚本/人工边界；双语与门禁；默认变化声明 | R4；C2 design.md:40 至 :42、:54、:55；implement.md:11 至 :17；父任务 manifest owner。 |
| C3 AC1 | 相对/绝对/空格中文路径；默认/显式 recipe 与 xelatex/lualatex；命令和报告目标一致 | R1；C3 design.md:4 至 :11、:39 至 :42。 |
| C3 AC2 | 正常 latexmk exit0+目标；源目录旧 PDF 不替代；no-outdir 显式 compiler 缺 PDF 失败；非0+PDF失败 | R2；C3 design.md:12 至 :17、:41 至 :42。旧 no-outdir 假绿被明确列为修复，不再与有效流程保留混淆。 |
| C3 AC3 | 所有手动 recipe+outdir 在零 TeX/Bib subprocess 下拒绝；给现有支持路径；无新旗标/recipe | R3；C3 design.md:19 至 :25、:43。 |
| C3 AC4 | 无 outdir 有效编译；无需重建目标；手动 recipe；shell-escape；失败分支 | R4；C3 design.md:14、:23 至 :24、:44；compile.py:315 的 Bib 容错及 :439 的信任门保留。 |
| C3 AC5 | Mock 调用真实 wrapper；有工具则隔离真实 smoke；缺工具明确未验 | R4；C3 design.md:38 至 :49；implement.md:17 至 :21 的 wrapper 命令和无安装边界。 |
| C3 AC6 | 两份公开说明/双语；路径相对基准；支持/拒绝组合；成功边界；门禁 | R4；C3 design.md:3、:19、:29 至 :36、:52；implement.md:7 至 :9；父任务资源集成。 |

### 关键设计与执行边界

- **C2 首次作用域明确。** C2 design.md:7 定义装配全文首次，不为每章创建新状态；
  无入口只检查文件内顺序。字符位置解决同一行先用后定义，origin 提供源路径/行号。
  `tex_loader.py:171` 与 :132 的现有 API 能支撑方案；不需要修改 loader。
- **C2 全称提取保持候选边界。** C2 design.md:23 禁止跨换行、句末和结构命令；
  :25 对无法可靠界定的全称保留 NEEDS-LLM。同一个定义采集器服务 terms 和 abbreviations，
  避免当前两套定义正则分叉。:44 已允许同步旧 full_after_abbrev 风格断言，
  无需为通过存量测试保留“后文统一用缩写”的强制建议。
- **C3 成功规则与手动容错不冲突。** C3 design.md:12 只覆盖正常完成的 latexmk；
  :16 明确包括无 outdir 显式 compiler 的旧假绿；:24 保持既有手动 BibTeX/Biber 非0继续，
  :17 不扩展 watch 中断处理。mtime、新鲜度、排版与任意 latexmkrc/jobname 均未被暗中承诺。
- **C1 实际响应核读可执行。** 当前原生委派工具可用；C1 design.md:45 至 :52
  指定隔离输入、规则版本/散列、原始输出、独立 reviewer 及无能力时的失败边界。
  这足以组织本地输出审阅，没有建立新 runner、benchmark 平台或付费 provider 依赖。
- **所有权与顺序闭环。** P design.md:24 明确 C1→C2→C3→集成；C2/C3 共用 scripts
  测试文件时串行交接。C1 的源文件/evals 不与其余 child 竞争；父任务独占 manifest 和
  两份 maintainer spec，在 child 公开资源完成后串行刷新，使局部门禁可执行。
- **命令与实际文件相符。** 三份子任务 implement.md 中所有存量 pytest 路径存在；
  `test_thesis_zh_guidance_fidelity.py`、`test_consistency_semantics.py`、
  `test_compile_outdir.py` 明确为后续新增，未被当作现有通过证据。
  `justfile:63` 的 ci 顺序确为 check-versions、lint、typecheck、test；
  resource sync 和 docs build 是单独门禁。
- **改动最小且可回滚。** 任务不修改公共路由、共享 parser/loader、其他技能实现、
  学校阈值、版本或许可；公开规则仍随 skill 自包含。P design.md:54 与各子回滚条款
  只撤本任务精确 diff，禁止整文件覆盖 C2/C3 累积测试或复原用户其他改动。
  本审阅未编辑任务产物或产品源码，仅持久化这一份合并报告。

## 盲区

Agent 对 Agent 计划的审阅不等于独立第二意见；双方可能共享盲点。
零问题只表示本轮未发现缺陷，不能证明计划完整，也不能替代用户批准。

