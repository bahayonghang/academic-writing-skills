# 来源依据评估(source-basis)

## 来源身份

`ref/claude-scholar/skills/nature-writing` v0.2.0,自述为"Community contribution based on
curated Nature/Nature Communications writing patterns and open research-writing notes"
(SKILL.md:5)。README.md:22-25 声明构建方式为对未列名的 Nature / Nature Communications
文章的 close reading,**无文章清单、无 DOI、无样本选择说明、无 Nature 官方作者指南引用**。

## 权威性定级

- 定级:**社区归纳的 Nature-leaning 修辞启发式**。
- 禁止在本仓库任何产出中称其为"Nature 官方规则/规范"。
- 新增参考文件的归属声明必须写明:社区归纳来源 + 无原文清单 + 与
  `ref/Research-Paper-Writing-Skills`(Peng Sida 笔记,MIT,已被 EN section-writing 吸收)同源的部分。

## 来源自身的置信措辞

article-architecture.md:29-33 对摘要诊断使用 "may"(may be missing context / may need
scope control / may feel ungrounded),且未提供 `paves the way`、`opens new avenues`、
`In this paper, we` 等词表。**因此这些诊断不具备升为硬性 [Script] 规则的来源依据**,
整合时保持候选提示措辞,归 LLM lane。

## 同源判定证据

- nature-writing 摘要三模板 = Research-Paper-Writing-Skills 摘要三版(同文字骨架)。
- 引言四版/技术挑战三版/pipeline 四版、方法三要素同上。
- latex-paper-en `references/writing/section-writing/index.md` 归属节已声明改编自
  `ref/Research-Paper-Writing-Skills`。
- 结论:上述内容为**非增量**,逐项判定见 delta-matrix.md。
