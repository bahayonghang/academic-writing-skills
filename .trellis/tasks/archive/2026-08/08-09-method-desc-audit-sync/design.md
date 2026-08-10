# C3 技术设计：paper-audit 接线与集成验收

方案已定稿（规划期核实完毕，无 A/B 留白）：**委托 + 双调用 + 解析升级**。机制事实与行号
见父 research/repo-recon.md §2.1。

## 1. 双调用实现落点

- 位置：audit.py 组装检查任务处（:2465 附近）。logic 检查由一条 task 变两条：
  `("logic", script, ["--cross-section"])` 保持原样；对 fmt=.typ 或 lang=en 的文档追加
  `("logic", script, ["--section", "methods"])`。zh 文档不追加。
- 解析合并：两次输出各自过 `_parse_script_output("logic", ...)` 后串接；module 同为 LOGIC，
  下游（evaluate_from_audit、报告渲染）无需感知双调用。
- 并发：沿用现有 executor 提交方式，两条 task 天然并行。
- 声明限制：paper-audit 文档（SKILL.md 适当小节或 modules 说明）加一句"zh 学位论文的方法
  叙述检查经 latex-thesis-zh `--method-narrative` 显式选章执行，不进入 audit 自动链"。

## 2. 解析升级实现落点

- `_parse_script_output` 重构为块感知状态机：
  1) 结构化正则扩为 `(Critical|Major|Minor|Info)` 与 `(P[0123])`。
  2) 命中头行 → 开新 issue（现有 message 清洗逻辑保留）。
  3) 续行判定：`^%\s*(Current|Suggested|Rationale|Meaning-Check)\b`（及 typst `//` 前缀
     变体）→ 丢弃；空行 → 结块。
  4) 无任何头行的输出维持现状逐行兜底（兼容非结构化脚本）。
- Info 不扣分：核实 `scholar_eval.py` 扣分表对未知 severity 的现行为（recon 记录扣分表只列
  三级），在 `evaluate_from_audit` 入口或扣分函数处显式跳过 `severity == "Info"`，加注释
  说明语义（Info=候选提示，不代表缺陷）。
- 专项单测（新测试函数，置于现有 audit 测试文件）：
  a) 4 续行 finding → 1 issue，severity/priority 取头行值；
  b) Info/P3 头行 → severity=Info 且不改变 ScholarEval 分数；
  c) 裸行输出 → 现状兜底行为不变；
  d) 现有测试套逐条调整（计数/分数基线按新语义重算，注释写明"块感知解析修复，2026-08"）。

## 3. 报告层写法

- focus block：位置与格式对齐 `SUBAGENT_TEMPLATES.md:64-208` 五个 cross-cutting lane；
  DO/DON'T 条目=prd R3.1；标题用 "Methodological interface & argumentation completeness"。
- C5 增补：在 `critical_reviewer_agent.md:98-114` 节内加一小段（不新设编号），连接类型枚举
  在现有四型上增 interface / residual-constraint 两型；不触碰 `:27` DON'T 行。
- 语言红线自查：三处 markdown 完成后 grep 确认无 "writing quality|写作质量|叙述质量" 新增。

## 4. 集成验收执行设计（prd R5）

- 端到端 fixture：spec §9 反例合成 `.tex`（en）与 `.typ` 双版本（脱敏，素材源=父 research
  spec 原文 §9），另备 zh 版仅供三技能侧验证。产物与输出摘要存本任务 research/。
- 分差验证：同一 fixture 干净版/病例版走 audit 评分路径，断言分差来源仅 Minor 项。
- trigger evals 如需补例：Bash python 写入（JSON hook 陷阱）。

## 5. 风险与提交分组建议

- 风险 1：现有 audit 测试对 issue 计数/分数的基线断言数量未知 → 步骤 2 先跑全量测出受影响
  集合再逐条调整；若调整面超预期（>20 处断言），暂停并把影响面报用户裁决。
- 风险 2：`--section methods` 对某些 EN 文档节名（如 "Approach"）不命中 → 沿用现有
  `--section` 匹配语义，不扩词表；未命中即该文档无第二调用产出，属既有口径。
- 提交分组建议（Phase 3.4 由主会话执行，实施代理不 commit）：
  A 组＝解析升级 + 专项单测 + 现有测试调整（`fix(paper-audit): 块感知解析与 Info/P3 语义`）；
  B 组＝双调用 + 端到端 fixture（`feat(paper-audit): 方法节 logic 双调用`）；
  C 组＝报告层 markdown + manifest + 双语页（`docs(paper-audit): 方法论接口审阅指引`）。
