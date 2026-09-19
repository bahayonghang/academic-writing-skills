# latex-thesis-zh 段落/小节单元受控润色（`polish` 模块）

任务目录：`.trellis/tasks/09-19-thesis-zh-unit-polish/`。单任务（不拆父子）：脚本、协议文档、路由、测试、docs 相互耦合，只能一起验收。

## 背景与需求来源

用户请求（2026-09-19）：结合 `ref/graduate-thesis-polish-and-write-skill` 与一份知乎润色提示词，优化 `latex-thesis-zh` 的中文学位论文润色能力；在使用该 skill 并触发"语言规则段落、章节润色"时生效；**尽量不要全文优化**——优化细节需要核对，防止错误润色。

需求来源与归属（细节见 `research/prior-art-mapping.md` §1）：

- S1：`ref/graduate-thesis-polish-and-write-skill/thesis-polish/`（MIT）。采纳其"单次只处理一个明确范围、绝不整本 Read"、K5 克制修改、K8 审校/写作模式区分、两个自检问题。
- S2：知乎回答《润色中文学术论文段落》。作者：大学生知识星球；链接 https://www.zhihu.com/question/582506176/answer/2083151703524877127；来源：知乎；著作权归作者所有，非商业转载须注明出处。采纳其"必须保留"清单、修改要求、"润色稿 + 修改说明三类"输出契约。

现状实测（`research/prior-art-mapping.md` §3）：`deai` / `expression` / `claim-forward` 在带章节结构的入口文件上可覆盖 S2 的大部分诊断项，但三者都不能对"润色稿相对原文是否漂移"做核对；`logic --emit-window` 已能给出 depth-3 小节的可改/只读坐标。缺口是：(1) 一份把润色限定在单元内、并规定核对步骤的 `[LLM]` 协议；(2) 一个对"原文 vs 润色稿"做确定性漂移核对的脚本。

## Goal

新增路由模块 `polish`（中文名"单元润色"）：

1. 润色以**单元**为粒度（一个自然段，或一个 depth-3 小节），一次只处理一个单元；章级/全文请求先列单元清单再逐单元处理，不产出整章替换稿。
2. 每个单元的润色稿在交付前经脚本核对（引用/标签/公式/数字/术语/结论强度/范围），核对结果与 `[LLM]` 改写块一起交付。
3. 输出遵循 S2 契约：先完整润色稿，再"修改说明"三类，不解释未改内容。

## Requirements

### R1 单元定义与范围控制

- R1.1 单元类型两种：`subsection`（depth-3 小节，编号规则与 `--subsection-context` 一致，含标题行）与 `paragraph`（可见正文自然段，切分与 `--paragraph-arc` 一致）。无 depth-3 标题的文档只有 `paragraph` 单元；不做 depth-2 回退。
- R1.2 上下文只读：`subsection` 单元附带 `prev.tail` / `parent_lead` / `next.head` 只读坐标（复用 `--emit-window` 语义）；`paragraph` 单元附带前后各一段只读坐标。只读部分不得出现在润色稿中。
- R1.3 全文/整章请求的处理方式固定为：`--plan` 列出单元清单 → 按清单顺序逐单元润色 → 每单元独立核对。超过 1200 字的单元按自然段拆分后逐段处理（与 paper-audit `POLISH_GUIDE.md` 的拆分规则一致）。
- R1.4 多轮顺序不变：论证/逻辑（`logic`）→ 句子结构 → 词汇/排版；`polish` 只在句子与词汇两层动作，段落顺序与论断增删不在范围（对应 `--strength` 语义表）。

### R2 脚本 `scripts/polish_unit_zh.py`

- R2.1 `--plan`：打印单元清单（单元 id、类型、标题、源文件与行区间、约字数、只读邻域坐标），不复制正文；可用 `--section` 缩小范围；`--first-chapter` 语义与 `analyze_logic.py` 相同。
- R2.2 `--verify`：对一个单元的原文与润色稿做漂移核对；原文来自 `--unit <id>`（脚本按 id 切片）或 `--original <file>`；润色稿来自 `--revised <file>`；可选 `--terms <json>`（格式复用 `check_consistency.py --custom-terms`）。
- R2.3 核对码 `UP-*`（定义见 design.md §3）：`UP-SCOPE`、`UP-CITE`、`UP-REF`、`UP-LABEL`、`UP-MATH`、`UP-NUM`、`UP-TOKEN`、`UP-TERM`、`UP-STRENGTH`、`UP-NEG`、`UP-LENGTH`。红线类（SCOPE/CITE/REF/LABEL/MATH/NUM）为 Error/P1；其余为 Warning 或 Info 候选。
- R2.4 脚本不产出替换文本；每条发现只带 `Meaning-Check: NEEDS-LLM`（与 `claim-forward` 同属"仅 `[LLM]` 层"）。
- R2.5 退出码：`--plan` 恒 0；`--verify` 有 Error 级发现时 1，否则 0。`--json` 输出结构化结果。
- R2.6 不修改 `analyze_logic.py`、`deai_check.py`、`parsers.py`、`check_style_zh.py`、`check_claim_forward.py`、`tex_loader.py`（字节不变）；复用方式见 design.md §4。
- R2.7 Fable 复审补充（2026-09-19 用户授权继续完善）：引用保护覆盖明确支持的 biblatex 单次/多次命令及可选注记、星号和大小写形式；交叉引用包含 `\Cref` 等支持命令的首字母大写形式。键抽取与载荷屏蔽共用边界。显式 `--terms` 的词面在 `UP-STRENGTH` 中屏蔽，但仍做 `UP-TERM` 频次检查；未配置术语的子串命中维持带上下文的 B 档候选，不宣称自动判定语义。
- R2.8 所有 CLI 参数给出帮助说明；A 档文本差异可直接阅读；`--plan` 文本不附核对结论；JSON 字段结构保持不变。

### R3 `[LLM]` 润色协议 `references/writing/unit-polish-zh.md`

- R3.1 模式判定：用户明确要求"润色/改写/优化语句"→ 出润色稿；"检查/审校/看看问题"→ 只出诊断（沿用 S1 K8 与本仓库 `literature` / `deai` 默认）。
- R3.2 必须保留（S2 清单逐条）：专有名词/理论名/变量名；数字/单位/实验参数；引文与图表编号；因果、相关、显著、不显著、可能等结论强度；研究对象、时间范围、方法步骤、样本参数；`\cite{}` / `\ref{}` / `\label{}` / 数学环境 / 模板宏。
- R3.3 改动准入（S1 K5）：只改硬命中（既有脚本发现）、口语化、语法错、逻辑断层、欧化长句；通顺句不动；不为"高级表达"换术语；不追求整齐句式。
- R3.4 修改偏好（S2）：一段一中心、结论先行（判据指向 `logic --paragraph-arc`，不重造）；优先具体研究动作动词（统计、比较、识别、检验、归纳、检测、计算）；删无信息垫话（诊断来源 `deai`）；无依据的反差/递进句式改为陈述（`不仅…而且` 不在 `deai` 壳集合内，由协议清单覆盖）；重复免责与泛泛局限只移位不删除（`claim-forward` 规则）；方法段按流程拆句。
- R3.5 输出契约：① 完整润色稿（单元内全文）；② 修改说明三类：删除了哪些无信息表达 / 调整了哪些句子逻辑或结构 / 哪些位置缺证据需作者补充（第三类沿用 `【待补证】` 标记）；③ `[LLM]` 改写块四字段（`Changed` / `Protected` / `Meaning-Check` / `Risk-Flags`）；④ `--verify` 报告摘要。不解释未修改内容，不重复正文。
- R3.6 自检：删除测试（删掉这句信息是否损失）；邻段句式对照（不引入本单元相邻段落没有的句式风格）；强度对照（参照 `over-claim-guard.md` 阶梯，保持原文结论强度，不得抬升一级，也不得擅自削弱；与 R3.2 一致）。
- R3.7 来源归属节：S1（MIT）与 S2（知乎，作者与链接）逐条写明采纳内容；不复制 S1/S2 原文段落。

### R4 路由与契约文档

- R4.1 `SKILL.md`：路由表新增 `polish` 行（主命令 `uv run python $SKILL_DIR/scripts/polish_unit_zh.py main.tex --plan`，Read next `references/modules/polish.md`）；路由规则新增一条（"润色这段/这一节/把第 X 章语言润色一下" → `polish`；整章/全文请求先 `--plan`）；Rewrite Contract 段把 `polish` 列入"仅 `[LLM]` 层"；Reference Map 新增协议文件；description 增触发词且总长 ≤400；`last_updated` 更新，`version` 不动。
- R4.2 `references/modules/routing-rules.md`：三分法"仅 `[LLM]` 层"组加 `polish`；逐类判据加一条；执行顺序放在 `expression` / `deai` / `claim-forward` 之后。
- R4.3 `references/modules/polish.md`：命令、单元模型、`UP-*` 码表与分档、退出码、与 `expression` / `deai` / `claim-forward` / `logic` / `consistency` 的边界（每条指向既有 owner）、契约段（四字段、`NEEDS-LLM`、指向 `../writing/over-claim-guard.md`）。
- R4.4 `references/modules/expression.md` 与 `deai.md` 各加一行指向 `polish`（单元级润色与核对走 `polish`）。
- R4.5 `examples/unit-polish.md`：一个 `--plan` → 单元润色 → `--verify` 的示例（合成文本，不含私有语料）。

### R5 spec、测试、evals

- R5.1 新建 `.trellis/spec/academic-writing-skills/unit-polish-contract.md` 并在 `index.md` 加行：单元定义、`UP-*` 语义、退出码、禁改清单、与 S-CTX / P-ARC / 改写契约的关系。
- R5.2 新建 `tests/skills/latex_thesis_zh/test_polish_unit_zh.py`（importlib 按路径加载）：`--plan` 在 `evals/fixtures/subsection-context/` 上输出的小节 id 与 `EXPECTED_PROJECT_IDS` 一致；无 depth-3 fixture 只列 `paragraph` 单元；每个 `UP-*` 码一条正例与一条反例；退出码；`--terms` 漂移；只读邻域不入润色稿（`UP-SCOPE`）；原文=润色稿时零发现且仍输出 `NEEDS-LLM`；六个禁改脚本 sha256（LF 规范化）不变。
- R5.3 契约测试同步：`tests/contracts/test_skill_contracts.py` `SKILLS["latex-thesis-zh"]["modules"]` 加 `polish`；`tests/contracts/test_polish_contract_alignment.py` `POLISH_MODULE_DOCS["latex-thesis-zh"]` 加 `references/modules/polish.md`；`tests/skills/latex_thesis_zh/test_latex_thesis_zh_coverage.py` `SMOKE_COMMANDS` 加 `("polish_unit_zh.py", ["main.tex", "--plan"], {0}, "润色单元清单")`。
- R5.4 `evals/evals.json` 追加 id 50（fixture `evals/fixtures/unit-polish/`：`main.tex` 含 depth-3 小节与 S2 垫话/递进/免责样本；`revised-ok.tex` 与 `revised-drift.tex` 两份润色稿；drift 版含引用键删除、数字改动、`可能`→`证明` 强度抬升）；`evals/trigger_eval.json` 追加 ≥2 条正例（"润色这一节""把 3.2.1 语言改学术一点"）与 ≥1 条负例（英文论文段落润色 → `latex-paper-en`）。两文件只用 Bash python 追加，前 49 条 / 前 53 条哈希不变。
- R5.5 docs：`docs/skills/latex-thesis-zh/index.md` 与 `docs/zh/.../index.md` 路由表加行、Module References 与写作参考加链接；`docs/usage.md` / `docs/zh/usage.md` token 列表加 `polish`；`check_resource_sync.py --skill latex-thesis-zh --write-manifest` 重生成 manifest 并补两份镜像页（zh 源 → zh 页原样、en 页翻译）。
- R5.6 Fable 复审回归：biblatex 与大写交叉引用漂移必须阻塞；术语屏蔽不影响术语频次及术语外强度变化；自定义 YAML 哨兵词证明加载路径与回退路径不同；帮助、A 档可读差异、清单无核对结论均有验证。文档与测试注册表的 `polish` 顺序跟随路由，列表保持连续。

## Acceptance Criteria

- [x] AC-01 `polish_unit_zh.py main.tex --plan` 在 `evals/fixtures/subsection-context/` 上列出 9 个 `subsection` 单元，id 集合等于 `["1.1.1","1.2.1","1.2.2","1.2.3","1.3.1","1.4.1","1.4.2","1.4.3","2.1.1"]`，输出不含任何正文行；退出码 0。
- [x] AC-02 同命令在 `evals/fixtures/thesis-project/` 上输出"本文档无 depth-3 标题"声明并只列 `paragraph` 单元；退出码 0；输出含 `润色单元清单`。
- [x] AC-03 `--verify --unit 1.2.1 --revised <原文逐字节副本>` 零发现、退出码 0、输出含 `Meaning-Check: NEEDS-LLM`。
- [x] AC-04 对 `revised-drift.tex`：`UP-CITE`、`UP-NUM`、`UP-STRENGTH` 各至少一条；退出码 1；输出不含 `Risk-Flags: overstatement`（`[Script]` 不得置该标记）。
- [x] AC-05 原有标题命令及标题文本原样保留时不报 `UP-SCOPE`；新增、删除或修改标题，或新增 `\input` / `\include` / `\begin{document}` → `UP-SCOPE` Error。相对原文新增只读邻域首句（至少 12 个汉字的精确子串）→ `UP-SCOPE` Error；原文已有的重复句不因原样保留而报错（与 AC-03 一致）。
- [x] AC-06 `--terms` 指定术语在润色稿中计数变化 → `UP-TERM`；未指定 `--terms` 时不报 `UP-TERM`。
- [x] AC-07 `analyze_logic.py`、`deai_check.py`、`parsers.py`、`check_style_zh.py`、`check_claim_forward.py`、`tex_loader.py` sha256（CRLF→LF 规范化）与 HEAD 一致（测试断言）。
- [x] AC-08 `tests/contracts/test_skill_contracts.py`、`test_polish_contract_alignment.py`、`test_deai_alignment.py`、`test_parsers_alignment.py`、`test_subsection_context_contract.py`、`test_claim_forward_contract.py`、`test_thesis_zh_guidance_fidelity.py`、`test_trigger_evals.py`、`test_docs_bilingual_resources.py`、`tests/skills/latex_thesis_zh/` 全绿。
- [x] AC-09 `SKILL.md` description 长度 ≤400；`version` 仍为 `6.0.0`；`last_updated` = 实施日期。
- [x] AC-10 `uv run python docs/scripts/check_resource_sync.py --skill latex-thesis-zh`、`just ci`、`just doc-build` 绿。
- [x] AC-11 协议文件含 S1、S2 归属节；新增或修改的公开技能、fixture、测试及 docs 不含私有语料内容或路径。任务规划文件可记录本地复核入口，但不得复制私有原文或润色稿；复核记录只含核对码与命中数。
- [x] AC-12 `references/` 新文件均为 kebab-case，位于 `modules/` 或 `writing/`，且被 `SKILL.md` 或其他文档链接（无孤儿）。

## Constraints

- 不 bump `version`；不改 `justfile` / `pyproject.toml` / `uv.lock`。
- 不新增 `deai` 类别、不改 `deai_check.py`（对齐锁与模式簇契约）；`不仅…而且` 等 S2 项只入协议 `[LLM]` 清单。
- 不改 `analyze_logic.py`（小节游标与段落切分只以 import 复用）；不改 `parsers.py`（哈希锁）。
- `[Script]` 层恒 `Meaning-Check: NEEDS-LLM`；本脚本无替换文本，报告不输出 `Risk-Flags` 行（四字段由 `[LLM]` 改写块补齐）。
- 阈值（`UP-LENGTH` 增长比例、`UP-NEG` 计数）无标定语料依据，默认值标注"未标定"，可由参数覆盖；不得在文档中宣称误报率。
- 私有语料 `ref/thesis/decrypted/` 只可在实施期做只记数字的本地复核，不进 fixture / 测试 / 文档。
- 不引入范例论文指纹机制（S1 K3 / reference-thesis.md），见 D4。
- typst / latex-paper-en 不在范围。

## 已确认决策

用户于 2026-09-19 明确回复“全部采用现有建议”，D1–D5 已解决。

- D1 "本章/本节将……"导语：S1 A1/B4 列为黑名单；本仓库 `structure-guide.md` 标题后导语规范明确推荐。保留本仓库规则，协议不删导语，S1 该项否决。
- D2 连接词冲突：`academic-style-zh.md` §3.1/§3.3 把 `不仅…而且` / `由此可见` / `综上所述` 列为推荐连接词；S2 与 `deai` 视 `综上所述` 为垫话、`不仅…而且` 为无依据递进。协议区分位置——段内垫话删除，章末小结/结论章首句的 `综上所述` 保留；`不仅…而且` 只在两分句都有证据时保留。本任务不修改 `academic-style-zh.md` §3。
- D3 用户术语表格式：复用 `check_consistency.py --custom-terms` 的 JSON（`{"zh": [[...]], "en": [[...]]}`，扁平化为受保护词集合），一份文件两处可用。
- D4 范例论文指纹（S1 K3）：本任务不引入（需用户提供范例、存在风格复制风险、无现成对应物）。
- D5 模块名：`polish`（与 paper-audit 的 `polish` 模块同名但分属不同 skill，测试按 skill 隔离）。
