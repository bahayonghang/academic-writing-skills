# 实施与集成证据

日期：2026-09-05 至 2026-09-06。基线：dev / d5e5444；最初只有本轮规划目录未跟踪。
用户先批准实施，再明确追加中文正文冒号/分号与句间逻辑要求。公共产品文件按写作、工程章、
标点、题注顺序单写者交接；独立 trellis-check 负责最后审阅和完整 CI。

## 交付映射

| 父要求 | 实际交付与证据 |
| --- | --- |
| 全部源 spec 覆盖 | [spec-transfer-analysis.md](spec-transfer-analysis.md) 的 28 项清单与采纳/拒绝裁决；原研究保留规划时点证据 |
| 摘要、小结、综述与结果口径 | 扩充四处既有语义指南与综述示例；[写作实际输出](../../09-05-thesis-zh-evidence-writing/research/output-evidence.md) 7 例 |
| 工程应用章 | 一份新指南，通过既有 logic 按正文内容到达；[工程实际输出](../../09-05-thesis-zh-engineering-chapter/research/output-evidence.md) 3 例 |
| 冒号/分号追加要求 | academic-style-zh.md §5.4 为唯一规则源，expression/deai 强调；[标点实际输出与导航](../../09-05-thesis-zh-punctuation-prose/research/output-evidence.md) 3 例 |
| 题注与条件版式 | 仅修改 ZH 两条题注识别/位置路径；[题注脚本、输出与视觉](../../09-05-thesis-zh-caption-layout/research/layout-evidence.md) 2 例及 6 页合成 TeX |
| 公共资源与边界 | 累计双语镜像、SKILL/路由、README/技能入口、271 项 manifest 同步；保持其他技能、CLI/检查码族与锁文件不变 |

新增 output eval 33–47 共 15 例、trigger 新增 10 条后共 49 条，既有记录保留。
实际响应由独立上下文的 gpt-5.6-sol/max Agent 只读取输入字段和当前指南后生成，主 Agent
逐条审阅。它们是当前 Agent 的合成输出观察，不是外部 provider A/B、人工盲评或真实论文效果。

## 针对性检查

| 子任务 | 实跑结果 |
| --- | --- |
| 写作 | 168 tests；双语资源 10 tests；资源同步通过；首次缺 vitepress 的构建失败由既有 lockfile 环境准备后解决，后续累计构建通过 |
| 工程 | 129 tests；双语资源 10 tests；资源同步、VitePress 构建、diff-check 通过 |
| 标点 | 106 tests；双语资源 10 tests；资源同步、构建、diff-check 通过；构建 HTML 验证新增跨语言锚点和三处导航 |
| 题注 | 红测 9 failed/4 passed → 绿测 13 passed；目标回归 152 tests，skill/trigger 53 tests，双语 10 tests；资源、目标 Ruff、构建通过 |

只新增一个题注回归测试文件，没有将语言判断写成计数正则或新增规则引擎。
题注测试通过完整 checker 覆盖合法命令、短标题/空白换行、注释、相似命令、位置及多文件源坐标。
默认行为变化是误报/假绿修复，未来提交说明须保留这一声明。

## 最终集成检查

独立检查结论为 PASS，详见 [implementation-check.md](implementation-check.md)。

| 检查 | 状态 |
| --- | --- |
| 全部 ZH 与 contracts 测试 | 837 passed，0 skip |
| 全量资源同步 | 271 manifest entries，退出 0 |
| just ci | 退出 0；Ruff 200 files；Pyright 0 errors/75 既有 warnings；pytest 1756 passed，0 skip |
| just doc-build 与 diff-check | 均退出 0；VitePress 1.6.4，11.46s；新增中英锚点及链接实际核验通过 |
| Trellis 结构 | 五任务递归预检退出 0，blocking=0，undefined requirement refs=0；父 context 10/10 通过，四子 context 已验证 |

## 实施中修正与范围外发现

- 摘要串行证据收紧：共同验证对象不证明串行，必须有明确前后接口依据。
- 标点因果边界收紧：出现实验、消融或来源文字本身不证明因果，继续服从 over-claim-guard。
- 新增跨语言 §5.4 链接以显式锚点修复，并从实际构建 HTML 核对；未清理范围外旧目录。
- 题注大小写与标点明确服从学校/模板，未规定时才选择项目内一致风格。
- 独立检查修复新增测试的 ModuleType.__file__ 类型收窄，清除本次引入的 2 条 Pyright warning；
  修复后所有最终门禁重新通过，剩余 75 条均不在本任务修改的 Python 文件。没有需重采的语义变更。
- 既有 `compile.py --recipe latexmk --outdir build` 会在外部 LaTeX 成功后查错 PDF 目录并返回 1。
  未扩展修改 compile.py；同一合成文档用已有无 outdir 调用成功编译 6 页并逐页目视。

开发环境只按已有锁定配置准备本地依赖，依赖声明与 lockfile 无 diff；未新增项目依赖或安装系统工具。
未修改或编译真实论文，未提交、归档、推送、发布或操作 GUI。真实学校模板、图源有效 ppi、
打印效果、跨平台、现场/硬件/生产闭环/收益/人工可用性保持 UNVERIFIED。

仓库 spec 已补充题注两路径回归、标点规则归属与跨语言 fragment 实证三个简短约定；
没有新增通用验证器、兼容别名、配置或测试框架。

## 实施验收时的任务状态

父/四子共 30 项 AC 已按证据勾选，实施状态元数据记为 verified。
四个子任务保持 Trellis 的 in_progress 生命周期状态，父任务保持规划/集成容器状态；
这遵守本地工作流“归档时才改 completed”的机制，不能据此推断仍有未完成产品实现。
以上为实施验收完成时的状态，当时尚未执行提交、归档和推送。

## 本地收尾授权

2026-09-06 用户明确要求“请提交所有改动和归档任务”。本次收尾据此提交全部已验收改动，
依次归档四个子任务及父任务，并记录会话。实际完成状态以归档后的 task.json 和 Git 历史为准。
未授权推送或发布。
