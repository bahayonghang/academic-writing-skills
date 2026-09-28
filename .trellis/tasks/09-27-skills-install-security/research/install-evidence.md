# 隔离安装验证

验证时间：2026-09-28 01:58:04 UTC（本地 2026-09-27，America/Chicago）。
来源：本地工作树，基线提交 `a9d2d32cf2e51a055a70496772b10e5a314d0267`。
修改后的源文件哈希见 `final-source-manifest.json`；安装副本哈希见
`install-evidence.json`。本次验证没有发布远端版本。

## 命令与安装范围

固定 CLI 为 `skills@1.7.0`。`--version` 返回 `1.7.0`；`--help` 确认本次使用的
`--skill`、`--agent`、`--copy`、`--yes` 和 `--json` 参数。完整输出分别保存在
`install-cli-version.txt` 和 `install-cli-help.txt`。

在新建临时项目执行：

```text
npx --yes skills@1.7.0 add <repo>/academic-writing-skills --skill latex-thesis-zh latex-paper-en paper-audit cover-letter --agent codex --copy --yes --json
```

安装目录是临时项目内的 `.agents/skills`。没有使用全局安装参数，没有覆盖用户已安装的
技能。验证结束后由 `TemporaryDirectory` 清理本次临时项目。

## 结果

- 安装退出码：`0`。安装输出见 `install-output.txt`。
- 四个 loader 的安装文件 SHA-256 均与源文件一致。安装文件位于临时项目内，且文件不是符号链接。
- ZH `check_format.py` 和 audit `prepare_review_workspace.py` 两个调用方的安装哈希也与源文件一致。
- 安装后测试：`225 passed, 54 deselected in 18.38s`，退出码 `0`，无 skip。
- 54 项排除用例均属于未安装的 `latex-defense-zh`；排除不计为通过。
- 验证通过 pytest 插件把 `test_tex_loader_security.py` 的 `SKILLS_ROOT` 指向安装目录。
  loader、调用方和 CLI 均从该目录加载。loader fixture 核对实际模块 `__file__`。

可重复运行的入口：

```text
uv run --extra dev python -B .trellis/tasks/09-27-skills-install-security/research/verify_local_install.py
```

## 证据限制

本地 `latex-defense-zh/SKILL.md` 尚未由 C4 集成，其完整安装验证保持 **UNVERIFIED**。
该技能的 loader 和 extract CLI 已纳入仓库聚焦测试，但这些测试不能填补完整安装证据。

原用户安装命令对应的 CLI 版本未知。本记录只证明固定 `skills@1.7.0` 对当前本地
工作树的复制安装与已运行测试。五宿主新会话、远端发布和针对新包的第三方重扫均未执行。
不能据此宣称安装告警消除或 `0 alerts`。
