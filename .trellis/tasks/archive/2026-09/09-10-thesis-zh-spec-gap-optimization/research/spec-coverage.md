# 全量 spec 阅读覆盖

- 日期：2026-09-10；基线 HEAD：`dd9f1e2`，分支 `dev`。
- 范围：58 个文件，共 3,787 行；递归枚举含隐藏文件，不依赖 Git 已跟踪状态。
- 主会话逐行读取本库 16 份契约和 3 份 guides；独立 spec_catalog_review 逐行读取三个参考目录的 39 份文件（1,256 行）。首次输出截断处已补读。
- 全部 47 个唯一 `ref/...` 引用路径存在；路径存在只证明可读取，不证明参考项目测试或运行有效。
- 当前 spec 包含本库开发契约、参考项目维护规范与通用思考指南。不存在可直接将其全部升级成中文论文强制规则的依据。
- 原始文件 SHA-256 与行数保存在 `spec-inventory.json`；本轮不修改 spec。

| 文件 | 行数 | 适用性与处理 |
| --- | ---: | --- |
| `.trellis/spec/academic-writing-skills/cover-letter-contracts.md` | 70 | 其他技能专属；保留位置/事实与规范真相源的原则，不迁移投稿信协议。 |
| `.trellis/spec/academic-writing-skills/deai-pattern-cluster-contract.md` | 88 | 直接适用；沿用 LLM-only、保真复核、正反例与标点单一规则源；不扩充词表。 |
| `.trellis/spec/academic-writing-skills/defensive-ai-rhetoric-contract.md` | 84 | 直接适用；校准具体解释的证据，不能以 hedge 或实验标签代替依据。 |
| `.trellis/spec/academic-writing-skills/docs-bilingual-resources.md` | 110 | 三子任务公开资源及父任务集成门禁；源、双语页面、manifest 与 fragment 必须一致。 |
| `.trellis/spec/academic-writing-skills/harness-workflow-contract.md` | 257 | 证据分类、UTF-8、真实 CLI 及本库写回位置适用；五工具运行验收不属本轮。 |
| `.trellis/spec/academic-writing-skills/index.md` | 29 | 本库契约索引；明确其他三个目录是参考项目；部分旧测试路径须以 tests/contracts 实物为准。 |
| `.trellis/spec/academic-writing-skills/method-narrative-contract.md` | 173 | 已有 M-*、接口表和方法门控；保持现状，不重复建方法分析能力。 |
| `.trellis/spec/academic-writing-skills/paper-audit-boundary-contracts.md` | 103 | paper-audit 专属；本轮不改评分、issue schema 或文献搜索链。 |
| `.trellis/spec/academic-writing-skills/paragraph-arc-audit-contract.md` | 94 | 审稿端专属；继承不以过渡词判断逻辑的原则，不改评分。 |
| `.trellis/spec/academic-writing-skills/paragraph-arc-contract.md` | 79 | 已有 P-ARC 及源码定位；只增强人工操作示例，不改阈值或扫描器。 |
| `.trellis/spec/academic-writing-skills/paragraph-arc-en-contract.md` | 64 | 英文差异；不得把英文密度阈值复制进中文。 |
| `.trellis/spec/academic-writing-skills/polish-rewrite-contract.md` | 94 | 直接适用；两层四字段、学术载荷与术语保护；脚本不得宣布语义保全。 |
| `.trellis/spec/academic-writing-skills/results-analysis-checker-contract.md` | 149 | 已有 RA-* 和范围/证据窗口；保持脚本契约，修正旧措辞指南与证据阶梯冲突。 |
| `.trellis/spec/academic-writing-skills/spec-checklist-convention.md` | 53 | 学校规范/阈值不可跨校外溢；C1 引用既有模板，不新增 checker 或阈值。 |
| `.trellis/spec/academic-writing-skills/subsection-context-contract.md` | 223 | 已有 S-CTX 和 current-only 边界；示例复用，不建新窗口协议。 |
| `.trellis/spec/academic-writing-skills/testing-and-tooling.md` | 282 | 三子任务验证依据；ZH 按路径加载、误报/假绿默认变化声明、完整输出回归。 |
| `.trellis/spec/claude-scholar/backend/database-guidelines.md` | 32 | settings/install ownership；不适用于目标写作流程。 |
| `.trellis/spec/claude-scholar/backend/directory-structure.md` | 37 | hooks/scripts/installer 分层；不迁移。 |
| `.trellis/spec/claude-scholar/backend/error-handling.md` | 35 | Claude hook 退出协议；不得当跨宿主规则。 |
| `.trellis/spec/claude-scholar/backend/index.md` | 39 | Node/安装器范围索引；不适用 Python checker。 |
| `.trellis/spec/claude-scholar/backend/logging-guidelines.md` | 32 | hook JSON/安装计数；只借鉴不提前报成功。 |
| `.trellis/spec/claude-scholar/backend/quality-guidelines.md` | 33 | CommonJS/POSIX/安装所有权；排除。 |
| `.trellis/spec/claude-scholar/frontend/component-guidelines.md` | 32 | 触发明确与渐进披露；目标已覆盖。 |
| `.trellis/spec/claude-scholar/frontend/directory-structure.md` | 35 | 组件安装布局；不增加 commands/agents/rules。 |
| `.trellis/spec/claude-scholar/frontend/hook-guidelines.md` | 31 | 文档需真实 activation 证据；不引入 hooks。 |
| `.trellis/spec/claude-scholar/frontend/index.md` | 39 | Markdown 用户界面范围索引。 |
| `.trellis/spec/claude-scholar/frontend/quality-guidelines.md` | 29 | 紧凑入口/便携说明；已覆盖。 |
| `.trellis/spec/claude-scholar/frontend/state-management.md` | 30 | sidecar/settings/卸载状态；不迁移。 |
| `.trellis/spec/claude-scholar/frontend/type-safety.md` | 29 | 真实宿主元数据；不照搬 allowed-tools。 |
| `.trellis/spec/guides/code-reuse-thinking-guide.md` | 223 | 复用与单一 owner 原则适用；Trellis 源码注册/rsync 路径不是本库操作指令。 |
| `.trellis/spec/guides/cross-layer-thinking-guide.md` | 259 | 检查输入、处理、输出与镜像的一致性；事件日志/版本站点实例不迁移。 |
| `.trellis/spec/guides/index.md` | 97 | 通用思考导航；高严重度候选须对照实物复核。 |
| `.trellis/spec/PaperSpine/backend/database-guidelines.md` | 36 | 安装/config 状态；只借鉴用户数据保留，不迁移状态层。 |
| `.trellis/spec/PaperSpine/backend/directory-structure.md` | 37 | scripts/references/dist 分工；借鉴真相源，不复制布局。 |
| `.trellis/spec/PaperSpine/backend/error-handling.md` | 36 | updater/artifact/wizard 退出行为；无对应运行面，排除。 |
| `.trellis/spec/PaperSpine/backend/index.md` | 41 | 参考 backend 预检索引；不是 ZH 开发命令。 |
| `.trellis/spec/PaperSpine/backend/logging-guidelines.md` | 27 | 简洁 CLI 与可读报告；不新建 logging 层。 |
| `.trellis/spec/PaperSpine/backend/quality-guidelines.md` | 34 | stdlib/unittest/120列/dist 约定不能覆盖本库 pytest/Ruff。 |
| `.trellis/spec/PaperSpine/frontend/component-guidelines.md` | 32 | 精确触发、精简入口可借鉴；不迁移 orchestrator/worker 结构。 |
| `.trellis/spec/PaperSpine/frontend/directory-structure.md` | 32 | 宿主 flat skills/legacy fallback；不引入目标包。 |
| `.trellis/spec/PaperSpine/frontend/hook-guidelines.md` | 26 | UI launcher 特约；绝对路径与 UI 优先不适用。 |
| `.trellis/spec/PaperSpine/frontend/index.md` | 40 | Markdown 用户界面索引；是定制 spec 而非空模板。 |
| `.trellis/spec/PaperSpine/frontend/quality-guidelines.md` | 27 | 双语/便携路径已覆盖，不重复建设。 |
| `.trellis/spec/PaperSpine/frontend/state-management.md` | 28 | 固定产物树与安装状态；只保留必要证据原则。 |
| `.trellis/spec/PaperSpine/frontend/type-safety.md` | 29 | 封闭选择集与版本解析；不据此新增写作 schema。 |
| `.trellis/spec/Research-Paper-Writing-Skills/backend/database-guidelines.md` | 34 | 静态资料职责可借鉴；不加隐藏状态。 |
| `.trellis/spec/Research-Paper-Writing-Skills/backend/directory-structure.md` | 29 | 短入口与示例分离；目标已具备。 |
| `.trellis/spec/Research-Paper-Writing-Skills/backend/error-handling.md` | 33 | 缺证据收窄/移除主张；按本库授权与保真契约适配。 |
| `.trellis/spec/Research-Paper-Writing-Skills/backend/index.md` | 40 | 明确无可执行 app backend；用于范围定界。 |
| `.trellis/spec/Research-Paper-Writing-Skills/backend/logging-guidelines.md` | 26 | 必要时给 claim-evidence 复核，不强制新台账。 |
| `.trellis/spec/Research-Paper-Writing-Skills/backend/quality-guidelines.md` | 36 | 紧凑双语资源可采用；checker/test 段是本地加注，源包没有对应实现。 |
| `.trellis/spec/Research-Paper-Writing-Skills/frontend/component-guidelines.md` | 22 | 目标/逻辑/范式/案例组织；用于 C1 现有例子。 |
| `.trellis/spec/Research-Paper-Writing-Skills/frontend/directory-structure.md` | 28 | 章节指南与示例银行；不另建并行资料体系。 |
| `.trellis/spec/Research-Paper-Writing-Skills/frontend/hook-guidelines.md` | 22 | 无运行 hooks；按需加载已覆盖。 |
| `.trellis/spec/Research-Paper-Writing-Skills/frontend/index.md` | 38 | 指南/示例导航；不引入 frontend 架构。 |
| `.trellis/spec/Research-Paper-Writing-Skills/frontend/quality-guidelines.md` | 36 | 主张证据与载荷保护；支持 C1 修正 AXES。 |
| `.trellis/spec/Research-Paper-Writing-Skills/frontend/state-management.md` | 25 | 逆向提纲与证据映射；C1 补一例完整操作。 |
| `.trellis/spec/Research-Paper-Writing-Skills/frontend/type-safety.md` | 29 | 元数据/真实链接适用；不另加状态枚举。 |
