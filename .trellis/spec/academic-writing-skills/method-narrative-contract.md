# 方法叙述跨技能契约

## 1. Scope / Trigger

修改以下任一表面前读本文：

- `latex-thesis-zh`、`latex-paper-en` 或 `typst-paper` 的方法叙述参考与
  `analyze_logic.py`；
- `M-HEADING`、`M-SEQWORD`、`M-EQUATION`、`M-EDGETABLE` 的判定、输出或对齐测试；
- `paper-audit` 的 logic 调度、`_parse_script_output`、Info/P3 报告、ScholarEval 接线或
  `section_methods` 审阅指引。

本文是开发时的跨技能可执行契约。面向写作者的详细语义分别由以下公开资源承载：

- zh：`latex-thesis-zh/references/writing/method-description-guide-zh.md`；
- en：`latex-paper-en/references/writing/section-writing/method.md`；
- Typst：`typst-paper/references/METHOD_SECTION.md`，语义以 en 参考为准并说明语法差异。

`SKILL.md`、模块页和审计 lane 只保留精确触发条件与上述权威资源的指针。

## 2. Signatures

```text
# zh：必须显式选章
analyze_logic.py thesis.tex --method-narrative --section <章名>

# en / Typst：既有 section 门控
analyze_logic.py paper.tex --section methods
analyze_logic.py paper.typ --section methods
```

```python
MN_HEADING_RUN = 3
MN_HEADING_HITS = 2
MN_EQUATION_LOOKAHEAD = 3

_parse_script_output(module_name: str, stdout: str) -> list[AuditIssue]

evaluate_from_audit(
    audit_issues: list[dict],
    literature_grounding_score: float | None = None,
) -> dict[str, float | None]
```

`AuditIssue` 的方法叙述输出面允许 `severity=Critical|Major|Minor|Info` 与
`priority=P0|P1|P2|P3`。本能力当前实际产生 `Minor/P2` 和 `Info/P3`。

## 3. Contracts

### 3.1 三技能判定

- `M-HEADING`：方法作用域内连续至少 3 个行内小标题段，其中至少 2 个标题后的首句命中
  报幕句式时，产生 1 条 `Minor/P2`。普通段落不清零；新 subsection 级标题清零。
- `M-SEQWORD`：方法小节首个自然段首句由顺序词起手且没有因果或约束词时，产生
  `Info/P3`。en/Typst 的顺序词只能来自 `TRANSITIONS["sequence"]`，不得另建词表。
- `M-EQUATION`：编号 LaTeX `equation|align|gather` 块结束后 3 个非空可见行内没有
  `式中|其中|where` 时，产生 `Minor/P2`；连续公式组只在块尾检查一次。Typst 仅检查带
  `<label>` 的块公式，未标注公式不检查。
- `M-EDGETABLE`：输出小节清单与空白逐边接口表，尾注 `[LLM] 待填写`。它是工作表，
  不是 finding，也不进入评分。

en 与 Typst 的 `MN_ANNOUNCE_RE`、`MN_SEQ_OPEN_RE`、`MN_CAUSE_EXEMPT_RE`、
`MN_EQ_GLOSS_RE` 源串必须一致；zh 使用中文正则，但三个结构常量必须一致。
`tests/contracts/test_method_narrative_alignment.py` 是跨副本锁。

### 3.2 门控与 audit 调度

- zh 只有 `--method-narrative --section <章名>` 同时存在时运行 M-*。缺 `--section` 时列出
  候选章并以状态码 2 退出；paper-audit 不猜章，也不自动运行 zh 方法叙述检查。
- en/Typst 只有 `--section methods` 运行 M-*；无 `--section` 时保留既有全文逻辑检查。
- paper-audit 对 en `.tex` 和所有 `.typ` 保留原 `--cross-section` logic task，并追加独立
  `--section methods` task。zh `.tex` 与 `.pdf` 不追加第二次调用。
- 两次 task 独立执行、分别解析，随后以 `module=LOGIC` 合并。不得把 `--section methods`
  加到原 task 上，否则会关闭全文检查。

### 3.3 Finding 块、报告与评分

结构化 finding 由一个头行和四类续行组成：

```text
%|// METHOD-NARRATIVE (Line N) [Severity: X] [Priority: Y]: [Script] M-* ...
%|// Current: ...
%|// Suggested: ...
%|// Rationale: ...
%|// Meaning-Check: NEEDS-LLM
```

- `_parse_script_output` 每个头行只创建 1 个 issue，并丢弃同一活动块内的四类续行。
- 空行结束活动块。结构化 finding 前后出现的裸诊断仍按既有 `Minor/P2` 逐行解析；混合输出
  不得因存在一个头行而丢弃其他裸行。
- 遇 `M-EDGETABLE` 标记后忽略其余工作表输出。
- Info/P3 保留在 quick-audit、gate、legacy peer、JSON 和 Phase 0 context；Phase 0 摘要也
  计入 Info。
- `evaluate_from_audit` 在任何扣分与维度路由前显式过滤 Info。不得改
  `MODULE_DIMENSION_MAP`、九维权重或 Critical/Major/Minor 的既有扣分值。

### 3.4 LLM lane 与资源同步

- 审计侧能力名为 `methodological interface and argumentation completeness` /
  `方法论接口与论证完整性`，不得把它命名为 writing quality、写作质量或叙述质量。
- `section_methods` focus block 检查六角色、逐边三对象、`M-NONDIRECT`、公式闭合及收益证据
  阶梯；notation 矛盾仍属于 `notation_and_numeric_consistency`。
- C5 在既有 `continuation|elaboration|contrast|cause-effect` 上增加
  `interface|residual-constraint`，严重程度仍沿用 C5 口径。
- 修改公开 `references/**/*.md` 或 `agents/**/*.md` 后，必须更新 manifest、英文同源页与
  完整中文译文，并执行单技能和全量资源检查及文档构建。

## 4. Validation & Error Matrix

| Condition | Required behavior |
| --- | --- |
| zh 开启 `--method-narrative` 但无 `--section` | 列候选章，exit 2，不猜章 |
| en/Typst 无 `--section methods` | 不运行 M-*；既有全文检查不变 |
| en `.tex` 或 `.typ` 进入 paper-audit | 一次 `--cross-section` + 一次 `--section methods` |
| zh `.tex` 或任意 `.pdf` 进入 paper-audit | 只有原全文 logic task，无 methods task |
| 一条 finding 带四条续行 | 1 个 issue；续行不膨胀计数 |
| 结构化 finding 与裸诊断混合 | finding 成块解析；裸诊断继续 Minor/P2 |
| Info/P3 finding | 报告与 context 可见；ScholarEval 扣分为 0 |
| M-EDGETABLE 及表格行 | 0 个 issue |
| Typst 无 label 块公式 | 不执行 M-EQUATION |
| 公开 agent/reference 内容变化 | manifest、en、zh 任一缺失即资源检查失败 |

## 5. Good / Base / Bad Cases

- Good：病例产生 `M-HEADING Minor/P2`、`M-SEQWORD Info/P3`、
  `M-EQUATION Minor/P2`；干净对照为 0；soundness 只因两条 Minor 下降 1.0。
- Base：调用 en/Typst logic 时不传 section，输出与方法叙述功能加入前一致。
- Bad：把原 `--cross-section` 改成 `--section methods`；把接口表算成 Minor；让 Info 从报告
  消失或进入 ScholarEval 扣分；为 Typst 未标注公式猜测编号状态。

合法标题负例必须保持零误报：EN/Typst Related Work 分组标题、Typst 实验分析 lead-in、
zh `\paragraph{核心结论概括}`。

## 6. Tests Required

- `tests/contracts/test_method_narrative_alignment.py`：三方结构常量、en/Typst 正则源串与公开
  M-* 表面一致。
- 三技能 `test_*_method_narrative.py`：病例、干净版、无门控、公式边界及三类合法标题负例。
- `tests/skills/paper_audit/test_paper_audit.py`：块解析、mixed fallback、M-EDGETABLE、Info/P3
  报告/context、ScholarEval 前置过滤和 `.tex|.typ|.pdf` 调度矩阵。
- `tests/skills/paper_audit/test_method_narrative_audit_integration.py`：真实三技能脚本、病例/干净
  对照及 soundness 分差来源。
- `tests/skills/paper_audit/test_paper_audit_topology_docs.py`：focus block、C5 与角色边界字符串锁。
- 最终运行四技能 `check_resource_sync.py --skill`、全量资源检查、`just doc-build` 和
  `just ci`。

真实论文语料的查准率与召回率不由合成测试证明；没有实文评估时保持 `UNVERIFIED`。

## 7. Wrong vs Correct

### Wrong

```python
# Replaces the full-document task and silently disables cross-section checks.
extra_args = ["--section", "methods"]

# Treats every output line, including continuation fields and the worksheet,
# as a scored Minor issue.
for line in stdout.splitlines():
    issues.append(AuditIssue("LOGIC", None, "Minor", "P2", line))
```

### Correct

```python
tasks.append(("logic", script, ["--cross-section"]))
if (fmt == ".tex" and lang == "en") or fmt == ".typ":
    tasks.append(("logic", script, ["--section", "methods"]))

# Parse one issue per structured header, suppress only its protocol fields,
# retain standalone fallback lines, and stop before M-EDGETABLE.
issues = _parse_script_output("logic", stdout)
```
