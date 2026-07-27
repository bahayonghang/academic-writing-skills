# 模块：表达重组

**触发**：学术语气、学术表达、提高写作、弱动词

## 脚本应用的规则

自动应用（大小写随原 token 保留）：

| 模式       | 替换     |
| ---------- | -------- |
| `get`      | `obtain` |
| `a lot of` | `many`   |

只报候选、绝不自动应用——模式可检出，但规则无法判断某次用法是误用还是正确用法：

| 模式      | 为何停在候选                                                              |
| --------- | ------------------------------------------------------------------------- |
| `make`    | "Make sure"、"make use of" —— 自动替换实测产出 "develop sure" / "develop use of" |
| `very`    | "very few" —— 自动替换实测产出 "highly few"                               |
| `kind of` | 删掉它会改变 "a kind of transformer" 的含义                               |

**不要把 `use → employ`、`show → demonstrate` 加回来。** 它们是被有意删除的：de-AI 指南把 "we use ..." 列为正确的学术英语，把 "demonstrate the effectiveness" 列为 AI 痕迹，套用这两条会让本模块与 [deai.md](deai.md) 互相打架（finding E15）。加搭配排除表也不是解法——`make sense`、`make up`、`make do`、`make it` 是开放集，漏一个就产出错误英语。

受保护 token（统计值、带单位数值、模型/数据集/基因名）在替换前被遮蔽，并列入 `Protected:`。完整分级：[protected-tokens.md](../writing/protected-tokens.md)。

```bash
uv run python -B scripts/improve_expression.py main.tex
uv run python -B scripts/improve_expression.py main.tex --section related
uv run python -B scripts/improve_expression.py main.tex --goal clarity --strength moderate
```

`--goal`（默认 `grammar`）与 `--strength`（默认 `minimal`）声明编辑范围，见 [routing-rules.md](routing-rules.md)。`--goal coherence` 在本模块无规则，会路由到 `logic`。

输出格式：

```latex
% CONTRACT [Script]: goal=grammar strength=minimal
% EXPRESSION (Line 23) [Severity: Minor] [Priority: P2] [Script]: Improve academic tone
% Original: We get 92.1\% accuracy on CIFAR-100.
% Revised:  We obtain 92.1\% accuracy on CIFAR-100.
% Rationale: Weak verb replaced: \bget\b -> obtain
% Changed:       1 lexical substitution(s): get -> obtain
% Protected:     92.1\%, CIFAR-100
% Meaning-Check: NEEDS-LLM
% Risk-Flags:    lexical-substitution
```

候选块（无 `Revised:` 行——脚本拒绝猜）：

```latex
% EXPRESSION (Line 31) [Severity: Minor] [Priority: P3] [Script]: Weak-expression candidate
% Original: Make sure the model converges.
% Candidate: weak verb "make" is context-dependent ("make sure", "make use of"); not auto-applied
% Changed:       none (candidate only: Make)
% Protected:     none
% Meaning-Check: NEEDS-LLM
% Risk-Flags:    not-assessed
```

本模块产出可直接替换原文的文本，适用改写契约。`[Script]` 层输出恒为 `Meaning-Check: NEEDS-LLM`，且只允许置规则可确定的标记（`none`、`not-assessed`、`lexical-substitution`、`whitespace-normalized`）；只有 `[LLM]` 层可提出 `PRESERVED`。字段定义与 `Risk-Flags` 闭集见 `references/modules/routing-rules.md`。

润色时不得升高措辞强度。把留有余地的报告换成更强的断言（`suggests` -> `demonstrates`、`may` -> `does`）是过度声称，不是语气改善：保持原强度，或置 `Risk-Flags: overstatement` 并明确说明。判据见 [over-claim-guard.md](../evidence/over-claim-guard.md)；报告动词四级阶梯见 [style-guide.md](../writing/style-guide.md)。

风格指南：[style-guide.md](../writing/style-guide.md)
