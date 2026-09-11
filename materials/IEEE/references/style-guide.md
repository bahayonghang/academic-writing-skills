# IEEE 写法总则

只引用 `core` 行。语料：261 篇 complete observation（2026-09-11）。

IEEE 自称（`this article proposes` / `we propose` / `This study introduces`）进 `phrase_bank`，不进 `anti_ai_patterns`。不要套 Nature 的 `Here we` 或 methods-last。

## 自称

| 用法 | ID | paper_count |
| --- | --- | ---: |
| `this article proposes` | R009 / P013 | 68 |
| `To address these limitations, we propose` | P007 | 5 |
| `This study introduces` | P001 | 7 |
| `is developed in this article` | P011 | 5 |

## 节序

| 模式 | ID | paper_count |
| --- | --- | ---: |
| Related Work 并入 Introduction | R002 / SP-IEEE-002 | 167 |
| 独立 Related Work | R006 / SP-IEEE-001 | 94 |
| Introduction 末 `The rest of this article is organized as follows` | R003 / P005 | 81 / 65 |

两种节序都是 IEEE Transactions 常态。有独立综述节时用 R006；综述写在引言中段时用 R002。

## 贡献与收束

| 用法 | ID | paper_count |
| --- | --- | ---: |
| 编号贡献列表（引导句随篇变化） | R004 | 121 |
| `The main contributions of this article are as follows.` | P004 | 19 |
| 结论局限 + future work / future research | R005 | 145 |
| `In future work` | P021 | 14 |

## Hedge

动词频次见 `knowledge/hedge_verbs.tsv`（该表尚未按 261 篇全量重聚）。complete 观察里 `propose` / `demonstrate` / `show` 是方法与结果的常用动词；`indicate` 用于较弱结果句。
