# C1 设计

父 `design.md` 是契约来源。本文件只写 C1 的文件清单与实现取舍。

## 1. 文件

新增：

- `academic-writing-skills/latex-defense-zh/scripts/rebuttal_common.py`：父 design §2 全部函数。
- `academic-writing-skills/latex-defense-zh/scripts/rebuttal_intake.py`：CLI 与归一化。
- `academic-writing-skills/latex-defense-zh/evals/fixtures/rebuttal/reviews/评阅书1.txt`：合成，两页（以换页符 `\f` 分隔），
  每页含重复水印行、`<数字>_<数字>_示例 第N页` 页脚与单独页码；评分表、学术评语与 3 条 `1.` 编号意见，第 3 条为复合意见，含 `图2-1`、`式(2-1)`、`文献[3]`。
- `academic-writing-skills/latex-defense-zh/evals/fixtures/rebuttal/reviews/评阅书2.txt`：合成，`1、` 编号，2 条，含 `第3章至第5章`、`2.3节`、`文献[1,2]`。
- `tests/skills/latex_defense_zh/test_defense_rebuttal_intake.py`。

修改：

- `tests/skills/latex_defense_zh/conftest.py`：`_SHARED_MODULE_NAMES` 追加 `"rebuttal_common"`；新增 fixture `rebuttal_thesis(tmp_path)`
  复制 `mini-thesis` 并写入含两条 `\bibcite` 的 `document.aux`。

fixture 文本必须是合成内容：题目、姓名、学号、评阅编号与正文均为虚构，与任何真实评阅书不同。

## 2. 实现取舍

- 页切分：PDF 按页；txt/md 按 `\f` 切页，无 `\f` 时整体一页（单页不做重复行删除）。
- 重复行判定对行做 `strip()` 后比较；水印截断行（如「学位中心学」）在每页出现时同样满足阈值，被删除。
- 评分解析在整篇文本上运行（评分表可能跨行：「总分」与数字分在两行时，先把评分区域行合并再匹配）。
- 编号递增检查避免把「1.5 倍」「2、3 两章」之类误切：只接受行首编号，且下一个编号等于上一个加 1。
- `find_anchors` 返回 `(text, kind, key)`，`key` 为归一化编号（`2-7`、`3`、`2.3`、`24`）；章范围 `第3章至第5章` 展开为 3、4、5 三个 chapter 锚点。
- 基线映射：图表式算法按 `kind` 前缀筛选 aux 标签（`fig:`/`tab:`/`eq:`/`alg:` 不作为强制约定；以 aux 中 `figure.`、`table.`、`equation.`、`algorithm.` 锚名判断类型），
  编号相等即匹配；章与节按 aux 中 `chapter.`/`section.` 锚名匹配；文献用 `\bibcite` 序号。多个标签编号相同时取第一个并 warning。
- 台账 YAML 用 `yaml.safe_dump(..., allow_unicode=True, sort_keys=False, width=1000)`，避免长中文被折行。
- 不新增依赖；PyMuPDF 导入写法与 `render_preview.py` 一致。

## 3. 测试清单（`test_defense_rebuttal_intake.py`）

| 测试                                 | 断言                                                                          |
| ------------------------------------ | ----------------------------------------------------------------------------- |
| `test_help_lists_cli_options`        | 父 design §8 intake 全部选项出现在 `--help`                                   |
| `test_txt_reviews_normalized`        | 无水印/页脚行；条数 3 与 2；等级、总分、同意答辩                              |
| `test_pdf_review_normalized`         | PyMuPDF 生成 PDF 后同上；`importorskip`                                       |
| `test_anchor_detection`              | 父 design §2 所列形式全部识别，章范围展开                                     |
| `test_anchor_mapping_with_thesis`    | `图2-1` → `fig:c2-profile`、`base_page` 12；`文献[1]` → bib 键                |
| `test_directory_layout_and_readonly` | `responses/`、`workspace/` 为评阅书目录的同级；输入与论文副本 sha256 不变     |
| `test_exit_codes`                    | 2（缺目录、.docx、嵌套）、3（monkeypatch 使 PyMuPDF 导入失败）、4（重复运行） |
| `test_force_keeps_ledger`            | `--force` 重写 reviews 与 state，`concerns.yaml` 字节不变                     |
| `test_without_thesis`                | 无 `--thesis` 时 label 为 null，`thesis.given=false`                          |
| `test_base_commit_recorded`          | `tmp_path` 中 `git init` 并提交后，state 记录 HEAD；无 git 可执行文件时 skip  |
