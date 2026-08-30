# Implement — zh 检查调度修复与专属检查器接通

前置：读 `prd.md` 与 `design.md`。改动集中在 `academic-writing-skills/paper-audit/scripts/audit.py`、`scripts/scholar_eval.py` 与 `tests/`。

## 命令约定（TPR-12）

本仓库的验证命令统一用下列形式，PowerShell 与 POSIX shell 均可直接执行。**不要用 `tail`、`head`、heredoc（`python - <<'PY'`）**——PowerShell 下不可用。

```
uv run --extra dev python -m pytest tests/skills/paper_audit/ -q
uv run --extra dev python -m pytest tests/skills/paper_audit/test_paper_audit.py::TestModeChecks -q
just ci
git diff --stat -- academic-writing-skills/latex-thesis-zh academic-writing-skills/latex-paper-en
```

需要读取长输出时写进文件再看：`just ci > ci.log 2>&1`，然后用 Read 工具打开 `ci.log`。
需要临时脚本时写成 `.py` 文件用 `uv run --extra dev python <file>` 执行，或用 `python -c "..."` 单行形式。

## 基线记录（开工第一步）

```
just ci > ci-baseline.log 2>&1
git rev-parse --short HEAD
```

把测试数与 HEAD 写回本文件"验收记录"。父 PRD 的 AC7 以此为准。

## 阶段 A — bib 输入修复（AC1-1 / AC1-2 / AC1-3）

**A1** 抽出 `_resolve_bibliography_paths(path, content, fmt) -> list[Path]`，由 `audit.py:62`-`:95` 现有逻辑原样迁移（去掉 `_read_source` 那一步）。改 `_load_bibliography_content` 调用它，签名与返回值不变（`test_literature_search.py:484`-`:499` 依赖）。

**A2** 在 `run_audit` 的 tasks 构造处（`audit.py:2486`-`:2511` 区间）为 `bib` 检查改传 `.bib` 路径：解析出 1 个直接传；多个则逐个生成 task 并合并 findings；0 个则打印显式 SKIP 行，不发起调用。

**A3** `fmt == ".tex"` 且（`lang == "zh"` 或 `venue == "thesis-zh"`）时为 `bib` 追加 `--standard gb7714`。**`.typ` 不追加**——`typst-paper/scripts/verify_bib.py` 只有 `--style`，传 `--standard` 会以退出码 2 失败（design §4）。

**A4** 从 `ZH_EXTRA_CHECKS`（`audit.py:301`）移除 `gbt7714`。

**校验**
```
uv run --extra dev python -m pytest tests/skills/paper_audit/test_literature_search.py -q
uv run --extra dev python -m pytest tests/skills/paper_audit/ -q
```
EN 侧若有测试因 `bib` 首次产出真实 finding 而失败，更新期望值（父 PRD Notes 记为预期结果）。不加条件分支回避。

**提交点 1**：`fix(paper-audit): 🐛 修复 bib 检查输入路径与 GB/T 7714 调度`

## 阶段 B — 解析显式化与语言覆盖（AC2-1 / AC2-2 / AC2-3）

**B1** 新增 `LANG_SCRIPT_OVERRIDES`、`LANG_NEUTRAL_REUSE`、`ZH_ONLY_TEX_CHECKS`（design §2）。注意覆盖表的键：`sentences` → `check_style_zh.py`，`grammar` → `None`，`pseudocode` → `None`。**不要把替换挂在 `grammar` 上**（design §0 推论 2）。

**B2** 在 `_resolve_script`（`audit.py:379`）内接入覆盖表：`.typ` 直接走现有 typst 分支不参与覆盖；覆盖值为脚本名则在 `SCRIPTS_ZH` 下解析；覆盖值为 `None` 返回 `None`。

**B3** 新增 `ScriptResolution`、`_classify_resolution`、`_resolve_check`（design §3）。`_resolve_check` 内部调 `_resolve_script`，保证 monkeypatch 仍生效。

**B4** 生产代码改调 `_resolve_check`，按 design §3 的六种 reason 输出日志。

**B5** `.pdf` 跳过清单（`audit.py:2492` 附近）加入 `ZH_ONLY_TEX_CHECKS` 全部成员。

**校验**
```
uv run --extra dev python -m pytest tests/skills/paper_audit/test_method_narrative_audit_integration.py -q
```
这四处（`:29`、`:42`、`:49`、`:75`）直接调用 `_resolve_script`，`:49` monkeypatch 它。**必须全绿**——若红，说明 B3 的包装层次错了，回 design §3 重看，不要改测试。

**B6** 新增 `tests/skills/paper_audit/test_zh_script_resolution.py` —— **可达性矩阵测试**（AC2-1）。维度是 `入口 × lang × fmt × 检查键`，入口取 design §0 的 E1–E4 四条。

| 入口 | 测试方式 |
|---|---|
| E1 `main→run_audit` | 直接调 `run_audit(mode=...)`，断言 `_resolve_check` 的结果集 |
| E2 `run_audit:2441→run_deep_review→run_audit` | 断言 Phase 0 实际收到的 mode 是 `quick-audit`（记录现状，不修改） |
| E3 `run_reaudit→run_audit` | 同 E2 |
| E4 `run_audit:2431→run_polish_precheck` | **专项断言**：`lang="zh"` 时 `_resolve_script("sentences", "zh", ".tex")` 指向 `check_style_zh.py`（AC2-2 的 polish 不回归证据） |

逐单元期望值取 design §1 判定表与 §2 格式规则。zh/.tex 的四项固定为：`grammar` = suppressed、`sentences` = override→`check_style_zh.py`、`figures` = lang-neutral-reuse、`pseudocode` = suppressed。

**B7** 日志四态断言（AC2-3）：`lang-neutral-reuse` / `override` / `suppressed` / `missing` 各一条。

**提交点 2**：`refactor(paper-audit): ♻️ 显式化检查脚本解析归属与语言覆盖`

## 阶段 C — adapter registry 与检查器接通（AC3-1 ~ AC3-4 / AC4-1 / AC4-2）

**C1** `script_map`（`audit.py:381`）新增 6 键（design §5 表）。

**C2** `ZH_EXTRA_CHECKS` **保持 `list[str]`**，扩为 `["consistency", "spec", "blind", "abstract", "conclusion", "literature", "tables"]`（design §6）。`audit.py:2476`-`:2477` 不改。

> 不要改成 `dict[str, list[str]]`。`tests/skills/paper_audit/test_paper_audit.py:419`-`:422` 的 `test_zh_extra_checks` 断言 `"consistency" in ZH_EXTRA_CHECKS`，改 dict 后变成查键会直接红（TPR-11）。补一条 `"gbt7714" not in ZH_EXTRA_CHECKS` 断言（AC7）。

**C3** 建 adapter registry（design §5）。每个脚本一个具名 adapter，登记实测 CLI、输出协议与字段路径。**不共用通用 JSON 解码器**，**不用"优先 JSON 否则文本"的猜测式解析**。

关键实测值，直接用，不要重新假设：
- 有 `--json`：`check_spec.py`、`analyze_abstract.py`、`analyze_conclusion.py`、`check_tables.py`、`check_style_zh.py`
- **没有 `--json`**：`blind_review.py`、`latex-thesis-zh/scripts/analyze_literature.py` → 各写专用文本 adapter。`blind_review.py` 的输出是 Markdown 标题 + `[HIGH]` / `[P0]`，与审计器既有 `[Severity: ...][Priority: ...]` 协议不同。

**C4** 只读边界：`blind` 传 `--check`，按可用元数据可选传 `--author` / `--supervisor`，**绝不传 `--generate`**（`blind_review.py:794` 是写回分支）。

**C5** 退出码语义收紧（design §9.1）：非零退出且无可解析输出一律生成错误项，不打印 `clean`。

**C6** `scholar_eval.MODULE_DIMENSION_MAP` 增 6 键（design §9.2），**同步更新 `tests/skills/paper_audit/test_literature_search.py:578` 的精确相等断言**，并在 `.trellis/spec/academic-writing-skills/paper-audit-boundary-contracts.md:53` 的错误矩阵补一行。

**C7** `gateEligible` 规则（design §7）：gate 的 zh 阻断候选集只含 `spec` 与 `blind`。

**C8** 测试：
- 每个 adapter 五类回归（AC3-1）：真实样例、未知参数（argparse 退出码 2）、非零退出、空输出、非法 JSON。
- 非零退出不报 clean（AC3-3）。
- `MODULE_DIMENSION_MAP` 相等锁已更新 + fail-closed 测试（AC3-4）。
- `blind_review.py` 参数不含 `--generate`；只读运行前后 fixture sha256 与 mtime 不变（AC4-1）。
- gate 的 zh 阻断候选集不含 `consistency`、不含可选章节存在性检查（AC4-2）。

**校验**
```
uv run --extra dev python -m pytest tests/skills/paper_audit/ -q
git diff --stat -- academic-writing-skills/latex-thesis-zh academic-writing-skills/latex-paper-en
```
第二条必须无输出（AC6）。

**提交点 3**：`feat(paper-audit): ✨ 接通中文学位论文专属检查器`

## Fixture manifest（TPR-08，AC8 的可复现基础）

**不用单一 fixture 承担全部断言。** 建三个最小 fixture，逐缺陷登记。放在 `tests/fixtures/paper_audit/zh_thesis/`。

### F1 `zh_thesis_defects.tex` + `zh_thesis_defects.bib`（正例）

| # | 嵌入片段（精确内容） | 目标脚本 | 预期 module | 预期 severity | gate 状态 | 适用 fmt |
|---|---|---|---|---|---|---|
| D1 | `.bib` 中一条缺 `publisher` 与 `address` 的 `@book` 条目 | `verify_bib.py --standard gb7714` | `BIB` | 按脚本产出 | 非阻断 | `.tex` |
| D2 | 正文含作者真实姓名与导师姓名 | `blind_review.py --check` | `BLIND` | 按脚本产出 | **阻断** | `.tex` |
| D3 | 缺一项 `check_spec.py` 判定为必需的规范项 | `check_spec.py --json` | `SPEC` | 按脚本产出 | **阻断** | `.tex` |
| D4 | 一句超过 80 字符且含 `COLLOQ_MAP` 口语词 | `check_style_zh.py --json` | `SENTENCES` | 按脚本产出 | 非阻断 | `.tex` |
| D5 | 摘要缺英文摘要 | `analyze_abstract.py --json` | `ABSTRACT` | 按脚本产出 | 非阻断 | `.tex` |
| D6 | 一张非三线表 | `check_tables.py --json` | `TABLES` | 按脚本产出 | 非阻断 | `.tex` |

每行的"预期 severity"在实现时由该脚本的真实输出填定，不预设；填定后写进测试常量。

### F2 `zh_thesis_clean.tex` + `zh_thesis_clean.bib`（负例）

D1–D6 对应的六处全部合规。断言：这六个 module 均无 finding。用于区分"fixture 缺陷"与"检测缺陷"。

### F3 `zh_thesis_optional_absent.tex`（负例，TPR-03 专用）

无附录、无符号表，其余合规。断言：`--mode gate --venue thesis-zh` **不因此 FAIL**——可选章节不得进阻断集。

### 格式负例

- `zh_thesis_defects.typ`：断言 `ZH_ONLY_TEX_CHECKS` 全部 reason = `format-exempt`，且 `bib` 不带 `--standard`。
- 用 F1 的 PDF 导出（或桩）断言 `ZH_ONLY_TEX_CHECKS` 全部 reason = `format-skipped`。

### 入口断言

四条真实入口（design §0 的 E1–E4）各有结构化断言，不做整份报告文本快照——文本快照对无关改动脆弱。断言对象是 `AuditIssue` 列表中的 `(module, severity, gate_blocker)` 三元组集合。

## 阶段 D — 收尾

```
just fix
just ci > ci-final.log 2>&1
```

`pyright` 是 `basic` 模式，`reportOptionalOperand` 等仍是 error 会卡 `just ci`——看 error 数不是 warning 数。新增的 `Path | None` 与 `dict.get` 返回值要显式收窄。

## 陷阱清单

| 陷阱 | 规避 |
|---|---|
| `tail` / heredoc | PowerShell 不支持；用上文"命令约定"的形式（TPR-12） |
| `evals/evals.json` | 格式化 hook 会压平数组；用临时 `.py` 文件写入，不用 `Edit` / `Write` |
| `SKILL.md` 路由表 | 格式化 hook 对齐表格会触发 `ROUTER_ROW_RE` contract 测试；本子任务原则上不改 `SKILL.md` |
| bare import 拿到 EN 副本 | `tests/conftest.py` 只把 EN 与 AUDIT 放进 `sys.path` 前排；测试里要 zh 脚本用 `importlib.util.spec_from_file_location` |
| `ZH_EXTRA_CHECKS` 改 dict | 会破坏 `test_paper_audit.py:422`；保持 `list[str]`（TPR-11） |
| 替换挂 `grammar` 键 | 会让中文 polish 丢失表达检查；必须挂 `sentences`（TPR-01） |
| `MODULE_DIMENSION_MAP` 只改源不改测试 | `test_literature_search.py:578` 是精确相等锁（TPR-06） |
| 越权改构建配置 | 不改 `justfile` / `pyproject.toml` / `uv.lock` |

## 验收记录

- [ ] 基线：HEAD = ____，`just ci` 测试数 = ____，状态 = ____
- [ ] AC1-1 / AC1-2 / AC1-3
- [ ] AC2-1（矩阵单元数 = ____） / AC2-2 / AC2-3
- [ ] AC3-1（adapter 数 = ____，每个 5 类回归） / AC3-2 / AC3-3 / AC3-4
- [ ] AC4-1 / AC4-2
- [ ] AC5：`just ci` 测试数 = ____（不低于基线）
- [ ] AC6：`git diff --stat` 对两个写作 skill 无输出
- [ ] AC7：`test_zh_extra_checks` 状态 = ____
- [ ] Fixture manifest F1 六行 / F2 / F3 / 格式负例 / 四入口断言
