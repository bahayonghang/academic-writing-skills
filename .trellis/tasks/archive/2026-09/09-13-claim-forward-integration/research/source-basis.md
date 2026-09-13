# 研究：两个"对抗防御式写作"参考 skill 的来源与可信度

日期：2026-09-13。本文只记录来源事实与本仓库的兼容性判断；差量矩阵见 `delta-matrix.md`。

## 来源 A：Kiterlin/anti-defensive-writing

- 路径：`ref/defensive/anti-defensive-writing/`（`SKILL.md` 与 `skill/anti-defensive-writing/SKILL.md` 内容相同；另含 `agents/openai.yaml`、`skill.json`、`README.md`、`examples/`）。
- 来源：`https://github.com/Kiterlin/anti-defensive-writing.git`，MIT 许可。
- 层级：句子 / 段落级。核心内容：
  1. 10 项检测清单（先声明"不做什么"、免责声明前置、连续多层 hedge、限定词堆叠、`not X but Y` 壳、"It is worth noting"类空转、过程编年而非结论、以"仅/only"自贬、把限制写在主张前面、结论段新增自我否定）。
  2. 6 类句子功能分类（claim / evidence / scope / limitation / transition / process），用于判断哪一类句子被防御性表达替换。
  3. 5 步改写流程：定位主张 → 主张前置 → 范围正面化 → 限制归位（methods / discussion / limitations 写一次）→ 最小改动复核。
  4. preferred / discouraged 句式对照表。
  5. 明确要求"保留必要精度"：限制只删重复，不删本体。
- 可信度：单作者仓库，无外部评审证据；规则与 Nature/Science 写作指南中"claim first, scope positively"一致。适用于 EN 论文；ZH 需要词表翻译，不能直接移植正则。

## 来源 B：Adkid-Zephyr/anti-defensive-writing-Skill

- 路径：`ref/defensive/anti-defensive-writing-Skill/`（`skills/anti-defensive-writing/SKILL.md` 中文，`skills/anti-defensive-writing-en/SKILL.md` 英文，`prompts/精简版提示词.txt`、`prompts/quick-prompt-en.txt`、`README.md`）。
- 来源：`https://github.com/Adkid-Zephyr/anti-defensive-writing-Skill.git`，HEAD `102c8b2`，MIT 许可。
- 层级：叙事 / 篇章级（"学术发布会原则"）。核心内容：
  1. 6 条叙事规则（主张先于限制、围绕优势组织、不设自己赢不了的对比、删除非主线内容、结论不新增自我否定、最小改动）。
  2. 自我削弱词表：遗憾的是 / 仅 / 仍明显落后 / 效果有限 / 存在严重不足。
  3. "不说输"5 步（①删除不利对比 ②重构叙事 ③把劣势改写为范围 ④用优势覆盖 ⑤删除非主线结果）。
  4. 实验义务（每个主张有实验支撑）、摘要/引言开头 4 项、结论不新增自我否定。
  5. 7 级决策优先级、8 问自查、最小改动提示词。
- 可信度：单作者仓库，面向中文期刊/学位论文投稿语境；部分规则以"投稿通过"为目标而非"陈述准确"。

## 兼容性切分（本仓库红线）

采纳边界依据以下四个已有约束：

| 约束锚点 | 内容 | 对来源 B 的影响 |
|---|---|---|
| `latex-thesis-zh/references/writing/conclusion-guide-zh.md` | 技术缺陷类不利结果必须如实陈述，不得弱化、省略或改写为范围局限 | 否决"不说输"①③⑤、叙事规则"删除非主线内容"、"把劣势改写为范围" |
| `paper-audit/references/OVER_CLAIM_GUARD.md` | calibration, not timid prose；不得为显得果断而删除 caveat | 采纳"主张前置 + hedge 降到证据支撑档"，否决"删除不利对比" |
| `paper-audit/agents/critical_reviewer_agent.md` | cherry-picking 检测（选择性报告） | 否决"只围绕优势组织""不设赢不了的对比"（会被审稿 lane 直接判为 cherry-picking） |
| `AGENTS.md` 学术事实保护 | 不改 cite/ref/label/公式；不伪造结果；改动以 diff + severity/priority 输出 | 所有改写只能是候选（`[Script]` 恒 `NEEDS-LLM`） |

结论：来源 A 可整体采纳（句子级）；来源 B 只采纳"叙事顺序 / 措辞校准"部分，拒绝"选择性呈现"部分。详细逐条判定见 `delta-matrix.md`。

## 命名冲突

仓库已有 `.trellis/spec/academic-writing-skills/defensive-ai-rhetoric-contract.md`（归档任务 08-05）。那里的"defensive"指 **defensive speculative explanation**（多机制堆叠 + 末尾 caveat，C 档 LLM-only，禁止向三份 `deai_check.py` 添加 hedge 正则/阈值）。本任务的概念不同：作者对自己贡献的**自我削弱 / 主张后置**。为避免同名，本任务统一使用：

- 英文术语：**claim-forward**（模块名、脚本名、代码前缀 `CF-*`）。
- 中文术语：**主张前置**（检查目标）/ **自我削弱**（被检对象）。
- 不使用 "defensive" 作为模块名或代码前缀。

## ZH 基线证据（私有语料，仅研究用，不进测试）

对 `ref/thesis/decrypted/` 中 5 篇博士学位论文全文计数（2026-09-13 grep）：

| 词 | 5 篇合计 | 判定 |
|---|---|---|
| 遗憾的是 / 仍明显落后 / 存在严重不足 / 本文不试图 / 并不主张 / 应谨慎 | 0 | 高信号词，可入词表；零基线意味着不会误报正常论文 |
| 效果有限 | 1 | 入词表，Minor |
| 未能 | 3 | 入词表但需上下文门控（引用他人工作时豁免） |
| 尚未 | 1–2 | 排除：与 `analyze_abstract.py` T-PAIN 痛点词重叠，属于合法的问题陈述 |
| 仅 | 15–48 / 篇 | 排除裸 `仅`：绝大多数是 `仅为 0.018`（数值）与 `不仅`（连词）；只保留 `仅…而已`、`仅能` 等自贬搭配（待 C2 标定） |

EN 侧无同类私有语料；EN 词表的基线只能靠 `examples/` 与 evals fixture 自建，标注为 UNVERIFIED。

## 已有覆盖（拒绝重复实现，只做交叉引用）

| 来源规则 | 已有实现 |
|---|---|
| `not X but Y` 对比壳 | `deai_check.py` `BINARY_CONTRAST_SHELLS`（EN/ZH） |
| "It is worth noting / 值得注意的是 / 需要指出的是" | `deai_check.py` throat_clearing / `FAKE_INSIGHT` / `AI_FILLER_CONNECTORS` |
| 连接词密度 | deai D4 |
| 过度声明向下校准 | `over-claim-guard.md` / `OVER_CLAIM_GUARD.md` / `check_overclaim` |
| 摘要开头 | EN `analyze_abstract.py` 五要素；ZH T-OPEN/T-PAIN/T-LEAD/T-INNOV；paper-audit EIC pitch |
| 实验义务 | paper-audit claim-evidence map（`CLAIM_EVIDENCE_CONTRACT.md`） |
| 优势解释 | EN `analyze_experiment.py` B3 |
| 最小改动 | polish contract `--strength minimal` |
