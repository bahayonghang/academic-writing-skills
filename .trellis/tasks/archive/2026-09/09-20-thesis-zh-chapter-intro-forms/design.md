# Design：正文章引言一段式 / 两段式

对应 `prd.md` R1-R7。§1-§3 为文档层，§4-§6 为脚本层（决策 D1 待用户复审）。

## 1. 边界与所有权

- 只改 `academic-writing-skills/latex-thesis-zh`、其 docs 镜像、tests、spec。`check_style_zh.py`、`deai_check.py`、`parsers.py`、`polish_unit_zh.py` 不动。
- 规则真相源：`references/writing/thesis-writing-guide.md`"正文章引言"节（既有节，改写扩充，不另建新指南——一段式与两段式是同一节的两种段式，拆文件会造成两处真相源）。
- 模块文档：`references/modules/logic.md`。路由：`SKILL.md` + `references/modules/routing-rules.md`。其余五份指南只改"指段数"的句子并加链接。
- 位置 → owner：

| 关注点 | 规则 owner | 脚本 owner | 本任务新增 |
| --- | --- | --- | --- |
| 章引言承上 / 启下 / 相对指代 / 篇幅 | thesis-writing-guide 章引言节；method-chapter-guide §三 | `_check_chapter_intro`（默认） | 章号列举正则修复；建议文案中立化 |
| 章引言段式与要件覆盖 | thesis-writing-guide 章引言节（新增小节） | 无 | `CI-STYLE` / `CI-MOVES` / `CI-LONG`（`--chapter-intro-style`） |
| 章引言背景重述 / 目录双写 | paragraph-roles-zh | `PR-INTRO-BG` / `PR-INTRO-TOC` | 不动 |
| 一段式超长句 / 意义套话 / 术语重复 | academic-style-zh；deai/guide | E-LONGSENT；deai | 只在指南反例处指路 |

## 2. 术语

| 术语 | 含义 | 取值 | 代码标识 |
| --- | --- | --- | --- |
| 位置形态 | 章引言写在哪里 | 编号引言节（`\chapter` 后直接 `\section{引言}`）/ 章后导语（章标题后不编号正文） | `intro_form` = `numbered` / `lead`（既有） |
| 段式 | 章引言有几个自然段 | 一段式 / 两段式 / 多段式（≥ 3） | `style` = `one` / `two` / `multi`（新增） |
| 要件 | 章引言必须完成的语义动作 | 问题 / 承上 / 方案 / 收束或路线 | `moves` 覆盖向量（新增） |

位置形态与段式正交：四种组合都合规。文档与代码不得再用"两形态"指段数。

## 3. 文档层

### 3.1 `thesis-writing-guide.md` 正文章引言节的目标结构

```text
## 正文章引言（一段式 / 两段式，承上启下）
  导语段：位置形态两者均合规（指路 method-chapter-guide §三）；段式两者均合规；推荐要件是承上句（有依赖时）——原推荐语改写处
  **篇幅**：原句保留
  ### 共同要件（要件固定、段数灵活）      —— R1.2 四要件表：要件 / 作用 / 典型句式 / 必需性
  ### 两段式                              —— 原"两段角色"+"可套用模板"原样搬入 + R1.5 一句补充
  ### 一段式                              —— R1.3 六步推进序表 + 模板 + 篇幅 + 起句三法 + 正反例
  ### 段式选型                            —— R1.4 两栏对照表 + 混用说明
  **弹性口径**：原四条原样保留
  **正反例**：原表保留 + 追加两行（一段式合规；一段式双写目录与路线）
  > 边界：原句保留
  ### 来源                                —— R1.6
```

### 3.2 一段式六步推进序（写入指南的表）

| 步 | 要件 | 句数 | 必需 | 写法要点 |
| --- | --- | --- | --- | --- |
| ① 对象锚定 | 问题 | 1~2 | 必需 | 本章对象的工艺现象或数据特性，带具体量（周期、比例、维数）；不重述绪论行业背景 |
| ② 问题推导 | 问题 | 1~3 | 必需 | 由现象推出本章要解决的技术问题及其后果（"导致……影响……"） |
| ③ 必要性句 | — | 0~1 | 可选 | 只有落到本章对象时保留（"为此，亟需……"）；"具有重要意义和学术价值"类空泛句删除（指路 deai） |
| ④ 承上接口 | 承上 | 0~1 | 按依赖 | 角色复用句 + 章节号，可列举（"第 3、4 章的预测模型作为本章适应度函数"）；并列章可省；不用"上一章" |
| ⑤ 方案宣告 | 方案 | 1~2 | 必需 | "针对该问题，本章……构建 / 提出<方法名>（English Full Name, ABBR），用于……" |
| ⑥ 收束或路线 | 收束或路线 | 1~3 | 必需 | 价值收束（"为……提供……支撑"）或方法路线（"首先……随后……最后……"），二选一或并用；不写节号目录 |

模板（合成，写入指南）：

```text
<对象>由<数据/工序>以<周期/规模>获得，而<关键量>……。<现象>导致<技术问题>，影响<后果>。
[第 X 章的<产出>在<条件>下<局限>。]
针对该问题，本章基于<思想>，构建<方法名>（English Full Name, ABBR），用于<作用>。
本章首先……，随后……，最后基于<数据>验证……；[为第 Y 章的<任务>提供<接口>。]
```

### 3.3 段式选型对照（写入指南的表）

| 条件 | 一段式 | 两段式 |
| --- | --- | --- |
| 承上 | 可压成一句角色复用句，或并列章不承上 | 需说明前章结论及其局限（≥ 2 句） |
| 问题层次 | 单一技术问题 | 两层以上问题，或需先立框架再立问题 |
| 方案 | 一句可宣告 | 方案含多个模块需逐一点名 |
| 篇幅 | 约 300~600 字、6~12 句 | 约 400~900 字；文献密集需 `\cite` 小型综述可 ≥ 3 段 |
| 全文一致性 | 各章可混用（语料 2/5 混用），不强求统一 | 同左 |
| 共同禁忌 | 同一引言内不双写节号目录与方法路线；不重述绪论背景与综述 | 同左 |

### 3.4 其余文件的追加 / 改写位置

| 文件 | 位置 | 内容 |
| --- | --- | --- |
| `method-chapter-guide-zh.md` | §三首条；§三列表末尾；§三正反例表；§十映射表 | 推荐语改写；"段式"条 + 链接；一段式合规行；`CI-*` 行 |
| `structure-guide.md` | 标题后导语规范章引言条 | "两段"→"一段式或两段式均可" |
| `process-chapter-guide-zh.md` | §十末段 | "两段式从第 3 章起适用"→"（一段式或两段式）" |
| `paragraph-roles-zh.md` | 指南分工第一条 | 措辞 |
| `modules/logic.md` | Chapter Intro Specialization；Paragraph Role Checks 节之后 | 措辞；新节 `## Chapter Intro Style Checks (--chapter-intro-style)` |
| `modules/routing-rules.md` | 章引言条 | 措辞 + 触发词 + flag |
| `SKILL.md` | `when_to_use`；`logic` 行；歧义速判；Reference Map L164；`last_updated` | R3.1 |
| `docs/**/index.md` ×2 | `logic` 行；写作参考列表 | flag；新 YAML 行 |

保真锁核对：`test_thesis_zh_guidance_fidelity.py` 不锁章引言句子；R2 只改含"两段"的句子，其他原句不动。

## 4. 脚本层

### 4.1 默认检查误伤修复（R5，默认行为变化例外）

```python
# 原
CHAPTER_DEP_REF_RE = re.compile(r"第\s*[一二三四五六七八九十百\d]+\s*章")
# 新：允许章号列举（顿号 / 逗号 / 波浪号 / 连字符 / 至和与及）
CHAPTER_DEP_REF_RE = re.compile(
    r"第\s*[一二三四五六七八九十百\d]+"
    r"(?:\s*[、，,～~\-—至和与及]\s*[一二三四五六七八九十百\d]+)*\s*章"
)
```

已验证："第 3、4、5 章""第 3～5 章""第3-5章""第三章和第四章"（命中"第三章"）"第 2 章"均命中；"第二和第三章"在"第三章"处命中。`CHAPTER_NUM_REF_RE`（P-FRAME 专用）不动。

建议文案（只改 `% 建议：` 行，observe 行与理由行不动）：

| 位置 | 原 | 新 |
| --- | --- | --- |
| `bridge_suggest` | 在章引言第一段用章节号回顾前一章…… | 在章引言中用章节号写一句角色复用句承接前一章解决了什么、得出什么结论，引出本章为何继续；一段式可压成一句。 |
| `preview_suggest` | 在章引言第二段说明本章…… | 在章引言中说明本章针对什么问题、核心思想，必要时预告本章方法路线或各节安排。 |
| 过简 `% 建议` | 扩展为承上启下两段——先承接前章…… | 补齐承上启下要件（一段或两段均可）——先承接前章，再交代本章问题、思路与方法路线。 |
| 过长 `% 建议` | ……章引言保留承上启下两段。 | ……章引言只保留承上启下要件。 |

过简 `% 理由` 行"章引言一般为 1~2 个自然段、约 300~500 字"已是段式中立，不改。

### 4.2 入口与分支

```python
analyze(file_path, section=None, cross_section=False, motivation_thread=False,
        intro_mainline=False, process_chapter=False, first_chapter=None,
        method_narrative=False, paragraph_arc=False, subsection_context=False,
        subsection=None, emit_window=False, paragraph_roles=False,
        chapter_intro_style=False) -> list[str]
```

- 新参数放末尾；`main()` 新增 `--chapter-intro-style`（help："运行章引言段式观察（一段式/两段式标签、要件覆盖、一段式过长；默认关闭）"）。
- 分支插在 `paragraph_roles` 分支之后、兜底行之前：`ci_ranges = ranges if section else [(1, len(lines))]`；`out.extend(_check_chapter_intro_style(content, lines, parser, sections, ci_ranges, first_chapter=first_chapter))`。
- `--method-narrative` 无 `--section` 的提前 return 路径不变；该路径下本 flag 不运行（文档注明）。

### 4.3 单元定位：`_chapter_intro_span`

```python
def _chapter_intro_span(chapter, headings, lines, parser) -> tuple[int, int, int, str] | None:
    """返回 (report_line, span_start, span_end, form)；无小节返回 None。
    form == "lead"：span = 章标题行+1 .. 首个小节行-1
    form == "numbered"：span = 引言小节标题行+1 .. 该小节结束行
    """
```

`_chapter_intro_block` 改为：调 `_chapter_intro_span` 取区间，再按原逻辑拼可见文本并返回 `(report_line, intro_text, form)`——输出字节不变（唯一触碰既有代码的点，列为回滚点）。既有"编号引言节形态适配"判定（章后正文 < 40 字且首小节标题含引言/概述）原样保留在 span 函数内。

段落：`paragraphs = [p for p in _split_arc_paragraphs(content, parser, sections) if span_start <= p.start <= span_end]`；`style = one / two / multi` 按 `len(paragraphs)`；`han = sum(汉字数)`；`sents = sum(len(p.sentences))`。

### 4.4 要件判定

| 要件 | 命中条件 | 复用 |
| --- | --- | --- |
| 问题 | 引言可见文本命中 `problem_markers` 任一 | 新 YAML |
| 承上 | `CHAPTER_BRIDGE_KEYWORDS_ZH` 任一，或 `CHAPTER_DEP_REF_RE`（新）命中；第 2 章（`is_first_body`）标"不适用" | 既有 |
| 方案 | 存在同一句同时含"本章"与 `solution_markers` 任一（`_arc_sentences` 切句） | 新 YAML + 既有切句 |
| 收束或路线 | `closing_markers` 任一，或 `CHAPTER_ROADMAP_KEYWORDS_ZH` 任一，或 `SECTION_NUM_PREVIEW_RE` | 新 YAML + 既有 |

内置默认（与 YAML 相等，测试断言）：

```python
CI_PROBLEM_MARKERS = ("问题", "难题", "难点", "瓶颈", "不足", "缺乏", "缺少", "难以", "无法", "导致", "影响", "制约", "挑战")
CI_SOLUTION_MARKERS = ("提出", "构建", "设计", "建立", "研究", "开发", "给出", "引入", "采用")
CI_CLOSING_MARKERS = ("提供支撑", "提供数据支撑", "提供依据", "提供基础", "奠定基础", "奠定了基础", "提供保障", "提供新思路", "提供工具", "打下基础", "为后续", "为第")
CI_ONE_PARA_MAX_HAN = 600  # 未标定 / UNVERIFIED
```

### 4.5 三码契约

所有码：`[Script]`、Info/P3、`Meaning-Check: NEEDS-LLM`；`Current` 只给标签、计数与覆盖向量，不复制整句。输出由 `_ci_finding(code, start, end, message, current, suggested, rationale)` 生成（行首 `% 章引言段式（行 N-M）`，结构同 `_pr_finding`），不改 `_pr_finding` / `_arc_finding`。

| 码 | 触发 | Current 内容 | 豁免 |
| --- | --- | --- | --- |
| `CI-STYLE` | 每个正文章引言块非空时各报一条 | `段式=一段式/两段式/多段式；位置=编号引言节/章后导语；约 N 字；P 段 S 句；要件 问题:✓/✗ 承上:✓/✗/不适用 方案:✓/✗ 收束或路线:✓/✗` | 引言块为空（默认检查已报） |
| `CI-MOVES` | 问题、收束或路线任一 ✗；或方案 ✗ 且默认"缺启下"未对该章触发（重算 `has_roadmap` / `has_chapter_action`，避免重复） | 缺失要件列表 | 引言块为空；`--section` 区间外 |
| `CI-LONG` | `style == one` 且 `han > CI_ONE_PARA_MAX_HAN` 且 `han <= max_chars`（900 / 1600，按位置形态） | `一段式约 N 字，阈值 600` | `han > max_chars`（默认"过长"已报，零重叠）；两段式 / 多段式 |

`--section`：finding 的 `start` 落在 `ci_ranges` 内才输出。`--first-chapter N`：第 2 章判定复用 `_check_chapter_intro` 的 `real_num == 2` 逻辑。

### 4.6 词表 `references/writing/chapter-intro-style-terms.yaml`

字段：`problem_markers`、`solution_markers`、`closing_markers`。加载器 `_load_chapter_intro_style_terms(script_dir)` 复制 `_load_paragraph_roles_terms` 的逐字段回退模式；文件头注释标 `CI_ONE_PARA_MAX_HAN = 600 未标定 / UNVERIFIED，阈值不由 YAML 覆盖`。docs 两份 neutral 镜像与源相等。

### 4.7 数据流

```text
assemble(file) → extract_headings / split_sections
  → 正文章列表（排除 _is_chapter_intro_exempt）
  → 每章：_chapter_intro_span → 区间内 ArcParagraph 列表
        ├─ 段数 / 汉字数 / 句数 → style
        ├─ 要件向量（问题 / 承上 / 方案 / 收束或路线）
        ├─ CI-STYLE（恒报）
        ├─ CI-MOVES（缺件）
        └─ CI-LONG（一段式超阈值且未超默认上限）
  → 按 ci_ranges 过滤 → 按行号排序 → findings
```

## 5. 兼容性与取舍

- 默认输出零变化边界：新 flag 关闭时不进分支；`_chapter_intro_span` 抽取须让 `baseline-before.txt`、`test_chapter_intro_forms.py`、`test_paragraph_roles.py` 全绿。
- 两处默认行为变化（正则、建议文案）是有意的误报 / 误导修复：`baseline-sample.tex` 只有一章、无章引言 finding，基线不受影响；存量断言全部落在 observe 行。commit 正文声明。
- 为什么挂在 `logic` 而非新模块：章引言的默认检查、PR-INTRO-*、S1 都在 `analyze_logic.py`；段式是同一单元的另一视角。
- 为什么 `CI-STYLE` 恒报：用户要的是"支持两种写法"，脚本先如实报告观察到的段式与要件，让 LLM / 作者按选型表判断，不由脚本判定"该用哪种"。
- 为什么不判定段式混用、不判意义句、不判对象锚定具体性：语料混用 2/5 合法；后两者需语义判断，且 deai / E-LONGSENT 已有 owner。
- 为什么 600：语料一段式上界 577 字；两段式下界 393 字；600 只是"一段已承载两段信息量"的提示阈值，标 UNVERIFIED，不由命令行覆盖。
- 词表不复用 `INTRO_PROBLEM_RE_ZH`（绪论漏斗专用，含"任务/目标"等泛词）与 `INTRO_BACKGROUND_RE_ZH`，避免耦合绪论检查。

## 6. 回滚

- 文档层单独 commit：`git revert`；manifest 重生成一次。
- 脚本层单独 commit：删除 flag、分支、`_check_chapter_intro_style`、`_ci_finding`、YAML、常量即恢复；正则与文案修复若引发未预见回归，可单独回退这两处并保留其余（它们与新 flag 无耦合）。
- `_chapter_intro_span` 抽取若导致基线或存量测试红，回退为在 `_chapter_intro_block` 内联并让新检查复制区间逻辑（在 spec 记录两处同步义务）。
