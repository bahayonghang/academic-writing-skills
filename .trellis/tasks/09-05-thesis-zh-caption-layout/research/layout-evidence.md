# 题注与版式实际证据

日期：2026-09-05。执行和目视审阅：主 Agent。真实论文未读取正文、修改或编译。

## 合成 TeX 编译与目视

可复现源文件：[layout-fixture/main.tex](layout-fixture/main.tex)。采用本机已有的 TeX Live 2025、
ctexart、caption/bicaption/subcaption、longtable、booktabs；不假称具备或验证任何学校模板。
图形是 TeX 矢量方框，无外部图片、私有数据或新依赖。

首次命令（仓库根目录）：

```powershell
uv run python academic-writing-skills/latex-thesis-zh/scripts/compile.py .trellis/tasks/09-05-thesis-zh-caption-layout/research/layout-fixture/main.tex --recipe latexmk --outdir build
```

结果：外部 latexmk 成功生成 `layout-fixture/build/main.pdf`，6 页；wrapper 返回 1，
报 `PDF not found: .../layout-fixture/main.pdf`。这是既有 wrapper 输出路径检查问题，
并非 bicaption/排版编译失败。未扩大范围修改 compile.py，保留此项为范围外缺陷。
uv 仅按已有锁定配置创建本地环境，没有新增项目依赖。

随后使用已有不带输出目录参数的调用：

```powershell
python -X utf8 academic-writing-skills/latex-thesis-zh/scripts/compile.py .trellis/tasks/09-05-thesis-zh-caption-layout/research/layout-fixture/main.tex --recipe latexmk
pdftoppm -png -scale-to 1200 .trellis/tasks/09-05-thesis-zh-caption-layout/research/layout-fixture/main.pdf .trellis/tasks/09-05-thesis-zh-caption-layout/research/layout-fixture/page
```

两条命令退出码均为 0。PDF 6 页，49,590 bytes；`page-1.png` 至 `page-6.png` 已由
`view_image` 逐页实际查看，不能仅凭文件存在推断目视通过。生成文件留在本地并被该目录
`.gitignore` 或仓库 build/log 规则忽略；源文件可复现。Windows Perl 发出 locale 回退提示，
没有阻止编译；最终 main.log 无 Warning、Overfull 或 Underfull 匹配。

| 页 | 实际视觉发现 | 裁决 |
| --- | --- | --- |
| 1 | 引用显示图 1、表 1/2；图目录含图 1 的中英文各一条，均指向第 2 页，无续图新增项；表目录正常 | PASS |
| 2 | 子图 (a)/(b) 标签只出现一次；主图中英文均为编号 1；方框、标题和正文无重叠或裁切 | PASS |
| 3 | 续图中英文仍为编号 1，均有续图文字；正文完整 | PASS |
| 4 | 双语表题在表体上方，固定列宽正文可读；长表编号 2，首段行 01–06，下方有接下页提示 | PASS |
| 5 | 续表仍为编号 2、重复表头，行 07–14 连续，表后正文紧随且无异常拉伸空白 | PASS |
| 6 | 后续页面正文和图 1/表 1 引用完整，无遗失内容 | PASS |

AUX 交叉证据：`fig:synthetic={{1}{2}...}`、`tab:bilingual={{1}{4}...}`、
`tab:long={{2}{4}...}`；LOF 恰有图 1 的两种语言首图条目，LOT 含表 1 双语条目及表 2
首表条目。空可选目录标题用于已安装 bicaption/caption 宏，并通过实际 LOF/LOT 验证。

此结果只证明合成示例中的宏、编号、目录与分页。页眉继承 ctexart 的目录标记，
不是学校模板验收对象。局部 LTpost 在示例中可用，不证明真实模板存在拉伸；
没有真实位图，故不声称检查了图源有效 ppi、用户图像清晰度或打印效果。

## 文档行为评测

2026-09-06 的实际回答见 [output-responses.md](output-responses.md)。gpt-5.6-sol/max 只投影
eval 46–47 的输入，主 Agent 逐条阅读后裁决；没有外部 provider A/B 或人工盲评。

| ID | 实际回答核对 | 裁决 |
| --- | --- | --- |
| 46 | 正确接受跨行 caption 与双语短标题；区分存在性和表体下方的位置问题；captionsetup、fakecaption、注释不能抵消缺失；沿用输入明确的 chapters/captions.tex 行锚点，未知 label 行号不编造 | PASS |
| 47 | 300 DPI 元数据不证明有效 ppi；真实入口/recipe 与学校宏优先；续图目录、LTpost 留白、二次缩放均先定位并做局部处理；无渲染页不报视觉通过，不清理/压缩/重绘PDF、不安装工具、不改class、不做UI | PASS |

ID 46 没有提供完整文件（files=[]），回答明确只是给定片段上的候选判断，所有 CLI 均未执行。
其诊断与本任务实际 public checker 回归及主 Agent 的合成 CLI 对照一致；不把另一个 fixture
的结果冒充它的真实 main.tex 输出。ID 47 的像素尺寸、排版宽度、模板与页面均缺失，回答
如实保留 missing evidence；本任务六页合成文档的视觉证据也不替代该未知 PNG 的验证。

## 题注回归与资源交接

实现 Agent 在源码修复前运行 test_caption_commands.py：9 failed / 4 passed；修复后 13 passed。
新增测试调用完整公开 checker，覆盖合法题注、注释/相似命令、错误位置、多文件路径与行号，
并有 ZH 路径加载及对称 import 状态恢复。
implement.md 目标脚本/多文件/parser 回归为 152 passed，skill+trigger 契约 53 passed，
双语资源契约 10 passed；271 项 manifest/单技能完整资源检查、目标 Ruff、doc-build 和 diff-check
均通过。新增 eval 46–47、trigger 第 49 条；最终全量 CI 由父任务独立检查另记。

## 修改前完整 CLI 对照

对同一合成 main.tex 执行 ZH `check_references.py` 与 `check_tables.py`（系统 Python -X utf8）。
references 报第 43 行双语表题缺失：`Missing caption in table environment`，即使上文已实际编译成功。
另有第 8/9 行三个前向引用提示，属既有检查行为，和题注修复无关。
tables 此文件报告 PASS / 0 issues：其旧 `\\caption` 前缀匹配会把第 41 行 `\\captionsetup`
当题注。这项假绿说明需同时锁命令边界，不能只凭复杂文件的 tables PASS 判断已支持 bicaption。
父任务此前的无 captionsetup 最小表格仍已复现两条 checker 的双语题注缺失误报。

## 修改后同一 CLI 对照

2026-09-06 主 Agent 在两脚本最小修复后，以相同参数重新运行上述 main.tex：
references 的第 43 行 `Missing caption` 消失，仅保留与本任务无关的三个前向引用 Minor 提示；
tables 仍为 1 table / PASS / 0 issues。表格路径的真假题注区分另由新增完整 checker 回归锁定，
因此不把此复杂 fixture 的单独 PASS 当作命令边界证明。

默认行为变化属于误报/假绿修复：合法双语题注不再报缺失，注释或 captionsetup 不能掩盖缺失，
下方表题仍报位置问题。未来若获准提交，应在提交说明中保留“默认行为变化”及其原因。
