# 常见错误

学术写作中的常见错误及修正方法。

## 中式英语（Chinglish）

### 冗余表达

| ❌ 中式英语 | ✅ 学术英语 |
|-------------|-------------|
| in recent years | recently |
| more and more | increasingly |
| play an important role in | is crucial for |
| make a contribution to | contribute to |
| have a great influence on | significantly affect |
| in order to | to |
| due to the fact that | because |
| a large number of | many / numerous |
| in the field of | in |

### 弱动词替换

| ❌ 弱动词 | ✅ 强动词 |
|----------|----------|
| use | employ, utilize, leverage |
| get | obtain, achieve, acquire |
| make | construct, develop, generate |
| do | perform, conduct, execute |
| show | demonstrate, illustrate, indicate |
| give | provide, offer, present |
| have | possess, exhibit, contain |

### 结构改进

| ❌ 中文结构 | ✅ 英文结构 |
|-------------|-------------|
| 本文提出了一种... | We propose... |
| 首先...然后...最后... | First,... Subsequently,... Finally,... |
| 通过...实现了... | ... is achieved by/through... |
| 与...相比，...更好 | Compared with..., ... outperforms... |
| 实验结果表明... | Experimental results demonstrate that... |

## 冠词使用

### 何时使用 "the"

- 特指已提及的事物
- 唯一的事物
- 最高级前

```latex
% 正确
The proposed method achieves the best performance.
The results in Table 1 show...
```

### 何时使用 "a/an"

- 首次提及
- 泛指

```latex
% 正确
We propose a novel method for...
An important observation is that...
```

### 何时不用冠词

- 复数泛指
- 不可数名词泛指

```latex
% 正确
Neural networks have been widely used.
Deep learning has achieved great success.
```

## 时态使用

### 各章节时态

| 章节 | 时态 | 示例 |
|------|------|------|
| 摘要-背景 | 现在时 | ... is an important task |
| 摘要-方法 | 现在时 | We propose... |
| 摘要-结果 | 过去时 | achieved, obtained |
| 引言-背景 | 现在时 | ... has attracted attention |
| 相关工作-一般 | 现在完成时 | have been proposed |
| 相关工作-具体 | 过去时 | proposed, introduced |
| 方法 | 现在时 | consists of, computes |
| 实验-设置 | 过去时 | was conducted |
| 实验-结果 | 现在时 | shows, demonstrates |
| 结论-总结 | 过去时 | proposed, presented |
| 结论-未来 | 将来时 | will explore |

## 标点符号

### 逗号

```latex
% 错误：缺少逗号
We propose a method which achieves good results.

% 正确：非限制性从句前加逗号
We propose a method, which achieves good results.
```

### 分号

```latex
% 用于连接相关的独立句子
The method is efficient; however, it has limitations.
```

### 冒号

```latex
% 用于引出列表或解释
The contributions are as follows: (1)..., (2)..., (3)...
```

## 数字表达

### 何时拼写

- 句首的数字
- 1-10 的数字（部分风格）

```latex
% 正确
Ten experiments were conducted.
We use 100 samples for training.
```

### 单位

```latex
% 正确：数字和单位之间有空格
The accuracy is 95.2\%.
The model has 1.5 million parameters.
```

## 参考文献引用

### 引用位置

```latex
% 错误：引用前无空格
word\cite{key}

% 正确
word \cite{key}
word~\cite{key}  % 不换行空格
```

### 多引用

```latex
% 正确
Previous work \cite{key1,key2,key3} has shown...
```

## 图表引用

### 一致性

```latex
% IEEE 风格
See Fig.~1 for details.
As shown in Fig.~2...

% ACM 风格
See Figure~1 for details.
As shown in Figure~2...
```

### 位置

```latex
% 正确：引用在句中
As shown in Fig.~1, the method achieves...

% 避免：引用作为句子主语
Fig.~1 shows the results.  % 可接受但不推荐
The results are shown in Fig.~1.  % 更好
```

## 公式

### 标点

```latex
% 公式是句子的一部分，需要标点
The loss function is defined as
\begin{equation}
  L = \sum_{i=1}^{n} (y_i - \hat{y}_i)^2.
\end{equation}
```

### 引用

```latex
% 正确
As shown in Eq.~(\ref{eq:loss})...
According to Equation~(\ref{eq:loss})...
```

## 下一步

- [写作规范](/zh/references/style-guide)
- [期刊会议](/zh/references/venues)
