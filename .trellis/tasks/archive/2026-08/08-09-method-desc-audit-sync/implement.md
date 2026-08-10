# C3 执行计划

前置依赖：C1、C2 归档（MN_ 常量定稿、契约测试在位）。读父 research/ 三文件。实施代理不执行
git commit。

## 步骤

### 1. 解析升级（先行，独立可回归）

- [x] `_parse_script_output` 块感知重构 + Info/P3 识别（design §2）。
- [x] Info 不扣分接点实现（核实 scholar_eval 现行为后选点，选择理由写注释）。
- [x] 专项单测 a-c + 全量跑出受影响的现有断言集合，逐条调整并注释（超 20 处即暂停报用户）。
- 验证：`uv run --extra dev python -m pytest tests/skills/paper_audit/ tests/contracts/`。
- 审查门：diff 审查（兜底路径不变、Info 语义单点实现、调整注释齐全）。

### 2. 双调用

- [x] audit.py logic 任务追加 `--section methods` 第二调用（en/typst；zh 不加）（design §1）。
- [x] zh 边界声明写入 paper-audit 文档。
- [x] 端到端 fixture（.tex/.typ 病例+干净版）：病例出 M-* issue、干净版无新增、
      cross-section 等全文检查无回归、soundness 分差仅来自 Minor。
- 验证：`uv run --extra dev python -m pytest tests/skills/paper_audit/`。

### 3. 报告层三处 markdown

- [x] focus block / C5 增补 / DEEP_REVIEW_CRITERIA + REVIEW_LANE_GUIDE 各一句（design §3）。
- [x] 措辞红线自查（grep 无"写作质量/叙述质量/writing quality"新增）。
- 验证：`uv run --extra dev python -m pytest tests/skills/paper_audit/`（字符串锁）。

### 4. 双语契约全链（paper-audit 公开资源）

- [x] `check_resource_sync.py --write-manifest`（本任务全部 references/agents 改动入册）。
- [x] docs/ 英文页与源一致 + docs/zh 完整中文译文（每个改动文件的页对）。
- 验证：`uv run python docs/scripts/check_resource_sync.py --skill paper-audit`；
  `uv run --extra dev python -m pytest tests/contracts/test_docs_bilingual_resources.py`。

### 5. 跨子集成验收（父 implement.md §2）

- [x] 契约测试绿；红线负例三条核对；端到端输出摘要存 research/；评分链四断言核对。
- [x] 全仓 `just ci`；四技能 `check_resource_sync.py --skill`；全量
      `check_resource_sync.py`；`just doc-build`。
- [x] trigger evals 核对完成；本任务不改变 skill trigger，故无需补例。
- [x] hypothesis 结论已定稿：合成 fixture 支持候选检查行为，真实论文语料的查准率与召回率
      保持 `UNVERIFIED`；证据见 `research/integration-evidence.md`，并纳入父任务 journal。

### 6. 收口

- [x] prd 与父 prd 验收标准逐项核对；trellis-check 全范围 → 3.3 spec 更新 → 3.4 提交
      （分组建议见 design §5）→ 父任务归档条件核对。

## 提交分组建议（仅 Phase 3.4 使用）

- A 组：步骤 1（解析升级 + 测试调整）。
- B 组：步骤 2（双调用 + fixture）。
- C 组：步骤 3-4（报告层 + manifest + 双语页）。
