# 逐项差量矩阵(delta-matrix)

来源锚点均相对 `ref/claude-scholar/skills/nature-writing/`。现有实现锚点均相对
`academic-writing-skills/`。判定:keep(原样采用)/ adapt(改造采用)/ reject(已覆盖或不采用)。
每条 adapt 项映射到子任务 PRD 的 D-* 编号与验收标准(AC)。

| # | 来源规则 | 来源锚点 | 现有实现锚点 | 判定 | Owner / D-* |
| --- | --- | --- | --- | --- | --- |
| N1 | 全文论证链 field-scale need→bottleneck→move→evidence→implication→boundary | references/article-architecture.md:8-16 | EN section-writing 无全文架构文件 | adapt | EN / D-EN-1 |
| N2 | 期刊式摘要六步 context→gap→approach→result→implication→boundary | article-architecture.md:18-27 | EN section-writing/abstract.md 只有 CS 式三模板 | adapt(并列模式,非替代) | EN / D-EN-1 |
| N3 | 摘要诊断:Here-we 开头缺上下文 / 末句宽泛承诺 / 全文无数字 | article-architecture.md:29-33(来源措辞为 may) | 无数字:EN analyze_abstract Results-VAGUE 已有(scripts/analyze_abstract.py:385);其余两项 EN/ZH 均无 | adapt → **LLM-only**,不进脚本硬规则(en+typst 哈希锁 tests/contracts/test_writing_modules_alignment.py TIER1_HASH_GROUPS;来源仅 may 级置信) | EN / D-EN-1 内嵌;ZH / D-ZH-1 |
| N4 | Results 证据阶梯六层 + claim-first 小节开头 `To test [question], we [action].` | article-architecture.md:51-67 | EN experiments.md 有 claim-to-experiment 表,无期刊叙事阶梯 | adapt | EN / D-EN-1 |
| N5 | Discussion 六步扩展 + 不逐图复述 | article-architecture.md:69-80 | EN experiments.md Discussion Layering 仅四步链 | adapt(期刊语境版,与既有四步链交叉引用) | EN / D-EN-1 |
| N6 | 结论四段式 + 无新数据 | article-architecture.md:82-91;conclusion.md:5-13 | EN section-writing/conclusion.md 五角色已覆盖 | reject | — |
| N7 | 标题公式 system+capability+application;prestige 词(novel/advanced/powerful/green/efficient)需具体化 | article-architecture.md:93-107 | EN title.md/optimize_title.py 已处理 vague words;`optimize_title()` 无条件删词(optimize_title.py:212-218),**不可**加词表 | adapt → doc-only(title.md 补公式与 prestige 告诫,标注 LLM 判断;脚本不动) | EN / D-EN-4 |
| N8 | 摘要三模板(challenge→contribution 等) | references/abstract.md | EN section-writing/abstract.md(同源) | reject | — |
| N9 | 引言四版/技术挑战三版/pipeline 四版/反模式 | references/introduction.md | EN section-writing/introduction.md(同源) | reject | — |
| N10 | 方法模块三要素/三层清晰度检查 | references/method.md | EN section-writing/method.md(同源) | reject | — |
| N11 | 实验三核心问题;表格规则(booktabs/精度/箭头/单位/右栏) | references/experiments.md:7-95 | 三问:EN experiments.md 已有;精度:check_tables.py:317 已有;箭头:experiments.md:32 已有文档;booktabs:tables.md 已有 | reject(残余:tables.md 补一句"方向标注接受 Unicode/LaTeX/文字形式,为可读性建议非强制"→并入 D-EN-4 doc-only) | EN / D-EN-4 |
| N12 | Related Work 主题综合式 | references/related-work.md | EN section-writing/related-work.md | reject | — |
| N13 | 反向提纲/段落单信息 | references/paragraph-flow.md | EN flow.md;ZH logic-coherence.md | reject | — |
| N14 | 五维拒稿风险表 + 投稿前自审 | references/paper-review.md | EN self-review.md;paper-audit 技能 | reject(paper-audit 边界:不向 paper-audit 引入本次内容) | — |
| N15 | 意图翻译六分解(claim/evidence/condition/comparison/implication/limitation,按英文章节序重写) | references/chinese-author-workflow.md:5-19 | EN translation-guide.md/translation.md 无此方法 | adapt | EN / D-EN-3 |
| N16 | 中文稿修复表六类 | chinese-author-workflow.md:21-30 | 后四类(显著无基线/首次无范围/相关性推机制/结果混含义):EN+ZH over-claim-guard 已覆盖;前两类(宽泛重要性先于对象/方法列表先于 gap)未覆盖 | adapt(只补前两类,后四类交叉引用) | EN / D-EN-3 |
| N17 | 结论局限两分法:技术缺陷 vs 范围局限;优先范围局限 | references/conclusion.md:17-29 | ZH conclusion-guide-zh.md 无;EN conclusion.md 已有 scope-limitation 偏好 | adapt → ZH;**重写为组织顺序指导,不得用于隐去基线落后/安全权衡等实质不利结果** | ZH / D-ZH-2 |
| N18 | 校准动词阶梯 show/demonstrate/suggest/indicate/may/could | SKILL.md:63-64 | EN/ZH over-claim-guard | reject | — |
| N19 | Results 叙事顺序应用于 zh 结果章 | article-architecture.md:51-67 | ZH results-analysis-guide-zh.md:192 五级阶梯是**证据强度**分级,与叙事顺序是不同概念,不可合并 | adapt-verify → ZH doc 核对:叙事顺序若缺失则补独立小节并显式区分两概念;已覆盖则落档不改 | ZH / D-ZH-3 |

## 共享措辞契约(父级持有)

N3 的 LLM-only 诊断在 EN/ZH 两侧措辞必须一致(候选提示,非判定):

1. 开头即 "Here, we / In this paper, we" 且前面没有上下文句 → **可能**缺少领域背景(候选,需结合摘要类型判断)
2. 末句为宽泛前景承诺且无范围限定 → **可能**需要收束范围(候选)
3. 全文无数字、比较或具体测试 → **可能**缺乏落地感(候选;EN 侧 Results-VAGUE 脚本项已存在,勿重复)

不引入脚本级 Nature profile;不新增硬词表。ZH 侧唯一脚本改动为一条 [LLM] Info 提示项
(沿用 B-SEM 既有模式),EN 侧零脚本改动。
