# implement.md — 执行计划（07-11-thesis-zh-process-chapter）

> 前置：实现前**必读** `research/chapter2-conventions.md` 与 `research/chapter2-content-analysis.md`——后者 §7 是 P-FRAME 放宽判据与第 2 章引言特判的依据（3/5 范文框架节不写章号；第二章引言为概述式不承上），实现不得回退到"强制章号映射/强制承上"的旧设想。

## 顺序清单

### 阶段 ① R2 章引言形态适配（默认行为 bug-fix）

- [x] 1.1 `analyze_logic.py`：`_check_chapter_intro` 增加"编号引言节"识别与取文逻辑（design.md ①）；新常量 `INTRO_SECTION_TITLES_ZH`、`CHAPTER_INTRO_NUMBERED_MAX_CHARS`（依 research 内容分析校准，缺省 1600）。
- [x] 1.2 tests：新增/扩展 `test_chapter_intro_forms.py`——编号形态正/反（缺承上、超篇幅）、章后导语回归、章标题"引言"豁免不受影响。
- [x] 1.3 验证：`uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/ -k "chapter_intro or intro_mainline" -q` 全绿。
- [x] 1.4 Commit ①：`fix(latex-thesis-zh): 章引言检查适配编号引言节形态`（声明默认行为变化：消除 2.1 引言形态误报）。

### 阶段 ② R3 `--process-chapter` 主线检查

- [x] 2.1 `analyze_logic.py`：新 flag、目标章定位（默认章号 2 / `--section` 覆盖）、章式预判、节分类启发式、P-FLOW / P-DERIVE / P-FRAME / P-ORDER / P-PAPER（design.md ②；正则常量集中定义便于测试）。
- [x] 2.2 tests：`test_process_chapter.py` 合成脱敏 fixture（正例章+病例章+方法章式负例），覆盖各检查一正一反、漏章点名、`--section` 覆盖、多文件定位。
- [x] 2.3 验证：`uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/test_process_chapter.py -q` 全绿。**本轮范围=技能能力建设，不对用户论文出诊断报告**（用户决策）；如需自检脚本行为，仅在合成 fixture 上跑，不 navigate 用户 `thesis/chapters/*.tex`。
- [x] 2.4 Commit ②：`feat(latex-thesis-zh): logic 新增 --process-chapter 过程分析章主线检查`。

### 阶段 ③ R5 format 源码卫生

- [x] 3.1 `check_format.py`：F-MD（Markdown 加粗残留）、F-NOTE（草稿备注保守词表）（design.md ③）。
- [x] 3.2 tests：一正一反用例（`**bold**` 命中；`\*\*` 与"仍需实验确认"不命中）；如现有 format 测试锁输出条数，同步更新。
- [x] 3.3 验证：`uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/ -k format -q` 全绿。
- [x] 3.4 Commit ③：`feat(latex-thesis-zh): format 新增 Markdown 残留与草稿备注检查`。

### 阶段 ④ R1 + R4 references 文档

- [x] 4.1 新建 `references/writing/process-chapter-guide-zh.md`（PRD R1 ①~⑩；正反例句取 research/ 两文件已注页码的原句；阈值注出处）。
- [x] 4.2 修 `references/writing/structure-guide.md` 双轨定位 + 直属节弹性口径；修 `references/writing/thesis-writing-guide.md` 指针行。
- [x] 4.3 `references/modules/logic.md` 增 `--process-chapter` 检查表；`references/modules/format.md` 增 F-MD/F-NOTE；`references/modules/routing-rules.md` 增判据条目。
- [x] 4.4 验证：`grep -rn "第二章：相关工作" academic-writing-skills/latex-thesis-zh/` 无残留；文档内命令可直接复制执行。
- [x] 4.5 Commit ④：`docs(latex-thesis-zh): 新增第二章过程分析章指南并修正结构指南双轨定位`。

### 阶段 ⑤ R6 SKILL.md + evals

- [x] 5.1 SKILL.md：logic 行 Use when 追加触发词；Reference Map 加新指南行；last_updated=2026-07-11（version 不动）。
- [x] 5.2 evals.json 追加 2 条路由用例（**Bash python 写入**，禁 Edit/Write 直改）。
- [x] 5.3 验证：`uv run --extra dev python -m pytest tests/contracts/ tests/skills/latex_thesis_zh/ -q` 全绿。
- [x] 5.4 Commit ⑤：`test(latex-thesis-zh): evals 追加过程分析章路由用例并更新 SKILL 指针`。

### 阶段 ⑥ 收尾门

- [x] 6.1 全量 `just ci` 绿（lint + pyright errors=0 + 全部 tests）。
- [x] 6.2 对照 prd.md Acceptance Criteria 逐条勾验。
- [x] 6.3 确认 `ref/thesis/decrypted/` 未入 git 跟踪（必要时补 .gitignore 条目，单独 chore commit）。

## 回滚点

每阶段独立 commit（design.md"兼容与回滚"），任一阶段验证不过可单独 revert 不影响其余；阶段 ① 与 ② 共享 analyze_logic.py，revert ① 前需确认 ② 未依赖其新常量。

## 复核门（review gates）

- 阶段 ② 完成后：人工复核合成 fixture 正/负例每条诊断是否符合 research 证据表（防启发式过拟合合成样本）；本轮不跑用户论文。
- 阶段 ④ 完成后：人工通读新指南，确认所有原句引用注明页码、无编造论文内容（红线 #2）。
