# 写作规范

学术论文写作的风格指南。

## 学术语气

### 正式性

```latex
% 避免
a lot of, kind of, stuff, things
really, very, pretty much

% 使用
numerous, substantial, considerable
significantly, substantially
```

### 客观性

```latex
% 避免主观评价
amazing, terrible, exciting, perfect

% 使用客观描述
effective, efficient, accurate, significant
```

### 谨慎性

```latex
% 避免绝对化
always, never, all, none

% 使用限定词
generally, typically, often, usually
in most cases, under certain conditions
```

## 简洁性

### 删除冗余

```latex
% 冗余
in order to → to
due to the fact that → because
at the present time → now
in the event that → if
```

### 避免重复

```latex
% 冗余
completely eliminate → eliminate
future plans → plans
basic fundamentals → fundamentals
```

## 主动与被动语态

### 何时使用主动语态

- 描述贡献
- 强调行动者

```latex
We propose a novel method...
Our approach achieves state-of-the-art performance...
```

### 何时使用被动语态

- 强调动作或结果
- 方法描述
- 实验设置

```latex
The model was trained on...
The experiments were conducted using...
The results are summarized in Table 1.
```

## 段落结构

### 主题句

每段以主题句开头，概括段落内容。

```latex
% 好的段落结构
Deep learning has revolutionized natural language processing.
[支持句1] Neural networks can learn complex patterns...
[支持句2] Pre-trained models like BERT have achieved...
[总结句] These advances have enabled numerous applications.
```

### 过渡词

| 关系 | 过渡词 |
|------|--------|
| 添加 | Furthermore, Moreover, Additionally, In addition |
| 对比 | However, In contrast, On the other hand, Unlike |
| 因果 | Therefore, Thus, Consequently, As a result |
| 举例 | For example, For instance, Specifically |
| 总结 | In summary, Overall, In conclusion |

## 各章节写作

### 摘要

**结构**：背景 → 问题 → 方法 → 结果 → 结论

**长度**：150-250 词（根据要求）

```latex
% 模板
[Background] ... remains a challenging problem.
[Problem] Existing methods suffer from...
[Method] In this paper, we propose...
[Results] Experimental results demonstrate that...
[Conclusion] Our approach achieves state-of-the-art performance.
```

### 引言

**结构**：背景 → 问题 → 现有方法局限 → 贡献 → 组织

**贡献陈述**：
```latex
The main contributions of this paper are summarized as follows:
\begin{itemize}
  \item We propose a novel ... for ...
  \item We design a ... mechanism to address ...
  \item Extensive experiments demonstrate that ...
\end{itemize}
```

### 相关工作

**组织方式**：
- 按主题分组
- 按时间顺序
- 按方法类型

**过渡**：
```latex
% 同类工作
Similarly, [Author] proposed...
Along this line, [Author] introduced...

% 对比
However, unlike our approach, [Author]'s method...
In contrast to previous work, we...
```

### 方法

**结构**：
- 问题定义
- 方法概述
- 各组件详细描述
- 算法/流程

**公式描述**：
```latex
where $x$ denotes the input, $W$ represents the weight matrix,
and $b$ is the bias term.
```

### 实验

**结构**：
- 数据集
- 基准方法
- 实现细节
- 主要结果
- 消融实验
- 分析讨论

**结果描述**：
```latex
% 比较
Our method outperforms the baseline by 5.2\% in accuracy.
Compared with [Method], our approach achieves 3.1\% improvement.

% 分析
The performance gain can be attributed to...
This improvement is due to...
```

### 结论

**结构**：总结 → 主要发现 → 局限性 → 未来工作

```latex
In this paper, we proposed ... for ...
Experimental results demonstrated that ...
In future work, we plan to extend ...
```

## 数学写作

### 符号一致性

- 全文使用一致的符号
- 首次使用时定义
- 使用标准符号

### 公式格式

```latex
% 行内公式
The loss function $L$ is defined as...

% 独立公式
\begin{equation}
  L = \frac{1}{N} \sum_{i=1}^{N} \ell(y_i, \hat{y}_i)
  \label{eq:loss}
\end{equation}
```

### 公式引用

```latex
As shown in Eq.~(\ref{eq:loss})...
According to Equation~(\ref{eq:loss})...
```

## 图表

### 图片

- 标题在下方
- 清晰可读
- 矢量图优先

```latex
\begin{figure}[t]
  \centering
  \includegraphics[width=\linewidth]{figure.pdf}
  \caption{Description of the figure.}
  \label{fig:example}
\end{figure}
```

### 表格

- 标题在上方
- 使用三线表
- 对齐数字

```latex
\begin{table}[t]
  \caption{Comparison of methods.}
  \label{tab:results}
  \centering
  \begin{tabular}{lcc}
    \toprule
    Method & Accuracy & F1 \\
    \midrule
    Baseline & 85.2 & 84.1 \\
    Ours & \textbf{90.5} & \textbf{89.3} \\
    \bottomrule
  \end{tabular}
\end{table}
```

## 下一步

- [常见错误](/zh/references/common-errors)
- [期刊会议](/zh/references/venues)
