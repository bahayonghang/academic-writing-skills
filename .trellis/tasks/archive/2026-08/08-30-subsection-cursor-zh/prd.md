# latex-thesis-zh 小节游标与跨标题接口检查

父任务：`.trellis/tasks/08-30-subsection-context-polish`
共用契约：父任务 `design.md`（单元定义与来源定位、三元窗口、canonical eligibility、
字段级 schema、出参投影、三个 `S-CTX-*` 码、只读边界与协议句真相源）

## 目标

在 `academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py` 中把分析单元从「章」下沉到
「小节」（`x.x.x`），并补上现有检查器不覆盖的跨标题接口。`P-ARC-LINK` 明确不跨标题连接段落
（`academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py:1528-1535`），本任务补的正是这块空白。

## 需求

### R-A1 小节游标

新增一个纯函数层，把文档展开为有序小节单元列表。

单元自身字段：`subsection_id / title / depth / parent_id / source_file /
source_start / source_end / assembled_start / assembled_end / section_scope`。

**相邻关系是派生的，不存进单元**（父 `design.md` §2.4 约定 5）：`prev_id`、`next_id`、
`same_parent`、`boundary` 由有序列表推导，只出现在窗口对象里。

深度按父 `design.md` §1.1 的 `depth = level - root_level + 1` 计算，不绑定 LaTeX 命令；
无 depth-3 时不回退，输出声明并返回空列表。

### R-A2 三个接口检查器

实现 `S-CTX-IN` / `S-CTX-OUT` / `S-CTX-ROLE`。**不实现 `S-CTX-DUP`**（父 `design.md` §3.0）。

输出形态与 `_arc_finding` 一致：`[Script]` + `Info` + `P3` + `Meaning-Check: NEEDS-LLM`，
附行号定位、可复算信号说明、人工复核问题，以及 `context_sides` 列表（父 `design.md` §2.5）。
升级规则见父契约 §3.2。

### R-A3 CLI

```
analyze_logic.py main.tex --subsection-context [--section <章名>] [--first-chapter N]
analyze_logic.py main.tex --emit-window --subsection 2.1.1
```

- `--subsection-context`：默认关闭的附加开关，形态对齐既有 `--paragraph-arc`。
- `--subsection <编号>`：把检查范围缩到单个单元。
- `--emit-window`：打印该单元三元窗口的部件与源坐标，**不复制正文**，供 LLM 层用
  `Read(offset, limit)` 取。部件数量按父 `design.md` §2.3 变化，不固定。
- 不传新开关时，`analyze_logic.py` 的输出逐字不变。

### R-A4 多文件装配

入口 `.tex` 通过 `\include` / `\input` 引入正文时，先用
`academic-writing-skills/latex-thesis-zh/scripts/tex_loader.py` 装配再枚举标题，
对外输出 `source_file` 与文件内行号（父 `design.md` §1.1.1）。

### R-A5 canonical eligibility

按父 `design.md` §2.2 实现 `_ctx_is_eligible`，**不复用 `_arc_is_eligible`**。
关键分歧：`is_heading_lead` 不排除。汉字下限 `SUBSECTION_CONTEXT_MIN_HAN = 20`。
无合格段时的窗口与 finding 语义按父 `design.md` §2.3。

### R-A6 术语真相源

新增 `academic-writing-skills/latex-thesis-zh/references/writing/subsection-context-terms.yaml`
（承接 / 前瞻 / 定位三组标记），形态与 `paragraph-arc-terms.yaml` 一致，YAML 缺失时按字段回退内置表。

### R-A7 references 与路由

- 新增 `academic-writing-skills/latex-thesis-zh/references/writing/subsection-context-zh.md`，
  是父 `design.md` §5 指定的 **canonical 契约文件**，含
  `<!-- S-CTX-CONTRACT:BEGIN -->` / `<!-- S-CTX-CONTRACT:END -->` 包裹的契约块。
- `academic-writing-skills/latex-thesis-zh/references/modules/logic.md` 增小节级入口与边界说明。
- `academic-writing-skills/latex-thesis-zh/SKILL.md` 的 `logic` 路由行补新旗标。
- `academic-writing-skills/latex-thesis-zh/references/writing/paragraph-arc-zh.md` 的
  「与 AXES 的关系」后补一句指向 `S-CTX-*`。

### R-A8 fixture 与测试

- **新增 depth-3 fixture**（主路径）：`evals/fixtures/subsection-context/` 多文件工程，
  含三级标题、同父节连续三小节缺进出接口、一处跨父节交接、一处单段小节、一处短段小节、
  一处列表/环境边界。
- **新增 article 类 fixture**（深度解耦）：根标题为 `\section`，`x.x.x` 落在 `\subsubsection`。
- 既有 `evals/fixtures/thesis-project/main.tex` 作为**无 depth-3** 的负向 fixture。
- fixture 内容为原创抽象文本，不含真实论文事实、数据或引用。

## 约束

1. 不改 `academic-writing-skills/latex-thesis-zh/scripts/parsers.py`。深度计算放在
   `analyze_logic.py` 调用侧，避免触发 `tests/contracts/test_parsers_alignment.py` 的四副本对齐锁。
2. 不改 `split_sections()` 的语义与返回类型，且小节枚举不经过它。
3. 不改 `SKILL.md` 的 `version`，只改 `last_updated`。
4. 新增 references 文档必须同步 `docs/resource-manifest.json`（`sourceSha256` + `en`/`zh` 页面）。
5. 不重造既有 owner 的检查，边界见父 `design.md` §3.3。
6. 本轮不引入任何需要数据标定的阈值。

## 变更清单（TPR-09）

穷尽列出，每项对应 `implement.md` 的一个步骤。

| 类别 | 路径 | 动作 | 步骤 |
| --- | --- | --- | --- |
| 脚本 | `academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py` | 改：抽出 `_endpoint_jaccard`；新增游标、eligibility、三检查器、三个 CLI 开关 | S2、S3、S6、S7 |
| 脚本 | `academic-writing-skills/latex-thesis-zh/scripts/tex_loader.py` | 只读复用，不改 | S4 |
| 资源 | `academic-writing-skills/latex-thesis-zh/references/writing/subsection-context-terms.yaml` | 新增 | S5 |
| 资源 | `academic-writing-skills/latex-thesis-zh/references/writing/subsection-context-zh.md` | 新增（canonical 契约文件） | S8 |
| 资源 | `academic-writing-skills/latex-thesis-zh/references/modules/logic.md` | 改：加入口与边界 | S8 |
| 资源 | `academic-writing-skills/latex-thesis-zh/references/writing/paragraph-arc-zh.md` | 改：补一句指向 `S-CTX-*` | S8 |
| 资源 | `academic-writing-skills/latex-thesis-zh/SKILL.md` | 改：`logic` 路由行 + `last_updated` | S8 |
| fixture | `academic-writing-skills/latex-thesis-zh/evals/fixtures/subsection-context/**` | 新增（多文件 depth-3） | S4 |
| fixture | `academic-writing-skills/latex-thesis-zh/evals/fixtures/subsection-context-article.tex` | 新增（article 类） | S4 |
| evals | `academic-writing-skills/latex-thesis-zh/evals/evals.json` | 改：加条目（Bash python 写入） | S10 |
| docs | `docs/resource-manifest.json` | 改：新增两个 references 的 sha256 与页面映射 | S9 |
| docs | `docs/skills/latex-thesis-zh/resources/writing/subsection-context-*.md` | 新增（en） | S9 |
| docs | `docs/zh/skills/latex-thesis-zh/resources/writing/subsection-context-*.md` | 新增（zh） | S9 |
| 测试 | `tests/skills/latex_thesis_zh/test_subsection_context.py` | 新增 | S3、S5、S6、S7 |

设计文件中原「全部改动在 `analyze_logic.py` 内」的绝对声明作废，以本表为准。

## 验收标准

每条 AC 标注所证明的 R。

- [x] **AC-A-01**（R-A1、R-A4）在新 depth-3 fixture 上，`--subsection-context` 输出的小节编号
      序列等于写死的期望序列（形如 `["2.1.1","2.1.2","2.1.3","2.2.1"]`），不只断言非空。
- [x] **AC-A-02**（R-A1）在 article 类 fixture（根标题 `\section`）上，`x.x.x` 落在
      `\subsubsection`，编号序列等于写死的期望序列，证明深度判定与命令解耦。
- [x] **AC-A-03**（R-A1）在 `evals/fixtures/thesis-project/main.tex`（无 `\subsection`）上，
      输出「无 depth-3 标题」声明，产出零条 `S-CTX-*`，不回退到 depth-2。
- [x] **AC-A-04**（R-A3）不传 `--subsection-context` 时，`analyze_logic.py` 在全部既有 fixture 上
      的输出逐字不变（与 S2 前的基线快照比对）。
- [x] **AC-A-05**（R-A2）三码各有至少一条命中用例与一条不命中用例；`S-CTX-DUP` 在代码、
      references、测试中均不出现（负向断言）。
- [x] **AC-A-06**（R-A2）连续 3 单元同时缺进出接口时产出一条 `Minor` / `P2`，
      2 个单元时不升级；单项仍为 `Info` / `P3`。
- [x] **AC-A-07**（R-A5）单段小节、短段（汉字数 `< 20`）小节、以列表结尾的小节各有独立用例，
      断言 `*_status == "no_eligible_paragraph"` 且对应码不产出。
- [x] **AC-A-08**（R-A3、R-A4）`--emit-window --subsection <id>` 输出的每个部件带
      `source_file` 与文件内行号；多文件 fixture 上 `source_file` 指向 `chapters/*.tex`；
      输出不含正文原句（对文档任意 20 字连续片段做子串检查）。
- [x] **AC-A-09**（R-A2、R-A5）跨父节单元的 `S-CTX-IN` 证据侧为 `["current","parent_lead"]`，
      同父节为 `["current","prev.tail"]`。
- [x] **AC-A-10**（R-A6）YAML 缺失、字段缺失、字段类型非法三种情形均回退内置表。
- [x] **AC-A-11**（R-A7）`subsection-context-zh.md` 含契约块标记，块内含三码、协议句、
      depth 定义句与「无 depth-3 不回退」声明句。
- [x] **AC-A-12**（R-A7）`docs/resource-manifest.json` 已收录新增两个 references 文件，
      双语页面存在，`tests/contracts/test_docs_bilingual_resources.py` 通过。
- [x] **AC-A-13**（全部）`just ci` 全绿，pyright error 数不增加。
