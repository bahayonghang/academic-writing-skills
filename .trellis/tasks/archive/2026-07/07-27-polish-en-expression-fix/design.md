# Design: EN + Typst 表达链路修复（C2）

## 落点与边界

- 改：EN `scripts/{improve_expression,analyze_grammar,analyze_sentences,translate_academic}.py`
  + EN `references/modules/{expression,grammar,sentences,translation}.md`
  + Typst 对应四脚本与四模块文档 + 保护 token 单点清单。
- **不改**：`deai_check.py`、`analyze_abstract.py`、`parsers.py`、任何 ZH 文件。

## 一、自动化分级（本设计的核心）

参照 skill 只给**原则**不给识别方法。把原则直接实现成"脚本自动识别并跳过全部类别"是不可能
的。每条规则/每类 token 必须落到三档之一：

| 档 | 标记          | 含义                                     | 输出行为                          |
| -- | ------------- | ---------------------------------------- | --------------------------------- |
| A  | `auto`        | 判定确定，可自动改写                     | 出 `Original/Revised` + 契约字段   |
| B  | `candidate`   | 模式可检出，但正误依赖上下文             | **只报告**，不给替换文本；`Risk-Flags: not-assessed` |
| C  | `llm-only`    | 规则无法可靠判定                         | 脚本不处理，仅由模块文档指导 LLM   |

### 1.1 替换规则分级（`improve_expression.py`）

| 规则                   | 档 | 理由与处置                                                                 |
| ---------------------- | -- | -------------------------------------------------------------------------- |
| `\bget\b → obtain`     | A  | 实测 `We get 92.1% accuracy` → `We obtain ...` 正确；需补保大小写           |
| `\bmake\b → develop`   | **B** | 实测 `Make sure`/`make use of` 均被改坏。降级为只报告候选，不自动替换 |
| `\bvery\b → highly`    | **B** | 实测 `very few` → `highly few` 错误。降级为候选                        |
| `\ba lot of\b → many`  | A  | 无已知反例                                                                  |
| `\bkind of\b → ""`     | **B** | 删除类改写语义风险高（`a kind of transformer` 是合法用法），降级候选  |

**降级而非加排除表**的理由：搭配排除表是开放集（`make sense` / `make up` / `make do` /
`make it` …），穷举必漏，漏了就产出错误英文。只报告候选把判断交给 LLM，成本低且不会写坏。
`--strength restructure` 下**仍不**自动应用 B 档——幅度控制的是改动层级，不是正确性豁免。

### 1.2 保护 token 分级（P2-1）

| 类别                                   | 档 | 检出方式                                             |
| -------------------------------------- | -- | ---------------------------------------------------- |
| 数值 + 单位 / 统计值（`p < 0.05`、`92.1%`、`3.2 GB`） | A | 数字模式，检出确定，直接跳过并记入 `Protected` |
| 含数字或连字符的标识符（`ResNet-50`、`CIFAR-100`、`BERT-base`、`GPT-4`） | A | 形态模式（含数字/连字符的大小写混合 token），检出确定 |
| 全大写缩写（`SOTA`、`GPU`、`TP53`）    | A  | 形态模式；副作用是保护了基因名的常见形态              |
| 一般模型名/数据集名（`Transformer`、`ImageNet`） | B | 无法与普通名词可靠区分，只报告"疑似专有名词，已跳过替换" |
| 基因/蛋白名的非全大写形态（`p53`、`Shh`）、化学名 | **C** | 规则不可判定。**不实现检出**，只在模块文档写入 LLM 指导 |

**明确不做的**：不引入基因/化学名词典（维护成本与误报都不可控，且非本仓职责）。C 档在文档层
解决——这正是参照 skill 的做法。

清单单点定义在 `latex-paper-en/references/writing/protected-tokens.md`（新建），Typst 侧建
`references/PROTECTED_TOKENS.md` 并**指向同一套规则**；SKILL.md 与模块文档只做指针。

### 1.3 其余脚本

- `analyze_grammar.py`：现有规则表逐条走上表分级；`grammar.md:19-22` 示例暴露的大小写损坏按
  A 档修复（保大小写）。
- `analyze_sentences.py`：本身就是 B 档性质（`Suggested:` 是建议不是断言），只需补契约字段。
- `translate_academic.py`：翻译整体是 C 档（脚本只出草稿 + 术语表 + `[PENDING CONFIRMATION]`
  提示），契约字段按 §2.2 嵌入。

## 二、契约字段落地

### 2.1 注释流三脚本（expression / grammar / sentences）

```latex
% EXPRESSION (Line 23) [Severity: Minor] [Priority: P2] [Script]: Improve academic tone
% Original: We get 92.1% accuracy on CIFAR-100.
% Revised:  We obtain 92.1% accuracy on CIFAR-100.
% Rationale: Weak verb replaced: get -> obtain
% Changed: 1 lexical substitution (get -> obtain)
% Protected: 92.1%, CIFAR-100
% Meaning-Check: NEEDS-LLM
% Risk-Flags: lexical-substitution
```

B 档候选（无 `Revised:`）：

```latex
% EXPRESSION (Line 31) [Severity: Minor] [Priority: P3] [Script]: Weak-verb candidate
% Original: Make sure the model converges.
% Candidate: "make" may be replaceable; context-dependent — not auto-applied
% Changed: none
% Protected: none
% Meaning-Check: NEEDS-LLM
% Risk-Flags: not-assessed
```

`analyze_sentences.py` 保留其 `Suggested:` 字段名不变（PRD Out of Scope），只追加四字段。

### 2.2 Markdown 报告（translate_academic）

在既有 `### Notes` 之后追加一个 `### Contract` 小节，用同名四字段，值语义一致：

```markdown
### Contract
- Changed: draft translation produced from rule-based glossary
- Protected: (none detected)
- Meaning-Check: NEEDS-LLM
- Risk-Flags: not-assessed
```

字段名与注释流**逐字一致**，便于 C1 的契约测试用同一组断言覆盖两种形态。

## 三、Typst 镜像策略

| 文件                                       | 策略                                      |
| ------------------------------------------ | ----------------------------------------- |
| `improve_expression.py` / `analyze_grammar.py` / `analyze_sentences.py` | **整文件逐字节镜像**（TIER1 锁），EN 为 canonical，同 commit 落地 |
| `translate_academic.py`                    | 不在锁内，按 Typst 自身形态独立实现，不强行统一 |
| `references/modules/EXPRESSION.md` 等       | 独立修复（修表 + 修示例 + 修坏链），不与 EN 强制一致（语言与注释符不同） |

镜像操作用整文件复制，**不做人工逐段同步**——spec 明写按成员级镜像会漏空白/顺序差异导致锁红。

## 四、文件改动面

| 文件                                                              | 改动          |
| ----------------------------------------------------------------- | ------------- |
| EN `scripts/improve_expression.py`                                 | 规则分级 + 保大小写 + 不压空白 + 契约字段 + 两 flag |
| EN `scripts/analyze_grammar.py`                                    | 保大小写 + 契约字段 + 两 flag |
| EN `scripts/analyze_sentences.py`                                  | 契约字段 + 两 flag |
| EN `scripts/translate_academic.py`                                 | `### Contract` 小节 |
| EN `references/modules/{expression,grammar,sentences,translation}.md` | 替换表对齐 + E15 说明 + over-claim 指针（C1 供文案）+ 输出示例 |
| EN `references/writing/protected-tokens.md`                        | **新建**，单点清单 |
| Typst `scripts/`（3 个）                                            | 逐字节镜像     |
| Typst `scripts/translate_academic.py`                              | 独立实现       |
| Typst `references/modules/{EXPRESSION,GRAMMAR,SENTENCES,TRANSLATION}.md` | 修表/示例/坏链 + 契约示例 |
| Typst `references/PROTECTED_TOKENS.md`                             | **新建**       |
| `tests/skills/...`                                                 | 反例回归测试   |

## 兼容性

- B 档降级使 `improve_expression` 的自动替换数量**下降**——属"误报修复"类默认行为变化，须按
  spec 在 commit message 双声明，并同 commit 更新受影响的存量用例。
- 契约字段为追加，既有首行格式不变。
- `analyze_sentences.py` 的 `Suggested:` 保持不变，无下游影响。

## Validation Shape

```bash
# 字节锁必须最先确认
uv run --extra dev python -m pytest tests/contracts/test_writing_modules_alignment.py -q

# 反例回归
uv run --extra dev python -m pytest tests/skills/ -k "expression or grammar or sentences" -q

# 确认未越权
git diff --stat -- '*/scripts/deai_check.py' '*/scripts/analyze_abstract.py' '*/scripts/parsers.py'

just ci
```
