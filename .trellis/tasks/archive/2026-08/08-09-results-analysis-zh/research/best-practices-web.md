# 实验结果分析写作最佳实践——网络调研纪要

> 检索日期 / 访问日期：2026-08-09（exa web search 两轮）。摘录为检索时返回的高亮片段；
> 写入公开 guide 前如需引用原文表述，须按 §一末"来源定位"表的 URL 重新抓取核对。
> 用途：为 `results-analysis-guide-zh.md` 的规则设计提供外部佐证与补充视角；
> 采纳原则按 qiaomu-meta 的 keep / adapt / reject 三分法逐条标注。

## 一、来源清单

| # | 来源 | 关键内容 |
| --- | --- | --- |
| 1 | Univ. of Toronto Engineering Communication Program, "Results and Discussions" | 讨论 = analysis（结论提取）+ interpretation（意义、局限、误差影响）两要素；每个 claim 必须绑定具体数据 + 逻辑解释（claim-data-warrant 三件套）；误差讨论须评估影响大小、发生可能性与规避方法，不得只列清单 |
| 2 | UCSD MAE 实验报告讲义（Swales & Feak 数据评述） | 图表导语分 indicative（"表 5 显示感染方式分布"）与 informative（"表 5 显示家用磁盘是主要感染源"）两级，正文应优先 informative；highlight（挑重点）与 comment（作者解释）应可区分；最优 highlighting 范例 = 报排序结构变化（rank order），而非只报均值 |
| 3 | MIT EECS Communication Lab, "Journal Article: Results" | 每图/表支撑一个明确结论，图序即叙事大纲；结果段结构 = rationale 主题句 → 发现 → 过渡句；空间分配与结论重要性成比例；与主结论矛盾的部分必须如实写出 |
| 4 | CityU OSAWEC（工科论文 Results 章） | Results 章八不写清单（原始数据、无解释图形、过度文献对比、显著性/应用外推等）；观察性评论可以有，意义与含义留给 Discussion |
| 5 | Flinders Univ., "Discussing Results" | 三层法：趋势描述 → 理论解释（relate results to theory）→ 含义；用 supported/indicated 不用 proved；离群点必须 acknowledge 并说明取舍，不得静默剔除 |
| 6 | Univ. of Melbourne（数据章写作） | 每个数据章开头给 statement of purpose、结尾给新知识陈述；选代表性数据并说明代表性依据 |
| 7 | Sheffield MEE 报告写作 | "This could be due to…" 类推测语句属于 Discussion 不属于 Results；Results 短语限于 "It can be seen that…/There is a linear relationship…" 类事实描述 |
| 8 | Peacock (2002, JEAP)：修订 Dudley-Evans 讨论节 move 模型 | 八 move 修订模型：information → finding →（un)expected outcome → reference to previous research → explanation → claim → limitation → recommendation；理科语料中 finding+explanation 循环（3+5/3+4）远多于 claim+文献循环；claim(90%)、finding(84%)、文献回指(73%) 接近必选 move |
| 9 | CASRAI, "Writing a Discussion Section" | 最常见失败 = 复述数字不解释 与 overreach；纪律：每个解释性 claim 必须能回溯到 Results 中实际展示的证据，否则降级为 hedged 或移入 future work；统计显著 ≠ 实际意义，二者混同是可检查的 overclaim 模式；null 结果需要真解读（排除效应量/与竞争理论不符/欠功效是三种不同 claim）；citation-dumping 是审稿人可识别的 padding |
| 10 | CASRAI, "Causal Analysis" | 因果语言纪律：claim 强度必须匹配设计强度，且在摘要/结果/讨论全程一致，不能只在 limitations 藏一句谨慎话；"X was associated with Y" 滑到 "X reduces Y" 是最常见的诚信滑坡 |

另：Manchester Academic Phrasebank "Discussing findings"——解释性 move 的语言全部为 tentative（"A possible explanation… / may be due to…"），佐证证据阶梯的谓词分级思路。

### 来源定位（URL 与完整题名，访问日期均为 2026-08-09）

| # | 完整题名 | URL |
| --- | --- | --- |
| 1 | Results and Discussions — U of T Engineering Communication Program Online Handbook | https://ecp.engineering.utoronto.ca/resources/online-handbook/components-of-documents/results-and-discussions/ |
| 2 | Lab Report Writing MAE 171A/175A（Results / Data Commentary 讲义，基于 Swales & Feak） | http://maecourses.ucsd.edu/callafon/labcourse/handouts/Results.pdf |
| 3 | Paper: Results — MIT EECS Communication Lab CommKit | https://mitcommlab.mit.edu/eecs/commkit/journal-article-results/ |
| 4 | Results — Online Support for Academic Writing for the Engineering Curriculum（CityU ELC） | https://osawec.elc.cityu.edu.hk/repo/front-page/thesis/results/ |
| 5 | Discussing Results（Simone Polden）— Flinders University SLSS | https://students.flinders.edu.au/content/dam/student/slss/academic-writing/discussing-results.pdf |
| 6 | Analysing data and reporting results — University of Melbourne Academic Skills | https://students.unimelb.edu.au/academic-skills/graduate-research-services/writing-thesis-sections-part-2/analysing-data-and-reporting-results |
| 7 | What goes in? What goes out? — Sheffield MEE Report Writing Website §4.3 | https://mee.group.shef.ac.uk/Report_writing_website/4.3.html |
| 8 | Peacock, M. (2002). Communicative moves in the discussion section of research articles. System 30(4)（PDF 镜像） | https://jolantasinkuniene.wordpress.com/wp-content/uploads/2014/03/peacock-communication-moves-in-discussion-section-of-ra.pdf |
| 9 | Writing a Discussion Section — CASRAI Guides | https://casrai.org/guides/writing-the-discussion-section-of-a-research-paper |
| 10 | Causal Analysis: A Guide to Causal Inference — CASRAI Guides | https://casrai.org/guides/causal-analysis |
| 附 | Discussing findings — Manchester Academic Phrasebank | https://www.phrasebank.manchester.ac.uk/discussing-findings/ |
| 附 | Writing Discussion Sections / Discussion Moves & Associated Academic Phrases — Oxford Lifelong Learning | https://lifelong-learning.ox.ac.uk/about/writing-discussion-sections 与 https://lifelong-learning.ox.ac.uk/about/discussion-moves |

## 二、keep / adapt / reject 判定

### keep（用户 spec 已覆盖且更严格，保持原样）

- 证据阶梯五级与谓词表（spec §6）——比 CASRAI"trace claim back to Results"更可操作，保留为核心机制。
- 判据逐指标绑定、区间端点方向、"等价"红线（spec §3.2/§5.3）——外部来源无同等精度，保留。
- 排序反转必须如实报告（spec §3.3）——与 MIT"矛盾必须写出"、CASRAI"不利结果不得隐藏"互证。

### adapt（外部机制融入 guide，需本地化转写）

1. **informative vs indicative 图表导语**（UCSD）→ 融入 guide 图表分工节：图表导语应为 informative（点出结论），indicative（只报图号内容）仅作段落开门；支撑 R-LOCALIZE。
2. **claim-data-warrant 三件套**（UToronto）→ 一致性解释句式模板："观察（表 X 数据）+ 结构事实（方法§Y 定义）+ 关联判词（与……一致）"。
3. **finding→(un)expected→explanation move 循环**（Peacock）→ 作为"强制论证顺序"的外部佐证写入 guide 依据注；意外结果（与预期不符）是合法且推荐的 move，不是要掩盖的缺陷——补充 spec 未显式覆盖的"预期外结果如何写"。
4. **统计显著 ≠ 实际意义**（CASRAI）→ 融入数值比较规则：R² 绝对差/相对差口径的依据注；效应量小到无实际意义时不得靠百分比放大。
5. **null/持平结果三种解读**（CASRAI）→ 融入正反例：性能持平时写"表现相当/具竞争力"并区分三种含义，不强行声称提升（与既有 experiment.md 数据真实性约束互证）。
6. **误差讨论三要素**（UToronto：影响、可能性、规避）→ 融入局限写法：不写无评估的误差清单。
7. **图序即叙事大纲、每图一结论**（MIT）→ 融入图表分工节导语。
8. **每数据章 purpose→新知识闭环**（Unimelb）→ 与既有本章小结规范互链，不重复。

### reject（不采纳，附理由）

- IMRaD 严格 Results/Discussion 分章（Sheffield/CityU）：中文工科学位论文主流为"一章一方法 + 章内结果与分析"合并结构（method-chapter-guide-zh.md 已锁定），不引入分章硬要求。
- p 值/显著性检验硬要求：与既有防误报红线 3 冲突（工业过程论文 5/5 无 p 值属惯例），维持"分方向口径"。
- 英文短语库直接翻译（Phrasebank/Oxford）：只取谓词分级思想，句式一律用中文学术惯用语重写。
- Swales move 编号术语直接进 guide：学位论文作者不需要 move 编号元语言，转写为自然的论证顺序表述。

## 三、对 RA-* 脚本检查设计的启示

- CASRAI 的"prove/confirm/establish 是审稿人红旗词"→ 支持 RA-CAUSAL/RA-EQUIV 词面检测的可行性：因果谓词与等价断言是词面可检的（区别于防御性推测解释的段落级组合判断，后者按 defensive-ai-rhetoric 契约保持 llm-only）。
- UCSD"最优 highlighting = 排序结构"→ RA-SECONDBEST（无次优比较）与 RA-UNIVERSAL（全面优于断言）的正当性佐证。
- Flinders"曲线描述要看整体趋势不逐点复述"→ RA-SHALLOW 浅层图表描述词检测的反面词表依据。
- CASRAI"一致性贯穿全文"→ RA-STAGE（管线阶段命名混用）作为一致性线索检查的依据。
