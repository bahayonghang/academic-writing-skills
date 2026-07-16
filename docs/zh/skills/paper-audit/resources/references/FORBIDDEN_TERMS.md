# FORBIDDEN_TERMS.md

未经用户明确确认，**不得修改**的受保护术语和结构。
这些规则适用于所有审核模式（`quick-audit`, `deep-review`, `gate`, `polish`和兼容性别名）。

---

## 1. LaTeX命令保护列表

以下 LaTeX 命令**永远**不得更改内容、拼写或结构：

|命令|原因|例子|
|---------|--------|---------|
| `\cite{key}` |参考书目——改变关键引用| `\cite{lecun1998}` |
| `\citep{key}` |附加引用| `\citep{vaswani2017}` |
| `\citet{key}` |文字引用| `\citet{hinton2006}` |
| `\ref{label}` |交叉引用——更改中断链接| `\ref{fig:arch}` |
| `\eqref{label}` |方程参考| `\eqref{eq:loss}` |
| `\autoref{label}` |自动输入参考| `\autoref{tab:results}` |
| `\cref{label}` |聪明参考| `\cref{fig:overview}` |
| `\Cref{label}` |smartef 大写参考| `\Cref{tab:ablation}` |
| `\pageref{label}` |页面参考| `\pageref{sec:method}` |
| `\hyperref[label]{text}` |超链接参考| `\hyperref[sec:exp]{Section 3}` |
| `\label{key}` |标签定义——更改会破坏所有引用| `\label{fig:arch}` |
| `\bibliography{file}` |参考书目文件参考| `\bibliography{references}` |
| `\bibliographystyle{style}` |参考书目风格| `\bibliographystyle{plain}` |
| `\input{file}` |文件包含| `\input{sections/intro}` |
| `\include{file}` |带分页符的文件包含| `\include{chapter1}` |

---

## 2. Typst 命令保护列表

|命令|原因|例子|
|---------|--------|---------|
| `@key` |参考书目引用| `@lecun1998` |
| `#cite(<key>)` |引文功能| `#cite(<vaswani2017>)` |
| `#ref(<label>)` |交叉引用| `#ref(<fig:arch>)` |
| `<label>` |标签定义| `<fig:overview>` |
| `#include "file"` |文件包含| `#include "sections/intro.typ"` |
| `#bibliography("file")` |参考书目文件| `#bibliography("refs.bib")` |

---

## 3. 数学环境保护清单

这些环境包含数学内容 - **永远不要**修改其中的 LaTeX/Typst 代码：

### LaTeX 数学环境
- `$...$`— 内联数学
- `$$...$$`— 显示数学（已弃用但受保护）
- `\(...\)`— 内联数学（首选）
- `\[...\]`— 显示数学（首选）
- `\begin{equation}...\end{equation}`
- `\begin{equation*}...\end{equation*}`
- `\begin{align}...\end{align}`
- `\begin{align*}...\end{align*}`
- `\begin{aligned}...\end{aligned}`
- `\begin{gather}...\end{gather}`
- `\begin{gather*}...\end{gather*}`
- `\begin{multline}...\end{multline}`
- `\begin{cases}...\end{cases}`
- `\begin{array}...\end{array}`
- `\begin{matrix}...\end{matrix}`（以及变体：pmatrix、bmatrix、vmatrix）

### Typst 数学环境
- `$...$`— 内联数学
- `$ ... $`— 显示数学（带空格）

### 为什么受到保护
数学表达式可能包含特定于域的符号。修改符号、运算符或
索引可以默默地改变数学含义，而不会出现语法错误。

---

## 4. 领域术语冻结列表

这些术语经常出现在学术写作中，但具有**精确的技术含义**。
未经用户确认，**不要**建议同义词或重写：

### 计算机科学/机器学习
- **梯度下降**（不是“斜率下降”或“导数最小化”）
- **反向传播**（不是“反向传播算法”）
- **注意力机制** / **自注意力** / **交叉注意力**
- **变压器**（架构，在提及架构时以“Transformer”大写）
- **困惑**（NLP 指标 — 不是“混乱”或“不确定性”）
- **过度拟合** / **欠拟合** / **泛化差距**
- **超参数**（不是 ML 上下文中的“元参数”或“配置参数”）
- **微调** / **预训练** / **迁移学习**
- **标记化** / **标记化器** / **子词标记化**
- **嵌入**（矢量表示——不是可互换的“编码”）
- **批量标准化** / **层标准化** / **实例标准化**
- **dropout**（正则化技术）
- **交叉熵损失** / **KL散度** / **ELBO**
- **精确度** / **召回率** / **F1 分数**（分类指标 - 非同义词）
- **BLEU** / **ROUGE** / **METEOR**（评估指标 - 不可互换）

### 数学/统计学
- **凸面** / **凹面**（不可互换）
- **双射** / **单射** / **满射** （不可互换）
- **随机**（并非在所有情况下都与“随机”同义）
- **期望** / **方差** / **协方差**（统计术语）
- **原假设** / **p值** / **统计显着性**
- **蒙特卡洛**（专有名词 - 始终大写）

### 一般学术术语
- **消融研究**（不是“成分分析”或“去除实验”）
- **最先进** / **SOTA**（没有上下文就不是“最佳表现”）
- **基线**（比较参考 - 与“默认”不是同义词）
- **基准**（标准化评估——与“测试”不是同义词）
- **语料库** / **语料库**（语言数据集 - 不是所有上下文中的“数据集”）

---

## 5. 工具使用规则

当审计模块遇到以上任一情况时：

1. **跳过**：不要将受保护的构造标记为问题。
2. **仅上下文**：可以分析周围的文本，但受保护的术语/命令本身是禁止的。
3. **确认**：如果确实需要更改受保护的术语（例如，损坏的`\ref`没有匹配的`\label`），将其报告为**问题**，但**不**自动修复。
4. **报告**：参考完整性问题（`\ref`没有`\label`）应通过报告`check_references.py`，不默默纠正。

---

## 6. 审计模块合规性

|模块|必须跳过|必须报告|
|--------|-----------|-------------|
| `analyze_grammar.py` |所有数学环境，所有`\cite`, `\ref`, `\label` |没有任何|
| `analyze_logic.py` |数学环境、引文内容|仅结构逻辑问题|
| `analyze_sentences.py` |所有数学环境|散文中的句子级问题|
| `deai_check.py` |数学环境、引用键|人工智能在散文中生成的模式|
| `check_format.py` |数学环境、引文|元数据格式违规|
| `check_references.py` |没什么（这是记者）|所有损坏/丢失的参考文献|
| `verify_bib.py` |没什么（这是记者）|所有号码布完整性问题|
| `visual_check.py` |所有文字内容|仅布局/视觉问题|

---

*最后更新：2026-02-27*
