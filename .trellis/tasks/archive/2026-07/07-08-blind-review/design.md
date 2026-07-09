# design — 盲审匿名化检查与盲审版tex生成

## 1. 检测面（--check）

| 规则 | 定位方式 | severity |
| --- | --- | --- |
| R1 作者/导师字段 | 字段宏正则：`\author{...}`、`\thusetup{author=,supervisor=,...}`、pkuthss `\设置{author}{...}` 等模板字段表（FIELD_PATTERNS，按模板 id 选用 + generic 兜底） | HIGH |
| R1 致谢非空 | 章节标题正则 `致\s*谢|acknowledg` 命中后取该章可见文本长度 > 阈值（~10 字） | HIGH |
| R1 全文姓名 | 仅 `--author`/`--supervisor` 提供时：assemble 后可见文本逐行 `str.find`（含去空格变体）；致谢/成果章内命中升 HIGH，其他章 MEDIUM | HIGH/MED |
| R2 成果条目 | 定位成果章（标题正则 `攻读.*(期间).*(成果|论文)`）；条目行检出 页码 pattern（`[:：]\s*\d+\s*[-–]\s*\d+`）、多作者列表征兆（顿号/逗号分隔 2+ 个 2-4 字中文词后随句点）、成果名称（引号/书名号包裹段） | HIGH |
| R3 扩展 | 原创性声明/授权（标题正则）、基金号（`No\.\s*\d|基金.*(编号|资助)`）、封面字段（题名页宏） | INFO（以学校通知为准） |

输出行格式沿用仓库契约：`% BLIND-REVIEW (chapters/ack.tex:L12) [HIGH] [P0] [Script]: R1 致谢内容未隐去`。

## 2. 生成面（--generate）

流程（全部基于 tex_loader 的文件级信息，不重新发明解析）：

1. `--check` 全量跑一遍 → findings 分为 `AUTO`（字段值替换、致谢占位）与
   `LLM`（R2 条目改写、正文姓名句、未识别字段）。
2. 受影响文件集合 = 含 AUTO/LLM finding 的源文件 ∪ 入口文件。
3. 每个受影响文件写 `<stem>_blind.tex`（同目录）；入口副本中把指向受影响文件的
   `\input{x}` / `\include{x}` 改为 `x_blind`；未受影响文件不复制、引用不改。
4. AUTO 替换（只在副本上）：
   - 字段值 → `□□□`（保留宏与花括号结构，长度不敏感）；
   - 致谢章：标题保留，正文整块替换为一行"（盲审版本，致谢内容略）"；
   - 每处替换点上一行插 `% BLIND-AUTO(R1): 原内容已隐去`。
5. LLM 项：副本原样保留 + 上一行插 `% TODO-BLIND(R2|R1): <指引>`；报告汇总所有 TODO 供
   agent 逐条给 diff 建议（`[LLM]` 标注，用户确认后应用）。
6. `--dry-run`：只打印第 2~5 步计划（文件清单 + 替换点列表），零写盘。
7. 幂等与安全：目标 `_blind` 文件已存在时要求 `--force` 才覆盖；写盘前后对原文件列表做
   内容哈希对比并在报告末尾打印"原文件未改动"确认行（这也是测试断言点）。

保真约束：替换只发生在字段值/致谢正文/注释插入三类位置，均先经 parser 确认不在
math/`\cite`/`\ref`/`\label` 上下文内；R2 条目内容脚本零改写（防止破坏署名次序事实）。

## 3. 模块文档与清单联动

- `references/modules/blind-review.md` 含「盲审隐匿清单」小表（R1/R2/R3 逐项 + 检查方式），
  格式与 spec-check 的逐项清单一致——终检时 spec-check 报告可提示
  "盲审送审前另跑 blind-review 模块"。
- `templates/yanshan.md` 的 `## 盲审` 节：R1/R2 用户提供原文（逐字）、R2 改写示例：

  改写前：`[1] 张三, 李四, 王五. 某某机构的某某研究[J]. 机械工程学报, 2024, 60(5): 100-110.`
  改写后：`[1] 第一作者，机械工程学报，2024`

  （示例中的姓名/题名为占位虚构，仅演示格式，须在文档中注明。）

## 4. SKILL.md 集成

- router 行：`blind-review` | 盲审送审前个人信息隐匿检查与盲审版生成 |
  `uv run python $SKILL_DIR/scripts/blind_review.py main.tex --check` |
  `references/modules/blind-review.md`。
- 路由规则：涉及"盲审/外审/送审版本/匿名版/隐去姓名致谢"走 `blind-review`；
  只问格式合规仍走 `spec-check`。
- Safety Boundaries 补一句：盲审生成只写 `_blind` 副本，永不修改原文件。

## 5. 测试设计

`tests/skills/latex_thesis_zh/test_blind_review.py`（importlib + 加载守卫）：

- fixture：在 `evals/fixtures/thesis-project/` 增加 `chapters/acknowledgement.tex`（含导师姓名）
  与 `chapters/achievements.tex`（两条成果：一条含姓名列表+成果名+页码，一条已合规），
  main.tex 增加 `\author{测试作者}` 与两个 `\input`（带 `% seed:` 埋点注释）。
  注意：该 fixture 同时服务 spec-check 的 wordcount 等检查器，加文件后回跑
  test_check_spec.py 确认无阈值级联破坏。
- 用例：check 检出全部预埋点（含行号）；generate 副本断言（原文件哈希不变、字段 □□□、
  致谢占位、TODO-BLIND 注释、`\cite`/`\ref`/`\label`/math 逐字保留）；dry-run 零写盘；
  已存在 `_blind` 时无 --force 拒绝；--author 全文扫描命中正文姓名句。

## 6. 取舍记录

- **不做** 姓名拼音/学号/邮箱等启发式全家桶：误报率高且校方通知未要求；R3 只列 INFO 提示。
- **不做** PDF 元数据清理（hyperref pdfauthor 除外——它是 tex 源内字段，纳入 FIELD_PATTERNS）。
- **不做** 成果条目自动改写：格式千差万别，脚本只定位 + LLM 给建议，红线是不改变署名次序事实。
