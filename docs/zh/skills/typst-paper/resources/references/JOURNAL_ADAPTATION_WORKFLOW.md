# 期刊改编工作流程

本参考文献定义了将论文从一个地点改编到另一个地点的分步过程。 `adapt` 模块使用此工作流程来指导系统格式转换。

## 工作流程概述

### 第 1 步：识别源格式和目标格式

1. **从文档序言中检测当前格式**：
   - `\documentclass{IEEEtran}` → IEEE
   - `\documentclass{acmart}` → ACM
   - `\documentclass[conference]{...}` → 会议论文
   - Typst：检查 `#import` 或模板使用情况
2. **接受用户的目标格式**：
   - 用户提供的期刊指南具有**最高优先级**
   - 如果未提供指南，请使用 VENUES.md 中的已知期刊或会议规则
   - 如果目标地点未知，请用户提供提交指南

### 第 2 步：生成差异检查表

比较这些维度的源需求和目标需求：

#### 2a.参考格式
- 引文风格变更（IEEE → APA 等）
- 交叉引用 CITATION_STYLES.md 以获取确切的规则
- BibTeX 样式文件更改 (`\bibliographystyle{...}`)
- 作者截断阈值更改

#### 2b.摘要格式
- 字数限制调整
- 结构化摘要与非结构化摘要
- 关键词要求（数量、格式）

#### 2c.数字和单位约定
- 交叉引用 NUMBER_UNIT_GUIDE.md
- SI 单位格式
- 数字-单词阈值
- 百分比和统计精度

#### 2d.图和表要求
- 标题格式（句子大小写与标题大小写）
- 图形分辨率要求（DPI）
- 表格样式（需要书签吗？）
- 放置规则（页面顶部、跨列）
- 颜色与灰度要求

#### 2e.页面布局（手动项目）
- 页边距、列、行距
- 字体系列和大小
- 页眉/页脚内容
- 页码样式

### 第 3 步：应用自动更改

对于源中可以更改的每个差异项：
1. 做出改变
2. 在评论中用 `[ADAPTED: reason]` 进行注释

可以自动化的更改：
- 参考书目风格切换
- 摘要字数修剪（标记，而不是剪切）
- 数字格式调整
- 字幕样式调整
- 软件包添加/删除

### 第四步：输出

交付两个工件：

**工件1：修改后的文本**
- 修改后的行上带有 `[ADAPTED: ...]` 注释的改编源
- 切勿改变实质性内容（论据、数据、结论）

**工件 2：手动检查表**
Word/LaTeX/Typst 设置中需要手动干预的项目：

```markdown
## Manual Adaptation Checklist

### Page Layout
- [ ] Set margins to [X cm / inches]
- [ ] Set columns to [single / double]
- [ ] Set line spacing to [single / 1.5 / double]
- [ ] Set font to [Times New Roman / Computer Modern / ...]
- [ ] Set font size to [10pt / 11pt / 12pt]

### Figures
- [ ] Verify all figures are [minimum DPI]
- [ ] Convert color figures to grayscale if required
- [ ] Check figure placement: [top of page / inline / ...]

### Tables
- [ ] Verify table style matches venue (booktabs / grid)
- [ ] Check caption position (above / below)

### Other
- [ ] Add/update page numbers
- [ ] Add/update running header
- [ ] Check supplementary material limits
- [ ] Verify total page count: [N pages max]
```

## 约束条件

- **永远不要改变实质性内容**：论点、数据、方法、结论必须保持不变
- **用户提供的指南覆盖所有默认值**：如果用户提供期刊的作者指南，这些规则绝对优先于 VENUES.md
- **标记不确定性**：如果指南不明确或未找到，请将其标记为供用户验证而不是猜测
- **保留所有引文、标签、数学环境**：与所有其他模块相同的保护规则
