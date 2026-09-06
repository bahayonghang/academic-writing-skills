# 设计

## 改动面

单文件：`academic-writing-skills/paper-audit/references/MODE_GUIDE.md`。
附带 `docs/resource-manifest.json` 一条 sha256 与
`docs/skills/paper-audit/resources/references/MODE_GUIDE.md`、
`docs/zh/skills/paper-audit/resources/references/MODE_GUIDE.md` 两份镜像。

## 机制

在 `### Auto-Detection at Intake` 小节标题之后、四条 bullet 之前插入门控前言，
替换现有的 "Surface these conditions to the user as a prompt" 无条件表述：

- 模式由用户显式给出 → 检测信号只作一句陈述，直接按指定模式执行。
- 模式由推断得出 → 保持现有提问行为。
- 无论哪种，检测到实质冲突 → 提问。

四条 bullet 各自补一个已指定模式下的处理句，不删除现有措辞主干。
`revision_coach_agent` 一条保持 dispatch 字面：审稿信输入会改变审查范围
（引入 reviewer 意见作为对比基线），按实质冲突定义本就应提问，与既有测试一致。

收尾句 `MODE_GUIDE.md:53-56` 从"present … and let the user confirm or decline"
改为两分支：陈述式呈现（已指定模式且无实质冲突）与确认式呈现（其余）。

`MODE_GUIDE.md:24-26` 的 re-audit 段落改为三分支：
在论文目录与当前工作目录按现有 `*audit_report*` / `*review_report*` /
`*final_issues*.json` 模式查找；恰好一个候选则陈述路径并继续；
零个或多于一个则停下只问该路径。停下询问这一行为本身不删除。

## 实质冲突的判据

只有两类升级为提问：

- 改变审查范围：需要纳入或排除章节，或引入新的对比基线（前次报告、审稿信）。
- 改变结论：会改变 gate 的 PASS/FAIL 判定，或会改变已产出 issue 的严重度。

不属于实质冲突的例子：目录里有旧报告但用户要的是全新 quick-audit——
旧报告不进入本次比对，范围与结论都不变，因此只陈述不提问。

属于实质冲突的例子：用户指定 `quick-audit`，但目录中存在审稿信文件——
审稿意见会改变本次要覆盖的范围，因此提问。

## 泛化边界

升级为规则：已由用户显式解决的决策不重新提问。
保留为条件指引：四类检测的具体文件名模式与标记串、30 页 / 25k 词阈值。
拒绝：不把"少提问"扩展到覆盖既有工作区或 `--previous-report` 零/多候选场景。

## 验收分层

`pytest` 与 `check_resource_sync.py` 只证明形状与同步。
AC3、AC4 是 LLM 行为验收，须保存实际响应并逐项审阅；
关键字匹配不能替代。真实论文场景验证本轮不做，写 missing evidence。

## 回退

只回退 `MODE_GUIDE.md`、其两份镜像与 manifest 中该条 sha256 的确切 diff。
