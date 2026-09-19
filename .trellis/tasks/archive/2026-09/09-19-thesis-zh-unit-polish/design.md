# 技术设计：`polish` 模块（单元润色 + 漂移核对）

## 1. 边界与所有权

`polish` 是编排层：单元坐标来自 `logic` 的小节游标与段落切分，单元前诊断来自既有脚本，改写发生在 `[LLM]` 层，核对由新脚本 `polish_unit_zh.py --verify` 完成。新增内容不重造下表任何一项的判据。

| 现象 | owner | `polish` 的用法 |
|---|---|---|
| 垫话（值得注意的是/综上所述/总之）、`不是…而是` 壳、伪洞察、句长均匀度 | `deai` | 单元前诊断（`deai_check.py --section <key>`），只读其发现 |
| 口语化、绝对化词、搭配、成分残缺、中英标点、数值单位、单句过长 | `expression` | 单元前诊断（`check_style_zh.py --section <key>`） |
| 免责句/限制句后置、自我削弱、hedge 堆叠 | `claim-forward` | 单元前诊断（`check_claim_forward.py --section <key>`） |
| 段落弧线、一段一中心 | `logic --paragraph-arc` | 单元前诊断（可选） |
| 小节游标、三元窗口、S-CTX | `logic --subsection-context` / `--emit-window` | 单元坐标与只读邻域 |
| 论断强度阶梯 | `over-claim-guard.md` | `UP-STRENGTH` 词表来源；协议自检 |
| 术语一致性 | `consistency --custom-terms` | `--terms` JSON 格式复用 |
| 冒号/分号句间逻辑 | `academic-style-zh.md §5.4`（`[LLM]`） | 协议指针 |

改写契约三分法归属：`polish` 属"仅 `[LLM]` 层"（脚本不产出替换文本）。`[LLM]` 改写块补齐四字段；`[Script]` 报告每条只带 `Meaning-Check: NEEDS-LLM`。

## 2. 单元模型

```text
PolishUnit
  unit_id      : "1.2.1"（subsection）| "introduction#3"（paragraph：章节键 + 段序）
  unit_type    : "subsection" | "paragraph"
  title        : 小节标题 | ""（paragraph）
  source_file  : 多文件工程的真实源文件（AssembledDocument.origin）
  source_start / source_end : 源文件行区间（subsection 含标题行）
  assembled_start / assembled_end : 装配后行区间（用于切片）
  han_count    : 可见汉字数（约字数）
  context      : {prev: (file,start,end) | None, parent_lead: ... | None, next: ... | None}  # 只读
```

- `subsection` 单元 = `analyze_logic._build_subsection_cursor()` 的 `SubsectionUnit`；`context` = `analyze_logic._build_context_window(units, index, paragraphs)` 的坐标部分。深度判定、无 depth-3 声明句（`SUBSECTION_CONTEXT_NO_DEPTH3`）与 `--first-chapter` 语义完全沿用，不复制实现。
- `paragraph` 单元 = `analyze_logic._split_arc_paragraphs(content, parser, sections)` 的 `ArcParagraph`，按 `section` 分组编号；`context` = 同章节内前后各一段。`is_heading_lead` 段照常入单元（协议要求不删导语，见 prd D1）。
- 单元清单永不复制正文（与 `--emit-window` 同一原则）；LLM 按坐标 `Read(offset, limit)` 读取。
- 长单元：`han_count > 1200` 的 `subsection` 单元在清单中标 `[需拆分]` 并列出其内部 `paragraph` 单元 id；核对仍可对整个小节运行。

## 3. 脚本契约 `scripts/polish_unit_zh.py`

### 3.1 CLI（扁平旗标，`--help` 必须列出路由表命令出现的全部 `--` 选项）

```text
usage: polish_unit_zh.py [-h] (--plan | --verify) [--section SECTION] [--unit UNIT]
                         [--first-chapter N] [--original FILE] [--revised FILE]
                         [--terms JSON] [--max-growth RATIO] [--json] tex_file
```

- `--plan`：单元清单。`--section` 缩小到一章；`--unit` 只打印该单元及其只读邻域坐标（等价 `--emit-window`，但对 paragraph 单元同样可用）。
- `--verify`：需要 `--revised FILE`，且 `--unit ID`（脚本从装配文档切片原文）与 `--original FILE` 二选一。`--terms JSON` 可选。`--max-growth` 默认 `0.20`（未标定）。
- 两模式互斥；`--verify` 缺 `--revised` 或缺原文来源时 argparse 报错（exit 2）。
- 所有位置参数与可选参数均带用途说明，`--help` 不只列参数名。

### 3.2 `--plan` 算法

1. `doc = assemble(tex_file)`；`parser = get_parser(tex_file)`；`sections = parser.split_sections(doc.content)`。
2. 设置 `analyze_logic._DOC = doc`（与 `analyze_logic.analyze()` 自身做法一致；`_parent_context_for_unit` / `_context_part` 依赖该模块级游标）。这是有意接受的耦合，由测试 `test_reused_logic_helpers_exist` 锁定三个 helper 名与签名。
3. `units = _build_subsection_cursor(doc, parser, sections, first_chapter)`；`paragraphs = _split_arc_paragraphs(doc.content, parser, sections)`。
4. 有 depth-3：逐单元 `_build_context_window(units, i, paragraphs)` 取坐标；无 depth-3：打印 `SUBSECTION_CONTEXT_NO_DEPTH3` 原句，再按 `sections` 列 paragraph 单元。
5. 报告：

```latex
============================================================
润色单元清单（polish）
============================================================
% CONTRACT [Script]: mode=plan entry=main.tex section=all
% 单元 1.2.1《缺口单元甲》 subsection chapters/method-a.tex L15-L19 约 86 字 [可改]
%   prev.tail   : chapters/method-a.tex L10-L10 [只读]
%   parent_lead : chapters/method-a.tex L12-L13 [只读]
%   next.head   : chapters/method-a.tex L21-L21 [只读]
% ...
% POLISH: 共 9 个单元。每次只处理一个单元；处理后运行 --verify；超过 1200 字的单元按内部段落单元逐段处理。
```

文本清单到此结束，不附 `核对结论 = PLAN` 或语义核对结论；JSON 保留既有字段结构。

### 3.3 `--verify` 算法与 `UP-*` 码

原文切片 `orig`（`--unit` 时取 `doc.lines[assembled_start-1:assembled_end]`，多文件用装配行）与润色稿 `rev`（`read_text_robust`）都先做同一套抽取：

| 码 | 抽取 | 判定 | 档 / Severity / Priority |
|---|---|---|---|
| `UP-SCOPE` | 标题命令（`\chapter` `\section` `\subsection` `\subsubsection` `\paragraph`）、`\input` / `\include` / `\begin{document}` 行；只读邻域可见文本的首句（`--unit` 时可得） | 标题命令序列或标题文本相对 `orig` 新增、删除或改变；或新增输入/文档结构命令；或新增只读邻域句子（≥12 个汉字的精确子串）。原样保留的标题及原文已有的重复句不报错 | A / Error / P1 |
| `UP-CITE` | `cite` / `citep` / `citet` / `upcite`，以及 biblatex 的 `cites`、`parencite(s)` / `autocite(s)` / `textcite(s)` / `footcite(s)` / `footcitetext(s)` / `smartcite(s)` / `supercite(s)` 的全部键组（逗号拆分、去空白）；覆盖首字母大写、星号、可选注记和多次引用的全局注记 | 键多重集不等 | A / Error / P1 |
| `UP-REF` | `\ref` / `\eqref` / `\autoref` / `\cref` / `\pageref` 及首字母大写形式的目标多重集 | 不等 | A / Error / P1 |
| `UP-LABEL` | `\label{...}` 集合 | 不等 | A / Error / P1 |
| `UP-MATH` | `$...$`、`\(...\)`、`\[...\]`、`equation*?` / `align*?` / `gather*?` 环境体，空白规范化后多重集 | 不等 | A / Error / P1 |
| `UP-NUM` | 可见文本（`parser.extract_visible_text`）中的数字 token：整数/小数/百分比/科学计数/带 `\,` 或空格的数值+单位 | 多重集不等 | A / Error / P1 |
| `UP-TOKEN` | 含数字的标识符、大写连字符名、≥2 字母全大写缩写（对齐 `polish-rewrite-contract` 的护栏类别） | 集合不等 | B / Warning / P2 |
| `UP-TERM` | `--terms` JSON 扁平化后的每个术语在可见文本中的计数 | 任一术语计数变化 | B / Warning / P2（未传 `--terms` 不报） |
| `UP-STRENGTH` | 先屏蔽显式 `--terms` 词面，再计数：阶梯词（证明/表明/揭示/发现/识别出/提示/支持/与…一致/可能表明/似乎/暗示/倾向于）、S2 强度词（因果/相关/显著/不显著/可能）、hedge（复用 `claim-forward-terms-zh.yaml` `hedges` 字段，缺失时内置回退） | 任一词计数变化；报告词面上下文与术语/普通用法提示。方向（更强级计数增加或 hedge 减少 → "疑似抬升"，其余 → "疑似削弱"）只作候选，不能据此断言语义变化 | B / Warning / P2 |
| `UP-NEG` | 否定标记（不、未、无、非、没有、并非、不能、无法）计数 | 计数变化 | B / Info / P3 |
| `UP-LENGTH` | 可见汉字数 | `rev > orig × (1 + max_growth)` 或 `rev < orig × (1 − max_growth)` | B / Info / P3，报告比例 |

- 引用键抽取和可见文本中的引用载荷屏蔽使用相同的受支持命令扫描，识别完整命令名、注记与全部键组；不匹配 `citereset` 等相似名称，不展开自定义宏。命令覆盖依据本地 biblatex 定义，属于 R2.7 的复审修补。
- 星号前允许空格/换行及去注释后保留的空白，与 LaTeX `\@ifstar` / `\@ifnextchar` 的读入行为一致；单次、多次引用和交叉引用都不能依赖星号必须紧贴命令名这一假设。
- 术语词面屏蔽仅影响 `UP-STRENGTH`；`UP-TERM`、数字等其他检查仍使用原始可见文本。无显式术语时不补猜词表，`支持向量机` / `相关研究` 等子串可能产生 B 档候选，交由语义复核。
- A 档给 `原文:` / `润色稿:` 两行（减少/增加的差异项），引用/交叉引用/标签渲染为 `cite{...}` / `ref{...}` / `label{...}`，其他项用引号分隔，空侧显示“无差异项”；不用 Python 容器表示法。不给替换文本；B 档只给 `候选:` 说明。JSON 数组与字段保持不变。
- 每条发现附 `% Meaning-Check: NEEDS-LLM`。`Risk-Flags` 不输出（脚本无替换文本；`[LLM]` 改写块负责四字段）。
- 结尾：`% POLISH: 核对结论 = BLOCK`（有 Error）或 `% POLISH: 核对结论 = PASS-SCRIPT（仍需 [LLM] 语义复核：因果、范围、术语替换）`。
- 零发现也输出 `PASS-SCRIPT` 行与 `NEEDS-LLM`（AC-03）。
- `--json`：`{"mode","entry","unit","original","revised","findings":[{code,tier,severity,priority,title,original,revised,candidate,basis}],"verdict"}`；Windows 重定向需 `PYTHONIOENCODING=utf-8`（内联，不 export）。

### 3.4 报告格式（与 `expression` / `claim-forward` 同族）

```latex
============================================================
润色单元核对（polish）
============================================================
% CONTRACT [Script]: mode=verify unit=1.2.1 original=chapters/method-a.tex:L15-L19 revised=revised.tex terms=none
% POLISH (chapters/method-a.tex:L15-L19) [Severity: Error] [Priority: P1] [Script]: UP-CITE 引用键集合发生变化
% 原文: cite{li2021}
% 润色稿: 无差异项
% 依据: SKILL.md Safety Boundaries（\cite{} 默认不动）
% Meaning-Check: NEEDS-LLM
% POLISH (chapters/method-a.tex:L15-L19) [Severity: Warning] [Priority: P2] [Script]: UP-STRENGTH 结论强度词计数变化（疑似抬升）
% 候选: 「可能」1→0，「证明」0→1；对照 over-claim-guard.md 阶梯，保持原文结论强度，不得擅自抬升或削弱
% Meaning-Check: NEEDS-LLM
% POLISH: 核对结论 = BLOCK
```

### 3.5 退出码

| 模式 | 情况 | 退出码 |
|---|---|---|
| `--plan` | 任何情况（含无 depth-3、`--section` 未命中给 `% ERROR` 行） | 0 |
| `--verify` | 无 Error 级发现 | 0 |
| `--verify` | ≥1 Error 级发现 | 1 |
| 两者 | 参数错误 | 2（argparse） |

## 4. 复用与禁改

- 复用（import，不复制）：`tex_loader.assemble` / `read_text_robust`；`parsers.get_parser` / `resolve_section_keys` / `extract_visible_text`；`analyze_logic._build_subsection_cursor` / `_split_arc_paragraphs` / `_build_context_window` / `SUBSECTION_CONTEXT_NO_DEPTH3` / `_has_numbered_depth3`。导入方式与 `check_style_zh.py` 相同（`try: from parsers import ... except ImportError: sys.path.append(...)`）；测试按路径 importlib 加载并弹出 `parsers` / `tex_loader` / `analyze_logic` 三个 sidecar。
- 禁改（字节不变，测试锁 sha256）：`analyze_logic.py`、`deai_check.py`、`parsers.py`、`check_style_zh.py`、`check_claim_forward.py`、`tex_loader.py`。
- hedge 词表读取 `references/writing/claim-forward-terms-zh.yaml` 的 `hedges`（PyYAML 缺失或字段缺失 → 内置回退，与该脚本同策略）。不新建第二份 hedge 表。

## 5. `[LLM]` 协议文件结构 `references/writing/unit-polish-zh.md`

1. 适用范围与模式判定（润色 vs 审校）。
2. 五步流程：`--plan` → 读单元与只读邻域 → 单元前诊断（三脚本 `--section` 输出中落在单元行区间内的条目）→ 改写（必须保留 / 改动准入 / 修改偏好）→ 写润色稿到临时文件并 `--verify` → 交付。
3. 必须保留清单（S2 逐条 + 红线四项）。
4. 改动准入（S1 K5）与不做清单（不删导语 D1；`综上所述` 位置规则 D2；不删限制只移位；不换术语）。
5. 输出契约模板（润色稿 → 修改说明三类 → `[LLM]` 四字段块 → 核对摘要）。`【待补证】` 复用 `references/deai/guide.md` 标记。
6. 自检三问。
7. 全文/整章请求的处理（清单驱动、逐单元、每单元独立核对、不合并成整章稿）。
8. 来源归属（S1 MIT；S2 作者/链接/来源/著作权声明）。

## 6. 变更清单

| 路径 | 动作 | 触发的锁/测试 |
|---|---|---|
| `academic-writing-skills/latex-thesis-zh/scripts/polish_unit_zh.py` | 新增 | `test_polish_unit_zh.py`、SMOKE、router `--help` 匹配 |
| `academic-writing-skills/latex-thesis-zh/references/modules/polish.md` | 新增 | `POLISH_MODULE_DOCS`、孤儿扫描、manifest、双语页 |
| `academic-writing-skills/latex-thesis-zh/references/writing/unit-polish-zh.md` | 新增 | 孤儿扫描、manifest、双语页、`REFERENCE_LAYOUTS` |
| `academic-writing-skills/latex-thesis-zh/references/modules/routing-rules.md` | 修改（三分法 + 判据） | `test_polish_contract_alignment.py`、manifest |
| `academic-writing-skills/latex-thesis-zh/references/modules/expression.md`、`deai.md` | 各加一行 | manifest |
| `academic-writing-skills/latex-thesis-zh/SKILL.md` | 路由行、路由规则、Rewrite Contract、Reference Map、description、`last_updated` | `test_skill_contracts.py`（格式化 hook 重排后必跑）、`test_polish_contract_alignment.py`、`test_skill_versions.py` |
| `academic-writing-skills/latex-thesis-zh/examples/unit-polish.md` | 新增 | manifest、双语页 |
| `academic-writing-skills/latex-thesis-zh/evals/fixtures/unit-polish/{main.tex,revised-ok.tex,revised-drift.tex}` | 新增 | eval id 50 绑定 |
| `academic-writing-skills/latex-thesis-zh/evals/evals.json`、`evals/trigger_eval.json` | Bash python 追加 | 前缀哈希、`test_trigger_evals.py` |
| `tests/skills/latex_thesis_zh/test_polish_unit_zh.py` | 新增 | — |
| `tests/skills/latex_thesis_zh/test_latex_thesis_zh_coverage.py` | `SMOKE_COMMANDS` 加行 | `test_smoke_commands_cover_router_table` |
| `tests/contracts/test_skill_contracts.py` | `modules` 加 `polish` | — |
| `tests/contracts/test_polish_contract_alignment.py` | `POLISH_MODULE_DOCS` 加 zh `polish.md` | — |
| `.trellis/spec/academic-writing-skills/unit-polish-contract.md`、`index.md` | 新增 / 加行 | — |
| `docs/skills/latex-thesis-zh/index.md`、`docs/zh/skills/latex-thesis-zh/index.md`、`docs/usage.md`、`docs/zh/usage.md`、`docs/resource-manifest.json`、`docs/{,zh/}skills/latex-thesis-zh/resources/{references,examples}/...` | 修改 / 新增 | `test_docs_bilingual_resources.py`、`check_resource_sync.py`、`just doc-build` |

## 7. 兼容性与回滚

- 既有模块行为零变化：六个禁改脚本字节不变；`deai` 对齐锁、`parsers` 哈希锁、S-CTX 契约块、claim-forward `NO_LEAK_FILES` 均不触碰。
- `polish` 是新路由 token；旧命令与旧 evals 前缀不变。
- 回滚：按 implement.md 三个评审门各一个 commit，`git revert` 任一门不影响其他模块。

## 8. 风险

- `UP-NUM` 以复用解析器产出的可见文本为准；宏参数是否保留取决于解析器，不能保证覆盖所有模板宏数值。模板宏原样保留仍由 R3.2 的 `[LLM]` 核对负责，不为此修改禁改解析器或宣称脚本覆盖全部宏。
- `UP-STRENGTH` 只计数不判语义，`不显著` 同时命中 `显著`：计数按最长匹配优先（先 `不显著` 再 `显著`）避免重复计数；仍为 B 档候选。
- 显式术语只能排除已知词面内的强度子串；未配置的普通用法仍可能误报。报告应展示语境和限制，不维护不断扩大的硬编码例外表，也不宣称消除误报。
- `UP-LENGTH` 阈值未标定：默认 0.20 标注"未标定"，实施期可在私有语料上只记数字复核（不入仓库）。
- 段落单元编号在正文编辑后会漂移：清单是一次性快照，协议要求每次润色前重新 `--plan`。
