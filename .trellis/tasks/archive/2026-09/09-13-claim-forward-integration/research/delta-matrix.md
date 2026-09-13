# 研究：差量矩阵（来源规则 × 现有实现 × 判定）

日期：2026-09-13。判定取值：**采纳**（新增实现）/ **改编**（换形态后采纳）/ **已覆盖**（只交叉引用）/ **否决**（与红线冲突）。Owner：C1 = latex-paper-en，C2 = latex-thesis-zh，C3 = paper-audit。

## 逐条判定

| # | 来源锚点 | 增量内容 | 现有实现锚点 | 判定 | Owner | 落点 |
|---|---|---|---|---|---|---|
| S1 | A 清单 1 | 段落/摘要先声明"不做什么"再说做什么 | 无 | 采纳 | C1/C2/C3 | `CF-DISCLAIM`：段首否定式免责句（"We do not claim / 本文不试图 / 并不主张"）出现在该段第一个主张之前 |
| S2 | A 清单 2、B 词表 | 自我削弱词（regrettably / merely / still lags far behind / limited effect / 遗憾的是 / 仍明显落后 / 效果有限 / 存在严重不足） | 无 | 采纳 | C1/C2/C3 | `CF-SELFWEAK`：词表命中 + 引用上下文豁免；裸 `仅` / `only` / `尚未` / `limited` 排除 |
| S3 | A 清单 3 | 同句连续 ≥3 层 hedge（may / possibly / to some extent / 可能 / 在一定程度上 / 或许） | deai 禁加 hedge 正则（`defensive-ai-rhetoric-contract.md`） | 改编 | C1/C2 | `CF-HEDGE-STACK` 放在新脚本 `check_claim_forward.py`，不进 `deai_check.py`；阈值 3，只报主张句 |
| S4 | A 清单 4 | 限定词堆叠（in some cases, under certain conditions, to a certain degree 连用） | 无 | 改编 | C1/C2 | 并入 `CF-HEDGE-STACK` 的计数词表，不单设代码 |
| S5 | A 清单 5 | `not X but Y` 壳 | deai `BINARY_CONTRAST_SHELLS` | 已覆盖 | — | 模块文档交叉引用 deai |
| S6 | A 清单 6 | "It is worth noting" 类空转 | deai throat_clearing / `FAKE_INSIGHT` | 已覆盖 | — | 交叉引用 |
| S7 | A 清单 7 | 过程编年（"We first tried… then…"）代替结论 | 无 | 采纳（LLM 层） | C1/C2 | `[LLM]` 判断项，写入 `references/writing/claim-forward.md`；脚本不做 |
| S8 | A 清单 8 | 以 only / merely / 仅 自贬结果 | 无 | 改编 | C1/C2 | 并入 `CF-SELFWEAK`，仅收搭配（`only marginally`、`仅能`、`仅…而已`），裸词排除（ZH 基线 15–48/篇） |
| S9 | A 清单 9 | 限制句写在主张句前面（同段） | 无 | 采纳 | C1/C2/C3 | `CF-CAVEAT-POS`：段内第一个限制句索引 < 第一个主张句索引 |
| S10 | A 清单 10、B 规则 5 | 结论段新增自我否定且无方向 | ZH `CC-OUTLOOK-TRANS` 要求展望前有承接句 | 改编 | C1/C2/C3 | `CF-CLOSE-NEG`：结论末段出现负面判定且后文无展望/方向标记；ZH 侧承接句合法，不报 |
| S11 | A 分类 | 6 类句子功能分类 | 无 | 改编 | C1/C2 | 脚本只用 claim / limitation / process 三类启发式；其余留给 `[LLM]` |
| S12 | A 改写 5 步 | 定位主张 → 前置 → 范围正面化 → 限制归位 → 最小复核 | polish contract 四字段 | 改编 | C1/C2 | 写入 `references/writing/claim-forward.md`，输出走 polish contract（Changed/Protected/Meaning-Check/Risk-Flags） |
| S13 | A 对照表 | preferred / discouraged 句式 | 无 | 采纳 | C1/C2 | `references/writing/claim-forward-terms.yaml`（EN）/ `claim-forward-zh.md` 表格（ZH） |
| S14 | A "保留必要精度" | 限制只在 methods / discussion / limitations 写一次 | `over-claim-guard.md` | 采纳 | C1/C2/C3 | 写入 over-claim-guard 新增"向上校准"节，与向下校准并列 |
| S15 | B 规则 1 | 主张先于限制 | 同 S9 | 已并入 | — | — |
| S16 | B 规则 2 | 只围绕优势组织 | `critical_reviewer_agent.md` cherry-picking | 否决 | — | 与选择性报告检测冲突 |
| S17 | B 规则 3 | 不设自己赢不了的对比 | 同上 + `conclusion-guide-zh.md` | 否决 | — | 删除不利对比 = 弱化不利结果 |
| S18 | B 规则 4 | 删除非主线内容 | `conclusion-guide-zh.md` | 否决 | — | 不利结果不得省略 |
| S19 | B "不说输" ②④ | 重构叙事顺序、用优势语句先行 | 无 | 改编 | C1/C2 | 只保留"顺序"含义，写入参考文档；①③⑤ 否决 |
| S20 | B 实验义务 | 每个主张有实验支撑 | paper-audit claim-evidence map | 已覆盖 | — | 交叉引用 |
| S21 | B 摘要/引言开头 4 项 | 开头先说贡献 | EN `analyze_abstract.py` 五要素；ZH T-OPEN 等 | 已覆盖 | — | 交叉引用；`CF-DISCLAIM` 对 abstract/introduction 段加权为 Minor |
| S22 | B 7 级决策优先级 | 1/3/5/6 级为选择性呈现 | — | 否决 1/3/5/6；采纳 2/4/7（顺序、措辞、最小改动） | C1/C2 | 参考文档"取舍说明"节 |
| S23 | B 8 问自查 | #1 主张是否第一句 #2 限制是否在主张后 #4 是否有自贬词 #8 结论是否新增否定 | 无 | 采纳 4 问；否决 #6（"是否删掉了不利对比"）等 | C1/C2/C3 | 参考文档"自查四问"；C3 进 `SUBAGENT_TEMPLATES.md` DO 列表 |
| S24 | B 最小改动提示词 | 逐句最小改写 | polish `--strength minimal` | 已覆盖 | — | 交叉引用 |

## 采纳汇总

| 代码 | 名称 | 层 | Severity | 段落门控 | Owner |
|---|---|---|---|---|---|
| `CF-DISCLAIM` | 段首否定式免责在主张前 | Script | Minor（abstract/introduction/contribution/conclusion）/ Info（其余） | 全部 | C1 C2 C3 |
| `CF-SELFWEAK` | 自我削弱词（搭配级） | Script | Minor | 全部；引用上下文豁免 | C1 C2 C3 |
| `CF-CAVEAT-POS` | 限制句位于主张句前 | Script | Info | 全部 | C1 C2 C3 |
| `CF-HEDGE-STACK` | 单句 ≥3 层 hedge | Script | Info | 主张句 | C1 C2 |
| `CF-CLOSE-NEG` | 结论末段负面判定无方向 | Script | Minor | conclusion / summary | C1 C2 C3 |
| `CF-LOSS-FRAME` | 过程编年 / 输者叙事 | LLM only | — | — | C1 C2（文档） |
| 自查四问 | S23 采纳部分 | LLM only | — | — | C1 C2 C3（文档） |

C3 只使用前三个加 `CF-CLOSE-NEG` 共 **5 个**观察码（`CF-HEDGE-STACK` 需句级计数，审稿 lane 不做）；固定集合由契约测试锁定。

## 与现有阈值/契约的关系

- `CF-HEDGE-STACK` 阈值 3 与 deai 的 hedge 相关规则无交集（deai 无 hedge 正则，且契约禁止添加）。
- `CF-*` 全部 exit 0、`[Script]` 恒 `NEEDS-LLM`，与 polish contract 一致。
- 不改 `analyze_conclusion.py`（其结果经 `zh_check_adapters.py` 流入 paper-audit，新增会改变审稿评分输入）。
- 不改 TIER1 哈希锁模块（`analyze_abstract` / `analyze_grammar` / `analyze_sentences` / `improve_expression`）。
- 新脚本注册 `EXPECTED_ABSENCES["check_claim_forward.py"] = ["typst"]`；typst 本轮不在范围。
