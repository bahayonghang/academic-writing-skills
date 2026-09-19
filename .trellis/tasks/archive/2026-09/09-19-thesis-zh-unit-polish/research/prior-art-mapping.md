# 先例映射与探针证据（unit-polish）

日期：2026-09-19。方法：qiaomu-meta-skill 的 prior-art `keep / adapt / reject / invent` 四分法。
外部目录检索（skills.sh / SkillsMP）**未运行**：用户已指定两份先例，本任务不做新技能发现。
记为 `missing evidence`，不据此声称"优于同类"。

## 1. 先例来源

| 编号 | 来源 | 许可/归属 | 用途 |
|---|---|---|---|
| S1 | `ref/graduate-thesis-polish-and-write-skill/thesis-polish/`（SKILL.md、meta-rules.md、patterns-*.md、reference-thesis.md） | MIT（仓库 LICENSE） | 审校模式、元规则 K1–K8、黑名单 A/B、句长 L1、破折号 C1、token 控制 |
| S2 | 知乎回答《润色中文学术论文段落》 | 作者：大学生知识星球；链接 https://www.zhihu.com/question/582506176/answer/2083151703524877127；来源：知乎；著作权归作者所有，非商业转载须注明出处 | 保留清单、修改要求、输出契约（润色稿 + 修改说明三类） |

S2 原文要点（逐条保留，供 prd 追溯）：

- 任务：润色中文学术论文**段落**，降低模板化表达和 AI 痕迹；保持研究含义、事实数据、结论强度不变。
- 输入：待润色正文 + 术语定义、实验参数、上下文。
- 必须保留：专有名词/理论名/变量名；数字/单位/实验参数；引文编号/图表编号；因果、相关、显著、不显著、可能等结论强度；研究对象、时间范围、方法步骤、样本参数。
- 修改要求：一段一中心、结论先行；优先"统计、比较、识别、检验、归纳、检测、计算"等具体研究动作；删"值得注意的是/重要的是/综上所述"；减少无依据"不仅…而且…/不是…而是…"；删重复免责与泛泛局限，必要限制放在对应事实附近；方法段按流程拆长句；不改因果、不增减强度、不扩范围；不新增数据/文献/概念/机制/结论；不为"高级表达"换术语；保留自然表达、不追求整齐句式。
- 输出：先完整润色稿；再"修改说明"只含三类（删除了哪些无信息表达；调整了哪些句子逻辑/结构；哪些位置缺证据需作者补）；不解释未修改内容，不重复正文。

## 2. 逐机制映射

| 先例机制 | 来源 | 处置 | 落点 | 理由 |
|---|---|---|---|---|
| 单次调用只处理一个明确范围，按章/节分批，绝不整本 Read | S1 SKILL.md L35/L139 | **keep** | 单元定义 + `--plan` + `UP-SCOPE` 拒绝超单元验证 | 与用户"尽量不要全文优化"同源 |
| K5 克制修改：只改硬命中/口语化/语法错/逻辑断层/欧化长句，通顺句不动 | S1 meta-rules K5 | **keep** | 协议"改动准入"节 | 与仓库 `--strength minimal` 默认一致 |
| K8 写作模式 vs 审校模式：审校默认诊断，明确要求才直接改 | S1 K8 | **adapt** | 协议"模式判定"：用户明确"润色/改写"→ 出润色稿；"检查/审校"→ 只出诊断 | 仓库 `literature`/`deai` 已有同款默认 |
| 两个核心自检（删除测试、范例测试） | S1 SKILL.md | **adapt** | 协议自检清单（删除测试保留；范例测试改为"对照本单元相邻段落的既有句式"） | 范例论文指纹机制未引入（见 reject） |
| 黑名单 A1 套话过渡词（值得注意的是/综上所述/本节将…） | S1 patterns-vocabulary | **adapt（部分）** | 垫话 → 指向 `deai` 的 `AI_FILLER_CONNECTORS`（已含 综上所述/值得注意的是）；"本节将/本章将"**不入黑名单**（冲突项 D1） | `structure-guide.md` 标题后导语规范推荐"本章/本节将……" |
| 黑名单 B 结构模式（冒号列举、三段排比、元评论尾巴、的字链、相邻句同开头） | S1 patterns-structure | **adapt** | 冒号/分号 → `academic-style-zh.md §5.4`（已有）；排比/同开头 → `deai` D 维度（已有）；的字链/元评论尾巴 → 协议 `[LLM]` 检查项，不做脚本规则 | 不新增 deai 类别（`deai-pattern-cluster-contract` 禁止） |
| L1 长句 ≤60 字/3 分句 | S1 patterns-syntax | **reject（阈值）** | 沿用 `expression` 的 `E-LONGSENT`（默认 80 字，`--max-chars` 可调） | 一个仓库不能有两套句长阈值 |
| C1 破折号禁用 | S1 patterns-layout | **reject** | `deai` 已有 em-dash guard | 已有 owner |
| I2 本章小结单段三段式 | S1 patterns-layout | **reject** | `logic` 章末小结检查已有 | 已有 owner |
| 审校输出格式（定位/原文/命中规则/严重程度/改写建议） | S1 SKILL.md | **adapt** | 复用仓库 `% MODULE (loc) [Severity] [Priority] [Script|LLM]` 格式与四字段契约 | 仓库格式是契约测试锁定的 |
| 范例论文指纹（reference-thesis.md，5–10 KB） | S1 K3 | **reject（本任务）** | 记入 prd 待决 D4 | 需要用户提供范例、存在风格复制风险、无现成对应物 |
| 段落级任务边界（段落而非全文） | S2 | **keep** | 单元定义 U2（自然段） | 与 S1 token 控制互证 |
| 必须保留清单 | S2 | **keep + invent（可验证化）** | 协议"必须保留"节 + `polish_unit_zh.py --verify` 的 `UP-CITE/REF/LABEL/MATH/NUM/TERM/STRENGTH/NEG` | 先例只给原则，仓库要求可判定项脚本化（三档分级） |
| 一段一中心、结论先行 | S2 | **adapt** | 指向 `logic --paragraph-arc`（P-ARC-*）作为单元前诊断；协议不重造判据 | 已有 owner |
| 具体研究动作动词（统计/比较/识别/检验…） | S2 | **adapt** | 协议 `[LLM]` 改写偏好，不做脚本替换表 | "进行+名词"改动词属 C 档（子串不可判定） |
| 删无信息垫话；减少无依据反差/递进 | S2 | **adapt** | 诊断输入来自 `deai --section`（filler_connector / binary_contrast_shell）；协议规定"有依据的递进保留" | 冲突项 D2：`academic-style-zh.md §3` 把 不仅…而且/综上所述/由此可见 列为推荐连接词 |
| 删重复免责与泛泛局限；必要限制贴事实 | S2 | **adapt** | 指向 `claim-forward`（CF-DISCLAIM/CF-CAVEAT-POS）；协议重申"只移位不删除限制" | `claim-forward-contract` 否决删除限制 |
| 方法段按流程拆长句 | S2 | **adapt** | 协议方法段专项 + `E-LONGSENT` 候选 | 已有句长 owner |
| 不改因果/强度/范围；不新增内容 | S2 | **keep + invent（可验证化）** | `UP-STRENGTH`（强度词漂移）、`UP-NEG`（否定漂移）、`UP-NUM`/`UP-CITE`（新增数据/文献）、`UP-LENGTH`（扩写） | 强度阶梯词表来自 `over-claim-guard.md` |
| 不为"高级表达"换术语 | S2 | **keep + invent（可验证化）** | `UP-TERM`（用户术语表计数漂移，`--terms`） | 术语表格式复用 `check_consistency.py --custom-terms` |
| 输出：润色稿 + 修改说明三类；不解释未改内容 | S2 | **keep** | 协议输出契约；与 `deai/guide.md` 的"改动说明 + 【待补证】"合并（三类之三 = 【待补证】） | 两份既有格式合一，不新增第三种 |

## 3. 探针证据（2026-09-19，本地实测，未入仓库）

探针 1：裸片段 `unit.tex`（无 `\chapter`，含 值得注意的是/综上所述/不仅…而且/通过对比实验验证了/原因在于/显著提升 + `\cite`/`\ref`）

| 脚本 | 结果 |
|---|---|
| `check_style_zh.py` | 仅 `E-INCOMP` 1 条 |
| `deai_check.py --analyze` | 0 条痕迹（无章节键时不产出） |
| `check_claim_forward.py` | 0 条 |

探针 2：带 `\chapter{绪论}\section\subsection` 的同内容片段

| 脚本 | 结果 |
|---|---|
| `deai_check.py --section introduction --analyze` | `filler_connector` ×2（值得注意的是、综上所述）、`low_information_density` ×1；`不仅…而且` 未报（`BINARY_CONTRAST_SHELLS` 只收 不仅…还/更） |
| `check_style_zh.py` | `E-COLLOQ`（很好）1 条 |
| `analyze_logic.py --emit-window --subsection 1.1.1` | 正确给出 `current L5-L6 [可改]`、`next.head L8-L9 [只读]`，无 prev（首单元） |

结论：

1. 既有脚本在**带章节结构的入口文件**上能覆盖 S2 的垫话清单（除 不仅…而且），但对**润色后的裸片段**全部失效——润色后核对必须由新脚本按"原文 vs 润色稿"做差分，不能靠再跑一次 deai。
2. `--emit-window` 已提供单元坐标与只读邻域，单元协议可直接复用，不必重造游标。
3. `不仅…而且` 不在 deai 壳集合中；deai 冻结（对齐锁 + 模式簇契约禁增类），故该项只能入协议 `[LLM]` 清单，不入脚本。

## 4. 所有权表（新增内容不得重造）

| 现象 | 既有 owner | 本任务用法 |
|---|---|---|
| 值得注意的是/综上所述/总之 等垫话；不是…而是 壳；伪洞察 | `deai`（`ChineseAITraceChecker`） | 单元前诊断输入 |
| 口语化、绝对化词、搭配、成分残缺、中英标点、单位、单句过长 | `expression`（E-*） | 单元前诊断输入 |
| 冒号/分号句间逻辑 | `academic-style-zh.md §5.4`（`[LLM]`） | 协议指针 |
| 免责句/限制句后置、自我削弱、hedge 堆叠 | `claim-forward`（CF-*） | 单元前诊断输入 |
| 论断强度阶梯 | `over-claim-guard.md` | `UP-STRENGTH` 词表来源 + 协议指针 |
| 段落弧线、一段一中心 | `logic --paragraph-arc`（P-ARC-*） | 单元前诊断输入 |
| 小节游标、三元窗口 | `logic --subsection-context/--emit-window`（S-CTX-*） | 单元坐标来源 |
| 术语一致性 | `consistency --custom-terms` | 术语表格式复用 |

## 5. 冲突项（进入 prd 待决）

- D1 `structure-guide.md` 标题后导语规范推荐"本章/本节将……"；S1 A1/B4 把"本节将/先框架后内容"列为黑名单。
- D2 `academic-style-zh.md §3.1/§3.3` 把 不仅…而且、由此可见、综上所述 列为推荐连接词；S2 与 `deai` 把 综上所述 视为垫话、不仅…而且 视为无依据递进。
- D3 用户术语表输入格式。
- D4 范例论文指纹机制是否引入。

## 6. 缺失证据

- 外部技能目录检索未运行。
- 新脚本的漂移检查在真实润色稿上的误报率未测：仅有合成 fixture；私有语料（`ref/thesis/decrypted/`）可在实现期做只记数字的复核，不入仓库。
