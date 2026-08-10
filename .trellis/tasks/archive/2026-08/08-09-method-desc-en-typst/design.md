# C2 技术设计：EN 扩展与 typst 镜像

判据唯一权威 = 父 design §2（不复述）。机制事实见父 research/repo-recon.md。实现前通读
EN `analyze_logic.py`（`--section` 门控分支 :750-767、TRANSITIONS :27-31、两条行级启发式）
与 typst 副本对应区段（行号偏移约 12）。

## 1. 检查器实现落点（EN 为准，typst 同构镜像）

- 挂载：新函数反向门控 `if section == "methods"`，置于 :750 节级检查区（现有检查的
  `if not section` 门控一律不动——audit 双调用依赖此互斥，见父 design §5）。
- 常量组织：MN_ 前缀常量与 zh 同名（MN_HEADING_RUN / MN_HEADING_HITS /
  MN_EQUATION_LOOKAHEAD / MN_ANNOUNCE_RE / MN_SEQ_OPEN_RE / MN_CAUSE_EXEMPT_RE /
  MN_EQ_GLOSS_RE），注释标注"唯一权威=父任务 design §2，由
  test_method_narrative_alignment.py 锁定"。
- M-SEQWORD 顺序词起手集合 = TRANSITIONS["sequence"]（新增类）派生，单一来源；
  MN_SEQ_OPEN_RE 由该词组拼接构造，不重复字面量。
- typst 行内小标题正则、labeled 块公式识别按父 design §2.1/§2.3；label 解析用现有
  parser/正则能力，不引入模板级 numbering 判定。
- M-EDGETABLE：EN 用 `\subsection`/`\subsubsection`，typst 用 `==`/`===`。

## 2. EN method.md 扩展写法

- 逐边表并入现有 Pre-Writing Table 之后（原表保留）；四个新节顺序：Inter-module interface
  contract → Equation closure → Heading discipline → Evidence tiers（映射节）。
- 每节 ≤25 行；Heading discipline 双向（反模式 + 合法边界，引用 style-guide.md 行号区间）。
- 诊断入口更新为含 `--section methods` 的现行命令（已在路由行，无命令变更）。

## 3. typst METHOD_SECTION.md

结构：authoritative 注记（`latex-paper-en/references/writing/section-writing/method.md`，
小写）→ Typst 语法差异要点 → 逐边接口表 Typst 示例 → 诊断入口。只译要点，不整文复制。

## 4. 契约测试实现（R4）

- `tests/contracts/test_method_narrative_alignment.py`：按 `test_body_chapters.py` 的
  importlib 模式分别加载三副本（zh 侧带 sys.modules 保存恢复），断言 prd R4 三组等式。
- 断言对象是**常量值/正则 pattern 源串**，不比对函数字节（允许注释与格式差异）。
- 与 `test_writing_modules_alignment.py` 的 Tier 锁并存：本测试锁判据语义，Tier 锁管
  文件级同构，互不替代。

## 5. 测试设计

- EN/typst 各自测试文件新增用例（定位现有 analyze_logic 测试文件，跟随其 fixture 惯例；
  EN 侧脚本在默认 sys.path 直接 import，typst 侧按其现有加载方式）。
- 红线负例：EN `_RELATED_WORK_BOLD`（`\textbf{Transformer-based methods.}` 三连 + 引文式
  正文，置于 related work 节名下）；typst `_EXP_LEADIN`（`*Strong Result Heading.* 数值句`
  置于 experiment 节名下）——两者在 `--section methods` 下不进入扫描范围，断言零 finding。
- TRANSITIONS 回归：对现有 LOGIC/METHODOLOGY fixture 断言补类后 finding 集合不增。

## 6. 风险与提交分组建议

- 风险：`--section methods` 的节名匹配对 "Methodology"/"Proposed Method" 等变体的覆盖——
  沿用现有 `--section` 匹配语义（parser section 键），测试加一条 "Proposed Method" 标题
  定位断言；不扩节名词表（那是现有机制的口径）。
- 提交分组建议（Phase 3.4 由主会话执行，实施代理不 commit）：
  A 组＝TRANSITIONS sequence + M-* 检查器 + 两侧测试 + 契约测试
  （`feat(latex-paper-en,typst-paper): 方法节叙述候选检查`）；
  B 组＝method.md 扩展 + METHOD_SECTION.md + SKILL.md + manifest + 双语页
  （`docs(latex-paper-en,typst-paper): 方法节逐边接口参考`）。
