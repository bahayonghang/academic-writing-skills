# 设计：共享可见正文 IR 与已复现缺陷修复

## 改造前基线（实跑记录，2026-08-25）

以下输出必须在改造后作为回归对照。所有命令在仓库根执行。

### B1 — V1 特殊章错选

fixture 结构（`\include` 顺序）：`nomenclature.tex`（符号和缩略语说明）→
`intro.tex`（绪论）→ `process.tex`（生产工艺流程与建模难点分析，含「工艺流程分析」
「建模难点」「总体框架」三节）→ `method.tex`（占位方法）→
`achievements.tex`（攻读学位期间取得的研究成果）。

```
uv run --extra dev python academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py <fixture>/main.tex --process-chapter
```

改造前输出（末段）：

```
% 过程分析章（chapters/nomenclature.tex:1）[Severity: Info] [Priority: P3]:
  [Script] 第“符号和缩略语说明”章未见过程分析章特征（章/节标题须同时含
  工艺/流程/过程分析/变量分析 与 总体框架/技术框架/研究方案）。
```

即定位阶段选中符号表章，真实工艺章（双信号均命中）未被检查。

### B2 — V2 阈值未归一

同一 4 行段落按 1 / 2 / 4 倍重复（词密度不变）：

| 篇幅 | `deai_check.py --analyze` 输出    |
| ---- | --------------------------------- |
| 1 倍 | 静默                              |
| 2 倍 | 静默                              |
| 4 倍 | `「因此」全文出现 8 次（上限 6）` |

### B3 — V3 生成表格/公式内容进入词频计数

7 次「首先」全部位于 `tabular` 行与 `equation` 的 `\text{}` 内：

```
第10行 [term_threshold] (result) 「首先」全文出现 7 次（上限 4）
```

对照：同 fixture 的控制行（`\clearpage`/`\newpage`）、跨行 `equation`、
`figure` 环境**零 finding**——手册 E1 所述症状不存在，勿按其原文写断言。

### B4 — V4 中文 help 乱码

`PYTHONUTF8=0` 且不设 `PYTHONIOENCODING` 时，`deai_check.py --help` 的中文以
GBK 字节输出（ASCII 部分正常）。设 `PYTHONIOENCODING=utf-8` 后正常。

## 架构

### 分层与 owner

```
tex_loader.assemble()            [既有，唯一 source owner，不改]
   -> AssembledDocument{content, lines, origins, missing, warnings, multi_file}
        |
visible_prose.build_ir(doc)      [新增]
   -> ProseIR{nodes, visible_zh_chars, visible_sentences, ir_version}
        |
   +----+----+----+
   |         |    |
 deai   process  (后续子任务的消费者)
 _check  chapter
```

`parsers.py` 保持不动。`visible_prose.py` 内部可调用
`parsers.LatexParser.extract_visible_text` 做单行剥离，但**跨行环境体的识别由
IR 自己的容器扫描负责**——这是 V3 的修复点，也是不动 `PRESERVE_PATTERNS`
（被 md5 锁定跨四副本）的原因。

### 节点模型

```python
@dataclass(frozen=True)
class ProseNode:
    node_id: str            # "N-000123"，稳定、与 assembled_span 起点绑定
    kind: str               # visible_paragraph|heading|list_item|table_cell
                            # |caption|math|control|comment|generated
    section_role: str       # frontmatter|abstract|nomenclature|body|appendix
                            # |achievements|acknowledgements|unverified
    source_span: tuple[str, int, int]   # (rel path, start, end)
    assembled_span: tuple[int, int]
    visible_text: str
    protected_tokens: tuple[str, ...]
    generated_from: str | None
    analysis_channels: tuple[str, ...]
```

`node_id` 用 `assembled_span` 起点派生（`f"N-{start:06d}"`），保证同一文档同一
构建结果稳定；不使用随机或时间派生 ID（后续 re-audit 需要跨轮比较）。

### 容器扫描（V3 的修复机制）

单行 `PRESERVE_PATTERNS` 无法剥离跨行环境体。IR 在行序列上做一次栈式扫描：

| 触发                                                                    | 进入状态 | 内部行 kind                                   |
| ----------------------------------------------------------------------- | -------- | --------------------------------------------- |
| `\begin{tabular}` / `\begin{tabularx}` / `\begin{longtable}`            | table    | `table_cell`                                  |
| `\begin{equation}` / `align` / `gather` / `multline` / `\[`             | math     | `math`                                        |
| `\begin{figure}` / `table`（浮动体）                                    | float    | 内部 `\caption{}` → `caption`，其余按嵌套判定 |
| `\begin{itemize}` / `enumerate` / `description`                         | list     | `list_item`                                   |
| `\clearpage` `\newpage` `\pagebreak` `\vspace` `\hspace` 等纯排版命令行 | —        | `control`                                     |
| 整行以 `%` 起                                                           | —        | `comment`                                     |

嵌套用栈处理（figure 内含 tabular 时最内层生效）。未闭合环境到章末或文末终止，
并在 IR 的 `warnings` 记录（沿用 `AssembledDocument.warnings` 的输出模式）。

**关键**：`\text{}` / `\mbox{}` 内的中文属于 `math` 节点，不进 `term_threshold`
通道——这是 B3 的直接修复。

### 章节角色分类与过程章选择（V1，两步，TPR-03）

角色分类和过程章选择是两步。不得把全部 `section_role=body` 的章当作过程章候选。
B1 是新建 fixture（`evals/fixtures/quality-regressions/b1-process-chapter/`），
不是既有 `evals/fixtures/thesis-project/main.tex`（后者 include 为 intro /
related / method-a / method-b / experiment / conclusion，成果/致谢用
`\input`，且无 `\frontmatter`/`\mainmatter`）。既有 fixture 不承担 B1 断言。

#### 第一步：`section_role`

四信号投票，不用单一序号推断：

1. **结构命令**：`\frontmatter` / `\mainmatter` / `\appendix` / `\backmatter`
   划分区间；区间内 chapter 继承基础 role
2. **include path**：`chapters/nomenclature.tex` 等路径线索（弱信号，只在标题
   分类失败时参考）
3. **标题 role classifier**：扩充现有豁免表为正向分类表

   | role               | 标题模式                                                    |
   | ------------------ | ----------------------------------------------------------- |
   | `abstract`         | 摘要 / abstract                                             |
   | `nomenclature`     | 符号 / 缩略语 / 术语表 / 主要符号 / 变量说明 / nomenclature |
   | `appendix`         | 附录 / appendix                                             |
   | `achievements`     | 攻读.*学位期间 / 成果 / 发表.*论文                          |
   | `acknowledgements` | 致谢 / acknowledg                                           |
   | `frontmatter`      | 目录 / contents / 插图索引 / 表格索引                       |
   | `body`             | 默认值，见下方缺省规则                                      |

4. **模板专用宏**：`templates/` 下四份快照已是模板事实唯一权威源，
   分类器读取其声明的专章宏（不新造模板知识）

缺省与冲突（可测试）：

| 输入 | `section_role` |
| --- | --- |
| 标题或路径唯一命中专章 | 该专章 role |
| 无 `\mainmatter`，标题/路径未命中专章，信号无冲突 | `body`（不因缺少 mainmatter 一律 `unverified`） |
| 标题与路径指向不同 role | `unverified` |
| `--section` 显式指定 | 不改 role；只影响第二步选择 |

既有 `thesis-project` fixture 无 mainmatter：绪论/方法/实验等未命中专章的
`\chapter` 得 `body`；`achievements` / `acknowledgement` 得专章 role。

#### 第二步：过程章选择

候选集合 = `section_role in {body, unverified}` 的 level-1 chapter。
在候选上应用既有双信号（`analyze_logic.py` 的 `PROCESS_SIGNAL_RE_ZH` 与
`PROCESS_FRAME_SIGNAL_RE_ZH`，匹配章标题 **或** 该章 level>=2 小节标题；
须过程信号与框架信号同时出现）：

| 双信号命中数 | 无 `--section` | 有 `--section` |
| --- | --- | --- |
| 1 | 选中该章 | 若指定章不是命中章：报冲突并要求确认，不静默改选 |
| 0 或 ≥2 | 输出「需显式指定」，不取首个 | 按标题包含或章序号定位指定章 |

B1 结构（`\include` 顺序）：`nomenclature.tex`（符号和缩略语说明）→
`intro.tex`（绪论）→ `process.tex`（生产工艺流程与建模难点分析，含「工艺流程分析」
「建模难点」「总体框架」三节）→ `method.tex`（占位方法，可含「方法」但不同时含
过程+框架双信号）→ `achievements.tex`（攻读学位期间取得的研究成果）。
预期：role 为 nomenclature / body / body / body / achievements。双信号在章标题
加 level>=2 小节标题的拼接文本上判定，唯一命中 `process.tex`。方法章保持
`body`，但不进入过程章主线检查。成果章因 role 过滤不进章引言主线。

现有两处 `_is_chapter_intro_exempt` 调用点
（`academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py:587`、
`:1954`）：`:1954` 改为第二步选择器；`:587` 改为按 role 过滤章引言检查——
`nomenclature` / `abstract` / `frontmatter` / `appendix` / `achievements` /
`acknowledgements` 不查承上启下；`body` 与 `unverified` 仍查（保守：宁可多查
不可漏查）。B1 输出已显示符号表章假阳性，属于已批准语义差异（R7）。

### 阈值归一（V2 的修复机制）

**约束先行（`tests/contracts/test_deai_alignment.py`，第四套锁，手册与
evidence-audit 均未覆盖）：**

| 成员                                                                        | 锁类型                                                                 | 对本设计的含义                                                                                                     |
| --------------------------------------------------------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `DEFAULT_THRESHOLDS["term_thresholds"]` 的 11 个 CJK 词                     | `test_term_thresholds_relationships:291-303` 要求 ZH 与 typst 同词同值 | **cap 值不能改**：全面 3 / 关键 5 / 其次 4 / 因此 6 / 显然 3 / 显著 5 / 核心 4 / 深入 3 / 然而 5 / 重要 5 / 首先 4 |
| `Checker._iter_visible_lines`                                               | `LOGIC_ALIGNMENTS:162`，docstring-stripped AST 跨 en/zh/typst 必须一致 | **不能改**；IR 消费要走新方法                                                                                      |
| `_apply_tier`                                                               | `LOGIC_ALIGNMENTS:159`                                                 | 不能改；`--tier` 对 cap 的缩放机制保持原样                                                                         |
| `Checker._check_term_threshold`                                             | 文件头 docstring `:24-26` 显式登记为 intentionally divergent           | **可改**（本设计的落点）                                                                                           |
| `DEFAULT_THRESHOLDS` 的 `overclaim`/`punctuation`/`sentence_length`/`tense` | `THRESHOLD_ALIGNMENTS:171-175`                                         | 不动                                                                                                               |

因此**不采用「按基准篇幅换算 cap 值」的方案**（会打断 typst 值锁），改为
**保持 cap 不变、改变计数口径**。下列常数在设计阶段锁定，实现不得改写，
也不得用真实学位论文量级作隐式输入（TPR-04）。

```yaml
# tone-thresholds.yaml —— 新增顶层键，不动 term_thresholds 子表
term_threshold_scaling:
  unit: per_visible_zh_chars
  window: 10000
  min_sample: 2000
  compare: ">"
```

通道与分母：

- 分子 `count`：`analysis_channels` 含 `term_threshold` 的节点里，该词项的
  substring 出现次数。
- 分母 `visible_zh_chars`：上述同一节点集合的可见汉字数（CJK 统一表意文字）。
  不进入该通道的 `math` / `control` / `comment` / `generated` / `table_cell` /
  `caption` / `list_item` 不计入分母。
- `term_threshold` 通道只挂 `visible_paragraph`。

判定式（整数，避免浮点）：

```
# visible_zh_chars < 2000
不触发

# visible_zh_chars >= 2000
触发 iff count * 10000 > cap * visible_zh_chars
```

性质（测试必须覆盖）：

| 分母 | 期望 |
| --- | --- |
| `min_sample-1`（1999） | 无论 `count` 多大都不触发 |
| `min_sample`（2000） | 触发 iff `count * 10000 > cap * 2000` |
| `min_sample+1`（2001） | 触发 iff `count * 10000 > cap * 2001` |

单调性：固定 `count` 时，增大分母不会把「不触发」变成「触发」，唯一例外是从
1999 跨到 2000（短文本静默 → 开始按比率判定）。跨过该点后，再增大分母只可能
从触发变为不触发。

B2 的 4 行重复段落若总可见汉字 < 2000，三个篇幅全部不触发，不能单独作为比率
oracle；比率断言用注入 `visible_zh_chars` 的单元测试。另建
`visible_zh_chars >= 2000` 的同密度 1/2/4 倍 fixture，证明 4 倍不再因累计计数
假阳性。

实现落点：`_check_term_threshold()`（未锁）内部改判定式，并改为消费 IR 的
`term_threshold` 通道——**新增私有方法**（如 `_iter_ir_nodes(channel)`），
`_iter_visible_lines()` 保持字节不变供其余 checker 使用。
`term_thresholds` 子表与 `_apply_tier` 均字节不变，四套锁全部不触发。

### CLI UTF-8（V4 的修复机制，TPR-06）

入口清单口径（2026-08-25 仓库复算，冻结）：

- `academic-writing-skills/latex-thesis-zh/scripts/` 下 24 个 `.py` 文件
- 其中 21 个含 `main()`：`analyze_abstract` `analyze_conclusion`
  `analyze_experiment` `analyze_literature` `analyze_logic` `blind_review`
  `check_consistency` `check_format` `check_references` `check_spec`
  `check_style_zh` `check_tables` `compile` `deai_batch` `deai_check`
  `detect_template` `generate_table` `map_structure` `online_bib_verify`
  `optimize_title` `verify_bib`
- 无 `main()` 的库文件 3 个：`bib_scan.py` `parsers.py` `tex_loader.py`

本子任务接入 helper 的入口只有 `deai_check.py` 与 `analyze_logic.py`。
其余 19 个 `main()` 不在本子任务验收内，列入后续工作项，不把「全部脚本入口」
写成已满足。

共享 helper（放 `visible_prose.py`；若该文件因此超过 400 行再拆 `cli_runtime.py`）：

```python
def ensure_utf8_stdio() -> str:
    """Return 'reconfigured' | 'repair_hint_emitted' | 'skipped'."""
```

| 流类型 | `reconfigure` | 结果 |
| --- | --- | --- |
| subprocess pipe / 文件流（TextIO） | 可用 | 设 `encoding="utf-8", errors="replace"`，返回 `reconfigured` |
| 测试替身 / 非 TextIO | 不可用，stderr 可写 | 写一行修复命令后返回 `repair_hint_emitted`，不抛异常 |
| stderr 亦不可写 | 不可用 | 返回 `skipped`，不抛异常 |
| Windows 原生 console / PowerShell 主机 | 本轮不测 | **missing evidence**（官方文档区分 console 与 pipe，pipe 测试不得外推） |

修复命令原文：`set PYTHONIOENCODING=utf-8`（cmd）与
`$env:PYTHONIOENCODING='utf-8'`（PowerShell）。

V4 回归只断言 pipe：`PYTHONUTF8=0`、清空 `PYTHONIOENCODING`、subprocess
按 utf-8 解码 `deai_check.py --help` 与 `analyze_logic.py --help`。

### 兼容层（TPR-05）

兼容面分成两类合同，不用一条「行为不变」覆盖。

**严格不变面**（快照逐字节）：

- `parsers.extract_visible_text(line)` 签名与行为字节不变
- 未迁移的 8 个消费者：`analyze_conclusion` `analyze_experiment`
  `analyze_literature` `blind_review` `check_format` `check_spec`
  `check_style_zh` `deai_batch` 的 stdout / CLI / flag / help
- 已迁移脚本的 CLI 命令名、flag 名、help 选项列表（help 中文编码属 V4，不算
  语义差异）
- `_iter_visible_lines` / `_apply_tier` / `term_thresholds` 子表 / `--tier`
  缩放

**已批准语义差异面**（golden delta，逐项）：

| ID | 文件 | 允许差异 | 证明 |
| --- | --- | --- | --- |
| D-V1-INTRO | `analyze_logic.py` | 章引言检查不再覆盖 nomenclature/achievements 等专章 | B1 与 thesis-project 的章引言 finding 集合 diff |
| D-V1-PROC | `analyze_logic.py` | `--process-chapter` 默认选择从「绪论后首个非豁免章」改为双信号唯一命中 | B1 改造前/后 stdout |
| D-V2-RATE | `deai_check.py` | 词项触发从 `count > cap` 改为 R3 整数比率，短文本不触发 | AC3/AC4 |
| D-V3-CH | `deai_check.py` | `table_cell`/`math`/`generated` 不进 `term_threshold` | AC5 |
| D-DEDUP | `deai_check.py` | finding 去重键改为 `rule_id + 归一化 source span + evidence hash` | AC8 |

快照目录：`research/baseline-snapshots/`（严格不变面）与
`research/approved-deltas/`（差异面，每项一份 before/after 与允许行清单）。
`thesis-project` 继续作为未迁移消费者的不变面夹具，不作为 B1 结构来源。

## 风险与缓解

| 风险                                    | 缓解                                                                                                                                                                           |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| IR 过度复杂、加载慢                     | 节点字段保持上述 9 个；按 module 提供投影视图（`ir.channel("term_threshold")`），不让消费者遍历全量节点                                                                        |
| 容器扫描排除过多，漏掉列表/表格中的贡献 | `kind` 不等于一律丢弃：`list_item` / `table_cell` / `caption` 各有 `analysis_channels`；E3（子任务 6）专门验证列表式科学问题不被漏识别                                         |
| 阈值口径变更破坏既有触发行为            | cap 与 `_apply_tier` 字节不变；短文本不触发；`>= min_sample` 用整数比率；不变面快照与 D-V2-RATE golden delta 分开                                                                 |
| role 分类器把正文章误判为特殊章         | 无 mainmatter 时未冲突章默认为 `body`；冲突才 `unverified`；过程章靠双信号第二步选择，不把全部 body 当候选                                                                         |
| 迁移波及 `parsers.py` 哈希锁            | `visible_prose.py` 只读 `parsers` 的公开 API，不改其成员；CI 的 `test_parsers_alignment.py` 作为守门                                                                           |
| 迁移波及 `deai_check.py` 第四套锁       | 只改登记为 intentionally divergent 的 `_check_term_threshold`；`_iter_visible_lines` / `_apply_tier` / `term_thresholds` 子表字节不变；CI 的 `test_deai_alignment.py` 作为守门 |

## 验证命令

```powershell
# 单元测试
uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/ -q

# 契约（哈希锁 + 路由表 + 版本）
uv run --extra dev python -m pytest tests/contracts/ -q

# V1 回归
uv run --extra dev python academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py `
  academic-writing-skills/latex-thesis-zh/evals/fixtures/<v1-fixture>/main.tex --process-chapter

# V4 回归（必须清 env）
uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/test_cli_encoding.py -q

# 文档同步
uv run --extra dev python docs/scripts/check_resource_sync.py --skill latex-thesis-zh

# 全量
just ci
just doc-build
```

## 未取证项

- IR 的真实 precision / recall / false-positive rate：**missing evidence**
  （子任务 6 建人工标注集）
- 性能基线（IR 构建耗时对比逐行处理）：**missing evidence**，实现时若发现
  明显退化再补测量
- Windows 原生 PowerShell console / GUI 主机编码：**missing evidence**
  （本轮只证明 subprocess pipe）
- 真实学位论文可见字数量级：**missing evidence**，不作为 `window` 或实现输入
