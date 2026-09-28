# 实施计划

状态：2026-09-27 用户批准实施，task.py start 已将任务切换为 in_progress。

## 进入条件

1. 用户在本轮最终摘要之后明确批准实施，包含默认拒绝项目外 include 和五副本范围。
2. 复核当前 HEAD、dirty 文件与 defense C2/C4 活动任务；按 design.md 划定所有权，禁止覆盖他人改动。
3. 审阅 prd/design/implement，运行 task.py validate；随后才能 task.py start。
4. 实施与检查遵循当前 Trellis sub-agent 工作流。主会话提供 manifest，并在下发前说明文件所有权和共享工作树约束；规划阶段不派发实现。

## 执行顺序

- [x] S1：冻结起点。复查五个 loader 哈希、两条在线告警及原任务接口；保存新旧版本差异。原始 research/reproduction.json 保留为修复前记录，不覆盖。
- [x] S2：添加真实五副本行为测试。先证明外部 read 被调用的旧行为会使拒绝断言失败；不使用真实用户文件。不把研究探针当作已修复的回归测试。
- [x] S3：实现统一根目录判断与 IncludeBoundaryError。保持 entry positional 参数，增加 project_root keyword；候选和回退都在读取前验证。同步五个副本，运行聚焦安全测试与原有多文件回归。
- [x] S4：defense 传递既有 --thesis 根目录，将边界异常转换为 ExtractError。测试嵌套主文件、CLI 非 0、目标 inventory 未创建/未覆盖。研究其他读取路径不扩展为本任务修改。
- [x] S4b：按用户补充批准，为 ZH check_format 与 audit prepare_review_workspace 增加特定边界异常传播及回归，保留其他回退。
- [x] S5：补五副本契约与 ZH 润色回归。审阅 diff 后只更新 loader 的 FROZEN_HASHES。其他冻结文件与 parsers ALIGNMENTS 保持不变。
- [x] S6：更新 skill 安全边界、README 链接、双语安装排障与 include-boundary-contract。defense SKILL.md 尚不存在时与 C4 集成协调，不创建第二入口。
- [x] S7：运行下列完整质量门。外部环境或旧基线失败必须记录实际原因；不得用目标测试通过替代 full gate。
- [ ] S8：在隔离临时目录中用固定版 npx skills 做本地来源安装验证；记录 version/help/实际命令/文件哈希和新旧行为。当前四个入口与 C4 完成后的 defense 分别记录，缺失部分保持未验证。
- [x] S9：独立检查修改范围与行为证据，完成 AC 对照。交付列出四项状态：本地修复、安装、发布、第三方重扫。没有新扫描就不宣称消警。不开 PR、不发布、不联系供应商。

## 验证命令

实施后聚焦门：

```text
uv run --extra dev python -m pytest tests/shared/test_tex_loader_security.py tests/contracts/test_tex_loader_alignment.py tests/shared/test_en_family_parsers_multifile.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_multifile.py tests/skills/latex_thesis_zh/test_polish_unit_zh.py tests/skills/latex_defense_zh/test_defense_extract.py -q
```

完整门：

```text
just ci
uv run python docs/scripts/check_resource_sync.py
just doc-build
git diff --check
```

`just ci` 顺序为 check-versions、lint、typecheck、test。资源门独立于四步 CI。不因本任务没有修改公开 references 就跳过仓库要求的资源检查；不为通过检查改无关资源。

不设置 pytest 进程级 PYTHONIOENCODING。需要中文子进程时仅对子进程设置 UTF-8，父进程同时明确 encoding。使用普通 shell 命令，不添加 rtk prefix。

隔离安装步骤在确定 CLI 版本与 help 后保存到 research/install-evidence.md。保存来源 commit 或 local-tree 哈希、安装路径相对临时目录、每个 skill 的 loader 哈希、实际命令和退出码。安装动作不得触发全局覆盖。安装后的安全测试必须 import 安装副本，不能仍测试仓库原文件。

## 证据与审批

规划已执行：在线 API/详情核查、五副本合成复现、五文件语法解析、两 ZH 远端内容比对、既有 TestTexLoader 六项测试。
规划未执行：以上新增安全回归、完整 CI、文档构建、npx 安装、修复后复现、五工具运行、第三方重扫。

完整安装门被 C4 入口缺失阻塞时，允许交付“本地实现检查通过、defense 安装待验证”，但不能勾选完整 AC6 或归档任务为全部完成。
对外发布或申请重扫必须有后续明确授权，审批前完成可审阅的代码、证据与申请草稿。

## 回滚与停止条件

- 出现 design 白名单之外的接口/目录变更需求，先报告并修订计划。
- 多副本既有差异无法保留、正常论文内容/源位置变化、学术事实变化时停止并定位，不调低断言。
- 只回滚本任务 diff。绝不全仓 checkout/reset、清理用户安装目录或重置其他活动任务。

## 本次续作结果（2026-09-28 UTC）

S1–S7、S9 完成。S8 四技能安装部分完成：skills@1.7.0 项目级复制安装退出 0，
安装后 225 passed、54 defense deselected、无 skip。完整 S8 等待 C4 集成 defense 入口，保留未勾选。

正式 just ci 四步通过：2787 passed、10 条件跳过；537 项聚焦测试无 skip。
资源检查、docs build、四个锚点、diff 检查及 native delegated 独立检查通过。
证据及 AC 对照见 research/implementation-evidence.md。未提交、发布、申请重扫或归档。
