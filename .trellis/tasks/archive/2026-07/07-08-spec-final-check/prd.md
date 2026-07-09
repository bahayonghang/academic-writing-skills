# 通用规范逐项终检机制与燕山2024清单

## Goal

定义一套**通用的「逐项检查清单」格式**（放在 `templates/*.md` 内，机器可解析），
新增终检脚本 `check_spec.py` 逐项执行可自动化条目，并把 `templates/yanshan.md`
从"获取指引"重写为《燕山大学研究生学位论文撰写规范（2024版）》的完整快照 + 全量检查清单，
使用户在定稿时能"对照规范文件逐项检查"。

## Requirements

1. **清单格式（通用契约）**：每个 `templates/*.md` 可含一个 `## 逐项检查清单` 段，
   表格列固定为 `ID | 检查项 | 规范依据 | 检查方式 | 适用`：
   - `ID`：学校前缀 + 序号（如 `YS-01`），全文件唯一；
   - `规范依据`：规范原文章节号（如 `§1.3.2`）；
   - `检查方式` ∈ `script:<checker>`（check_spec.py 内建检查器）/ `module:<router-module>`
     （提示走既有模块，如 `module:tables`）/ `llm`（agent 逐项判读正文）/ `manual`
     （需编译 PDF 或打印核对，列给用户自查）；
   - `适用` ∈ `通用` / `硕士` / `博士`。
2. **check_spec.py**：
   - CLI：`check_spec.py main.tex --template yanshan --degree master|doctor [--bib refs.bib] [--spec-file 自定义.md] [--json]`；
   - 解析清单 → 逐项执行 `script:` 检查器 → 输出逐项报告：每条
     `ID / 检查项 / 状态(PASS|FAIL|NEEDS-LLM|MANUAL|SKIP) / 证据（数值、文件:行号）`；
   - `--spec-file` 允许传任意符合格式的清单文件（通用性核心：任何学校规范都能整理成清单后接入）；
     清单中 `script:` 引用了不存在的检查器时降级为 NEEDS-LLM 并提示，不报错中断；
   - 不重复实现既有模块已覆盖的检查（表格/交叉引用/GB7714 等），对应条目用 `module:` 引到既有命令。
3. **yanshan.md 重写**：以 `../../../.trellis/tasks/07-08-spec-check-blind-review/research/yanshan-2024-spec-extracted.txt`
   为唯一事实来源，收录 2024 版关键规范事实（内容要求 / 书写要求 / 排版打印要求三章）+
   全量 `## 逐项检查清单`（每条带 § 依据），保留现有"学术不端检测"节；预留 `## 盲审` 节位
   （内容由 07-08-blind-review 子任务填充）。
4. **SKILL.md**：Module Router 增加 `spec-check` 行 + 路由规则（触发词：对照规范逐项检查/终检/
   定稿检查/规范符合性/格式自查）+ Example Request 一条；`references/modules/spec-check.md`
   写明五步工作流（识别模板 → 载清单 → 跑脚本 → LLM 逐项处理 NEEDS-LLM → 汇总逐项报告，
   manual 项列给用户）。
5. **对齐锁**：新增契约测试锁定「清单 md ↔ 脚本注册表」一致性（见 design.md §5）。

## Acceptance Criteria

- [ ] `templates/yanshan.md` 清单条目 ≥ 40 条，覆盖规范三大章；每条 `规范依据` 都能在
      research 提取文本中找到对应章节（抽查核验）；无编造条目。
- [ ] 对 `evals/fixtures/thesis-project/main.tex` 跑
      `uv run python .../check_spec.py main.tex --template yanshan --degree doctor`
      退出码语义正确，输出含全部清单条目的逐项状态；`--json` 可解析。
- [ ] fixture 至少能触发 3 个 FAIL（预埋违规：如关键词数量、结论超字数、标题超 15 字之一）
      与多数 PASS/NEEDS-LLM，证明检查器真的在判定（fixture 埋点须与断言联动，参见既有
      fixture 工程约定）。
- [ ] `--spec-file` 用一个最小自定义清单（测试 fixture）跑通，未知检查器正确降级 NEEDS-LLM。
- [ ] 新契约测试：yanshan.md 清单可解析、ID 唯一、检查方式枚举合法、`script:` 检查器
      与 check_spec.py 注册表双向一致、`module:` 名与 SKILL.md 路由表模块名一致。
- [ ] `tests/contracts/test_skill_contracts.py`（ROUTER_ROW_RE）与 trigger evals 通过；
      `just ci` 全绿。
- [ ] SKILL.md 只改 `last_updated`，`version` 不动。

## Constraints

- 检查器只做源文本可静态判定的事：字数/数量/存在性/顺序/导言区配置；版式渲染类一律 `manual`。
- 字数统计口径（含图表 vs 纯文字）在报告中说明为近似值，阈值判定留缓冲带（见 design.md §3）。
- 不动 `\cite`/`\ref`/`\label`/数学环境；检查只读不写。
