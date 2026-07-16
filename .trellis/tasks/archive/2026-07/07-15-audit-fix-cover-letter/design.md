# design.md — cover-letter A-CL-1…11 技术设计

> 所有行号已对照 dev@d3768e4 实读核实。涉及文件全部位于
> `academic-writing-skills/cover-letter/scripts/`（下称 `scripts/`）与 `references/`。

## 0. 改动面总览

| 文件 | 涉及发现 |
|------|----------|
| `scripts/build_letter_claim_map.py` | A-CL-2（strip_tex_comments 单源+main 入口）、A-CL-3（NUMBER_UNIT_PATTERN 单源）、A-CL-9（candidate 增 char_offset） |
| `scripts/align_check.py` | A-CL-2（letter claim 管道剥注释）、A-CL-9（offset→section 映射 + char_offset 输出） |
| `scripts/verify_letter_against_manuscript.py` | A-CL-3（单位边界）、A-CL-4（方向词窗口） |
| `scripts/extract_manuscript_facts.py` | A-CL-3（headline numbers）、A-CL-7（删 fork，阻塞）、A-CL-11（doc 注释） |
| `scripts/journal_fit_check.py` | A-CL-1、A-CL-5、A-CL-6、A-CL-10 |
| `scripts/cover_letter.py` | A-CL-5（--dedup-length 透传）、A-CL-8（_exit_code）、A-CL-10（payload 透传） |
| `references/MODE_GUIDE.md` | A-CL-1（:95 heuristic 改述）、A-CL-5（Mode 2 dedup 指引） |
| `references/CLAIM_EVIDENCE_CONTRACT.md` | A-CL-11（覆盖缺口注记） |
| `references/ISSUE_SCHEMA.md` | A-CL-9（source_section 枚举增 `body`；可选字段增 `char_offset`） |
| `tests/skills/cover_letter/` | 全部新增回归测试（新文件 `test_cover_letter_journal_fit.py` + 扩展既有三文件） |

**不改**：`scripts/parsers.py`、`scripts/tex_loader.py`（vendored，ALIGNMENTS 哈希锁）、
SKILL.md、evals/evals.json、任何 fixture 原文（新夹具全部 tmp_path 合成）。

## 1. A-CL-1 — journal_fit 复用 extract_claims

现状：`journal_fit_check._count_claims`（:106-113）单正则
`\bwe (?:report|present|show|demonstrate|find|propose|introduce|describe|provide)\b`；而
`build_letter_claim_map.LETTER_CLAIM_PATTERNS`（:17-36）覆盖 our-主语、this-work 句式、
数字+方向词句、部署/金额句。

**方案（选定）**：`_count_claims(text) = len(extract_claims(text))`，顶部
`from build_letter_claim_map import extract_claims`。

- import 结构核实：本目录脚本互相 bare import（`align_check.py:23` 已
  `from build_letter_claim_map import ...`；CLI 直跑时脚本目录在 `sys.path[0]`；测试经
  `_load` 把 `SCRIPT_DIR_COVER_LETTER` 插到 `sys.path[0]`）。`build_letter_claim_map` 模块名
  全仓唯一（paper-audit 的叫 `build_claim_map`），无需加入测试 loader 的
  `_SHARED_MODULE_NAMES` 驱逐表。
- 输入核实：`_read_letter_visible` 已产出干净文本（.tex 走 `clean_text`、.md 剥
  frontmatter/heading），`split_sentences` 的 `_SALUTATION_RE` 处理残留称呼 → 直接可用。
- **阈值语义**：`TIER_BUDGETS`（:43-47，top 2-5 / mid 3-6 / conf 2-5）**数值不动**。
  校准实算（fixture 逐句核对）：`journal_fit_fixture_letter.md` 新计数 = 2
  （"We report ALAI…" + "On SWaT-Stream…47%…2.1x faster" 一句）∈ [2,5] → HIGH（旧计 1 →
  假 LOW，即父任务实测的 exit 2 根因）；`align_check_fixture_letter.md` 新计数 = 5
  （we propose / 47% 句 / 2.1x 句 / 73%+modalities 句 / deployed+$1.2M 句）∈ ieee-trans
  [3,6] → HIGH。overpitch 上限分支（>max → MEDIUM）语义保留。
- 文档：MODE_GUIDE.md:95 的 "counts only first-person claim sentences…undercounts"
  改述为 "counts LETTER_CLAIM_PATTERNS claim-bearing sentences（与 align-check 同一抽取器）"。
- 默认行为变化声明：evidence_density 判定面变宽（误报 LOW 修复例外），commit 声明。

**否决项**：在 journal_fit 内扩本地正则 —— 会制造第二份 claim 定义，重蹈本 bug。

## 2. A-CL-2 — .tex letter claim 管道前置剥 `%` 注释

现状核实：`align_check._strip_tex_comments`（:170-181）只喂 disclosure 检查
（:242-243）；claim 路径 `run_align_check`（:304 原文直读 → :311 build_claim_map）与
`build_letter_claim_map.main`（:307 原文直读）都吃到注释行。`presubmission_check`
的 `_strip_latex_comment`（:197-202，`(?<!\\)%`）是行级样板。journal-fit 不受影响
（`_read_letter_visible` .tex 走 `clean_text`，parsers.py:339 已剥注释）。

**方案（选定）**：函数上移单源。

1. 把 `_strip_tex_comments` 原样迁入 `build_letter_claim_map.py`，改名公开
   `strip_tex_comments(text) -> str`（逐行 `(?<!\\)%` 截断，语义零变化）。
2. `align_check.py` 删私有副本，import 复用；disclosure 路径（:242-243）调用点同名替换。
3. 两个 claim 入口 gate by suffix：
   - `build_letter_claim_map.main`：`if letter_path.suffix.lower() == ".tex": letter_text = strip_tex_comments(letter_text)`。
   - `align_check.run_align_check`：已有 `letter_is_tex` 判定（:332 同式）提前到读文件处，
     `.tex` 时以剥注释文本进 `build_claim_map`；传给 `_check_ai_disclosure_consistency` 的
     原文参数不变（其内部自行剥，保持 CL-4 测试语义）。
4. `.md` 不剥——`%` 是正文百分号（"47% reduction" 是 claim 本体）。

方向必须是 build 持有函数：import 方向为 align → build（align_check.py:23），反向会成环。

## 3. A-CL-3 — 数字+单位正则跨文件契约（单源）

三处现状：

| 位置 | 现值 | 病 |
|------|------|----|
| verify:82 | `\b\d+(?:\.\d+)?\s*(?:%\|pp\|x\|×\|ms\|s\|MB\|GB\|FLOPs?)` | 裸 `s`、无词边界、不认 `\%` |
| build:46（ANCHOR metric） | 同上 | 同上 |
| extract:257 | `\b\d+(?:\.\d+)?\s*(?:\\?%\|pp\|x\|×\|ms\|MB\|GB\|FLOPs?)` | 无 `s` 也无边界（`3 ppm`→`3 pp`） |

**契约（选定单源，否决"三处同步常量"——同目录互 import 无障碍，同步注释迟早漂移）**：

```python
# build_letter_claim_map.py — A-CL-3 single source
# `%`/`×` 是非词字符不能带 \b；词字符单位统一 \b 封边，"3 seconds" 命中而
# "3 sensor streams" 不再被捕成 "3 s"；`\\?%` 兼容 LaTeX 转义（下游归一化
# 均已 replace("\\","")，verify:100-104 / extract:265 核实）。
NUMBER_UNIT_PATTERN = r"\b\d+(?:\.\d+)?\s*(?:\\?%|×|(?:pp|x|ms|s|seconds?|MB|GB|FLOPs?)\b)"
```

- 消费点：`ANCHOR_PATTERNS["metric"][0]`（build:46）、`number_patterns[0]`（verify:82）、
  `number_patterns[0]`（extract:257）。money/modality/dataset 等其余 pattern 各文件保持本地。
- `seconds?` 显式收编：旧行为里 "3 seconds" 靠裸 `s` 意外命中，封边后需显式词形保住真阳性。
- **有意分歧（写进代码注释）**：`LETTER_CLAIM_PATTERNS`（build:26-27）的单位子集是
  "数字+方向动词"claim 触发器、无裸 `s` 故无本 bug，不并入单源，避免顺带拓宽 claim 抽取面。
- 已知残留（记录不修）：manuscript 侧匹配是 `str.find(needle)` 子串（verify:120-126），
  claim 若真写裸 "3 s" 仍可能子串命中 "3 se…"；claim 侧封边已消除主要误配路径，
  regex 化 manuscript 匹配属过度工程。

测试对（枚举）：claim "processes a batch in 3 seconds" vs manuscript "3 sensor streams"
→ False；claim "supports 3 sensor streams" 不再产出 metric needle（anchor 类型核对）；
"47 ms"/"5 GB"/"2.1x faster" 保持命中；"3 ppm" 不再命中；extract headline_numbers 对
"47\%" 归一化不变（既有 `test_extract_manuscript_facts_captures_extended_headline_numbers` 锁）。

## 4. A-CL-4 — 方向词-only 分支收紧（CL-1 家族）

现状：`_SPECIFIC_METRIC_RE`（verify:39-43）不含 reduction/improvement（注释 :43-46 明言
这是有意的 direction-only 宽松档）；宽松档 `elif keywords:`（:129-130）允许方向词出现在
数字 ±`_NUMERIC_WINDOW`(160) 的任意位置 → "30% improvement" 可被"30%（抽样比例）…
100 字外的 improvement（另一对象）"验证通过。

**方案（选定，镜像 local_specific 既有机制）**：

```python
_DIRECTION_RE = re.compile(r"\b(?:reduction|improvement)\b", re.IGNORECASE)
_DIRECTION_WINDOW = 60  # 方向名词通常紧跟数字同一小句；60 字符≈一个从句
```

- claim 侧：与 `local_specific`（:109-117）同法，取数字 ±`_CLAIM_METRIC_WINDOW`(40) 内的
  方向词集 `local_direction`。
- manuscript 侧分支序：`if local_specific:` 原 160 窗口全匹配（不动，CL-1 语义）→
  `elif local_direction:` 要求全部方向词落在数字 ±60 子窗口 → `elif keywords:` 原宽松档
  （方向/指标词离数字 >40 的 claim 兜底，防过度收紧）→ `else:` 裸数字存在性（不动）。
- `metric_keywords`（:91-94）列表不改，補注释说明 = specific ∪ direction 的并集关系
  （A-CL-4 的不一致由分支显式化解决，不靠删词）。

回归核对（逐条推演过）：`test_numeric_match_rejects_metric_swap` 三断言——metric swap 走
specific 分支不变；`"47% reduction"` vs `"we report a 47% reduction in latency"`：
direction 词距数字 1 字符 < 60 → True 保持。`test_align_check_numeric_match_requires_local_cooccurrence`：
73% 与 reduction 相距 >160 → 三分支皆 False 保持。新增杀伤测试：60<距离<160 的
不相干 improvement → 由 True 变 False（这是本项的行为变化点，假绿修复例外+声明）。

## 5. A-CL-5 — 长度双报 dedup（presubmission L1 胜出）

事实核实：CLI `--mode optimize`（cover_letter.py:183-201）只跑 presubmission + align，
**不**跑 journal-fit；双报发生在 MODE_GUIDE:123 矩阵声明的 "optimize 时 journal_fit
Optional" 代理工作流（同一 word_limit：journal_fit:287-296 vs presubmission:626-646）。

**方案（选定）**：opt-in flag，默认零变化。

- `run_journal_fit(letter_path, venue, skill_dir, *, dedup_length: bool = False)`；
  `_check_format_compliance(..., include_length=not dedup_length)`——跳过 :287-299 字数
  分支，banned-phrase 分支（:301-315）保留；跳过时 evidence 追加
  `"Word-count check delegated to presubmission L1 (--dedup-length)."`。
- `journal_fit_check.main` 与 `cover_letter.build_parser` 各加 `--dedup-length`
  （store_true）；`_run_journal_fit` 透传。
- MODE_GUIDE Mode 2 步骤与 :123 矩阵行补一句：optimize 会话追加 journal-fit 时带
  `--dedup-length`，长度信号唯一归 `L1`。

**胜出理由**：L1 有 Minor(>1.0)/Major(≥1.2) 两档阶梯 + 精确超字数提示（presubmission:634-645），
journal-fit 只有 MEDIUM/LOW 粗档（:287-299）；且 MODE_GUIDE 矩阵中 presubmission 在
optimize 恒跑、journal-fit 可选——可选者让位常跑者。

**否决项**：(a) journal-fit 永久摘除长度检查——单独跑 journal-fit 会假绿（超长信 format
轴 HIGH）；(b) `_run_optimize` 自动并入 journal-fit findings——超出 dedup 范围的默认行为
变化，违反"新增能力藏 flag 后"约定。

契约测试联动：MODE_GUIDE 出现新 `--dedup-length` 字样 →
`test_mode_guide_flags_all_exist_in_cli` 要求它真实存在于 `cover_letter.py` parser（已计划）。

## 6. A-CL-6 — 顶刊 scope_fit 1-hit=HIGH + 双计分拆除

**方案（选定 1-hit=HIGH，否决扩词表）**：`_check_scope_fit(letter_text, venue, tier)`
增 tier 参数（`run_journal_fit`:382 调用点已持有 tier）；`tier == "top-journal"` 时
`len(hits) >= 1 → HIGH`，0 hit 仍 LOW；其余 tier 维持 2/1/0 → HIGH/MEDIUM/LOW。
理由：350 词硬顶（templates/nature.md:4 + JOURNAL_TIERS.md "≤350 words. Editors expect
tightness"）下要求两个 scope 关键词与"信息密度优先"的顶刊文风冲突；扩词表主观且会随
venue 漂移，1-hit 规则可被单条校准测试钉死。

**双计分（原审计 finding 8）**：1-hit=HIGH 本身**不解决**反而放大 "broad scientific"
双计分（一词既拉满 scope 轴又计入 novelty paradigm_signals）。补充修复：从
`_check_novelty_framing` 的 paradigm_signals（journal_fit_check.py:173-176）删去
`broad scientific`——它是 scope 词汇，混在 resolve/answer/establish/address/reframe/paradigm
这组范式动词里本就归类错误。删除后一词只贡献 scope 轴，双计分拆除。

回归核对：`journal_fit_fixture_letter.md` 无任何 scope 词与范式动词（逐词核对）→
scope LOW、novelty LOW、overall LOW 不变，`test_journal_fit_classifies_low_for_underframed_nature`
与 `test_journal_fit_cli_json_emits_axes` 保持绿。行为变化点（顶刊 1-hit 由 MEDIUM→HIGH；
含 "broad scientific" 信的 novelty 少一个信号）按误报修复例外双声明。

## 7. A-CL-7 — 删 `_extract_title_local` fork（阻塞批次）

上游契约：A-EN-10 修 canonical `extract_title` 非贪婪截断（cover-letter 副本现状
parsers.py:605 `\{(.+?)\}`）+ en/audit/cover-letter 三副本重同步。本任务**只消费**同步
结果，不改 parsers.py。

执行前置检查（批次入口）：

1. `git log --oneline -- academic-writing-skills/cover-letter/scripts/parsers.py` 确认
   EN 任务同步 commit 已达；`uv run --extra dev python -m pytest tests/contracts/test_parsers_alignment.py -q` 绿。
2. 关键行为探针：用 `thanks_author_fixture.tex` 直接调 canonical `extract_title`，看输出
   是否已剥 `\thanks` 资助文本。

两分支预案（fork 的价值 = 平衡花括号 **+** `\thanks/\footnote` 剥离，:224-240 docstring 自述）：

- **分支 A**（canonical 输出已无 `\thanks` 泄漏）：整删 `_extract_title_local`，
  `extract_facts` 改调 `parsers.extract_title`；同时清理 import 面（`_extract_balanced_block`
  等若因此闲置则按"自己改动产生的孤儿"原则移除）。
- **分支 B**（canonical 平衡提取但不剥 thanks——按 EN design §4 的 R10 用例含 thanks/footnote
  剥离，此分支**不应发生**）：视为 A-EN-10 未按前置契约落地，回到 EN 任务补齐后重走分支 A；
  本任务不得以缩薄 fork 收尾归档（prd 验收 v2.3：无 blocked 完成分支，终批禁改行为代码）。
- 判据即测试：`test_extract_title_strips_thanks_and_keeps_nested_braces`（NSF/supported
  不得入 title）与 `test_extract_manuscript_facts_returns_expected_shape` 双绿为准。

## 8. A-CL-8/9/10 — 小修

- **A-CL-8** `cover_letter._exit_code`（:38-47）：

  ```python
  def _severity(finding: Any) -> str:
      if isinstance(finding, dict):
          return str(finding.get("severity", "")).lower()
      return str(getattr(finding, "severity", "")).lower()
  ```

  消灭 `"" or finding.get(...)` 对 dataclass 的 AttributeError 路径；返回逻辑（major→2/
  非空→1/空→0）不变。
- **A-CL-9** `source_section` 位置化（管线现状核实：`split_sentences`（build:69-72）
  `replace("\n", " ")` 丢换行、candidate 仅带序号 `id: letter:{index+1}`（build:253），
  全管线无任何 char offset / 行号；`verify_claim_candidates` 用 `dict(candidate)` 浅拷贝
  （verify:173），additive 键自然透传）。三步：

  1. **补位置**（`build_letter_claim_map.py`）：新增 `_locate_sentence(sentence, text,
     start) -> int`——token 化后 `re.escape` + `\s+` 连接的宽松正则（抵消 split_sentences
     的换行归一化），配 moving cursor（`start`）防重复句错配；`build_claim_map` 为每条
     claim 计算 `char_offset`（相对传入的 letter 文本；定位失败 = -1）写入 candidate
     （additive 键，`id`/`section_key` 等既有键不动）。
  2. **位置→section**（`align_check.py`）：新增 `_source_section_for_offset(offset,
     letter_text) -> str`，结构模型 per `references/LETTER_STRUCTURE.md` 五段式，只用
     结构标记不用 claim 关键词：`_SALUTATION_RE`（自 build import）搜称呼终点，offset
     在其前 → `header`；空行（`\n\s*\n`）切段，称呼后第一段 → `opening`；新增
     `_VALEDICTION_RE`（`^(?:Sincerely|Best regards|Kind regards|Yours (?:sincerely|
     faithfully)|Respectfully)\b`，MULTILINE|IGNORECASE）首个落款行起 → `closing`；
     其余段落或 offset == -1 → `body`（诚实回退标签）。`run_align_check` 用与
     build_claim_map **同一份文本**调用映射（A-CL-2 后 `.tex` 为剥注释文本，offset
     语义一致——依赖批次 1 先行，顺序已满足）；`candidate_to_issue(candidate, facts,
     letter_text=None)` 增默认参数，None 时回退 `body`（既有直调用例不破）；
     `AlignCheckIssue` 末尾追加 `char_offset: int = -1`（带默认值，既有构造点零改动），
     JSON（asdict）自动带出。
  3. **schema**（`references/ISSUE_SCHEMA.md`）：`source_section` 枚举补 `body`（脚本侧
     诚实回退标签），Optional fields 表补 `char_offset`。

  **有意不做**：`contributions`/`fit`/`declarations` 的关键词推断（语义启发式冒充位置，
  评审已否决）；markdown 标题映射（两个 fixture 信均为纯散文段落，无标题可锚）。
  纯 `.md` 散文信的交付物 = `opening`/`closing` 结构判定 + 中间段 `body` 回退 + 精确
  `char_offset`。这是 Low 项，不重构 claim 管道。
- **A-CL-10** `run_journal_fit`（:379）：`tier_missing = not meta.get("tier")`；
  `JournalFitResult` 增 `warnings: list[str] = field(default_factory=list)`；缺失时写
  `"Template `<venue>` frontmatter has no `tier`; defaulting to mid-journal."`。
  渲染：`_format_protocol` 加 `% JOURNALFIT [Warning] ...` 行；`main` 的 JSON dict 与
  `cover_letter._run_journal_fit` payload 增 `"warnings"` 键（additive，不动既有键）。
  内置十模板均有 tier（`test_templates_have_valid_frontmatter` 锁定）→ 默认输出零变化。

## 9. A-CL-11 — doc-only 处置与理由

`extract_manuscript_facts.py:42-46` 已记录反捏造决策：free-text 回退曾从
`\thanks{Corresponding author: a@u.edu}` 刮出邮箱 local part 报成作者，故意移除。
IEEE `\thanks` / acmart `\authornote` 里的通讯作者标注属同一风险面——**不扩猜测式提取**，
维持"显式 `\corresponding` 命令，否则回退第一作者"。

落点：(1) `CORRESPONDING_AUTHOR_PATTERNS`（:47）上方注释补一句覆盖缺口 + 指回 :42-46
理由；(2) `references/CLAIM_EVIDENCE_CONTRACT.md` 增两行 "known extraction gaps"；
(3) 表征测试：acmart `\authornote{Corresponding author: x@y.edu}` → corresponding =
第一作者且不含 `@`（与既有 `test_extract_corresponding_author_never_scrapes_thanks_email`
构成 IEEE/acmart 双模板锁，锁的是"缺口存在且回退安全"这一文档化行为本身）。

## 10. 测试装载与新文件

- 新文件 `tests/skills/cover_letter/test_cover_letter_journal_fit.py`（A-CL-1/5/6/10）：
  复制既有 `_load` 惯用法（importlib spec_from_file_location + `_SHARED_MODULE_NAMES`
  快照/对称恢复，命名空间前缀 `_cl_jf_`），路径常量取自 `tests.support.paths`；含加载
  守卫用例 `assert hasattr(module, "TIER_BUDGETS")`。
- A-CL-2/3/4 → 扩展 `test_cover_letter_align_check.py` / `test_cover_letter_scripts.py`；
  A-CL-8/9/11 → `test_cover_letter_scripts.py`。全部夹具 tmp_path 合成，不动 evals/。

## 11. 风险与回滚

| 风险 | 缓解 | 回滚 |
|------|------|------|
| A-CL-1 抬高 claim 计数 → 长信落 overpitch MEDIUM | 校准测试锁两 fixture 为 HIGH；MEDIUM 分支语义未变 | 按批次 2 文件集自快照还原 |
| A-CL-3 封边漏掉真实裸 `s` 写法 | `seconds?` 显式收编 + 测试对枚举；残留写进注释 | 单源常量一处还原即全还原 |
| A-CL-4 过度收紧误杀真陈述 | 保留 `elif keywords` 兜底档 + `_DIRECTION_WINDOW=60` 由正反测试钉住 | 按批次 1 文件集自快照还原 |
| A-CL-6 顶刊 1-hit 放松过度 | 0-hit 仍 LOW；fixture 负例锁定 | 参数化改动小，还原即复原 |
| MODE_GUIDE 改动触发 flag 契约测试 | `--dedup-length` 先落 parser 再写文档；跑 `test_mode_guide_flags_all_exist_in_cli` | 文档行随批次文件集还原 |
| A-CL-7 上游未剥 thanks | 回开 EN 任务补齐（分支 B 不落地），Batch 1-3 十项不受阻塞 | 本任务保持 in_progress 至 Batch 4 完成，不提前归档 |
| 全局 | 每批次以 validation gate 收口并登记拟提交分组（文件集 + 拟 commit message）+ `git stash create` 快照；实际 `git commit` 统一延至 Phase 3.4（.trellis/workflow.md） | `git checkout <上一批次快照> -- <批次文件集>`（跨批次共享文件以快照为基准，不误伤已过 gate 的批次） |
