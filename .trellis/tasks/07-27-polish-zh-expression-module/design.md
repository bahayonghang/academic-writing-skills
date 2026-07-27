# Design: ZH expression 模块（C3）

## 落点与边界

- 新增：`scripts/check_style_zh.py`、`references/modules/expression.md`、
  `references/formatting/number-unit-guide-zh.md`。
- 改：`SKILL.md`（路由表 + Reference Map + 路由规则）、`references/modules/routing-rules.md`、
  `evals/trigger_eval.json`。
- **不改**：`deai_check.py`、`analyze_abstract.py`、`check_spec.py`、`parsers.py`、
  任何 EN / Typst 文件。

## 一、与现有检查的关系（零重叠是硬要求）

| 领域           | Owner                              | `expression` 的处置                      |
| -------------- | ---------------------------------- | ---------------------------------------- |
| 人称（我们/本文）| `abstract` 的 T-VOICE / T-OPEN     | **不实现**，文档指路                      |
| 论断强度分级   | `references/writing/over-claim-guard.md` | 只做词汇层替换建议，强度分级不重复实现 |
| 数字用法（模板专属）| `spec-check` YS-36（`llm` 判定） | 只做通用可判定项，双向指路                |
| 句长均匀度（AI 痕迹）| `deai` D1（`--tier` 门控，CV）   | 只做单句可读性长度，语义区分写入文档      |
| 段落顺序 / 论证 | `logic`                            | 不触碰                                    |
| 结论/摘要章骨架 | `conclusion` / `abstract`          | 不触碰                                    |

## 二、逐检查器契约

档位定义同 C2：**A=auto**（判定确定，可给替换）/ **B=candidate**（只报候选，不给替换文本）/
**C=llm-only**（脚本不实现，文档指导）。

| ID           | 来源                      | 输入区域                       | 排除条件                                                                 | 档 | 误报预算 |
| ------------ | ------------------------- | ------------------------------ | ------------------------------------------------------------------------ | -- | -------- |
| `E-COLLOQ`   | style-zh §1.1/§1.3 口语化 | 可见中文正文                   | 引文块、`\texttt`、代码环境；术语表中已登记的词                           | A  | 0（闭集词表） |
| `E-ABSOLUTE` | style-zh §2 绝对化词汇    | 可见中文正文                   | 引用他人观点的语境（`文献[N]认为…`）；数学环境                            | B  | 低 |
| `E-COLLOC`   | style-zh §4.1 搭配不当    | 可见中文正文                   | 无                                                                        | A  | 0（闭集错误搭配对） |
| `E-INCOMP`   | style-zh §4.2 成分残缺    | 以「通过/经过/利用」开头的句子 | 上一句已有明确主语且本句为承接分句；中文允许的承前省略                    | **B** | 中——中文 pro-drop 普遍，**必须只报候选** |
| `E-PUNCT`    | style-zh §5.3 标点混用    | 中文语境句（含中文字符的行）   | 行内英文片段内部（§5.2 允许）；括号内全英文（§5.3 明确允许）；数学环境；`\url`/`\path`/文件名 | **B** | 中——排除区判定本身有边界情况 |
| `E-NUMSPACE` | style-zh §6.2 数值与单位  | 可见正文中的「数字+单位」形态  | 百分号、角度、摄氏度等按国标不空格的情形；数学环境内                      | A  | 低 |
| `E-UNITFONT` | style-zh §6.2 单位正体    | **数学环境内**（只读）         | —                                                                        | **B（永不 fix）** | 低——见 §3 红线 |
| `E-NUMSTYLE` | style-zh §6.1 概数/序数   | 可见中文正文                   | 图表编号、公式编号、章节号、参考文献编号                                  | B  | 中 |
| `E-LONGSENT` | 可读性                    | 可见中文正文，按中文标点断句   | 公式行、表格行、列举项；`deai` D1 已报的同一句不重复                       | B  | 低 |

**分级理由（关键几条）**：

- `E-INCOMP` 降 B：中文承前省略主语是合法的（"本文提出 X 方法。通过实验，验证了其有效性。"
  第二句省略「本文」在学位论文中普遍且可接受）。规则只能识别句式模式，无法判定是否真缺主语。
- `E-PUNCT` 降 B：`academic-style-zh.md` §5.2/§5.3 自身就给了两条**允许英文标点**的例外（英文
  术语后、括号内全英文）。排除区可实现，但边界情况（中英混排的复合括号）无法穷举。
- `E-UNITFONT` 特殊：见 §3。

## 三、单位正斜体与数学环境红线

`academic-style-zh.md:136` 要求单位用正体。LaTeX 中该问题位于数学环境内（`$3.2 kg$` 里的 `kg`
默认斜体，须写 `$3.2\,\mathrm{kg}$`）。而**红线一：绝不修改数学环境**。

处置：`E-UNITFONT` **只读数学环境、只报告、永不给替换文本**，且输出必须显式说明"位于数学环境
内，需作者手动调整"。这是本设计中唯一一个"检出确定但仍不能 auto"的检查器——**分档依据是红线
而非判定能力**，实现时不要误当成可以升 A 档。

## 四、输出形态

```latex
% EXPRESSION (chapters/chap03.tex:42) [Severity: Minor] [Priority: P2] [Script]: E-COLLOC 搭配不当
% 原文: 该策略有效增加了模型的效率。
% 建议: 该策略有效提高了模型的效率。
% 依据: academic-style-zh.md §4.1（增加效率 → 提高效率）
% Changed: 1 collocation fix (增加效率 -> 提高效率)
% Protected: none
% Meaning-Check: NEEDS-LLM
% Risk-Flags: lexical-substitution
```

B 档（无「建议」行）：

```latex
% EXPRESSION (chapters/chap03.tex:57) [Severity: Info] [Priority: P3] [Script]: E-INCOMP 疑似成分残缺
% 原文: 通过对比实验，验证了所提方法的有效性。
% 候选: 「通过…，<动词>了…」句式疑似缺主语；中文承前省略亦合法，请人工判断
% Changed: none
% Protected: none
% Meaning-Check: NEEDS-LLM
% Risk-Flags: not-assessed
```

字段名（`Changed` / `Protected` / `Meaning-Check` / `Risk-Flags`）与 EN/Typst **逐字一致**，
中文只出现在说明文本里——与仓库既有做法一致（`check_spec.py` 状态值是英文 `NEEDS-LLM`，
evidence 是中文）。

## 五、新增/复用符号

- 新建 `check_style_zh.py`：常量 `COLLOQ_MAP`、`ABSOLUTE_TERMS`、`COLLOC_ERRORS`、
  `INCOMP_PATTERNS`、`UNIT_NO_SPACE`、`APPROX_NUM_CHARS`。
- 复用：`parsers.py` 的 `get_parser` / `extract_visible_text` / `resolve_section_keys`；
  `tex_loader.assemble` 与 `doc.lineref`（多文件定位）。**只消费不修改**。
- 不复用 `deai_check.py` 的任何断句逻辑——避免与 D1 形成隐式耦合；中文断句在本脚本内独立实现。

## 六、文件改动面

| 文件                                              | 改动                                           |
| ------------------------------------------------- | ---------------------------------------------- |
| `scripts/check_style_zh.py`                        | 新建，9 个检查器                                |
| `references/modules/expression.md`                 | 新建；指向 style-zh；含 §1 边界表与 over-claim 指针（C1 供文案） |
| `references/formatting/number-unit-guide-zh.md`    | 新建；GB/T 15834 / GB/T 15835 / GB 3100 系列；模板优先级声明 |
| `SKILL.md`                                         | 路由表 +1 行；Reference Map + `academic-style-zh.md` 与新参考；路由规则序列 |
| `references/modules/routing-rules.md`              | `expression` 判据 + 五条边界                    |
| `evals/trigger_eval.json`                          | 新增触发用例（Bash python 写入）                |
| `tests/skills/latex_thesis_zh/test_check_style_zh.py` | 新建，每检查器正反例                        |

`last_updated` 更新，`version` 不动。

## 七、标准优先级（写进 number-unit-guide-zh.md）

学校模板规范 **>** 通用国标。冲突时以 `templates/<template>.md` 快照为准（模板快照是本仓模板
事实的唯一权威源）。已知引用点：`templates/yanshan.md:13`（GB 3100 / GB/T 3101 / GB/T 3102 /
GB/T 15835）、`:62`（数字按 GB/T 15835）、`:151`（YS-36）。

## 兼容性

- 全部为新增文件 + SKILL.md 增行，无既有检查器行为变化，不触发"默认行为变化须双声明"条款。
- 新脚本不进 `TIER1_HASH_GROUPS`（ZH 专属，无对齐副本）——实现时**不要**顺手加进去。

## Validation Shape

```bash
uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/test_check_style_zh.py -q
uv run --extra dev python -m pytest tests/contracts/ -q       # ROUTER_ROW_RE + 契约字段
git diff --stat -- '*/latex-paper-en/' '*/typst-paper/'       # 期望空
git diff --stat -- '*/scripts/deai_check.py' '*/scripts/analyze_abstract.py' '*/scripts/check_spec.py'  # 期望空
just ci
```
