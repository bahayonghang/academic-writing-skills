# 中文学位论文小节上下文检查器契约

## 1. Scope / Trigger

修改 `latex-thesis-zh/scripts/analyze_logic.py` 的 `--subsection-context`、`--subsection`、
`--emit-window`，小节编号、三元窗口、`S-CTX-*` 判据、术语 YAML、fixture 或公开资源时，
必须遵守本文。面向写作者的语义说明以
`latex-thesis-zh/references/writing/subsection-context-zh.md` 为权威；本文锁定开发接口、
编号父链、窗口 schema、验证错误与防回归门禁。

## 2. Signatures

```text
uv run python scripts/analyze_logic.py INPUT --subsection-context
    [--subsection X.X.X] [--section SECTION] [--first-chapter N]
uv run python scripts/analyze_logic.py INPUT --emit-window --subsection X.X.X
```

```python
_build_subsection_cursor(
    doc: AssembledDocument,
    parser,
    sections: dict[str, tuple[int, int]],
    first_chapter: int | None = None,
) -> list[SubsectionUnit]

_build_context_window(
    units: list[SubsectionUnit],
    index: int,
    paragraphs: list[ArcParagraph],
) -> dict[str, object]

_check_subsection_context(
    units: list[SubsectionUnit],
    windows: list[dict[str, object]],
    terms: dict[str, tuple[str, ...]],
) -> list[str]

SUBSECTION_CONTEXT_MIN_HAN = 20
SUBSECTION_CONTEXT_MIN_HAN_RATIO = 0.30
```

新参数必须追加在 `analyze()` 现有位置参数之后且默认关闭；未传新开关时，既有 fixture/flag
组合的输出必须逐字不变。

## 3. Contracts

### 3.1 小节游标与编号父链

- 先用 `tex_loader.assemble()` 装配 `\include` / `\input`，再在 assembled content 上调用
  `extract_headings()`；对外坐标必须经 `AssembledDocument.origin()` 投影回源文件与文件内行号。
- `root_level = min(heading.level)`，`depth = heading.level - root_level + 1`；小节单元只取
  `depth == 3`，不绑定 `\subsection` 或 `\subsubsection` 命令。
- 编号必须同时跟踪 `root_numbered` 与 `parent_numbered`。`\chapter*`、`\section*` 等无编号
  标题会使对应父链失效；其下标题不得复用上一编号根/父的计数器生成伪 `x.x.x`。
- 单元只保存自身字段。`prev_id`、`next_id`、`same_parent`、`boundary` 必须由有序单元列表
  派生，不进入 `SubsectionUnit`。
- 没有有效编号的 depth-3 单元时不回退到 depth-2，输出固定声明且不产出 S-CTX 观察。

### 3.2 窗口与可编辑边界

窗口只序列化坐标，不复制正文：

```json
{
  "subsection_id": "2.1.1",
  "editable": {"part": "current", "source_start": 12, "source_end": 55, "status": "ok"},
  "read_only": [
    {"part": "prev.tail", "source_file": "chapters/method.tex", "source_start": 4, "source_end": 9, "status": "ok"}
  ],
  "same_parent": {"prev": true, "next": true},
  "boundary": "",
  "prev_id": "2.1.0",
  "next_id": "2.1.2"
}
```

- 只有 `current` 可产出改写建议；`prev.tail`、`next.head`、`parent_lead` 一律只读。
- `read_only` 顺序固定为 `prev.tail`、`parent_lead`、`next.head`；缺失部件不进数组，状态在
  `prev_tail_status` / `parent_lead_status` / `next_head_status` 中表达。
- 跨父节时 `parent_lead` 从真实父标题行开始，截止第一个子标题前的最后合格导语行；不得把
  无编号子标题及其正文纳入父导语。
- canonical eligibility 要求汉字数不少于 20、汉字占比不少于 0.30，并排除列表项、环境
  收尾与豁免章节；与 P-ARC 不同，标题后的第一个正文段不得因 `is_heading_lead` 被排除。

### 3.3 Findings 与术语

- 码集固定为 `S-CTX-IN`、`S-CTX-OUT`、`S-CTX-ROLE`；不得恢复未标定的 `S-CTX-DUP`。
- 单项是 `[Script]` + Info/P3 + `Meaning-Check: NEEDS-LLM`；同一父节连续 3 个单元同时缺
  IN/OUT 时增加 `S-CTX-IN+OUT` Minor/P2 汇总，单项不升级。
- `context_sides` 是列表；跨父节 IN 使用 `["current", "parent_lead"]`，同父节使用
  `["current", "prev.tail"]`。
- `subsection-context-terms.yaml` 逐字段加载；文件缺失、字段缺失或字段类型非法时，只回退
  该字段到内置同值表。

## 4. Validation & Error Matrix

| 条件 | 行为 |
| --- | --- |
| 无有效编号 depth-3 单元 | 输出 `% 小节级：本文档无 depth-3 标题，未产出小节级观察。`；零条 S-CTX |
| `--emit-window` 未带 `--subsection` | argparse 失败：`--emit-window 必须与 --subsection 一起使用` |
| 指定小节不存在 | 输出 Critical/P0 `未找到小节`；不回退到相邻单元 |
| current 无合格段 | `current_lead_status=no_eligible_paragraph`；三码均不产出 |
| prev/next 无合格段 | 对应只读部件缺省并记录状态；抑制依赖该证据侧的 IN/OUT |
| 第一/最后单元 | `boundary=first/last`；缺失方向的观察不产出 |
| 窗口 index 越界（内部调用） | `_build_context_window` 抛 `IndexError` |

## 5. Good / Base / Bad Cases

- Good：book 根为 `\chapter`、article 根为 `\section` 时，都按深度得到真实 `x.x.x`；多文件
  坐标指向 `chapters/*.tex`。
- Base：文档没有有效 depth-3，返回固定声明和空观察集，不把 depth-2 当小节。
- Bad：编号章之后出现 `\chapter*`，仍沿用旧章计数给其子标题编号；这是被禁止的父链继承。
- Bad：窗口正文或相邻小节完整内容进入报告；窗口只能输出坐标与状态。

## 6. Tests Required

- book/article 两类根命令分别锁定期望编号序列；`--first-chapter`、星号根/父标题和无 depth-3
  必须有独立回归。
- 多文件 fixture 锁定 `source_file` 与文件内行号，且扫描源文任意连续 20 字，确认窗口输出
  不含正文片段。
- 锁定 current/prev/next 无合格段、跨父节 `parent_lead`、first/last boundary、三码命中与
  干净反例，以及连续 2/3 单元升级边界。
- 锁定术语文件缺失、字段缺失、字段非法三种逐字段回退。
- 公开资源变化后运行单技能/全量 resource sync、双语 contract、docs build 与 `just ci`。

## 7. Wrong vs Correct

### Wrong

```python
# 星号根只跳过当前标题，旧 counters 仍可被其子标题复用。
if starred:
    continue
```

### Correct

```python
if starred and depth == 1:
    counters[1:] = [0, 0]
    root_numbered = False
    parent_numbered = False
    continue

if depth == 3 and not (root_numbered and parent_numbered):
    continue
```

质量门：

```powershell
uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/test_subsection_context.py -q
uv run python -X utf8 docs/scripts/check_resource_sync.py --skill latex-thesis-zh
uv run python -X utf8 docs/scripts/check_resource_sync.py
just doc-build
just ci
git diff --check
```
