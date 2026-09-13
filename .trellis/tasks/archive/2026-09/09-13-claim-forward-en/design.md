# C1 技术设计：check_claim_forward.py（EN）

## 边界

- 新脚本，独立于所有哈希锁模块；只 import `parsers`（`LatexParser.split_sections` / `extract_visible_text` / `get_comment_prefix`）与标准库；`yaml` 为可选 import（同 `analyze_logic.py` P-ARC 写法）。
- 输出到 stdout；`--json` 时输出 `{"file", "section", "findings": [...], "summary": {...}}`。
- 不写文件、不改源 tex。

## 数据流

```
main.tex -> LatexParser.split_sections() -> {section_key: body}
  -> (--section 过滤) -> 段落切分（空行 / \par）-> 句子切分（. ? ! 后接空格+大写；忽略 e.g. / i.e. / et al. / Fig. / Eq.）
  -> 每句打标：claim | limitation | disclaim | process | other（启发式，见下）
  -> 段内规则（CF-DISCLAIM / CF-CAVEAT-POS）+ 句内规则（CF-SELFWEAK / CF-HEDGE-STACK）+ 结论末段规则（CF-CLOSE-NEG）
  -> Finding(code, line, severity, priority, original, candidate, note)
  -> 文本渲染 / JSON
```

行号：优先用 `split_sections` 提供的 section 起始行 + 段内偏移；若不暴露起始行，用 `source.find(sentence)` 回退到首次出现行，与 `improve_expression.py` 的 `location` 写法一致。

## 句子功能启发式（来源 A 六分类的三类子集）

| 标签         | 触发                                                                                                                                                        |
| ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `claim`      | 主语 we / our / this paper / the proposed + 动词 propose / show / demonstrate / achieve / introduce / present / outperform / improve；或含数值 + 比较词     |
| `limitation` | 起始 however / although / while / despite / note that，或含 limitation / limited to / does not / cannot / fails to / only（仅作句法信号，不单独成 finding） |
| `disclaim`   | 句首 `We do not (claim                                                                                                                                      | argue     | attempt)`、`This (paper                                        | work) does not`、`It is not our (goal | intention)`、`Rather than`、`We make no claim` |
| `process`    | `We (first                                                                                                                                                  | initially | then) tried`、`After several attempts`、`Our initial approach` |
| `other`      | 其余                                                                                                                                                        |

## 五码规则

| 码               | 规则                                                                                                                                                                                                       | Severity / Priority                                                           | Candidate 生成                                                                            |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `CF-DISCLAIM`    | 段内首个 `disclaim` 句索引 < 首个 `claim` 句索引                                                                                                                                                           | Minor/P2（abstract, introduction, contribution, conclusion）；Info/P3（其余） | 首个 claim 句前移到段首，disclaim 句原文保留其后（不删）                                  |
| `CF-SELFWEAK`    | terms YAML `self_weakening` 搭配命中（regrettably, unfortunately, merely, only marginally, still lags far behind, of limited effect, suffers from serious, falls short of, we were unable to）；引用句豁免 | Minor/P2                                                                      | 用 YAML `prefer` 模板替换该搭配（如 falls short of -> reaches {ratio} of，占位由 LLM 填） |
| `CF-CAVEAT-POS`  | 段内首个 `limitation` 句索引 < 首个 `claim` 句索引，且该段非 Limitations 段                                                                                                                                | Info/P3                                                                       | 主张句与限制句交换顺序，其余不动                                                          |
| `CF-HEDGE-STACK` | `claim` 句内 hedge 词表命中数 ≥3（may, might, could, possibly, potentially, to some extent, in some cases, under certain conditions, somewhat, relatively, arguably, it seems, appears to）                | Info/P3                                                                       | 保留最强一个 hedge，删其余；候选注明 check over-claim ladder                              |
| `CF-CLOSE-NEG`   | `conclusion` / `summary` 末段出现 `limitation` 或 `self_weakening` 命中，且其后同段无方向标记（future work, we plan, will, next step, opens, promising）                                                   | Minor/P2                                                                      | 追加方向句占位 `[LLM: add direction]`；不删负面判定                                       |

## 豁免

- 句内含 `\cite{`，或前一句含 `\cite{` 且本句主语为 they / these methods / prior work / existing。
- 数学环境文本已由 `extract_visible_text` 剥离。
- section key 为 `limitations`，或 `\section*{Limitations}` / `\paragraph{Limitations}` 内：跳过 `CF-CAVEAT-POS` 与 `CF-CLOSE-NEG`。
- `related` 段跳过 `CF-DISCLAIM`（related work 中 "we do not survey" 属合法范围声明）。
- 同句已被 deai `BINARY_CONTRAST_SHELLS` / throat_clearing 覆盖的模式不在本脚本词表内（去重靠词表不重叠，不靠运行时调用 deai）。

## terms YAML 结构

```yaml
version: 1
self_weakening:
  - match: "falls short of"
    prefer: "reaches {ratio} of"
  - match: "still lags far behind"
    prefer: "trails {baseline} by {gap}"
hedges:
  [
    may,
    might,
    could,
    possibly,
    potentially,
    "to some extent",
    "in some cases",
    "under certain conditions",
    somewhat,
    relatively,
    arguably,
    "it seems",
    "appears to",
  ]
disclaim_openers:
  [
    "we do not claim",
    "we do not argue",
    "this paper does not",
    "it is not our goal",
    "we make no claim",
    "rather than",
  ]
direction_markers:
  ["future work", "we plan", "next step", "opens", "promising", "will"]
process_openers:
  [
    "we first tried",
    "we initially",
    "after several attempts",
    "our initial approach",
  ]
```

脚本内 `_DEFAULT_TERMS` 与 YAML 等值；测试用 monkeypatch 指向不存在的 YAML 路径验证 fallback。

## 与现有契约的关系

- polish contract：`claim-forward` 在 "`[LLM]` layer only" 组。脚本输出的 `Candidate` 是建议不是替换文本，故不带 Changed/Protected/Risk-Flags 四字段；LLM 采纳后按 `[LLM]` 层输出四字段。`Meaning-Check: NEEDS-LLM` 保留以对齐 expression 输出风格。
- deai：`CF-HEDGE-STACK` 是 hedge 计数，deai 契约禁止的是向 `deai_check.py` 加 hedge 正则；本脚本独立，不触碰契约。
- over-claim guard：候选中任何升级措辞都标注 check over-claim ladder；脚本不判断证据档。

## 兼容与回滚

- 全新文件，删除脚本 + 路由行 + 测试即回滚；SKILL.md 与 routing-rules 改动为增行。
- `EXPECTED_ABSENCES` 注册保证 typst 缺失不触发对齐测试失败。

## 取舍

- 独立脚本而非 `improve_expression.py --goal claim-forward`：后者被 TIER1 哈希锁（en+typst 字节一致）阻断；expression 的 `--goal` 语义是润色目标，不含段落级顺序规则。
- 正则而非 LLM-only：来源 A 的 10 项中 5 项可确定性检出，且 ZH 零基线证据支持低误报；其余（过程编年、叙事重构）留 LLM。
- 不做自动重排：候选只展示顺序调换，不生成新句，避免伪造主张。
