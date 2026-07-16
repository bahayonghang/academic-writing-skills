# bib查询解析健壮性修复

## Goal

修复 bib-search-citation 六项审计发现（父任务 `07-15-skills-deep-audit-opt` 登记表 A-BIB-1 ~ A-BIB-6，含决策 D4）：shlex 撇号崩溃、preview 丢 warnings、`has:code` 子串误判、year 消歧后缀、非整数过滤值裸 ValueError、含冒号自由文本被静默重解释。

## 范围与红线

- 只改 `academic-writing-skills/bib-search-citation/` 下的 `scripts/`、`references/`、`tests/`。
- **不改 SKILL.md**（version 归 07-15-audit-fix-version-ci 按 D1 统一处理；last_updated 归父任务集成阶段按 D6 处理；SKILL.md 有 contract 字符串锁）。
- 不静默改变过滤语义（A-BIB-6 按父任务处置为 doc-first + 警告扩展，不改 `FIELD_OP_RE` 的解析结果）。
- 错误出口契约不变：spec 类错误 → stderr JSON `{"error": ...}` + exit 2（`search_bib.py:1414-1420`）。

## Requirements

### R1（A-BIB-1，High）：compact query tokenizer 容错不配对引号

- 现状（已实测复现）：`search_bib.py:499` `shlex.split("children's early language")` 抛 `ValueError: No closing quotation`，被 `main()` 捕获后 exit 2，含撇号的正常英文查询完全不可用。
- 要求：
  - `shlex.split` 失败时回退到自定义正则切分（保留双引号短语分组、单引号按字面处理），**不报错、exit 0**。
  - 回退发生时向 `meta.parse_warnings` 追加一条 `{"type": "query_tokenizer_fallback", "message": ...}` 警告。
  - 正常路径（引号配对）行为零变化：`claim:"low latency"` 等双引号短语分组在正常与回退两种模式下均保持。

### R2（A-BIB-2，Medium）：preview 呈现 warnings

- 现状：`preview_bib_search.py:169-190` `render_preview` 不渲染 `meta.parse_warnings` 与 per-result `warnings`，broken.bib 的预览看起来干净，违反 SKILL.md 安全边界「.bib 畸形时须报告条目可能被跳过」（SKILL.md:127-128）。
- 要求：
  - `meta.parse_warnings` 非空时渲染 `Warnings` 区块，风格与现有行式渲染一致；最多显示 5 条，超出部分显示 `... and N more` 指回 JSON。
  - per-result `warnings`（如 duplicate_key，`search_bib.py:1268-1275` 生成）逐条渲染在该条目块内。
  - `meta.encoding_fallback` 存在时渲染一行编码回退提示。
  - 无 warnings 时输出与现状完全一致（现有 preview 测试逐字符断言不受影响）。

### R3（A-BIB-3，Medium，按 D4）：`has:code` 词表逐词界定匹配语义

- 现状（已实测复现）：`has_code`（`search_bib.py:975-977`）对 `CODE_HINT_TERMS`（:130-138）做裸子串匹配，`code`→encoder/barcode、`repo`→reported 均误判：`"reported results"`、`"encoder-decoder"`、`"barcode"`、`"we encode the signal"` 全部返回 True。
- 要求：
  - 按 D4 对**整个词表逐词**定义匹配语义（见 design.md 词表），统一为词边界匹配（短语按带边界的词序列匹配），不允许残留任何裸子串项。
  - 新增词表项 `codeavailable`：Zotero 惯用 tag `CodeAvailable`（本仓 fixture 与 query-syntax.md 示例均在用）在词边界下会丢失，须显式保留为真正例。
  - 负例测试（必须为 False）：`"reported results"`、`"encoder-decoder"`、`"barcode"`、`"we encode the signal"`。
  - 正例测试（必须为 True）：`"code available"`、`"github.com/x"`、`"source code released"`、`"CodeAvailable"`。
  - fixture 端到端稳定性：library.bib 三条目 `flags.code` 修复前后一致（已验证：Doe/Roe/Lee 均 True→True），`has:code` 过滤结果集不变。
  - 残留局限写入 `references/limitations-and-errors.md`：词边界不解决语义否定（"without a linked repository" 仍为 True）与泛词（"dress code"）。

### R4（A-BIB-4，Medium）：YEAR_RE 接受消歧后缀

- 现状（已实测复现）：`YEAR_RE`（`search_bib.py:31`）尾部 `\b` 使 `year={2024a}` 解析为 None，被任何年份过滤静默排除。
- 要求：
  - `entry_year`（:951-956）对 `year={2024a}` 返回 `2024`（int）；适用字段保持现状不变：先 `year` 后 `date`。
  - 后缀定义：单个小写 ASCII 字母 `[a-z]`（BibTeX 消歧惯例）；`2024-06-15` 等日期形式行为不变；`20245` 仍不得误配。

### R5（A-BIB-5，Low）：非整数值转 SpecError

- 现状（已实测复现）：`parse_query_token` 中 `limit:abc`（:565）、`recent:x`（:576）及 `parse_year_filter` 中 `year:20x4`（:627/:629/:635）抛裸 `ValueError: invalid literal for int() ...`，用户看到的是 Python 内部话术。
- 要求：三处 `int()` 包装为 `SpecError`，措辞与 `validate_spec:287-289` 已验证路径一致（`"limit must be an integer, got {value!r}"` 风格）；exit 2 + stderr JSON 形状不变。

### R6（A-BIB-6，Low，doc-first）：含冒号自由文本的重解释

- 现状（已实测核实，**与父任务登记表有一处偏差**）：`FIELD_OP_RE`（:27-29）要求 field 以 `[A-Za-z_]` 开头，因此 `10:30` **不会**被重解释（保留为自由文本，已实测）；`genotype:phenotype` 会被静默转成 `field_contains` 过滤并从相关性评分中消失（已实测）。
- 要求：
  - `references/query-syntax.md` 新增「Colons in free text」小节：精确说明哪类 token 会被解释为字段过滤（字母/下划线开头）、哪类不会（数字开头如 `10:30`）、被重解释的后果（不参与评分）、以及规避方式（冒号改空格；评分 tokenizer 本就按非字母数字切分，语义无损）。
  - 扩展现有 `unknown_field_filter` 警告（`search_bib.py:1334-1343`）：message 增加「若是自由文本请把冒号改为空格」的指引；**warning `type` 不变**（现有测试 `test_typo_field_filter_emits_warning` 断言 type），过滤语义不变。

## Acceptance Criteria

- [ ] R1–R6 每项（含 Low 的 R5/R6）都有对应回归测试落在 `academic-writing-skills/bib-search-citation/tests/test_bib_search.py`，且新测试在修复前会失败（tests-first 验证过）。
- [ ] R3 的四个负例、四个正例全部过测；library.bib 三条目 `flags.code` 与 `has:code` 结果集修复前后一致。
- [ ] 现有 28 项 bib 测试（含 broken.bib / phantom.bib / quote_trap.bib fixture 测试）全部保持绿色：`uv run --extra dev python -m pytest academic-writing-skills/bib-search-citation/tests -q`。
- [ ] 无 warnings 输入时 preview 输出与修复前逐字节一致（现有 preview 断言不改动即通过）。
- [ ] 错误出口契约不变：所有 SpecError 路径 exit 2 + stderr JSON `{"error": ...}`；tokenizer 回退路径 exit 0。
- [ ] SKILL.md 零改动；`references/` 文档改动与代码行为一致。
- [ ] `just ci` 除终批 R4a 承接的双语资源同步原因外全绿。实施中复核
  `.trellis/spec/academic-writing-skills/docs-bilingual-resources.md` 后确认：本任务必须修改的两份
  source reference 已进入 `docs/resource-manifest.json`，但用户限定本子任务不得修改技能目录外文件；
  因此 `test_manifest_matches_live_public_inventory` 与 `test_inventory_only_cli_passes` 的 source
  hash 红由
  `07-15-audit-release-integration` R4a 同步 manifest 与双语目标后消解。本子任务仍须运行并记录
  `just test` / `just ci` 的完整输出，且除这两项同因失败外不得有失败。

## 与父任务 PRD 的偏差声明

1. A-BIB-6 登记表示例 `10:30` 经实测**不成立**（`FIELD_OP_RE` 的 field 必须以字母/下划线开头），实际受影响的是 `genotype:phenotype` 类字母开头 token；文档小节须按实测事实书写，不照抄登记表示例。
2. A-BIB-3 词边界化会使 Zotero tag `CodeAvailable`（camelCase 连写）从 True 变 False——这是本仓 fixture 与文档示例依赖的真正例，故词表须新增 `codeavailable` 项，属于 D4「逐词界定语义」的必要补充而非扩大范围。
3. 两份 `references/` 已纳入双语资源 manifest；本子任务按用户红线只修改 source，文档镜像与
   manifest hash 明确留给终批 `audit-release-integration` R4a，不在本任务越界同步。
