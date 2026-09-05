# latex-thesis-zh 实践增量独立实施检查

日期：2026-09-06
基线：`dev` / `d5e5444`
范围：父任务 `09-05-thesis-zh-practice-spec` 及 `evidence-writing`、
`engineering-chapter`、`punctuation-prose`、`caption-layout` 四个子任务。

## 结论

**PASS。** 源码、指南、路由、双语公开资源、eval/trigger 追加、15 条实际响应和既有
视觉证据均与父/子 PRD、design 及适用 spec 一致。检查发现 1 项 Low 级问题，已在本轮
直接修复；修复后没有遗留的本任务范围内问题。

本轮脚本默认行为变化仍限于 ZH `references` / `tables` 两条路径的题注误报与假绿修复：合法
`\caption` / `\bicaption` 得到识别，注释、`\captionsetup` 与相似命令不能掩盖缺失，
表体下方题注继续报告位置问题。工程章仍复用 `logic`，定量结果只按请求或真实内容复用
`experiment --results-analysis`；RA-*、E-*、H-* 家族和其他 skill 脚本未扩张。标点建议保持
`[LLM]`-only，`academic-style-zh.md` §5.4 是唯一规则 owner。

## Findings (fixed)

- **Severity: Low**
- **File:** `tests/skills/latex_thesis_zh/test_caption_commands.py:188`
- **Issue:** 新增 ZH 加载守卫直接把 `ModuleType.__file__` 传给 `Path`。运行时测试通过，但
  Pyright 将 `__file__` 视为 `str | None`，因此本任务新增 2 条 `reportArgumentType` warning，
  会把任务自身告警混入仓库既有告警。
- **Fix:** 先将两个 `__file__` 保存为局部变量并分别断言非 `None`，再构造 `Path`。这保留
  原有 ZH 路径守卫，并让 Pyright 正确收窄类型。修复后题注回归 `13 passed`，Pyright 从
  `77 warnings` 降为 `75 warnings`；剩余告警均不位于本任务改动的 Python 文件。

## Findings (not fixed)

- **Severity: Low / out of scope**
- **File:** `academic-writing-skills/latex-thesis-zh/scripts/compile.py`
- **Issue:** 已有 `--recipe latexmk --outdir build` 调用可由外部 TeX 成功生成
  `build/main.pdf`，但 wrapper 随后仍在入口目录查找 `main.pdf` 并返回 1。
- **Why not fixed:** 该问题由 `caption-layout/research/layout-evidence.md` 的合成编译记录
  暴露，未由本任务改动引入；父/子设计和本次授权明确排除 `compile.py` 修复。无 `--outdir`
  的合法 wrapper 调用已退出 0，题注与版式证据没有把前一调用误报为编译失败或视觉通过。

## 追溯复核

- **证据写作（ID 33--39）：** 摘要串行/并行只依据真实接口，小结覆盖框架、方法、系统章型
  及独立任务，综述按主题簇—代表归因—簇末比较组织，展示范围与冻结聚合/共同样本分开。
  实际响应保留给定引用、标签、公式、数值和适用范围，没有新增组件作用、比较排名或因果结论。
- **工程应用章（ID 40--42）：** 新指南以正文任务而非章号判型，使用
  “来源工件—运行约束—设计目标/系统属性—可证机制—验证证据”；回放、影子、试点、生产/
  闭环分级以及可靠性、业务收益、跟踪保真度、人工可用性分项取证。真实方法章仍走
  `--per-chapter`，无定量结果的工程章不追加 RA。
- **标点与句间逻辑（ID 43--45）：** 只移除连续正文的标签壳和无根据结论，完整句关系不由
  实验/消融词面自动推断；合理引出、复杂并列、关键词、数学、代码、URL、引用和模板用途保留。
  两语构建产物各含 1 个 `punctuation-prose` id，目录、expression、deai 各 1 条 href 均正确。
- **题注与版式（ID 46--47）：** 两个公开 checker 的实际代码路径和新增 13 项回归覆盖普通/
  双语题注、可选短标题、空白换行、注释/相似命令、下方表题及多文件原始坐标；测试按路径加载
  ZH 副本并对称恢复 `sys.path` / `sys.modules`。指南将续图目录、长表 `\LTpost`、子题注、
  二次缩放和有效 ppi 全部保持为模板与渲染证据驱动的局部判断。
- **公开资源与语料：** `evals.json` 的 HEAD 32 项前缀逐项不变，当前 47 项；
  `trigger_eval.json` 的 HEAD 39 项前缀逐项不变，当前 49 项。271 条 manifest 记录通过全量
  源语言、哈希、双语目标、Markdown 形状和链接检查；新增工程章资源为 `sourceLocale: zh`。
- **spec 同步：** `testing-and-tooling.md` 记录题注两路径回归，
  `docs-bilingual-resources.md` 记录跨语言显式 fragment 验收，
  `deai-pattern-cluster-contract.md` 记录标点规则唯一 owner 与 LLM-only 边界。

## Verification

- **Lint: pass.** `rtk just ci` 退出 0；Ruff format 检查 `200 files already formatted`，
  Ruff rules 为 `All checks passed!`。
- **TypeCheck: pass.** 修复后 `rtk just typecheck` 与最终 `rtk just ci` 均退出 0；
  Pyright 为 `0 errors, 75 warnings, 0 informations`。75 条告警不在本任务改动的 Python 文件，
  本检查未扩大范围修复。
- **Tests: pass.** 修复后 `test_caption_commands.py` 为 `13 passed`；统一目标命令
  `tests/skills/latex_thesis_zh tests/contracts -q` 为 `837 passed`；最终 `just ci` 的完整
  pytest 为 `1756 passed`。上述运行均无 skip。
- **Resource sync: pass.** `rtk uv run python docs/scripts/check_resource_sync.py` 退出 0，
  `all resources (271 manifest entries)`。
- **Docs: pass.** `rtk just doc-build` 退出 0；VitePress 1.6.4 完成 client/server build 与
  page rendering，`build complete in 11.46s`。
- **Diff: pass.** `rtk git diff --check` 退出 0，无输出。

## 证据限制

本检查读取了 33--47 的完整实际响应及逐项裁决，并核对保存的六页合成编译/AUX/LOF/LOT/
逐页目视记录；遵守任务要求，没有重复编译或操作真实论文。真实学校 class、用户论文图像的
有效 ppi 与打印效果、真实论文整体质量、跨模型/provider 稳定性、现场/硬件、长期生产闭环、
业务收益和人工可用性仍为 `UNVERIFIED / missing evidence`，不能由静态语料、单测、合成页或
本地 Agent 响应推出。
