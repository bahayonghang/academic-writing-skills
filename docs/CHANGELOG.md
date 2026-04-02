# Changelog

本文档根据 Git 提交历史整理，记录项目主要功能与文档变更。

## [Unreleased] - 2026-04-01

### Added
- 为 `latex-paper-en`、`latex-thesis-zh`、`typst-paper` 新增 Abstract 模块：五元素摘要结构诊断（`analyze_abstract.py`）。
- 为 `latex-paper-en`、`latex-thesis-zh`、`typst-paper` 新增 Tables 模块：三线表合规检查（`check_tables.py`）与表格生成（`generate_table.py`）。
- 为 `latex-paper-en`、`typst-paper` 新增 Adapt 模块：跨 venue 格式适配工作流。
- 为 `latex-paper-en`、`typst-paper` 新增 6 份参考指南：ABSTRACT_STRUCTURE、CITATION_STYLES、JOURNAL_ABBREVIATIONS、JOURNAL_ADAPTATION_WORKFLOW、NUMBER_UNIT_GUIDE、TABLE_GUIDE。
- 为 `latex-thesis-zh` 新增 3 份参考指南：ABSTRACT_STRUCTURE、CAPTION_GUIDE、TABLE_GUIDE。
- 为 `latex-thesis-zh` 文档站点新增全部 11 个模块页面（之前文档缺失）。
- 为 `paper-audit` 新增 DEEP_REVIEW_CRITERIA（16 类问题分类法）、CHECKLIST（通用+六大 venue 专项）、QUALITATIVE_STANDARDS（SRQR 定性研究评审标准）。
- 为 `paper-audit` 新增 editor_in_chief_agent（EIC desk-reject 筛选智能体）。
- 为 `paper-audit` 新增专项 reviewer 智能体：prior_art、critical、domain、methodology。

### Changed
- 重构文档站点侧边栏：所有技能现在展示可折叠的 Modules / References 子分组。
- 更新所有技能 index.md，补充新模块到模块路由表与推荐提示词。
- 更新 usage.md 与 quick-start.md，新增 abstract 和 tables 相关命令与模块列表。
- 提取 VitePress config.ts 侧边栏为 helper 函数，EN/ZH 自动生成。
- 更新 `paper-audit` 文档（EN/ZH）：`deep-review` 默认委员会流程、`--focus` 单维度路由、`committee/consensus.md` 输出、Desk Reject 分数封顶规则。

## [Unreleased] - 2026-02-28

### Added
- 新增 `paper-audit` 的 polish 模式、ScholarEval 8 维评估与 PDF 视觉检查能力（`663bea3`）。
- 新增在线文献元数据验证（CrossRef + Semantic Scholar，无需 API Key）（`b371b43`）。
- 为四个技能新增参考文献完整性检查器（`0c51f9d`）。
- 为 `latex-paper-en`、`latex-thesis-zh`、`typst-paper` 新增 Caption 模块文档与入口（`25d2e6c`）。
- 为 `paper-audit` 新增 `FORBIDDEN_TERMS.md` 与 `QUICK_REFERENCE.md`（`805267d`）。

### Changed
- 更新 README 与文档站点，补充 caption 生成功能与审查能力说明（`f16edf7`、`c1ae8f4`）。
- 扩展 `paper-audit` 审查词与标准，纳入 caption audit 规则（`41ddd53`）。
- 新增并行检查执行与 JSON 输出格式（`f65de29`）。
- 重构动态导入逻辑，并将字体阈值参数化（`b3f8ed2`）。
- 统一文档术语“配方”为“编译配置”（`2af7eba`）。
- 更新安装文档与许可证说明，补充 `skills` 安装路径（`7ec3805`、`77d7d5e`）。

### Fixed
- 修复嵌套浮动环境 caption 检测与 Typst 字符串处理问题（`5d8cbf7`）。
- 修复 `visual_check.py` 导入错误并优化重叠检测（`72e4700`）。

### Tests
- 新增 `check_references` 单元测试并补全 `conftest` 路径配置（`398fcc3`）。

### Chore
- 删除 `paper-audit` 旧版可行性分析草稿（`4b4925c`）。
- 新增 docs/doc-build 快捷命令，并移除 `docs/justfile`（`79785b9`、`742fa5c`）。
- 初始化 `paper-audit` 技能基础能力（3 模式 + PDF 支持）（`3faa3d1`）。
