# 图表标题（Caption）生成与优化指南

当用户要求为图表生成英文标题或中英双语标题时，请遵循以下规范。是否使用双语题注、
中英顺序、大小写和目录写法均以学校最新规范与实际模板宏为准；不能从一个学校的示例推出
所有中文学位论文都必须改用 `\bicaption`。

## 1. 英文格式规范

- 先按学校规范与实际模板统一使用 **Title Case** 或 **Sentence case**。校规与模板均未规定时，
  才可把名词性短语用 Title Case、完整句子用 Sentence case 作为项目内的可选统一风格。
- 标题末尾是否加句号同样服从校规、模板和论文现有一致做法；以下示例使用 Sentence case，
  不构成所有学校的强制规则。

## 2. 写作风格（极简与去AI味）

- 直接描述图表内容：去除“The figure shows”或“This diagram illustrates”这类冗余开头。直接以 `Architecture of...`, `Performance comparison of...`, `Visualization of...` 开头。
- 表格图表常用句式：对于表格，推荐使用 `Comparison with...`, `Ablation study on...`, `Results on...` 等标准学术表达。
- 避免使用复杂的生僻词，如 showcase, depict 等，请直接使用 show, compare, present。

## 3. 双语输出说明（\bicaption）

中文学位论文通常使用 `bicaption` 宏包或其他类似机制来实现双语标题。请提示用户将结果放置入如下格式中：

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth]{figures/example.pdf}
  \bicaption{中文标题}{English Title in Title Case or Sentence Case}
  \label{fig:example}
\end{figure}
```

注意 LaTeX 的语法转义：必须对特殊字符（如 `%`、`_`、`&`）进行转义。如有数学公式，保持 `$` 包裹。

## 4. 输出示例

**用户输入：**
为这个图生成双语标题：本图展示了不同模型在三个数据集上的准确率对比。

**Agent 回复：**
```latex
% 图表标题 [Severity: Minor] [Priority: P2]: 建议使用双语 caption
% 中文标题：不同模型在三个数据集上的准确率对比
% English Title：Accuracy comparison of different models across three datasets
%
% 示例用法：
% \bicaption{不同模型在三个数据集上的准确率对比}{Accuracy comparison of different models across three datasets}
```

## 5. 题注命令与模板边界

- `check_references.py` 与 `check_tables.py` 的存在性检查识别 `\caption`、`\bicaption`，
  以及它们在命令后使用空白/换行和合法可选短标题的形式。
- 存在性检查只证明真实题注命令出现，不验证中英文内容、字体、目录或模板排版是否正确；
  `\captionsetup`、注释中的题注和相似自定义命令不算题注。
- 学校 class 已提供专用题注宏时，先查 class 文档与论文现有用法。不得为统一风格强制把
  所有模板替换成 `\bicaption`，也不新增任意宏别名配置。

## 6. 续图与图目录

只有实际模板或已加载宏包支持时，才使用 `\ContinuedFloat`、空目录题注或模板专用续图宏。
局部修改后同时检查：

1. 续页是否沿用预期编号与“续”标记；
2. `.aux` / 图目录是否只出现模板要求的条目，短标题是否正确；
3. 前一页、续页和下一页的题注、页眉页脚与正文是否发生挤压。

编译成功或图目录文件存在都不能代替实际查看这些页面。若模板没有相应续图语义，保留
现状并报告所需模板证据，不套用其他学校的宏。

## 7. 子题注去重

先确认 `subcaption`、`subfig` 或学校宏如何生成主题注、子题注和英文目录项。只有主/子层级
确实重复同一信息时才局部删减；不能把“避免重复”解释为所有子题注都改单语，亦不能在
不了解模板语义时删除英文题注。验收时查看主图、每个子图标号及中英文题注的阅读顺序。

## 8. 有效图像清晰度与可编辑源

图像文件写有“300 DPI”元数据不代表论文中的有效分辨率合格。有效 ppi 由像素尺寸和最终
排版宽度共同决定，例如横向有效 ppi = 横向像素数 / 最终宽度（英寸）。目标阈值以学校或
出版要求为准；没有最终排版尺寸时不能宣布清晰度通过。

- 优先保留并修改可编辑矢量或原始图源，再导出论文使用的 PDF/PNG；不要只在低分辨率
  截图上反复缩放。
- 同时核对可编辑源、导出图和编译页：源文件存在不证明导出正确，PNG 存在也不证明最终页
  清晰、未裁切或文字可读。
- Windows 下只有在工具确因非 ASCII 路径失败时，才复制到任务自有的 ASCII 临时名处理；
  这只是操作兼容建议，不改变源文件所有权，也不是默认步骤。

## 9. 视觉验收边界

图表版式修改须通过现有 `compile.py` wrapper 使用论文实际入口和 recipe 编译，再查看受影响
页面及相邻页。单测、日志、`.aux`、图目录或一张 PNG 只能提供局部证据；没有实际查看渲染页
时，视觉结论保持 `missing evidence`。不自动清理或压缩原 PDF，不安装工具，也不使用 UI
自动化替代授权的文件与命令行路径。
