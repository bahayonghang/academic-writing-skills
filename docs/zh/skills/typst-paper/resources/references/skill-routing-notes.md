# 路由、工作流与安全说明（typst-paper）

本扩展指南从 `SKILL.md` 原样迁出。路由不明确、需要组合模块或出现边界问题时阅读。

## 路由规则（完整）

- 首先从用户请求推断模块。仅当请求仍然同样良好地映射到多个不兼容的模块时才请求该模块。
- 如果用户请求 2-3 项兼容检查，请按顺序运行它们，而不是将所有内容合并为一项通用检查。
- 当需要多个模块时使用此执行顺序：`compile` -> `bibliography` -> `format` -> `pseudocode` / `tables` -> `grammar` / `sentences` / `deai` -> `logic` / `literature` / `experiment` -> `title` / `expression` / `translation` / `adapt`.
- 对同一段正文执行多轮润色时，应从粗到细：论证/逻辑 -> 句子结构 -> 词汇/格式，不要反向执行；参见 `references/modules/WORKFLOW.md`。
- 对于参考书目请求，请在运行脚本之前决定 BibTeX 与 Hayagriva；不要事后猜测格式。
- 摘要-引言-结论对齐、引言漏斗断裂或贡献漂移优先使用 `logic`；只有用户明确要求相关工作综合、比较或研究空白推导时才使用 `literature`。
- 对于整篇论文的动机/红线问题（“每个介绍承诺都得到测试和解决吗？”），运行`logic`和`--motivation-thread`;它附加一个只读的 Promise Map + Closure Map 启发式并保留默认值`logic`输出不变。
- 对于分级 de-AI / AIGC 维度分析，运行`deai`和`--tier light|medium|heavy`;它缩放阈值，添加双语 D1 句子长度检查，并按维度 (D1-D5) 标记结果。省略`--tier`保留默认输出。
- 保持`pseudocode`为了`algorithm-figure`, `algorithmic`, `lovelace`、标题、包装器和类似 IEEE 的样式挂钩问题，即使用户将其表述为格式问题。
- 如果命令失败，请报告确切的命令和退出代码，然后再建议下一个回退；不要默默地用通用的散文评论替换失败的脚本运行。

## 触发场​​景（完整列表）

当用户已有 `.typ` 论文项目并需要以下帮助时，请使用此技能：

- Typst 编译或导出问题
- 格式或期刊或会议合规性
- BibTeX 或 Hayagriva 的参考书目验证
- 语法、句子、逻辑或表达复习
- 文献综述重组、相关工作综合或研究差距推导
- 翻译或双语润色
- 标题优化
- 伪代码和算法块审查
- 去AI编辑
- 实验部分回顾

## 安全原理（完整）

- 不要发明引文、标签或实验主张——一旦用户信任，捏造的证据比明确标记的差距更难撤回。
- 默认保持 `@cite`、`<label>`、数学块和 Typst 宏不变；这类意外编辑在 diff 中比正文修改更难发现，而且 Typst 通常只在编译时暴露错误。
- 将编译诊断与散文重写分开——将它们捆绑在一起会鼓励用户同时应用两者，并且不知道哪个更改破坏了什么。
- 除非用户明确要求外部验证或确认引文元数据可以发送到第三方 API，否则请勿启用在线参考书目检查。

## 所需输入（详细信息）

- `main.typ` 或 Typst 条目文件。
- 可选 `--section SECTION` 用于目标分析。
- 当请求目标引用时可选的参考书目路径。
- 当用户关心 IEEE、ACM、Springer 或类似期望时，可选期刊或会议上下文。

如果参数缺失，保留已推断的模块，只询问缺少的 Typst 入口文件、章节、参考书目路径或投稿场所上下文。

## 辅助脚本

- `scripts/deai_batch.py`: 批处理`deai`许多部分/文件的模块。
- `scripts/online_bib_verify.py`: 背后的在线后端`verify_bib.py --online`.
