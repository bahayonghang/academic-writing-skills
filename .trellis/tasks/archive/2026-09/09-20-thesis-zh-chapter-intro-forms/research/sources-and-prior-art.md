# 来源与先例研究（2026-09-20）

按 qiaomu-meta-skill 先例发现流程记录。指南正文只引用本文 §2 带 URL 的条目；§3 语料只用统计。

## 1. 需求来源

用户 2026-09-20 要求：中文大论文第 2 章起的引言支持两种写法——一段式与两段式；两段式沿用既有指南；一段式参考用户提供的截图（某水泥熟料博士论文第 4 章 4.1 引言，单段约 556 字），并注明"他的也不一定好，可以作为参考"。要求重新总结写法并创建 `latex-thesis-zh` 优化任务。

## 2. 可引用来源（带 URL）

| # | 来源 | 采纳要点 | 证据标签 |
| --- | --- | --- | --- |
| W1 | 万维书刊《学位论文写作指南及模板——引言及过渡段》，https://www.eshukan.com/academic/show.aspx?id=170089 | "其他各章的引言通常也是一个自然段，引出本章主题并简要交代其内容即可，起导读作用"；给出开门见山式 / 提问式 / 承上启下式三种一段写法示例；章标题与节标题之间不得无引言段 | 一段式合法性的直接依据 |
| W2 | 上海外国语大学《研究生学位论文格式规范指导》，https://graduate.shisu.edu.cn/_upload/article/34/80/bd4949214d11ab764fb3259a644c/26c942f8-0ab8-44aa-97cf-f4e41291ea81.pdf | "在每一章的开头，应在总结前文的基础上，提纲挈领地对本章的内容进行介绍……有必要时，可以将开头和结尾的这些部分分别列为独立的小节" | 承上 + 概述两要件；编号引言节 / 章后导语两位置形态均合规 |
| W3 | Pat Thomson, *connecting chapters/chapter introductions*, https://patthomson.net/2014/01/16/connecting-chapterschapter-introductions/ | LINK / FOCUS / OVERVIEW 三步；"keep the three moves" 但改稿时可打散段落 | "要件固定、段数灵活"的设计依据 |
| W4 | Thesis Hub, *Structuring Thesis Chapters: The Introductory/Concluding Paragraphs*, https://thesishub.org/structuring-thesis-chapters-the-introductory-concluding-paragraphs/ | 单个引言段同时完成：承接前章 [1]、引入本章对象 [2]、预告本章 [3]、关联全文论点 [4] | 一段式四要件的英文范例 |
| W5 | ANU Academic Skills, *Chapter writing*, https://www.anu.edu.au/students/academic-skills/research-writing/chapter-writing | 章引言须给出本章论点与其对全文研究问题的贡献；小标题不能替代过渡句 | 方案宣告要件 |
| W6 | The Ohio State University, *Hacking the Thesis — Your Outline*, https://u.osu.edu/hackingthethesis/managing-stuff/your-content/outline/ | 每章引言：link back to previous chapters、state the aim、outline how | 承上 / 方案 / 路线三要件 |
| W7 | Leshem & Bitzer (2021), *'Signposting' research stories in doctoral theses*, https://doi.org/10.5785/37-1-965 | 过度路标使文本"somewhat overdone as the text becomes repetitious" | 一段式不双写目录与路线、不重述背景 |
| W8 | 万维书刊《学位论文开头/结尾的八种写法》，http://eshukan.com/academic/show.aspx?id=151354 | 章引言四种起法（开门见山 / 引语 / 回顾前文 / 轶事） | 已在 09-20 段落职责任务引用，交叉引用 |

仓库已有出处（不重复引用）：清华《研究生学位论文写作指南》§4.5（章引言不重复绪论综述）已录入 `method-chapter-guide-zh.md` §三。

## 3. 私有语料

`ref/thesis/decrypted/` 5 篇工业博士论文，统计见 `reference-corpus-stats.md`。只入研究文件，不进指南、fixture 与测试。

## 4. 技能目录先例

### 4.1 运行记录

- `research_prior_art.py`（qiaomu）在 Windows 下 `subprocess.run(["npx", ...])` 报 `FileNotFoundError`（与 09-20 段落职责任务相同）。改 `--skip-skills-sh` 只跑 SkillsMP，3 条查询得 25 个候选家族，输出 `research/prior-art-candidates.json`。
- `npx skills find "thesis chapter introduction"` 经 `cmd //c` 手动运行成功。安装量只反映采用度，不是质量评分；SkillsMP stars 属于源仓库。

### 4.2 候选与处置（只读，未执行任何候选代码）

| 候选 | 安装量 | 内容 | 处置 |
| --- | --- | --- | --- |
| hkustdial/supervisor-skills:intro-drafter | 464 | 论文级 Introduction 六段散文生成器 | reject：面向全文引言，不涉及章引言 |
| alterlab-ieu/alterlab-academic-skills:alterlab-thesis-supervisor | 76 | 人设式论文导师 | reject：与诊断型模块不适配（同 09-20 任务结论） |
| santifs/thesis-writing-skill:thesis-writing | 28 | 全论文五模式；"Each chapter earns the next" | adapt（原则层）：章引言须说明本章为何在此处，已由既有承上口径覆盖，不新增 |
| robertguss/claude-code-toolkit:chapter-architect | 27 | 书籍章节节拍大纲 | reject：非学术 |
| willoscar/research-units-pipeline-skills:thesis-chapter-reconstructor | 15 | 围绕主线重写章目标与承接 | keep（已有）：09-20 段落职责任务已采纳 |
| SkillsMP 25 个家族 | — | 金融 thesis-tracker、PPT 模板、论文格式转换、本仓库自身镜像（brycewang-stanford/auto-empirical-research-skills:latex-thesis-zh、bahayonghang/academic-writing-skills:latex-thesis-zh） | 全部不相关或为自身镜像，合并后不计 |

结论：没有任何先例区分中文学位论文章引言的一段式与两段式，也没有段式判定或要件覆盖检查。本任务的一段式六步推进序、段式选型判据与 `--chapter-intro-style` 观察均为**原创（invent）**，证据来自 §2 W1/W3/W4 与 §3 语料。

## 5. keep / adapt / reject / invent

- keep：既有两段式模板、承上分级、两位置形态均合规、路线预告≠节号目录、不重述背景、不双写目录。
- adapt：W3 "要件固定、段数灵活"→ 段式选型判据；W1 三种一段写法 → 一段式起句方式（开门见山 / 提问 / 承上）作为可选起法说明；W7 → 一段式内不重复路标。
- reject：所有目录先例的生成式/人设式路线；一段式必须含"意义句"的模板化要求（只有熟料 5/5 使用，粉磨用"为此，亟需……"，不能升为通用规则——泛化门槛）。
- invent：一段式六步推进序与合成正反例；"位置形态 / 段式"术语分离；`CI-STYLE` / `CI-MIX` / `CI-MOVES` / `CI-LONG` 观察码；`CHAPTER_DEP_REF_RE` 章号列举扩展。

## 6. 泛化门槛记录

用户样例（单篇）不直接升为规则。升为核心规则的只有跨 3 篇不相关论文（熟料、粉磨、烧成）与 W1/W4 重复出现的行为："一段内按 对象 → 问题 → 方案 → 收束/路线 推进即合规"。样例的"意义句""英文缩写命名"保留为可选要件；样例的具体工艺内容只进合成 fixture。
