# implement — thu-pku-generic 模板检查清单扩充

> 2026-07-09 修订：research 步骤已完成（research/ 下 5 个文件），并依研究结论
> 增补步骤 2（有据事实修正）、细化步骤 5（检查器窄幅参数化）与步骤 7（unknown-template 测试更新）。

## 步骤

1. ~~**research**~~ **已完成**：`research/` 含 thuthesis-manual-facts / tsinghua-grad-spec /
   pku-grad-spec / gbt7713-generic-items / missing-evidence 五文件，逐条带来源。
   实现中**每条清单条目、每个阈值、每处事实修正都必须能指到其中的来源行**；
   research/ 未覆盖的条目不写（或降级 generic 惯例项并标注"以本校规范为准"）。
2. **有据事实修正（PRD Req.5，仅三处）**：
   - thuthesis.md 图表/公式编号：现行默认点号"图 2.1"，连字符与点号均合规（v7.7.1 手册）；
   - pkuthss.md 符号说明章节：强制改条件式（官方原文措辞）；
   - generic.md GB/T 7713.1 版本注记（2006 废止 → 2025 版 2026-02-01 实施）。
   → verify: 每处 diff 对应 research/ 出处；`test_venue_templates_layout.py` 字符串断言仍在。
3. **generic.md 加 `## 逐项检查清单`**（GEN-xx：国标有据项 script 化——kw_count 3~8、
   title_len、heading_depth、appendix_letter 等；图表按章编号、罗马页码、每章另起页、
   本章小结等校级惯例项标注"以本校规范为准"且多为 llm/manual；字数类不设阈值只报数）
   → verify: `check_spec.py <fixture>/main.tex --template generic --degree master` 清单加载执行成功。
4. **thuthesis.md / pkuthss.md 加清单**（THU-xx / PKU-xx：文件头加"事实核查日期 2026-07-09 + 来源"；
   官方量化项——清华题名≤25/摘要800–1000限一页/关键词≤5/致谢限一页/目录至二级，
   北大题名≤20/博士摘要800–1000/硕士摘要600左右/关键词3~5逗号/致谢≤1000字——按 PRD 参数化
   边界决定 script/llm；**负面证据红线**：两校均无正文/绪论/结论字数、文献量、近五年占比规定，
   wordcount/intro_len/conclusion_len/bib_count/bib_recency 一律不写 script、不套燕山值；
   模板特有事实项 module:/manual，如 pkuthss ugly 选项、默认 biblatex 样式偏离校规、\makeblind）
   → verify: 分别跑 check_spec.py；`tests/contracts/test_spec_checklists.py` 全绿。
5. **TEMPLATE_THRESHOLDS 增补 + 检查器窄幅参数化**（仅 PRD 允许的范围）：
   - 有据阈值：THU 摘要 (800,1000)（硕博同）；PKU 博士摘要 (800,1000)；PKU 题名 20、
     关键词 (3,5)+逗号分隔等——具体键形取实现时最小方案；
   - 既有 checker 读新键须带缺省值=现行硬编码行为；禁止新增 checker 函数；
   - "600左右"/"≤5 无下限"等不可界定区间的项落 llm 并逐字引用原文。
   → verify: yanshan fixture `check_spec.py --template yanshan --degree doctor --year 2026`
   输出与改动前一致（改前先存基线）；新阈值有对应测试用例。
6. **detect_template 回归**：改动前后各跑
   `uv run python academic-writing-skills/latex-thesis-zh/scripts/detect_template.py <fixture>/main.tex --json`，
   diff 仅含步骤 2 的有据修正条目 → verify: 手工对比 + 在 test 侧补一条
   "`## 逐项检查清单` 节内容不进入 key_requirements" 的断言。
7. **既有测试更新**：`test_check_spec.py::test_unknown_template_exits_2_with_hint` 现以
   thuthesis 充当未知模板（清单落地后不再 exit 2）——改用真正不存在的模板名，断言语义不变。
   → verify: 该测试绿。
8. **全量回归** → verify: `just ci` 全绿（基线 1000 过）。

## 回滚点

- 每个模板文件的清单独立成 commit-able 单元；任一清单证据不足即整节撤下（不留半截表格，
  避免契约测试半红）。
- 检查器参数化独立可回退：若参数化引入 yanshan 回归，回退参数化、相应条目降级 llm。

## 审查门

- 清单零编造：每条能指到 research/ 来源行或模板文档；"常见惯例"类措辞只允许出现在
  generic.md 并带"以本校规范为准"限定。
- 负面证据同样是证据：研究确认"无此规定"的条目出现在 THU-/PKU- 清单即为违规。
