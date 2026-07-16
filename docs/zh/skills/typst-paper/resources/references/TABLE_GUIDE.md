# 三行表格指南（打字员）

本指南使用 Typst 文档中的“三行”约定定义了专业学术表格的标准。

## 三行表标准

三行表格恰好有三个水平线并且**没有垂直线**：

1. **顶部规则**：列标题上方
2. **中间规则**：列标题下方，数据行上方
3. **底部规则**：最后一个数据行下方

### 打字机实施

```typst
#figure(
  table(
    columns: 3,
    stroke: none,
    table.hline(stroke: 0.8pt),
    [*Model*], [*Precision*], [*Recall*],
    table.hline(stroke: 0.5pt),
    [Baseline], [85.3], [82.1],
    [Ours], [*91.2*], [*89.5*],
    table.hline(stroke: 0.8pt),
  ),
  caption: [Comparison of model accuracy (%).],
) <tab:accuracy>
```

### 要点

- 在表格上设置 `stroke: none` 以删除所有默认边框
- 使用 `table.hline(stroke: 0.8pt)` 进行顶部和底部规则（较重）
- 使用 `table.hline(stroke: 0.5pt)` 作为中尺（较轻）
- 切勿使用 `table.vline()` — 三行表格中没有垂直线
- 切勿在数据行之间添加额外的 `table.hline()`

### 反模式（必须标记）

- `table.vline()` 表中任意位置
- 超过 3 个 `table.hline()` 调用
- 生成网格线的默认笔画（非无）
- `stroke: 1pt` 或表格元素本身上的类似内容

## 数字对齐

Typst 没有内置 `siunitx` 等效项。对于小数点对齐：
- 使用 `align: right` 右对齐数字列
- 手动确保小数点位置一致

```typst
table(
  columns: (auto, 1fr, 1fr),
  align: (left, right, right),
  // ...
)
```

## 统计显着性标记

|象征|意义|
|--------|---------|
| `*`    |p < 0.05|
| `**`   |p < 0.01|
| `***`  |p < 0.001|

## 数字精度规则

|数据类型|精确|例子|
|-----------|-----------|---------|
|百分比|小数点后 1 位| 85.3% |
|平均值+/-标准差|2 位小数| 3.14 +/- 0.05 |
|p 值|3位有效数字| 0.003 |

每列内的精度必须一致。

## 标题和注释的位置

- **标题**：使用`#figure(caption: [...])`— 使用时，Typst 默认将表格标题置于上方`figure.where(kind: table)`显示规则
- **标签**：数字后`<tab:name>`
- **表注**：在图中表格下方添加：`[Note. Bold values indicate best performance.]`

## 大胆的最佳价值

使用`*bold*`Typst 中的语法：`[*91.2*]`大胆强调最佳价值观。

## 单词兼容性注意事项

转换为 .docx 时：
1. 在Word中创建标准表格
2. 全选->边框->无边框
3. 添加顶部边框、标题底部边框、表格底部边框
4. 结果：三行表
