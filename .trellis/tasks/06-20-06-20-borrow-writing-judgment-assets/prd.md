# 借鉴 scientific-paper-writing 的 4 项写作判断力资产

## 背景

参考技能 `ref/scientific-research-skills/scientific-paper-writing`（写作期元技能）含若干判断力资产，
而本套件 `academic-writing-skills`（写后期润色+校验套件）在以下 4 处空白或偏薄。本任务把这 4 项
**本地化吸收**进本套件，不照搬其领域内容（群体基因组学）和单技能 meta/tasks 架构。

来源对比分析见会话记录；本任务只落地确认采纳的 ①~④。

## 目标范围

仅作用于 3 个**写作/润色类**技能：`latex-paper-en`、`latex-thesis-zh`、`typst-paper`。
`paper-audit` / `cover-letter` / `bib-search-citation` **不在本任务范围**（① 进 paper-audit 审计维度列为后续 follow-up）。

## 需求（4 项资产）

### ① Over-claim 保守表达替换词典（最高价值，含脚本化）
- 新增共享参考文档：确定性动词梯子（demonstrate→reveal→suggest→may indicate→hint）+
  7 类替换表（因果 / 首创 / 普适 / 效应量 / 时序 / 应用 / 比较）+ 高频陷阱句式表。
- 示例**本地化**为 CS/通用学术语境（en/typst 英文；zh 中文学位论文语境），不用 popgen 例子。
- **脚本层**：`tone-thresholds.yaml` 新增 over-claim 触发词配置；`deai_check.py` 新增一个
  YAML 驱动的 checker，对无歧义的因果/首创词（caused by、drives、first、novel、universally…）
  发 `[Script]` LOW severity 提示并给保守替换。YAML 缺失时回退内置默认（与现有 checker 一致）。
- 与现有 `claim-evidence-contract.md` 的边界：后者管"证据**够不够**支撑 claim"，本资产管"措辞**分级降级**"。

### ② 结构级 AI 痕迹（LLM 判断）
- 在各技能 de-AI 指南中新增"结构级痕迹"小节：完美对称 IMRAD、过度声明式过渡
  （"Having established X, we next…"）、中立无立场 Discussion、段落长度均匀化。
- 标 `[LLM]` provenance，纯判断力补充，不新增脚本（句长方差已有 `_check_sentence_length_variance`）。

### ③ 修改三层法的"顺序不可逆"原则（编排原则）
- 在各技能写作流程/哲学文档中新增简短小节：润色次序 = 论证逻辑 → 句子结构 → 词汇排版，
  说明"顺序反了白费功夫"。落到 SKILL.md 的润色路由提示一句话引导。

### ④ AI 黑名单的"快照 + 维护节律"（治理）
- 在各技能黑名单/语气词文件头部加维护声明：黑名单是快照非终态，建议每半年依 excess-vocabulary
  研究更新，注明来源（Kobak et al., *Sci. Adv.* 2025；Geng & Trotta 2025）。

## 约束（项目护栏）

1. **三副本镜像**：内容须同时落到 en/zh/typst；注意命名差异（en/zh 用 `references/{类}/小写.md`，
   typst 用扁平 `references/大写.md`）。zh 为中文语境，措辞与示例须中文本地化，不是英文直译。
2. **SKILL.md 版本同步规则**：改 SKILL.md 只更新 `last_updated`，**不 bump `version`**（全仓版本统一）。
3. **不碰 parsers.py**：本任务不改解析器，避免触发 `test_parsers_alignment` 锁。
4. **零捏造**：替换词典与示例不得引入虚构数据/引用；维护来源须真实可核。
5. 改完跑 `just ci`（lint → typecheck → test）必须全绿。

## 验收标准

- [ ] ① over-claim 参考文档在 3 技能各就位（en/typst 英文、zh 中文本地化），含动词梯子 + 7 替换表 + 陷阱句式表
- [ ] ① `tone-thresholds.yaml` 新增 over-claim 配置段（3 副本）；`deai_check.py` 新增 checker（3 副本），发 `[Script]` LOW，YAML 缺失可回退
- [ ] ① 新增针对 over-claim checker 的单元测试，通过
- [ ] ② de-AI 指南结构级痕迹小节就位（3 副本，zh 中文化）
- [ ] ③ 修改三层顺序原则就位（3 副本）+ 各 SKILL.md 润色路由一句话引导
- [ ] ④ 黑名单维护声明就位（3 副本），来源真实
- [ ] 3 个 SKILL.md 仅改 `last_updated`，`version` 不变
- [ ] `just ci` 全绿
- [ ] 不在范围内的技能（audit/cover-letter/bib）未被改动

## Notes
- ⑤（时态表颗粒度+信号词）与 ⑥（reviewer 怀疑点排序）已明确**不在本任务**，留作后续。
- ① 进 paper-audit 作为审计维度，列为独立 follow-up 任务。
