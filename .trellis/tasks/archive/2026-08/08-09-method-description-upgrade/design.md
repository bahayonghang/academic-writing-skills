# 父任务技术设计：方法描述模块升级（共享判定·唯一权威）

子任务 design.md 只写各自实现细节，**不得复述或改写本文件 §2 判据**（引用节号）。机制事实
与行号证据见 `research/repo-recon.md`（下称 recon）。

## 1. 四层架构

```text
第 1 层 参考文件（LLM 车道判断力）
  zh:    references/writing/method-description-guide-zh.md（新建）
  en:    references/writing/section-writing/method.md（扩展）
  typst: references/METHOD_SECTION.md（新建，authoritative = EN，路径小写）
第 2 层 脚本候选检查（[Script] 车道，恒 NEEDS-LLM）
  zh:    analyze_logic.py --method-narrative + 显式 --section 选章（沿 --process-chapter 先例）
  en/ty: analyze_logic.py --section methods 分支内新增（反向门控 if section == "methods"）
第 3 层 工作流接线
  SKILL.md Reference Map + zh 路由行；改写顺序按 spec §10：
  先总体数据流与模块过渡 → 再模块内部句子 → 最后调整标题
第 4 层 paper-audit（能力命名："方法论接口与论证完整性"，见 §5）
  focus block + C5 模块粒度 + Phase 0 logic 双调用与解析升级
```

## 2. M-* 判据表（唯一权威；跨技能同名同义，由 C2 契约测试锁定）

### 2.1 M-HEADING（Minor / P2）

- 结构判据（全语言统一）：方法作用域内，**连续 ≥3 个行内小标题段**（遇 `\subsection` 级及
  以上标题清零；中间普通段不清零），**且其中 ≥2 个**小标题后首句命中报幕句式 → 报 1 条
  （定位首个命中处，消息含计数）。阈值 3/2 定死，不开参数。
- 行内小标题识别：
  - zh/en：行首 `\paragraph{...}`。
  - typst：段首 `\*[^*\n]+[.。]\*` 强调句。
- 报幕句式正则：
  - zh：`(?:本|该)(?:模块|节|方法)?(?:主要)?(?:用于|负责|旨在|是为了)`
  - en/typst：`\b(?:This|The)\s+(?:module|component|stage|block)\s+(?:is used to|aims to|is responsible for|serves to)\b`
    或 `\bWe\s+(?:now\s+)?(?:introduce|describe|present)\s+the\b.{0,40}\b(?:module|component)\b`

### 2.2 M-SEQWORD（Info / P3）

- 对象：方法作用域内小节标题（zh/en `\subsection`/`\subsubsection`；typst `==`/`===`）后
  首个自然段的首句。
- 触发：首句命中顺序词起手且整句无因果/约束词。
- 顺序词起手：
  - zh：`^(?:接下来|然后|随后|在.{0,12}(?:之后|基础上))[，,]?\s*本(?:节|小节|部分)(?:将)?(?:介绍|给出|阐述)`
  - en/typst：`^(?:Next|Then|Subsequently|After (?:that|this)),?\s+(?:we|this section)\b`
    ——该词组并入 TRANSITIONS 新增 `sequence` 类（单一来源，见 §6）。
- 因果/约束免除词：
  - zh：`因此|由于|为(?:了)?(?:解决|克服|消除|获得)|仍|然而|但`（与 logic-coherence.md 信号词表对齐）
  - en/typst：`therefore|thus|however|to address|due to|because|since|remaining`

### 2.3 M-EQUATION（Minor / P2）

- 对象：
  - zh/en：编号公式环境 `equation`/`align`/`gather`（带 `*` 不计）。
  - typst：**带 `<label>` 的块级 `$ ... $` 公式**（决策定稿：编号取决于模板级
    `#set math.equation(numbering:)`，逐式判定不可静态可靠；labeled ⇒ 被引用 ⇒ 必然编号，
    label 可正则稳定解析。未 labeled 的块公式不查——宁漏勿误）。
- 触发：公式块结束后 **3 个非空可见行**内无释义引导词（zh：`式中|其中`；en/typst：`where`）。
- 连续多式共享释义块只判块尾一次（GB/T 多式合并释义合法）。
- 公式前目的句与下游用途判断留 LLM（参考文件承载）。

### 2.4 M-EDGETABLE（骨架输出，非 finding）

方法作用域内输出：小节标题清单 → 相邻对空白接口表（Markdown 列：上游小节｜上游产出｜
连接类型｜中间变换｜下游用途；后四列留空），尾注 `[LLM] 待填写`。位置在诊断输出末尾。

### 2.5 作用域（门控）

- zh：`--method-narrative` **必须**配 `--section <中文章名/英文键>` 显式选章（复用现有
  `--section` 语义，recon §2.2；一次一章，多章多次调用）。缺 `--section` 时：不猜章，
  打印候选章清单后非零退出。候选线索（仅提示不判定）：标题含 `方法|原理|设计`（parser
  正则）∪ 含实验节（EXP_SEC_RE）− NON_METHOD_CHAPTER_RE。单章文件照旧配 `--first-chapter`。
- en/typst：`--section methods`（现有节门控分支）；无 `--section` 或其他节值不跑 M-*。

### 2.6 跨技能契约锁（C2 交付）

新契约测试 `tests/contracts/test_method_narrative_alignment.py`：importlib 加载三份
analyze_logic 副本，断言——结构常量（3/2 阈值、后视 3 行）三方相等；en/typst 全部 M-* 正则
源串逐字相等；zh 中文正则存在且结构常量一致。锁定后 C3 集成验收不再依赖人工 diff。

## 3. 报幕反模式边界（红线负例，三技能 fixture 均锁）

行内小标题三处合法用法不得触发（recon §2.5）：EN/typst Related Work 分组标题、typst 实验
分析段 lead-in、zh `\paragraph{核心结论概括}`。参考文件明写："标题只负责导航，被禁的是
报幕句替代因果衔接，而非行内小标题本身"。en/typst 由 `--section methods` 门控天然排除，
zh 由显式选章排除；fixture 仍须锁定，防未来门控松动。

## 4. 证据分级映射（不建第二套体系）

spec §6 四类主张（定义事实/机制级作用/经验性能/因果归因）作为主张类型前置分类：
en/typst 映射 `claim-evidence-contract.md` 强度梯 + over-claim-guard 措辞；zh 映射
`references/writing/over-claim-guard.md`。参考文件只加映射表与互链。zh 词表扩条目为可选项，
非本任务范围。

## 5. paper-audit 共享判定（细节在 C3 design）

- 能力命名：**方法论接口与论证完整性**。审计侧全部产物（focus block、C5 增补、
  DEEP_REVIEW_CRITERIA、REVIEW_LANE_GUIDE）不得出现"写作质量/叙述质量"措辞
  （recon §2.6 两 agent DON'T 冲突）；报幕句式类风格判据只在 Phase 0 脚本车道出现。
- Phase 0 定稿：**委托 + 双调用**。原全文调用（`--cross-section`）保持不变；对 EN/typst
  文档新增第二次调用 `--section methods`，两次输出合并为 LOGIC 模块 issue。zh 文档不做
  第二调用（显式选章在 audit 无章号语境），此边界写入 paper-audit 文档为已声明限制。
- 解析升级：`_parse_script_output` 增块感知（finding 头行开 issue，
  Current/Suggested/Rationale/Meaning-Check 续行并入同一 issue）+ severity 识别扩 `Info`、
  priority 扩 `P3`；Info 不参与 ScholarEval 扣分。此修复改变现有委托检查的 issue 计数与
  分数基线——回归策略与影响面收敛见 C3 design（本任务只保证 logic 链正确，见 recon §4.3）。

## 6. 与既有能力的分工边界（防重复）

| 既有能力 | 边界 |
| --- | --- |
| zh S1 `_check_heading_leads`（标题后导语存在性/长度） | M-HEADING 查报幕密度+句式，互补 |
| zh 章引言承上启下（章级） | M-* 查章内模块间衔接 |
| EN Module Triad + 逐模块预写表 | 扩展逐边视角，原表保留 |
| EN flow.md / audit C5（段落级）、C3（章级） | M-EDGE 填模块级空隙 |
| deai throat_clearing / Declarative scaffolding | AI 痕迹句式；报幕句不在其词表，M-HEADING 补位 |
| EN/typst TRANSITIONS | 仅新增 `sequence` 类（M-SEQWORD 依赖；`example` 类缺口进遗留清单） |

## 7. 契约锁与同步动作链

见 recon §2.3-2.4 与 `.trellis/spec/academic-writing-skills/docs-bilingual-resources.md`。
要点：双语方向 = 源语言页一致镜像 + 另一语言完整翻译；paper-audit 的 references 与 agents
改动同样走 manifest + 双语全链；双语校验不在 `just ci`，各子任务须显式跑
`check_resource_sync.py --skill <skill>`，C3 终检加全量 checker + `just doc-build`。

## 8. 提交纪律

实施代理（trellis-implement）不执行 git commit。各子任务 implement.md 中的"提交分组"仅为
Phase 3.4 主会话提交时的分组建议与回滚边界。

## 9. 借鉴取舍与证据状态

见 `research/external-sources.md`（adapt/reject/原创点/missing evidence）。
