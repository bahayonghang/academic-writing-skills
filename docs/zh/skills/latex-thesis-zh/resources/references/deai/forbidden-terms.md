# 受保护术语 - 禁止修改

未经明确许可，绝不能修改以下术语。

## 技术术语（保持原样）

### 机器学习
- Transformer、BERT、GPT、ResNet、VGG
- Attention mechanism、Self-attention
- Backpropagation、Gradient descent
- Batch normalization、Layer normalization
- Dropout、Regularization

### 数学
- 变量：x、y、z、θ、α、β、γ
- 集合：ℝ、ℕ、ℤ
- 运算：∑、∏、∫、∂
- 关系：∈、⊂、∀、∃

### 领域专用内容
- 用户定义的技术术语
- 算法名称
- 数据集名称
- 基准名称

## LaTeX 环境 - 禁止解析

```latex
% Never modify content inside these:
\begin{equation} ... \end{equation}
\begin{align} ... \end{align}
\begin{gather} ... \end{gather}
$...$ (inline math)
\[...\] (display math)
```

## 引用命令 - 禁止修改

```latex
\cite{key}
\citep{key}
\citet{key}
\parencite{key}
\textcite{key}
\ref{label}
\eqref{label}
\label{label}
```

## 算法内容

```latex
\begin{algorithm}
\begin{algorithmic}
% All content here is protected
\end{algorithmic}
\end{algorithm}
```

## 代码清单

```latex
\begin{lstlisting}
% Code is protected
\end{lstlisting}

\begin{verbatim}
% Verbatim content is protected
\end{verbatim}
```

## 用户定义的受保护术语

在此添加项目专用术语：
- [添加受保护术语]
- [每行一个]
