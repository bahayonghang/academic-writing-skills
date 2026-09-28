# Include 边界独立实施检查

- 检查方式：**native delegated**，独立 `trellis-check` 子代理。
- 检查日期：2026-09-28 UTC。
- 基线：`a9d2d32cf2e51a055a70496772b10e5a314d0267`。
- 范围：`design.md` 白名单内全部累计修改，包含五个 loader、三个调用方、四个测试文件、四个 SKILL 安全说明、双语 README/安装页、spec 及索引；另核读本任务 `research/verify_local_install.py`。共 22 个产品/测试/文档路径对应 `final-source-manifest.json`，安装 helper 单独列入检查。
- 载入材料：完整 native hook 对应的任务 PRD、design、implement、check.jsonl 全部规范、diagnosis 和 caller-boundary-amendment，以及 `trellis-start`、`trellis-check`。
- 写入范围：本报告。没有修改产品、测试、安装 helper 或主会话证据文件，没有提交、发布或创建 defense 入口。

## Findings (fixed)

无。独立检查没有发现需要直接修复的任务内问题。

## Findings (not fixed)

无未修复的已确认任务内缺陷。以下是既定验收边界，不计为代码修复项：

- `academic-writing-skills/latex-defense-zh/SKILL.md` 当前仍不存在。defense 的源码行为已纳入测试，安装验证等待 C4 集成；不能关闭完整 AC6 或把整项任务归档为全部完成。
- 第三方重扫仍为 pending；没有远端发布。本地测试和四包安装通过不能证明原告警已消除。
- Windows junction、实际 UNC 网络共享、真实 POSIX 运行、并发链接替换和五宿主运行没有新增验收证据。Windows 路径拒绝测试覆盖未发起外部解析的分支；POSIX 分派测试在本机模拟分派，不能计为真实 POSIX 运行。
- 86 条 Pyright warning 属于现有未修改代码和测试范围，本轮没有扩展清理。

## 行为核对

| 检查面 | 证据与结论 |
| --- | --- |
| 根目录所有权 | EN canonical `tex_loader.py:105` 的 `_entry_and_root` 在 entry 读取前确定固定 root；默认使用解析后的 entry.parent，显式 root 须为现有目录且包含 entry。保留 positional entry，新增 keyword-only project_root。 |
| 拒绝顺序 | EN canonical `tex_loader.py:84` 先检查词法包含，再解析链接并检查解析后包含；`:128` 的候选和回退都在 exists/read 之前经过同一检查。显式越界候选不被同名回退隐藏。 |
| Windows 与异常 | `tex_loader.py:128` 对 NUL、盘符相对路径、非 Windows 的 Windows 形式做明确拒绝；原生外部根路径/盘符/UNC 在外部 resolve 前被词法检查拦截。`IncludeBoundaryError` 保留稳定码、raw、source、line、reason；不返回部分成功结果。 |
| 两条公开路径 | `iter_files:150` 与 `assemble:241` 同步固定 root 和递归读取检查；保留节点结构、AssembledDocument 结构、编码、循环、注释、缺失诊断及 `.typ` passthrough。 |
| 五副本 | 独立 AST/文本比对确认新增三个成员，修改 `_resolve_include_target`、`iter_files`、`assemble`；EN/AUDIT/cover-letter 全文相同，两个 ZH 文件只保留技能 docstring 差异。其余成员保持原状。 |
| defense 调用方 | `extract_thesis.py:274` 传入 thesis root，把边界异常转换为 ExtractError；source 映射已相对 root，prefix 置为 `.` 避免重复前缀。`:1181` 的异常分支先于创建/写入 inventory。嵌套 main 和新建/已有输出保护有真实 CLI 测试。 |
| 已批准的两处传播 | ZH `check_format.py:238` 与 audit `prepare_review_workspace.py:702` 只重抛 IncludeBoundaryError；普通 OSError、UnicodeError、ValueError 回退由六条测试保留。 |
| 测试加载与安全断言 | `test_tex_loader_security.py:21` 按真实五个路径加载并恢复 sys.path/sys.modules；`:44` 覆盖五副本×两接口×三命令×四种越界，监测外部 read/exists 为零并要求异常。`:203` 验证 Windows 非法形式没有外部 resolve；`:258` 验证内部链接、父目录语义和 root alias。 |
| 冻结与对齐 | `test_polish_unit_zh.py` 只有 tex_loader 的一个 FROZEN_HASHES 值更新；新 LF hash 为 `7d96184955646e514451d1478743a26e5ff79a8686533d1ee8c02798ab0a7fec`。其他冻结值及 parsers ALIGNMENTS 没有修改。 |
| 安装来源 | `verify_local_install.py:21` 在 collection 后把安全测试 SKILLS_ROOT 改到安装树。loader 的 __file__ 守卫、caller fixture 的文件路径/sidecar 类身份守卫、CLI 的绝对脚本路径均使用安装副本。`:100` 和 `:121` 检查副本仍位于临时项目并与源文件哈希一致；没有把仓库 loader 测试计为安装通过。 |
| 文档与声明 | 四个 SKILL、双语安装页、README 链接和 include-boundary-contract 一致说明默认行为变化、显式 root、错误码及四类状态。没有跨技能运行依赖、扫描消警声明或新增 CLI 放宽选项。 |

## Verification

| 项目 | 执行者与命令 | 结果 |
| --- | --- | --- |
| Lint | 本检查代理：`just lint` | PASS，exit 0；242 files already formatted；All checks passed。 |
| TypeCheck | 本检查代理：`just typecheck` | PASS，exit 0；0 errors、86 warnings、0 informations。新增任务测试没有新 warning。 |
| 五副本差异 | 本检查代理：Python AST 成员差异、LF SHA-256 和副本文本比较 | PASS；改变成员及副本差异与设计一致。 |
| 聚焦回归 | 实施代理执行，本检查代理核读 `implement-focused.txt` | PASS，537 passed / 0 skip，27.22s。命令见下方。 |
| 安装副本 | 主会话执行，本检查代理核读 helper、`install-evidence.json`、`installed-tests.txt` | PASS；skills@1.7.0，四个项目级 copy 安装，install_exit=0；225 passed、54 defense deselected，18.38s，test_exit=0。四个 loader 和两处调用方哈希匹配。 |
| 资源门 | 主会话执行，本检查代理核读 `final-resource-gate.txt` | PASS，297 manifest entries。 |
| 文档构建和锚点 | 主会话执行，本检查代理核读 `final-docs-build.txt`、`docs-anchors.json` | PASS；双语 installation 各两个新增锚点全部存在。 |
| 完整 CI | 主会话负责 `just ci` 四步 | 本报告结算时仍在运行，最终结果由主会话记录到 `final-ci.txt` 和 `implementation-evidence.md`；上述聚焦测试不能替代完整 CI。 |

聚焦命令：

```text
uv run --extra dev python -m pytest tests/shared/test_tex_loader_security.py tests/contracts/test_tex_loader_alignment.py tests/shared/test_en_family_parsers_multifile.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_multifile.py tests/skills/latex_thesis_zh/test_polish_unit_zh.py tests/skills/latex_defense_zh/test_defense_extract.py -q
```

安装命令：

```text
npx --yes skills@1.7.0 add <repo>/academic-writing-skills --skill latex-thesis-zh latex-paper-en paper-audit cover-letter --agent codex --copy --yes --json
```

结论：已审阅代码范围可以进入主会话质量门结算。无需产品返修；完整 CI、C4 安装补验及第三方扫描保持各自状态，不合并为一个完成结论。
