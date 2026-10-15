# 设计：latex-defense-zh rebuttal 模块

本文件是三个子任务共享的契约。子任务 design 只写本文件未覆盖的实现细节；冲突时以本文件为准，修改本文件须回到规划阶段。

## 1. 边界与数据流

```text
$REVIEWS/ (只读)          $THESIS/ (只读)
   │                          │  *.aux、git
   ▼                          ▼
rebuttal_intake.py ──► $ROOT/workspace/{rebuttal_state.json, reviews/R<n>.md, concerns.yaml}
                               │  LLM：拆分复合意见、分类、定处理方式（status=planned）
                               ▼
rebuttal_build.py --plan-only ──► workspace/revision_plan.md   ← 检查点 R2：用户批准处理方式
                               │  用户或 latex-thesis-zh 修改论文并重新编译（本模块不参与）
                               │  LLM：写回复、修改位置、证据（status=done）
                               ▼
rebuttal_build.py ──► responses/{review-result.md, response-all.md, response-R<n>.md}
                      workspace/{anchors.json, revision_plan.md}
                               ▼
rebuttal_check.py ──► workspace/check.json + R-* 结果行（最多 3 轮修台账 → build → check）
```

- `$ROOT` 默认等于 `$REVIEWS` 的父目录；`--root` 覆盖。脚本只写 `$ROOT/responses/` 与 `$ROOT/workspace/`。
- `$REVIEWS` 不得等于 `$ROOT/responses` 或 `$ROOT/workspace`，也不得在其内部；违反时退出码 2。
- 论文仓库读取范围：`*.aux`（跳过隐藏目录，与 `extract_thesis.load_aux_numbers` 同规则）、`--main` 指定或自动选出的主文件的 include 树
  （复用 `tex_loader`，遵守 `.trellis/spec/academic-writing-skills/include-boundary-contract.md`）、`git` 只读命令。
- `$THESIS` 可选：未给出时 intake 只做评阅书提取，锚点不映射标签；build 与 check 中依赖论文的检查跳过并写入 `skipped`。

## 2. 共享模块 `scripts/rebuttal_common.py`

C1 创建，C2 复用。只含三个脚本共用的部分：

- `load_aux_labels(root) -> dict[str, AuxLabel]`：`AuxLabel(number, page, title, file)`；解析 `\newlabel{l}{{num}{page}{title}...}`，
  跳过 `sub@`；同名标签浅层文件优先（与 `load_aux_numbers` 一致）。复用 `extract_thesis.read_group`、`skip_ws` 与 `tex_loader.read_text_robust`。
- `load_bibcites(root) -> dict[str, str]`：序号 → bib 键（`\bibcite{key}{{n}...}`）。
- `ANCHOR_PATTERNS` 与 `find_anchors(text) -> list[Anchor]`：识别 `图a-b`、`表a-b`、`式(a-b)`/`公式(a-b)`、`算法a-b`、`第N章`（阿拉伯或中文数字）、
  `第N章至第M章`、`a.b节`/`a.b.c节`、`文献[n]`/`文献[n,m]`/`文献[n-m]`。分隔符接受 `-`、`.`、`－`、`—`。
- `load_ledger(path)` / `dump_ledger(path, data)`：YAML 读写，`allow_unicode=True`、`sort_keys=False`；校验 `schema` 字段。
- `emit(findings, as_json)`：与 `check_deck.py` 相同的结果行格式（§6）。
- `git_changed_files(thesis, base) -> set[str] | None`：`git -C <thesis> diff --name-only <base>` 并上 `git ls-files --others --exclude-standard`，
  路径为仓库相对 POSIX；非 git 仓库或命令失败返回 `None`。子进程用 `encoding="utf-8", errors="replace"`
  （`.trellis/spec/academic-writing-skills/harness-workflow-contract.md` 的 UTF-8 子进程协议）。

## 3. 目录与文件契约

```text
$ROOT/
  <评阅书目录>/                 输入，只读
  responses/
    review-result.md            预评审结果行
    response-all.md             「博士生修改说明」全文
    response-R1.md …            单个评阅人
  workspace/
    rebuttal_state.json
    reviews/R1.md …             归一化评阅原文
    concerns.yaml               台账（唯一事实源）
    revision_plan.md            修改计划
    anchors.json                build 解析出的锚点
    check.json                  最近一次 check 结果
```

`rebuttal_state.json` 字段：

| 字段 | 含义 |
| --- | --- |
| `schema` | `"rebuttal-state/1"` |
| `stage` | `pre-review` / `final-review` / `predefense` / `other`（只影响标题文字） |
| `form_title` | 表格标题文字，默认按 stage 取，`--form-title` 覆盖 |
| `reviews_dir` | 相对 `$ROOT` 的评阅书目录 |
| `reviews[]` | `{id, file, sha256, pages, text_layer: bool}`；`id` 为 `R1`…，按文件名中的阿拉伯数字排序，无数字时按文件名排序；`--order` 覆盖 |
| `thesis` | `{given: bool, base_commit: str\|null, aux_labels: int}`；`base_commit` 为 intake 时 `git rev-parse HEAD`，`--base-commit` 覆盖 |
| `rendered` | `{<responses 相对路径>: sha256}`，build 写入；用于检测手改 |
| `created`、`updated` | ISO 日期 |

`workspace/reviews/R<n>.md` 格式（脚本生成，LLM 不改）：

```text
# R1 <源文件名>

## 评分
总分：90
总体评价：A
是否同意答辩：同意答辩

## 学术评语
<合并换行后的段落>

## 不足之处和建议
1. <第 1 条，合并换行>
2. <第 2 条>
```

该文件是 workspace 内部产物，可以使用 Markdown 标题；纯文本等价规则（§5）只约束 `responses/`。

## 4. 台账 `concerns.yaml`

```yaml
schema: rebuttal-ledger/1
reviewers:
  - id: R1
    total_score: 90          # 解析失败为 null
    grade: A                 # A–E 或 null
    agree_defense: 同意答辩
    praise: "<学术评语全文>"  # 只读引用，不回复
concerns:
  - id: R1-3b                # 评阅人-条号[小写字母子项]
    reviewer: R1
    item: 3                  # 评阅书中的条号
    quote: "<评阅原文的逐字子串>"
    quote_short: null        # 可选；quote 超过 160 字时由 LLM 给出首尾摘录，渲染时用它
    category: figure
    severity: Minor          # Critical|Major|Minor|Info
    priority: P2             # P0–P3
    shared_with: [R2-1a]
    anchors:
      - text: 图2-7
        kind: figure         # figure|table|equation|algorithm|chapter|section|reference
        label: fig:ch2_framework   # intake 由基线 aux 反查；查不到为 null
        base_number: 2-7
        base_page: 27
    action: revise           # revise|add|clarify|partial|future_work|decline
    status: open             # open|planned|done|needs_user_input
    owner: drawio            # latex-thesis-zh|drawio|manual|none
    plan: "<修改计划>"
    response: "<回复正文>"
    locations:
      - label: fig:ch2_framework        # 优先：LaTeX 标签
      - file: chapters/chapter6.tex     # 无标签时：文件 + 节号文字
        section: "6.1"
    evidence:
      kind: git_diff         # git_diff|user_confirmed|none
      files: [drawio/xxx.drawio, fig/xxx.png]
      note: ""
    source: "[LLM]"          # intake 生成的条目为 "[Script]"；LLM 改写后改为 "[LLM]"
```

规则：

- intake 每条编号意见生成一条 `R<n>-<item>`，`status: open`、`action: null`、`source: "[Script]"`、`quote` 为整条原文。
- 复合意见由 LLM 拆为 `R<n>-<item>a`、`b`…，删除原整条；每个子项一个处理动作，`quote` 为原文的逐字子串。拆分规则写入 `references/rebuttal-workflow.md`。
- `category` 枚举：`writing`（表述、缩写、符号）、`figure`、`table`、`reference`、`structure`、`experiment`、`generalization`、
  `theory`、`complexity`、`deployment`、`application`、`innovation`、`other`。
- `action` 与必填字段：

| action | 含义 | 必填 | 允许的完成用语 |
| --- | --- | --- | --- |
| `revise` | 修改已有内容 | `locations`、`evidence.kind≠none` | 是 |
| `add` | 补充新内容 | `locations`、`evidence.kind≠none` | 是 |
| `clarify` | 只在回复中说明，论文不改 | `response` 写明理由 | 否 |
| `partial` | 部分采纳 | `locations`、`evidence.kind≠none`、`response` 写明未采纳部分的理由 | 是（限已改部分） |
| `future_work` | 列为后续工作；可同时在论文展望或局限中补充 | `response`；若补充了论文文字则 `locations` 与 `evidence` | 只对补充的论文文字 |
| `decline` | 不采纳 | `response` 给出学术理由 | 否 |

- `status: planned` 表示用户已批准处理方式；`done` 表示回复与证据齐全；`needs_user_input` 表示 LLM 无法决定，须用户回答。
- 台账中的数字、结论与位置只能来自评阅原文、论文或用户确认；LLM 不写论文中不存在的实验结果。

## 5. responses 渲染：纯文本等价 Markdown

允许：普通段落、空行分段、普通文字行。禁止（R-MD-SYNTAX 检查）：

- 行首 `#`、`>`、`-`、`*`、`+`、`<数字>.`、`<数字>)`（会被渲染成标题、引用或列表）；
- 行内 `**`、`__`、反引号、`[文字](链接)`、`<标签>`、`|` 表格、`$` 数学、`\` 转义、脚注 `[^`；
- 行尾两个以上空格（硬换行）。

编号写成「意见1：」「意见3（2）：」，评阅人分节写成「一、评阅人1意见的修改说明」。原样复制与从渲染视图复制得到相同文字。

`response-all.md` 结构：

```text
博士生修改说明

总体说明：<感谢一次；意见总条数与拆分后项数；各处理方式计数；「下文页码均指修改后论文」>

一、评阅人1意见的修改说明

意见1：<quote，超过 160 字时截取首尾并以「……」相连，截取由 LLM 在台账中给出 quote_short>
回复：<response>
修改位置：<位置列表，以「；」分隔>

意见2：…

二、评阅人2意见的修改说明
…
```

- 子项意见：同一条号的子项共用「意见3：」原文一次，其后依次写「（1）回复：…」「（1）修改位置：…」。
- 跨评阅人重叠：每个评阅人小节自足，回复全文写出；可在末尾加「（与评阅人1意见3（2）一并修改）」。
- 位置渲染：图表式算法 →「图2-8（第28页）」；章 →「第6章」；节 →「第2.4节（第25页）」；文献 →「参考文献[24]」；
  当前编号与 `base_number` 不同 →「原图2-7，现图2-8（第28页）」；无标签的文件位置 →「第6.1节」。页码取修改后 aux。
- `review-result.md`：`总体评价 1（A）；总体评价 2（A）`，评阅人按 `R<n>` 顺序；等级为 null 时写「（ ）」并由 check 报告。
- `response-R<n>.md`：标题行「评阅人<n>意见的修改说明」，其后为该评阅人的逐条内容，不含总体说明。
- `revision_plan.md` 位于 workspace，可用 Markdown 表格：列为 意见 / 分类 / 处理方式 / 负责方 / 计划 / 目标文件 / 状态，按负责方再按文件分组；重叠意见合并为一行并列出全部编号。

## 6. 结果行与退出码

结果行与 D-* 同格式：

```text
% R-CODE (concern=<id>, <相对文件>:<行>) [Severity: Critical|Major|Minor|Info] [Priority: P0|P1|P2|P3]: [Script] <中文说明>
```

`--json` 输出 `{findings[], summary{Critical,Major,Minor,Info}, skipped[]}`，同时写 `workspace/check.json`。

| 脚本 | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| `rebuttal_intake.py` | 成功 | — | 输入错误（目录不存在、无评阅书、不支持格式、目录嵌套违规） | 有 PDF 但缺 PyMuPDF | `workspace/reviews/` 已存在且无 `--force` |
| `rebuttal_build.py` | 成功 | — | 台账校验失败 | — | responses 被手改且无 `--force` |
| `rebuttal_check.py` | 无 Critical/Major | 有 Critical 或 Major | 输入错误 | — | — |

intake 的 `--force` 只重写 `reviews/` 与 `rebuttal_state.json`；`concerns.yaml` 已存在时永不覆盖，新增的评阅条目以 warning 列出，由 LLM 合并。

## 7. R-* 码表

| 码 | 严重度 / 优先级 | 判据 | 来源 |
| --- | --- | --- | --- |
| R-COVER | Critical / P0 | `reviews/R<n>.md` 的某条编号意见在台账中无对应 `item`；或 `status=done` 的条目 `response` 为空 | Script |
| R-STATUS | Major / P1 | 存在 `open`、`planned` 或 `needs_user_input` | Script |
| R-QUOTE | Major / P1 | `quote` 不是对应评阅原文（去空白后）的子串；或 `quote_short` 按「……」切分后有一段不是子串 | Script |
| R-COMMIT | Critical / P0 | `action ∈ {revise, add, partial}`（或 `future_work` 且有 `locations`）时：`evidence.kind=none`；或 `git_diff` 时 `evidence.files` 与 locations 解析出的文件均不在 `git_changed_files(base)` 中；`$ROOT` 与评阅书目录下的路径不计入 | Script |
| R-CLAIM | Critical / P0 | `action ∈ {clarify, decline}` 或 `status≠done` 的 `response` 含完成用语（已修改、已补充、已增加、已删除、已调整、已完善、已重绘、已修正、已更正、已统一） | Script |
| R-LOC | Major / P1 | 需要位置的条目 `locations` 为空；或 `label` 不在当前 aux；或 `file` 不存在 | Script |
| R-PAGE-STALE | Major / P1 | 某个 `evidence.files` 或位置文件中的 `.tex` 修改时间晚于其对应 aux（无章 aux 时比 `document.aux`） | Script |
| R-RENUM | Minor / P2 | 锚点当前编号与 `base_number` 不同，而 responses 中该条只出现原编号 | Script |
| R-MD-SYNTAX | Major / P1 | responses 文件违反 §5 | Script |
| R-PLACEHOLDER | Critical / P0 | responses 或台账 `response` 含 `〔待填写〕`、`TODO`、`TBD`、`XX`、`??` | Script |
| R-NUM-SRC | Major / P1 | 回复中的带小数或百分号数字未出现在论文可见文本中（NEEDS-LLM 复核，可能是评阅原文中的数字） | Script |
| R-REVIEW-CHANGED | Major / P1 | 评阅书文件 sha256 与 `rebuttal_state.json` 不同 | Script |
| R-SHARED | Minor / P2 | `shared_with` 互指的条目 `action` 一类为已修改、一类为 `clarify`/`decline`/`future_work` | Script |
| R-RESULT | Major / P1 | `review-result.md` 的等级与台账不一致，或台账等级为 null | Script |
| R-SYNC | Minor / P2 | responses 当前内容与 `rendered` 记录的 sha256 不同（手改，提示把改动写回台账） | Script |
| R-TONE | Info / P3 | 同一开头句（前 12 字）在回复中出现 3 次以上；`decline`/`future_work` 理由含「时间」「经费」「工作量」；含贬抑评阅人的词 | Script，NEEDS-LLM |

- 依赖论文的码（R-COMMIT 的 git 部分、R-LOC 的 aux 部分、R-PAGE-STALE、R-RENUM、R-NUM-SRC）在未给 `--thesis` 或非 git 仓库时进入 `skipped`，
  并对 `evidence.kind=git_diff` 的条目报 R-COMMIT Info「无法核对 git 证据，请用户确认」。
- `user_confirmed` 证据不做 git 核对，但 `note` 为空时报 R-COMMIT Minor。

## 8. CLI 契约

```text
rebuttal_intake.py --reviews DIR [--thesis DIR] [--main FILE] [--root DIR] [--stage pre-review|final-review|predefense|other]
                   [--form-title TEXT] [--order FILE,FILE,...] [--base-commit SHA] [--force] [--json]
rebuttal_build.py  --workspace DIR [--thesis DIR] [--plan-only] [--force] [--json]
rebuttal_check.py  --workspace DIR [--thesis DIR] [--json]
```

- `--workspace` 指 `$ROOT/workspace`；`$ROOT` 与 responses 目录由此推出，评阅书目录由 `rebuttal_state.json` 推出。
- intake `--json` 输出 `{root, reviewers[{id, file, grade, total_score, items, anchors}], warnings[], ledger_written: bool}`。
- build `--json` 输出 `{written[], anchors_resolved, anchors_unresolved[], plan_only: bool}`。
- 三个脚本都用 `uv run python -B $SKILL_DIR/scripts/<name>.py` 调用，`--help` 列出全部选项（`test_skill_contracts.py:625` 对照 references 中的选项）。

## 9. 评阅书归一化规则（intake）

1. 每页取文本（PyMuPDF `page.get_text("text", sort=True)`）；`.txt`/`.md` 以 `tex_loader.read_text_robust` 读入并按换页符或整体视为一页。
2. 删除在不少于 `max(2, ceil(2/3 × 页数))` 页中出现的行（水印、页眉）；删除匹配 `第\s*\d+\s*页$` 的行与只含 1–3 位数字的行。单页输入不做重复行删除。
3. 标题集合（可扩展常量）：评语类 `对学位论文的学术评语`、`学术评语`、`评阅意见`；不足类 `论文的不足之处和建议`、`不足之处和建议`、`存在的不足`、`主要问题`、`修改意见`、`问题与建议`。
   找不到不足类标题时，全文作为一节并 warning `W-NO-SECTION`，由 LLM 切分。
4. 编号切分：行首 `\d+[.、．)]`、`（\d+）`、`\(\d+\)`；编号需从 1 递增，不递增的行并入上一条。
5. 换行合并：中文字符之间直接拼接；英文与数字之间补一个空格。
6. 每页非空白字符少于 50 时视为无文字层，warning `W-NO-TEXT`，该评阅书生成空骨架，`text_layer=false`。
7. `.docx`、`.doc`、图片文件：退出码 2，提示「请导出为 PDF 或 TXT」。

## 10. 测试与 fixture

- fixture 目录：`academic-writing-skills/latex-defense-zh/evals/fixtures/rebuttal/`，全部合成。
  - `reviews/评阅书1.txt`（`1.` 编号，含水印行与页脚、跨行意见、复合意见、`图2-1`、`文献[3]`）。
  - `reviews-pdf/` 不入库：测试用 PyMuPDF 在 `tmp_path` 生成多页 PDF（含重复水印与 `1、` 编号），无 PyMuPDF 时 skip。
  - 论文树：复用 `evals/fixtures/mini-thesis/`（已有 `chapters/chapter2.aux` 等，含 `{编号}{页码}{标题}`，无 `document.aux` 与 `\bibcite`）。
    测试把它复制到 `tmp_path`，在副本中写入含 `\bibcite` 的 `document.aux`；C2 再改写副本的 aux 与 tex 制造「修改后」状态与 git 历史。
    `mini-thesis/` 原文件不改（defense 现有测试依赖它）。
- 测试文件名加 `test_defense_rebuttal_` 前缀；脚本按 `tests/skills/latex_defense_zh/conftest.py` 的 `load_script` 方式加载，
  并把 `rebuttal_common` 加入 `_SHARED_MODULE_NAMES`。
- git 相关测试在 `tmp_path` 内 `git init`；无 git 可执行文件时 skip。

## 11. 回滚

每个子任务只新增文件或在 design 列出的文件中追加内容。回滚为删除该子任务新增文件并撤销所列文件中的对应段落；
不用 `git checkout` 整文件还原（C3 同时改动多个共享 docs 文件）。本设计不授权 commit、archive 或 push。
