# C2 设计

父 `design.md` 是契约来源。本文件只写 C2 的文件清单与实现取舍。

## 1. 文件

新增：

- `academic-writing-skills/latex-defense-zh/scripts/rebuttal_build.py`
- `academic-writing-skills/latex-defense-zh/scripts/rebuttal_check.py`
- `academic-writing-skills/latex-defense-zh/evals/fixtures/rebuttal/concerns-done.yaml`：合成的「已完成」台账，对应 C1 两份 txt 评阅书，
  覆盖 `revise`、`add`、`clarify`、`future_work`、`decline` 与一组 `shared_with`。
- `tests/skills/latex_defense_zh/test_defense_rebuttal_build.py`
- `tests/skills/latex_defense_zh/test_defense_rebuttal_check.py`

修改：

- `tests/skills/latex_defense_zh/conftest.py`：新增 fixture `rebuttal_case(tmp_path)`：
  1. 复制评阅书目录与 mini-thesis 副本（含 C1 写入的 `document.aux`）；`git init` 并提交为基线；
  2. 运行 intake；
  3. 修改副本：在 `chapters/chapter2.tex` 插入一张图使原 `图2-1` 变为 `2-2`（同步改 `chapter2.aux`，页码后移一页），改写一处文字；提交；
  4. 把 `concerns-done.yaml` 写入 `workspace/concerns.yaml`（证据文件指向第 3 步改动的文件）；
  5. 把副本中全部 aux 的修改时间设为晚于 tex（`os.utime`）。
     返回 `SimpleNamespace(root, reviews, thesis, workspace)`。无 git 可执行文件时依赖它的测试 skip。

## 2. build 实现取舍

- 渲染用纯 Python 字符串拼接，不用 Jinja2：输出为纯文本，模板逻辑只有循环与位置格式化。
- 子项分组：同一 `item` 的条目按 `id` 后缀字母排序；原文只输出一次，取父条目的完整 quote（从 `reviews/R<n>.md` 第 `item` 条读取）或任一子项的 `quote_short`。
- 总体说明计数：意见条数 = 各评阅书编号意见数之和；项数 = 台账条目数；处理方式计数按 `action`。感谢句只出现在总体说明。
- 输出统一 `\n` 换行、UTF-8 无 BOM、文件末尾一个换行。
- `anchors.json`：`[{concern, text, label, base_number, base_page, number, page, status: resolved|missing|no_thesis}]`。
- `rendered` 记录写入后文件的 sha256；首次渲染时 responses 文件不存在，不触发退出码 4；文件存在但不在 `rendered` 中视为手改。

## 3. check 实现取舍

- 每个码一个函数 `check_<code>(ctx) -> list[Finding]`，`ctx` 含台账、state、评阅原文、responses 文本、aux、git 改动集合；顺序按父 design §7 表格。
- R-QUOTE 比较前去除全部空白字符（PDF 提取的换行与空格不稳定）。
- R-COMMIT：`files = evidence.files ∪ locations 中的 file ∪ label 所在 aux 对应的 tex`；标签对应 tex 由 aux 文件名推断（`chapters/chapter2.aux` → `chapters/chapter2.tex`）。
  从 `git_changed_files` 结果中剔除以 `$ROOT` 相对仓库路径或评阅书目录开头的路径后再求交集。
- R-PAGE-STALE：比较 tex 与同名 aux 的 `st_mtime`；无同名 aux 时比 `document.aux`；都不存在时报 R-LOC。
- R-MD-SYNTAX：逐行正则；报告行号；父 design §5 的禁止项各一个正则常量。
- R-NUM-SRC：从回复中取 `\d+\.\d+` 与 `\d+(\.\d+)?%`；论文数字集合不含时报 Major，消息注明 NEEDS-LLM；评阅原文中出现的同一数字降为 Info。
- R-TONE：开头句取每条回复前 12 个字符计数；词表常量写在脚本顶部。
- 结果排序：严重度 → 码名 → concern 编号。

## 4. 测试清单

`test_defense_rebuttal_build.py`：

| 测试                              | 断言                                                 |
| --------------------------------- | ---------------------------------------------------- |
| `test_help_lists_cli_options`     | build 与 check 的 `--help` 含父 design §8 选项       |
| `test_plan_only`                  | 只写 `revision_plan.md`；重叠意见合并为一行          |
| `test_full_render_structure`      | 5 类文件存在；每条含三段；总体说明计数正确           |
| `test_location_renumber_and_page` | 「原图2-1，现图2-2（第13页）」                       |
| `test_plain_text_equivalent`      | 去 Markdown 渲染后逐行相同                           |
| `test_hand_edit_guard`            | 手改后退出码 4；`--force` 覆盖并更新 `rendered`      |
| `test_invalid_ledger_exit_2`      | 缺 `schema`、非法 `action` 时退出码 2 并列出全部错误 |
| `test_readonly`                   | 论文副本与评阅书目录 sha256 不变                     |

`test_defense_rebuttal_check.py`：`test_clean_case_passes` 加 16 个 `test_<code>_negative`（每个在 `rebuttal_case` 上做最小破坏），
另有 `test_commit_ignores_rebuttal_root_changes`、`test_skipped_without_thesis`、`test_json_payload_and_check_json`。
