# 回复质量门

本文件规定 `rebuttal_check.py` 的 R-* 码、判据、严重度、修复方法、跳过规则与 NEEDS-LLM 复核。流程与台账字段见 [回复流程](rebuttal-workflow.md)，回复写法见 [回复写法](rebuttal-writing.md)。

## 用法

```bash
uv run python -B $SKILL_DIR/scripts/rebuttal_check.py --workspace $ROOT/workspace --thesis $THESIS --json
```

- 读取 `workspace/concerns.yaml`、`workspace/rebuttal_state.json`、`workspace/reviews/R<n>.md`、`responses/*.md`、评阅书目录，以及论文仓库的 aux、主文件 include 树与 git 只读命令。
- 只写 `workspace/check.json`（内容与 `--json` 输出相同）。不写论文仓库、评阅书目录与 responses。
- 退出码：0 无 Critical 与 Major 结果；1 至少一条 Critical 或 Major 结果；2 输入错误（workspace 缺少状态文件或台账、台账无法解析、`--thesis` 不存在）。

## 输出格式

文本模式每条结果一行，末行为汇总：

```text
% R-COMMIT (concern=R1-3b, workspace/concerns.yaml:88) [Severity: Critical] [Priority: P0]: [Script] 声明的修改文件自基线提交以来没有改动：chapters/chapter2.tex
% R-MD-SYNTAX (concern=-, responses/response-R1.md:9) [Severity: Major] [Priority: P1]: [Script] Markdown 语法会改变粘贴结果：行首标记
% 汇总：Critical 1，Major 1，Minor 0，Info 0；skipped：无
```

- `concern=` 为台账条目 id。针对整个文件的结果写 `-`；针对评阅人的结果写 `R<n>`。
- 位置为台账中该条目 `id:` 所在行，或 responses、评阅原文中的行。
- `--json` 输出 `{findings[], summary{Critical, Major, Minor, Info}, skipped[]}`。
- 严重度与优先级：Critical = P0，Major = P1，Minor = P2，Info = P3。

## R-* 码表

| 码               | 严重度   | 判据                                                                                                                                                                                                         | 修复                                                                              |
| ---------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------- |
| R-COVER          | Critical | 评阅原文的某条编号意见在台账中没有对应 `item`；或 `status: done` 的条目 `response` 为空                                                                                                                      | 补条目或补回复。拆分子项时保留每个条号                                            |
| R-STATUS         | Major    | 存在 `open`、`planned` 或 `needs_user_input` 条目                                                                                                                                                            | 完成回复与证据后改为 `done`；`needs_user_input` 先问用户                          |
| R-QUOTE          | Major    | 条号在评阅原文中不存在；`quote` 去空白后不是该条原文的子串；或 `quote_short` 按「……」切分后有一段不是子串                                                                                                    | 从 `workspace/reviews/R<n>.md` 逐字复制原文                                       |
| R-COMMIT         | Critical | `status: done` 且需要位置的条目（`revise`、`add`、`partial`，或有 `locations` 的 `future_work`）：`evidence.kind` 为 `none`；或为 `git_diff` 时，`evidence.files` 与位置解析出的文件自基线提交以来都没有改动 | 修改论文并提交；或核对 `evidence.files` 路径；或改用 `user_confirmed` 并写 `note` |
| R-COMMIT         | Minor    | `user_confirmed` 证据的 `note` 为空                                                                                                                                                                          | 写明用户确认的内容                                                                |
| R-COMMIT         | Info     | 未给 `--thesis`、论文仓库不是 git 仓库或没有基线提交时，`git_diff` 证据无法核对                                                                                                                              | 请用户确认，或给出 `--thesis`                                                     |
| R-CLAIM          | Critical | `clarify`、`decline` 条目，或 `status` 不是 `done` 的条目，`response` 含完成用语（已修改、已补充、已增加、已删除、已调整、已完善、已重绘、已修正、已更正、已统一）                                           | 删去完成用语；论文确实改了时把 `action` 改为 `revise` 或 `add` 并补证据           |
| R-LOC            | Major    | `status: done` 且需要位置的条目 `locations` 为空；`label` 不在修改后的 aux 或 bib 键中；`file` 在论文仓库中不存在；或位置涉及的 `.tex` 没有对应 aux                                                          | 补位置、修正标签或路径；完整编译修改后论文                                        |
| R-PAGE-STALE     | Major    | 证据文件或位置文件中的 `.tex` 修改时间晚于对应 aux（章 aux 不存在时比主文件 aux）                                                                                                                            | 完整编译修改后论文，再运行 build                                                  |
| R-RENUM          | Minor    | 锚点的当前编号与送审版本不同，而 `response` 只写了原编号（该锚点不在 `locations` 中）                                                                                                                        | 回复中改写为修改后编号，或把该标签加入 `locations`                                |
| R-MD-SYNTAX      | Major    | responses 的某行违反纯文本等价规则：行首标记、`**`、`__`、反引号、链接、HTML 标签、表格竖线、`$`、反斜杠、脚注、行尾硬换行空格                                                                               | 改台账 `response` 的文字后重新 build                                              |
| R-PLACEHOLDER    | Critical | responses 或台账 `response` 含 `〔待填写〕`、`TODO`、`TBD`、`XX`、`??`、`？？`                                                                                                                               | 填写内容；未完成的条目保持非 `done` 并报告用户                                    |
| R-NUM-SRC        | Major    | 回复中带小数或百分号的数字不在论文可见文本中，也不在评阅原文中（NEEDS-LLM）                                                                                                                                  | 回到论文原句核对；数字有误时改回复                                                |
| R-NUM-SRC        | Info     | 上述数字不在论文中，但见于该评阅人的原文（NEEDS-LLM）                                                                                                                                                        | 确认引用的是评阅原文中的数字                                                      |
| R-REVIEW-CHANGED | Major    | 评阅书文件不存在，或 sha256 与 intake 时不同                                                                                                                                                                 | 确认文件来源后运行 `rebuttal_intake.py --force`，再合并台账                       |
| R-SHARED         | Minor    | `shared_with` 指向不存在的条目；或互指的两条中一条修改论文（`revise`、`add`、`partial`），另一条为 `clarify`、`decline` 或 `future_work`                                                                     | 统一处理方式，或在回复中写明两处处理不同的原因                                    |
| R-RESULT         | Major    | 台账中某评阅人的 `grade` 为空；`review-result.md` 未生成；或其中的等级与台账不同                                                                                                                             | 对照原件补 `grade`，重新 build                                                    |
| R-SYNC           | Minor    | responses 中的文件在上次 build 后被手改，或已被删除                                                                                                                                                          | 把改动写回台账，运行 `rebuttal_build.py --force`                                  |
| R-TONE           | Info     | 3 条以上回复的前 12 字相同；`decline`、`future_work` 的理由含「时间」「经费」「工作量」；回复含可能贬抑评阅人的用语（NEEDS-LLM）                                                                             | 按 [回复写法](rebuttal-writing.md) 改写                                           |

证据与位置检查（R-COMMIT、R-LOC）只针对 `status: done` 的条目。未完成的条目由 R-STATUS 报告。

## git 证据的口径

- 基线：状态文件中的 `thesis.base_commit`（intake 记录，`--base-commit` 可覆盖）。
- 改动文件 = `git diff --name-only <基线> HEAD`（已提交的改动）并上 `git status --porcelain`（未提交与未跟踪的改动）。改名条目只计新路径。
- 全部 git 命令带 `--no-optional-locks`，不写 `.git/index`。
- `$ROOT` 与评阅书目录位于论文仓库内时，其下路径不计入改动文件。
- 位置标签所在的 tex 文件由 aux 文件推出（`chapters/chapter2.aux` → `chapters/chapter2.tex`）。

## 跳过规则

未给 `--thesis` 时，以下检查记入 `skipped`：

| skipped 名      | 内容                                             |
| --------------- | ------------------------------------------------ |
| `R-COMMIT(git)` | git 证据核对；`git_diff` 条目另报 R-COMMIT Info  |
| `R-LOC(aux)`    | 标签与文件存在性；`locations` 为空的检查照常执行 |
| `R-PAGE-STALE`  | tex 与 aux 的时间比较                            |
| `R-RENUM`       | 编号变化检查                                     |
| `R-NUM-SRC`     | 数字来源检查                                     |

给了 `--thesis`，但论文仓库不是 git 仓库或状态文件没有基线提交时，只跳过 `R-COMMIT(git)`。

## NEEDS-LLM 复核

R-NUM-SRC 与 R-TONE 是候选结果，由 LLM 逐条复核：

1. R-NUM-SRC：打开修改后论文中对应的段落、表或图注，确认数字与单位。数字来自评阅原文时，确认引用无误。复核后在交付说明中写「已核对」或给出修正。
2. R-TONE：重复开头改为直接写处理内容；资源类理由改为学术理由；贬抑用语删除。
3. 复核结论写进交付说明，不写进 responses。

## 修复循环

1. `rebuttal_build.py` → `rebuttal_check.py --json`。
2. 先处理 Critical，再处理 Major；Minor 与 Info 在交付说明中列出。
3. 修台账后重新 build；修论文后重新编译论文，再 build。
4. 最多 3 轮。3 轮后仍有 Critical 或 Major 结果时停下报告。
