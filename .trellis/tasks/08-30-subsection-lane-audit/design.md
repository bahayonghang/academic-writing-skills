# 设计：paper-audit 小节级审阅通道与窗口装配

父任务 `design.md` 是语义契约来源。本文件只写 paper-audit 侧的落点。
变更清单以 `prd.md` 的「变更清单」表为准。

## 1. 装配与小节索引（TPR-01）

### 1.1 装配

`academic-writing-skills/paper-audit/scripts/prepare_review_workspace.py` 现在只导入
`read_text_robust`（`:19-27`），并把单文件原始文本交给 `build_section_index`（`:223-253`）。

改为：`.tex` 入口先调
`academic-writing-skills/paper-audit/scripts/tex_loader.py` 的 `assemble(entry)`（`:167-171`），
拿到 `AssembledDocument`（含 `content` 与 assembled-line → source 的 origin map）。
`.typ` / `.pdf` 保持现有读取路径，小节层直接降级（§1.4）。

既有 section 级流程仍用原来的 content 来源，不受影响；小节层是并列的新数据流。

### 1.2 全量标题枚举

```python
def build_subsection_units(assembled, parser) -> list[dict]
```

- 在装配后的 `content` 上调 `parser.extract_headings()`，**全量遍历**。
- 不经过 `split_sections()`：它只保留可分类的语义 section，无关键词标题会被丢弃
  （`academic-writing-skills/paper-audit/scripts/parsers.py:60-65`）。
- `root_level` 在**全文档**范围统计，编号计数器也在全文档范围推进，保证跨 section 编号连续。
- 深度、编号、`*` 标题跳过、排除区规则与父 `design.md` §1 逐条一致。

深度计算与 zh 侧**不共享代码**——两个 skill 的 `scripts/` 是并列副本，仓库既有约定是各自
持有副本、由契约测试锁定一致性（同 `parsers.py` 的处理方式）。

### 1.3 坐标

每个单元同时记 `assembled_start/end` 与 `source_file` + `source_start/end`。
对外产物（`subsection_index.json`、窗口文件）只暴露源坐标。

### 1.4 降级

| 输入 | `subsection_index_status` | 单元列表 |
| --- | --- | --- |
| `.tex`，有 depth-3 | `"ok"` | 非空 |
| `.tex`，无 depth-3 | `"no_depth3_headings"` | 空 |
| `.typ` / `.pdf` | `"unsupported_format"` | 空 |

该字段写在 `section_index.json` 顶层（伴随字段）与 `subsection_index.json` 顶层两处，取值相同。

## 2. 产物落点（TPR-08）

真实类名是 `WorkspaceLayout`（`academic-writing-skills/paper-audit/scripts/paths.py:34-39`），
不是 `ReviewLayout`。原设计写错，此处更正。

在 `WorkspaceLayout` 上新增：

```python
@property
def subsection_index(self) -> Path:      # artifacts/data/subsection_index.json
    return self.data_dir / "subsection_index.json"

@property
def windows_dir(self) -> Path:           # artifacts/windows/
    return self.artifacts / "windows"

def window_file(self, subsection_id: str) -> Path:
    return self.windows_dir / f"{subsection_id}.json"
```

`windows_dir` 加入 `WorkspaceLayout` 的目录创建列表（现 `paths.py:156` 附近的
`sections_dir` 等同一处）。

工作区路径形态：`{--output-dir}/{slug}/artifacts/...`，`slug` 由
`prepare_review_workspace.py:30-33` 的 `slugify(title or source.stem)` 得到
（同文件 `:237-239`）。`section_index.json` 的既有落点是
`artifacts/data/section_index.json`（`paths.py:96-97`）。

**CLI 更正**：`prepare_review_workspace.py` 只接受 `input`、`--output-dir`、`--overwrite`
（`:302-318`）。`--review-dir` 属于 `audit.py` 的 checkpoint 路径，不是这个脚本的参数。
原 `implement.md` S11 的命令写错，见新 S12。

## 3. 窗口文件

每个单元写一份 `artifacts/windows/<subsection_id>.json`，内容即父 `design.md` §2.4 的窗口对象。

合格段判定用父 `design.md` §2.2 的 canonical eligibility。数值与 zh 侧相同：
`SUBSECTION_CONTEXT_MIN_HAN = 20`、汉字占比 `>= 0.30`；英文正文用契约中写明的等价投影
（可见字符数 `>= 60`）。**不允许实现者自行调整下限**（TPR-05）。

部件缺失与 `*_status` 语义按父 `design.md` §2.3；`read_only` 数组长度 0~3，顺序固定为
`prev.tail`、`parent_lead`、`next.head`。

## 4. lane 接入调度链（TPR-02，Route A）

### 4.1 deep-review

| 落点 | 改动 |
| --- | --- |
| `audit.py:224-264` `FOCUS_TO_ALLOWED_LANES` | `"full"` 与 `"logic"` 集合加入 `"subsection_context_polish"` |
| `audit.py:275-291` `ROLE_TO_REVIEW_LANES` | `"logic"` 集合加入同名 lane |
| `audit.py:951-1002` `_write_lane_outputs` | 不新增 fallback 生成器；该 lane 只经 `allowed_lanes` 过滤进入调度 |
| `checkpoint.py` | 无改动，沿用 `mark_lane_completed` / `completed_lanes` |

`_selected_lanes_for_focus`（`:917-919`）与 `_load_completed_lanes`（`:922-929`）不改，
lane 加入常量后自动生效。

lane 的产物由 LLM subagent 写入 `artifacts/comments/subsection_context_polish.json`，
形态遵循 `ISSUE_SCHEMA.md`，`source_kind: "llm"`（父 `design.md` §2.5）。
**不写脚本 fallback issue**：`.trellis/spec/academic-writing-skills/paragraph-arc-audit-contract.md:5-8`
已把同类审稿侧观察定义为人工观察而非脚本 finding。

因此「lane 已启用」的可测证据是：常量集合包含它、窗口文件已生成、checkpoint 能记录它，
**不是**自动出现 issue JSON。

### 4.2 polish

`audit.py:2418-2425` 的 polish 路径进 `run_polish_precheck`；`:2330-2346` 组装
`precheck_data` 并经 `_write_state_file`（`:2235`）落盘。

改动：`precheck_data` 增

```json
"subsection_windows": {
  "status": "ok",
  "index": "artifacts/data/subsection_index.json",
  "units": [
    {"subsection_id": "2.1.1", "window": "artifacts/windows/2.1.1.json"}
  ]
}
```

`status` 复用 §1.4 的三个取值。无小节层时 `units` 为空数组，Mentor 编排回退到既有章节切分。

## 5. 协议镜像与一致性锁（TPR-06）

canonical 与 mirror 两个文件见父 `design.md` §5。mirror 文件为新建
`academic-writing-skills/paper-audit/references/SUBSECTION_CONTEXT_PROTOCOL.md`。

`tests/contracts/test_subsection_context_contract.py` 断言：

1. 两个契约块经 `re.sub(r"\s+", " ", text).strip()` 规范化后**完全相等**。
   父任务与子任务中原「一字不差」的措辞统一改为此规则，不再有两种强度。
2. 契约块内含三码 `{S-CTX-IN, S-CTX-OUT, S-CTX-ROLE}`；`S-CTX-DUP` **不出现**（负向断言）。
3. 契约块内含协议句、depth 定义句、「无 depth-3 不回退」声明句。
4. `REVIEW_LANE_GUIDE.md` / `SUBAGENT_TEMPLATES.md` / `agents/section_reviewer_agent.md` /
   `POLISH_GUIDE.md` 含 mirror 文件路径字符串，且**不含**协议句正文。
5. 从 `audit.py` 导入 `FOCUS_TO_ALLOWED_LANES` 与 `ROLE_TO_REVIEW_LANES` 读常量，
   断言 lane 在 `full` / `logic` 中、不在 `methodology` / `literature` 中（读常量，不做字符串匹配）。

## 6. POLISH_GUIDE 改造

现文（`academic-writing-skills/paper-audit/references/POLISH_GUIDE.md` 末段）：

```
- Mentor receives ONLY the target section via Read(offset=start-1, limit=end-start+1)
- For sections > 1200 words: orchestrator splits at subsection boundaries,
  spawns two Mentor calls
```

改为：Mentor 以小节为单元接收窗口，坐标取自 `artifacts/windows/<id>.json`；
`current` 可改，`prev.tail` / `next.head` / `parent_lead` 只读（协议句只引用 mirror 文件路径）；
单个小节仍 > 1200 词时再按段落边界切，切出的两半共享同一份 prev / next 上下文。
无小节层时（`status != "ok"`）回退到既有章节切分。

## 7. ISSUE_SCHEMA

`academic-writing-skills/paper-audit/references/ISSUE_SCHEMA.md` 的 JSON 示例增两个字段，
Guidance 段增一条：

- `subsection_id`：点分十进制串，如 `"2.1.1"`；无小节层时省略。
- `context_sides`：**列表**，取值域见父 `design.md` §2.5。原单值 `context_side` 不采用。

写明 S-CTX 类 issue 的 `source_kind` 恒为 `"llm"`、`severity` 为 `"minor"`
（`S-CTX-IN+OUT` 汇总项为 `"moderate"`），受 `ISSUE_SCHEMA.md:5-14,30-38` 的枚举约束。
二者为 optional，required 列表不变，下游消费者未版本化前不得升为必填。

## 8. 兼容性

- `section_index.json` 只增一个顶层伴随字段，既有键与值不变。
- 小节索引在独立文件，下游消费者不受影响。
- 不新增 `audit.py` 的 mode 或必填参数。
- 无窗口文件时，既有 lane 与 Mentor 路径行为不变。
- `ISSUE_SCHEMA` 的两个新字段缺失时，`consolidate_review_findings.py` 与
  `diff_review_issues.py` 行为不变。
