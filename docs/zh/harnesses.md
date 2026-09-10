# 工具接入

快照日期：**2026-09-07**（Asia/Shanghai）。下表能力以该日官方文档为准。本机已安装 CLI 不等于运行时验证。未运行项保持 **UNVERIFIED**。

适用工具：Claude Code、Codex、Grok Build、Kimi Code、OMP（Oh My Pi）。

## 两条路径 {#two-paths}

两条路径分开使用。

| 路径 | 对象 | 已跟踪入口 | 不要混入 |
| --- | --- | --- | --- |
| 维护本开发仓库 | 项目维护者 | 根目录 `AGENTS.md`；Claude Code 另加载 `CLAUDE.md` | 论文项目的 skill 复制步骤、仅面向稿件的 `SKILL.md` 流程 |
| 把技能安装进论文项目 | 论文 skill 使用者 | 各技能 `SKILL.md` 及该技能的 `references/` | 本仓库 Trellis 生命周期、被忽略的 harness 适配目录、维护者 agent 与 hook |

技能包复制进稿件仓库后仍须可用。不要依赖本开发仓库的私有绝对路径，也不要依赖本机全局工具配置。

## 共同的显式读取 {#explicit-read}

新 clone 可以通过已跟踪文件加载共同规则，不依赖被忽略的 harness 目录、私有绝对路径或隐含全局 hook。

**维护者 clone**

1. 打开已跟踪的 `AGENTS.md`。
2. Claude Code：打开已跟踪的 `CLAUDE.md`。该文件首行是 `@AGENTS.md`。Claude Code 不原生读取 `AGENTS.md`。
3. 其他工具：通过原生发现加载 `AGENTS.md`，或在会话中打开 `AGENTS.md`。不要把 Claude 的 `@AGENTS.md` 导入语法当成通用语法。
4. 修改某个技能时，打开该技能的 `SKILL.md`，再打开 `references/` 中被路由到的文件。

**论文 skill 使用者**

1. 打开已安装技能的 `SKILL.md`。
2. 打开该技能 `references/` 中被路由到的文件（技能指向时再打开 `templates/`、`examples/`、Markdown `agents/`）。
3. 若当前工具没有自动加载该技能，仍按上述顺序显式读取。

不要依赖 `.claude/`、`.codex/`、`.agents/`、`.cursor/`、`.grok/`、`.kimi-code/`、`.omp/`。Git 忽略 `.claude/`、`.codex/`、`.agents/`、`.cursor/`。这些目录没有已跟踪文件。本仓库没有 `.grok/`、`.kimi-code/`、`.omp/`。

`SKILL.md` frontmatter 中的 Markdown `allowed-tools` 是部分 Claude 兼容加载器的指导信息。只有当前平台真正强制执行时，才把该列表当作沙箱。

## 证据状态 {#evidence}

本轮关闭的是**静态规则与隔离脚本交付**。本轮不关闭**五平台运行验证完成**。未运行的运行时项保持 **UNVERIFIED**。

| 检查 | 2026-09-07 状态 |
| --- | --- |
| 当前 working copy 上的 `grok inspect` | 已验证发现根目录 `Agents.md` / `Claude.md` 以及项目 Trellis skills/agents。当时 Claude 兼容 hooks 处于禁用。该项覆盖当前 working copy 发现。新 clone 检查保持 UNVERIFIED。 |
| 隔离 CLI（`paper-audit` 同级完整布局 vs 单技能） | 本机已验证。完整同级布局：missing=0，RUN=11。仅 paper-audit：missing=8，RUN=3（受限覆盖）。该行不是五套工具运行时通过。 |
| Claude Code 新会话 `/context` | UNVERIFIED |
| Codex 新会话 `AGENTS.md` 链、skills、agents、hooks | UNVERIFIED |
| Kimi Code 项目 `AGENTS.md`、skills、agents、委派 | UNVERIFIED |
| OMP 交互会话 `AGENTS.md`、`skill://`、`.omp` agents、Trellis extension | UNVERIFIED |
| 五套工具上的 `npx skills add` 复制或符号链接布局 | UNVERIFIED |
| 五套工具运行时（新会话、委派、hooks 信任） | UNVERIFIED |
| 当前 SHA 上的 hosted GitHub Actions（Windows/Ubuntu × Python 3.10/3.13） | UNVERIFIED |

2026-09-07 记录的本机 CLI 版本：Claude Code 2.1.263、Codex 0.153.4、Grok Build 1.0.22、Kimi Code 0.41.0、OMP（Oh My Pi）18.1.12。这些版本描述研究用机器。本仓库五套工具运行时保持 UNVERIFIED。

## 接入矩阵 {#access-matrix}

| 工具 | 维护者入口 | 论文 skill 入口 | 加载方式 | 委派 | 权限 |
| --- | --- | --- | --- | --- | --- |
| Claude Code | 已跟踪 `CLAUDE.md`，含 `@AGENTS.md` | 已安装 `SKILL.md`；可选项目 `.claude/skills/<name>/SKILL.md` | 原生 `CLAUDE.md`；skill 正文按需加载 | 项目 `.claude/agents/*.md`；`SubagentStart` / `PreToolUse` 可注入上下文 | `CLAUDE.md` 是指导。阻断需要 settings 或 `PreToolUse` hook。项目 hooks 需要信任。 |
| Codex | 已跟踪根目录 `AGENTS.md`（global → project → cwd 链） | 已安装 `SKILL.md`；项目 `.agents/skills` 先注入 name/description | 每次 run 构建 `AGENTS.md` 链 | `.codex/agents/*.toml`；`SubagentStart` additionalContext | sandbox 与 approval 来自运行时和 agent 配置。项目 hooks 可能还需要用户级启用和一次审查。 |
| Grok Build | `AGENTS.md` 系列与 `CLAUDE.md` 系列 | 已安装 `SKILL.md`；原生 `.grok/skills`；也兼容 Claude skills/plugins | 官方文档：两套规则族 | 内置 general-purpose / explore / plan，以及 `.grok/agents`；存在项目 hooks | mode、项目 permission 与 sandbox 分层。项目 hooks 需要 `/hooks-trust`。 |
| Kimi Code | 将 `AGENTS.md` 作为参考上下文（agent system prompt 是另一层） | 已安装 `SKILL.md`；`.kimi-code/skills` 与 `.agents/skills`（Project > User > Extra > Built-in） | 参考上下文，加上显式读取 `SKILL.md` | 内置 coder / explore / plan；`.kimi-code/agents` 与 `.agents/agents`；独立 child context | 每次 dispatch 通常需要批准，除非存在 allow rule 或 Ask When Needed。Agent 的 `tools` / `disallowedTools` 可限权。 |
| OMP（Oh My Pi） | 已跟踪的独立 `AGENTS.md` / `CLAUDE.md`；官方也记录 `.omp/AGENTS.md` | 已安装 `SKILL.md`；优先 `.omp/skills`；`agents` provider 也读取 `.agents/skills` | 启动时 metadata；正文通过 `skill://` | `task` tool；项目 `.omp/agents/*.md`；model / effort / spawns / prewalk | `--approval-mode`、agent 工具列表、spawn 深度与 model role 分层。 |

此处 OMP 指 **Oh My Pi**（`https://omp.sh/`，仓库 `can1357/oh-my-pi`）。

## Claude Code {#claude-code}

- 维护者：提交 `CLAUDE.md`。保持首行为 `@AGENTS.md`。
- 论文使用者：打开已安装技能的 `SKILL.md`。Claude Code 项目技能路径为 `.claude/skills/<skill>/`。该路径在本开发仓库中被 gitignore。
- 新会话 `/context` 检查保持 UNVERIFIED。
- 官方来源（2026-09-07）：
  [Memory / CLAUDE.md / AGENTS.md](https://code.claude.com/docs/en/memory)、
  [Skills](https://code.claude.com/docs/en/skills)、
  [Subagents](https://code.claude.com/docs/en/sub-agents)、
  [Hooks](https://code.claude.com/docs/en/hooks)。

## Codex {#codex}

- 维护者：提交根目录 `AGENTS.md`。Codex 构建 global → project → cwd instruction chain。
- 论文使用者：打开已安装技能的 `SKILL.md`。项目技能在 `.agents/skills` 存在时使用该树。本仓库 gitignore `.agents/`。
- 新会话 chain、skill 发现与 hook 触发保持 UNVERIFIED。
- 官方来源（2026-09-07）：
  [AGENTS.md](https://developers.openai.com/codex/guides/agents-md)、
  [Skills](https://developers.openai.com/codex/skills)、
  [Subagents](https://developers.openai.com/codex/subagents)、
  [Config reference](https://developers.openai.com/codex/config-reference)。

## Grok Build {#grok-build}

- 维护者：打开 `AGENTS.md`。Grok Build 也可能读取 `CLAUDE.md`。
- 论文使用者：打开已安装技能的 `SKILL.md`。原生项目技能路径为 `.grok/skills`。本仓库没有该目录。
- 2026-09-07 的 `grok inspect` 通过兼容路径发现了 working copy 的根规则文件和 Trellis skills/agents。当时 Claude 兼容 hooks 处于禁用。新 clone 与 hook-trust 检查保持 UNVERIFIED。
- 官方来源（文档页日期：skills/plugins 2026-08-11，subagents 2026-07-21；研究快照 2026-09-07）：
  [Skills, plugins, marketplaces](https://docs.x.ai/build/features/skills-plugins-marketplaces)、
  [Subagents](https://docs.x.ai/build/features/subagents)、
  [Permissions](https://docs.x.ai/build/features/permissions)。

## Kimi Code {#kimi-code}

- 维护者：将 `AGENTS.md` 作为参考上下文打开。
- 论文使用者：打开已安装技能的 `SKILL.md`。项目技能路径为 `.kimi-code/skills` 与 `.agents/skills`。本仓库没有 `.kimi-code/`。`.agents/` 被 gitignore。
- 项目发现与 Agent/AgentSwarm 委派保持 UNVERIFIED。
- 官方来源（2026-09-07）：
  [Skills](https://moonshotai.github.io/kimi-code/en/customization/skills)、
  [Agents and sub-agents](https://moonshotai.github.io/kimi-code/en/customization/agents)、
  [Configuration](https://moonshotai.github.io/kimi-code/en/configuration/config-files)。

## OMP（Oh My Pi） {#omp}

- 维护者：打开独立的 `AGENTS.md`。官方文档也描述 `.omp/AGENTS.md`。本仓库没有 `.omp/`。
- 论文使用者：打开已安装技能的 `SKILL.md`。启动时可能只注入 metadata；通过 `skill://` 或直接打开文件读取正文。
- 2026-09-07 的独立 `read` 探针未返回 skills。交互发现与 Trellis extension 保持 UNVERIFIED。
- 官方来源（2026-09-07）：
  [Context files](https://github.com/can1357/oh-my-pi/blob/main/docs/context-files.md)、
  [Skills](https://github.com/can1357/oh-my-pi/blob/main/docs/skills.md)、
  [Task agent discovery](https://github.com/can1357/oh-my-pi/blob/main/docs/task-agent-discovery.md)、
  [Task tool](https://github.com/can1357/oh-my-pi/blob/main/docs/tools/task.md)、
  [Oh My Pi repository](https://github.com/can1357/oh-my-pi)、
  [omp.sh](https://omp.sh/)。

## 相关页面

- [安装](/zh/installation) — 维护者 clone 与论文项目 skill 安装，含 `paper-audit` 同级布局
- [使用指南](/zh/usage) — 安装后的跨技能路由
