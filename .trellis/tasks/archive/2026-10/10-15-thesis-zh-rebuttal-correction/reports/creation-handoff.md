# Creation handoff：中文学位论文评阅回复归属修正

## 结果

`latex-thesis-zh` 6.0.0 接管学位论文评阅书整理、台账、修改说明与 R-* 核对；`latex-defense-zh` 恢复为原五模块 Beamer 答辩稿技能。未发布、未提交，任务保持 in_progress 等待交付后的收尾授权。

## 本轮实际研究的参考

- 本仓库原 `latex-defense-zh` 回复实现：保留原文、覆盖、完成证据、aux 和 git 核对，迁移所需最小依赖，不复制完整 deck 实现。
- 本仓库 `latex-thesis-zh` 根入口、openai 适配与 eval：沿用定向模块路由和本仓库格式；为评阅书单独 intake 明确输入例外。
- 本地 `qiaomu-meta-skill` 2.8.1：采用 description-first、渐进披露、隔离安装证据和声明分层。其新包命名、作者、许可与通用目录要求不覆盖既有项目。

历史外部候选未在本轮重读或执行，不列为新验证参考，详见 prior-art-research.md。

## 取舍

- 保留：现有 CLI、台账 schema、16 个 R-*、只读输入、输出覆盖保护和学术事实保护。
- 适配：能力归属、包内依赖、fixture、路由、双语文档、精确资源契约和独立安装测试。
- 拒绝：跨技能导入、全套 deck 复制、自动正文修改、修改历史档案、以静态用例冒充真实模型路由。
- 新增：归属与独立安装回归保障；未宣称新增回复算法或优于外部技能。

## 收益与证据

- [design advantage] 学位论文回复与正文工作流归入同一技能，回复脚本仍保持只读论文边界，Beamer 入口恢复单一职责。
- [validated advantage] defense-restoration.json：53 个基线文件哈希全部匹配，git diff 对 53c2ab5 为空，无回复产品文件残留。
- [validated advantage] 独立安装测试 4 项通过：只复制 thesis 包、包外 cwd、无仓库 PYTHONPATH，运行真实三个 CLI，并验证输入哈希和跳过行为。
- [validated advantage] trigger-eval.json：8/8 本次迁移的启发式 smoke 通过；匹配词和排除规则在 trigger-cases.json 公开，不是 provider-backed 证据。
- [hypothesis] 正确归属有助于真实助手选择技能；尚无跨模型或五工具对比证据。

## 验证与限制

完整 `just ci` 通过：2847 passed / 11 skipped；Pyright 0 errors / 86 条既有警告。资源同步 305 项、文档构建和 diff 检查通过，详见 check-results.md。原回复定向测试为 39 passed / 1 skipped；PDF 提取用例因未安装 PyMuPDF 跳过。真实论文操作、实际 XeLaTeX 验收、provider 路由和五工具运行未执行。

通用 Qiaomu validator 为 **FAIL（既有目录规范不匹配）**：迁移前后均缺少包内 README.md、agents/interface.yaml、manifest.json；仓库使用根 README、agents/openai.yaml 与 pyproject 版本元数据。本次没有为清零通用检查增加重复文件。qiaomu-validation-baseline.json 与 qiaomu-validation.json 保存原结果；skill-ir-raw.json 保存原导出，skill-ir.json 明示从仓库格式补充字段，不把适配冒充通用校验通过。

没有新增论文修改授权；真实材料验收与可选依赖安装不属于本次范围。

保留的既有 P2 限制：嵌套主 tex 引用有效兄弟目录时，数字提取可能跳过 R-NUM-SRC；本次为保持原行为未扩展修复，详见审查报告。
