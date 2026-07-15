# 执行清单 — 07-15-audit-fix-latex-paper-en

约定：
- 每个 finding 先写**失败的回归测试**，确认红，再修，确认绿（tests-first）。
- 快速验证命令别加 `PYTHONIOENCODING=utf-8`（memory 陷阱：会炸 test_skill_contracts 的 subprocess 用例）。
- 新测试路径常量一律 `from tests.support.paths import SCRIPT_DIR_EN, SKILLS_ROOT`（spec 约定）。
- 缩写：`PYT = uv run --extra dev python -m pytest`。
- **提交纪律（workflow.md Phase 3.4）**：Phase 2 批次内**不执行 `git commit`**。每批以验证闸门
  收口后，登记一条**拟提交分组**（Gn：文件集**分列「修改的既有文件」与「本批新建文件」** +
  拟用 commit message）；全部批次绿、`just ci` 通过且 Phase 3.3 spec 更新完成后，在 Phase 3.4
  把分组一次性呈报用户确认，确认后按序提交。
  批内回滚一律 **scoped restore，禁用 reset**：既有文件 `git checkout -- <该批修改文件>`
  （需留证先 `git stash push -- <files>`）；本批**新建文件（各批的 test_*.py 等）checkout
  无法移除，按分组登记清单单列显式 `rm`**。不用 commit revert。

---

## Batch 0 — 基线确认（无代码改动）

- [ ] 确认前置任务 07-15-audit-fix-version-ci 已合入 dev（`git log --oneline -5` 可见版本对齐 commit）。
      若未合入：停，先等绿基线（父约束 #1）。
- [ ] `just ci` → 记录当前全绿基线（约 1177+ 用例）。
- [ ] `PYT tests/contracts/test_parsers_alignment.py tests/contracts/test_deai_alignment.py -q` → 全绿快照。

## Batch 1 — R1：check_references 多文件（A-EN-1）

1. [ ] 新建 `tests/skills/latex_paper_en/test_check_references_multifile.py`：
       - fixture：沿用 `tests/shared/test_en_family_parsers_multifile.py:177-194` 的
         `_write_tex_project` 模式，label（`\label{fig:arch}` + `\caption`）放
         `sections/method.tex`，`\ref{fig:arch}` 放 `sections/intro.tex`；
       - 用例 A：run_all 后 undefined-reference issue 数 == 0（当前红：假 P0）；
       - 用例 B：CLI exit code == 0（subprocess 或调 main 前 monkeypatch argv）；
       - 用例 C：故意留一个真 undefined ref，文本输出定位含 `sections/intro.tex:`；
       - 用例 D：缺失 `\input{ghost}` 产生 WARN 行，不 crash；
       - 用例 E（单文件不变性）：单文件 fixture 输出串与改动前 golden 相同（`Line N` 格式）。
       验证：`PYT tests/skills/latex_paper_en/test_check_references_multifile.py -q` → A/B/C/D 红。
2. [ ] 按 design §2.2 改 `check_references.py`（main 接 assemble；LabelInfo/RefInfo 补
       源坐标；`_add_issue` 加 `location`；`_format_issues` 用 location；JSON 加
       `file`/`source_line`）。
3. [ ] 验证：`PYT tests/skills/latex_paper_en -q` 全绿（含既有 test_latex_paper_en_scripts.py
       的 check_references 用例零断言改动）。
4. [ ] `just fix` → `just lint`。

**Review Gate 1**：diff 只含 check_references.py + 新测试；内部行号全装配坐标、渲染边界才转
lineref（design §7 风险 1 检查项）。
**拟提交分组 G1**（记录，不提交）：文件集 = `check_references.py` + `test_check_references_multifile.py`；
message：`fix(latex-paper-en): [AI] check_references 接入 tex_loader.assemble 修多文件假 P0（A-EN-1）`。
**回滚点：`git checkout -- <G1 修改文件>` + `rm <G1 新建文件>`。**

## Batch 2 — R2+R5：section 别名统一（A-EN-2 / A-EN-5）

1. [ ] 新建 `tests/skills/latex_paper_en/test_section_aliases.py`（红先行）：
       - analyze_logic：`--section methods` 命中 method 区间（断言非 "Section not found"）；
         `--section "related work"` 时 A1/A3 检查照跑；未知名输出含 available 列表；
         `method_2` 重复节都被扫描；
       - analyze_literature：`--section "related work"`/`literature` 命中；默认 `related` 行为不变；
       - deai_batch：`--section methods` found；未知名列 available。
       验证：`PYT tests/skills/latex_paper_en/test_section_aliases.py -q` → 红。
2. [ ] 改 `analyze_logic.py`（design §3.2：:676 与 :736 两处 + import）。
3. [ ] 改 `analyze_literature.py`（design §3.3：`_find_section_bounds` 返回多区间 + 迭代）。
4. [ ] 改 `deai_batch.py`（design §3.3：:273-277 + import）。
5. [ ] SKILL.md 示例实跑验证（用 tests fixture 或临时合成论文）：
       `uv run python -B academic-writing-skills/latex-paper-en/scripts/analyze_logic.py <fixture>.tex --section methods`
       → exit 0 非 Section-not-found；同法验 SKILL.md:62 `analyze_literature ... --section related`。
6. [ ] `PYT tests/skills/latex_paper_en -q && just lint`。

**Review Gate 2**：三脚本错误文案格式与 `deai_check.py:1066-1075` 样板一致。
**拟提交分组 G2**（记录，不提交）：文件集 = `analyze_logic.py`/`analyze_literature.py`/
`deai_batch.py` + `test_section_aliases.py`；message：`fix(latex-paper-en): [AI]
analyze_logic/literature/deai_batch 统一 resolve_section_keys（A-EN-2/A-EN-5）`。
**回滚点：`git checkout -- <G2 修改文件>` + `rm <G2 新建文件>`。**

## Batch 3 — R4+R10：canonical parsers.py + 三副本同步（A-EN-4 / A-EN-10）

1. [ ] 在 `tests/shared/test_parsers.py`（或新建 `tests/skills/latex_paper_en/test_parsers_title_abstract.py`）
       写红测试：
       - R4：环境式 abstract fixture → `split_sections` 含 `abstract` 键、区间为 begin..end 行；
         标题式已存在时不重复；`% \begin{abstract}` 不注册；
       - R10：design §4 五个用例（嵌套花括号 / thanks 嵌套体 / footnote / `\title {X}` 空白 /
         无 \title 走 Typst 分支）。
       验证：`PYT <该文件> -q` → 红。
2. [ ] 改 `academic-writing-skills/latex-paper-en/scripts/parsers.py`：
       - `LatexParser.split_sections` abstract 环境注册（design §3.4）；
       - `extract_title` 平衡花括号 + 新增模块级 `_strip_balanced_commands`（design §4）。
3. [ ] **三副本同步**（canonical → 镜像，逐字节）：把上述两个成员 + 新 helper 同步到
       `paper-audit/scripts/parsers.py` 与 `cover-letter/scripts/parsers.py`。
4. [ ] 编辑 `tests/contracts/test_parsers_alignment.py`：`ALIGNMENTS` 增
       `("_strip_balanced_commands", ["en", "audit", "cover_letter"])`（唯一列表变更）。
5. [ ] 验证（闸门链，逐条跑）：
       - `PYT tests/contracts/test_parsers_alignment.py -q` → 全绿（三副本互比一致）；
       - `PYT tests/shared -q`；
       - `PYT tests/skills/latex_paper_en tests/skills/paper_audit tests/skills/cover_letter -q`
         （下游消费方：extract_section_anchors 新增 abstract 键、extract_title 新行为；
         有翻红用例逐个核对是否"旧断言锁旧缺陷"，是则更新断言并在 commit message 声明）；
       - deai_check abstract 可达：临时 fixture 实跑
         `uv run python -B .../deai_check.py fixture.tex --section abstract` → 命中非 ERROR。
6. [ ] `just lint && just typecheck`（pyright basic，看 error 数）。

**Review Gate 3**：diff 恰好三份 parsers.py 被改成员逐字节相同（`git diff` 三段可互 diff 校验）；
ALIGNMENTS 仅 +1 行；zh/typst parsers.py 零改动（typst 任务地盘，design §6）。
**拟提交分组 G3**（记录，不提交）：文件集 = en/audit/cover_letter 三份 `parsers.py` +
`test_parsers_alignment.py` + 新测试文件（含受新真值影响而更新断言的用例）；message：
`fix(parsers): [AI] abstract 环境注册 + extract_title 平衡花括号，三副本同步（A-EN-4/A-EN-10）`，
message 声明默认行为变化（split_sections 新增 abstract 键）与 A-CL-7 前置契约。
**回滚点：`git checkout -- <G3 修改文件>` + `rm <G3 新建文件>`，不影响 G1/G2。**

## Batch 4a — R3：分析/检查脚本批量接入 assemble（A-EN-3 主体）

1. [ ] 新建 `tests/skills/latex_paper_en/test_multifile_scripts.py`（红先行）：
       共享一个模块级 fixture 工厂（skeleton main + sections/intro|method|experiment.tex +
       环境式 abstract + figure/table/algorithm 素材各一），逐脚本两条用例：
       - 多文件：脚本在 skeleton 上产出与单文件等价的关键发现（当前红：0 发现 / not found）；
       - 单文件：输出与改前一致（既有用例覆盖者标注即可，不重写）。
       本批覆盖脚本（9+1）：deai_check、analyze_logic、analyze_experiment、analyze_literature、
       analyze_abstract、check_figures、check_tables、check_pseudocode、optimize_title、deai_batch。
2. [ ] 按 design §2.1/§2.3/§2.4 表逐脚本改造（读取位点见表；行号标签 → `doc.lineref`；
       deai_check 只动不锁成员，suggestions JSON 在 main() 后处理补 source 字段；
       deai_batch 的 `process_section_file` 保持单文件读）。
       **analyze_abstract 特别项**（design §2.6/§6）：改法须 loader 无关，改完把
       `typst-paper/scripts/analyze_abstract.py` 字节镜像同步（en+typst Tier-1 锁）。
3. [ ] 验证（每改 2-3 个脚本跑一轮）：
       - `PYT tests/skills/latex_paper_en -q`；
       - `PYT tests/contracts/test_deai_alignment.py -q`（deai_check 改动后必跑——锁定成员
         源码必须零 diff）；
       - `PYT tests/contracts/test_writing_modules_alignment.py -q`（analyze_abstract 改动后必跑——
         en/typst 哈希互比）；
       - `PYT tests/skills/paper_audit -q`（run_audit 汇聚这些脚本 JSON/输出）。
4. [ ] `just fix && just lint && just typecheck`。

**Review Gate 4a**：grep 确认改动脚本内无残留裸 `read_text` 入口
（`rg -n "file_path.read_text|tex_file.read_text" academic-writing-skills/latex-paper-en/scripts`
仅剩 design §2.5 白名单脚本 + deai_batch:191 + §2.6 三脚本的 assemble=None 降级分支）；
deai 锁零漂移；analyze_abstract en/typst 哈希一致。
**拟提交分组 G4**（记录，不提交）：文件集 = 本批 9+1 脚本 + typst `analyze_abstract.py` +
`test_multifile_scripts.py`；message：`fix(latex-paper-en): [AI] 十脚本接入 assemble
消多文件盲区（A-EN-3 主体，九分析/检查+deai_batch）`。**回滚点：`git checkout -- <G4 修改文件>` +
`rm <G4 新建文件>`（含 test_multifile_scripts.py）。**

## Batch 4b — R3 扩入：grammar/sentences/expression 三脚本 + typst 字节同步（A-EN-3 裁决补列）

1. [ ] 在 `test_multifile_scripts.py` 补三脚本红测试（fixture 工厂复用，文件边界留空行，
       design §2.6 sentences 段落合并注意点）：
       - analyze_grammar：规则语料（如 "the data shows"）放 `sections/method.tex` →
         多文件下 GRAMMAR 发现非空且定位 `sections/method.tex:N`（当前红：skeleton 下 0 发现）；
       - analyze_sentences：超阈值长句放分节文件 → LONG SENTENCE 发现，定位为段首行的
         `sections/x.tex:N` 形态；
       - improve_expression：弱表达（"a lot of"）放分节文件 → EXPRESSION 建议，**Revised 建议的
         定位落在正确源文件行**（可回写性断言，design §2.6）；
       - 三脚本各一条单文件不变性用例（`Line N` 标签逐字节不变）。
       验证：`PYT tests/skills/latex_paper_en/test_multifile_scripts.py -q` → 三脚本用例红。
2. [ ] 按 design §2.6 模式改 en 侧三脚本（import 降级扩 `assemble`；`analyze()` 接
       `doc.content/lines` + `doc.lineref`；`assemble=None` 降级路径保留；三者已用
       `resolve_section_keys`，别名逻辑零改动）。
3. [ ] **typst 字节同步**：三脚本改后整文件镜像到 `typst-paper/scripts/`
       （analyze_grammar/analyze_sentences/improve_expression 各一）。
4. [ ] 验证：
       - `PYT tests/contracts/test_writing_modules_alignment.py -q`（四文件 Tier-1 组全绿）；
       - `PYT tests/skills/latex_paper_en -q`；
       - typst 侧既有用例：`PYT tests/skills/typst_paper -q`（若目录名不同以 `PYT tests -q
         -k typst` 定位；typst 副本经 typ_loader.assemble 获得 `.typ` 装配，属声明过的
         顺带收益，翻红用例逐个核对是否"旧断言锁单文件行为"）。
5. [ ] SKILL.md 路由表命令全量实跑（AC）：:59-:70 各行示例命令替换 fixture 路径逐条执行，
       记录 exit code（grammar/sentences/expression 三行本批已改码，属一等回归面）。
6. [ ] `just fix && just lint && just typecheck`。

**Review Gate 4b**：`git diff` 中 en/typst 三对文件逐对零差异（可 `diff <(git show :en) <(git show :typst)`
或直接比对工作区）；写作模块锁全绿；typst 侧除这三个文件外零改动。
**拟提交分组 G5**（记录，不提交）：文件集 = en 三脚本 + typst 三脚本镜像 +
`test_multifile_scripts.py` 增量；message：`fix(latex-paper-en): [AI]
grammar/sentences/expression 接入 assemble 并同步 typst 副本（A-EN-3 裁决扩入）`，
message 声明 typst 侧 `.typ` 多文件装配顺带启用。**回滚点：`git checkout -- <G5 修改文件>` + `rm <G5 新建文件>`。**

## Batch 5 — Low 四项（A-EN-6/7/8/9）

1. [ ] R8 红测试（`tests/skills/latex_paper_en/test_logic_funnel_brackets.py` 或并入
       test_section_aliases.py）：`[0, 1]` 不触发 first_prior、`[12]` 触发（构造 funnel 输出
       可区分的两个 fixture）。改 `analyze_logic.py:220`（design §5 NUMERIC_CITE_RE）→ 绿。
2. [ ] R7：删 `check_figures.py:142-144` 死表达式与陈旧注释；既有/新增 check_quality 用例保持绿
       （Batch 4a 的 check_figures 多文件用例即回归面）。
3. [ ] R6：删 SKILL.md:134 重复行 → `PYT tests/contracts/test_skill_contracts.py -q`（必跑，
       防 hook 重排表格触发 ROUTER_ROW_RE）。
4. [ ] R9：check_format.py docstring + `references/modules/format.md` 加 best-effort 注记
       （行为零变化）→ `PYT tests/skills/latex_paper_en -q` 确认 check_format 用例不红；
       `PYT tests/contracts/test_docs_bilingual_resources.py -q`（改了 references/ 下文档，
       双语资源契约测试必跑）。
5. [ ] `just fix && just lint`。

**Review Gate 5**：R6/R9 是纯文档 diff、无行为变化；R7/R8 各有测试背书。
**拟提交分组 G6**（记录，不提交）：文件集 = SKILL.md、check_figures.py、analyze_logic.py、
check_format.py、`references/modules/format.md` + 相应测试；message：
`fix(latex-paper-en): [AI] Low 级清理：SKILL 重复行/死表达式/funnel 误判/format 注记（A-EN-6..9）`。
**回滚点：`git checkout -- <G6 修改文件>` + `rm <G6 新建文件>`。**

## 收尾 — 全量集成验证（Phase 2 末）

- [ ] `just ci` 全绿（lint → pyright（error 数为 0 增量）→ 全部测试）。
- [ ] `PYT tests/contracts -q` 单独复跑（parsers/deai/writing-modules 三锁 + skill contracts +
      versions）。
- [ ] 对照 prd.md 逐条勾 AC；确认每项 finding（含 Low，R9 除外）有具名回归测试文件。
- [ ] 汇总"接管的锁成员清单"（design §6 两张表：parsers 三副本成员 + writing-modules 四文件）
      写入任务 notes，供 typst-paper 与 cover-letter 子任务 rebase 时对照。
- [ ] 回报父任务：A-EN-2 的 SKILL.md 示例表述勘误（prd Notes）；确认 grammar/sentences/
      expression 已按裁决纳入落地，并声明 typst 侧 `.typ` 多文件装配顺带启用（供 A-TY-* 排重）。

## Phase 3.3 → 3.4 — spec 更新与提交（workflow.md 约定，全批次绿后才进入）

- [ ] Phase 3.3：如实现过程沉淀出可执行约定（如"第三套 writing-modules 锁的同步纪律"），
      走 `trellis-update-spec` 落 `.trellis/spec/`；无沉淀则记录"无"。
- [ ] Phase 3.4：将 G1–G6 六个拟提交分组（各自文件集 + message，见各批 Gate）**一次性呈报
      用户确认**；确认后按 G1→G6 顺序逐组 `git add <文件集> && git commit`。
- [ ] 提交前逐组核对：`git status` 中无分组外漂移文件；G3/G5 的 message 含默认行为变化双声明。
