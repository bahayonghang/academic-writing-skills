# 实施与验证记录

后续归档决定：用户已要求提交并归档；AC6 保留部分完成，详见 `archive-note.md`。
下文保留实施验证时的状态与执行记录。

状态：本地实现、完整 CI、文档门禁、四技能隔离安装和独立检查通过。
任务保持 `in_progress`。`latex-defense-zh` 的完整安装证据等待 C4 入口集成。

验证日期：2026-09-28 UTC / 2026-09-27 America/Chicago。
基线：`a9d2d32cf2e51a055a70496772b10e5a314d0267`，本地 `dev` 工作树。
源码范围为 `final-source-manifest.json` 中的 22 个文件，包含五个 loader、三个调用方、
对应测试、四个现有技能入口、安全规范及双语说明。任务研究记录单独保存。

## 本轮续作

- [LLM] 按现有批准恢复同一任务。实施子代理核读已有五副本和三调用方修改，未发现需要追加的产品代码修复。
- [Script] 增加 6 项普通异常回退回归：ZH format 和 audit workspace 分别覆盖 OSError、UnicodeError、ValueError。
- [Script] 收窄两个新增测试文件中的动态模块、异常字段及 AST 类型判定，消除 7 条新增类型警告；保持行为断言。
- [Script] 完善隔离安装工具，记录固定 CLI 的 version/help、安装命令、四个 loader 和两个调用方的复制哈希。
- [LLM] 完成 native delegated 独立全范围检查，未发现待修复问题。报告见 `independent-review.md`。

## 修复前后证据

原 `reproduction.json` 保持不变，记录修复前五副本可读取合成的外部内容。
补充的 `head-rejection-evidence.json` 从 Git HEAD 提取旧 loader 到临时目录，直接调用
当前的真实拒绝测试。五副本 × 两接口 × 三命令 × 四种越界共 120 项，全部在
`external read occurred before rejection` 断言失败；无跳过、无意外通过。

修改后的计划聚焦测试为 537 passed、0 skip（27.22 秒）。覆盖读取前拒绝、定位错误、
两处通用异常回退保留、defense inventory 不创建/不覆盖、项目内合法路径和源位置兼容。

## 验证结果

| 检查 | 结果 | 证据 |
| --- | --- | --- |
| 计划六文件聚焦 pytest | PASS：537 passed，0 skip | `implement-focused.txt` |
| 实施 lint / typecheck | PASS：0 errors，86 warnings；本任务两新增测试文件没有新增 warning | `implement-lint.txt`、`implement-typecheck.txt` |
| 独立检查 lint / typecheck | PASS：242 files；0 errors，86 warnings | `independent-review.md` |
| `just ci` 四步 | PASS：exit 0；版本检查 1 passed，lint 通过，typecheck 0 errors / 86 warnings，全量测试 2787 passed / 10 skipped（256.17 秒） | `final-ci.txt`、`ci-summary.json` |
| 全量资源检查 | PASS：297 manifest entries | `final-resource-gate.txt` |
| `just doc-build` | PASS：16.58 秒 | `final-docs-build.txt` |
| 双语新增锚点 | PASS：2 页 × 2 个 id 均存在 | `docs-anchors.json` |
| `git diff --check` | PASS：exit 0；仅 Git 行尾转换提示 | 主会话执行 |
| 四技能复制安装 | PASS：安装和测试退出码均为 0；225 passed，54 defense deselected，无 skip | `install-evidence.md`、`install-evidence.json`、`installed-tests.txt` |

当前验证在 Windows、Python 3.13 上运行。类型检查保留 86 条警告，没有批量修改无关文件。
全量测试的 10 项跳过分别为：5 项 defense 编译需显式设置 `DEFENSE_ZH_COMPILE=1`；
3 项预览测试缺少可选 `pymupdf`；2 项 Unicode 协议仅适用于非 Windows。
本机有 latexmk 和 xelatex，但没有开启上述编译测试开关。跳过项不计为通过。
本任务 537 项聚焦测试和 225 项安装后测试均无 skip。

## AC 对照

| AC | 状态 | 依据及限制 |
| --- | --- | --- |
| AC1 | PASS | `diagnosis.md`、原扫描快照和原复现可回溯；截断及 API/页面等级差异均保留原因未查明；本轮未刷新供应商扫描 |
| AC2 | PASS | 五副本、两接口、三命令、四种越界的真实拒绝测试；外部 read 和 exists 调用为 0；符号链接用例无 skip |
| AC3 | PASS | 稳定错误码、来源行号、论文 CLI 和 defense CLI 非 0；inventory 写入保护；普通异常回退回归 |
| AC4 | PASS | 项目内路径、中文及空格、显式根目录、源位置、循环、缺失、编码和既有 multifile 回归 |
| AC5 | PASS | 聚焦、对齐、润色及完整 `just ci` 四步通过；10 项既有条件跳过单列记录 |
| AC6 | PARTIAL | 双语说明、资源、docs、四技能复制安装通过；defense 完整安装等待 C4，不能勾选完整 AC6 |
| AC7 | PASS | 分列本地修复、安装、发布和重扫；未宣称告警已消除 |

## 交付状态与剩余项

| 项目 | 状态 |
| --- | --- |
| 本地行为修复 | 聚焦、完整 CI、文档门禁和独立检查通过 |
| 隔离安装 | 四技能通过；defense 完整安装 UNVERIFIED，等待现有 C4 任务集成入口 |
| 提交与远端发布 | 未执行；本轮授权不含 commit、push、PR 或发布 |
| 第三方重扫 | pending；没有针对修改后包的新扫描证据 |

未执行真实 UNC 网络共享、junction、并发链接替换、其他操作系统原生运行、五宿主新会话
及原用户未知版本 CLI 的安装复现。模拟 POSIX 路径分支不计为 POSIX 主机验证。
源码目录检查不构成 TeX 执行沙箱。

后续由 C4 集成 `latex-defense-zh/SKILL.md` 后，再补该技能安装证据和完整 AC6。
本轮不新建该入口，不变更其他活动任务，不归档当前任务。
