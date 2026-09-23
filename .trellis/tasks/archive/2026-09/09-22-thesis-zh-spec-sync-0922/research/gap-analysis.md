# latex-thesis-zh 对照论文 spec 差距分析（2026-09-22）

> 历史初稿，保留问题发现轨迹，不作为当前实施合同。2026-09-22修订后的事实与范围见 [planning-evidence.md](planning-evidence.md) 及父子 prd/design/implement；尤其“format空路由”、原始作者缩写化、PDF自动化、可选CF码、旧模板改动和单一默认快照推论已被纠正。

源：`D:/Documents/LYH/200-Learning/00博士毕业/毕业论文/thesis/.trellis/spec/writing/`（34 份 Markdown + `term-groups-20260920.json`），`backend/quality-guidelines.md`，`materials/电气工程学院-研究生学位论文格式审查清单-2025.md`（111 条）。
目标：`academic-writing-skills/latex-thesis-zh/`，基线 dev `88bd045`，工作树干净。
本文件只记录差距与判定，不含实现。

## 1. 与既往同步任务的关系

| 既往任务 | 已覆盖（本轮不重做） |
| --- | --- |
| 09-05-thesis-zh-practice-spec（4 子） | 摘要串并行、三章型小结、综述综合/归因、结果展示口径、工程应用章、双语题注误报、冒号/分号（LLM-only） |
| 09-10-thesis-zh-spec-gap-optimization（3 子） | 指南证据保真、术语同义漂移误判（G4）、缩写先用后定义顺序（G5）、编译 outdir |
| 09-13-claim-forward-zh | 主张前置、自我削弱、免责句后置（CF-DISCLAIM / CF-SELFWEAK） |
| 09-19-thesis-zh-unit-polish | 单元润色 UP-*（含 UP-NUM / UP-MATH 多重集核对） |
| 09-20-thesis-zh-paragraph-roles | 六槽位职责 PR-*、"一处完整、其余指代"、四类重复 |
| 09-20-thesis-zh-chapter-intro-forms | 章引言一段式/两段式 CI-* |

09-10 之后论文 spec 新增 12 份文件：`body-chapter-paragraph-roles`（已覆盖）、`structural-redundancy`（部分覆盖）、`ch3-fidelity-subsection`（项目专属）、`cross-chapter-term-register` + `term-groups-20260920.json`、`degree-and-absolute-wording`、`energy-index-terminology`、`envelope-terminology`、`mismatch-terminology`、`regime-migration-terminology`、`sampling-rate-terminology`、`support-domain-and-extrapolation`。
既有文件 09-10 后的实质修改集中在 `symbols-and-numbers`（首现三路判定、XOR、`~\%`、千分空）、`equation-source-layout`（清单 79/81/83）、`result-analysis`（R-CROSS-SURFACE、显示层复算）、`method-description` §13（M-CODLANG 等 8 码、拆句保持公式记号多重集）、`literature-review` §4.1、`anti-defensive-hedging`（三类处置）、`citations-and-bibliography`（清单 44、97–104）、`figure-table-layout`（清单 67 表身语义、半行接排）。

## 2. 实测探针（2026-09-22，内存合成 .tex，不改论文）

| 探针 | 结果 | 判定 |
| --- | --- | --- |
| `check_style_zh.py`：「绝对误差为 0.3，完全忽略了噪声，极易发散」 | E-ABSOLUTE 报「绝对」「完全」；「极易」不报 | 「绝对误差」误报（spec 明确保留）；「极易」漏报 |
| `check_style_zh.py`：「50~\% 与 95\%，1\,300~$^\circ$C，0.1746」 | 仅 E-PUNCT；无千分空、无百分号空格判定 | 无清单 40/41 判定；E-NUMSPACE 词表把 `%` 硬编码为不空格，与学院 `~\%` 口径相反 |
| `check_consistency.py --terms`：「被控变量（CV）」首现后二次括注 + `Controlled Variable, CV` Title Case | PASS | 无 XOR / 二次括注 / Title Case 首现判定 |
| `deai_check.py --analyze`：「Atmaca 等分析……\cite{a1}」+ 六个「进一步」 | 无相关 finding | 无作者引述标注位置判定；无递进词密度上限 |
| `references/formatting/formula-guide.md:34` | 示例 `A &= B + C \\ &= D + E` 为推荐写法 | 与学院清单 81（续行不重复关系符）直接冲突；论文 spec 已注明该示例不适用 |
| `check_format.py` | 无任何公式规则（仅 chktex + F-MD / F-NOTE / F-PLACEHOLDER） | `templates/yanshan.md` YS-37/38 路由到 `module:format` 为空路由 |
| `check_tables.py` | 无「同上/同左」、无「量/单位」表头、无题注标点检查 | 清单 65/67/68 无脚本面 |
| `check_references.py` / `bib_scan.py` | 无同一文献多次引用页码（postnote）判定 | 清单 44 无脚本面 |
| `verify_bib.py` | 有 等/et al. 语种、期刊卷期页、题名全大写 | 无作者「姓全大写+名首字母无点」、出版地城市、页码缺失（图书/学位论文）判定（清单 98/101/102） |
| `check_consistency.py --custom-terms` 格式 | `{"zh": [[...]], "en": [[...]]}` | 与论文 `term-groups-20260920.json` 逐字段一致，可直接复用 |

## 3. 差距清单

严重度/优先级按仓库约定；来源标注 GENERIC（任何中文学位论文）/ COLLEGE（燕山电气学院 2025 清单条目号）/ PROJECT-MECH（项目专属规则，但其机制可泛化）。

| # | 差距 | 来源 | 现状 | 归属 |
| --- | --- | --- | --- | --- |
| G1 | 项目级术语治理文件：同指术语组之外还需「禁用词 → 按槽位替换表」「锁定名」「数学/引文/bib 豁免」「不得脚本替换」 | PROJECT-MECH（6 份 *-terminology.md 共 ≥ 60 条替换项；cross-chapter-term-register） | 仅 `--custom-terms` 同义组；无禁用词与替换候选机制 | C1 |
| G2 | 缩写合格首现后 XOR：禁「中文全称（ABBR）」二次括注、Title Case 首现、「中文全称 ABBR」并列 | GENERIC + COLLEGE 36 | 无判定（探针 PASS） | C1 |
| G3 | 程度副词：「极易/极低/高度贴合」逐句改写候选；「绝对误差/绝对值/最优+表格」豁免 | GENERIC（spec 明确「不做全局替换」） | E-ABSOLUTE 误报「绝对误差」，漏「极易」 | C1 |
| G4 | 数值与单位 `~`，百分号按普通单位（`50~\%`）；平面角紧贴 | COLLEGE 40（与 GB/T 15835 不空格口径相反，须按校配置） | E-NUMSPACE 硬编码 `%` 不空格 | C2 |
| G5 | 千分空：整数 ≥ 4 位、小数 ≥ 4 位用 `\,` 分组；年份/型号/编号/DOI 不分节 | COLLEGE 41 | 无判定 | C2 |
| G6 | 公式源码：编号公式前引导句以「：」收束、公式末不加标点（79）；续行不以关系/运算符起行、`A &= B \\ &= C` 违规（81）；「见式（1-1）」不用上式/下式（78）；式中/其中体例（83/84） | COLLEGE 76–85；GENERIC 78/81 亦见 GB/T 7713.1 | `check_format.py` 无公式规则；`formula-guide.md` 示例与 81 冲突 | C2 |
| G7 | 作者引述文献标注紧跟作者短语/「等」 | GENERIC（用户约定，全文适用） | 无判定 | C3 |
| G8 | 同一文献多次引用需标页码 `[3]101-108` | COLLEGE 44 | 无判定 | C3 |
| G9 | 著录细则：作者姓全大写、名首字母无点；图书/学位论文出版地；页码齐全 | COLLEGE 97/98/101/102（GB/T 7714 通则） | `verify_bib.py` 部分 | C3 |
| G10 | 综述递进词密度上限（「进一步」≤ 5、「针对」≤ 7，综述范围内） | GENERIC（阈值为项目标定，作 UNVERIFIED 默认） | 无判定 | C3 |
| G11 | 关键定量结果跨表面一致：同口径数字在表、正文、小结三处同一终值（R-CROSS-SURFACE）；小结 headline 数字须存在于本章结果表；不同名指标不互推（R-CROSS-METRIC）；显示层复算 vs 源层门控 | GENERIC | RA-* 9 码无跨表面数字核对；UP-NUM 只在单元内 | C4 |
| G12 | 评价集命名锁（测试集/离线评价集/滚动决策集不混用） | PROJECT-MECH（锁定名机制 = G1） | 无 | C1（机制）/ C4（应用） |
| G13 | 学院 2025 审查清单（111 条）无法路由：`templates/yanshan.md` 为 2024 研究生院规范 58 条（YS-01..58），编号体系不同；一审 > 15 项自费二审、二审 > 5 项暂缓答辩 | COLLEGE 全部 | `--spec-file` 可接自定义清单，但无学院层模板、无对应 checker | C5 |
| G14 | 全文第三人称（除致谢）；正文页底留白 ≤ 2 行（各章末除外，需 PDF） | COLLEGE 88 / 87 | 人称仅摘要 T-VOICE；无 PDF 页底留白检查 | C5 |
| G15 | 方法叙述表达约束：M-CODLANG（张量操作编程术语）、M-FIGTEXT（正文与架构图标注一致）、M-FORMDUPE（公式后自然语言复述）、M-SEMICOLON、N-ISOLATE（超参数入方法段）、M-DETAILINV、M-TERMREG、M-REDUNDANT；拆句保持公式记号多重集 | GENERIC | 技能 M-* 为 CLOSURE/EDGE/EQUATION/HEADING/SEQWORD 等 12 码，无上述 8 码；PR-EQ-NARR ≈ M-FORMDUPE；UP-MATH ≈ 记号多重集但仅 polish | C6（文档层）+ C1 词表 |
| G16 | 防御性说明三类处置：保留证据边界 / 否定改正面定义 / 未验证弱点写成 trade-off 而非设计优点；禁比喻词（门禁/筑牢/本质安全/理论性能上界） | GENERIC | claim-forward 有「范围转肯定」；无「弱点不得改写为优点」、无比喻词表 | C6 + C1 词表 |
| G17 | 结构冗余：删前文预告后补一句桥接使「上述/如图/本节」有所指；不得换词复述、不得改「首先/其次」 | GENERIC | paragraph-roles-zh 有四类重复与「一处完整」；缺桥接与禁换词 | C6 |
| G18 | 题注：中文题注不含标点、编号后空一汉字（46/65）；对象+内容、无「+」/样本数/「测试集…结果」空壳；英文 sentence case 按校锁定 | COLLEGE 46/65 + GENERIC | caption-guide Title/Sentence 二选一说明；无标点检查 | C2（脚本）+ C6（文档） |
| G19 | 表身「空白 = 无此项/未测」「— = 测过未发现」；禁「同上/同左」；同列同单位移至表头「量/单位」 | COLLEGE 67/68 | 无 | C2 |
| G20 | 摘要：成对引号 U+201C/U+201D；作者动作过去时；估计/预测/现场应用动词分工；无具体数字 | GENERIC（引号）/ PROJECT（其余） | T-* 无引号检查 | C6 |
| G21 | 标题与章节安排描述不含公式符号 | GENERIC | 无 | C6（结构指南）+ C5 可选 script |

## 4. 已判定不迁移

- 项目专属内容：Ch3 保真度小节、系统章 §6/§7、过程章变量集、五段漏斗、结论章「定性不给数字」（与 YS-16 定性定量评价冲突，保留学校规范）、Yangquan 证据分档。
- 术语禁用词的**具体词条**（工况迁移、支撑域、包络、运行绩效、失配、时间尺度失配）：只作为 C1 治理文件的示例格式，不进内置默认词表。
- 页面几何、封面、题名页、成果页字体字号（清单 1–7、105–110）：manual 项，沿用 `templates/yanshan.md` 既有 manual 分流。
- `thesis_analysis.page_whitespace` 等论文仓库脚本：不移植，C5 只以 pymupdf 可选实现清单 87。
- 09-10 的 G1–G6 判定不重开；PR-*/CI-*/RA-*/UP-*/CF-* 阈值不动。

## 5. 约束（沿用仓库既有）

- 新能力默认藏在新 flag 或新模板后；默认输出零变化（`tests/fixtures/paragraph_arc/baseline-before.txt` 逐字节锁）。误报修复例外须同 commit 更新存量单测并在 commit 正文声明。
- `[Script]` 恒 `Meaning-Check: NEEDS-LLM`；启发式 Info/P3 并标 UNVERIFIED；不复制整句。
- 学校阈值走 `TEMPLATE_THRESHOLDS` 或新模板文件；不得让燕山口径外溢到 thuthesis/pkuthss/generic（`BANNED_NON_YS_METHODS`）。
- 新 checker 必须被至少一份 `templates/*.md` 清单引用（`test_spec_checklists.py` 双向锁）。
- `parsers.py`、`deai_check.py` 字节不变（对齐锁）。
- 公开 `references/**` 每文件同步 `docs/resource-manifest.json` 与 en/zh 镜像；`evals/*.json` 只能 Bash python 追加。
- 私有语料、论文原句、作者/校名不进公开文件。
