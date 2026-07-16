# 模块：标题优化

**触发器**：标题、标题、标题优化、创建标题、改进标题

**目的**：按照 IEEE/ACM/Springer/NeurIPS 最佳实践生成和优化论文标题。

**使用示例**：

**从内容生成标题**：
```bash
uv run python -B scripts/optimize_title.py main.tex --generate
# Analyzes abstract/introduction to propose 3-5 title candidates
```

**优化现有标题**：
```bash
uv run python -B scripts/optimize_title.py main.tex --optimize
# Analyzes current title and provides improvement suggestions
```

**检查标题质量**：
```bash
uv run python -B scripts/optimize_title.py main.tex --check
# Evaluates title against best practices (score 0-100)
```

**标题质量标准**（基于 IEEE 作者中心和顶级期刊或会议）：

|标准|重量|描述|
|-----------|--------|-------------|
|**简明**| 25% |删除“研究”、“研究”、“小说”、“新”、“改进”|
|**可搜索性**| 30% |前 65 个字符中的关键术语（方法 + 问题）|
|**长度**| 15% |最佳：10-15个字；可接受：8-20 个字|
|**特异性**| 20% |具体的方法/问题名称，而不是模糊的术语|
|**无行话**| 10% |避免使用晦涩的缩写（AI、LSTM、DNA 等除外）|

**标题生成工作流程**：

**第1步：内容分析**
摘要/简介摘录：
- **问题**：解决了什么挑战？
- **方法**：提出了什么方法？
- **领域**：什么应用领域？
- **主要成果**：主要成就是什么？ （选修的）

**第2步：关键词提取**
确定3-5个核心关键词：
- 方法关键词：“Transformer”、“图神经网络”、“强化学习”
- 问题关键词：“时间序列预测”、“故障检测”、“图像分割”
- 领域关键词：“工业控制”、“医疗影像”、“自动驾驶”

**第3步：标题模板选择**
顶级期刊或会议的常见模式：

|图案|例子|使用案例|
|---------|---------|----------|
|解决问题的方法|“基于变压器的时间序列预测方法”|一般研究|
|方法：域中的问题|“图神经网络：工业系统中的故障检测”|特定领域|
|问题通过方法|“通过注意力机制进行时间序列预测”|以方法为中心|
|方法+关键特征|“用于实时物体检测的轻量级变压器”|注重绩效|

**第 4 步：标题候选生成**
生成 3-5 名不同侧重点的候选人：
1. 以方法为中心
2. 以问题为中心
3. 以应用为中心
4. 平衡（推荐）
5. 简洁变体

**第 5 步：质量评分**
每位候选人都会收到：
- 总分（0-100）
- 按标准细分
- 具体改进建议

**标题优化规则**：

**删除无效词语**：
|避免|原因|
|-------|--------|
|一项研究|冗余（所有论文都是研究）|
|研究|冗余（所有论文均为研究论文）|
|小说/新|出版物暗示|
|改进/增强|含糊不清，没有具体内容|
|基于|往往是不必要的|
|使用/利用|可以用介词代替|

**优选结构**：
```
Good: "Transformer for Time Series Forecasting in Industrial Control"
Bad:  "A Novel Study on Improved Time Series Forecasting Using Transformers"

Good: "Graph Neural Networks for Fault Detection"
Bad:  "Research on Novel Fault Detection Based on GNNs"

Good: "Attention-Based LSTM for Multivariate Time Series Prediction"
Bad:  "An Improved LSTM Model Using Attention Mechanism for Prediction"
```

**关键词放置策略**：
- **前 65 个字符**：最重要的关键字（方法 + 问题）
- **避免以**开头：冠词（A、An、The）、介词（On、In、For）
- **优先级**：名词和技术术语优先于动词和形容词

**缩写指南**：
|可以接受|标题中避免|
|------------|----------------|
|人工智能、机器学习、深度学习|晦涩的特定领域首字母缩略词|
|LSTM、GRU、CNN|化学式（除非非常常见）|
|物联网、5G、GPS|实验室特定缩写|
|DNA、RNA、核磁共振|非标准方法名称|

**具体期刊或会议调整**：

**IEEE 交易**：
- 避免使用带有下标的公式（除了像“Nd–Fe–B”这样的简单公式）
- 使用标题大小写（主要单词大写）
- 典型长度：10-15 个字
- 示例：“智能制造中预测性维护的深度学习”

**ACM 会议**：
- 创意标题更灵活
- 可以使用冒号作为字幕
- 典型长度：8-12 个字
- 示例：“AttentionFlow：神经网络中注意力机制的可视化”

**施普林格期刊**：
- 更喜欢描述性而非创意性
- 可以稍长一些（最多20个字）
- 示例：“工业物联网系统中实时异常检测的综合框架”

**NeurIPS/ICML**：
- 简洁且有影响力（8-12 个字）
- 方法名称经常突出
- 示例：“变形金刚通过梯度下降在上下文中学习”

**输出格式**：

```latex
% ============================================================
% TITLE OPTIMIZATION REPORT
% ============================================================
% Current Title: "A Novel Study on Time Series Forecasting Using Deep Learning"
% Quality Score: 45/100
%
% Issues Detected:
% 1. [Critical] Contains "Novel Study" (remove ineffective words)
% 2. [Major] Vague method description ("Deep Learning" too broad)
% 3. [Minor] Length acceptable (9 words) but could be more specific
%
% Recommended Titles (Ranked):
%
% 1. "Transformer-Based Time Series Forecasting for Industrial Control" [Score: 92/100]
%    - Concise: ✅ (8 words)
%    - Searchable: ✅ (Method + Problem in first 50 chars)
%    - Specific: ✅ (Transformer, not just "Deep Learning")
%    - Domain: ✅ (Industrial Control)
%
% 2. "Attention Mechanisms for Multivariate Time Series Prediction" [Score: 88/100]
%    - Concise: ✅ (7 words)
%    - Searchable: ✅ (Key terms upfront)
%    - Specific: ✅ (Attention, Multivariate)
%    - Note: Consider adding domain if space allows
%
% 3. "Deep Learning Approach to Time Series Forecasting in Smart Manufacturing" [Score: 78/100]
%    - Concise: ⚠️ (10 words, acceptable)
%    - Searchable: ✅
%    - Specific: ⚠️ ("Deep Learning" still broad)
%    - Domain: ✅ (Smart Manufacturing)
%
% Keyword Analysis:
% - Primary: Transformer, Time Series, Forecasting
% - Secondary: Industrial Control, Attention, LSTM
% - Searchability: "Transformer Time Series" appears in 1,234 papers (good balance)
%
% Suggested LaTeX Update:
% \title{Transformer-Based Time Series Forecasting for Industrial Control}
% ============================================================
```

**交互模式**（推荐）：
```bash
uv run python -B scripts/optimize_title.py main.tex --interactive
# Step-by-step guided title creation with user input
```

**批量模式**（适用于多篇论文）：
```bash
uv run python -B scripts/optimize_title.py "papers/*.tex" --batch --output title_report.json
```

**标题 A/B 测试**（可选）：
```bash
uv run python -B scripts/optimize_title.py main.tex --compare "Title A" "Title B" "Title C"
# Compares multiple title candidates with detailed scoring
```

**最佳实践总结**：
1. **从关键词开始**：将方法+问题放在前10个词中
2. **具体一点**：“Transformer”>“深度学习”>“机器学习”
3. **去除绒毛**：删除“小说”、“研究”、“研究”、“基于”
4. **检查长度**：目标是 10-15 个单词（英语）
5. **测试可搜索性**：您会通过这些关键字找到这篇论文吗？
6. **避免行话**：除非它被广泛认可（AI、LSTM、CNN）
7. **匹配期刊或会议风格**：IEEE（描述性）、ACM（创意）、NeurIPS（简洁）

参考：[IEEE Author Center](https://conferences.ieeeauthorcenter.ieee.org/)、[Royal Society Blog](https://royalsociety.org/blog/2025/01/title-abstract-and-keywords-a-practical-guide-to-maximizing-the-visibility-and-impact-of-your-papers/)

