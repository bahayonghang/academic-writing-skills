# 执行计划：paper-audit 小节级审阅通道与窗口装配

前置：`.trellis/tasks/08-30-subsection-cursor-zh` 已完成并归档。本任务的用词、三码与协议句
以 zh 侧 `academic-writing-skills/latex-thesis-zh/references/writing/subsection-context-zh.md`
的契约块为准。

变更清单见 `prd.md`「变更清单」表；下面每个步骤对应表中的一到多行（TPR-09）。

## 步骤

### S1 读取 zh 侧已落地的契约（不改代码）

- 读 `academic-writing-skills/latex-thesis-zh/references/writing/subsection-context-zh.md`，
  取出 `<!-- S-CTX-CONTRACT:BEGIN -->` / `<!-- S-CTX-CONTRACT:END -->` 之间的整块。
- 读 zh 侧 `analyze_logic.py` 的 `_ctx_is_eligible` 与窗口构建，确认 canonical eligibility
  的实际数值。
- 读 `academic-writing-skills/paper-audit/scripts/tex_loader.py:167-171`，确认 `assemble()`
  返回对象的 origin map 字段名。

### S2 装配接入

- `prepare_review_workspace.py` 对 `.tex` 入口改用 `assemble()`；`.typ` / `.pdf` 走原路径。
- 既有 section 级流程的 content 来源保持不变。

验证：多文件 fixture 上 `extract_headings()` 返回非空（现状为 0）。

### S3 小节单元构建

- 实现 `build_subsection_units`：全量 `extract_headings()`、全文档 `root_level` 与编号计数器、
  `*` 标题跳过、**无 depth-3 不回退**、排除区过滤、origin map 映射为源坐标。
- 写 `artifacts/data/subsection_index.json`，`section_index.json` 增顶层
  `subsection_index_status`。

验证：新增 `tests/skills/paper_audit/test_subsection_index.py`，覆盖
多文件编号序列等于期望序列（AC-B-01）、无关键词标题被收录（AC-B-02）、
无 depth-3 降级（AC-B-03）、`.typ` / `.pdf` 降级（AC-B-04）、源坐标正确（AC-B-05）。

### S4 `WorkspaceLayout` 与窗口文件

- `paths.py` 的 `WorkspaceLayout`（**不是 `ReviewLayout`**，TPR-08）增 `subsection_index`、
  `windows_dir`、`window_file()`，并把 `windows_dir` 加入目录创建列表。
- 按父 `design.md` §2.4 写窗口 JSON；合格段用 canonical eligibility，数值取自 S1，
  不自行调整。

验证：窗口 JSON 不含正文原句（对文档任意 20 字连续片段做子串检查）；
部件数量按 `*_status` 断言，不断言固定数量（AC-B-06）。

### S5 lane 接入调度链

- `audit.py:224-264` `FOCUS_TO_ALLOWED_LANES["full"]` / `["logic"]` 加 `subsection_context_polish`。
- `audit.py:275-291` `ROLE_TO_REVIEW_LANES["logic"]` 加同名 lane。
- `_write_lane_outputs` 不加 fallback 生成器。
- polish 路径 `precheck_data` 增 `subsection_windows`（设计 §4.2）。

验证：新增 `tests/skills/paper_audit/test_subsection_lane_wiring.py`，
断言 focus 矩阵（AC-B-07）、polish state 键（AC-B-08）、
无 LLM 参与时不产出 `artifacts/comments/subsection_context_polish.json`（AC-B-09）。

### S6 mirror 协议文件

- 新增 `academic-writing-skills/paper-audit/references/SUBSECTION_CONTEXT_PROTOCOL.md`，
  契约块内容与 S1 取出的 zh 契约块规范化后完全相等。

### S7 lane / template / agent 文档

- `REVIEW_LANE_GUIDE.md` 增 `subsection_context_polish`（max 10 issues、职责边界、
  启用条件写明 `--mode polish` 与 `deep-review --focus logic|full`）。
- `SUBAGENT_TEMPLATES.md` 增 focus block：读 `artifacts/windows/<id>.json`，
  按源坐标 `Read(offset, limit)`；DO/DON'T；finding 必须带 `subsection_id` 与 `context_sides`。
- `agents/section_reviewer_agent.md` 增一段，**只写 mirror 文件路径**，不复制协议句。

三个文件均不含协议句正文（AC-B-10 的负向断言）。

### S8 POLISH_GUIDE 改造

- Context Window Management 段按设计 §6 改写；保留 1200 词语义；
  无小节层时回退既有章节切分（AC-B-11）。

### S9 ISSUE_SCHEMA

- 增 `subsection_id` 与 `context_sides`（列表）两个 optional 字段，Guidance 增一条，
  写明 `source_kind: "llm"` 与 severity 取值，required 列表不变（AC-B-12）。

验证：`uv run --extra dev python -m pytest tests/contracts/test_claim_evidence_contract.py`

### S10 SKILL.md 与 manifest

- `academic-writing-skills/paper-audit/SKILL.md` 增新 lane 的路由说明；
  只改 `last_updated`，**不改 `version`**。
- 用 Bash python 更新 `docs/resource-manifest.json` 中所有被改动 references 文件的
  `sourceSha256`，同步双语页面。

验证：
```bash
uv run --extra dev python -m pytest tests/contracts/test_skill_contracts.py tests/contracts/test_docs_bilingual_resources.py
```

### S11 契约测试

- 新增 `tests/contracts/test_subsection_context_contract.py`，五项断言见设计 §5（AC-B-13）。

### S12 跨技能集成验收（父 AC-P-03 / AC-P-04）

真实命令（TPR-08 更正：脚本参数是 `--output-dir`，不是 `--review-dir`；产物在
`{output-dir}/{slug}/artifacts/data/`）：

```bash
FIX=academic-writing-skills/latex-thesis-zh/evals/fixtures/subsection-context/main.tex

uv run --extra dev python academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py \
  "$FIX" --subsection-context > /tmp/zh_ctx.txt

uv run --extra dev python academic-writing-skills/paper-audit/scripts/prepare_review_workspace.py \
  "$FIX" --output-dir /tmp/review_out --overwrite
# 上一条打印 "WORKSPACE: /tmp/review_out/<slug>"，slug 由 slugify(title or stem) 得到

uv run --extra dev python - <<'PY'
import json, pathlib, re, sys
ws = next(pathlib.Path("/tmp/review_out").iterdir())
audit_ids = [u["subsection_id"] for u in
             json.loads((ws / "artifacts/data/subsection_index.json").read_text("utf-8"))["units"]]
zh_ids = re.findall(r"小节窗口 (\d+(?:\.\d+)+)", pathlib.Path("/tmp/zh_ctx.txt").read_text("utf-8"))
expected = ["2.1.1", "2.1.2", "2.1.3", "2.2.1"]   # 与 fixture 一起写死，S4(A) 产出
assert audit_ids == expected, audit_ids
assert zh_ids == expected, zh_ids
PY
```

期望序列常量由子任务 A 的 fixture 一并给出，两侧都断言等于它，
**不只断言两侧相等**（防止两个空集合互等而误通过）。

同一 fixture 上再断言窗口 `source_file` 指向 `chapters/*.tex`、行号为文件内行号（AC-P-04）。

### S13 只读边界行为核对（父 AC-P-07 / AC-B-15）

- 构造 bait fixture：在 `prev.tail`、`next.head`、`parent_lead` 中各放一个明显可改的表达问题。
- 跑一次 `subsection_context_polish` lane 与一次 polish Mentor 调用。
- 人工核对全部改写建议只锚定 `current`。
- 结论记入任务 notes，标注 **manual + UNVERIFIED**，不得用字符串契约测试代替。

### S14 全量校验

```bash
just fix
just ci
```

## 回滚点

回滚只在**不撤销任何 R** 的前提下允许在本执行计划内透明进行；任何会撤销或收窄一条 R 的
处置，必须停止并走父 `prd.md` 的「合同变更 gate」（TPR-09）。

| 触发 | 处置 | 是否需回父规划 |
| --- | --- | --- |
| S2 `assemble()` 在某类入口上抛错 | 该入口按 §1.4 降级为 `unsupported_format`，其余不变 | 否——R-B1 已含降级 |
| S4 窗口文件数量过大 | 只为 `--focus` 命中的 section 内单元生成窗口，索引仍全量 | 否——R-B2 不变 |
| S5 lane 加入 `FOCUS_TO_ALLOWED_LANES` 后打破既有 deep-review 测试 | 修正测试预期集合；lane 不得从常量中移除 | 否 |
| 需要把 lane 降级为「不自动启用的手工协议」 | **停止**，返回父任务同步修订父 R3/AC-P-08 与 B 的 R-B3/AC | 是 |
| 需要撤销 `subsection_index.json` 独立文件、改回塞进 `section_index.json` | **停止**，返回父任务同步修订 | 是 |
| 需要恢复 `S-CTX-DUP` 或改动三码 | **停止**，返回父任务（该码本轮已按 TPR-07 移除） | 是 |

## 完成定义

`prd.md` 的 AC-B-01 ~ AC-B-15 全部勾选完成，S12 的编号序列断言通过，
S13 的行为核对已执行并按 UNVERIFIED 记录，`just ci` 全绿。
