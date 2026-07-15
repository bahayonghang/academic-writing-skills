# 面向审稿人的自我评审

## 客观的

以持怀疑态度的审稿人的身份阅读本节，并在加强散文之前了解拒绝的风险。

## 五维清单

|方面|问题|
| --- | --- |
|贡献|本节揭示了哪些新知识？新奇类型是否明确？|
|书写清晰|知识渊博的读者能够理解段落角色、术语和符号吗？|
|实验实力|性能或结果声明是否有可见的指标和设置支持？|
|评估完整性|基线、消融、指标和数据集是否足以满足要求？|
|方法健全性|假设、模块动机和限制是否明确？|

## 声明-证据图

在响应中使用这种紧凑的形状：

```text
Claim: exact claim or proposed claim
Evidence: citation / figure / table / metric / method section / missing
Status: supported / needs evidence / unsupported
Safe wording: bounded wording that fits the visible evidence
Missing evidence: concrete experiment, citation verification, comparison, or detail
```

## 修改决定

- `supported`：保留声明，但保留设定边界。
- `needs evidence`：仅保留作为弱或有条件声明，或请求丢失的锚点。
- `unsupported`：删除、软化或标记为待决证据。

## 拒绝风险信号

- 主要的摘要或引言声明没有实验证据。
- 方法模块没有动机或消融。
- 相关工作省略了最强的比较器。
- 讨论重复结果，没有机制或限制。
- 结论表明问题已得到解决，超出了评估设置。
