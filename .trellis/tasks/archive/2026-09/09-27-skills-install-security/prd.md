# npx skills 安装告警诊断与安全边界优化

## Goal

修复 LaTeX include 的项目目录越界读取，使安装告警有可追溯的原因、行为修复和复核记录。保留合法多文件解析结果与源位置。

2026-09-27 用户明确批准按规划实施，任务已进入 `in_progress`。提交、发布和联系扫描服务仍未授权。

## Background

- 2026-09-27 在线查询：两个 ZH 技能各有一条 Socket `gptAnomaly`，均指向 `scripts/tex_loader.py`。扫描时间分别为 2026-09-25 07:31:52.299 UTC、2026-09-26 03:46:34.166 UTC。
- 两个副本在 `tex_loader.py:65` 解析目标，在 `:98`、`:204` 读取，`:223` 递归组装。没有项目根目录边界检查。
- 合成文件验证发现 `latex-paper-en`、`paper-audit`、`cover-letter` 三个同类副本也受影响。五副本的完整路径、哈希、源位置与测试矩阵见 `research/diagnosis.md`。
- 扫描另称代码末尾 `return do` 不完整。本地五个文件语法解析通过，两个 ZH 文件与查询到的远端 main 内容一致。扫描截断说法的原因未查明。
- 本地 defense 缺少 `SKILL.md`，公开 main 已有该文件。入口由 `09-23-defense-zh-catalog-docs` 管理，本任务不重复创建。

## Requirements

| ID | 要求 | 严重度 / 优先级 | 来源 |
| --- | --- | --- | --- |
| R1 | 记录扫描来源、时间、包标识、源码版本和复现结果；区分源码缺陷、扫描描述偏差和第三方状态 | Major / P1 | [Script] 在线数据与 reproduction.json；[LLM] 因果分析 |
| R2 | 五个 loader 在递归读取前拒绝越界；覆盖 input/include/subfile 和两个公开遍历接口 | Major / P1 | [Script] 五副本均复现 |
| R3 | 越界时明确报告来源和原因，终止当前操作；不得把不完整分析报告为正常成功 | Major / P1 | [LLM] 下游 warnings 消费存在差异 |
| R4 | 保留目录内引用、回退查找、中文及空格路径、源位置、循环、缺失文件与编码行为；明确项目根目录时支持嵌套 main | Major / P1 | [Script] 既有 multifile 测试和 defense Source.load |
| R5 | 保持独立安装和五副本行为一致；保留学术保护规则、公开返回结构与无关代码 | Major / P1 | AGENTS 与 unit-polish-contract |
| R6 | 同步安全边界和双语安装排障说明；分别报告本地修复、安装、发布和第三方重扫状态 | Minor / P2 | qiaomu trust、install evidence、claim guard |

## Acceptance Criteria

- [x] AC1 → R1：报告可回溯两条告警、版本和复现。截断说法及 API/页面等级不一致分别记为原因未查明。
- [x] AC2 → R2：五个真实副本 × 两接口 × 三命令，在目标读取前拒绝父目录越界、外部绝对路径和符号链接越界。测试断言外部读取函数未被调用，且未正常返回。
- [x] AC3 → R3：异常含稳定错误码、来源相对路径与行号。论文分析 CLI 和 defense extract CLI 越界退出非 0；defense 不创建或覆盖 inventory。缺失文件与越界拒绝可区分。
- [x] AC4 → R4：合法项目内用例和既有回归通过；目录内的 `..` 可用，目录名前缀相近的外部路径不可用；显式 `--thesis` 根目录内的嵌套 main 可用。
- [x] AC5 → R5：五副本行为测试、既有对齐和润色回归通过；冻结哈希仅按已审阅 diff 更新。`just ci` 四步全部通过。
- [ ] AC6 → R5/R6：安全说明、双语安装说明、资源门禁与 docs build 通过。隔离安装记录 CLI 版本、命令、来源版本和文件哈希；缺少 defense 入口时该安装证据保持未验证，等待 C4 集成。
- [x] AC7 → R1/R6：交付分列行为修复、安装验证、远端发布、第三方重扫状态。无针对新版本的扫描证据，不宣称 `0 alerts` 或安装告警消除。

2026-09-28 UTC 续作验收：`just ci` 四步通过（2787 passed、10 条件跳过），聚焦
537 passed、隔离安装 225 passed / 54 defense deselected；资源、文档构建和独立检查通过。
完整证据见 `research/implementation-evidence.md`。AC6 的四技能安装部分通过，
defense 仍等待 C4 入口；任务保持 `in_progress`，未提交、发布或申请第三方重扫。

## Scope and Constraints

- 包含五个 `tex_loader.py`、defense 既有根目录传递与异常转换、已获补充批准的 ZH check_format 和 audit prepare_review_workspace 异常传播、相关测试和安全说明。一个任务处理同一根因，按依赖顺序执行。
- 默认边界为入口文件父目录；更大边界仅接受宿主调用方明确给出的项目根目录，不从论文内容推断。
- 默认拒绝越界会改变原先可读取项目外 `.tex` 的行为。实施审批须包含该兼容性变化，不新增任意外部路径放行开关。
- 不扩展到 Typst、TeX 编译沙箱、附件/图片/aux 的全面访问控制、全仓技能重构或上游 CLI 等级映射修复。
- 不改论文正文、数字、引用、公式、术语或结论；仅用合成测试内容。不升级版本、不 push、不发布、不发送 issue、不隐藏告警。

## Decisions and Deferred Evidence

无阻塞实施的用户决策。原安装 CLI 版本和锁文件未提供，未重跑原始安装；Windows junction、UNC、并发链接替换及五宿主运行证据分别记录。第三方重扫需要新证据，对外发布需要独立授权。
