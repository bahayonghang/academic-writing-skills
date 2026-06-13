# latex-paper-en venue 事实核查（网络调研子任务产出，2026-06-12）

> 用途：与 latex-paper-en 代码审计报告（E 系列发现）配套的外部事实基线。每条已附来源。

## 核查结论（skill 须对齐的 2026-06 事实）

1. **IEEEtran**：CTAN 现行仍是 **v1.8b (2015-08-26)**，IEEE 官方会议模板仍基于它（US Letter, Times, 10pt），2024-2026 无新模板系统、无换字体。IEEE Author Center 摘要指引是"单段 **up to 250 words**"，**不存在 IEEE 全局 150-200 词规则**（限制按 venue 而异）。
   来源：ctan.org/pkg/ieeetran；ieee.org/conferences/publishing/templates.html；template-selector.ieee.org；journals.ieeeauthorcenter.ieee.org（structure-your-article）
2. **acmart**：CTAN 现行 **v2.18（2026-05-31 发布）**——八个 ACM 模板合一为 "Primary Article Template"、新字体集、新增无障碍特性，是 2026 年重大变更。Review 投稿单栏 `\documentclass[manuscript,review,anonymous]{acmart}`；TAPS 流程不变。**ACM 2026-01-01 起全面 Open Access**（仅 CC-BY/CC-BY-NC-ND；2026 年机构不在 ACM Open 时 APC $250/$350 优惠价）。
   来源：ctan.org/pkg/acmart；acm.org/publications/taps/word-template-workflow；authors.acm.org/journals/submission-process；acm.org/publications/openaccess
3. **NeurIPS 2025/2026**：正文 **9 页**；**camera-ready +1 页（共 10）**；checklist 强制（缺失=desk reject）；样式文件按年命名 **neurips_2025.sty / neurips_2026.sty**（2026 含 main/position/eandd 选项，Word 已停用）。**lay summary 只属 Position Paper track**（main-track lay summary 是 ICML 的要求）。2026：abstract deadline 5月4日、paper deadline 5月6日、悉尼主会场。LLM 政策：重大/非常规 LLM 使用须披露；LLM 不能署名；禁止 prompt injection；Position track 更严（no-AI 承诺）。
   来源：neurips.cc/Conferences/2025/CallForPapers；neurips.cc/Conferences/2026/CallForPapers；neurips.cc/Conferences/2026/MainTrackHandbook；neurips.cc/Conferences/2025/LLM
4. **ICML 2026**：投稿正文 **8 页**，references/appendix 不限；camera-ready **9 页（+1）**；强制声明正式名称是 "**Impact Statement**"（非 "Broader Impact Statement"，main track 强制、可用模板句）；样式包 **icml2026**（icml2026.sty），camera-ready 用 `\usepackage[accepted]{icml2026}`。新增：camera-ready 时 OpenReview **lay summary** + 财务 COI 披露。Deadline 2026-01-28，首尔。
   来源：icml.cc/Conferences/2026/CallForPapers；icml.cc/Conferences/2026/AuthorInstructions
5. **ICLR 2026**：投稿正文 **9 页**；rebuttal/camera-ready **10 页（+1）**；references/appendix/ethics statement 不计。**LLM 披露**：ideation/写作中的重大 LLM 角色须在专门 LLM-usage 节（可放附录）描述；未披露可 desk reject；禁止 prompt injection。**互惠审稿**：≥3 篇投稿的作者须审 ≥6 篇；每篇投稿须 ≥1 位作者注册审 ≥3 篇。样式精确名 **iclr2026_conference.sty/.bst**（LaTeX 强制）。
   来源：iclr.cc/Conferences/2026/AuthorGuide；blog.iclr.cc/2025/11/19（LLM 政策）
6. **ACL 2026 / ARR**：long **8 页**正文 + references 不限（camera-ready 9 页 +1）；short 4（+1→5）。**Limitations 节 long AND short 都强制，缺失 desk reject**（不计页数）。ACL 2026 全部经 ARR/OpenReview；**Responsible NLP Checklist 强制**（2024-12 起填错/误导=desk reject）；2024-02-15 起无匿名期。样式 acl.sty——**同时提供官方 Word 模板**。
   来源：aclrollingreview.org/cfp；acl-org.github.io/ACLPUB/formatting.html；2026.aclweb.org/calls/main_conference_papers
7. **AAAI 2026**：投稿 = **7 页技术内容** + references/reproducibility checklist 另计。**camera-ready 无免费 +1 页——只能购买（$300/页，最多 2 页）**。样式 aaai2026.sty + aaai2026.bst（LaTeX 仅 PDFLaTeX；也支持 Word）。
   来源：aaai.org/conference/aaai/aaai-26/main-technical-track-call/；aaai.org/conference/aaai/aaai-26/submission-instructions/
8. **COLM**：严格 **9 页**正文，citations 不限；2026 camera-ready **+1 页**；样式精确名 **colm2025_conference.sty / colm2026_conference.sty**（github.com/COLM-org/Template）；2026-03-31 截稿、旧金山 10 月；无 short track；采用 ICLR 2026 LLM 政策但豁免轻量写作/代码辅助披露。
   来源：colmweb.org/2025/cfp.html；colmweb.org/cfp.html
9. **CVPR 2026**：**8 页含图表** + references 不限；双盲。LLM 政策（FAQ）：工具随便用但作者全责；**虚构引用或明显事实错误 → 可不经评审直接拒**；"LLM 干的"不是辩护理由；禁止 prompt injection。补充材料（含视频）允许。
   来源：cvpr.thecvf.com/Conferences/2026/AuthorGuidelines
10. **"通用要求"核查**："references 不计页数"对 NeurIPS/ICML/ICLR/ACL/AAAI/CVPR/COLM 全部成立。**"所有 venue 都要求 LaTeX"是错的**：ACL 提供官方 Word 模板，AAAI-26 接受 LaTeX 或 Word。LaTeX-only 成立的是 NeurIPS/ICML/ICLR/COLM。
11. **arXiv**：摘要元数据上限 **1920 字符**（"abstracts longer than 1920 characters will not be accepted"，**不是 1500**）。2023-12-01 起对 TeX 投稿自动生成实验性 HTML 版。生成式 AI 不能署名；重大使用须按学科惯例披露（2023-01 政策，仍有效）。**2025-10-31 起 arXiv CS 的 review/survey/position 文章须提供已通过期刊/会议同行评审的证明**（workshop 不算），否则大概率拒收——针对 LLM 生成综述泛滥。
    来源：info.arxiv.org/help/prep.html；blog.arxiv.org 2023-12-21、2023-01-31、2025-10-31
12. **LLM/润色政策矩阵**（均允许润色，披露要求各异）：
    - NeurIPS 2025/2026：拼写/语法/编辑免披露；LLM 作为方法重要组件须在 checklist 申报；LLM 不能署名。
    - ICML 2025/2026：LLM 禁署名；prompt injection = desk reject；作者全责；2026 新增审稿用 LLM 的 A(保守)/B(宽松) 双政策框架。
    - ACL/ARR：纯语言润色免披露；生成式写作/代码用途**必须**在 Responsible NLP Checklist + Acknowledgements 申报；checklist 填错 = desk reject。
    - ICLR 2026 / COLM 2026：重大角色须专节披露，未披露 desk reject；COLM 豁免轻量辅助。
    - CVPR：无披露机制；作者全责；虚构引用→拒。
    - IEEE：AI **生成**内容（文/图/代码）须在 **Acknowledgments 节**披露（系统名+涉及章节）；纯编辑/语法"建议披露非强制"。
    - ACM：生成内容须在 Work 内显著披露（如致谢节）；**修订后纯写作辅助免披露**；生成式 AI 不得署名。
    - Springer Nature："AI-assisted copy editing" 豁免；生成式用途记录在 Methods；AI 图像禁止；LLM 不署名。
    - Elsevier：语法/拼写豁免；其余须在参考文献前加专门声明段 "Declaration of Generative AI..."（随论文发表）；AI 不署名。
    来源：见上各 venue 官网 + open.ieee.org（AI 指南）+ acm.org/publications/policies/frequently-asked-questions + springernature.com（AI 政策）+ elsevier.com（generative-ai-policies-for-journals）

## skill 须修正的事实错误摘要（由核查得出，对应代码审计 E 系列）

1. NeurIPS：camera-ready 是 **+1** 页（非 +0）；lay summary 属 Position track / ICML（非 NeurIPS main）；样式文件按年命名。
2. AAAI 2026：camera-ready 无免费 +1 页——只有付费页（$300/页，至多 2）。
3. arXiv 摘要：1920 字符，非 1500。
4. IEEE 摘要：无官方 150-200 词规则（官方指引 ≤250 词）。
5. "所有 venue 要求 LaTeX"：错——ACL、AAAI 接受 Word。
6. acmart：须更新到 v2.18 (2026-05-31) + ACM 2026 全面 OA。
7. 样式文件命名精度：iclr2026_conference.sty、colm2025_conference.sty。
8. 值得补充的 2025-26 新事实：ICLR/COLM LLM 披露 desk-reject 规则、ICLR 互惠审稿配额、arXiv CS 综述/立场文同行评审要求（2025-10-31）、ICML 2026 审稿 LLM 双政策、NeurIPS 2026 悉尼+5月4日摘要截止。
