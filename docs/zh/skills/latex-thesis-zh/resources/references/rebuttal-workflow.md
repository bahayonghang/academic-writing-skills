# 评阅意见回复流程

本文件规定评阅意见回复（rebuttal）三个脚本的用法、目录布局、意见台账字段、复合意见拆分规则、处理方式选择、检查点、证据要求与修复循环。回复文字的写法见 [回复写法](rebuttal-writing.md)，R-* 码见 [回复质量门](rebuttal-gate.md)。

适用场景：学位论文预评审、盲审、终评审或预答辩的评阅书返回后，逐条写「博士生修改说明」或「评阅意见修改审查表」中的回复，并核对论文是否真的改了。期刊或会议的审稿回复信不在范围内。

## 用法

```bash
uv run python -B $SKILL_DIR/scripts/rebuttal_intake.py --reviews $REVIEWS --thesis $THESIS --main document.tex --stage pre-review --json
uv run python -B $SKILL_DIR/scripts/rebuttal_build.py --workspace $ROOT/workspace --thesis $THESIS --plan-only
uv run python -B $SKILL_DIR/scripts/rebuttal_build.py --workspace $ROOT/workspace --thesis $THESIS --json
uv run python -B $SKILL_DIR/scripts/rebuttal_check.py --workspace $ROOT/workspace --thesis $THESIS --json
```

`$REVIEWS` 为评阅书目录，`$THESIS` 为论文仓库根目录，`$ROOT` 为 `$REVIEWS` 的父目录（intake 加 `--root` 时为该目录）。

| 脚本                 | 选项                                                                                                                                                                                                                                     |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `rebuttal_intake.py` | `--reviews DIR`（必填）、`--thesis DIR`、`--main FILE`、`--root DIR`、`--stage pre-review\|final-review\|predefense\|other`（缺省 `pre-review`）、`--form-title TEXT`、`--order FILE,FILE,...`、`--base-commit SHA`、`--force`、`--json` |
| `rebuttal_build.py`  | `--workspace DIR`（必填）、`--thesis DIR`、`--plan-only`、`--force`、`--json`                                                                                                                                                            |
| `rebuttal_check.py`  | `--workspace DIR`（必填）、`--thesis DIR`、`--json`                                                                                                                                                                                      |

| 脚本                 | 退出码                                                                                                                                                                                |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `rebuttal_intake.py` | 0：成功（可有 warning）；2：输入错误（目录不存在、无评阅书、`.docx`/`.doc`/图片、评阅书目录与输出目录嵌套）；3：有 PDF 但未安装 PyMuPDF；4：`workspace/reviews/` 已存在且无 `--force` |
| `rebuttal_build.py`  | 0：成功；2：台账或 workspace 校验失败；4：responses 中的文件在上次生成后被手改且无 `--force`                                                                                          |
| `rebuttal_check.py`  | 0：无 Critical 与 Major 结果；1：至少一条 Critical 或 Major 结果；2：输入错误                                                                                                         |

- `--thesis` 可省略。省略时 intake 不映射锚点标签、不记录基线提交；build 的修改位置不带当前编号与页码；check 跳过依赖论文的检查（见 [回复质量门](rebuttal-gate.md)）。
- 读 PDF 需要 PyMuPDF（`uv pip install pymupdf`）。没有文字层的扫描版 PDF 生成空骨架并报 W-NO-TEXT，由用户提供 TXT 或由 LLM 读图后填写台账。

## 目录布局

```text
$ROOT/
  <评阅书目录>/                 输入，只读
  responses/                    粘贴用文本，由 rebuttal_build.py 生成
    review-result.md            预评审结果行：总体评价 1（A）；总体评价 2（B）
    response-all.md             「博士生修改说明」全文
    response-R1.md …            单个评阅人的修改说明
  workspace/                    中间产物
    rebuttal_state.json         状态文件
    reviews/R1.md …             归一化评阅原文（脚本生成，不手改）
    concerns.yaml               意见台账（唯一事实源）
    revision_plan.md            修改计划（按负责方分组的表格）
    anchors.json                build 解析出的锚点
    check.json                  最近一次 check 结果
```

- 三个脚本只写 `responses/` 与 `workspace/`。评阅书目录与论文仓库只读：论文仓库只读取 `*.aux`、主文件 include 树与 git 只读命令。
- `$ROOT` 可以位于论文仓库内部（例如 `<论文仓库>/rebuttal/pre-review/`）。此时 check 核对 git 证据时排除 `$ROOT` 与评阅书目录下的路径。
- 评阅书目录不能等于 `responses/` 或 `workspace/`，也不能位于它们内部，否则 intake 退出码 2。

### 状态文件 `rebuttal_state.json`

| 字段                 | 含义                                                                                                                           |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `schema`             | `"rebuttal-state/1"`                                                                                                           |
| `stage`              | `pre-review`、`final-review`、`predefense`、`other`                                                                            |
| `form_title`         | 修改审查表标题，缺省按 `--stage` 取，`--form-title` 覆盖；供核对 Word 表格标题，responses 不写入                               |
| `reviews_dir`        | 评阅书目录相对 `$ROOT` 的路径                                                                                                  |
| `reviews[]`          | `{id, file, sha256, pages, text_layer}`；`id` 为 `R1`、`R2`…，按文件名中的阿拉伯数字排序，无数字时按文件名排序，`--order` 覆盖 |
| `thesis`             | `{given, base_commit, aux_labels, main}`；`base_commit` 为 intake 时论文仓库的 `HEAD`，`--base-commit` 覆盖                    |
| `rendered`           | `{<responses 相对路径>: sha256}`，build 写入，用于检测手改                                                                     |
| `created`、`updated` | ISO 日期                                                                                                                       |

## intake：读取评阅书

1. 每页取文本。`.txt` 与 `.md` 按换页符分页，没有换页符时整体视为一页。
2. 删除水印与页眉：在不少于 `max(2, ceil(2/3 × 页数))` 页中重复出现的行。删除「第 N 页」行与只含 1–3 位数字的页码行；紧跟「总分」的数字行保留为总分。
3. 按标题切分「学术评语」与「不足之处和建议」，再按行首编号（`1.`、`1、`、`（1）`、`(1)`）切分意见。编号须从 1 递增，不递增的行并入上一条。
4. 换行合并：中文字符之间直接拼接，英文与数字之间补一个空格。
5. 解析总分、总体评价（A–E）与是否同意答辩。
6. 识别锚点：`图a-b`、`表a-b`、`式(a-b)`、`公式(a-b)`、`算法a-b`、`第N章`、`第N章至第M章`、`a.b节`、`文献[n]`、`文献[n,m]`、`文献[n-m]`。提供 `--thesis` 时用送审版本的 aux 反查标签，写入 `label`、`base_number` 与 `base_page`。
7. 写 `workspace/reviews/R<n>.md` 与状态文件。台账 `concerns.yaml` 只在不存在时写入骨架。

| warning            | 含义与处理                                                                      |
| ------------------ | ------------------------------------------------------------------------------- |
| W-SKIP-FILE        | 目录中的非评阅书文件被忽略；同名的 `.md`、`.txt`、`.pdf` 只读一份（优先级同此顺序），其余被忽略 |
| W-NO-TEXT          | PDF 没有文字层；提供 TXT，或由 LLM 读图后填写台账                               |
| W-NO-SCORE         | 未解析到总分、总体评价或是否同意答辩；对照原件在台账 `reviewers` 中补填         |
| W-NO-SECTION       | 未找到「不足之处和建议」类标题，全文按一节切分；由 LLM 复核切分                 |
| W-NO-NUMBER        | 不足之处没有编号，整节记为第 1 条；由 LLM 拆分为子项                            |
| W-UNNUMBERED       | 第 1 条编号前的文字未进入台账；确认其中是否含意见                               |
| W-ANCHOR-AMBIGUOUS | 一个锚点对应多个标签，取第一个；核对 `label`                                    |
| W-ANCHOR-MISSING   | 锚点在送审版本 aux 中找不到标签（例如「第3章至第5章」中间的章）；不影响后续步骤 |
| W-NO-AUX           | 论文仓库没有 aux；先编译送审版本再重跑 intake                                   |
| W-NO-GIT           | 论文仓库不是 git 仓库；修改证据只能用 `user_confirmed`                          |
| W-LEDGER           | 已有台账无法读取；修正 YAML 语法                                                |
| W-LEDGER-MISSING   | 重跑 `--force` 后出现台账没有的条目；由 LLM 合并到台账                          |

`--force` 只重写 `workspace/reviews/` 与状态文件，已有台账永不覆盖。

基线提交：intake 记录的 `base_commit` 应是送审版本。如果论文已在送审后提交过修改，用 `--base-commit <送审版本的提交>` 指定，否则 check 无法看到这些修改。

## 意见台账 `concerns.yaml`

台账是 responses 的唯一事实源。responses 中的文字只改台账，然后重新 build。

```yaml
schema: rebuttal-ledger/1
reviewers:
  - id: R1
    total_score: 88 # 解析失败为 null
    grade: A # A–E 或 null
    agree_defense: 同意答辩
    praise: "<学术评语全文>" # 只读引用，不回复
concerns:
  - id: R1-3b # 评阅人-条号[小写字母子项]
    reviewer: R1
    item: 3 # 评阅书中的条号
    quote: "<评阅原文的逐字子串>"
    quote_short: null # quote 超过 160 字时给出首尾摘录，以「……」相连
    category: figure
    severity: Minor # Critical|Major|Minor|Info
    priority: P2 # P0|P1|P2|P3
    shared_with: [] # 与其他评阅人重叠的条目 id
    anchors: [] # intake 生成，不手改
    action: revise # revise|add|clarify|partial|future_work|decline
    status: done # open|planned|done|needs_user_input
    owner: drawio # latex-thesis-zh|drawio|manual|none
    plan: "<修改计划>"
    response: "<回复正文>"
    locations:
      - label: fig:c2-profile # 优先：LaTeX 标签或 bib 键
      - file: chapters/chapter2.tex # 无标签时：文件 + 节号
        section: "2.3"
    evidence:
      kind: git_diff # git_diff|user_confirmed|none
      files: [chapters/chapter2.tex]
      note: ""
    source: "[LLM]" # intake 生成为 "[Script]"，LLM 改写后为 "[LLM]"
```

| 字段                    | 取值                                                                                                                                                                                   |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `category`              | `writing`（表述、缩写、符号）、`figure`、`table`、`reference`、`structure`、`experiment`、`generalization`、`theory`、`complexity`、`deployment`、`application`、`innovation`、`other` |
| `severity` / `priority` | Critical / P0、Major / P1、Minor / P2、Info / P3；按意见对论文结论的影响判定                                                                                                           |
| `owner`                 | `latex-thesis-zh`（正文修改）、`drawio`（图）、`manual`（用户自己改，例如 bib 文件、实验）、`none`（论文不改）                                                                         |
| `status`                | `open`：intake 生成；`planned`：用户已批准处理方式；`done`：回复、位置与证据齐全；`needs_user_input`：LLM 无法决定，须用户回答                                                         |
| `locations[]`           | 每项须含 `label`（LaTeX 标签或 bib 键）或 `file`（论文仓库相对路径，可加 `section`）                                                                                                   |
| `evidence.files`        | 论文仓库相对路径                                                                                                                                                                       |

台账中的数字、结论与位置只能来自评阅原文、论文或用户确认。LLM 不写论文中不存在的实验结果。

## 拆分复合意见

一条编号意见含多个独立的修改要求时，拆为子项 `R<n>-<条号>a`、`b`、`c`…，删除原整条。

1. 判据：每个子项能单独给出一个处理方式与一个修改位置。同一要求的多处表述（「图2-1文字过于密集，图注也过长」）不拆。
2. 每个子项的 `quote` 是原文的逐字子串，去掉引导语（「写作规范方面：」）与分隔标点。
3. 子项按原文顺序编字母。渲染时同一条号的子项共用一次「意见N：」原文，其后为「（1）回复：」「（1）修改位置：」。
4. 子项继承原条目的 `reviewer`、`item` 与 `anchors` 中属于本子项的部分。
5. 不同评阅人提出的同一问题不合并为一条：各自保留条目，用 `shared_with` 互指，回复全文分别写出。

## 处理方式选择

| action        | 含义                     | 必填                                                                       | 回复中的完成用语     |
| ------------- | ------------------------ | -------------------------------------------------------------------------- | -------------------- |
| `revise`      | 修改已有内容             | `locations`、`evidence.kind≠none`                                          | 允许                 |
| `add`         | 补充新内容               | `locations`、`evidence.kind≠none`                                          | 允许                 |
| `clarify`     | 只在回复中说明，论文不改 | `response` 写明理由                                                        | 不允许               |
| `partial`     | 部分采纳                 | `locations`、`evidence.kind≠none`；`response` 写明未采纳部分的理由         | 只用于已改部分       |
| `future_work` | 列为后续工作             | `response`；如在论文局限或展望中补充了讨论，另填 `locations` 与 `evidence` | 只用于补充的论文文字 |
| `decline`     | 不采纳                   | `response` 给出学术理由                                                    | 不允许               |

选择顺序：

1. 意见指出的错误或缺失在论文中确实存在，并且答辩前能改完：`revise` 或 `add`。
2. 意见源于理解差异，论文中已有相应内容：`clarify`，回复中写出原文所在位置。若该处表述确实容易误读，改用 `revise` 并改写表述。
3. 意见要求的补充实验、新数据或新平台在答辩前无法完成：`future_work`。可在论文「局限与展望」中补充讨论，并把该节作为修改位置；回复中不得写成实验已完成。
4. 意见与论文的问题范围或研究假设冲突：`decline`，理由写学术依据（问题范围、假设、已有文献的做法），不写时间、经费或工作量。
5. 意见只有部分可采纳：`partial`，分别写已改部分与未采纳部分的理由。
6. 无法判断是否采纳、或需要用户提供实验数据：`status: needs_user_input`，在 `plan` 中写出要问用户的问题。

## 检查点

| 检查点 | 时机                                                                | 内容                                                                                                                                                                           |
| ------ | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| R1     | intake 之后                                                         | 向用户报告每位评阅人的总分、等级、意见条数、锚点数与 warnings。请用户确认评阅人顺序（R1、R2 与原件编号一致）与基线提交（送审版本）。顺序不对时用 `--order` 加 `--force` 重跑。 |
| R2     | LLM 拆分并填写 `action`、`owner`、`plan`、`status: planned` 之后    | 运行 `rebuttal_build.py --plan-only`，把 `workspace/revision_plan.md` 交给用户批准处理方式。`decline` 与 `future_work` 条目逐条说明理由。用户批准前不写回复。                  |
| R3     | 论文修改并重新编译、回复与证据填写为 `status: done`、check 通过之后 | 交付 `responses/` 文件清单、质量门计数与遗留项。用户把文本粘贴进 Word 表格。                                                                                                   |

R2 与 R3 之间，论文修改由用户或 `latex-thesis-zh` 完成，图由 `drawio` 类工具完成。本模块不修改论文源文件，也不编译论文。修改完成后提交到 git，并完整编译修改后论文（aux 须晚于 tex），再写回复。

## 证据要求

- `git_diff`：`evidence.files` 或 `locations` 解析出的文件中，至少一个在基线提交之后有改动（已提交或未提交均计入）。只适用于论文仓库是 git 仓库的情况。
- `user_confirmed`：用户在对话中确认已修改，`note` 写明确认内容（例如「图由导师在 Visio 中重绘，PNG 已替换」）。check 不核对 git。
- `none`：论文未修改。只允许用于 `clarify`、`decline` 与没有位置的 `future_work`。

证据与位置检查只针对 `status: done` 的条目。

## 修复循环

1. 运行 `rebuttal_build.py`，再运行 `rebuttal_check.py --json`。
2. 按 [回复质量门](rebuttal-gate.md) 修改台账（或修改论文后重新编译），再 build、check。
3. 最多 3 轮。3 轮后仍有 Critical 或 Major 结果时，停下并把剩余结果与原因报告给用户。
4. NEEDS-LLM 结果（R-NUM-SRC、R-TONE）逐条回到论文原句或评阅原文复核，在交付说明中写出复核结论。

responses 中的文件被手改后，build 退出码 4，check 报 R-SYNC。处理方式：把手改内容写回台账后运行 `rebuttal_build.py --force`。
