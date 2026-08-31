# 设计：latex-thesis-zh 小节游标与跨标题接口检查

父任务 `design.md` 是语义契约来源。本文件只写 zh 侧的实现落点。
变更清单以 `prd.md` 的「变更清单」表为准；本文件不再声称改动只在一个文件内（TPR-09）。

## 1. 代码落点

主要改动在 `academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py`，位置紧随现有
段落弧线区块（`_check_paragraph_arc` 之后）。此外还涉及新增 references、YAML、fixture、
docs 页面、manifest、`evals.json` 与测试文件，逐项见 `prd.md` 变更清单。

### 1.1 复用清单

| 复用对象 | 用途 |
| --- | --- |
| `parser.extract_headings(content)` | 取 `level` / `title` / 行号，算 depth |
| `academic-writing-skills/latex-thesis-zh/scripts/tex_loader.py` | 装配 `\include` / `\input` 并保留 origin map |
| `_split_arc_paragraphs` | 段落切分，用于取 `prev.tail` / `next.head` / current 首末段 |
| `_arc_finding` | finding 渲染，保持与 `P-ARC` 同形态 |
| `_zh_loc` | 中文行号定位串 |
| `_arc_link_missing` 的 Jaccard 计算 | 抽出为可复用函数，不改 `P-ARC` 行为 |
| `PARAGRAPH_ARC_LINK_THRESHOLD` | `S-CTX-IN` 的下阈值 |
| `PARAGRAPH_ARC_DOUBLE_MISSING_RUN` | 升级连续数 |
| `_load_paragraph_arc_terms` | 复制为 `_load_subsection_context_terms`，读新 YAML |

**不复用 `_arc_is_eligible`**（父 `design.md` §2.2 / TPR-05）。实际实现排除
`is_heading_lead`（`analyze_logic.py:1372-1379`），而小节首段正是被 `:1247-1258` 标为
`is_heading_lead` 的那一段。沿用会让 `current` 首段与 `next.head` 全部落空。

Jaccard 抽取是唯一一处触碰既有代码的改动：把 `_arc_link_missing` 内联的端点 token Jaccard
提成 `_endpoint_jaccard(left_text, right_text) -> float | None`，`_arc_link_missing` 改为调用它。
行为等价，由既有 `P-ARC` 测试守住。

### 1.2 新增结构

```python
SUBSECTION_CONTEXT_MIN_HAN = 20
SUBSECTION_CONTEXT_MIN_HAN_RATIO = 0.30


@dataclass
class SubsectionUnit:
    subsection_id: str        # "2.1.1"
    title: str
    depth: int
    parent_id: str            # "2.1"
    source_file: str          # "chapters/method-a.tex"
    source_start: int         # 文件内行号，1-based，标题行
    source_end: int
    assembled_start: int      # 装配后全局行号
    assembled_end: int
    section_scope: str        # split_sections 归属键，仅用于排除区判定
```

`prev_id` / `next_id` / `same_parent` / `boundary` **不进 dataclass**，由有序列表在窗口构建时
派生（父 `design.md` §2.4 约定 5；解决 TPR-03 中 PRD 与 dataclass 的冲突）。

游标构建：`_build_subsection_cursor(assembled, parser, sections, first_chapter) -> list[SubsectionUnit]`，
纯函数、无 IO，输入是已装配的文档对象（含 origin map）。

### 1.3 装配与来源坐标

```python
doc = tex_loader.assemble(entry_path)      # 已有能力
content = doc.content
origin = doc.origin_map                    # assembled line -> (source_file, source_line)
```

标题枚举在 `content` 上做，随后每个单元的 `assembled_*` 经 `origin` 映射为
`source_file` / `source_*`。对外输出（`--emit-window`、finding 定位）一律用源坐标。

实现前须确认 `latex-thesis-zh/scripts/tex_loader.py` 暴露的 origin map 字段名与
paper-audit 副本是否一致；不一致时按本 skill 副本的实际字段写，不改脚本。

### 1.4 深度、编号与无 depth-3 处置

```
root_level = min(levels)                       # 无标题 -> 返回空列表
if 3 not in present_depths: 返回空列表 + 声明   # 不回退（父 design.md §1.1）
```

声明文本固定为：

```
% 小节级：本文档无 depth-3 标题，未产出小节级观察。
```

编号：三个计数器 `[c1, c2, c3]`，遇 depth-k 标题时 `c_k += 1` 并把更深计数器清零。
`--first-chapter N` 把 `c1` 初值设为 `N - 1`。标题命令带 `*` 时跳过。

`extract_headings` 是否保留 `*` 信息需在实现前确认：`parsers.py:147` 的正则是
`\\(?P<command>chapter|section|subsection|subsubsection|paragraph)\*?`，`*` 被匹配但未捕获。
若 heading dict 未带该标记，在 `analyze_logic.py` 侧按行号回读原始行判断，不改 `parsers.py`。

## 2. canonical eligibility

```python
def _ctx_is_eligible(paragraph: ArcParagraph) -> bool:
    visible = paragraph.visible
    han = _arc_han_count(visible)
    return (
        han >= SUBSECTION_CONTEXT_MIN_HAN
        and han / max(len(visible), 1) >= SUBSECTION_CONTEXT_MIN_HAN_RATIO
        and paragraph.section not in _ARC_EXEMPT_SECTIONS
        and not paragraph.in_item
        and not paragraph.ends_with_env
    )
```

与 `_arc_is_eligible` 的唯一有意分歧是不排除 `is_heading_lead`，该分歧写进
`references/writing/subsection-context-zh.md` 与 `paragraph-arc-zh.md` 的交叉说明。

## 3. 窗口构建

```python
def _build_context_window(units, index, paragraphs) -> dict
```

返回父 `design.md` §2.4 的窗口对象。部件缺失与 `*_status` 按 §2.3：

- prev/next 单元不存在 -> 该部件不进 `read_only`，`boundary` 置 `"first"` / `"last"`。
- 单元存在但无合格段 -> 该部件不进 `read_only`，在返回对象顶层记
  `prev_tail_status` / `next_head_status` / `current_lead_status` = `"no_eligible_paragraph"`。
- `same_parent.prev == false` 时追加 `parent_lead`；`parent_lead` 自身无合格内容时同样省略。

## 4. 三个检查器

```python
def _check_subsection_context(units, windows, terms) -> list[str]
```

| 码 | 判定 | 不产出条件 |
| --- | --- | --- |
| `S-CTX-IN` | current 首段首句未命中承接标记，且 `_endpoint_jaccard(证据侧末句, current 首段首句) < 0.0200` | `boundary == "first"`，或证据侧 `status != "ok"`，或 `current_lead_status != "ok"` |
| `S-CTX-OUT` | current 末段末句未命中前瞻/收束标记，且 `next.head` 首句未命中回指标记 | `boundary == "last"`，或 `next_head_status != "ok"` |
| `S-CTX-ROLE` | current 首段未命中定位标记，且与 parent 标题关键词无交集 | `current_lead_status != "ok"` |

`S-CTX-IN` 的证据侧：`same_parent.prev == true` 用 `prev.tail`；`false` 用 `parent_lead`，
`parent_lead` 缺失时回退 `prev.tail`。实际使用的证据侧写进 finding 的 `context_sides`。

升级：按 `parent_id` 分组，组内连续 3 个单元同时报 IN 与 OUT -> 一条 `S-CTX-IN+OUT`（Minor/P2）。

## 5. CLI 装配

```python
cli.add_argument("--subsection-context", action="store_true", ...)
cli.add_argument("--subsection", help="限定单个小节编号，如 2.1.1")
cli.add_argument("--emit-window", action="store_true", ...)
```

`analyze()` 增三个形参，位置在 `paragraph_arc` 之后，保持既有位置参数调用不破。
`--emit-window` 要求同时传 `--subsection`，否则 `parser.error`。

`--emit-window` 输出示例（部件数量随 §2.3 变化，不固定）：

```
% 小节窗口 2.1.1《XXX》
% current    : chapters/method-a.tex L12-L55   [可改]
% prev.tail  : chapters/method-a.tex L4-L9     [只读]
% next.head  : chapters/method-a.tex L57-L61   [只读]
% next.head  : (无合格段) status=no_eligible_paragraph
```

## 6. 术语 YAML

`academic-writing-skills/latex-thesis-zh/references/writing/subsection-context-terms.yaml`：

```yaml
inbound:   [在此基础上, 针对上述, 基于此, 前述, 上一小节, 承接]
outbound:  [为后续, 为下一, 提供输入, 由此可得, 综上]
locating:  [本节, 本小节, 下面, 以下]
```

具体词条按 `paragraph-arc-terms.yaml` 的规模控制，不做词表扩张。
加载函数缺失字段时按字段回退内置同值表。

## 7. 兼容性

- 三个新开关默认 `False`，`analyze()` 在全 `False` 时不进入任何新代码路径。
- 既有位置参数顺序不变，新形参追加在尾部。
- 不新增外部依赖。
- 报告仍是 `% ` 注释块行列表，无新输出格式。
