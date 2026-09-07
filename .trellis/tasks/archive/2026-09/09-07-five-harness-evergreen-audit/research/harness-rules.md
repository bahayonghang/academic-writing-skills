# Research: 五套 harness 的项目规则、发现与委派边界

- Query: 审查 Claude Code、Codex、Grok Build、Kimi Code、Oh My Pi（OMP）的项目入口、skill 发现、委派、权限与上下文机制，并给出强模型/便宜模型分工及最小改造计划
- Scope: internal + official primary documentation
- Date: 2026-09-07 (Asia/Shanghai)
- Local repository: branch `dev`, HEAD `f32fa909971b6975820dc4ad5565c278d5496b62`
- Planning boundary: 只写本研究文件；没有修改项目说明、平台配置、产品 skill、全局设置，也没有启动付费模型会话

## 结论

> 主线程范围裁决：本文“改造计划”章节是研究候选，不是已选实施清单。最终优先级、文件范围、验收与依赖以父任务 design.md / implement.md 和六个子任务为准。本次采纳共享 AGENTS、Claude 薄入口、公开事实修正、双语能力表及真实证据边界；不采纳批量跟踪/生成平台 adapters、gitignore allowlist、模型路由配置、matrix schema 验证器或上游 Trellis 改造。文中的 P0 候选在最终计划中按实际影响定为 P1/P2；Ruff py39 是较低语法目标，不是已经复现的 Python3.10 运行错误，本次不改。

当前项目不能把“本机五套 harness 都可维护”当作成立事实。根 `AGENTS.md` 与
`CLAUDE.md` 已跟踪，但 `.gitignore:2,86-88` 忽略 `.claude/`、`.agents/`、
`.codex/`、`.cursor/`；`git ls-files` 证明这些平台目录没有进入版本库。Grok、Kimi、
OMP 的原生项目目录 `.grok/`、`.kimi-code/`、`.omp/` 当前不存在。新克隆只能得到两份
根规则文件，得不到本机 Trellis skills、agents、hooks、commands 或 OMP extension。

根规则本身也不一致。`AGENTS.md:1-27` 是简洁的当前仓库约定，`:28-48` 是 Trellis
管理块；`CLAUDE.md:5-108` 复制了一套更长的仓库说明，却在 `:7` 声称 v3.0.0、六个
skill、Claude Code 专用安装和 MIT。当前 `pyproject.toml:3` 是 6.0.0，README 已列六个
skill，但安装入口是跨 harness 的 `npx skills add`，且用户已决定保留
`README.md:156-158` 的 “Academic Use Only — Not for commercial use”。
`pyproject.toml:24` 的 MIT classifier 也冲突。Claude 官方明确说明 Claude Code 读取
`CLAUDE.md` 而不读取 `AGENTS.md`，并推荐用 `@AGENTS.md` 导入来共享单一规则源；因此
`CLAUDE.md` 应成为很薄的 Claude 适配入口，而不是第二份仓库手册。

本次还确认两项公开说明漂移：`README.md:106` / `README_CN.md:92` 声称 PDF 审查需要
`pdfplumber`，但 `paper-audit/SKILL.md:32-33` 与 `paper-audit/scripts/pdf_parser.py:79-131`
实际使用可选 `pymupdf` / `pymupdf4llm`；`pyproject.toml:50` 的 Ruff target 为 py39，
而 `pyproject.toml:6`、`AGENTS.md:18` 均以 Python 3.10+ 为项目契约。这些属于项目说明
一致性问题，不应塞进某个 harness 私有规则。

## 证据边界

### 已验证的本机状态

- CLI 可执行版本：Claude Code 2.1.263、Codex 0.153.4、Grok Build 1.0.22、Kimi Code
  0.41.0、OMP 18.1.12、Trellis 0.7.0-beta.3。
- `omp` 的 PowerShell wrapper 指向 npm 包
  `@oh-my-pi/pi-coding-agent/dist/cli.js`；其 help、官网 `omp.sh` 和源仓库
  `can1357/oh-my-pi` 一致。这里的 OMP 是 **Oh My Pi**，不是本机另一个 `pi`
  命令（`@earendil-works/pi-coding-agent`）。
- `trellis platforms` 只报告当前项目已配置 Claude Code、Cursor、Codex；
  `trellis init --help` 同时提供 `--grok`、`--kimi`、`--omp` 生成入口。
- `grok inspect` 是本轮唯一完整、无模型调用的项目发现握手：它识别了根
  `Agents.md`、`Claude.md`（Windows 大小写等价）、13 个项目 Trellis skills、3 个
  项目 Trellis agents；还显示 Claude 兼容 hooks 被用户配置关闭。因此只能说当前
  working copy 的 Grok 规则/skill/agent 发现已验证，不能说 Trellis hooks 已执行。
- `kimi doctor` 仅证明用户级 `config.toml` 与 `tui.toml` 可解析；它没有验证项目
  `AGENTS.md`、skills、agents 或委派。
- `omp read skill://trellis-start` 返回 `Unknown skill` / `Available: none`。该独立
  `read` 子命令可能没有建立完整交互会话，所以这是一次失败的非模型发现探针，不能
  推导 OMP 交互会话也必然失败。
- 当前 Codex 会话确实收到了项目 `AGENTS.md` 与项目 Trellis skill 目录清单，但没有
  另起全新 Codex 进程验证 `.codex/hooks.json` 的授权、事件触发或 subagent context
  注入。

### 明确 UNVERIFIED

- Claude Code 的 `/context` 新会话是否列出修订后的 `CLAUDE.md`、项目 skills/agents，
  以及项目 hooks 是否获信任并触发。
- Codex 新会话的 AGENTS chain、项目 skill/agent 发现与四类 hook 的真实触发。
- Kimi Code 新会话的项目 `AGENTS.md`、`.agents/skills`、`.kimi-code/agents` 发现以及
  Agent/AgentSwarm 的委派。
- OMP 新会话的 standalone `AGENTS.md`、`.agents/skills`、`.omp/agents` 和 Trellis
  extension 注入。
- `npx skills add` 在五套 harness 上的真实复制/软链布局与 trigger 准确率。本仓库的
  1756 个 pytest 通过只证明静态契约和脚本行为，不运行真实模型 trigger eval；详见
  `research/test-baseline.md:27-32`。

## “安装使用”与“维护本仓库”是两层契约

| 层面 | 权威内容 | 项目应说明什么 | 不应混入什么 |
|---|---|---|---|
| 用户安装并使用 academic skills | `academic-writing-skills/<skill>/SKILL.md`，README 只负责选择与安装路由 | 支持的安装命令、harness 发现位置、可选依赖、每个 skill 的输入/输出边界 | Trellis task lifecycle、维护者 agents/hooks、便宜 worker 策略 |
| 贡献者维护本仓库 | `AGENTS.md` + `.trellis/` + 已跟踪的平台 adapters | 构建/测试、任务流程、生成文件所有权、五套 harness 的启动/验证方法 | 将某个 harness 名称写成模型或价格保证 |

Harness 是运行与配置层；模型/推理强度/价格是每次会话或 agent 的路由选择。README 的
“推荐模型”是动态建议，不能当作固定的 harness 能力声明，更不能由此推断某 harness
一定便宜或一定更强。

## 五套 harness 能力矩阵

| Harness | 项目规则入口 | Skill 发现 | 委派与上下文 | 权限边界 | 当前项目状态 |
|---|---|---|---|---|---|
| Claude Code | 原生 `CLAUDE.md`；官方建议 `@AGENTS.md` 复用共享规则 | 项目 `.claude/skills/<name>/SKILL.md`；skill 正文按需加载 | 项目 `.claude/agents/*.md`；`SubagentStart`/`PreToolUse` 等 hooks 可注入上下文 | CLAUDE 是指导性 context；真正阻断要用 settings/PreToolUse hook，项目 hooks 需信任 | 根 `CLAUDE.md` 已跟踪但未导入 AGENTS；本机 `.claude` 完整但被忽略，team clone 缺失；运行未验 |
| Codex | 根到 cwd 的 `AGENTS.md` chain，近层后加载 | 项目根到 cwd 的 `.agents/skills`，先注入 name/description，再按需读 SKILL | `.codex/agents/*.toml`；`SubagentStart` 等 hooks 支持 additionalContext | sandbox/approval 来自运行时与 agent config；本项目 comments 说明 hooks 还依赖用户级启用和一次审查 | 根 AGENTS 已跟踪；本机 `.agents/.codex` 被忽略；当前会话只部分验证，fresh session/hook 未验 |
| Grok Build | 官方可同时读 AGENTS family 与 CLAUDE family | 原生 `.grok/skills`，也兼容 Claude skills/plugins | 内置 general-purpose/explore/plan + `.grok/agents`；当前官方已有 project hooks | permissions/mode/sandbox 与规则 prompt 分层；项目 hooks 要 `/hooks-trust` | `grok inspect` 验证当前 working copy 借 Claude/Codex 兼容层发现 skills/agents；`.grok` 缺失；Claude hooks 当前禁用 |
| Kimi Code | `AGENTS.md` 作为参考 context；agent system prompt 是另一层 | 项目 `.kimi-code/skills` 与 `.agents/skills`，Project > User > Extra > Built-in | 内置 coder/explore/plan；现行官方也支持 `.kimi-code/agents` 与 `.agents/agents` 自定义 agent；独立 child context | 每次 dispatch 通常出现批准，除非 allow rule/Ask When Needed；agent tools/disallowedTools 可限权 | 仅用户 config doctor 通过；项目 `.kimi-code` 缺失且 `.agents` 被忽略；项目发现/委派未验 |
| OMP (Oh My Pi) | 推荐 `.omp/AGENTS.md`；也兼容 standalone `AGENTS.md`/`CLAUDE.md`，同深度按 provider priority 去重 | 启动时只放 metadata，正文通过 `skill://` 按需读取；`.omp/skills` 优先，`agents` provider 也读 `.agents/skills` | `task` tool；项目 `.omp/agents/*.md`；agent 可设 model/effort/spawns/prewalk，extension 可监听 session/context/tool events | `--approval-mode`、agent tool list、spawn depth 与 model role 分层 | 精确产品身份已验；`.omp` 缺失；独立 read 探针未发现 skill；交互 discovery/extension 未验 |

## 官方文档依据（2026-09-07 快照）

### Claude Code

- [Memory / CLAUDE.md / AGENTS.md](https://code.claude.com/docs/en/memory)：项目
  `CLAUDE.md` 应进入版本控制；Claude 不原生读 AGENTS，推荐 `@AGENTS.md` 导入；
  `/context` 可验证实际加载。
- [Skills](https://code.claude.com/docs/en/skills)：项目 skill 路径与发现/按需加载。
- [Subagents](https://code.claude.com/docs/en/sub-agents)：项目 `.claude/agents` 应跟代码
  共享，且 agent 可单独配置 model。
- [Hooks](https://code.claude.com/docs/en/hooks)：`PreToolUse`、`SubagentStart` 等事件。

### Codex

- [AGENTS.md](https://developers.openai.com/codex/guides/agents-md)：每次 run 构建
  global→project→cwd instruction chain，并给出验证命令。
- [Skills](https://developers.openai.com/codex/skills)：progressive disclosure 与项目
  `.agents/skills`。
- [Subagents](https://developers.openai.com/codex/subagents)：agent model/reasoning 可继承或
  显式配置；官方将强模型用于复杂多步工作，将 Terra/Luna 一类用于扫描和窄执行。
- [Config reference](https://developers.openai.com/codex/config-reference)：hooks 表和
  SessionStart/SubagentStart/UserPromptSubmit/PreToolUse 等事件 schema。

### Grok Build

- [Skills, plugins, marketplaces](https://docs.x.ai/build/features/skills-plugins-marketplaces)
  （官方页标注 updated 2026-08-11）：原生 `.grok/skills`、项目 hooks、Claude Code 与
  AGENTS family 兼容。
- [Subagents](https://docs.x.ai/build/features/subagents)（updated 2026-07-21）：内置
  general-purpose/explore/plan 与 `.grok/agents`。
- [Permissions](https://docs.x.ai/build/features/permissions)：mode、project permission
  与 sandbox 的边界。

### Kimi Code

- [Skills](https://moonshotai.github.io/kimi-code/en/customization/skills)：项目
  `.kimi-code/skills` + `.agents/skills` 及优先级。
- [Agents and sub-agents](https://moonshotai.github.io/kimi-code/en/customization/agents)：
  coder/explore/plan、项目 `.kimi-code/agents` + `.agents/agents`、tool allow/deny 与
  override 风险。
- [Configuration](https://moonshotai.github.io/kimi-code/en/configuration/config-files)：
  `secondary_model` 明确用于通常较便宜的 subagent pool，并支持 per-spawn model。

### OMP

- [Context files](https://github.com/can1357/oh-my-pi/blob/main/docs/context-files.md)：
  `.omp/AGENTS.md`、standalone AGENTS/CLAUDE 兼容、provider priority 与注入顺序。
- [Skills](https://github.com/can1357/oh-my-pi/blob/main/docs/skills.md)：启动时 metadata、
  `skill://` 按需正文、`.omp`/agents/codex providers 与 one-level layout。
- [Task agent discovery](https://github.com/can1357/oh-my-pi/blob/main/docs/task-agent-discovery.md)：
  `.omp/agents`、model role、effort、spawns、prewalk。
- [Task tool](https://github.com/can1357/oh-my-pi/blob/main/docs/tools/task.md)：独立 child
  session、batch/background、并发与隔离边界。
- [Oh My Pi repository](https://github.com/can1357/oh-my-pi) 与
  [omp.sh](https://omp.sh/)：产品身份与 CLI 名称。

## 本机 Trellis 模板与现行 harness 文档的漂移

以下路径属于已安装 npm 包的 **source templates**，不是本仓库当前 active config，不能
直接修改来完成项目适配：
`C:/home/lyh/.npm-global/node_modules/@mindfoldhq/trellis/dist/{configurators,templates}`。
`trellis init/update` 生成到项目目录后，`.trellis/.template-hashes.json` 才记录模板基线；
项目自定义应改生成文件并让 update 识别 drift，不应手改 hash。

1. `dist/configurators/grok.js:4-11` 仍把 Grok 定义为 “no hooks”，依据是旧 0.2.x；
   Grok 1.0.22 官方已支持项目 `.grok/hooks`。现有 pull-based agent 仍可作为兼容实现，
   但 Trellis meta 文档不能继续把“无 hooks”写成当前产品事实。
2. `dist/configurators/kimi.js:15-18` 与 `dist/templates/kimi/index.js:11-14` 仍称 Kimi
   没有项目 custom agents；Kimi 0.41 官方已支持 `.kimi-code/agents` 与
   `.agents/agents`。现有“agent prompt 作为 skill，再派 built-in coder”的做法可能仍可
   工作，是否迁移到 custom agents 应由真实委派 smoke 决定，不能只因新能力存在就重构。
3. `dist/configurators/omp.js:5-25` 生成 `.omp/commands`、`.omp/skills`、`.omp/agents`
   和 TypeScript Trellis extension，与 OMP 18.1.12 的原生 provider/extension 方向一致；
   但项目当前没有生成或跟踪这些文件。
4. 本项目 `.agents/skills/trellis-meta/references/platform-files/platform-map.md:26-27`
   复制了上述旧 Grok/Kimi 能力判断；`:96-111` 的 OMP 路径描述较接近现状。由于整个
   `.agents` 被忽略，这份 meta 又只存在于当前 working copy，不能视为团队规则。

## 强模型与便宜模型分工

模型路由必须按工作风险和判断难度决定，不能按 harness 品牌决定。

| 工作 | 默认责任 | 便宜 worker 的输入与边界 | 升级/复核条件 |
|---|---|---|---|
| 规则所有权、AGENTS/CLAUDE 冲突、license 意图、跨 harness capability 解释 | 强模型规划 + 独立强模型审查 | 只可收集文件、行号、官方 URL、版本输出 | 任一语义冲突、法律/发布含义、官方文档漂移 |
| 生成/同步 Grok、Kimi、OMP adapters | 便宜模型执行 | 已批准的文件清单；只改平台目录和对应 docs/tests；不得改全局 config | 生成器冲突、需决定 pull/hook/custom-agent 架构、真实发现失败 |
| CLAUDE 去重、README 双语同步、依赖名修正 | 便宜模型执行 | 强模型给出 canonical 文本和配对文件；执行精确替换 | 中英含义分叉、license 文案需要新条款、安装范围改变 |
| gitignore allowlist、hook 权限、agent tool/sandbox/model frontmatter | 强模型设计；便宜模型按清单修改 | 精确路径与预期 discover output；不新增用户级开关 | 可能泄露 local settings、扩大 write/network 权限、递归委派 |
| 静态/CLI smoke、hash/diff/docs-sync | 便宜模型执行 | 命令、预期退出码、不得调用模型/写全局状态 | 任何失败、发现结果与预期不符、需要安装/登录/付费调用 |
| 新会话真实加载/委派验收 | 各 harness 的真实运行时；强模型复核证据 | 固定无害 fixture、限制写目录、记录版本/输出；费用需单独授权 | 触发外部写、凭据/登录、付费模型试跑或权限扩大 |

## 按优先级的最小改造计划

### P0：建立团队可克隆的单一规则链

1. `AGENTS.md`：保留为跨 harness 的仓库规则真源；只补充项目级 evergreen 约定，例如
   安装使用与维护 harness 分层、生成文件所有权、五 harness 验证台账入口。不要复制各
   harness 的动态能力表到五处。
2. `CLAUDE.md`：首行导入 `@AGENTS.md`；删除已在 AGENTS/README/skill 中有真源的长篇
   重复，只保留 Claude 专属加载/验证提示。删除 v3.0.0、Claude-only、MIT 等错误声明。
3. `.gitignore`：用明确 allowlist 让经批准的 `.claude`、`.agents`、`.codex`、`.grok`、
   `.kimi-code`、`.omp` adapter 进入版本库；继续忽略 `.claude/settings.local.json`、
   session/cache/auth 等用户态文件。禁止简单删除所有 ignore 后把本机私有配置全收进来。
4. 用当前项目 Trellis CLI 的 `--grok --kimi --omp` 生成候选，再逐文件审查；Claude/Codex
   现有生成文件要先与 template hash 对比，保留项目定制。若决定修 Trellis 上游能力表，
   另开上游变更；本项目完成不依赖修改全局 npm 包。

必须通过：`git check-ignore -v` / `git ls-files` 对批准路径的断言；`git diff --check`；
`trellis platforms` 包含五套目标；`task.py validate`；敏感/本机路径扫描；CLAUDE 新会话
`/context`、Codex fresh session、`grok inspect`、Kimi fresh session、OMP fresh session 的
逐项发现台账。没有 handshake 的项继续标 `UNVERIFIED`。

### P0：修正公开事实与 license 冲突

文件：`CLAUDE.md`、`README.md`、`README_CN.md`、`pyproject.toml`，必要时现有 docs 对应页。

- 以用户已确认的 “Academic Use Only / noncommercial” 意图为准，删除 MIT classifier 与
  CLAUDE MIT 声明；不擅自起草新许可证条款。若发布系统要求合法 license 文件或 SPDX，
  这是单独的法律文本决策。
- 把 PDF 依赖修为实际的 `pymupdf` / enhanced `pymupdf4llm`，与 SKILL 保持一致。
- 统一 Python target（至少消除 pyproject 的 py39 与项目 3.10+ 契约冲突）。
- README 平台表述应区分“安装兼容已验证”与“维护 harness adapter 存在”。未跑真实安装
  smoke 的 Grok/Kimi/OMP 不写成已验证支持。

必须通过：版本/依赖/license 文本检索；`just check-versions`；README 中英配对契约；
`uv run --extra dev python docs/scripts/check_resource_sync.py`；`just doc-build`；相关
paper-audit PDF import tests。license 的法律完备性不由 pytest 证明。

### P1：按 harness 生成并校准 Trellis adapters

- Claude：`.claude/skills`、`.claude/agents`、hooks + settings；保持 agent 无 hook 时的 pull
  fallback。只跟踪 `settings.json`，不跟踪 `settings.local.json`。
- Codex：`.agents/skills`、`.codex/agents`、`.codex/hooks.json` 与脚本；项目 config 只放
  project-valid keys，不试图替用户启用 feature/trust。
- Grok：先保留可工作的 pull-based agents；修项目 meta 中“无 hooks”的绝对陈述。只有
  当真实 hook smoke 证明 stdout/additionalContext 契约满足 Trellis 后，才迁移为 hook
  注入。
- Kimi：先验证 Trellis 当前 commands-as-skills + built-in coder 路径；再比较原生 custom
  agents。迁移条件应是上下文/权限/发现收益，而不是“新 API 存在”。
- OMP：生成 `.omp/commands`、skills、agents、extension；确认 extension 的 Python 命令在
  Windows 可用。不要与独立 Pi `.pi` adapter 混用。

必须通过：template/source 与生成文件清单核对；skills frontmatter 解析；三个 agent 的
职责/写权限/递归边界 parity；每平台一次无害 discover + dispatch smoke；hook/extension
分别记录“发现、获信任、触发、注入”四级证据，不能只记录文件存在。

### P1：为能力漂移建立单一台账与检查

新增一份维护者文档作为五 harness matrix 真源，README 只链接和展示经验证支持级别。
台账每行包含：harness/CLI 版本、官方文档快照日、instruction path、skill path、agent
path、hook/permission 要求、安装 smoke、discovery smoke、delegation smoke、证据状态。
静态测试只检查已批准的路径、frontmatter、文档链接与无矛盾；不要把模型判断硬编码为
封闭 alias 表或将版本推荐写死为永久能力。

必须通过：matrix schema/链接检查、生成文件 drift 检查、docs sync/build。周期性检查可
报告 drift，但自动升级 harness 或写用户全局配置仍需单独授权。

### P2：实现成本分层的 agent 路由

在各平台的 agent 配置中使用语义角色（plan/review/worker 或平台等价物），把具体模型映射
留在支持该能力的平台/用户配置层。项目 agent contract 固定任务、工具、写目录、升级条件
和最终强模型复核，避免把某个随时变化的型号写进共享 AGENTS。先做静态配置与 dry-run；
真实付费比较、性能基准和质量 A/B 仍需另行授权。

## 建议验收顺序

1. 先完成 P0 规则链、gitignore allowlist 与公开事实修正。
2. 再生成五套 adapter 候选，先静态校验，再逐 harness 做 fresh-session discovery。
3. discovery 通过后才做无害 delegation/context smoke；权限或 hook 未获信任时记录具体
   `UNVERIFIED`，不通过扩大用户全局权限来“修绿”。
4. 最后只跑一次 `just ci`、resource sync、docs build；只有新失败或未决风险才重复。
5. 由强模型复核：规则是否仍只有一个真源、五套差异是否被保留、便宜 worker 是否被
   文件边界和升级条件约束、任何“支持”声明是否都有对应 runtime handshake。

## Caveats / Not Found

- 没有找到项目 `.grok/`、`.kimi-code/`、`.omp/`；这不是“平台不支持”，只是当前项目
  未生成原生 adapter。
- 没有运行 `trellis init/update`，所以本文没有修改 template hashes 或生成候选。
- 没有运行任何 harness 的真实模型调用、安装器或外部写操作。
- Grok/Kimi 的当前官方能力比 Trellis 0.7.0-beta.3 模板说明更新。本文只建议先校准事实
  与运行证据，不要求为追新能力立刻改架构。
