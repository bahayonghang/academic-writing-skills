# latex-thesis-zh 增量缺口分析

日期：2026-09-10；HEAD：`dd9f1e2`。范围和逐文件记录见 [spec-coverage.md](spec-coverage.md)。
本报告是当前源码/指南审阅及定向探针的结论；没有实施以下修复。

## 结论

优先补齐六个具体缺口，合并为三个实施子任务。当前技能已具备方法叙述、结果分析、
段落弧线、小节上下文、工程章和版式验收规则，不应再建设一套同名能力。
主要问题是旧指南与新证据规则冲突、checker 把语义假设当事实，以及编译成功判据不一致。

| Finding | 严重度/优先级 | 缺口 | 归属 |
| --- | --- | --- | --- |
| G1 | Major/P1 [LLM] | 旧指南示范无证据数字替换、孤立准确率推导改进与机制 | C1 |
| G2 | Major/P1 [LLM] | 因果与“首次”措辞表仍允许通过标签/hedge 替代证据 | C1 |
| G3 | Minor/P2 [LLM] | 通用篇幅/逐篇综述/GPU 必选要求与章型、模板冲突 | C1 |
| G4 | Major/P1 [Script] | 不同技术概念被当同义词，按频次建议改名 | C2 |
| G5 | Minor/P2 [Script] | 先用后定义漏报、合法逐章缩写重引误报 | C2 |
| G6 | Minor/P2 [Script] | outdir 未一致传递，实际 PDF 被漏判或旧 PDF 被判成功 | C3 |

## G1：教学例子绕过证据约束

`academic-writing-skills/latex-thesis-zh/references/writing/writing-philosophy-zh.md:64`
把“可能有助于提升”改成“准确率提升了3.2%”，没有给出新数字的来源；同文件第 86 行还有
直接替入 12.3% 的示例。
`academic-writing-skills/latex-thesis-zh/references/modules/logic.md:11`
至第 14 行用单个 95% 支持“提升”，再归因为捕获长程依赖，缺比较基线与区分性证据。

已有反证：`academic-writing-skills/latex-thesis-zh/references/writing/over-claim-guard.md:8`
要求先判断实质证据；`academic-writing-skills/latex-thesis-zh/references/writing/paragraph-arc-zh.md:83`
已有不代入真实结果的原创示例。因此修复是条件化/替换旧例子，不是新建 evidence checker。

## G2：措辞阶梯与实质证据阶梯冲突

`academic-writing-skills/latex-thesis-zh/references/writing/over-claim-guard.md:14`
把干预/消融直接连到“证明”；第 41–42、114、122 行继续使用方法标签作因果资格捷径；
第 48、104、121 行将未检索的首次表述改成“据我们所知”，仍保留了未经证实的优先权主张。

对照 `academic-writing-skills/latex-thesis-zh/references/writing/results-analysis-guide-zh.md:219`
至第 239 行，组件贡献与因果归因明确分级；严格受控、预算一致且能排除替代解释才支持后者。
`academic-writing-skills/latex-thesis-zh/references/writing/academic-style-zh.md:137`
也明确消融标签不自动证明因果。应让措辞表回指这个既有规则源。
保留真正充分证据下的强陈述，不能用一律改为“相关”掩盖问题。

## G3：旧的通用配方与当前体裁规则冲突，操作示例仍偏薄

`academic-writing-skills/latex-thesis-zh/references/writing/writing-philosophy-zh.md:92`
至第 110 行仍给通用摘要字数、固定章节篇幅、逐篇文献描述及 GPU/超参数必选项。
`academic-writing-skills/latex-thesis-zh/references/writing/abstract-structure.md:94`
至第 98 行已区分 thesis 默认模型与 five 后备模型；
`academic-writing-skills/latex-thesis-zh/references/modules/literature.md:54`
至第 60 行已允许主题综合和选择性单篇展开。
`abstract-structure.md` 第 72–76 行自身仍残留无适用边界的默认长度表，需一并消歧，
但不能在本轮推导或更改学校的实际数值标准。

另一个 P2 操作性机会是
`academic-writing-skills/latex-thesis-zh/examples/logic-and-experiment.md:1`：
目前 22 行仅含命令与预期输出。可补一例从已有段落逆向提取
“段主题—章目标—证据—建议处置”的过程，复用 AXES/P-ARC/current-only，
不强迫每个局部请求产出整篇台账。

## G4：内置术语组混淆概念层级

`academic-writing-skills/latex-thesis-zh/scripts/check_consistency.py:58`
至第 71 行混合深度学习/深度神经网络、机器学习/机器智能、循环/递归神经网络等概念；
第 200–208 行只根据同组共现和频次直接建议统一名称。

当前内存探针：输入“深度学习是一类研究方法。深度神经网络是该领域使用的模型。”
得到 WARNING，建议统一使用“深度学习”。这是可复现的错误建议。
`tests/skills/latex_thesis_zh/test_latex_thesis_zh_checker_precision.py:146`
至第 155 行把深度神经网络/深层学习作为“真漂移”正例，测试也需纠正。
保留用户通过既有 custom-terms 明确声明的分组；不新建词典或推断概念等价。

## G5：缩写缺少首用顺序与合法重引判定

`academic-writing-skills/latex-thesis-zh/scripts/check_consistency.py:276`
只看全局是否有定义；第 290–296 行把任意多定义都报告为问题；
第 243 行的定义正则可跨行吞入章节标题，定位失真。

当前探针：
- 两次 CNN 使用后才定义：PASS。
- 两章各首现定义同一个 CNN：multiple_definitions。

这与 `academic-writing-skills/latex-thesis-zh/references/modules/consistency.md:13`
至第 15 行的先定义、逐章重引指导不一致。应按正文装配顺序判断全文首次有效使用与定义，
同一明确释义的同章/跨章重引不报冲突；不另加每章必须重新定义的检查或章状态。
无主文件的散文件输入不能伪造跨文件阅读次序。
符号/单位的完整语义一致性仍需 LLM，本轮仅准确说明脚本覆盖范围，不加数学改写器。

## G6：编译器输出和 wrapper 的成功判据脱节

`academic-writing-skills/latex-thesis-zh/scripts/compile.py:278`
和第 290 行传给 latexmk 的 outdir 正确，第 330–335 行却在源码目录查 PDF。
非 recipe 分支第 203–239 行未转交 outdir，且只凭进程 exit 0 报源目录 PDF。

当前 mock 探针（TeX 进程以 0 返回）：
- 只有 build/main.pdf：recipe 返回 1。
- 只有源码目录旧 main.pdf：recipe 返回 0，并报告旧路径。

历史真实 TeX 复现见
`.trellis/tasks/archive/2026-09/09-05-thesis-zh-practice-spec/research/implementation-check.md:33`
至第 39 行。当时明确排除修复，本轮作为新任务，不回改旧验收。
最小设计覆盖已有 latexmk recipe 和显式 compiler 分支；手动多步 recipe 的 outdir
目前也未正确支持，先显式拒绝该组合，避免继续静默忽略。
完整手动 recipe 输出目录与 BibTeX/Biber 路径协同另行扩展，不在本轮隐含承诺。

## 已覆盖、重复建设与延期项

| 能力/建议 | 当前依据 | 决定 |
| --- | --- | --- |
| 方法模块/接口/公式闭合 | method-narrative-contract 与 method-description-guide-zh | 已有，保留 |
| 结果展示/统计集合与证据分级 | results-analysis-checker-contract 与 results-analysis-guide-zh | 已有，修正冲突引用 |
| 工程章运行约束、机制和证据 | engineering-application-chapter-guide-zh；logic 模块 | 已有，不新建 engineering checker |
| 中文标点与句间关系 | academic-style-zh §5.4；deai-pattern-cluster-contract | 已有，保持 LLM-only |
| 双语题注与视觉门禁 | test_caption_commands；compile/caption/table 指南 | 已有，不以 checker 绿替代视觉 |
| 全文语义符号统一、真实学校 class、印刷效果 | 需要源文/模板/人工证据 | UNVERIFIED；非本轮新增实现 |
| 新 IR、状态机、评估平台、配置层、安装器/hooks | 本轮没有新增接口需求 | reject |
| 五宿主 fresh-session、provider A/B、人工盲评 | 当前没有独立执行记录 | missing evidence；不列为产品缺陷 |

## 验证与证据分层

- 当前定向基线：105 passed（ZH scripts 与 trigger corpus contracts）；它不能检出上述全部缺陷。
- 定向内存/Mock 探针复现 G4/G5/G6；只证明对应 Python 行为，不是本轮真实 TeX 验证。
- 当前 evals 47 条、trigger 49 条；33 个 eval 的 files 为空，但部分输入直接在 prompt 中。
  不能用这个统计推断完全没有输出证据。
- 09-05 归档另有 15 条实际 Agent 响应及六页合成 TeX 视觉证据；这些是历史限定场景证据，
  不升级成本轮 provider A/B、人工盲评或真实论文总体质量改善。
- 08-25 归档计划不得代替现行实现检查，也不构成恢复其拟议 IR/runner 的理由。
- 本轮不跑无关全套 CI；最终只验证规划产物、引用、树结构和工作区边界。
