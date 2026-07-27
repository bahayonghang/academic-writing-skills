# Module: 中文表达检查（expression）

**触发**：这段太口语、改学术一点、句子太长太绕、标点乱、搭配不当、数值单位写法

**规则真相源**：[academic-style-zh.md](../writing/academic-style-zh.md)；数字与单位另见 [number-unit-guide-zh.md](../formatting/number-unit-guide-zh.md)。

## 命令

```bash
uv run python -B $SKILL_DIR/scripts/check_style_zh.py main.tex
uv run python -B $SKILL_DIR/scripts/check_style_zh.py main.tex --section 绪论
uv run python -B $SKILL_DIR/scripts/check_style_zh.py main.tex --goal concision --strength moderate
uv run python -B $SKILL_DIR/scripts/check_style_zh.py main.tex --max-chars 70 --json
```

`--goal`（默认 `grammar`）与 `--strength`（默认 `minimal`）声明编辑范围，见 [routing-rules.md](routing-rules.md)。`--goal coherence` 在本模块无规则，会路由到 `logic`。`--tier` 与二者无关，它是 `deai` 的检测灵敏度。

## 边界：本模块不做什么

每一格都有既有 owner，重造必冲突。

| 领域                      | Owner                                                 | 本模块的处置                                                                              |
| ------------------------- | ----------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| 人称（我们 / 本文）       | `abstract` 的 T-VOICE / T-OPEN                        | **不实现任何人称检查**；T-VOICE 只查第一人称，T-OPEN 查首句是否定位研究对象，两者维度不同 |
| 论断强度分级              | [over-claim-guard.md](../writing/over-claim-guard.md) | 只做词汇层替换建议（`E-ABSOLUTE`），强度分级不重复实现                                    |
| 模板专属数字规范          | `spec-check` 的 YS-36（判定方式 `llm`）               | 只做通用可判定项（间距、正斜体、概数/序数用字），定稿终检走 `spec-check`                  |
| 句长均匀度（CV，AI 痕迹） | `deai` 的 D1（需 `--tier`）                           | 只查**单句可读性长度**；均匀度不在此，两者不报同一条                                      |
| 段落顺序与论证            | `logic`                                               | 不触碰                                                                                    |
| 结论 / 摘要章骨架         | `conclusion` / `abstract`                             | 不触碰                                                                                    |

## 九个检查器与分档

**A = auto**（判定确定，给替换建议）/ **B = candidate**（只报候选，不给替换文本）。

| ID           | 依据          | 输入区域                                 | 排除条件                                                          | 档            |
| ------------ | ------------- | ---------------------------------------- | ----------------------------------------------------------------- | ------------- |
| `E-COLLOQ`   | style-zh §1.1 | 可见中文正文                             | 「特别是」是 §3.4 推荐的举例连接词，不报                          | A             |
| `E-ABSOLUTE` | style-zh §2   | 可见中文正文                             | 引述他人观点的语境（`文献[N]`、`已有研究`、`前人研究`…）          | B             |
| `E-COLLOC`   | style-zh §4.1 | 可见中文正文                             | 动宾之间允许「了/过」与 ≤6 字定语，但不跨标点                     | A             |
| `E-INCOMP`   | style-zh §4.2 | 以「通过/经过/利用/借助/采用」开头的句子 | 句中已有主语标记（本文、本研究、作者、该方法…）                   | B             |
| `E-PUNCT`    | style-zh §5.3 | 含中文字符的行                           | 行内英文片段、全英文括号（§5.2/§5.3 的两条豁免）、URL/路径/文件名 | B             |
| `E-NUMSPACE` | style-zh §6.2 | 可见正文的「数字+单位」                  | 百分号、千分号、角度、摄氏度等按国标不空格的量                    | A             |
| `E-UNITFONT` | style-zh §6.2 | **数学环境内（只读）**                   | 已用 `\mathrm` / `\text` / `\si` 等正体包裹                       | B（永不 fix） |
| `E-NUMSTYLE` | style-zh §6.1 | 可见中文正文                             | 图/表/式/章/节/条/页/卷/册/第 之后的编号                          | B             |
| `E-LONGSENT` | 可读性        | 可见中文正文，按中文标点断句             | 公式行、表格行、列举项、环境行                                    | B             |

**`E-INCOMP` 为什么不能是 A 档**：中文承前省略主语是合法且普遍的（「本文提出 X 方法。通过实验，验证了其有效性。」第二句省略「本文」在学位论文中完全可接受）。规则只能识别句式模式，无法判定是否真缺主语。

**`E-PUNCT` 为什么不能是 A 档**：`academic-style-zh.md` §5.2/§5.3 自身就给了两条允许英文标点的例外。排除区可实现，但中英混排的复合括号等边界情况无法穷举。

**`E-UNITFONT` 的特殊性**：检出是确定的，但问题位于数学环境内，而「绝不修改数学环境」是红线一。因此它只报告、永不给替换文本，输出中明确写「需作者手动调整」。**分档依据是红线而非判定能力**——不要误当成可以升 A 档。

**style-zh §1.3 的单字动词（用/做/看/想/试）不实现**：它们是「采用」「制作」「看法」等合法词的子串，规则层无法判定，属 llm-only。这类替换由 `[LLM]` 层按 §1.3 表格判断。

## 输出形态

A 档（给替换建议）：

```latex
% EXPRESSION (chapters/chap03.tex:42) [Severity: Warning] [Priority: P2] [Script]: E-COLLOC 搭配不当
% 原文: 该策略有效增加了模型的效率。
% 建议: 该策略有效提高了模型的效率。
% 依据: academic-style-zh.md §4.1（增加效率 → 提高效率）
% Changed:       1 collocation fix (增加了模型的效率 -> 提高了模型的效率)
% Protected:     none
% Meaning-Check: NEEDS-LLM
% Risk-Flags:    lexical-substitution
```

B 档（无「建议」行，只有「候选」）：

```latex
% EXPRESSION (chapters/chap03.tex:57) [Severity: Info] [Priority: P3] [Script]: E-INCOMP 疑似成分残缺
% 原文: 通过对比实验，验证了所提方法的有效性。
% 候选: 「通过/经过/利用…，<动词>了…」句式疑似缺主语；中文承前省略主语亦合法，请人工判断
% 依据: academic-style-zh.md §4.2（成分残缺）
% Changed:       none
% Protected:     none
% Meaning-Check: NEEDS-LLM
% Risk-Flags:    not-assessed
```

## 改写契约

本模块产出可直接替换原文的文本，适用改写契约。`[Script]` 层输出恒为 `Meaning-Check: NEEDS-LLM`，且只允许置规则可确定的标记（`none`、`not-assessed`、`lexical-substitution`、`whitespace-normalized`）；只有 `[LLM]` 层可提出 `PRESERVED`，且仍是待作者核对的提案。字段定义与 `Risk-Flags` 闭集见 `references/modules/routing-rules.md`。

改写不得升高措辞强度。把留有余地的表述换成更强的断言（「可能」→「能够」、「有助于」→「显著提升」）是过度声称，不是表达改善：保持原强度，或置 `Risk-Flags: overstatement` 并明确说明。判据见 [over-claim-guard.md](../writing/over-claim-guard.md)——本模块只做词汇层替换建议，强度分级不在此重复实现。
