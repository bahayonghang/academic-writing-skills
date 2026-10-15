# latex-thesis-zh 评阅意见回复契约

## 1. Scope / Trigger

修改 `academic-writing-skills/latex-thesis-zh/` 的 rebuttal 脚本（`rebuttal_intake.py`、`rebuttal_build.py`、`rebuttal_check.py`、
`rebuttal_common.py`）、台账字段、R-* 判据、responses 渲染格式，以及对应公开资源时适用。
三个脚本通过状态文件、意见台账与 responses 串成一条流水线；任一环节改名或改格式，下游会静默失配。
详细字段以技能内 `references/rebuttal-workflow.md`、`references/rebuttal-writing.md` 与 `references/rebuttal-gate.md` 为准，
本文件只锁跨脚本的接口。评阅回复属于中文学位论文工作流；Beamer 答辩稿仍归 latex-defense-zh，见 [defense-deck-contract.md](./defense-deck-contract.md)。

## 2. Signatures

```text
rebuttal_intake.py --reviews DIR [--thesis DIR] [--main FILE] [--root DIR] [--stage pre-review|final-review|predefense|other]
                   [--form-title TEXT] [--order a.pdf,b.pdf] [--base-commit SHA] [--force] [--json]
rebuttal_build.py --workspace DIR [--thesis DIR] [--plan-only] [--force] [--json]
rebuttal_check.py --workspace DIR [--thesis DIR] [--json]
```

所有命令写作 `uv run python -B $SKILL_DIR/scripts/<name>.py …`；stdout/stderr 在 `__main__` 中重设为 UTF-8。

| 脚本   | 退出码                                                                                                                                                                    |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| intake | 0 成功（可有 W-*）；2 输入错误（目录不存在、无评阅书、`.docx`/`.doc`/图片、评阅书目录与输出目录嵌套）；3 有 PDF 但缺 PyMuPDF；4 `workspace/reviews/` 已存在且无 `--force` |
| build  | 0；2 台账或 workspace 校验失败；4 responses 文件在上次生成后被手改且无 `--force`                                                                                          |
| check  | 0 无 Critical/Major；1 有；2 输入错误                                                                                                                                     |

## 3. Contracts

- 包归属：三条 rebuttal 入口仅由 `latex-thesis-zh` 提供；仅整理评阅书允许不提供论文源，不能被正文模块的 LaTeX 输入要求拦截。
- 独立安装：回复脚本仅依赖本技能脚本和声明的运行依赖，不导入 `latex-defense-zh` 的 `extract_thesis` / `check_deck`，也不访问其 fixture。
- 回复模块与正文修改模块分离：回复脚本不改、提交或编译论文；正文修改按用户批准的计划走已有写作模块，不因归属相同而扩大授权。
- Claude 兼容 `allowed-tools` 应包含填写台账所需的 Write/Edit；回复场景的写入范围仍仅为用户指定的 responses/workspace，不因此授权修改论文。其他平台按真实能力映射，不能把元数据声明当作运行验证。

- 目录：`$ROOT` 缺省为评阅书目录的父目录；脚本只写 `$ROOT/responses/` 与 `$ROOT/workspace/`。
  评阅书目录不能等于或位于这两个目录内部。
- workspace 文件：`rebuttal_state.json`（`schema: "rebuttal-state/1"`）、`reviews/R<n>.md`（脚本生成，不手改）、
  `concerns.yaml`（`schema: "rebuttal-ledger/1"`，唯一事实源）、`revision_plan.md`、`anchors.json`、`check.json`。
- responses 文件：`review-result.md`、`response-all.md`、`response-R<n>.md`；内容是纯文本等价 Markdown，
  台账 `response` 原样进入 responses，因此 `response` 同样不得含行首标记、`**`、反引号、链接、HTML、`|`、`$`、`\`。
- 台账枚举固定：`action` ∈ revise、add、clarify、partial、future_work、decline；`status` ∈ open、planned、done、needs_user_input；
  `owner` ∈ latex-thesis-zh、drawio、manual、none；`evidence.kind` ∈ git_diff、user_confirmed、none。条目 id 形如 `R<n>-<k>[a-z]`。
- `--force`：intake 只重写 `reviews/` 与状态文件，台账不覆盖；build 覆盖被手改的 responses 文件。
- 只读：评阅书目录与论文仓库只读。论文仓库只读取 `*.aux`、主文件 include 树，并只运行 `git diff --name-only`、
  `git status --porcelain` 与 `git rev-parse`，均带 `--no-optional-locks`。
- git 证据口径：修改文件 = `git diff --name-only <基线> HEAD` ∪ `git --no-optional-locks status --porcelain -z`；重命名只计新路径；
  `$ROOT` 与评阅书目录位于论文仓库内时，其下路径不计为修改文件。基线取状态文件 `thesis.base_commit`。
- done-only：R-COMMIT 与 R-LOC 只检查 `status: done` 的条目；未完成条目由 R-STATUS 报告。
- R-* 码集合固定为 16 个：R-COVER、R-STATUS、R-QUOTE、R-COMMIT、R-CLAIM、R-LOC、R-PAGE-STALE、R-RENUM、R-MD-SYNTAX、
  R-PLACEHOLDER、R-NUM-SRC、R-REVIEW-CHANGED、R-SHARED、R-RESULT、R-SYNC、R-TONE。R-NUM-SRC 与 R-TONE 为 NEEDS-LLM 候选。
  `--json` 含 `findings`、`summary`、`skipped`；严重度与优先级 Critical=P0、Major=P1、Minor=P2、Info=P3。

## 4. Validation & Error Matrix

| Condition                                          | Required behavior                                                          |
| -------------------------------------------------- | -------------------------------------------------------------------------- |
| 评阅书目录含 `.docx`/`.doc`/图片且无可读评阅书     | intake 退出 2                                                              |
| 扫描版 PDF 无文字层                                | 生成空骨架并报 W-NO-TEXT，退出 0                                           |
| 已有 `workspace/reviews/`、无 `--force`            | intake 退出 4，不写任何文件                                                |
| responses 文件被手改、无 `--force`                 | build 退出 4；check 报 R-SYNC Minor                                        |
| `clarify`/`decline` 或未完成条目的回复含完成用语   | R-CLAIM Critical                                                           |
| `status: done` 的修改类条目无证据或 git 无对应修改 | R-COMMIT Critical                                                          |
| 无 `--thesis`                                      | R-COMMIT(git)、R-LOC(aux)、R-PAGE-STALE、R-RENUM、R-NUM-SRC 记入 `skipped` |
| 有 `--thesis` 但非 git 仓库或无基线提交            | 只跳过 R-COMMIT(git)，`git_diff` 条目报 R-COMMIT Info                      |
| 评阅书 sha256 与 intake 时不同                     | R-REVIEW-CHANGED Major                                                     |

## 5. Good / Base / Bad Cases

- Good：修改一个 R-* 判据时，同时改 `rebuttal_check.py`、`references/rebuttal-gate.md`（含双语资源页与 manifest 散列）与该码的正反例测试。
- Base：用 `evals/fixtures/rebuttal/concerns-done.yaml` 与 `mini-thesis` 跑 intake → build → check，check 零结果。
- Bad：为消除 R-COMMIT 把 `evidence.kind` 改为 `user_confirmed` 而用户未确认；在 fixture 或任务目录写入真实评阅人、作者或论文题目。

## 6. Tests Required

- `tests/skills/latex_thesis_zh/`：`test_thesis_rebuttal_intake.py`（归一化、锚点、退出码、`--force`）、
  `test_thesis_rebuttal_build.py`（渲染格式、位置与页码、手改保护）、`test_thesis_rebuttal_check.py`（16 码正反例、git 口径、skip 规则）、
  `test_thesis_rebuttal_installed.py`（独立安装），入口归属回归（三个回复模块归 thesis，defense 保持五个原模块）。
- 契约测试：`tests/contracts/test_skill_contracts.py`、`test_trigger_evals.py`、`test_docs_bilingual_resources.py`；
  资源门 `uv run python docs/scripts/check_resource_sync.py`。

- 隔离安装回归：只复制 thesis 技能，移除仓库 PYTHONPATH，从包外 cwd 通过三个 CLI 跑合成评阅书与有真实 git 修改证据的论文；核对回复输出、R-* 结果和输入哈希不变。
- 触发边界：中文学位论文评阅回复为正例；Beamer、期刊/会议回复和审稿评分不由此模块接管。静态 fixture 通过不等于 provider 触发通过。

## 7. Wrong vs Correct

```yaml
# Wrong: clarify item claims a change that did not happen.
- id: R1-3d
  action: clarify
  response: 已补充第2章与第3章的衔接说明。

# Correct
- id: R1-3d
  action: clarify
  response: 第3章引言第1段说明了第2章模型在本章中的用途。
```
