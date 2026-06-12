# 北京大学论文模板 (pkuthss)

> 事实核查日期：2026-06。

## 模板信息
- **模板名称**: pkuthss
- **现行仓库**: https://codeberg.org/CasperVector/pkuthss（原 Gitea 仓库已于 2024-08 归档迁出）
- **文档类**: `\documentclass[doctor]{pkuthss}`
- **维护状态**: 原作者仓库最后实质更新为 2024-04；社区有活跃分支
  （如 iofu728 的 Overleaf 适配版，符合 2022 研究生格式审核），使用前
  **以学校最新格式审核要求为准**，必要时优先选择近期通过审核的分支。

## 特殊格式要求

### 图表编号
- 格式：`图3.1` / `表3.1`（章号.序号，用点号）
- 配置：模板自动处理

### 参考文献
- 样式：`biblatex-gb7714-2015`
- 推荐：使用 biblatex

### 特殊章节
- 必须包含"符号说明"章节
- 符号表格式有特定要求

## 编译方式

```bash
# 使用 latexmk
latexmk -xelatex thesis.tex

# 使用 make（如果有 Makefile）
make
```

## 常用命令

```latex
% 文档类选项
\documentclass[
  doctor,           % 博士论文
  % master,         % 硕士论文
  openany,          % 章节可在任意页开始
  oneside,          % 单面打印
]{pkuthss}

% 封面信息
\pkuthssinfo{
  cthesisname = {博士研究生学位论文},
  ethesisname = {Doctor Thesis},
  ctitle = {论文标题},
  etitle = {English Title},
  cauthor = {作者姓名},
  eauthor = {Author Name},
  studentid = {学号},
  date = {\zhdigits{2024}年\zhnumber{6}月},
  school = {信息科学技术学院},
  cmajor = {计算机软件与理论},
  emajor = {Computer Software and Theory},
  direction = {研究方向},
  cmentor = {导师姓名},
  ementor = {Supervisor Name},
  ckeywords = {关键词1，关键词2，关键词3},
  ekeywords = {keyword1, keyword2, keyword3},
}
```

## 注意事项

1. 使用 XeLaTeX 编译
2. 符号说明章节是必需的
3. 注意检查页眉格式
4. 参考文献格式需严格遵循
5. 模板维护放缓（原仓库已归档），提交前与学院确认当年格式审核要求
