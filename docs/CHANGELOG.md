# Changelog

本文档根据 Git 提交历史整理，记录项目主要功能与文档变更。

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
- 更新安装文档与许可证说明，补充 `skilks` 安装路径（`7ec3805`、`77d7d5e`）。

### Fixed
- 修复嵌套浮动环境 caption 检测与 Typst 字符串处理问题（`5d8cbf7`）。
- 修复 `visual_check.py` 导入错误并优化重叠检测（`72e4700`）。

### Tests
- 新增 `check_references` 单元测试并补全 `conftest` 路径配置（`398fcc3`）。

### Chore
- 删除 `paper-audit` 旧版可行性分析草稿（`4b4925c`）。
- 新增 docs/doc-build 快捷命令，并移除 `docs/justfile`（`79785b9`、`742fa5c`）。
- 初始化 `paper-audit` 技能基础能力（3 模式 + PDF 支持）（`3faa3d1`）。
