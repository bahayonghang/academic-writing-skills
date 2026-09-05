# 设计

## 修复与边界

只修改 academic-writing-skills/latex-thesis-zh/scripts/check_references.py、
scripts/check_tables.py 的题注识别/定位责任；优先使用已有注释处理。
用最小命令识别支持 caption/bicaption 及其合法可选标题，保留命令边界，不实现任意宏展开、
配置式别名表或通用 TeX AST。存在性检查不声称验证题注内容或模板排版。
表格位置检查针对现有已支持表环境，不借机扩展长表解析器。
新增计划测试文件 tests/skills/latex_thesis_zh/test_caption_commands.py；
ZH 模块通过 importlib 按路径加载并对称恢复 sys.path/sys.modules。

## 指南落点

扩充同 skill 的 references/formatting/caption-guide.md、table-guide.md、
references/modules/compile.md、references/latex/compilation.md；必要的 format/tables/references
模块页只加指针。题注中英文字母大小写遵循实际校规，不从一个案例推出通用要求。
- 续图：有相应宏支持才用 ContinuedFloat/空目录题注；检查 AUX/图目录与下一页。
- 长表：确有 LTpost 拉伸才局部固定间距，不改全局 class。
- 子题注：按模板语义避免重复，而非所有学校必须改单语。
- 表格：已有固定列宽时先排查 resizebox 与小字号的二次压缩，检查溢出/可读性。
- 图像：像素尺寸及最终排版宽度共同决定有效 ppi；已有可编辑源优先；
  图源/PNG/编译页一起核对，Windows ASCII 临时名只是遇到编码故障后的操作建议。

wrapper 已支持 --recipe xelatex-bibtex / xelatex-biber，使用项目实际入口，
不固定 document.tex/XeLaTeX 为所有论文唯一选择，不直接执行旧指南清理命令。
不增加 PDF 压缩、重绘、系统安装或 UI 自动化能力。

## 回归与视觉证据

先将已复现 bicaption 红测和普通/缺失对照写入目标测试；再修复。
补命令边界、注释、位置和多文件映射。最小合成 TeX 的宏/包取自已安装工具，
不能假称拥有 ysuthesis。支持条件不足时只报告静态/单测证据。
如 TeX/Poppler 可用，在任务本地临时输出中编译和渲染代表页，
记录原/后命令、退出码、AUX/目录、PNG路径、实际视觉发现于 research/layout-evidence.md；
不操作用户论文，不把存在一张 PNG 视作已完成目视核验。

## 文档行为评测

evals/evals.json 追加两个合成 output 场景：合法双语题注的 references/tables 审查，
以及只有300 DPI元数据、尚无编译页的版式请求。前者必须与实际 checker 输出一致，
后者不得自称版式通过、擅改模板或清理原PDF；不给工具时保留 missing evidence。
evals/trigger_eval.json 追加“已有中文LaTeX论文的双语续图/长表留白”正例，
保留既有DOCX/英文/Typst近邻负例，不新建module。
修改后用当前Agent对两个场景保存实际响应、命令或未运行原因及逐项裁决，
并入 research/layout-evidence.md；语料形状检查不能替代响应审阅。
