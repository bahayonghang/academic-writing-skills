# IEEE 会议/期刊 (LaTeX)

> 这是从 `references/venues/catalog.md` 提取的期刊/会议专项快照。
> 当用户指定 IEEE 为目标投稿场所时，直接加载此文件，无需读取完整目录。

## 风格

- 贡献的积极声音
- 方法的过去式
- 结果讨论的现在时

## 格式

- 两列布局
- 摘要：单段，最多 250 词（依据 IEEE Author Center；不存在全局“150-200 词”规则）
- 关键词：3-5 个术语
- IEEEtran 仍为 v1.8b（2015）；IEEE 尚未更改其模板或字体要求

## 引文

- IEEE 风格：[1]、[2-4]
- 参考书目中的完整参考

## 图/表

- 图下方有文字说明
- 表格上方的标题
- 在出现之前在文本中引用

## 伪代码

- IEEEtran 只将 `figure` 和 `table` 识别为标准浮动体；不要假定专用的 `algorithm` 浮动体符合 IEEE 要求。
- IEEE 投稿中的 LaTeX 伪代码优先使用 `figure` + `algorithmicx` / `algpseudocodex`。
- 为伪代码块提供正常的图形标题，并在图形出现之前在文本中引用它。
- 优先使用直接的图题，例如 `Adaptive inference procedure`，而不是 `The proposed algorithm...`。
- 显式输入/输出标记和简短的内联注释是建议的默认值，而不是 IEEE 硬性要求。
