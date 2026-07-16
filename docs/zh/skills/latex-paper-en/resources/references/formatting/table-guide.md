# 三行表格指南

本指南使用“三行”（书签）约定定义了专业学术表格的标准。所有与表相关的检查和生成都遵循这些规则。

## 三行表标准

三行表格恰好有三个水平线并且**没有垂直线**：

1. **顶部规则** (`\toprule`)：列标题上方
2. **中间规则** (`\midrule`)：列标题下方，数据行上方
3. **底部规则** (`\bottomrule`)：最后一个数据行下方

### 反模式（必须标记）

- 垂直线（`|`在列规格中，`\vline`, `\hline`和`|`)
- 内部水平线（`\hline`或者`\cline`数据行之间，分组子标题除外）
- 使用 `\hline` 代替 booktabs 命令
- 序言中缺少 `\usepackage{booktabs}`

### 最小正确示例

```latex
\begin{table}[t]
  \caption{Comparison of model accuracy (\%).}
  \label{tab:accuracy}
  \centering
  \begin{tabular}{lSSS}
    \toprule
    Model & {Precision} & {Recall} & {F1} \\
    \midrule
    Baseline   & 85.3 & 82.1 & 83.7 \\
    Ours       & \textbf{91.2} & \textbf{89.5} & \textbf{90.3} \\
    \bottomrule
  \end{tabular}
\end{table}
```

## 小数点对齐

使用`siunitx`包裹`S`按小数点对齐数字的列类型：

```latex
\usepackage{siunitx}
\sisetup{detect-weight, mode=text}
% Column spec: {l S[table-format=2.1] S[table-format=2.1]}
% Wrap non-numeric headers in braces: {Precision}
```

什么时候`siunitx`不可用，将数字列右对齐`r`并手动确保小数点位置一致。

## 统计显着性标记

在表注中使用带有脚注定义的上标符号：

|象征|意义|
|--------|---------|
| `*`    |p < 0.05|
| `**`   |p < 0.01|
| `***`  |p < 0.001|
| `n.s.` |不重要|

将显着性标记放置在值之后：`91.2***`。

## 数字精度规则

|数据类型|精确|例子|
|-----------|-----------|---------|
|百分比|小数点后 1 位| 85.3% |
|平均值±标准差|2 位小数| 3.14 ± 0.05 |
|p 值|3 位有效数字| 0.0032 |
|相关系数|2-3 位小数| 0.87 |
|大计数|无小数| 1,024 |

每列内的精度必须一致。同一列中的混合精度是一个警告。

## 标题和注释的位置

- **标题**：表格上方（`\caption{...}`前`\begin{tabular}`)
- **标签**：紧接在标题之后 (`\label{tab:...}`)
- **表注**：位于表下方，以“注”开头。 （英文）或“注：”（中文）

表注格式：

```latex
\begin{tablenotes}
  \small
  \item Note. Bold values indicate best performance.
  \item * $p < 0.05$; ** $p < 0.01$; *** $p < 0.001$.
\end{tablenotes}
```

或者使用`\par\vspace{2pt}{\footnotesize Note. ...}`后`\end{tabular}`如果`threeparttable`未加载。

## 大胆的最佳价值

在比较表中，使用粗体显示每列中的最佳值`\textbf{}`。使用时`siunitx`S 柱，使用`\bfseries`或包裹在`{\textbf{91.2}}`.

当“最佳”方向不明确时添加方向指示器：

- `↑`（越高越好）：准确率、召回率、F1
- `↓`（越低越好）：错误率、延迟、丢失

## Booktabs 包要求

这`booktabs`必须加载包`\toprule`, `\midrule`, `\bottomrule`。这些命令生成可变权重规则（顶部/底部比中间重）以实现专业外观。

切勿将 `\hline` 与同一表中的 booktabs 命令混合使用。

## 单词兼容性注意事项

当提交到需要 .docx 的场所时，请通过以下方式转换三行表格：
1. 在Word中创建标准表格
2. 选择整个表格→边框→无边框
3. 将顶部边框添加到第一行，将底部边框添加到标题行，将底部边框添加到最后一行
4. 结果：符合书页美感的三行表格
