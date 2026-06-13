# cover-letter 政策调研（网络调研子任务产出，2026-06-12）

> 用途：与 cover-letter 代码审计报告（C 系列发现）配套的外部政策基线。每条已附来源。

## 一、主要出版商 2025–2026 Cover Letter 要求

1. **Elsevier**：推荐附上，建议 ≤1 页，聚焦研究目标与主要发现；以各刊 Guide for Authors 为准。
   来源：elsevier.support/publishing/answer/what-should-be-included-in-a-cover-letter
2. **Nature 旗舰刊**：cover letter **可选**（optional），但定位为机密沟通渠道——**不给审稿人看**，应用于提供机密信息（COI、在审/在印相关工作）；避免重复摘要和引言。
   来源：nature.com/nature/for-authors/initial-submission
3. **Springer Nature**：标准三段式（标题+文章类型+背景 / 做了什么+发现+重要性 / 为何匹配期刊）+ 固定声明句式："We confirm that this manuscript has not been published elsewhere and is not under consideration by another journal. All authors have approved the manuscript and agree with its submission to [期刊名]."；建议在信中提出推荐/回避审稿人及理由。
   来源：support.springernature.com/.../6000245674-cover-letter
4. **Wiley**：无出版社级统一要求，逐刊规定；典型要求：动机/新颖性、推荐与回避审稿人、COI（**无冲突也须声明**）、相关投稿/预印本披露、润色服务披露；*Small* 等刊要求被拒重投必须在 cover letter 说明前次投稿及修改详情。
   来源：onlinelibrary.wiley.com（author-guidelines + CoverLetter template）
5. **IEEE**：两极分化——*Proceedings of the IEEE* 强制详细 cover letter（缺失可退回）；*IEEE TIM* 明言"没特别的事就不要交"；IEEE/ACM ToN：含已发表材料或被拒重投时必须说明差异（逐点回应）。
   来源：proceedingsoftheieee.ieee.org；ieee-ims.org/publication/ieee-tim；sites.google.com/view/ieee-acm-ton
6. **ML 顶会（NeurIPS、ICML、CVPR、ICLR）根本不使用 cover letter**——OpenReview 结构化表单（作者列表、摘要、checklist）替代自由格式信函。**cover letter 技能对 ML 会议投稿场景不适用，应明确边界**。
   来源：neurips.cc/Conferences/2025/CallForPapers；icml.cc/Conferences/2025/PeerReviewFAQ

## 二、AI 使用披露政策（2025–2026）

7. **ICMJE 2026 年 1 月更新版**：新增 Section V "AI 在出版中的使用"（作者用 AI、审稿人用 AI、编辑职责三小节）+ Section III.L.2 作者数据访问权。
   来源：icmje.org/news-and-editorials/updated_recommendations_jan2026.html
8. **ICMJE 明确要求 AI 使用须在 cover letter 中说明**（Section V.A）："使用此类技术的作者应**在 cover letter 和投稿作品的相应部分**描述其使用方式"；AI 不得署名；未披露可被认定为学术不端。**这是对 cover letter 内容的直接新要求**。
   来源：icmje.org/recommendations/browse/artificial-intelligence/ai-use-by-authors.html
9. **COPE**：AI 不能署名、使用须在 Materials and Methods 等部分透明披露；作者全责（2023-02 声明维持有效）。
   来源：publicationethics.org/cope-position-statements/ai-author
10. **Elsevier（2025-09 更新）**：写作辅助须在文末参考文献前加专门声明段（随论文发表）；纯语法/拼写豁免；AI 图像全面禁止。**披露位置在稿件内而非 cover letter**。
    来源：elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals
11. **Springer Nature / Nature Portfolio**：LLM 使用记录在 Methods；AI copy editing 豁免；AI 图像禁止。*Nature Ecology & Evolution* 2025 社论建议：**"用了生成式 AI 准备稿件文本，请在 cover letter 中向编辑声明"**。
    来源：nature.com/nature-portfolio/editorial-policies/ai；nature.com/articles/s41559-025-02907-0
12. **Science（AAAS）最严格**：AI 辅助须 **cover letter + 致谢 + methods 三处披露**（methods 含完整 prompt、工具名及版本）；少数明文把 AI 披露写入 cover letter 要求的出版方。
    来源：science.org/content/page/science-journals-editorial-policies
13. **IEEE**：AI 生成内容须在 Acknowledgments 披露；纯编辑增强建议披露非强制；2025-09 重申，并禁止审稿人用公开 AI 平台生成审稿意见。
    来源：journals.ieeeauthorcenter.ieee.org（submission-and-peer-review-policies）
14. **ACM**：生成式 AI 须在 Work 内显著披露；基础文字处理豁免；不确定时"宁可披露"。
    来源：acm.org/publications/policies/frequently-asked-questions
15. **Wiley（2025-10-28 新版 AI 指南）**：列出工具名、版本和确切用途；位置可为 Methods/专门声明/Acknowledgements；禁止 AI 创建/篡改研究数据和图像。
    来源：newsroom.wiley.com（2025-10-28 press release）
16. **"AI 写 cover letter 本身"无主流出版商明文禁止，但有两条红线**：(a) ICMJE/Science/NEJM/APS 要求披露 AI 参与投稿材料准备（APS 明确要求"在 Cover Letter 中向编辑披露 AI 工具使用"；NEJM 要求双重披露）；(b) 编辑反感模板化 AI 腔信件（CORR 主编报告 AI 生成投稿信激增、缺乏实质内容；通用模板信被视为海投信号）。
    来源：journals.aps.org/authors/ai-based-writing-tools；science.org/content/article/letters-scientific-journals-surge

## 三、编辑实务：Desk Rejection 与 Cover Letter

17. **编辑确实读 cover letter，且是 desk review 第一步**（JIBS 2024-06 社论："The first step in the desk-review process entails reading the cover letter"；该刊 65% desk reject）。JIBS 建议包含：研究问题独特框架、特殊请求（如需懂新方法的审稿人）、**曾读过稿件的人员名单**（防双盲破坏）、与自有论文/共享数据集重叠说明（建议附 originality matrix）。
    来源：link.springer.com/article/10.1057/s41267-024-00712-8
18. **作者推荐审稿人功能收缩**：Cureus（Springer Nature 旗下）2025-08-25 全面取消作者推荐审稿人（此前发生配偶审稿、伪造账号事件；该刊 2025-10 被 WoS 除名）；PLOS ONE 早已取消（研究显示全用作者推荐审稿人可使接受率提高 20 个百分点）。
    来源：retractionwatch.com/2025/08/29/mega-journal-cureus-halts-author-peer-reviewer-suggestions
19. **多数出版商"保留+加固"**：IOP 仍接受但必须搭配编辑独立选择的审稿人；Wiley 在 Hindawi 事件（撤稿 8000+）后要求核验推荐审稿人身份且"不得仅由作者推荐"。**含义：推荐审稿人段落应标注"视期刊而定"，不应默认生成**。
    来源：publishingsupport.iopscience.iop.org；editors.wiley.com/page/peer-review-101
20. **通用模板信是负面信号**：高投稿量期刊 desk reject 50–80%，编辑初筛读 cover letter；"一眼能识别通用模板信"，视为海投信号。
21. **必备合规要素共识**：未一稿多投+全体作者批准声明（Springer 固定句式）、COI（Nature 系建议放 cover letter 因对审稿人保密；Wiley 无冲突也须声明）、相关在审/在印工作与预印本披露、被拒重投说明。**Data availability 一般在投稿系统/稿内单独提交，非 cover letter 必备项**。

## 四、ICMJE 2026-01 版变更细节

22. 版本时间线：2025-01 更新 → 2025-05 停止维护"遵循期刊名单" → **2026-01 现行最新版**（新增 Section V 和 III.L.2）。
23. AI 核心条款：投稿时必须披露是否使用 AI；使用者须**同时在 cover letter 和稿件相应部分**描述用法；AI 不得署名、不得作为一手引用来源；未披露可构成不端。
24. **Disclosure Form 仍是 2021-02 版**；COI 走表格/系统，ICMJE 并无"COI 必须写进 cover letter"要求（与 AI 披露的明确 cover letter 要求形成对比）。

## 对 cover-letter 技能的关键启示

- **AI 披露段落已成 cover letter 新必备模块**（ICMJE 2026.1 / Science / NEJM / APS 明文要求；Nature 系推荐）——技能若不支持生成 AI 使用声明段落即属功能缺口。
- **推荐审稿人段落须降级为条件项**（Cureus 取消、PLOS ONE 取消、Wiley/IOP 加固）。
- **ML 会议场景应明确排除或提示**（NeurIPS/ICML/CVPR/ICLR 无 cover letter；ICLR 2026 的 LLM 披露在论文附录，与 cover letter 无关）。
- **长度与反模板化**：各方一致 ≤1 页；编辑反感通用化 AI 腔——生成器应强调期刊定制化与具体发现陈述。
