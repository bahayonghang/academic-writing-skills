# 清华大学论文模板 (thuthesis)

> 事实核查日期：2026-06。

## 模板信息
- **模板名称**: thuthesis
- **GitHub**: https://github.com/tuna/thuthesis
- **CTAN**: https://ctan.org/pkg/thuthesis
- **文档类**: `\documentclass{thuthesis}`
- **版本基线**: v7.6.0（2025-03-28，含本科生 2025 规范更新；CTAN 2026-05 仍有更新）。
  写作前从 CTAN 或 GitHub releases 获取最新版，旧版与学校审核要求可能不一致。

## 特殊格式要求

### 图表编号
- 格式：`图 3-1` / `表 3-1`（章号-序号，用连字符）
- 配置：模板自动处理

### 参考文献
- BibTeX 样式：`thuthesis-numeric.bst`（数字编号）或 `thuthesis-author-year.bst`（作者-年份），
  随模板分发，基于 gbt7714 v2.1.6+ 派生，需配合 natbib：
  `\usepackage[sort]{natbib}` + `\bibliographystyle{thuthesis-numeric}` + `\bibliography{refs}`
- 也可使用 `biblatex-gb7714-2015`（backend=biber）
- 注意：v4 时代的旧版专用 bst 样式已废弃，现行版本只提供上述两个 bst

### 公式编号
- 格式：`(3-1)`（章号-序号）

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
