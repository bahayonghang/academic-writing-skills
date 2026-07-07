# Design: cover-letter AI 披露一致性 + 结构级 AI 痕迹

Evidence: `../07-05-skills-deep-analysis-optimization/research/bib-cover-findings.md` (CL-3 / CL-4)

## 0. 总原则

- 只报告不改写（R3）：两项新能力都只产出 finding（`source_kind="script"`），走既有 ISSUE_SCHEMA / protocol 输出，不触碰信件或稿件内容。
- 不新建 `deai_check.py` 副本：CL-3 是把 en 结构壳检查中**适合信件体裁的两项**裁剪移植进 `presubmission_check.py`，以信件域常量实现。因此 `tests/test_deai_alignment.py` 的锁范围不变，无需新增"有意分歧"条目（锁只锁 en/zh/typst 的 deai 副本；cover-letter 没有 deai 副本）。此结论回应 PRD Notes 第 2 条。
- 不加 CLI 旗标、不改 exit-code 语义：新检查内嵌进 `run_align_check()` / `run_checks()`，`generate`/`optimize` 的默认集成自动获得。

## 1. CL-4（先做）：AI 披露一致性 lane

### 位置与数据流

`align_check.py` 新增 `_check_ai_disclosure_consistency(letter_text, manuscript_text) -> AlignCheckIssue | None`，在 `run_align_check()` 的 claim 循环后调用、结果追加进 issues。该函数两个输入在 `run_align_check` 中现成（`letter_text` 原文 + `load_manuscript_text` 展开后的稿件全文）。

### 检测逻辑

- 模式单源：`from presubmission_check import DECLARATION_PATTERNS`，用其 `ai_disclosure` 家族做"存在性"判定（同目录 bare import，与现有 import 约定一致；presubmission_check 模块 import 无副作用）。
- 极性分类（`_ai_disclosure_polarity(text) -> "positive" | "negative" | "absent"`）：
  - 新增小型 `NO_AI_PATTERNS`（如 `no (?:generative )?ai`、`did not use`、`without (?:the use of )?(?:generative )?ai`）；任一命中 → `negative`。
  - 否则 `ai_disclosure` 家族任一命中 → `positive`；都不中 → `absent`。
  - 已知局限（记录在 docstring）：同侧混合陈述（"用了 ChatGPT 润色 + 分析未用 AI"）按 negative 归类，属启发式；finding 引用原句，用户可见可判。
- 预处理：稿件侧逐行剥 `%` 注释（防止匹配到被注释掉的披露语句）；信件侧仅当 `.tex` 同样剥注释，`.md` 原文。
- 三情形（均 severity=`moderate` / P2，对应 PRD "medium"）：
  | 情形 | quote | evidence_anchor |
  |---|---|---|
  | 稿件有、信无 | `""`（信中无可引；这正是问题本身） | 稿件披露句（`_sentence_around` 取整句，截 280） |
  | 信有、稿件无 | 信中披露句 | `[{type:"missing",...}]` |
  | 两侧极性矛盾 | 信中披露句 | 稿件披露句 |
- 两侧都 `absent` → 不产 finding（venue 是否要求披露由 presubmission 的 `D-ai_disclosure` 模板驱动检查负责，职责不重叠）。
- 字段：`comment_type="disclosure_consistency"`（ISSUE_SCHEMA 枚举扩一项，见 §3）、`manuscript_section_anchor="none"`、`confidence="high"`（正则直接命中）、`claim_strength="observed"`、`quote_verified` 按 quote 是否非空。

## 2. CL-3：AI-tone 阈值 + 结构壳（`presubmission_check.py`）

### 2.1 同词阈值 3+ → 2+（取舍：固定 2，不做长度自适应）

- `_scan_ai_tone`：`>=3` 保持 Major/P1（现行为不变，回归安全）；`==2` 新增 Minor/P2。
- **取舍理由（PRD R2 要求写明）**：信件体裁长度方差天然小（模板 word_limit 200–500；且 AI-tone 检查在无 `--journal` 时也要跑，拿不到 word_limit 基准）。长度自适应会引入"无模板时用什么基准"的额外配置维度，而 ≤600 词里同一促销词出现 2 次已是明确信号。选固定 2：确定性、无配置、行为可测。

### 2.2 新增聚合多样性检查（code `AI-DIV`）

- 统计 `BANNED_TONE_PATTERNS` 中"至少命中 1 次"的**不同词条数** d：
  - d ≥ 4 → 一条 Major/P1；d == 3 → 一条 Minor/P2；d < 3 → 不报。
  - finding 列出命中的词条与各自次数，quote 取首个命中词。
- 动机：研究结论"词汇多样的 AI slop（每词各 1 次）整体漏过"。与 per-term 检查语义不重叠（repetition vs. diversity），两者可同时触发，消息文案区分。
- 边界取舍：3 档设 Minor 而非 Major，因合法 ML 信件可能自然含 "state-of-the-art"+"superior"+1 个其他词；4 个不同促销词密度在 ~300 词信里几乎必是模板腔。

### 2.3 结构壳移植两项（en → 信件域裁剪）

| en 检查 | 移植 | 参数（信件域） | 理由 |
|---|---|---|---|
| `_check_burstiness` 平行段首 | ✅ `S1` Minor/P2 | window=3 连续段、段首 key=前 2 个词 token（与 en pin 同值，跨技能语义一致） | 信件仅 3–6 段，3 连同头（如 "Our approach …"×3）高信噪；声明段惯用 "We confirm/We declare" 在 k=2 下不同 key，不误报。复用现成 `_paragraphs(views)`，跳过 `Dear` 称呼段 |
| `_check_sentence_length_variance` 句长 CV | ✅ `S2` Minor/P2 | 全信级（不分节）；句数 ≥8 才计；CV < 0.25 报 | en 默认 min=5/CV<0.30 且 tier 门控；信件样本短、CV 噪声大 → 抬 min 至 8、收紧阈值至 0.25 压误报。cover-letter 无 tier 体系，默认开启，由零误报验收样例约束 |
| `_check_throat_clearing` | ❌ 不移植 | — | 信件体裁等价物已有：`L2` opener 陈词 + `G3` 弱转折段首；再加会双报 |
| `_check_low_information_density` | ❌ 不移植 | — | 信件的声明段合法地"模板化且无 evidence marker"，≤400 词里误报风险高、增量信号低 |

- 新 code 登记：`_comment_type_for_code`（`S1`/`S2`/`AI-DIV` → `"tone"`）与 `_title_for_code` 各补分支。
- 阈值以模块常量实现（不引 YAML）：信件单体裁，en 的 tone-thresholds.yaml 是为论文分节/分 tier 服务的，这里引入即过度配置。

## 3. 契约与文档同步

- `references/ISSUE_SCHEMA.md`：`comment_type` 枚举加 `disclosure_consistency`，语义行 + severity guidance（moderate 档）补一句。
- `references/PRESUBMISSION_RULES.md`：G4 行改为 2+/3+ 阶梯；新增 `AI-DIV`/`S1`/`S2` 规则行与参数、取舍摘要（含"为何不移植 throat-clearing / LID"）。
- `SKILL.md`：presubmission 能力行（≈L39）补 "structural AI-trace checks"；align-check 描述（≈L31/68 区域）补 "AI-disclosure consistency"；`last_updated` 已是 2026-07-06 无需动；**version 不动**（全仓同步规则）。
- `references/MODE_GUIDE.md`：align-check 模式段如列 lane 清单则补一行（实施时核对）。
- ⚠️ SKILL.md 若涉及表格改动，注意全局格式化 hook 对齐表格触发 ROUTER_ROW_RE 契约测试的既有陷阱（memory：skill-md-formatter-gotcha）。

## 4. 测试与 evals

### 单测（根 `tests/`，沿用 importlib spec_from_file_location 装载模式；fixture 字符串一律 raw string）

- `test_cover_letter_align_check.py` 追加（CL-4）：稿件有信无 / 信有稿件无 / 极性矛盾（信 "no AI" vs 稿件 "ChatGPT for editing"）→ 各 1 条 moderate `disclosure_consistency`；两侧一致披露、两侧全无 → 0 条该类 finding；注释掉的稿件披露（`% We used ChatGPT...`）不触发。tmp_path 内联最小 .tex/.md。
- `test_cover_letter_presubmission.py` 追加（CL-3）：同词 2 次 → Minor、3 次 → Major（回归）；3 个不同词各 1 次 → AI-DIV Minor、4 个 → Major；3 连同 2-token 段首 → S1；~10 句等长句 → S2；一封自然多变的人写信 → S1/S2/AI-DIV/AI\* 全零（零误报守卫）。

### evals（验收标准第 2 条）

- 新 fixtures：`evals/fixtures/ai_slop_letter.md`（多样促销词各 1 次 + 3 连平行段首 + 均匀句长）、`evals/fixtures/human_letter.md`（具体、多变、无促销词）、`evals/fixtures/disclosure_fixture.tex`（含 acknowledgments AI 披露句的最小稿件）。
- `evals.json` 追加 3 条：#7 presubmission(ai_slop_letter) → regex 命中结构 trace（`S1|S2|AI-DIV`）；#8 presubmission(human_letter) → not_contains `[S1]`/`[S2]`/`[AI-DIV]`；#9 align-check(align_check_fixture_letter.md × disclosure_fixture.tex) → regex 命中 disclosure 一致性 finding。
- ⚠️ `evals.json` 禁 Edit/Write（JSON hook 压平数组），走 `Bash` python json 读改写（memory：evals-json-formatter-gotcha）。

## 5. 兼容性与风险

- `optimize_fixture_letter.md` 本就 slop 浓：新检查可能在既有 eval/测试输出里多出 finding。evals 断言全是"存在性 regex"，多 finding 不破坏；单测如有精确计数/绝无断言，实施时先核对断言意图再更新期望（宁改期望不改 fixture 语义）。
- `align_check_fixture_letter.md` × `generate_fixture.tex` 两侧均无披露 → CL-4 不产新 finding，既有 align-check 测试不受扰动。
- exit code：AI-DIV/S1/S2 多为 Minor，不改变现有 fixture 的 exit-code 期望；出现 Major（≥3 同词已是现行为）语义不变。
- 性能：新增均为对 ≤1k 行文本的常数次正则扫描，可忽略。

## 6. 验收对照（PRD Acceptance Criteria）

1. 三情形披露 finding → §1 三情形 + 单测三断言。
2. AI 样例 ≥1 结构 trace、人写样例零误报 → §4 evals #7/#8 + 单测零误报守卫。
3. `just ci` 全绿；不改 en/zh/typst 任何代码 → 改动面限定 cover-letter skill 目录 + 根 tests/ 两个既有测试文件。
