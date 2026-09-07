# 常青维护与五套 Harness 审查报告

日期：2026-09-07。对象：academic-writing-skills，dev@f32fa909971b6975820dc4ad5565c278d5496b62。

**结论：现有自动门禁通过，但项目说明与五套 harness 尚未对齐；新增边界复现找到了 Windows 子进程崩溃和独立安装覆盖下降。** 建议批准六个子任务的有限改造，不做整体重构。

本轮为强模型规划/审查：主线程协调，agent_skill_architect 检查能力与规则，quality_release_auditor 检查 CI/历史失败；独立规划复核另记于本任务证据。便宜模型没有参与本轮判断。用户原有 README 模型推荐改动未更改。

独立强模型规划复核：**GO，0项剩余阻断**。初审6项修订及闭环见 [planning-review.md](research/planning-review.md)。当前仍等待用户批准实施，父子任务全部保持planning。

## 项目结构和关键链路

- 六个产品 skill 位于 `academic-writing-skills/`：latex-paper-en、latex-thesis-zh、typst-paper、bib-search-citation、cover-letter、paper-audit。SKILL.md 路由到包内 scripts/references/evals；该目录不是 harness 的维护配置目录。
- `paper-audit/scripts/audit.py` 负责 checker 执行与报告流程；部分 checker 解析到同级 writing skills。parser/de-AI/写作模块保留按技能副本，并由 `tests/contracts/` 的对齐测试保护，不建议无证据抽成共享库。
- `tests/skills/`、`tests/contracts/`、`tests/shared/` 与 bib-search-citation 的内置 tests 是不同发现路径。justfile 与 pytest 默认配置当前不一致。
- 公开资源从 skill 源经 `docs/resource-manifest.json` 同步到英文/中文 docs，由 `docs/scripts/check_resource_sync.py` 校验，VitePress 构建检查页面链接。
- `.github/workflows/deploy.yml` 只有 release 文档部署；没有普通 PR/push 的项目质量检查。
- AGENTS/CLAUDE 是 tracked 入口；本机 .claude/.codex/.agents/.cursor 均被忽略，Grok/Kimi/OMP 的原生目录缺失。不能从本机文件存在推导团队 clone 已获得原生适配。

## 已执行检查

| 检查 | 结果 |
|---|---|
| just ci | 退出0；版本一致、Ruff通过；Pyright 0 errors / 75 warnings；1756 passed / 0 failed / 0 skipped |
| 默认 pytest 收集 | 1714，较 just test 少42项 bib-search-citation 测试 |
| 全量资源同步 | 271 manifest entries 通过 |
| just doc-build | VitePress 1.6.4 通过，18.90s |
| git diff --check | 既有 README_CN.md:14 行末双空格报错；用户原有修改保留 |
| 编码对照 | 默认环境成功；仅 PYTHONIOENCODING=utf-8 崩溃；完整 UTF8 mode 成功 |
| 安装布局对照 | 完整 checkout RUN11/missing0；只有 paper-audit 时 RUN3/missing8，均在 UTF8 mode 下 |
| Trellis 结构 | 父+6子均有规划三文档/两份实际上下文清单；7份 validate通过，机械预检0阻断 |

具体命令、环境及原始输出见 [test-baseline.md](research/test-baseline.md) 和 [runtime-findings.md](research/runtime-findings.md)。新增复现并未修改产品代码；现有1756测试没有覆盖该 Windows 环境组合。

## 优先级与证据

| ID | 发现及影响 | 代码/说明证据 | 计划归属 |
|---|---|---|---|
| F1 / P1 | Windows stream UTF8 + locale GBK 会崩溃 | `audit.py:686-692` 未约定管道编码，`:611/:618` 对 None 调用 strip；真实调用栈已保存 | C3：成对固定 Python checker 输出/读取编码及真实 subprocess 回归 |
| F2 / P1 | 单 skill 安装可成功但检查覆盖下降 | `audit.py:398-402,495-507,2757-2760` 依赖 sibling 且 missing 继续；`docs/installation.md:24-40` 未提前说明 | C4：清楚说明完整集合布局并执行 isolation smoke，不改既有降级/gate语义 |
| F3 / P1 | 普通提交缺少自动质量门禁 | `.github/workflows/deploy.yml:3-6,40-44`；近10 runs无当前 dev SHA | C2：新增 PR/push CI，复用现有测试/完整资源/构建命令 |
| F4 / P1 | 共同说明漂移，五工具维护接入未形成可复现说明 | `CLAUDE.md:7` v3/MIT；`pyproject.toml:3,24`；`.gitignore:2,86-88`；各工具忽略/缺失目录 | C1/C4：共同规则+薄入口+有来源/日期的能力说明 |
| F5 / P2 | 文档推荐默认 pytest 漏42项；local ci 不含全量 docs target 检查 | `pyproject.toml:88-92`、`justfile:107-110`、`docs/installation.md:52-59`；docs契约测试只校验 inventory 子集 | C2/C4：统一发现，CI单列 full sync+build；文档明确 Python 门禁与文档门禁 |
| F6 / P2 | 静态技能元数据和真实委派证据容易混同 | 六个 SKILL 的 allowed-tools；`tests/contracts/test_trigger_evals.py:1-9` 不调用真实模型；audit.py deterministic fallback | C5/C6：适配现有能力、保留 provenance、顺序执行不冒充独立审查 |
| F7 / P2 | PDF 依赖说明不符代码 | `README.md:106` / `README_CN.md:92` 写 pdfplumber；PDFParser实际 lazy import PyMuPDF/pymupdf4llm | C1：修正安装说明，无需依赖升级 |

许可方向已由用户明确为“仅限学术、禁止商业使用”。C1 将统一冲突声明，不将其改为 MIT，也不编造新许可证条文。README 两处推荐模型改动由用户持有，本轮与未来 C1 都须保留。

## 历史失败工作流的根因

[run 27467312342](https://github.com/bahayonghang/academic-writing-skills/actions/runs/27467312342) 在 2026-06-13 的旧 SHA `73e428d` 失败：中英文 template 页面均指向不存在的 `../templates/index`。提交 `7913cbb` 改为四个具体模板链接后，[run 27467927802](https://github.com/bahayonghang/academic-writing-skills/actions/runs/27467927802) 成功。它是**已修复的历史故障**，不是当前失败。详细命令和原始错误摘录见 [ci-workflow.md](research/ci-workflow.md)。

预防机制是让完整资源检查与 VitePress build 在 PR/push 检查阶段执行，不重复修改已修链接。新增 workflow 不自动保证 branch protection 或 release tag 只引用已通过的 SHA；这些需要独立的远端授权和证据。

## 五套 Harness 的适用位置

下表是基于能力与本仓库问题的工作分配建议，不是模型质量或价格排行榜。完整来源和本机版本见 [harness-rules.md](research/harness-rules.md)。

| Harness | 规划/审查适用点 | 可交给低成本执行的范围与边界 |
|---|---|---|
| Claude Code | 最适合审查现有 Claude 元数据、CLAUDE导入链、skill语义和多 reviewer 工作流；支持独立agent与hooks | 已批准的文档同步/skill片段；以单agent任务和文件范围隔离，不能让工具字面代替权限。[官方子代理](https://code.claude.com/docs/en/sub-agents) |
| Codex | 本仓库 Windows复现、Python边界、CI日志和跨文件diff审查最直接；AGENTS与命令工具已在本会话可用 | 编码单函数、pytest配置、限定回归测试；强模型保留根因、CI权限、最终验收。[官方子代理](https://developers.openai.com/codex/subagents) |
| Grok Build | 可做现有规则发现与独立强模型复审；本轮 grok inspect 已发现共同规则/兼容 skills，当前官方已支持hooks | 按批准清单执行文本/脚本任务；权限和hook信任要实际确认，不沿用Trellis旧“无hooks”判断。[官方功能](https://docs.x.ai/build/features/skills-plugins-marketplaces) |
| Kimi Code | 适合在明确上下文包内审查或执行独立模块；当前具备built-in及custom agents | 可用 secondary_model 承接机械文档、测试和窄代码任务；实际模型/费用由账户配置确定，不能按品牌认定便宜。[官方配置](https://moonshotai.github.io/kimi-code/en/configuration/config-files) |
| OMP / Oh My Pi | 适合多provider的独立审查与互不重叠任务编排；有 task、role/model/effort 和extension边界 | 已批准的文档/测试任务可批量交worker；最终独立审查由强模型承担。不是 Pi，且本次交互发现/扩展未验证。[官方任务文档](https://github.com/can1357/oh-my-pi/blob/main/docs/tools/task.md) |

低成本 worker 的交接至少包含：已批准结论、输入证据、唯一文件范围、具体检查、不可改变的语义、失败升级条件。出现新接口/跨目录变更/学术结论/权限扩张或测试无法解释时回到强模型。此次不做付费模型基准，也不发布未经核对的价格表。

## 建议批准范围

[design.md](design.md) 提供每项要改的文件和依赖；[implement.md](implement.md) 提供必须通过的检查与执行顺序。六子任务为 C1项目规则、C2 CI/测试发现、C3编码、C4接入/安装、C5跨工具skill执行、C6验收回写。

选择**共享项目规则与显式加载的最小方案**，保留用户级/本机工具资产边界。研究中建议的批量 adapter生成、gitignore放行、Trellis上游改造、固定模型路由配置不纳入本轮推荐实施。

后续证实的经验写入项目 `.trellis/spec/academic-writing-skills/harness-workflow-contract.md`，明确适用工具及版本证据，并同步相应公开说明/skill内容；不默认写全局共享记忆。

## 延后项与验收边界

- Pyright的75 warning：无本次关联运行证据，不批量修复。
- deploy.yml 的 pages/id-token权限可从workflow下沉到deploy job（P2）；若单独批准，改该文件并静态核验各job权限/触发，后续实际部署再验。
- ZIP内容过滤/可复现性、真实npx安装与软链接布局、五平台新会话、真实模型触发/费用比较、current SHA hosted matrix：没有执行证据，保持 **UNVERIFIED**。
- 对真实五工具运行验收没有授权/环境时，只完成并标注静态和脚本层交付，不能将运行验证项勾成通过。规划完成不等于六个实施子任务完成。
