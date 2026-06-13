# cover-letter 审计报告（agent 原始产出，2026-06-12）

审计对象：`academic-writing-skills/cover-letter/`（39 文件，实测 4430 行），版本 5.2.0（与 pyproject 一致）。方法：全量逐文件阅读 + 临时目录 Python 投喂取证（未修改仓库任何文件）+ 外部政策调研。
配套外部政策基线：见同目录 `cover-letter-policy-research.md`。

## §1 外部环境调研结论（对照 skill 现状）

| # | 调研结论 | 来源 | 对 skill 的影响 |
|---|---------|------|----------------|
| 1 | **ICMJE 2026 年 1 月更新版新增 Section V"AI 在出版中的使用"**：AI 辅助须"在 cover letter 和稿件相应部分"双重披露，未披露可构成学术不端 | icmje.org/recommendations/（2026-01 更新版） | skill 的声明体系完全没有 `ai_disclosure` 项 → **C5(P0)** |
| 2 | Science/AAAS 要求 cover letter + 致谢 + methods 三处披露 AI；APS 明确要求"在 Cover Letter 中向编辑披露 AI 工具使用"；NEJM 要求双重披露；Nature Ecol&Evol 2025 社论建议在 cover letter 中声明生成式 AI | science.org editorial-policies；journals.aps.org/authors | science.md/nature.md 模板未含任何 AI 披露段 → **C5** |
| 3 | Elsevier AI 披露在稿内专门声明段、IEEE 在致谢节、ACM 在 Work 内（纯写作辅助免披露）、Springer Nature 在 Methods 节——各家位置不同，模板应逐 venue 区分 | 各出版商政策页 | 模板 frontmatter 具备承载逐 venue 差异的结构，但该知识缺位 |
| 4 | **NeurIPS/ICML/CVPR/ICLR 没有 cover letter 环节**（OpenReview/CMT 结构化表单替代） | OpenReview 投稿流程 | icml.md/cvpr.md 暗示主赛道适用 → **C6(P1)** |
| 5 | **作者推荐审稿人正被行业收紧**：Cureus 2025-08 全面取消（后被 WoS 除名）、PLOS ONE 早已取消、IOP/Wiley 加固核验 | retractionwatch.com 2025-08-29；PLOS 编辑流程页 | 7 个模板默认建议 suggested_reviewers → **C7(P1)** |
| 6 | Nature 旗舰刊 cover letter **可选且为机密渠道**（不给审稿人，用于 COI/在审相关工作）；Springer Nature 有固定声明句式；IEEE 两极分化（Proc. IEEE 强制，IEEE TIM 明言"没事别交"） | nature.com initial-submission；springer.com cover-letters | nature.md 未体现机密渠道用途；ieee-trans.md 未提两极化 → **C13/C22** |
| 7 | Data availability 一般走投稿系统/稿内单独声明，**非 cover letter 必备**；ICMJE COI 走 2021 版 Disclosure Form，无"COI 必须写进 cover letter"要求 | icmje.org/disclosure-of-interest/ | nature/science 模板把 data_availability 列为 cover letter required → **C13(P1)** |
| 8 | 编辑确实读 cover letter 且是 desk review 第一步（JIBS 社论，desk reject 率 65%；高投稿量期刊 50-80%）；建议包含：独特框架、特殊请求、曾读过稿件人员名单（防双盲破坏）、与自有论文/数据集重叠说明；被拒重投说明（Wiley Small、IEEE ToN 强制） | JIBS 编辑部社论（Springer Link） | "编辑读信"前提成立；但上述 2025-26 实务要素未进知识库 → **C22(P2)** |
| 9 | AI 写 cover letter 本身无明文禁止，但编辑反感模板化 AI 腔（CORR 主编报告 AI 生成投稿信激增，通用模板信被视为海投信号） | CORR 主编社论 | 反 AI 腔检查方向正确（加分项）；但缺"本信由 AI 辅助生成，提交前请核实期刊 AI 政策"的自我风险提示 → 并入 **C5** |

## §2 审计发现总表

### P0（核心能力在常见真实输入下失效 / 直接合规风险）

| # | 发现 | 位置 (file:line) | 证据 |
|---|------|------------------|------|
| **C1** | **作者提取在含 `\thanks` 的标准模板下全军覆没，且会提取出错误的通讯作者**。`\author{...\thanks{...}}` 因 `[^}]+` 在 \thanks 的闭括号处截断，捕获文本含 `\` 被整体丢弃；通讯作者回退正则（IGNORECASE）从 thanks 文本里抓出 email 局部名 | `scripts/extract_manuscript_facts.py:31-35`（`[^}]+`）、`:37-40`、`:59-69`（`_clean` 在截断后才清 \thanks，顺序错） | Python 实测：NeurIPS 样式 `\author{David S.~Hippocampus\thanks{...} \\ Dept...}` → `authors=[]`, `corresponding=''`；article 样式 `\author{Alice Smith\thanks{Corresponding author: alice.smith@uni.edu} \and Bob Jones}` → `authors=[]`, **`corresponding='alice.smith'`**。generate 模式将以 "Sincerely, alice.smith" 署名——逼近 SKILL.md:109 "Never fabricate authors" 红线 |
| **C2** | **标题提取：嵌套花括号截断、`\thanks` 资助声明泄入标题**。`\{(.+?)\}` 非贪婪停在首个 `}` | `scripts/parsers.py:378` | 实测：`\title{Adaptive \textbf{Latency-Aware} Inference for {Streaming} Detection}` → `'Adaptive Latency-Aware'`（丢一半）；`\title{Latency-Aware Inference\thanks{This work was supported by NSF.}}` → 资助声明进信件开头 |
| **C3** | **只读单文件，不解析 `\input/\include`**：多文件工程下 facts 全空，align-check 把信中**真实有据**的主张一并误报 | `scripts/align_check.py:162-163`、`scripts/extract_manuscript_facts.py:55-56`；姊妹 latex-thesis-zh 已有 `tex_loader.py` 修复，此处未跟进 | 实测：main.tex 仅含 `\input{sections/...}` → `abstract=''`, `contributions=[]`, `headline_numbers=[]`；对 fixture 信跑 align-check → **5/5 全部 moderate 误报**，包括稿件真实支持的 47%/2.1x 主张 |
| **C4** | **align-check 核心验证器系统性漏检**：数字与度量关键词只要在**全文档任意位置**各自出现即判 `verified`，与 docstring 宣称的"同段落内"不符。差异化卖点（防 overclaim）同时存在误报（C3）与漏检（C4） | `scripts/verify_letter_against_manuscript.py:49-80`（`_has_numeric_match` 全文匹配）、`:7-10`（docstring "within the same paragraph"） | 实测：稿件仅含 "73% of industrial sites lack monitoring" + 他处的 "reduction"，信中伪主张 "achieves a 73% reduction in memory footprint" → `verify_claim → (True, 'medium')`，**漏报** |
| **C5** | **AI 使用披露完全缺位**：ICMJE 2026.1 已明确要求 AI 辅助在 cover letter 中披露（Science/APS/NEJM 同向），但 10 个模板 frontmatter、`LETTER_STRUCTURE.md` 声明清单（7 项）、`DECLARATION_PATTERNS`（6 键）均无 `ai_disclosure`；skill 本身就是 AI 生成信件，SKILL.md 亦无政策风险提示 | `references/LETTER_STRUCTURE.md:45-55`；`scripts/presubmission_check.py:97-135`；`templates/*.md` frontmatter；SKILL.md 全文 | `grep -riE "generative|LLM|disclos"` 全目录仅命中 conference extension disclosure；0 个 AI 披露相关条目 |

### P1（功能/契约错位、必然误报、与行业现实相悖）

| # | 发现 | 位置 (file:line) | 证据 |
|---|------|------------------|------|
| **C6** | **ML 会议边界错误**：NeurIPS/ICML/CVPR 实际无 cover letter 环节。仅 neurips.md 有弱免责；icml.md 写 "Use this snapshot for the main track"，cvpr.md 写 "Declarations (Required for CVPR)..."，暗示主赛道存在该流程 | `templates/icml.md:21`、`templates/cvpr.md:41-44`（对比 `templates/neurips.md:21`）；`references/JOURNAL_TIERS.md:29-41` | 调研结论 2/4；SKILL.md:75 把三者列为一等公民 venue |
| **C7** | **suggested_reviewers 默认建议与行业趋势相悖，且必然误报**：7 个模板列入 optional_declarations，而 `DECLARATION_PATTERNS` 无对应模式 → 即使信里**已写**推荐审稿人，仍输出 "absent; consider adding" | 7 个模板 frontmatter；`scripts/presubmission_check.py:362-376`（`DECLARATION_PATTERNS.get(kind, ())` 空元组恒 False） | 实测：含 "We suggest the following reviewers..." 的信跑 nature 模板 → 仍报 `D-suggested_reviewers-opt ... is absent` |
| **C8** | **声明模式键集与模板键集失配**（C7 的一般化）：`prior_presentation`、`excluded_reviewers`、`artifact_evaluation`、`reproducibility_statement` 均无模式，对应 optional 项**无条件**报 minor；一旦移入 required 即成永久 major 误报 | `scripts/presubmission_check.py:97-135` vs 各模板 frontmatter | 实测：信中已写 "previously presented as a poster..." → 仍报 `D-prior_presentation-opt` 缺失 |
| **C9** | **MODE_GUIDE 宣传不存在的 CLI 能力**（幽灵 flag）：`--out-format md\|jourcl`、generate 的 `--output`、`--strict`、optimize 的 `--section`、journal-fit 的 `--manuscript`（"richer scope-fit analysis" 为空操作）。另：SKILL.md 是 5 模式，MODE_GUIDE 自称 "four cover-letter modes" 且无 presubmission 章节、集成矩阵缺行 | `references/MODE_GUIDE.md:13-14,24,38,80,3,96-103`；`scripts/cover_letter.py:158-179`；`scripts/journal_fit_check.py:427-439` | 逐一比对 argparse 定义，5 个 flag 均不存在 |
| **C10** | **`split_sections` 继承 EN 旧 bug，ZH 已修未回灌**：① `\section*{...}` 星号漏检；② 注释行 `% \section{...}` 误判；③ 复数标题漏检——**自带 fixture 的 `\section{Experiments}` 都拿不到锚点**；④ 重复键覆盖 | `scripts/parsers.py:57-66,113-132`；对比 `latex-thesis-zh/scripts/parsers.py:56-91` | 实测：`\section*{Introduction}` → `{}`；`% \section{Conclusion}` → 误报；fixture 的 section_anchors 缺 `experiment`/`result` |
| **C11** | **编码崩溃**：`_read_letter` 用 `read_text(encoding="utf-8")` 无容错（同套件其他读文件处均 `errors="replace"`），GBK 信件直接 UnicodeDecodeError | `scripts/presubmission_check.py:158` | 实测：GBK 编码信件 → CRASH。中文用户（投稿信场景）概率不低 |
| **C12** | **claim 提取硬上限 12 条，超出静默丢弃**，违背 SKILL.md:30 "every claim ... must trace to visible evidence"，且无 truncation 提示 | `scripts/build_letter_claim_map.py:69-77`（`max_items: int = 12`） | 实测：20 个 claim 句 → 仅提取 12，后 8 条不检 |
| **C13** | **Nature/Science 模板把 `data_availability` 列为 cover letter required 声明**，与现实不符（走投稿系统/稿内）；叠加措辞匹配过窄的误报 | `templates/nature.md:5-10`、`templates/science.md` frontmatter；`scripts/presubmission_check.py:115-121` | 实测："includes a data availability section..." 的信 → 仍报 `D-data_availability` major |

### P2（失同步、死代码、依赖、测试机制、触发覆盖）

| # | 发现 | 位置 (file:line) | 证据 |
|---|------|------------------|------|
| **C14** | `STRONG_CLAIM_PATTERN` 双副本失同步：align_check 9 词 vs builder 16 词 → severity 判定与建议相互矛盾 | `scripts/align_check.py:29-33` vs `scripts/build_letter_claim_map.py:55-61` | 实测："significantly" → align 判非 strong、builder 判 strong |
| **C15** | 死代码/伪计数：`_manuscript_supports` 中 `contrib_str` 构建后仅 `del contrib_str  # placate linters`；循环末尾空操作 continue | `scripts/build_letter_claim_map.py:128-137` | 从 paper-audit 改写时未清理 |
| **C16** | **PyYAML 非标准库硬依赖**且无降级：安装到 `~/.claude/skills/` 后运行时不保证存在 → presubmission/journal-fit/统一 CLI 全部 ImportError | `scripts/presubmission_check.py:27`、`scripts/journal_fit_check.py:25` | frontmatter 极简，手写解析即可去依赖 |
| **C17** | **测试防遮蔽机制名不副实**：`_load` 注释声称 cover-letter scripts dir 优先，实测被测脚本的 `from parsers import ...` 命中 `sys.modules` 缓存（解析到 **paper-audit** 副本）；且 `_load` 永久把 cover-letter 目录置于 `sys.path[0]` 不恢复。当前因三副本字节级一致而无症状 | `tests/test_cover_letter_scripts.py:25-29`；`tests/conftest.py:34-49` | Python 复现确认 |
| **C18** | 测试在**仓库 fixtures 目录内**写临时文件（`_tmp_aligned.md` 等）而非 `tmp_path`，断言失败时残留污染仓库 | `tests/test_cover_letter_align_check.py:88,108`；`tests/test_cover_letter_presubmission.py:63,78` | 源码可见 |
| **C19** | journal-fit 启发式必然粗糙且无局限性披露：scope_fit 靠 2 个字面关键词（Nature 信不含 "field/discipline" 即 LOW→P1）；`_count_claims` 只认第一人称句式 | `scripts/journal_fit_check.py:129-180,119-126,183-227` | 代码可见；SKILL.md/examples 未提示局限 |
| **C20** | 杂项契约小错：① `--json` 空操作 flag；② 生成稿把 venue slug 入句 "for consideration at ieee-trans"；③ G1 em-dash=major 不在 ISSUE_SCHEMA severity 清单内；④ examples 全用 legacy 脚本不用统一 CLI | `scripts/extract_manuscript_facts.py:202`；`scripts/cover_letter.py:83`；`references/ISSUE_SCHEMA.md:70-74` vs `references/PRESUBMISSION_RULES.md:61`；`examples/*.md` | 逐一核对 |
| **C21** | **中文触发覆盖不足**：frontmatter `description`/`when_to_use` 零中文 token；"投稿信"仅在正文 :51；trigger_eval 16 条仅 1 条中文 | `SKILL.md:3-7,51`；`evals/trigger_eval.json:20-23` | 中文用户说"帮我写投稿信"时路由依赖正文弱信号 |
| **C22** | 期刊知识快照缺 2025-26 编辑实务：Nature 机密渠道用途、IEEE 期刊两极化、双盲"曾读过稿件人员名单"、被拒重投说明、Springer 固定声明句式均未进 references/templates | `references/JOURNAL_TIERS.md`、`templates/nature.md`、`templates/ieee-trans.md` | 调研结论 1/6/8/9 对照 grep 无命中 |
| **C23** | **禁语三处失同步**：FORBIDDEN_PHRASES Tier 3 九条 vs 代码 J1 八条 vs PRESUBMISSION_RULES.md 六条；Tier 4 宣称由 presubmission_check 使用（:3）但**完全未实现**；Tier 1 "We are excited to share" 未被 L2a 覆盖 | `references/FORBIDDEN_PHRASES.md:3,37-58` vs `scripts/presubmission_check.py:86-95` vs `references/PRESUBMISSION_RULES.md:44-55` | 三方逐条比对；optimize fixture 信中的 "your prestigious journal" 实测不会被脚本命中 |

## §3 确认健康、无需动的部分

1. **parsers.py 拷贝纪律**：与 EN 规范副本字节级一致，由 ALIGNMENTS 哈希锁强制——六 skill 中最好的防漂移机制（C10 是 EN 系全家共有的上游欠账，非 cover-letter 私有漂移）。
2. **无 Gemini 残留**；`$SKILL_DIR` 约定一致；`allowed-tools` 最小化。
3. **evals 质量高于姊妹 skill 修复前水平**：4 个 fixture 真实可跑（IEEEtran 论文 + 三封不同缺陷的信），断言锚定具体 token（47%、2.1x、$1.2M），trigger_eval 16 条含 8 条带类别标注的负例；`test_skill_contracts.py:515` 强制路由表命令与 `--help` 一致。
4. **测试覆盖无死角**：8 个脚本全部有直接测试；无孤儿文件。
5. **输出契约执行到位**：lowercase severity + P1-P3 + source_kind 三脚本一致且有测试；exit code 0/1/2 全脚本统一。
6. **安全边界文本是六 skill 中最完整的**：注入防护、never fabricate 清单、"Never disable align-check"、不联网声明（SKILL.md:106-112）。
7. **SKILL.md 形态健康**：138 行，渐进式加载，五模式路由表-Workflow-Output Contract 相互一致（错位发生在 MODE_GUIDE，见 C9）。
8. **反 AI 腔/反模板腔方向与编辑现实吻合**。

## §4 建议修复分组

**组 A：提取层修复（C1/C2/C3/C10，一次性解决）**
- 平衡括号提取（parsers.py 已有 `_extract_balanced_block`，改造 `extract_title`/`AUTHOR_COMMAND_PATTERNS` 复用）；`_clean` 的 \thanks 剥离改为在平衡捕获之后、丢弃判定之前；删掉 corresponding 回退正则或限定在 `\corresponding*` 命令。
- 从 latex-thesis-zh 移植 `tex_loader.py` 与 `_split_sections_from_headings`（星号/注释/复数/重复键四修）；**EN 是规范副本，应先修 EN 再让 alignment 测试带动全家（含 paper-audit）**。

**组 B：align-check 精度（C4/C12/C14）**
- `_has_numeric_match` 收紧到段落/窗口共现（与 docstring 对齐），或至少把全文档命中降级为 `confidence: low`；取消 12 条硬上限或输出 `truncated: true`；STRONG_CLAIM_PATTERN 提为单一常量模块两处导入。

**组 C：政策合规知识更新（C5/C6/C7/C13/C22/C23）**
- 模板 frontmatter 新增 `ai_disclosure` 声明类型（nature/science/cell 按 ICMJE 2026.1 设 required，IEEE/ACM 标注披露位置在稿内），`DECLARATION_PATTERNS` 同步加模式；SKILL.md Safety Boundaries 加"本 skill 产出为 AI 辅助文本，提交前核对目标刊 AI 披露政策"。
- icml.md/cvpr.md 加 neurips.md 同款免责；suggested_reviewers 降为条件提示并补 2025-26 收紧背景；nature/science 的 data_availability 降为 optional 并注明机密渠道用途；FORBIDDEN_PHRASES Tier1/3/4 与代码三方对齐（Tier 4 要么实现要么移除声明）。

**组 D：健壮性与文档（C8/C9/C11/C16/C20）**
- `_scan_required_declarations` 对无模式的 kind 跳过或输出警告；`_read_letter` 加 `errors="replace"`；MODE_GUIDE 删 5 个幽灵 flag、补 presubmission 章节与矩阵行；PyYAML 换手写 frontmatter 解析或 try-import 降级；`--json` 空 flag 删除。

**组 E：测试与触发（C17/C18/C21）**
- `_load` 改为加载前后 `sys.modules.pop("parsers")` + finally 恢复 sys.path；临时信件改用 `tmp_path`；description/when_to_use 增补"投稿信、致编辑信"中文 token，trigger_eval 补 3-4 条中文正/负例。

取证产物：复现脚本在审计临时目录（repro2/3/4.py），仓库零修改。
