# Implement：latex-thesis-zh 正文方法+实验章优化

执行顺序即 commit 顺序，每步末验证；R2/R3/R4 涉及默认行为变化的步骤须更新存量单测并在 commit message 声明。开工前置：确认 07-11 任务分支状态（`analyze_logic.py` 有交叠），必要时先 rebase。

## Step 0：前置与 fixture 准备

- [ ] `git log --oneline -5` + `python .trellis/scripts/task.py list` 确认 07-11 成果已在当前分支（`--process-chapter`、F-MD/F-NOTE 存在）。
- [ ] 造合成 fixture（`tests/` 下，领域内容脱敏替换，问题模式对齐 prd 错误示范表 P1~P3/P5~P10 + E-* 正负例）：
  - 装配样本（1 个多章 .tex）：规范方法章负例（防误报红线 12 条情形全覆盖）+ 问题方法章正例 + 过程分析章边界例。
  - 单章样本：编号引言节形态、中文图名 includegraphics、占位表格行。
- 验证：fixture 能被现有脚本解析不报错（`PYTHONIOENCODING=utf-8 python analyze_logic.py <fixture>`）。

## Step 1：R2 误报五连修（commit: `fix(latex-thesis-zh): 修复正文方法章五类检查误报`）

- [ ] R2a `_check_heading_leads` 编号引言节适配（抽 `NUMBERED_INTRO_SEC_RE` 公共常量，与 `_check_chapter_intro` 共用）。
- [ ] R2b `mixed_punctuation` 剥离 `\includegraphics/\input` 参数（design D6 二选一策略）。
- [ ] R2c `oral_vague` "特别" 负向断言。
- [ ] R2d `_needs_method_justification_zh` 定义句式负向条件。
- [ ] R2e `_check_process_chapter` 双信号章式预判（design D5）。
- [ ] 每项：precision 测试追加正例（原误报样本不再报）+ 负例（原真阳保留）；更新受影响存量断言。
- 验证：`uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/ -x` 绿；fixture 单章样本上 P5/P7/P8/P9/P10 全部消除、真阳保留。

## Step 2：R3 拼接感+草稿态（commit: `feat(latex-thesis-zh): 拼接表述默认全章检查与草稿态识别`）

- [ ] R3a P-PAPER 抽出为 `_check_paper_stitching`，默认管线全章全量报告；从 `_check_process_chapter` 移除防双报；迁移 07-11 存量 P-PAPER 单测（--process-chapter → 默认；首处 → 全量）。
- [ ] R3b F-NOTE 增 `DRAFT_NOTE_HEDGE` 词表组（design D2 护栏：`复算` 负向断言双向锁定）。
- [ ] R3c 新增 `F-PLACEHOLDER` 规则（≥2 空占位单元格；仅表体行）。
- [ ] R3d `_check_thesis_vs_chapter` 保守词面版；若合成负例误报 >0 → 执行预设降级（撤脚本、归 R1⑧ 指南清单），在 commit message 记录。
- 验证：pytest 绿；装配 fixture 上 P-PAPER 多处全报、HEDGE 词命中、占位行命中；规范负例零误报。

## Step 3：R4 实验逐章检查（commit: `feat(latex-thesis-zh): analyze_experiment 逐方法章检查与结构提示`）

- [ ] R4a 默认模式无 `discussion` 节时输出结构提示 Info（更新 analyze_experiment 存量单测：假绿用例改断言提示存在）。
- [ ] R4b `--per-chapter`：章切分 + EXP_SEC_RE/METHOD_SEC_RE 定位 + E-DATA/E-ATTR/E-REF/E-FIG/E-METRIC/E-PARAM/E-ABL/E-ECHO（severity 按 design D3 表）。
- [ ] R4c `analyze_logic.py --first-chapter N`（缺省行为不变）。
- [ ] 新增 `tests/skills/latex_thesis_zh/test_body_chapters.py`：E-* 每项 ≥1 正例 + 1 负例（负例覆盖防误报红线：无显著性检验不报、人工基线不报、教科书节不触发 E-FIG、并列章 E-ECHO 只 Info）。
- 验证：pytest 绿；装配 fixture `--per-chapter` 逐章产出且行号正确；`--first-chapter 3` 下单章缺承上可检出/已写承上不误报。

## Step 4：R1+R5 指南与口径（commit: `docs(latex-thesis-zh): 方法章专章指南与承上口径修正`）

- [ ] 新建 `references/writing/method-chapter-guide-zh.md`（design §3 十节结构 + 脚本映射表；素材：research/body-chapter-conventions.md + web-best-practices.md，阈值全部注明出处）。
- [ ] thesis-writing-guide.md：方法章节加新指南指针（与 process-chapter 指针同型）；"承上启下两段式"改标推荐形态 + 弹性口径三条（并列可不承上/角色复用句/方法路线预告）。
- [ ] `_check_chapter_intro` 缺承上分级与文案（design D8）+ 对应单测。
- [ ] 自查：新指南与 process-chapter-guide-zh.md / introduction-guide-zh.md 无口径矛盾（grep 交叉关键词）。
- 验证：pytest 绿；`just lint` 绿。

## Step 5：R6 路由+evals+收尾（commit: `chore(latex-thesis-zh): 方法章路由触发词与 evals 用例`）

- [ ] SKILL.md `logic`/`experiment`/`format` 行 Use when 触发词 + Reference Map 指针行（注意 formatter 表格对齐陷阱）；只改 last_updated 不 bump version。
- [ ] modules/{logic,experiment,format,routing-rules}.md 更新（design §1 对应项）。
- [ ] evals.json 追加 ≥3 用例（方法章诊断正例 / 过程分析章边界例 / 实验逐章用例）——**走 Bash python 写入**（JSON hook 陷阱）。
- [ ] 用户论文只读复测（人工验收，不进 CI）：chapter3~6 逐项对照 prd 验收标准第 2 条。
- 验证：`just ci` 全绿（lint + pyright errors=0 + 全量 tests + contracts）。

## Step 6：Phase 3 收尾

- [ ] trellis-check 全量核查 → 视需要 trellis-update-spec（若沉淀出新约定：如"检查器默认行为变化三例外"模式）。
- [ ] 按 5 个 commit 切分提交（git-commit skill，中文 Conventional Commits）；更新 memory 索引。

## 回滚点

每个 Step 独立 commit 即回滚单元；Step 2 的 R3d 有预设降级路径（不算返工）；Step 3 若 E-* 误报率在真实样本上不可接受，可整体保留在 `--per-chapter` 后不动默认行为（R4a 提示除外）。
