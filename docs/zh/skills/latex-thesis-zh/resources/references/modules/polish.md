# 模块：单元润色（polish）

明确要求“润色这段”“润色这一节”“把第 X 章语言润色一下”时使用。先列单元，再逐单元改写和核对；只要求检查或审校时只交付诊断。完整流程见 [单元润色协议](../writing/unit-polish-zh.md)。

## 命令与单元

```bash
uv run python $SKILL_DIR/scripts/polish_unit_zh.py main.tex --plan
uv run python $SKILL_DIR/scripts/polish_unit_zh.py main.tex --plan --section introduction
uv run python $SKILL_DIR/scripts/polish_unit_zh.py main.tex --plan --unit 1.1.1
uv run python $SKILL_DIR/scripts/polish_unit_zh.py main.tex --verify --unit 1.1.1 --revised revised.tex
uv run python $SKILL_DIR/scripts/polish_unit_zh.py main.tex --verify --original original.tex --revised revised.tex --terms terms.json --max-growth 0.20 --json
```

`$SKILL_DIR` 替换为本技能安装目录。`--plan` 与 `--verify` 互斥。核对需要 `--revised`，且 `--unit` 与 `--original` 二选一。单章入口可用 `--first-chapter N` 声明真实章号，语义沿用小节上下文游标。

- `subsection` 是相对标题树的 depth-3 小节，包含原有标题行，不固定绑定某个 LaTeX 命令；编号与 [logic](logic.md) 相同。
- 没有 depth-3 标题时只列 `paragraph` 自然段单元，不回退到 depth-2。段落编号形如 `introduction#3`。
- 清单只列编号、类型、标题、源文件行区间、约字数和只读邻域坐标，不复制正文。`prev.tail`、`parent_lead`、`next.head` 或前后自然段均只读。
- 超过 1200 个可见汉字的小节标记需拆分，并列出内部段落单元；逐段润色和核对，不合并成整章替换稿。每次改写前重新运行 `--plan`，避免沿用编辑前的行号。

## 核对码与分档

| 码 | 判定范围 | 档 / Severity / Priority |
| --- | --- | --- |
| `UP-SCOPE` | 标题命令或标题文本增删改；新增输入/文档结构命令；新增只读邻域首句的精确子串（至少 12 个汉字）。原样标题及原文已有重复句不报 | A / Error / P1 |
| `UP-CITE` | 引用键多重集变化 | A / Error / P1 |
| `UP-REF` | `\ref` / `\eqref` / `\autoref` / `\cref` / `\pageref`（含首字母大写及星号形式）的目标多重集变化 | A / Error / P1 |
| `UP-LABEL` | 标签集合变化 | A / Error / P1 |
| `UP-MATH` | 空白规范化后的数学内容多重集变化 | A / Error / P1 |
| `UP-NUM` | 可见正文数字、百分比、科学计数及数值单位 token 多重集变化 | A / Error / P1 |
| `UP-TOKEN` | 含数字标识符、大写连字符名、全大写缩写集合变化 | B / Warning / P2 |
| `UP-TERM` | 用户术语计数变化；未传术语表时不检查 | B / Warning / P2 |
| `UP-STRENGTH` | 强度词与 hedge 计数变化及上下文，疑似方向仅供复核，不判定语义 | B / Warning / P2 |
| `UP-NEG` | 否定标记计数变化（未标定启发式） | B / Info / P3 |
| `UP-LENGTH` | 可见汉字数增减超出比例阈值 | B / Info / P3 |

`UP-CITE` 识别 `\cite`、`\citep`、`\citet`、`\upcite`，以及 biblatex 的 `\parencite`、`\autocite`、`\textcite`、`\footcite`、`\footcitetext`、`\smartcite`、`\supercite`；同时识别 `\cites` 和这些 biblatex 命令的 `s` 复数形式。支持首字母大写、星号、每组 `[前注][后注]{键}`，多重引用还支持 `(全局前注)(全局后注)`；各组引用键统一按多重集比较。不展开自定义宏，也不把任意含 `cite` 的命令名当作引用。

`--max-growth` 默认 `0.20`，对增长和缩短均检查；阈值未标定，不代表误报率或质量分数。`--terms` 复用 [consistency](consistency.md) 的自定义术语 JSON：`{"zh": [["软测量", "软传感器"]], "en": [["MAE", "mean absolute error"]]}`。这里将各组扁平化后逐词保护，不授权同义词替换。

`UP-STRENGTH` 计数前跳过 `--terms` 明确列出的术语片段，避免把“支持向量机”里的“支持”当作结论词；术语计数变化仍由 `UP-TERM` 报告，术语之外的强度词仍参与核对。未配置的术语或“相关研究”等普通用法可能产生候选，须结合报告上下文判断，不能据计数变化断言语义漂移。

A 档报告确定的差异项；B 档只给复核候选，不给替换文本。每条 `[Script]` 发现只带 `Meaning-Check: NEEDS-LLM`，不输出 `Risk-Flags` 行。可见文本解析不能覆盖所有模板宏数值；因果、范围和术语语义仍需人工或 LLM 核对。

## 退出码与改写契约

`--plan` 退出码为 0（含无 depth-3 或章节未命中声明），文本报告只列清单，不附核对结论；`--verify` 有 Error 时为 1，否则为 0；参数错误为 2。核对结论为 `BLOCK` 或 `PASS-SCRIPT`；零发现也带 `NEEDS-LLM`，不得据此宣称语义已保全。

本模块仅 `[LLM]` 改写适用四字段契约。`[Script]` 绝不得声称 `PRESERVED`；`[LLM]` 的 `PRESERVED` 仍是待作者核对的提案。交付块沿用 [路由契约](routing-rules.md)：

```latex
% POLISH (source.tex:L10-L14) [Severity: Info] [Priority: P3] [LLM]: 单元润色提案
% Changed:       <实际改动>
% Protected:     <受保护内容>
% Meaning-Check: <PRESERVED | NEEDS-LLM>
% Risk-Flags:    <none | not-assessed | lexical-substitution | whitespace-normalized | overstatement | ambiguity | terminology-drift | invented-claim>
```

按 [over-claim-guard.md](../writing/over-claim-guard.md) 对照强度阶梯，保持原文结论强度，不得擅自抬升或削弱。脚本候选不授权加强表述。

## 与既有模块的边界

- [expression](expression.md) 负责口语、语法、标点、数值单位与单句长度；[deai](deai.md) 负责垫话、结构壳与句长均匀度。只复用其单元前诊断。
- [claim-forward](claim-forward.md) 负责主张位置、自我削弱与免责句；本流程保持原强度，只允许在单元内移位限制，不删除限制或不利结果。
- [logic](logic.md) 负责小节游标、只读窗口、段落弧线和论证结构。此模块只改句子与词汇，不改段落顺序或增删论断；编辑轴沿用既有语义，脚本不接收编辑轴参数。
- [consistency](consistency.md) 负责全文术语一致性；此处只核对用户术语在原文与润色稿中的计数。
