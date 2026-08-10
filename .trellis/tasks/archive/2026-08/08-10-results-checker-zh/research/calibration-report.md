# RA-* 真实语料标定报告

## 范围与方法

- 日期：2026-08-10。
- 语料：`ref/thesis/decrypted/` 中 5 篇论文各自配对存在的 PDF 与提取 TXT；实际检查输入为
  TXT，PDF 只用于确认论文级来源，不作为原始 LaTeX 工程证据。
- 执行：在系统临时目录中将每个二级实验或结果分析节包装为最小 LaTeX 区间，运行
  `uv run python academic-writing-skills/latex-thesis-zh/scripts/analyze_experiment.py
  <temp>.tex --results-analysis`；未向仓库写入中间语料。
- 限制：TXT 不保留原始 LaTeX 命令、表格结构和可靠段落边界。因此，本报告只能观察词面
  候选，不能证明真实 LaTeX 工程中的查准率或召回率。

证据标签：本表全部命中均为 **PDF-TXT proxy**，不是原始 LaTeX 运行结果；合成边界矩阵为
**synthetic contract evidence**。两者均不能证明真实论文查准率或召回率。

效果口径：**UNVERIFIED / missing evidence**。

## 命中逐条裁决

标记说明：`真` 只表示 PDF-TXT 代理文本仍足以支持该词面候选，不等于真实 LaTeX 真阳性；
`误报` 表示命中由提取结构造成；`存疑` 表示缺少原始 LaTeX 章级窗口或段落边界，无法可靠
裁决。

| 论文 | TXT 行 | 检查项 | 标记 | 裁决依据 |
| --- | ---: | --- | --- | --- |
| 城市固废焚烧 | 3623 | RA-TRANSITION | 存疑 | 节尾落在 PDF 页标，原章小结窗口缺失 |
| 城市固废焚烧 | 5672 | RA-DISTVOCAB | 误报 | 命中对象为箱线图图题；原 LaTeX 图题不属于可见正文段落 |
| 城市固废焚烧 | 5676 | RA-TRANSITION | 存疑 | 节尾为图题，原章小结窗口缺失 |
| 城市固废焚烧 | 7697 | RA-TRANSITION | 存疑 | 节尾为图题，原章小结窗口缺失 |
| 城市固废焚烧 | 9209 | RA-TRANSITION | 存疑 | 节尾为图题，原章小结窗口缺失 |
| 城市固废焚烧 | 11294 | RA-TRANSITION | 存疑 | 节尾落在 PDF 页标，原章小结窗口缺失 |
| 城市固废焚烧 | 11974 | RA-TRANSITION | 存疑 | 节尾落在 PDF 页标，原章小结窗口缺失 |
| 水泥烧成系统多指标预测 | 3819 | RA-TRANSITION | 存疑 | 节尾落在 PDF 页标，原章小结窗口缺失 |
| 水泥烧成系统多指标预测 | 6074 | RA-TRANSITION | 存疑 | 节尾落在 PDF 页标，原章小结窗口缺失 |
| 水泥烧成系统多指标预测 | 7830 | RA-TRANSITION | 存疑 | 节尾落在 PDF 页标，原章小结窗口缺失 |
| 水泥熟料数据增强 | 3765 | RA-TRANSITION | 存疑 | 节尾为表题，原章小结窗口缺失 |
| 水泥熟料数据增强 | 6345 | RA-TRANSITION | 存疑 | 提取节尾缺少下一层标题与章小结上下文 |
| 水泥熟料数据增强 | 9916 | RA-INTERLEAVE | 误报 | 分页与图题合并了多个模型分析段落 |
| 水泥熟料数据增强 | 9978 | RA-INTERLEAVE | 误报 | PDF 提取丢失原段落边界，多个模型说明被合并 |
| 水泥熟料数据增强 | 10033 | RA-INTERLEAVE | 误报 | 指标表行进入同一文本块，制造数值/归因切换 |
| 水泥熟料数据增强 | 10106 | RA-TRANSITION | 存疑 | 节尾虽有总结句，但原下一节接口与章小结上下文缺失 |
| 水泥熟料数据增强 | 11516 | RA-TRANSITION | 存疑 | 节尾与本章小结边界在包装时被截断 |
| 水泥熟料数据增强 | 11516 | RA-INTERLEAVE | 误报 | 表格与节尾正文被 PDF 提取合并为一个块 |
| 水泥粉磨 | 3728 | RA-TRANSITION | 存疑 | 节尾落在 PDF 页标，原章小结窗口缺失 |
| 水泥粉磨 | 5719 | RA-TRANSITION | 存疑 | 节尾落在 PDF 页标，原章小结窗口缺失 |
| 水泥粉磨 | 8453 | RA-TRANSITION | 存疑 | 节尾落在 PDF 页标，原章小结窗口缺失 |
| 水泥粉磨 | 10580 | RA-TRANSITION | 存疑 | 提取区间只剩标题，不能判断原始节末接口 |
| 锌冶炼浸出过程 | 3604 | RA-TRANSITION | 存疑 | 节尾落在 PDF 页标，原章小结窗口缺失 |
| 锌冶炼浸出过程 | 5277 | RA-TRANSITION | 存疑 | 节尾为图题，原章小结窗口缺失 |
| 锌冶炼浸出过程 | 7166 | RA-TRANSITION | 存疑 | 节尾为图题，原章小结窗口缺失 |

汇总：25 条脚本命中中，`误报` 5、`存疑` 20、`真` 0。该汇总反映 PDF-TXT 代理文本的
可判定性，不是“25 个结果节”的分母，也不代表原始 LaTeX 工程中的检查效果。

## RA-INTERLEAVE / RA-STAGE 裁决

- `RA-INTERLEAVE`：删除。结果节内 4 次命中全部为 PDF 提取造成的段落、图题或表格合并，
  误报占多数的裁决门已满足。保留合成正例作为“运行时不得再命中”的回归样例。
- `RA-STAGE`：保留 `Info/P3`。5 篇语料中 0 命中，未观察到误报；规范性语境排除和至少两类
  保真度指标门控由合成边界测试锁定。由于没有真实正例，召回率仍为 `UNVERIFIED`。

## G2 边界矩阵

`tests/skills/latex_thesis_zh/test_results_analysis.py` 覆盖：双通道去重、`result_N` 后缀族、
`--section`/`--per-chapter` 组合、多文件 `源文件:行号`、RA-STAGE 规范声明、RA-CAUSAL
三档、局部最优排除、defensive-ai-rhetoric 五形态与默认/逐章零回归。标定裁决后 focused
套件已全绿；准确测试数与最终质量门记录在子任务 `prd.md` 的验证证据中。该矩阵只属于
synthetic contract evidence，真实效果声明仍遵守上述 `UNVERIFIED` 口径。
