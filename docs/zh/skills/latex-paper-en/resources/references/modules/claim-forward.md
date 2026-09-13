# 模块：主张前置检查（Claim-Forward）

**触发**：claim-forward、主张前置、自我削弱、防御性语气、under-claiming、"读起来像在道歉"、"先说我们不做什么"、hedge 堆叠、结尾段乏力

**目的**：检出把论文自身主张后置或削弱的表述（主张前的免责声明、主张前的限制句、自我削弱搭配、hedge 堆叠、以负面判定收尾的结论段），并给出最小的重排或替换建议。本模块绝不删除任何限制、不利对比或非主线结果；只改顺序与措辞。

## 命令

```bash
uv run python -B scripts/check_claim_forward.py main.tex
uv run python -B scripts/check_claim_forward.py main.tex --section introduction
uv run python -B scripts/check_claim_forward.py main.tex --section conclusion --json
```

`--section` 接受与其他模块相同的键与别名（`introduction`、`contribution`、`results`、`discussion`、`conclusion` 等）。不带 `--section` 时扫描全部已识别章节。退出码恒为 0；未知章节会打印一行 `ERROR` 并列出可用键。

## 脚本原始输出

五个 `[Script]` 观察码。每个块都带 `Original`、`Candidate` 与 `Meaning-Check: NEEDS-LLM`；候选是给 LLM 层的提案，不是替换文本。

| 码 | 触发条件 | Severity / Priority | 候选形态 |
| --- | --- | --- | --- |
| `CF-DISCLAIM` | 段内首个范围否定句（"We do not claim ..."、"This paper does not ..."）出现在首个主张句之前 | abstract、introduction、contributions、conclusion 中为 Minor / P2；其余为 Info / P3 | 主张句前移，免责句保留在其后 |
| `CF-SELFWEAK` | 对作者自身结果使用自我削弱搭配（`regrettably`、`still lags far behind`、`falls short of`、`of limited effect`、`only marginally`、`we were unable to` 等） | Minor / P2 | 搭配被 `prefer` 模板替换，模板中的 `{placeholders}` 由 LLM 从稿件证据填入 |
| `CF-CAVEAT-POS` | 同一段内限制句位于它所限定的主张句之前 | Info / P3 | 主张句与限制句交换顺序；限制句保留 |
| `CF-HEDGE-STACK` | 一个主张句上叠加三个及以上 hedge（`may`、`possibly`、`to some extent`、`in some cases` 等） | Info / P3 | 保留第一个 hedge，删去其余；备注要求先对照过度声明阶梯再加强措辞 |
| `CF-CLOSE-NEG` | 结论 / 总结章的最后一段以负面判定收尾，其后没有方向标记（`future work`、`we plan`、`opens` 等） | Minor / P2 | 原句加 `[LLM: add the direction this limitation points to]` |

汇总行：`% CLAIM-FORWARD: <n> finding(s) (CF-...=k, ...)`。

## 豁免（脚本内置）

- 含 `\cite`/`\citep`/`\citet` 的句子，以及紧随其后、主语为已有工作的句子（`these methods`、`prior`、`existing`、`they` 等）。把已有工作描述为不足属于正当比较。
- 任何 `Limitations` 标题（`\section*{Limitations}`、`\paragraph{Limitations}`）：限制本就该写在那里，因此其内部关闭 `CF-DISCLAIM`、`CF-CAVEAT-POS` 与 `CF-CLOSE-NEG`。
- Related Work：关闭 `CF-DISCLAIM`（"we do not survey ..." 是范围声明）。
- 裸 `only`、`limited`、`not` 不触发；只有 `references/writing/claim-forward-terms.yaml` 中的搭配才触发。
- 数学、引用、标签与题注在匹配前已被解析器剥离。

## 技能层响应

1. 对请求的章节运行脚本（默认先跑 `introduction`、`contribution`、`conclusion`；它们代价最高）。
2. 对每个发现，按 [claim-forward.md](../writing/claim-forward.md) 判定：该句是主张、范围声明、限制还是过程叙述？只重排或替换；绝不删除 caveat。
3. 加强任何措辞之前，先核对 [over-claim-guard.md](../evidence/over-claim-guard.md)（"向上校准"节）中的证据档。阶梯是上限；claim-forward 只把措辞抬到证据已支撑的那一档，绝不越过。
4. 以 `[LLM]` 层块输出改写，带契约四字段（`Changed`、`Protected`、`Meaning-Check`、`Risk-Flags`）；`[Script]` 块本身保持 `NEEDS-LLM`。
5. 同时应用写作指南中仅属 `[LLM]` 的判断 `CF-LOSS-FRAME`（过程编年，如 "We first tried X, which failed, then ..."）；脚本不发该码。

## 与其他模块的边界

- `deai`：`not X but Y` 对比壳与 "It is worth noting" 类空转留在 `deai`；它们不在本模块词表内。这里的 hedge 计数与 `deai_check.py` 无关，后者按契约不含任何 hedge 正则。
- `abstract`：开头结构诊断（五要素）属于 `abstract`；本模块只报告位于摘要首个主张之前的免责声明。
- `expression`：词汇层语气润色；claim-forward 输出不是词汇替换表，也不经 `--goal`/`--strength` 处理。
- `experiment` / paper-audit 的 claim-evidence map：主张是否有证据归它们管；本模块假定证据存在，只修主张的位置与措辞。

## 词表

`references/writing/claim-forward-terms.yaml`（字段：`self_weakening`、`hedges`、`disclaim_openers`、`direction_markers`、`process_openers`）。脚本内置等值回退表，YAML 缺失或某字段非法时按字段回退。EN 搭配精度 UNVERIFIED（仅合成 fixture）；调词表而不是改代码。
