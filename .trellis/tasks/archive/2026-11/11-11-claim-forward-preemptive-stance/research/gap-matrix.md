# 研究：差距矩阵（文章主张 × 仓库现状 × 判定）

日期：2026-11-11。判定取值：**已覆盖**（只交叉引用）/ **采纳**（新增规则）/ **改编**（换形态后采纳）/
**否决**（与红线或既有契约冲突）。本文件只记事实与判定；需求见 `prd.md`，机制见 `design.md`。

## 1. 仓库现状（已核对的文件）

- 防御性写作的主阵地是 `claim-forward` 模块（2026-09-13 三子任务落地），不是 `deai`。
  - 规则源：`latex-paper-en/references/writing/claim-forward.md`、
    `latex-thesis-zh/references/writing/claim-forward-zh.md`。
  - 脚本五码：`CF-DISCLAIM` `CF-SELFWEAK` `CF-CAVEAT-POS` `CF-HEDGE-STACK` `CF-CLOSE-NEG`；
    `CF-LOSS-FRAME` 仅 LLM。码集合由 `tests/contracts/test_claim_forward_contract.py` 锁定。
  - 中文指南另有"防御性说明的三类处置（仅 LLM）"（2026-09-22），英文指南没有这一节。
- `deai` 负责清嗓子句（值得注意的是 / it is worth noting）、`不是 X 而是 Y` 壳、七类 H-* 模式簇，
  以及"防御性推测解释"（多机制堆叠加末尾统一撤回，2026-08-05）。
- 改写契约四字段的 `Risk-Flags` 闭集是
  `none | not-assessed | lexical-substitution | whitespace-normalized | overstatement | ambiguity | terminology-drift | invented-claim`，
  由 `test_polish_contract_alignment.py` 与 `test_deai_pattern_cluster_contract.py` 锁定三方一致。
- 强度方向：三个 SKILL.md、EN/Typst 的 expression / grammar / sentences 模块都只写"不得升高措辞强度"。
  只有 `latex-thesis-zh/references/writing/unit-polish-zh.md` 写了"不得抬升也不得擅自削弱"并有 `UP-STRENGTH`。
- `typst-paper` 没有任何 claim-forward 内容（`grep` 零命中）；上一轮明确记为"本轮不在范围"。

## 2. 逐条判定

| # | 文章主张 | 仓库现状 | 判定 | 落点 |
|---|---|---|---|---|
| G1 | 预设反驳壳：这并不意味着 / 不能简单地认为 / 虽然…但总体而言…在一定程度上 | 规则源零命中（仅 EN 脚本的限制句开头正则含 `admittedly`）。上一轮矩阵 S1 只把"预设辩解"落成段首免责句 `CF-DISCLAIM`，段内让步壳没有落点 | 采纳（仅 LLM） | EN/ZH claim-forward 指南新增处置 |
| G2 | 让步后否定：承认真实混杂后写"但这并不影响…判断" | 零命中。它是过度声称，不是自我削弱；按"去防御"思路直接删让步句会让断言更强 | 采纳（仅 LLM，边界规则） | 指南写明转交 over-claim-guard 与结果分析，禁止删除 |
| G3 | 过强断言与模糊让步同段共现（案例一） | over-claim-guard 与 claim-forward 各自成文，共用阶梯，没有"同段共现时先后顺序"的说明 | 采纳（仅 LLM） | 指南新增修复顺序与去重规则 |
| G4 | 空泛谦辞：存在一定不足 / 仍有提升空间 / 具有一定参考价值 | ZH 词表有 `略显不足` `存在严重不足` 等带主语门控的搭配；后两句零命中。`conclusion-guide-zh.md` 把"仍存在一定不足"列为合法承接句，`analyze_conclusion.py` 的提示文案也这样建议 | 改编（仅 LLM，不进词表） | 指南要求限制句写出对象与条件；承接句写出具体局限时保留 |
| G5 | AI 润色把作者判断磨平 | 三方契约只防升高，无对称规则，也无对应风险标记；仅 ZH 单元润色已对称 | 采纳 | 三方改写契约补"不得擅自削弱"，`Risk-Flags` 增 `understatement` |
| G6 | 保留必要条件，区分真实边界与预设辩解 | 仅 ZH 有三类处置；EN 缺 | 采纳 | EN 指南补三类处置 |
| G7 | Typst 论文同样需要 | 无 claim-forward 模块；G5 的闭集三方锁定，Typst 必然同步 | 部分采纳 | Typst 只随 G5 同步契约；模块移植列为后续 |
| G8 | 用户会说"去除防御性表述 / 防御性写作 / 预设辩解" | ZH 的 SKILL.md 描述、路由行、模块触发词、trigger_eval 都没有这些说法；EN 模块触发词有 `defensive tone` | 采纳 | 触发词与 trigger_eval；同时写清"防御性推测解释"仍归 deai |
| G9 | 案例来自访谈与人数/比例 | 现有 claim-forward 示例全部是机器学习与工程指标 | 采纳 | 新增合成 fixture 与示例，覆盖质性证据与计数/比例 |
| G10 | 发现实际问题才修改；不凑错误数量 | 模式簇契约要求证据充分的样例保持静默，claim-forward 模块没有等价句 | 采纳 | 模块文档补一句：零发现是合法结果 |
| G11 | 值得注意的是 / 需要强调的是 | `deai_check.py` throat_clearing 与 filler 已覆盖 | 已覆盖 | 交叉引用 |
| G12 | 证据前置、人数与比例分开、分母与单位 | results-analysis（RA-*，含分母与共同样本）、paper-audit claim-evidence | 已覆盖 | 交叉引用 |
| G13 | 小结重复、段首段尾反复说、冒号前空转 | paragraph-roles（PR-*）、deai 冒号讲义腔、academic-style-zh §5.4 | 已覆盖 | 交叉引用 |
| G14 | 25 项清单整体 | 分散在 deai / expression / logic / format / bibliography 各模块 | 否决 | 再导入一份清单会产生第二规则源 |
| G15 | 保留作者的态度与情绪 | `pattern-clusters.md` 禁止自动注入第一人称、观点、幽默或情绪 | 否决 | 学术正文只保留判断强度，不注入情绪 |
| G16 | 把上述句式当作要删的词 | claim-forward 契约 §3.1"不新增观察码，不建词表"；文章自己也承认这些说法在具体语境里可能合理 | 否决 | 一律按语境由 LLM 判断 |

## 3. 两个方向不能混

文章把"删预设辩解"和"收回过强断言"放在同一个改写里完成，这是对的，但两者方向相反：

- 预设反驳壳、空泛谦辞是措辞弱于证据或没有内容，属 claim-forward 的范围。
- 让步后否定、"充分证明…是关键因素"是措辞强于证据，属 over-claim-guard 的范围。

只按"去防御"处理会删掉让步句而留下过强断言。因此 G2、G3 的规则必须写明先按证据校准断言，
再处理让步句，且让步句涉及真实混杂时不得删除。

## 4. 既有契约给本任务的限制

- `CF-*` 脚本码集合固定为五个；paper-audit 文档与 agent 中出现的 `CF-*` 集合也固定为五个。
- `claim-forward-contract.md` §3.1：文档层处置不新增观察码，不建词表。
- 禁改：`deai_check.py` 三副本、TIER1 哈希组四脚本、`analyze_conclusion.py`、`check_style_zh.py`、
  paper-audit 五个哈希锁定文件。
- 命名：不得用 `defensive` 命名 claim-forward 契约下的模块、脚本、码或文件；用户同义词可出现在触发词散文中。
- ZH 词表精度按 5 篇私有博士论文调过；改 YAML 需要重跑基线，私有语料不进测试。
- `EXPECTED_ABSENCES["check_claim_forward.py"] = ["typst"]`。

## 5. 外部先例检索（2026-11-11）

`qiaomu-meta` 自带的 `research_prior_art.py` 在 Windows 上因找不到 `npx` 可执行文件而失败，
改为直接运行它底层的两条命令。

- skills.sh，查询 `anti defensive writing`：
  `kiterlin/anti-defensive-writing`（352 installs）、`adkid-zephyr/anti-defensive-writing-skill`
  （中文 232、英文 162）、`boom5426/nature-paper-skills@anti-defensive-writing`（33）、
  `devilyuu/anti-defensive-writing-zh`（5），其余为 1–2 次安装的转载。
  前两个就是上一轮已研究并归属的来源，本地副本在 `ref/defensive/`。
- skills.sh，查询 `academic hedging`：`shaishavmaisuria/research-paper-lifecycle-skills@polish-prose`（116）、
  `junbolian/academic-humanizer`（8）、`linyeegiong/academic-deai`（4）等。
- SkillsMP，两条查询按 stars 排序返回的都是无关的高星仓库，没有可用候选。
- 未找到名为 CigarBall-Writing 的条目。

installs 是采用量，stars 属于仓库，都不是质量评分。本轮没有打开上述新候选的源码，
它们对本任务的价值为 **missing evidence**；本任务的规则只来自文章配图和仓库已有的两个来源。
`ref/defensive/anti-defensive-writing/SKILL.md` 第 185 行有一条"删除主要为防范假想反驳而存在的句子"的总则，
上一轮只把它落成了段首免责句，G1 是对这条总则的补全。
