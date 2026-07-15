# 清华大学论文模板 (thuthesis)

> 事实核查日期：2026-07-09。模板事实来源：thuthesis v7.7.1 手册（thuthesis.dtx）与
> CHANGELOG（GitHub tuna/thuthesis）；校规事实来源见「逐项检查清单」头部。

## 模板信息
- **模板名称**: thuthesis
- **GitHub**: https://github.com/tuna/thuthesis
- **CTAN**: https://ctan.org/pkg/thuthesis
- **文档类**: `\documentclass{thuthesis}`
- **版本基线**: v7.7.1（2026-05-26，同步《写作指南》2026 年 5 月版：统一博士、硕士授权页措辞）。
  写作前从 CTAN 或 GitHub releases 获取最新版，旧版与学校审核要求可能不一致。

## 特殊格式要求

### 图表编号
- 格式：按章编号，模板默认用句点连接：`图 2.1` / `表 2.1`；研究生要求"."或"-"均可（如 `图 2-1`），全篇统一
- 配置：模板自动处理；需要连字符时用 `\thusetup{number-separator = -}`（或分别设置 figure/table/equation-number-separator）

### 参考文献
- BibTeX 样式：`thuthesis-numeric.bst`（数字编号）或 `thuthesis-author-year.bst`（作者-年份），
  随模板分发，基于 gbt7714 v2.1.6+ 派生，需配合 natbib：
  `\usepackage[sort]{natbib}` + `\bibliographystyle{thuthesis-numeric}` + `\bibliography{refs}`
- 也可使用 `biblatex-gb7714-2015`（backend=biber）
- 注意：v4 时代的旧版专用 bst 样式已废弃，现行版本只提供上述两个 bst

### 公式编号
- 格式：按章编号，模板默认句点 `(2.1)`；与图表同用 number-separator 可改为 `(2-1)`，全篇统一

### 页面设置
- 自动由模板处理
- 不要手动修改页边距

## 编译方式

```bash
# 推荐使用 latexmk
latexmk -xelatex main.tex

# 或手动编译
xelatex main
bibtex main
xelatex main
xelatex main
```

## 常用命令

```latex
% 封面信息
\thusetup{
  title = {论文标题},
  title* = {English Title},
  author = {作者姓名},
  supervisor = {导师姓名},
  degree-category = {工学博士},
}

% 摘要
\begin{abstract}
  摘要内容...
\end{abstract}

\begin{abstract*}
  English abstract...
\end{abstract*}

% 关键词
\thusetup{
  keywords = {关键词1, 关键词2, 关键词3},
  keywords* = {keyword1, keyword2, keyword3},
}
```

## 注意事项

1. 必须使用 XeLaTeX 编译
2. 确保系统安装中文字体（SimSun, SimHei, KaiTi）
3. 参考文献使用模板配套样式（thuthesis-numeric.bst / thuthesis-author-year.bst 或 biblatex-gb7714）
4. 提交前检查模板版本是否为最新（CTAN / GitHub releases）

## 逐项检查清单

> 供 `spec-check` 模块终检使用（`--template thuthesis`）。事实核查日期 2026-07-09。来源：
>
> - 校规条目（§ 号为其自身章节号）：《研究生学位论文写作指南》，清华大学研究生院 2025 年
>   3 月版公开副本（官方域名托管）
>   https://www.dhs.tsinghua.edu.cn/wp-content/uploads/2023/12/2025032107444819.pdf ；
>   研究生院正式发布渠道限校内网络访问。2026 年 5 月版原文未公开获得，据 thuthesis
>   CHANGELOG 其差异仅为"统一博士、硕士授权页的措辞"。
> - 模板条目（依据列标"thuthesis 手册"）：thuthesis v7.7.1 手册（thuthesis.dtx，
>   GitHub tuna/thuthesis）。
>
> 该指南**没有**正文/绪论/结论字数、参考文献条数、近五年占比、结论禁引、各章"本章小结"
> 等规定，故本清单无此类条目，也不得套用其他学校数值。
> 检查方式：`script:<checker>` = `check_spec.py` 自动判定；`module:<模块>` = 走 SKILL.md
> 对应模块命令；`llm` = agent 对照正文逐项判读；`manual` = 需编译 PDF/打印核对。

| ID | 检查项 | 规范依据 | 检查方式 | 适用 |
| --- | --- | --- | --- | --- |
| THU-01 | 论文题目"严格控制在 25 个汉字（符）以内"（指南无副题名合计条款，副题名一并计入 25 字判定） | §2.3.1 | script:title_len | 通用 |
| THU-02 | 中文摘要控制在 800～1000 汉字（符） | §2.3.5 | script:abstract_len | 通用 |
| THU-03 | 摘要篇幅限制在一页内书写 | §2.3.5 | manual | 通用 |
| THU-04 | 关键词"不超过 5 个，每个关键词之间用分号间隔"（官方无个数下限，人工判断；thuthesis 源文件中 keywords 以西文逗号分隔、由模板自动输出为全角分号） | §2.3.5 | llm | 通用 |
| THU-05 | 英文 Keywords 与中文摘要部分的关键词对应 | §2.3.5 | script:kw_zh_en_match | 通用 |
| THU-06 | 中文摘要在前、Abstract 在后（§2.1 组成顺序），摘要中文版与英文版文字内容对应 | §2.1 §2.3.5 | script:abstract_order | 通用 |
| THU-07 | 摘要中不出现图片、图表、表格或其他插图材料 | §2.3.5 | llm | 通用 |
| THU-08 | 摘要切忌写成全文提纲（避免"第 1 章……；第 2 章……"陈述方式），重点是结果和结论 | §4.3 | llm | 通用 |
| THU-09 | 目录列至二级节标题（例如 2.2.5）即可 | §2.3.6 | llm | 通用 |
| THU-10 | 一般不建议使用三级节标题；编号最深至四段（x.x.x.x，\subsubsection），不出现更深层级 | §2.3.9.2 | script:heading_depth | 通用 |
| THU-11 | 组成部分及顺序符合规定（中英文封面、名单、授权说明、摘要、Abstract、目录、清单与符号说明、正文、参考文献、附录、致谢、声明、个人简历与学术成果、指导教师评语、答辩委员会决议书），各项独立成部分、每部分从新的一页开始 | §2.1 | llm | 通用 |
| THU-12 | 正文从另页右页开始，每一章应另起页 | §2.3.9.1 | script:new_page_chapter | 通用 |
| THU-13 | 章标题如"第 1 章 引言"：章序号用阿拉伯数字，章序号与标题名之间空一个汉字符（模板 name={第,章} 自动处理） | §2.3.9.2 | llm | 通用 |
| THU-14 | "学位论文指导小组、公开评阅人和答辩委员会名单"原则上限一页 | §2.3.3 | manual | 通用 |
| THU-15 | 图、表和表达式按章编号，两数字间用半角横线"-"或小数点"."连接（如"图 2-1"或"图 2.1"），全篇统一；thuthesis 默认点号，可用 number-separator 选项改连字符 | §2.3.19 | llm | 通用 |
| THU-16 | 图序与图题置于图下方（11pt 居中）、表序与表题置于表上方；表采用三线表（上下边线 1.5 磅、第三线 1 磅，必要时可加辅助线） | §2.3.19 | module:tables | 通用 |
| THU-17 | 各分图以 (a)、(b)、(c) 作为图序，并须有分图题 | §2.3.19 | llm | 通用 |
| THU-18 | 图宜紧置于首次引用该图的文字之后（图表交叉引用完整无断档） | §2.3.19 | module:references | 通用 |
| THU-19 | 跨页图在次页注明"续"字；续表在每页表序前加"续"字并重复表头；过宽图表逆时针旋转 90° 放置 | §2.3.19 | manual | 通用 |
| THU-20 | 表达式序号加括号置于表达式右边行末；较长表达式在运算符或括号之后回行，上下行尽可能在"="处对齐 | §2.3.19 | module:format | 通用 |
| THU-21 | 参考文献著录与标注统一按 GB/T 7714—2015 执行（不区分理工科和人文社科）；"顺序编码制"或"著者-出版年制"仅选一种并全文统一 | §3 §3.4 | module:bibliography | 通用 |
| THU-22 | 参考文献表与正文引用一一对应；引文参考文献表置于正文后另起页；阅读性参考文献可集中列入附录（标题"书目"） | §3.5 §3.1 | module:bibliography | 通用 |
| THU-23 | 使用模板配套文献样式：thuthesis-numeric / thuthesis-author-year（bst 配 natbib，或 biblatex 的 style=thuthesis-author-year），样式由 gbt7714 / biblatex-gb7714-2015 少量改编 | thuthesis 手册 | llm | 通用 |
| THU-24 | 附录依顺序用大写字母编号（附录 A、附录 B……），只有一个附录时也编"附录 A"，每个附录应有标题 | §2.3.11 | script:appendix_letter | 通用 |
| THU-25 | 附录内图表式另行编号，如"图 A.1""表 B.2""式（C-3）" | §2.3.11 | llm | 通用 |
| THU-26 | 引言大致包含：问题的提出、选题背景及意义、文献综述、研究方法、论文结构安排；文献综述"述"的同时要有"评" | §4.4 | llm | 通用 |
| THU-27 | 结论是最终的、总体的结论，不是正文各章小结的简单重复；交代研究工作的局限，提出未来工作的意见或建议 | §4.6 | llm | 通用 |
| THU-28 | 评价自己的研究成果实事求是：除非有足够证据，避免使用"首次""领先""填补空白"或类似词语 | §4.6 | llm | 通用 |
| THU-29 | 除留学生外一律用汉语简体书写；非通用性新名词、新术语、新概念随即解释清楚 | §4.1 §2.3.18 | llm | 通用 |
| THU-30 | 量和单位严格执行 GB 3100—1993、GB/T 3101—1993、GB/T 3102—1993，全文统一、不得两种混用 | §2.3.18 | llm | 通用 |
| THU-31 | 致谢限一页，标题和篇眉内容均为"致谢" | §2.3.12 | manual | 通用 |
| THU-32 | 声明单独一页，标题和篇眉内容均为"声明" | §2.3.13 | manual | 通用 |
| THU-33 | 在学期间学术成果按类型分列并连续编号（学术论文、专著/译著、专利、研究报告、作品等）；未取得成果写"无"；已录用未刊载论文加括号注明被××××期刊录用 | §2.3.14 | llm | 通用 |
| THU-34 | 页边距上下左右均 3.0 厘米、装订线 0 厘米，页眉/页脚距边界 2.2 厘米；A4 标准纸 | §2.4.1 §2.2 | manual | 通用 |
| THU-35 | 篇眉从"摘要"开始，内容与该部分章标题相同，奇偶页相同、各部分首页也有篇眉，五号字居中 | §2.4.2 | manual | 通用 |
| THU-36 | 页码：中文摘要至符号和缩略语说明用大写罗马数字从Ⅰ连续编排；正文第 1 章起用阿拉伯数字从 1 连续编排；页码置页脚居中、两侧不加修饰线 | §2.4.2 | manual | 通用 |
| THU-37 | 从中文摘要开始双面印刷（封面等四部分单面、无篇眉页码） | §2.4.1 | manual | 通用 |
