# 模块：主张前置检查（claim-forward）

**触发**：主张前置、自我削弱、"写得太谦虚/像在道歉"、"先说本文不做什么"、hedge 堆叠、结论末段负面收尾、"本文不试图"、"遗憾的是"。

**目的**：检出把论文自身主张后置或削弱的表述（主张前的免责句、写在主张前面的限制句、自我削弱搭配、主张句上的 hedge 堆叠、以负面判定收尾且无展望方向的结论末段），并给出最小的顺序调换或搭配替换候选。本模块绝不删除任何限制、不利对比或非主线结果；只改顺序与措辞。

## 命令

```bash
uv run python $SKILL_DIR/scripts/check_claim_forward.py main.tex
uv run python $SKILL_DIR/scripts/check_claim_forward.py main.tex --section introduction
uv run python $SKILL_DIR/scripts/check_claim_forward.py main.tex --section conclusion --json
```

`--section` 接受与其他模块相同的英文键与中文章节名（`introduction` / `绪论`、`contribution`、`results`、`discussion`、`conclusion` / `结论与展望` …）。不传 `--section` 时扫描全部识别到的章节。多文件工程经 `tex_loader` 展开 `\input` / `\include`。退出码恒为 0；未知章节打印 `ERROR` 行并列出可用键。

## 脚本原始输出

五个 `[Script]` 码。每个块带 `Original`、`Candidate` 与 `Meaning-Check: NEEDS-LLM`；候选是给 `[LLM]` 层的提案，不是替换文本。

| 码               | 触发条件                                                                                                                                             | Severity / Priority                                                 | 候选形态                                                          |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- | ----------------------------------------------------------------- |
| `CF-DISCLAIM`    | 段内首个否定式免责句（"本文不试图 …""本文并不主张 …"）出现在首个主张句之前                                                                            | 摘要、绪论、贡献、结论章 Minor / P2；其余章 Info / P3                | 主张句前置，免责句保留在其后                                      |
| `CF-SELFWEAK`    | 对自身结果使用自我削弱搭配（`遗憾的是`、`仍明显落后于` 不门控；`效果有限`、`存在严重不足`、`并不理想`、`仅能` / `仅仅` / `未能` 等须句中有自身主语） | Minor / P2                                                          | 搭配替换为 `prefer` 模板，`{占位}` 由 LLM 从稿件证据填入          |
| `CF-CAVEAT-POS`  | 同一段内**关于自身工作**的限制句（含本文 / 本章 / 所提 / 该方法 等主语）先于其限定的主张句                                                          | Info / P3                                                           | 主张句与限制句调换；限制句保留                                    |
| `CF-HEDGE-STACK` | 同一主张句叠加三个及以上 hedge（`可能`、`或许`、`在一定程度上`、`似乎` …）                                                                           | Info / P3                                                           | 保留第一个 hedge，去掉其余；注释提示先对照过度声明阶梯再加强      |
| `CF-CLOSE-NEG`   | 结论 / 总结章**末段**以负面判定结束，其后同段无方向标记（`展望`、`未来工作`、`有待`、`下一步` …）                                                    | Minor / P2                                                          | 原句后追加 `[LLM: add the direction this limitation points to]` |

汇总行：`% CLAIM-FORWARD: <n> finding(s) (CF-...=k, ...)`。

## 脚本内置豁免

- 含 `\cite` / `\upcite` / `\citep` / `\citet` 的句子，以及其后一句若主语为前人工作（`该类方法`、`上述方法`、`现有方法`、`传统方法`、`文献`、`他们` …）。说前人工作有不足属于合法比较。
- 标题含 `不足` / `局限` / `研究范围` / `范围界定` 的小节：限制本就该写在那里，其内关闭 `CF-DISCLAIM`、`CF-CAVEAT-POS`、`CF-CLOSE-NEG`；带 `subject_gate` 的搭配（`仅能` / `仅仅` / `未能`）也不报。
- `related`（相关工作 / 研究现状）段关闭 `CF-DISCLAIM`（"本文不综述 …"是范围陈述）。
- “然而 … 难以 … 因此本文提出 …”这类问题陈述不是自身限制，`CF-CAVEAT-POS` 不报（5 篇基线中该形态占位置类命中的 90% 以上，是中文学位论文段落的正常动机结构）。
- 裸 `仅`、`尚未`、`不能`、`只` 永不触发（`仅为 0.018`、`不仅` 是数值与递进用语，`尚未解决` 是摘要痛点词 T-PAIN 的合法用语）；只有 `references/writing/claim-forward-terms-zh.yaml` 里的搭配才触发。带 `subject_gate` 的搭配（`效果有限`、`存在严重不足`、`存在较大差距`、`并不理想`、`差强人意`、`略显不足`、`仅能`、`仅仅`、`未能`）须句中出现本文 / 本章 / 本研究 / 所提 / 本方法 / 提出的 主语才报；只有 `遗憾的是` / `令人遗憾` / `仍明显落后` 类不门控。
- `有望` 在结论 / 总结章不计入 hedge 堆叠（展望语境合法）。
- 数学环境、引用命令、标签、题注在匹配前由解析器剥离。

## Skill 层响应

1. 对请求的章节运行脚本（默认先跑 `introduction`、`contribution`、`conclusion`，代价最高）。
2. 对每条发现，按 [claim-forward-zh.md](../writing/claim-forward-zh.md) 判定：该句是主张、范围陈述、限制还是过程叙述？只调序或替换搭配，绝不删除 caveat。
3. 在加强任何措辞之前，先查 [over-claim-guard.md](../writing/over-claim-guard.md) 的"向上校准"节。阶梯是上限：claim-forward 只把措辞抬到证据已经支撑的那一级，不越级。
4. 改写以 `[LLM]` 层块输出，带四个契约字段（`Changed`、`Protected`、`Meaning-Check`、`Risk-Flags`）；`[Script]` 块本身保持 `NEEDS-LLM`。
5. 同时应用写作指南中仅 `[LLM]` 的判断 `CF-LOSS-FRAME`（过程编年，如"起初尝试 X，失败后改用 …"）；脚本不发该码。

## 与其他模块的边界

- `deai`：`不是 X 而是 Y` 对比壳与"值得注意的是 / 需要指出的是"清嗓子句留在 `deai`，不进本模块词表。本模块的 hedge 计数与 `deai_check.py` 无关，后者按契约不含 hedge 正则。
- `abstract`：摘要骨架与痛点词（T-PAIN / T-OPEN / T-VOICE）归 `abstract`；本模块在摘要只报先于首个主张的免责句，不报痛点陈述。
- `conclusion`：`CC-OUTLOOK-TRANS` 查"展望前有承接"，`CF-CLOSE-NEG` 查"负面判定后无方向"，两者不冲突——负面判定 + 承接句 + 展望即同时通过。结论章三段式、贡献动词、展望空话仍归 `conclusion`。
- `expression`：`E-ABSOLUTE` 处理绝对化词汇（方向相反：过度声称 vs 自我削弱），词表零交集；claim-forward 输出不是词汇替换表，也不走 `--goal` / `--strength`。
- `experiment` / paper-audit 主张—证据映射：主张有没有证据归它们；本模块假定证据已存在，只修主张的位置和措辞。

## 词表

`references/writing/claim-forward-terms-zh.yaml`（字段：`self_weakening`（含 ZH 特有 `subject_gate`）、`hedges`、`disclaim_openers`、`direction_markers`、`process_openers`、`limitation_section_titles`）。脚本内置等值回退表，YAML 缺失或某字段非法时按字段回退。词表基线来自 5 篇私有博士学位论文（只做研究，不进测试），搭配级精度按该基线调过；调词表改 YAML，不改代码。
