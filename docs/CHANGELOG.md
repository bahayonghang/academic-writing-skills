# Changelog

本文档根据 Git 提交历史整理，记录 major/minor 版本的主要功能、修复、文档与工具链变化。

发布维护约定：每次更新 `pyproject.toml` 或技能 metadata 中的 major/minor 版本号
（如 `5.2.0`、`5.3.0`）时，必须同步更新本文件，并把上一版本以来的用户可见变化
从 `Unreleased` 归档到对应版本段落。

## [Unreleased]

### Added

- 暂无。

## [5.3.0] - 2026-07-09

> 当前工作区已将项目版本推进到 `5.3.0`；本节按 `5.2.0` 之后的 Git 历史整理。

### Added

- `latex-thesis-zh` 新增 `spec-check` 规范逐项终检，覆盖燕山模板清单与结构化问题输出（`33a4b55`）。
- `latex-thesis-zh` 新增 blind-review 盲审匿名化检查与盲审版生成流程（`c209851`）。
- `latex-thesis-zh` 新增 THU/PKU/generic 逐项检查清单，并将模板阈值参数化（`b6679c6`）。
- `cover-letter` 新增 AI 披露一致性 lane 与结构级 AI 痕迹检查（`93a67f4`）。
- 全技能新增学术去 AI 味结构壳检查、over-claim 保守表达 guard、时态信号词检测与 reviewer 怀疑点排序（`7311420`、`0abb569`、`3a8e3c2`、`8cf4622`）。
- `latex-thesis-zh` 新增章引言、本章小结、章节标题结构与公式断行排版专项指导（`7cf89e8`、`04c7009`、`95ee0bc`、`a99eb32`）。
- 新增论文分节写作参考体系和 research-writing eval coverage（`8d9fa96`、`e67cecc`）。

### Changed

- 对 `latex-thesis-zh` 进行集中优化：多文件论文解析、GB/T 7714 2025 校验、模板知识单源化、SKILL 路由/CLI 契约、fixture/evals 覆盖（`e46bddd`、`3e0e4ec`、`59810a2`、`83a933d`、`71d4d0b`、`7e0b5c5`）。
- 重构 EN 系 parsers 的多文件装配与章节切分基础，并对 `bib-search-citation`、`latex-paper-en`、`typst-paper`、`cover-letter` 做真实工程/路由/提取精度修复（`e84f5af`、`6217ef7`、`57482af`、`c6d73bb`、`6155dea`）。
- 六技能复审后统一 frontmatter 与 `paper-audit` Scripts 表，补充润色三层顺序原则和 AI 黑名单维护节律（`612651c`、`efbb8b6`、`10aaa6a`）。
- 精简中英文 README 路由、同步模块文档与技能契约，并清理九项文档与元数据一致性遗留（`d63772d`、`d90e92a`、`02dd30d`、`92ee774`）。

### Fixed

- 修复 `latex-thesis-zh` 英文摘要时态门控在 thuthesis/pkuthss 模板中的漏检（`75a763a`）。
- 同步 `typst-paper` deai 检查与 EN 副本，并修复 `presents` 误伤（`a6eb919`）。
- 修复 `paper-audit` `critical_count` 评分惩罚贯通与空文献误判（`762bf80`）。
- 修复 `cover-letter` 指标张冠李戴泄漏与 Bib 重复键静默问题（`2a31fd9`）。
- 修复论文模板资源链接（`7913cbb`）。

### Tests and Tooling

- 重组 `tests/` 目录并集中路径常量（`d516f97`）。
- 为 `deai_check` 三副本建立对齐锁测试，并记录 importlib 加载与双层阈值配置约定（`2a0d9be`、`fa714a9`）。
- 将 `.trellis/` 排除在项目 lint/format gate 外，跟踪并收纳 Trellis 工作流升级（`7ee5dc4`、`890a190`、`9bc15d8`）。
- 将 docs Pages 部署限制为 release 触发（`44d5ce8`）。

## [5.2.0] - 2026-06-04

### Added

- 发布 5.2.0 诊断增强，扩展学术写作技能的诊断能力（`e02c3f4`）。
- 新增 `cover-letter` 投稿信对齐校验技能，并登记文档入口与回归覆盖（`d2ca6b4`、`c4bdb30`、`524ce89`）。
- `paper-audit` 重构审稿工件布局，生成双语 HTML 报告并同步修订建议说明（`ea3ef88`、`42a6809`）。

### Changed

- 完善技能导航、双语说明与技能描述运行时契约（`ecc90ff`、`d2b5cd6`）。
- 降低技能中的不安全执行路径（`30a7f1c`）。
- 忽略本地文档构建产物并同步依赖清单（`fca8d91`、`6f4651d`）。

## [5.1.0] - 2026-05-21

### Added

- `paper-audit` 增强深度审稿综合与返修工作流（`c1ab622`）。

## [5.0.0] - 2026-05-20

### Breaking

- 聚焦写作技能套件边界，收窄技能定位与职责面（`fe380e7`）。

### Added

- 建立 claim-evidence 支撑契约，并同步文档站发布文档（`8f7a272`、`fc57c26`）。

## [4.0.0] - 2026-05-14

### Added

- `paper-audit` 支持深度审稿断点续跑、修订分数轨迹和合成 AI 腔夹具（`4f9d817`、`fb759a9`、`9a87e8d`）。
- 写作技能新增 AI 腔检测阈值与模板快照（`96de8dc`）。
- 补齐契约测试模块覆盖并迁移 `paper-audit` 模式名（`a59c776`）。

### Changed

- 发布 4.0.0 并同步锁文件版本（`1cb7ad4`、`bc9d828`）。
- 启用 pyright basic 类型检查，并将部分类型问题降级为 warning（`9aec9d9`）。
- 消歧 Reference Map，添加无脚本说明，并清理过期计划文档（`8cd8f27`、`4498895`）。

### Fixed

- 标记未验证引文并降低框架锁置信度，避免审稿结论过度确认（`8f6b75c`）。

### Chore

- 从版本控制移除 `docs/node_modules`（`ac1273c`）。
- 将 Pages 部署限制为 `main` 分支（`362ee73`）。

## [3.1.0] - 2026-05-09

### Added

- 新增 Bib 本地文献检索技能与文档入口，完善 `bib-search-citation` 本地检索契约（`3184a2c`、`a2893aa`）。
- `paper-audit` 新增预审规则、投稿前检查流程、委员会聚焦评审、期刊式审稿报告、文献搜索引擎与 9 维 ScholarEval（`0e49f68`、`d2ac967`、`79c1258`、`c6cc909`）。
- `paper-audit` 新增伪代码审查、IEEE gate、专项 reviewer、问题整合工作流与审查参考资料（`2fcc14d`、`3af0a0f`、`ee7ee49`）。
- `latex-paper-en` 与 `typst-paper` 新增 IEEE/IEEE-like 伪代码检查（`409f718`、`3b2ea24`）。
- 全技能新增摘要、表格、引文支持，反引用堆叠规则、逻辑分析深度检查与文献综述质量检查（`9d88360`、`0beac22`、`1251e68`）。
- 新增 literature/survey-draft 能力，强化综述写作综合链条约束（`ea86944`、`369a69f`、`38f57ae`）。
- `parsers` 新增标题、摘要和引用键提取能力（`283b217`）。

### Changed

- 收紧五个学术写作技能的路由与契约规则，并约束技能描述运行时长度（`1c4442f`、`f6319dd`）。
- 重构 `paper-audit` 功能模块并更新参考文档、模式指南和投稿前指南（`5afa154`、`cc23a64`、`4d6e7fb`）。
- 优化技能套件描述、模块文档、evals 与跨技能消歧（`d583c5b`）。
- 同步中英文文档站点、安装说明、侧边栏与资源页（`a35b1bf`、`840e70c`、`4625bfc`、`6bf75c6`、`92a109f`）。

### Fixed

- 修正北京大学模板 `pkuthss` 链接（`e24513c`）。

### Tests and Tooling

- 新增引用堆叠检测测试、逻辑/实验分析与契约验证测试，并更新 eval 触发配置（`e7df4ea`、`15e93f9`、`3aa3c11`）。
- 多次重建 VitePress 文档站点并同步构建产物（`94a1979`、`0be6696`、`7d85120`、`cb52b5f`）。

## [3.0.0] - 2026-03-11

### Added

- 新增 Industrial AI 深度研究技能，后续重命名为 `industrial-ai-research` 并补齐标准化字段（`d2c9ea8`、`3c9c832`）。
- `paper-audit` 升级论文审查流程与模板（`ae5ac54`）。

### Changed

- 引入 PyYAML，并将项目版本推进到 3.0.0（`1facc5c`）。
- 完善 LaTeX 与 Typst 技能结构，重构技能文档结构和项目文档表格风格（`e9dfcee`、`6e75f0f`、`0fa59c5`）。
- 更新项目定位描述，聚焦学术论文后期排版、验证与润色（`69e0a17`、`bd19903`）。

## [2.0.0] - 2026-02-28

### Added

- 新增 `paper-audit` 技能基础能力：3 模式、PDF 支持、polish 模式、ScholarEval 8 维评估与 PDF 视觉检查（`3faa3d1`、`663bea3`）。
- 新增参考文献完整性检查器与在线文献元数据验证（CrossRef + Semantic Scholar）（`0c51f9d`、`b371b43`）。
- 新增并行检查执行、JSON 输出格式、图表标题模块文档和 caption audit 审查标准（`f65de29`、`25d2e6c`、`41ddd53`）。
- 新增实验分析模块脚本与中英文文档（`b35016b`）。

### Changed

- 统一四个技能的参考资料目录结构，精简 SKILL 定义并移除重复 README（`7d3e66a`、`4810fef`）。
- 统一审查脚本结构并整理输出逻辑（`5023146`）。
- 更新 README、文档站点、安装文档、许可证说明与首页安装命令（`c1ae8f4`、`f16edf7`、`d599dec`、`77d7d5e`、`7ec3805`）。
- 统一术语“配方”为“编译配置”（`2af7eba`）。

### Fixed

- 修复 `visual_check.py` 导入错误并优化重叠检测（`72e4700`）。
- 修复嵌套浮动环境 caption 检测与 Typst 字符串处理问题（`5d8cbf7`）。
- 加固 `paper-audit` 动态导入并参数化字体阈值（`b3f8ed2`）。

### Tests and Tooling

- 新增 `check_references` 单元测试并补全 `conftest` 路径配置（`398fcc3`）。
- 规范化测试代码风格，升级项目版本与开发依赖锁定（`e42875d`、`1fd1522`、`ad57b6d`）。
- 新增 `just doc` / `just doc-build` 快捷命令，并移除 `docs/justfile`（`79785b9`、`742fa5c`）。

## [1.2.0] - 2026-02-20

### Added

- 新增 Typst 论文写作技能支持及去 AI 化脚本支持（`803ee78`、`239c967`）。
- 新增标题优化脚本、中文论文模板检测和参考文献检查脚本（`4b45556`、`4b15acc`）。
- `latex-paper-en` 与 `typst-paper` 新增高级分析脚本（`385e4e4`、`cbf3fc9`）。

### Changed

- 重构所有技能脚本代码质量，更新技能定义、README 与文档站点（`e220933`、`77d596b`、`eb0e556`）。
- `latex-thesis-zh` 重构 skill 架构并迁移参考文档至 `resources/` 目录（`76a8ffe`）。
- 迁移到 pytest，并新增 `latex-paper-en`、`latex-thesis-zh` 脚本测试（`bfeaadc`、`daa4697`）。

### Chore

- 添加开发工具配置、AI 助手配置与 `.kiro` 忽略规则（`470d357`、`2f9b2d2`、`788830d`）。

## [1.1.0] - 2026-01-21

### Added

- 新增通用解析器模块，支持 LaTeX 与 Typst 格式（`ae79ab1`）。
- 新增图片检查脚本，验证插图合规性（`ae79ab1`）。
- 为 LaTeX 技能新增去 AI 写作模块，并增强技能定义与去 AI 化模块（`68c92ce`、`8398d58`）。
- 新增术语与翻译参考指南（`457a903`）。

### Changed

- 重构去 AI 化脚本，简化代码结构（`11da67b`）。
- 添加 `pyproject.toml`、测试基础设施、依赖与工具配置（`547fc88`）。
- 更新中英文文档站点、README 安装说明、输出协议与失败处理说明（`b815eb6`、`1751f25`、`34d3501`）。

## [1.0.0] - 2026-01-01

### Added

- 初始化 LaTeX academic writing skills、双语 README、技术规格、打包工具和 VitePress 文档站点（`ceb9e17`、`a31cf42`、`d9b0d9b`、`46e5e34`、`7910502`）。
- 添加 GitHub Pages 部署工作流，并在 release 发布时部署文档（`5178926`、`1c974f4`）。

### Fixed

- 为 GitHub Pages 禁用 Jekyll 处理，并修正 Pages 部署环境配置（`b10f470`、`6c62b43`、`a866ed8`）。
