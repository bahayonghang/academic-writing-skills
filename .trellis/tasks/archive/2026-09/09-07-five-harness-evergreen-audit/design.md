# 设计：五工具共享项目事实，按真实能力执行

## 边界与决策

这是审查后待批准的最小改造设计。本轮只产出任务材料；产品、正式规则、CI 与知识回写均在后续批准后实施。用户已明确许可方向为“仅限学术、禁止商业使用”，不改成 MIT，不自行扩写法律条款。

项目的六个独立 skill、按技能携带的 Python 副本、现有语义/哈希对齐测试、源资源→双语镜像→manifest 链路继续作为既有设计基础。没有证据支持把它们重构成共享框架。75 个 Pyright warning 作为既有基线，不纳入批量清理。

## 三个不能混同的层次

1. **项目规则**：AGENTS.md 保存仓库维护的共同事实、权限边界、入口与门禁；CLAUDE.md 引用共同规则并只保留 Claude 加载差异。
2. **Skill 使用**：SKILL.md 与包内 references 保证搬到论文仓库后仍可使用，不能依赖这个开发仓库的私有绝对路径或本机全局配置。
3. **Harness 能力**：工具发现、委派 API、hook/扩展、权限与模型选择属于执行器；能力须在当前会话确认，Markdown 的 allowed-tools 不等于所有平台都强制执行的权限。

团队可分享的事实入口是版本控制中的文档。当前 `.claude/`、`.codex/`、`.agents/`、`.cursor/` 均被忽略且没有 tracked 文件；它们只是本机环境证据。最小方案保留这种本机边界，在已跟踪 AGENTS/CLAUDE 和新增双语 harness 指南中写明显式读取与接入步骤。**不批量纳入个人配置、不引入自动配置器、不为凑齐五套创建空目录或假 hook。**

## 子任务与所有权

| ID | 子任务 | 优先级 | 独占主要文件 | 前置 |
|---|---|---|---|---|
| C1 | `09-07-harness-project-contract` | P1 | AGENTS.md、CLAUDE.md、README.md、README_CN.md、pyproject.toml 的描述/许可字段 | 批准 |
| C2 | `09-07-harness-ci-gates` | P1 | .github/workflows/ci.yml（新增）、justfile、pyproject.toml 的 pytest 配置 | C1（共享 pyproject 顺序编辑） |
| C3 | `09-07-harness-audit-encoding` | P1 | paper-audit/scripts/audit.py、tests/skills/paper_audit/test_paper_audit_integration.py | 批准；与 C1/C2 可独立 |
| C4 | `09-07-harness-onboarding` | P1 | docs/installation.md、docs/zh/installation.md、docs/harnesses.md（新增）、docs/zh/harnesses.md（新增）、docs/.vitepress/config.ts、tests/skills/paper_audit/test_installed_layout.py（新增）；paper-audit/SKILL.md 安装依赖段及两语入口 | C1/C2/C3 |
| C5 | `09-07-harness-skill-portability` | P2 | 六个 SKILL.md；paper-audit/references/workflow-detail.md、SUBAGENT_TEMPLATES.md、editorial_decision_standards.md；paper-audit/agents/synthesis_agent.md；对应双语页与资源 manifest | C4（顺序编辑paper-audit入口） |
| C6 | `09-07-harness-validation-closeout` | P2 | 新增 .trellis/spec/academic-writing-skills/harness-workflow-contract.md、spec index；父子任务验收记录；必要时校准双语 harness 指南的状态列 | C1–C5 |

README 用户原有模型推荐改动不属于 C1 修改内容；实施前重新记录实际 diff，仅处理该子任务拥有的说明段落。任务树只表示归属，上表和各子任务 implement.md 才表示依赖。

问题到工具的唯一映射见 implement.md 的 C1–C6 批准表（“适用 harness / 证据状态”列）：区分本轮已执行取证与仅有文档能力依据的候选路径；不以工具品牌判定强弱或费用。各子任务沿用该表，不在自身文档另造不一致的工具排名。

## 具体设计

### 共享规则和说明（C1）

AGENTS.md 说明六技能根目录、规范与公开资源来源、`just ci` 的真实四段门禁、文档门禁、规划/实施授权边界、学术事实保护与便宜模型不能自行提升范围。CLAUDE.md 使用 Claude 支持的导入方式引用该文件，删除旧 v3、MIT 和重复维护的规则描述。其他 harness 用原生 AGENTS 发现或明确读取路径；不假设 Claude 导入语法在其他平台通用。README 的 PDF 依赖改为当前 PDFParser 的 PyMuPDF / 可选 pymupdf4llm，版本取源元数据，不增新版本文件。pyproject 保留现有学术用途方向并移除冲突 MIT classifier，不发明新的许可证标识。

### CI 与测试发现（C2）

以 pytest 配置作为唯一测试发现来源，覆盖 `tests` 与 `academic-writing-skills`；just test 调用相同入口，避免一处手工 glob、一处漏测。变更前后用收集到的 node-id 集合对比，已知现状为默认 1714 vs just test 1756，相差 42。新增 PR/push 检查工作流，Python 覆盖 Windows/Ubuntu 与最低支持版 3.10/当前本地版 3.13；所有矩阵单元复用 just ci。独立文档 job 采用与现有 Pages 一致的 Node 20，使用 docs/package-lock.json 的 npm ci，运行资源同步和 docs build。Python 环境使用 uv.lock 的冻结同步。保留 release-only 的 deploy.yml 和生产权限，不触发部署；仓库保护规则和线上 required checks 不在本轮授权内。

CI 从干净 runner 的供给步骤明确写入 C2 implement.md：setup-python@v7、setup-uv@v10.0.1、setup-just@v4，uv0.12.10/just1.58.0，并将 UV_PYTHON 绑定到matrix。不能依赖本机工具或 runner 未承诺的预装项。

### 编码协议（C3）

只在 `_run_check_script` 这个可信的本仓库 Python checker 边界指定 UTF-8 输出与管道解码：复制当前环境并设置子进程 PYTHONIOENCODING=utf-8，subprocess 明确 encoding=utf-8。不修改全局环境，不把 decode 错误当空输出成功。保留超时、returncode、stdout/stderr 及已有 issue 解析接口。真实 subprocess 回归覆盖中文/标点，Windows 增加 PYTHONUTF8=0 与仅 PYTHONIOENCODING=utf-8 的场景；本地原始命令不崩溃是必要验收。

### 安装与工具指南（C4）

新增一个双语五工具能力矩阵，明确维护本仓库与在论文项目安装 skill 是不同路径。所有平台有共同的显式读取 AGENTS/SKILL/ref 步骤；分别写明原生发现、上下文加载、委派和权限限制，附日期与官方来源。CLI 已安装不作为运行通过证据。对 paper-audit 明示完整审查需要同级 writing skills，给出完整集合的复制布局；隔离 smoke 必须证明完整布局无意外 script-not-found。单 skill 模式标为受限覆盖，本次不改变其既有 exit/gate 语义，不新增 installer 或复制全部 sibling 脚本。npx 安装器及 symlink 布局没有实测前标为 UNVERIFIED。

安装完整能力的 sibling 要求也必须写入 C4 拥有的 paper-audit/SKILL.md 依赖段及两语入口；C5 在 C4 完成后顺序修改该入口，不能只修安装站而遗漏安装后的权威说明。

### 跨工具执行与模型分工（C5）

保留 Claude frontmatter 元数据，但六技能明确脚本与语义契约不依赖 Read/Bash/Task 的字面名称；映射到会话现有 read/search/exec/delegate 能力。paper-audit 的 lane 必须保留输入证据、只读范围、预期输出和 provenance。有原生委派则按独占范围并行；没有委派则顺序完成同一检查视角，并注明不是多个独立 reviewer。自动 deterministic fallback 不得声称实际调用了其他模型。不给技能新加模型 provider、费用规则引擎或配置项。

强模型决定根因、学术证据与严重度、权限边界、降级语义和最终验收；较便宜模型只执行已批准且有明确文件/测试边界的机械修改。任务包出现新接口、跨目录扩张、学术结论变化或失败原因超出计划时立即回主审。

报告/overall_assessment 用正文明确 native delegated 或 sequential single-agent；后一种不得称 independent panel，CONSENSUS 只代表同一会话跨视角一致。synthesis agent 与 editorial decision standards 的解释同步，但不改现有 JSON schema、阈值或评分。无真实 reviewer 执行的 deterministic fallback 明确标脚本回退。

### 验收与回写（C6）

记录每个平台版本/模型、入口、加载证据、是否真实委派、测试命令及退出结果。静态规则审查、隔离 CLI、真实新会话是三类独立证据。真实会话、付费模型、全局 hook 授权、安装工具需在相应既有授权内进行；缺少环境则保持 UNVERIFIED，不以脚本或文案测试替代。能完成共同项目规则与指南不等于五平台已全量实测，关闭状态必须明确是哪类验收。

批准经验最终写入项目 spec 并注明五套工具适用范围，包含编码协议、安装边界、测试入口、委派和证据判定；公开用户指南同步对应事实。本方案选择项目知识库作为回写位置，不默认写入全局 Basic Memory。

推荐批准范围是“静态规则与隔离脚本交付”：C1–C5验收通过，C6的共同门禁/完整台账/回写/范围保护均通过即可关闭该范围。台账内可选的真实五工具运行项保持独立状态，未执行记UNVERIFIED；它们不是隐藏的静态验收阻断，也不因此获得“运行验证通过”结论。

## 回退与非目标

各子任务按自己的 diff 回退；源资源与双语镜像/manifest 同进同退。不可回退用户 README 原有模型推荐改动。无需兼容层、数据库、发布自动化平台或新依赖。历史 VitePress 死链接已经修复，不重复修旧 commit。价格和模型可用性使用当次配置事实，不写永久排名。
