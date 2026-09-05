# `latex-thesis-zh` 题注与版式合成输出采样（ID 46--47）

- 采样日期：2026-09-06
- 当前 Agent：`gpt-5.6-sol / max`
- 采样性质：这是当前 Agent 对合成输入生成的实际最终回答，不是外部 provider 或独立人类盲评，也不在本文件裁决验收条件。
- 输入提取：从 `academic-writing-skills/latex-thesis-zh/evals/evals.json` 仅投影 `id`、`prompt`、`files`；`expected_output` 与 `assertions` 未输出到当前 Agent 上下文。两条输入的 `files` 均为 `[]`，未读取真实论文、调用外部模型或执行产品脚本。
- 证据边界：没有借用本任务其他 fixture、编译记录或目视结果来冒充输入文件的实跑证据。

## 读取的规则来源

- `academic-writing-skills/latex-thesis-zh/SKILL.md`
- `academic-writing-skills/latex-thesis-zh/references/formatting/caption-guide.md`
- `academic-writing-skills/latex-thesis-zh/references/formatting/table-guide.md`
- `academic-writing-skills/latex-thesis-zh/references/modules/references.md`
- `academic-writing-skills/latex-thesis-zh/references/modules/tables.md`
- `academic-writing-skills/latex-thesis-zh/references/modules/compile.md`
- `academic-writing-skills/latex-thesis-zh/references/latex/compilation.md`

## ID 46

### 输入

`files: []`

```text
请审查已有中文 LaTeX 学位论文 main.tex 的双语图表题。main.tex 通过 \input{chapters/captions} 引入子文件。chapters/captions.tex 中：第3行 figure 使用跨行的 \caption [流程简称]\n{系统流程} 后接 \label{fig:flow}；第8行 table 使用 \bicaption[参数表]{参数设置}[Parameters]{Parameter settings}，位于 tabular 之前并后接 \label{tab:param}；第14行另一个 table 先结束 tabular，第18行才写 \bicaption{消融结果}{Ablation results} 与 \label{tab:ablation}；第24行 table 只有 \captionsetup{font=small}、\fakecaption{占位} 和被注释掉的 % \caption{不应计入}，但有 \label{tab:missing}。请分别按 references 和 tables 模块给出检查结果，保留源文件与行号，不修改源码。
```

### 实际回答

`files: []` 表明当前没有可读取的 `main.tex` 或 `chapters/captions.tex`。以下结论仅依据题目给出的源行描述，是候选判断，不是脚本实跑结果；未生成退出码，也未补造未知的标签行号。实际文件可用时，两个模块的真实入口分别为：

```bash
uv run python $SKILL_DIR/scripts/check_references.py main.tex
uv run python $SKILL_DIR/scripts/check_tables.py main.tex
```

以上命令在本回答中均未执行。

**`references` 模块候选判断**

| 位置 | 判断 |
| --- | --- |
| `chapters/captions.tex:3` | `\caption [流程简称]` 后换行再给出 `{系统流程}`，属于带合法可选短标题和命令后空白的真实普通题注；后接 `\label{fig:flow}`。基于所给描述，不产生缺题注候选。普通 `\caption` 的存在性应被接受，但是否满足该校双语题注要求仍需 class 或学校规范，当前为 `missing evidence`。 |
| `chapters/captions.tex:8` | `\bicaption[参数表]{参数设置}[Parameters]{Parameter settings}` 是带中英文可选短标题的真实双语题注，后接 `\label{tab:param}`。基于所给描述，不产生缺题注候选。 |
| `chapters/captions.tex:18` | `\bicaption{消融结果}{Ablation results}` 仍是真实题注，后接 `\label{tab:ablation}`。`references` 只检查题注存在性，不因它位于 `tabular` 之后而把它判为缺失；位置问题由 `tables` 处理。 |
| `chapters/captions.tex:24`（题目给出的 table 位置） | `\captionsetup{font=small}`、`\fakecaption{占位}` 和注释中的 `% \caption{不应计入}` 均不是真实题注。已有 `\label{tab:missing}`，因此按给定描述应报告缺题注候选，严重度为 Major/P1。`references` 实跑会定位到 label 所在行，但题目没有给出该精确行号，因此该定位为 `missing evidence`。 |

是否存在未定义引用、未引用标签、编号断档或同文件内引用先于定义，需要完整装配后的实际工程才能判断；题目没有给出这些证据。

**`tables` 模块候选判断**

| 位置 | 判断 |
| --- | --- |
| `chapters/captions.tex:3` | 这是 `figure`，不属于 `check_tables.py` 扫描的 `table` / `table*` 范围。 |
| `chapters/captions.tex:8` | 真实 `\bicaption` 位于 `tabular` 之前，题注存在且位置满足该项结构检查。双语措辞、字体、目录项和模板渲染不由此检查证明。 |
| `chapters/captions.tex:14`、`chapters/captions.tex:18` | 该表在第14行的内容结构中先结束 `tabular`，第18行才出现真实 `\bicaption`，因此应报告“题注位于表体之后”的位置候选。`references` 接受其存在，不会抵消这里的位置问题。 |
| `chapters/captions.tex:24` | 该表没有真实 `\caption` 或 `\bicaption`；设置命令、相似命令和注释不能掩盖缺失，因此 `tables` 也应报告缺题注候选。 |

三线表规则、表注、数值精度与 `booktabs` 加载情况未在题目中提供，均为 `missing evidence`。本回答不修改源码。

## ID 47

### 输入

`files: []`

```text
我的中文博士论文已有 LaTeX 工程，某 PNG 只标了 300 DPI，没有像素尺寸、最终排版宽度或编译页；续图需要进入图目录但不要重复目录项；longtable 后出现大块留白；一个定宽表又套了 \resizebox 并缩小字号。请给出有条件的排查与验收步骤。必须使用 skill 自带 compile.py 和项目实际入口/recipe，不清理、压缩或重绘原 PDF，不安装工具，也不做 UI 自动化；缺少视觉证据时请明确标记 missing evidence。
```

### 实际回答

当前只有问题描述，没有工程文件、像素尺寸、实际入口、recipe、编译页或渲染页面。下面是条件性排查步骤，不代表已经执行编译或目视验收。

1. **先确定项目入口与 recipe。** 从项目现有构建配置、模板说明或历史命令确认实际入口文件、引擎和参考文献后端。只选择与项目匹配的 recipe，不把 `main.tex`、XeLaTeX 或某一种 bibliography 后端当作通用默认值。确认后通过 skill wrapper 运行：

   ```bash
   uv run python $SKILL_DIR/scripts/compile.py <实际入口.tex> --recipe <项目检测所得-recipe>
   ```

   该命令是入口模板，本回答未执行。验收时要求 wrapper 退出码为 0，并使用 wrapper 报告的 PDF 路径；不得绕过 wrapper 直接调用 TeX 编译器。

2. **核对 PNG 的有效 ppi。** 先取得图像的横纵像素尺寸，再从最终编译页确定实际排版宽度和高度（英寸）。分别计算：

   ```text
   横向有效 ppi = 横向像素数 / 最终宽度（英寸）
   纵向有效 ppi = 纵向像素数 / 最终高度（英寸）
   ```

   将有效 ppi 与学校或出版要求比较，并在编译页检查文字可读性、裁切和缩放伪影。“300 DPI”元数据本身不能证明有效 ppi 或清晰度合格。当前缺少像素尺寸、最终排版尺寸和编译页，因此有效 ppi 与视觉清晰度均为 `missing evidence`。

3. **核对续图与图目录。** 先查实际 class 和已加载宏包对续图的定义，仅在模板支持时使用 `\ContinuedFloat`、空目录题注或模板专用宏。重新编译后检查 `.aux` 与图目录：续页应沿用预期编号和“续”标记，整组图应出现模板要求的目录项且不重复，短标题应正确。随后查看前一页、续页和下一页，检查题注顺序、正文挤压及页眉页脚。当前没有 class 语义、图目录或渲染页，这些结果均为 `missing evidence`。

4. **定位 `longtable` 后留白的真实 owner。** 先在编译页确认留白与表尾、分页、后续段落及重复表头的关系。只有页面证据表明局部 `\LTpost` 或相关 longtable glue 导致该留白时，才在受影响的 `longtable` 外做最小局部设置；若留白来自浮动体、分页或其他对象，则保持 `\LTpost` 不变。修改后重新通过同一入口和 recipe 编译，并查看表尾、后续段落、分页、重复表头及相邻页。当前没有编译页，留白成因与修复效果为 `missing evidence`。

5. **排查定宽表的二次缩放。** 定宽列之外又套用 `\resizebox` 并缩小字号，存在重复缩放的候选风险，但不能只凭源码描述决定删除哪一层。先在编译页核对文字是否过小、列宽是否溢出、换行是否异常、表线是否错位。只有确认某一外层缩放造成不可读时，才移除该冗余层；之后重新检查宽度、换行、表线对齐和可读性。当前没有渲染页，是否存在不可读二次缩放及应移除哪一层均为 `missing evidence`。

6. **完成渲染验收。** wrapper 编译成功后，使用现有且已获授权的文件或命令行渲染路径查看所有受影响页面及相邻页，核对续图编号与目录项、题注顺序、溢出、留白、裁切、缩放和文字可读性。只看到日志、`.aux`、图目录、PNG 或生成的 PDF 都不足以证明视觉结果；没有实际查看渲染页时，最终视觉状态继续标记为 `missing evidence`。

整个流程不清理、压缩或重绘原 PDF，不安装工具，不修改 class，也不使用 UI 自动化。
