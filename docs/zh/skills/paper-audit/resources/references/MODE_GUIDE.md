# 模式指南

每个的详细工作流程`paper-audit`模式。顶层`SKILL.md`保持
路由表；该文件保存每个模式的步骤、相位顺序和
委员会派遣规则。

接下来阅读：
- `references/PRESUBMISSION_GUIDE.md`为`PRESUBMISSION`模式集成层。
- `references/REVIEW_LANE_GUIDE.md`用于截面和横切审查通道定义。
- `references/SUBAGENT_TEMPLATES.md`用于审阅者任务模板。

## 输入分辨率

- 首先解析论文路径，并在解析时保留用户提供的相对路径
已经可以工作了。
- 从扩展名推断论文格式 (`.tex`, `.typ`, `.pdf`） 前
选择检查或解析器行为。
- 推断`report-style`来自请求：使用`peer-review`当用户询问时
用于期刊评论散文，例如摘要/主要问题/次要问题/
推荐;否则默认为`deep-review`.
- 首先从请求推断输出语言，然后再回到论文
当请求不明确时的语言。
- 为了`re-audit`， 要求`--previous-report PATH`。如果丢失，请停止
立即并仅询问该路径，而不是运行新的审核。
- 说明锁定模式、报告风格、焦点、语言和地点（如果已知）
在运行命令之前，当其中任何命令是推断的而不是显式的时
假如。

### 进气口自动检测

将这些条件作为提示向用户显示；从不自动切换模式
未经确认。目标是在之前捕获明显的模式不匹配
运行错误的工作流程。

- **以前的报告存在**：如果文件名为`*audit_report*`,
  `*review_report*`, `*final_issues*.json`，或匹配`--previous-report`
语义存在于论文目录或当前工作中
目录，询问用户是否想要`re-audit`模式。
- **论文中的修订标记**：如果来源包含
  `\latextrackchanges`, `changes`包宏，`track-changes`,
  `changeBars`, `\added{`, `\deleted{`, `\replaced{`, `<changes>`，或一个
  `Revision History`部分，询问这是否是修订后的提交，以及
无论`re-audit`是有意的。
- **长纸上的抛光模式**：如果模式为`polish`但论文超过
30页或25k字，询问是否`deep-review`之前比较合适
进行中。
- **检测到审稿人字母**：如果输入或工作目录包含
审阅者字母形状的文件（标记：`Reviewer 1`, `R1:`, `审稿人 1`,
  `Editor's Comments`, `Decision Letter`）， 派遣
  `agents/revision_coach_agent.md`首先将其解析为结构化的
路线图，然后将路线图输入`re-audit`.

始终以简单语言呈现检测到的信号（“发现
`final_issues.old.json`在论文旁边——这看起来像是重新审核”）和
让用户确认或拒绝。

## 演示面

- `deep-review`：制作问题包、修订路线图和工件路径
主要摘要表面。提及模式级字段是可以接受的
例如此处的审查通道或来源。
- `peer-review`：使审稿人的散文成为主要的总结面。请勿暴露
原始内部键，例如`review_lane`, `source_kind`， 或者`root_cause_key`在
顶级散文摘要；将它们保留在工件包中。
- `gate`：首先显示结论，然后是 EIC 筛选，然后是阻止者，然后是建议
建议。
- `re-audit`：显示状态桶（`FULLY_ADDRESSED`, `PARTIALLY_ADDRESSED`,
  `NOT_ADDRESSED`, `NEW`）在任何新的审计评论之前。

## 通用步骤0

解析`$ARGUMENTS`，锁定走纸路径，如果用户这样做则推断模式
不提供之一。如果必须的话，请在运行命令之前说明推断的模式
推断它。

## `quick-audit`

1. 跑步：
   ```bash
   uv run python -B "$SKILL_DIR/scripts/audit.py" <paper> --mode quick-audit ...
   ```
2. 提交一份简明的报告：
   - `Submission Blockers`第一的
   - 然后`Quality Improvements`
   - 然后检查清单项目
   - 大喊`PRESUBMISSION`当重要时，将机械结果分开
   - 将快速审核结果标记为`[Script]`出处
3. 如果用户在快速筛选后明确希望审阅者进行深度批评，
升级到`deep-review`.

## `deep-review`

将此用作默认审阅者样式路径。

如果用户明确想要提交式审阅者报告（例如：
《SCI审稿人》、《期刊审稿报告》、《综述/重大问题/次要问题》
问题/建议”或“审稿报告”），保留相同的深度审查证据
管道但使`peer_review_report.md`组合中的**主视图**
CLI 摘要，同时保留`review_report.md`作为更丰富的证据包。在
这条路径，将原始模式字段保留在工件中，而不是
面向审稿人的散文。

### 第 1 阶段：准备工作区

```bash
uv run python -B "$SKILL_DIR/scripts/prepare_review_workspace.py" <paper> --output-dir ./review_results
```

这将创建：

- `artifacts/meta/full_text.md`
- `artifacts/meta/metadata.json`
- `artifacts/data/section_index.json`
- `artifacts/data/claim_map.json`
- `artifacts/summary/paper_summary.md`
- `artifacts/sections/*.md`
- `artifacts/comments/`
- `artifacts/references/`（审阅代理的最少副本）
- `artifacts/committee/`（委员会评审员工件）

### 第2阶段：第0阶段自动审核

```bash
uv run python -B "$SKILL_DIR/scripts/audit.py" <paper> --mode deep-review ...
```

将此视为**仅限阶段 0**。它提供脚本支持的上下文和分数，
不是最终的审查。`PRESUBMISSION`调查结果留在这里以供重点关注
理论/文献/方法论/逻辑评论；只有完整/编辑深度审查才能
促进高信号机械发现`pre_submission_readiness`
审查通道（见`PRESUBMISSION_GUIDE.md`).

### 阶段3A：学术预审委员会（默认）

决定委员会重点：
- 如果`--focus ...`已提供，请使用它。
- 否则，使用下面的关键字图从用户请求中推断。
- 如果没有匹配，则默认为`full`（所有五个角色）。

派遣委员会评审员（按照这个确切的顺序）并让他们写
将工件放入工作区：

1. `agents/committee_editor_agent.md`
   - 写：`committee/editor.md`
   - 写：`comments/committee_editor.json`
2. `agents/committee_theory_agent.md`
   - 写：`committee/theory.md`
   - 写：`comments/committee_theory.json`
3. `agents/committee_literature_agent.md`
   - 写：`committee/literature.md`
   - 写：`comments/committee_literature.json`
4. `agents/committee_methodology_agent.md`
   - 写：`committee/methodology.md`
   - 写：`comments/committee_methodology.json`
5. `agents/committee_logic_agent.md`
   - 写：`committee/logic.md`
   - 写：`comments/committee_logic.json`

如果子代理不可用，请在线运行委员会审阅者，但保留
相同的文件输出。

然后写：`committee/consensus.md`
- 包括：总分（1-10）、优先顺序以及最重要的 3 个问题
首先修复
- 评分公式：
  - 9.0 开始
  - 减去：`1.5 * (# major) + 0.7 * (# moderate) + 0.2 * (# minor)`
  - 下限为 1.0
  - 如果编辑判定为 Desk Reject，则上限为 4.0

`render_deep_review_report.py`自动嵌入`committee/*.md`进入
`review_report.md`当存在时。

### 阶段 3B：分区和横切审查通道（覆盖范围）

读：

- `references/SUBAGENT_TEMPLATES.md`
- `references/REVIEW_LANE_GUIDE.md`

然后分派审阅者任务：

- 分段审查通道
  - 简介/相关工作
  - 方法
  - 结果
  - 讨论/结论
  - 附录（如果有）
- 交叉审查通道
  - 主张与证据
  - 符号和数字的一致性
  - 评估的公平性和可重复性
  - 自我标准一致​​性
  - 现有技术和新颖性基础
  - 提交前准备（完全/仅限编辑重点）
  - 中文学位论文评阅（`zh_thesis_review`；仅 `lang == "zh"` 且 full/editor 焦点）


每个通道写入一个 JSON 数组到`comments/`.

如果子代理不可用，请使用内置的确定性后备通道
传入`scripts/audit.py`因此工作流程仍然写入与通道兼容的 JSON
进入`comments/`合并前。

### 第四阶段：整合

```bash
uv run python -B "$SKILL_DIR/scripts/consolidate_review_findings.py" <review_dir>
uv run python -B "$SKILL_DIR/scripts/verify_quotes.py" <review_dir> --write-back
uv run python -B "$SKILL_DIR/scripts/render_deep_review_report.py" <review_dir>
```

合并规则：

- 合并精确的重复项
- 将不同的论文级结果分开，即使它们共享一个根
原因
- 保留单一结果，除非明显误报
- 分配`comment_type`, `severity`, `confidence`， 和`root_cause_key`

### 第五阶段：呈现结果

总结：

- 1小段总体评价
- 主要/中等/次要问题的计数
- 3 个最高优先级的修订项目
- 识别选择的**主视图**`--report-style`
- 路径到`review_report.md`, `revision_suggestions.md`（根），和
  `artifacts/data/final_issues.json` / `artifacts/summary/peer_review_report.md`

## `gate`

1. 跑步：
   ```bash
   uv run python -B "$SKILL_DIR/scripts/audit.py" <paper> --mode gate ...
   ```
2. **EIC 筛选**（第 0.5 阶段）：阅读`agents/editor_in_chief_agent.md`和
对论文标题进行主编直接拒稿筛选，
摘要和引言。这评估球场质量、投稿场所适配度、致命性
缺陷和演示基线。直接拒稿判决是一个障碍。
3. 报告通过/失败。
4. 首先呈现 EIC 筛选结果（结论 + 分数 + 理由）。
5. 接下来列出阻止者。
6. 将建议性项目与阻碍性项目分开。
7. 保持`PRESUBMISSION`主要/次要项目咨询；仅关键机械
调查结果可以堵住大门。
8. 对于 IEEE 伪代码检查，明确哪些问题是强制性的，
这些只是 IEEE 安全的建议。

## 恢复协议

深度评论写了一个`checkpoint.json`在工作区根目录下，这样一个会话
被中断（代币预算、代理超时、用户`Ctrl-C`) 可以在哪里接载
它停止了而不是重新开始第一阶段。

### 文件

- `<review_dir>/checkpoint.json`— 模式定义于`scripts/checkpoint.py`.
- 状态生命周期：`prepared` -> `in_progress` -> `suspended` -> `completed`.
- 阶段列表反映了阶段 1-5：`prepare`, `phase0_audit`, `committee`,
  `lanes`, `consolidation`, `present`.

### 阅读

- `scripts/audit.py --review-dir <review_dir>`印刷
  `[checkpoint] status=... lanes_completed=N lanes_suspended=M`发射时
在运行阶段 0 之前。当用户输入“继续”/“继续”时，处理
中的任何条目`completed_lanes`正如已经完成的那样，仅发送
其余的`lanes` / `committee`代理。

### 更新中

当派遣审查通道或委员会代理人时，指示其致电
`checkpoint.mark_lane_completed(<review_dir>, <lane_name>)`（或者
`mark_lane_suspended`部分失败）。阶段 3B 审查通道模板应使用
这`review_lane`值（例如`claims_vs_evidence`,
`notation_and_numeric_consistency`) 作为审查通道标识符，因此合并
可以关联。

### 重置

- `scripts/audit.py --review-dir <review_dir> --no-resume`来电
  `checkpoint.reset_checkpoint`，将检查点恢复到初始状态
  `prepared`状态而不删除任何工作区工件。当
用户明确要求干净地重新运行。

### 工作空间边界

检查站只存在于里面`<review_dir>/`。审计工具不
触摸用户的工作目录并且不删除其中的其他文件
工作区。恢复是非破坏性的。

## `re-audit`

1. 需要`--previous-report PATH`.
2. 跑步：
   ```bash
   uv run python -B "$SKILL_DIR/scripts/audit.py" <paper> --mode re-audit --previous-report <path> ...
   ```
3. 如果新旧都`final_issues.json`捆绑包可用，也可以运行：
   ```bash
   uv run python -B "$SKILL_DIR/scripts/diff_review_issues.py" <old_final_issues.json> <new_final_issues.json>
   ```
4. 展示：
   - 根本原因感知状态标签：`FULLY_ADDRESSED`, `PARTIALLY_ADDRESSED`,
     `NOT_ADDRESSED`, `NEW`
   - 在可用时使用结构化的先前发行捆绑包，但仍然接受
Markdown 之前的报告

## `polish`

1. 运行审核预检查：
   ```bash
   uv run python -B "$SKILL_DIR/scripts/audit.py" <paper> --mode polish ...
   ```
2. 如果存在拦截者，请停止并报告。
3. 仅在预检查安全的情况下才进行抛光。

## 委员会焦点路由（深入审查）

为了`deep-review`，默认使用**学术预审委员会**。这
是一个 5 角色审核通行证：

1. 编辑器（直接拒稿屏幕）
2. 审稿人1（理论贡献）
3. 审稿人3（文献对话/差距）
4. 审稿人 2（方法透明度）
5. 审稿人4（逻辑链）

如果用户请求单个维度，则仅运行匹配委员会
角色。

文学焦点意味着：
- 验证文献是否是主题综合的或仅仅是
列举的
- 验证矛盾是否得到承认而不是平息
- 验证所声称的间隙是否是真实的而不是由制造商制造的
选择性引用
- **不要**重写相关工作的散文；将其交给
需要时特定于格式的写作技巧

如果`--focus ...`提供后，它会覆盖关键字推断：

- `--focus full`（默认）
- `--focus editor|theory|literature|methodology|logic`

### 关键词图（英文+中文）

|重点|关键词|
|---|---|
|编辑|"desk拒绝", "预筛", "编辑", "EIC", "主编", "预筛", "初筛"|
|理论|"理论", "贡献", "新颖性", "理论对话", "理论", "贡献", "创新性"|
|文学|"相关工作", "文学", "研究差距", "引用", "文献", "综述", "研究差距", "引用", "差距是假的", "引用引用"|
|方法论|"方法", "样本", "编码", "数据", "设计", "SRQR", "方法", "样本", "编码", "数据", "研究设计", "透明度"|
|逻辑|"logic", "argument", "causal", "structural", "运算", "计算器", "逻辑", "结构"|

输出语言：匹配用户请求的语言。如果有歧义，请匹配
纸质语言。
