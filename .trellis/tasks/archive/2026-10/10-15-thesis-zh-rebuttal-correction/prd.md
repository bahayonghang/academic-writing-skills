# 纠正中文学位论文评阅回复能力归属

## Goal

将中文学位论文评阅意见回复能力完整迁入 `latex-thesis-zh`，使 `latex-defense-zh` 恢复为中文 Beamer 答辩稿技能。保留现有回复能力与事实保护，修正安装、路由、文档和测试归属。

## Background

- 用户明确要求创建任务并纠正归属；消息中的 `atex-defense-zh` 按上下文理解为 `latex-defense-zh`。
- 当前 `dev` / `5851407`，创建任务前工作树干净；误放来自 `791f4fd`、`b5c47d3`、`340cc70`，合计 39 个文件；功能前基线为 `53c2ab5`。
- 旧任务树位于 `.trellis/tasks/archive/2026-10/10-15-defense-zh-rebuttal*`，保持历史原样。
- `rebuttal_common.py:26` 依赖 `extract_thesis`，`rebuttal_check.py:37` 依赖 `check_deck`；直接搬目录不能保证独立安装。
- 现有能力为三条 CLI、四个 Python 文件与 16 个 R-* 码。以当前实现及 defense-rebuttal-contract 为准，旧 PRD 不替代当前实现证据。

## Requirements

- R1 仅撤销三笔误放功能提交对 defense 的扩展，保留原五模块和之前的 include 边界修复；defense 包恢复至 `53c2ab5` 内容。
- R2 回复脚本、三份 reference、一份 example、合成 fixture、eval 与回归测试迁至 thesis；保留 CLI 参数、退出码、台账 schema、输出结构、R-* 语义与现有台账兼容。
- R3 thesis 接管评阅书整理、逐条回复、修改说明、修改审查表；Beamer 继续归 defense；期刊/会议 rebuttal 与 paper-audit 评分不纳入。仅有评阅书时允许 intake，论文相关检查如实 skipped。
- R4 回复模块只读论文与评阅书，仅写用户指定的 responses/workspace；实际正文修改仍遵循 thesis 既有模块与授权边界。保留学术事实、手改覆盖、git/aux 证据及隐私保护。
- R5 按 qiaomu-meta-skill 做现有 Production 包的有界迁移：精简根入口、详细 reference、确定性脚本、触发边界和独立安装证据；保留现有技能名、作者、许可与 6.0.0 版本。
- R6 更新 README/usage 双语、两技能首页、双语资源、manifest 与相关 spec，新增纠错变更说明；不改写历史任务与日志。

## Acceptance Criteria

- [x] AC1 defense 包相对 `53c2ab5` 无内容差异；原五模块入口和回归测试通过。
- [x] AC2 单独复制 thesis 包，在无仓库 PYTHONPATH 的隔离目录运行 intake → build → check；无 defense 脚本或 fixture 依赖。
- [x] AC3 原回复测试迁移并保持覆盖，16 个 R-*、只读输入、覆盖保护、git 证据、aux 页码和跳过边界通过；新增隔离安装与归属测试。
- [x] AC4 thesis 包含评阅回复/修改说明/修改审查表正例与 Beamer/期刊回复/评分排除例；defense 不再声明回复能力。静态 trigger 不冒充真实模型触发证据。
- [x] AC5 双语资源检查、just ci 四步、just doc-build、git diff --check 通过；当前公开资源无错误归属的回复命令/链接。
- [x] AC6 交付 qiaomu handoff 与本次证据；真实评阅书、五工具和 provider 未执行时保持 NOT_RUN/UNVERIFIED，旧验收不冒充迁移后验证。

## Out of Scope

不新增回复算法、OCR、DOCX 输出、联网检索、自动论文修改或质量阈值变化；不修改公共 parser/loader；不重建旧任务树，不改写历史提交、归档任务、journal；不提交、推送、发布或操作真实论文。

## Planning Status

用户已于 2026-10-15 批准最终计划，task.py start 成功。实施与本地验收完成，AC1–AC6 满足；任务保持 in_progress，尚未提交或归档。完整证据与限制见 reports/check-results.md 和 reports/creation-handoff.md。
