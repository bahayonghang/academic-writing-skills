# 共用语义契约：小节单元与三元上下文窗口

本文件是两个子任务共同实现的唯一契约来源。子任务不得各自定义单元或窗口语义。

## 1. 小节单元（subsection unit）

### 1.1 深度而非命令

`x.x.x` 在两类文档里对应不同的 LaTeX 命令：

| 文档类型                               | 根标题     | `x.x.x` 对应命令 |
| -------------------------------------- | ---------- | ---------------- |
| 中文学位论文（book 类，有 `\chapter`） | `\chapter` | `\subsection`    |
| 会议/期刊论文（article 类）            | `\section` | `\subsubsection` |

因此单元不能绑定命令。`parsers.py` 的 `HEADING_LEVELS` 是命令级映射
（`chapter=1, section=2, subsection=3, subsubsection=4`），需要在其上再算一层深度：

```
root_level = min(h["level"] for h in headings)
depth(h)   = h["level"] - root_level + 1
```

**小节单元 = `depth == 3` 的标题及其正文，直到下一个 depth ≤ 3 的标题为止。**

**无 depth-3 时不回退**（TPR-04 的产品决定）。文档不存在 `depth == 3` 标题时，两侧一律：

- 单元列表为空，不产出任何 `S-CTX-*` 观察；
- 输出一行声明。zh 侧为报告首行注释，audit 侧写入新建
  `subsection_index.json` 的顶层 `subsection_index_status` 字段：

  ```
  % 小节级：本文档无 depth-3 标题，未产出小节级观察。
  ```

  ```json
  {"subsection_index_status": "no_depth3_headings"}
  ```

  `section_index.json` 继续保持既有 JSON 数组形态和逐项 schema，不增加 metadata sentinel，
  也不改为 `{sections: [...]}` envelope。该兼容性决定由用户在 2026-08-30 实施阶段确认：
  合法 JSON 数组无法同时承载命名顶层字段，而现有 CLI、报告器与 agent 都直接消费数组。

取消原「回退到最大 depth（下限 2）」的写法。理由：源需求是 `x.x.x`；depth-2 单元在 zh 侧
已由 S1 / 章引言检查覆盖，回退会让「下沉到 x.x.x」在验收上退化为 x.x，且 identifier 是
两段还是三段无法定义。

### 1.1.1 单元的来源定位（TPR-01）

单元标识不只是编号，还必须能定位到**源文件与文件内行号**，否则多文件论文上
`Read(offset, limit)` 会读错文件。

- 入口文档若通过 `\include` / `\input` 引入正文，两侧都必须先装配再枚举标题。
  zh 侧用 `latex-thesis-zh/scripts/tex_loader.py`；audit 侧用
  `academic-writing-skills/paper-audit/scripts/tex_loader.py` 的 `assemble()`
  （`:167-171`，携带 assembled-line → source 的 origin map）。
- 标题枚举走 `extract_headings()` 全量遍历，**不经过 `split_sections()`**。
  `split_sections()` 只保留可分类的语义 section，无关键词的正文章会被丢弃
  （`academic-writing-skills/paper-audit/scripts/parsers.py:60-65` 的 `chapter_ranges` docstring
  记录了这一既有差异）。
- 每个单元记录两组坐标：`assembled_start` / `assembled_end`（装配后全局行号，用于内部计算）
  与 `source_file` / `source_start` / `source_end`（origin map 映射回的文件内行号，
  用于对外输出与 `Read`）。窗口文件对外只暴露源坐标。

### 1.2 编号推导

按 depth 维护三个计数器，遇到标题时重置更深层计数器。`\section*` 一类带 `*` 的无编号
标题不计数、不构成单元。zh 侧 `--first-chapter N` 覆盖 depth-1 计数器初值，语义与
`analyze_logic.py` 现有 `--first-chapter` 一致。

编号格式为点分十进制字符串，例如 `2.1.1`。该字符串是两个 skill 之间唯一的单元标识。

### 1.3 排除区

沿用 `P-ARC` 的既有边界，不新增例外：`abstract`、`conclusion`、`acknowledgment`、
`appendix`、`organization`、`summary` 所属范围内的单元不进入小节级检查。

## 2. 三元上下文窗口

### 2.1 prev / next 选取

`prev` 与 `next` 是文档顺序上相邻的同 depth 单元，**允许跨父节**。

字段级类型见 §2.4。`same_parent` 是逐方向的两个布尔值，不是单值。

当 `prev` 与当前单元不同父（`same_parent.prev == false`）时，窗口额外附上当前单元父标题的
导语区间 `parent_lead`（父标题行到其第一个子标题行之间的可见正文）。跨节交接的真正承接位置
在父节导语，不在上一个小节的末段。

### 2.2 窗口内容与合格段（TPR-05）

| 部件           | 取值                        |
| -------------- | --------------------------- |
| `prev.tail`    | prev 单元的最后一个合格段   |
| `current.full` | 当前单元全部行              |
| `next.head`    | next 单元的第一个合格段     |

**不能沿用 `_arc_is_eligible`。** 实际实现排除 `is_heading_lead`
（`academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py:1372-1379`），而标题后的第一个
正文段正是小节级分析要看的段（`:1247-1258` 把它标为 `is_heading_lead`）。沿用会让
`current` 首段与 `next.head` 全部落空。

因此定义一套独立的 canonical eligibility，两侧逐条一致：

| 条件 | 取值 |
| --- | --- |
| 汉字数下限 | `>= 20`，常量 `SUBSECTION_CONTEXT_MIN_HAN`。低于 `PARAGRAPH_ARC_MIN_HAN = 40`，因为小节首段常为一到两句的定位句 |
| `is_heading_lead` | **不排除**（与 `P-ARC` 相反，这是有意分歧） |
| `in_item` | 排除 |
| `ends_with_env` | 排除 |
| 排除区 section | 排除，集合同 §1.3 |
| 非中文正文（英文段、纯公式段） | 排除；判定为可见文本中汉字占比 `< 0.30` |

汉字下限与占比阈值是**两侧共用的同一个数值**，不允许「因语种不同而不同」。paper-audit 侧
处理英文论文时，同一条件用「可见字符数 `>= 60`」作为汉字下限的等价投影，该投影写在
§2.4 的 schema 中，不由实现者自行决定。

### 2.3 无合格邻段时的窗口语义（TPR-05）

| 情形 | 窗口 | finding |
| --- | --- | --- |
| prev 单元存在但无合格段 | `prev.tail = null`，附 `prev_tail_status: "no_eligible_paragraph"` | `S-CTX-IN` 不产出 |
| next 单元存在但无合格段 | `next.head = null`，附 `next_head_status: "no_eligible_paragraph"` | `S-CTX-OUT` 不产出 |
| current 无合格段 | `current.full` 仍输出全部行；`current_lead_status: "no_eligible_paragraph"` | 三码均不产出 |
| `boundary == "first"` | 无 `prev` 部件 | `S-CTX-IN` 不产出 |
| `boundary == "last"` | 无 `next` 部件 | `S-CTX-OUT` 不产出 |

窗口区间数量**不固定**。原「总是三个、跨父节四个」的说法作废；验收改为断言各部件的
存在性与 `*_status` 取值，见父 `prd.md` 的 AC-P-05。

### 2.4 字段级 schema（TPR-03）

窗口对象是两侧唯一的共享数据结构。字段名、类型与可空性如下，不允许各自变形。

```json
{
  "subsection_id": "2.1.1",
  "title": "<标题可见文本>",
  "depth": 3,
  "parent_id": "2.1",
  "source_file": "chapters/method-a.tex",
  "editable": {
    "part": "current",
    "source_start": 12,
    "source_end": 55,
    "status": "ok"
  },
  "read_only": [
    {
      "part": "prev.tail",
      "subsection_id": "2.0.3",
      "source_file": "chapters/method-a.tex",
      "source_start": 4,
      "source_end": 9,
      "status": "ok"
    },
    {
      "part": "next.head",
      "subsection_id": "2.1.2",
      "source_file": "chapters/method-a.tex",
      "source_start": 57,
      "source_end": 61,
      "status": "ok"
    },
    {
      "part": "parent_lead",
      "subsection_id": null,
      "source_file": "chapters/method-a.tex",
      "source_start": 2,
      "source_end": 3,
      "status": "ok"
    }
  ],
  "same_parent": { "prev": false, "next": true },
  "boundary": "",
  "prev_id": "2.0.3",
  "next_id": "2.1.2"
}
```

约定：

1. `same_parent` 是 `{prev: bool|null, next: bool|null}`；相邻单元不存在时该方向为 `null`。
2. `parent_lead` 是 `read_only` 的一个合法 `part`，只在 `same_parent.prev == false` 时出现。
3. `status` 取值 `"ok" | "no_eligible_paragraph" | "absent"`。`read_only` 中不出现
   `status == "absent"` 的项，缺失的部件直接不进数组。
4. `read_only` 数组长度为 0~3，由 §2.3 决定；顺序固定为 `prev.tail`、`parent_lead`、`next.head`。
5. **cursor 字段是派生而非存储**：`prev_id`、`next_id`、`same_parent`、`boundary` 由有序单元
   列表推导，实现侧的 cursor 数据结构只存 §1 的单元自身字段。窗口对象是派生结果的序列化形态。
   两个子任务的 PRD 不得再要求 cursor item 内含相邻字段。

### 2.5 finding 出参投影（TPR-03）

两个 skill 的出参形态不同，共享的是**语义标签**，不是同一条 JSON。投影表如下。

| 面 | 载体 | 码 | 来源标记 | 严重度 | 证据侧字段 |
| --- | --- | --- | --- | --- | --- |
| zh 脚本 | `analyze_logic.py` 的 `% ` 注释块 | `S-CTX-IN/OUT/ROLE` | `[Script]` | `Info` / `P3` + `Meaning-Check: NEEDS-LLM` | `context_sides` 写在注释行内，取值见下 |
| paper-audit | `ISSUE_SCHEMA.md` 的 JSON issue | 同码，写在 `title` 前缀 | `source_kind: "llm"` | `severity: "minor"`（可升 `"moderate"`） | 可选字段 `subsection_id` + `context_sides` |

`source_kind` 与 `severity` 的取值受 `ISSUE_SCHEMA.md:5-14,30-38` 约束，只能是
`script|llm` 与 `major|moderate|minor`。audit 侧一律 `llm`：既有
`.trellis/spec/academic-writing-skills/paragraph-arc-audit-contract.md:5-8` 已把同类审稿侧观察
定义为人工观察而非脚本 finding，S-CTX 沿用该判定，audit 侧**不新增脚本 fallback issue 生成器**。

`context_sides` 是**列表**，不是单值。原 `context_side: prev|current|next` 作废，理由是
`S-CTX-IN` / `S-CTX-OUT` 本身同时用到 current 与一侧邻段。取值域：

```
["current", "prev.tail"] | ["current", "next.head"] | ["current", "parent_lead"] | ["current"]
```

| 码 | `context_sides` |
| --- | --- |
| `S-CTX-IN`（同父） | `["current", "prev.tail"]` |
| `S-CTX-IN`（跨父） | `["current", "parent_lead"]` |
| `S-CTX-OUT` | `["current", "next.head"]` |
| `S-CTX-ROLE` | `["current"]` |

### 2.6 只读 / 可改边界

窗口输出**行号区间，不复制正文**。理由有二：报告不因携带上下文而膨胀；
`paper-audit` 的 `POLISH_GUIDE.md` 既有惯例就是让 Mentor 用 `Read(offset, limit)` 取正文。

只有 `current` 可以产出改写建议。`prev.tail`、`next.head`、`parent_lead` 一律只读，
仅作为 finding 的证据来源。这一条是本任务的核心授权边界。

**唯一的协议句真相源**（TPR-06）：

```
只有 current 可产出改写建议；prev.tail、next.head、parent_lead 一律只读，仅作证据。
```

该句的规范拷贝存放在
`academic-writing-skills/latex-thesis-zh/references/writing/subsection-context-zh.md`。
paper-audit 侧的镜像文件唯一指定为
`academic-writing-skills/paper-audit/references/SUBSECTION_CONTEXT_PROTOCOL.md`（新建）。
`REVIEW_LANE_GUIDE.md`、`SUBAGENT_TEMPLATES.md`、`agents/section_reviewer_agent.md`、
`POLISH_GUIDE.md` **只交叉引用该文件，不各自复制协议句**。

字符串锁不能证明模型输出遵守该边界，行为验收见父 `prd.md` 的 AC-P-07。


## 3. Finding 码

**三个**新码，前缀 `S-CTX-`，避开已占用的 `P-ARC-`、`E-`、`T-`、`CC-`、`YS-` 命名空间。

| 码           | 可复算信号                                                                               | 人工复核问题                             |
| ------------ | ---------------------------------------------------------------------------------------- | ---------------------------------------- |
| `S-CTX-IN`   | current 首段未命中显式承接标记，且首段与 `prev.tail` 末句的端点 token Jaccard `< 0.0200` | 本小节是否需要承接上一小节的结论或产出？ |
| `S-CTX-OUT`  | current 末段未命中前瞻或收束标记，且 `next.head` 首句未命中回指标记                      | 本小节是否需要为下一小节交出输入或问题？ |
| `S-CTX-ROLE` | current 首段未出现指向父节的定位标记，也未复用父标题关键词                               | 本小节在父节 `x.x` 中承担什么角色？      |

### 3.0 已移除：`S-CTX-DUP`（TPR-07）

原第四码 `S-CTX-DUP`（相邻小节复述）**本轮不交付**。

理由：它需要一个 Jaccard 上阈值 `T_dup`，而可用于标定的证据不存在——既有
`academic-writing-skills/latex-thesis-zh/evals/fixtures/thesis-project/` 没有 depth-3 单元，
本任务新增的 fixture 是合成文本，在其上取出的分布不能代表真实论文。凭合成样本固定一个
上阈值等同于凭直觉取值。

处置：本轮把合同缩减为三码。四码的全部引用（父 R1/R4、A 的 R-A2 与 AC、B 的前置、
契约测试的码集）同步改为三码。若日后要补 `S-CTX-DUP`，另立任务，并先取得真实论文样本。

### 3.1 阈值

下阈值复用 `PARAGRAPH_ARC_LINK_THRESHOLD = 0.0200`，比较为严格小于（`== 0.0200` 通过）。
复用而非新设，理由是同一 Jaccard 量表上再引入第二个下阈值会产生两套判据。

本轮不引入任何需要标定的新阈值。`SUBSECTION_CONTEXT_MIN_HAN = 20`（§2.2）是构造性下限，
不是从数据标定出来的判据；它的作用是排除单句定位段以下的碎片，取值理由写进 references。

### 3.2 严重度与升级

三码单项在 zh 侧一律 `[Script]` + `Info` + `P3` + `Meaning-Check: NEEDS-LLM`，与 `P-ARC` 的
既定取舍一致；在 audit 侧按 §2.5 投影为 `source_kind: "llm"` + `severity: "minor"`。

升级规则：同一父节内连续 3 个单元同时报 `S-CTX-IN` 与 `S-CTX-OUT` 时，额外生成一条
`S-CTX-IN+OUT` 的 `Minor` / `P2`（audit 侧 `severity: "moderate"`）汇总观察，单项仍不升级。
连续数复用 `PARAGRAPH_ARC_DOUBLE_MISSING_RUN = 3`。

### 3.3 与既有检查器的边界

| 领域                     | 既有 owner                                  | S-CTX 的处置         |
| ------------------------ | ------------------------------------------- | -------------------- |
| 段内首句/末句/展开形态   | `P-ARC-LEAD` / `P-ARC-CLOSE` / `P-ARC-FLAT` | 不重复报告           |
| 同一标题内相邻段接口     | `P-ARC-LINK`（不跨标题）                    | 只做跨标题部分       |
| 章引言承上启下           | S1 / `_check_chapter_intro`                 | depth-1 不进入 S-CTX |
| 句级表达、标点、数值单位 | `check_style_zh.py` 的 `E-*`                | 不触碰               |
| AI 痕迹、句长均匀度      | `deai`                                      | 不触碰               |
| 论断强度                 | `over-claim-guard.md`                       | 不触碰               |

## 4. 术语真相源

新增 `academic-writing-skills/latex-thesis-zh/references/writing/subsection-context-terms.yaml`，
三组标记：承接（`承接`/`回指`）、前瞻（`交棒`）、定位（`本节`/`本小节`/`上一小节` 等）。
YAML 缺失或字段无效时按字段回退同值内置表，形态与 `paragraph-arc-terms.yaml` 一致。

paper-audit 不复制该 YAML。audit 侧的 S-CTX 是 LLM 观察（§2.5），不做词表匹配，
只按 mirror 文件中的三码语义与人工复核问题工作。

## 5. 跨技能一致性锁（TPR-06）

新增 `tests/contracts/test_subsection_context_contract.py`，仿
`tests/contracts/test_paragraph_arc_audit_contract.py` 的形态。

**真相源与镜像**（两个文件，不是三个）：

| 角色 | 文件 |
| --- | --- |
| canonical | `academic-writing-skills/latex-thesis-zh/references/writing/subsection-context-zh.md` |
| mirror | `academic-writing-skills/paper-audit/references/SUBSECTION_CONTEXT_PROTOCOL.md` |

`agents/section_reviewer_agent.md`、`REVIEW_LANE_GUIDE.md`、`SUBAGENT_TEMPLATES.md`、
`POLISH_GUIDE.md` 只允许交叉引用 mirror 文件的路径，不复制协议句；契约测试断言这四个文件
**不含**协议句正文，只含该路径字符串。这样「谁是真相源」在测试里是可判定的。

**比较规则**：取两个文件中被 `<!-- S-CTX-CONTRACT:BEGIN -->` / `<!-- S-CTX-CONTRACT:END -->`
标记包裹的块，各自经 `re.sub(r"\s+", " ", text).strip()` 规范化后**必须完全相等**。
父 `prd.md` 与两个子任务中原有的「一字不差」措辞统一改为「规范化空白后完全相等」，
不再存在两种强度。

锁定内容：

1. 三码集合 `{S-CTX-IN, S-CTX-OUT, S-CTX-ROLE}` 在契约块内出现，且四码时代的 `S-CTX-DUP`
   **不出现**（负向断言，防止移除不彻底）。
2. §2.6 的协议句在契约块内出现。
3. §1.1 的 depth 定义句与 §1.1 的「无 depth-3 不回退」声明句在契约块内出现。
4. `subsection_context_polish` 同名出现在 `REVIEW_LANE_GUIDE.md`、`SUBAGENT_TEMPLATES.md`
   与 `academic-writing-skills/paper-audit/scripts/audit.py` 的
   `FOCUS_TO_ALLOWED_LANES["full"]` / `["logic"]`（后者用导入后读常量，不用字符串匹配）。

## 6. 不做什么

- 不让脚本自动改写正文。三码全部是观察，改写由 LLM 层按窗口执行。
- 不给 `analyze_logic.py` 加 `--json`（当前无此形态，不在本任务扩面）。
- 不改 `split_sections()` 的既有语义与返回类型；小节层是新增的并列结构，且**不经过**它枚举标题（§1.1.1）。
- 不动 `parsers.py` 的四份副本对齐关系（`tests/contracts/test_parsers_alignment.py` 锁定）；
  深度计算放在调用侧，不进 `parsers.py`。
- 本轮不交付 `S-CTX-DUP`（§3.0）。
- audit 侧不新增脚本 fallback issue 生成器（§2.5）。
