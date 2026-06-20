# Design — ⑤ 时态信号词检测 / ⑥ reviewer 怀疑点排序 / ① over-claim 进 paper-audit 维度

## 设计原则（含实测修正）

- **复用既有扩展点，零新框架**：⑤ 完全复刻 `_check_overclaim` 的 YAML 驱动 checker 模式；⑥① 是参考文档 + agent/lane 文案接线。
- **脚本最小、文档承载判断力**：唯一脚本改动是 ⑤ 的 `_check_tense`（deai_check.py ×3）；⑥① 不写脚本。
- **不动解析器、不动打分权重**：零 `parsers.py`、零 `SCHOLAR_EVAL_DIMENSIONS` 改动 → 不触发 `test_parsers_alignment` 与权重和测试。
- **高精度优先于召回**：⑤ 正则只收无歧义现在时报告动词，`is`/`are` 留给文档判断（见三）。

> **实测修正（Phase C）**：原假设"⑤ 经 deai 模块自动流入 paper-audit"**不成立**。`audit.py` 调用 deai
> 用 `deai_check.py <file>`（**无 `--analyze`**），默认只回一行 "Use --analyze for full analysis"，
> 故 deai 的逐条 trace（overclaim/throat-clearing/tense 等）**不进 audit issue**——这是既有行为
> （borrow 任务的 overclaim 同样如此）。结论：**⑤ 是写作技能（en/typst/zh）特性；paper-audit 的
> 时态/over-claim 觉察由 ⑥①（REVIEWER_PSYCHOLOGY 怀疑点 #7 语言问题 + claims_vs_evidence lane）承载**。
> 不在本任务改 audit 的 deai 调用（越界、会改 issue 量/clarity 打分/快照，且与用户 lane/agent 决策冲突）。
> 已验证 ⑤ **不破坏 audit**（quick-audit 跑通、deai 照常输出、无异常）。

## 一、文件落点映射

| 资产 | latex-paper-en | latex-thesis-zh | typst-paper | paper-audit |
|---|---|---|---|---|
| ⑤ checker | `scripts/deai_check.py` | `scripts/deai_check.py` | `scripts/deai_check.py` | （经 deai 自动复用，无改动） |
| ⑤ YAML 段 | `references/deai/tone-thresholds.yaml` | `references/deai/tone-thresholds.yaml` | `references/AI_TONE_THRESHOLDS.yaml` | — |
| ⑤ 时态文档 | `references/modules/tense-guide.md` | `references/writing/tense-guide-zh.md` | `references/TENSE_GUIDE.md` | — |
| ⑤ 测试 | `tests/test_deai_tense.py`（根级，conftest 已置 SCRIPT_DIR_EN） | — | — | — |
| ⑥ 文档 | — | — | — | `references/REVIEWER_PSYCHOLOGY.md` |
| ⑥ 接线 | — | — | — | `agents/critical_reviewer_agent.md`、`agents/synthesis_agent.md` |
| ① 文档 | — | — | — | `references/OVER_CLAIM_GUARD.md` |
| ① 接线 | — | — | — | `references/SUBAGENT_TEMPLATES.md`、`agents/claims_evidence_reviewer_agent.md`、`references/CHECKLIST.md` |
| references 登记 | `SKILL.md`(last_updated) | `SKILL.md`(last_updated) | `SKILL.md`(last_updated) | `SKILL.md`/`AUDIT_GUIDE.md`(last_updated) |

> en 有 `modules/`、`writing/`、`evidence/`；时态属写作机制 → en 用 `modules/`。zh 无 `modules/写作` 习惯，时态文档与 `writing/` 写作族一致 → `writing/tense-guide-zh.md`。typst 扁平大写。

## 二、⑤ 时态 checker 脚本设计（deai_check.py）

### 2.1 数据契约（tone-thresholds.yaml / AI_TONE_THRESHOLDS.yaml 新增段）

追加在现有 `overclaim:` 段后，三副本一致：

```yaml
# Tense signal words: present-tense reporting verbs that usually signal a
# past-tense violation when they appear in Methods/Results narration.
# Emits [Script] LOW traces. en/typst gate to method/result sections;
# zh gates to the English-abstract region only. "is"/"are" are intentionally
# excluded (too noisy) — see references tense guide for the judgment-level list.
tense:
  enabled: true
  present_signals:
    "\\bshows?\\b": past_in_methods_results
    "\\breveals?\\b": past_in_methods_results
    "\\bdemonstrates?\\b": past_in_methods_results
    "\\bindicates?\\b": past_in_methods_results
    "\\bpresents?\\b": past_in_methods_results
    "\\bconfirms?\\b": past_in_methods_results
    "\\bachieves?\\b": past_in_methods_results
    "\\boutperforms?\\b": past_in_methods_results
```

> 与 `term_thresholds` / `overclaim` 无重叠（那些是计数词/因果短语，这里是时态动词）。

### 2.2 假阳性过滤（`_tense_false_positive`，仿 `_is_false_positive`）

命中后按 30 字符前后文排除：

1. **图表/公式主语**：match 前出现 `Figure|Fig\.?|Table|Tab\.?|Eq\.?|Equation|Algorithm|Scheme|Section`（+可选编号）→ 跳过（"Figure 2 shows" 合法）。
2. **软件/工具主语**：match 前是大写驼峰工具名 + 现在时（"PLINK supports"）的常见构式 → 跳过（启发式：前一 token 全大写或驼峰且非句首）。
3. **指代图表的展示动词**：`as shown in|as illustrated in|as depicted in` 上下文 → 跳过。

保守起见过滤宁紧勿松（LOW 级，漏报可接受，误报伤信任）。

### 2.3 checker 实现（EN 基准，zh/typst 镜像）

复刻 `_check_overclaim`（line 367/574）+ `__init__`（line 261-263）+ DEFAULT_THRESHOLDS（line 76）模式：

1. `DEFAULT_THRESHOLDS` 增 `tense` 默认块（YAML 缺失/不可解析回退）。
2. `__init__`：`tense_cfg = self.thresholds.get("tense", {})`；`self._tense_enabled`；`self._tense_signals = list(...present_signals.items())`。
3. 新增 `_check_tense(self, section_name) -> list[dict]`：
   - `enabled` 假 → 返回 `[]`。
   - **en/typst 门控**：仅当 `resolve_section_keys` 归一后的 `section_name` ∈ {`method`, `result`}（含 `_2/_3`）才检测；否则 `[]`。复用 `_find_pattern_in_section`，但命中后过 `_tense_false_positive`。
   - trace dict 复用现有 schema：`{category:"tense", suggestion_type:"past_in_methods_results", severity:"low", section, line, ...}`，`[Script]` 走现有路径。
4. `check_section`（line 367 区域）追加 `results["traces"].extend(self._check_tense(section_name))`。

### 2.4 zh 英文摘要区域门控（仅 zh deai_check.py）

zh 正文中文无时态，`split_sections` 的 `abstract` 只识别中文 `摘要`，英文摘要不在 section key 中。故 zh 的 `_check_tense` 不走 section 门控，改为**区域门控**：

1. 在 `__init__` 计算英文摘要行范围 `self._en_abstract_range`：正则 `\\begin{abstract}...\\end{abstract}`（**排除** `\\begin{cabstract}` 中文摘要）映射到行号区间；找不到 → `None`。
2. `_check_tense`：`self._en_abstract_range is None` → `[]`（no-op）；否则仅在该行区间内逐行检测。
3. **English-line 门控**：每行 `extract_visible_text` 后，ASCII 字母占比 < 阈值（如 0.5）→ 跳过（滤掉中文行/中英混排的中文句）。
4. 同样过 `_tense_false_positive`。

> 该区域定位是 deai_check.py 内的局部正则，**不进 parsers.py**（约束 2）。zh checker 与 en/typst 的差异仅"section 门控 vs 区域门控"这一处，副本核对时显式标注。

### 2.5 副本对齐

三份 deai_check.py 是有意副本（同 parsers 策略，但 deai_check.py **未被 hash 锁定**）。EN 先实现跑通 → 镜像 typst（逻辑全同）→ 镜像 zh（替换 section 门控为 2.4 区域门控）。改完逐份 diff 核对。

## 三、`is`/`are` 不进正则的取舍

时态宪法点名 `is/are/shows/reveals`，但 `is`/`are` 在 Methods/Results 里合法用法极多（定义 "X is defined as"、通论、被动 "are aligned to"、图表 "Table 1 is ..."）。进正则将产生大量误报，违背 LOW-但-可信 的定位。沿用 borrow 任务确立的原则（"判断留文档、正则只收无歧义项"，见 memory `borrow-writing-judgment-2026-06-20`）：`is`/`are` 的时态判断写进 tense-guide 的自查清单，由 LLM/人判断，不进脚本。

## 四、⑥ reviewer 怀疑点排序设计（paper-audit）

### 4.1 文档 `references/REVIEWER_PSYCHOLOGY.md`

本地化自 `reviewer_psychology.md`，去 popgen 例子，改通用学术/CS：

- **阅读路径**：Step1 Title→Abstract→Fig1→Conclusion（3-5min 定生死）→ Step2 跳读图表/Methods 参数 → Step3 Results/Discussion 找 over-claim/漏洞 → Step4 Intro 细读/Supp 抽查。
- **8 层怀疑点降序**（核心）：① 数字↔claim 不匹配 ② 方法参数缺失 ③ 引用支持不足 ④ over-claim ⑤ 故事不闭环 ⑥ 图文脱节 ⑦ 语言问题 ⑧ 结果太干净。每层给"写作侧应对"。
- **让 reviewer 找不到 reject 理由**策略 + reviewer 类型（domain/method/generalist）。

### 4.2 agent 接线

- `critical_reviewer_agent.md`：新增一节，要求按 8 层怀疑序组织/优先 critique（最可能触发 reviewer 怀疑的先列），引用 `references/REVIEWER_PSYCHOLOGY.md`。
- `synthesis_agent.md`：合并 findings、生成 revision roadmap 时，按怀疑层级加权排序（与现有 severity 排序协同，不替换）。
- 不改 `consolidate_review_findings.py` 排序键（用户选"不加脚本排序键"）。

## 五、① over-claim 审计维度设计（paper-audit）

### 5.1 文档 `references/OVER_CLAIM_GUARD.md`

镜像 `latex-paper-en/references/evidence/over-claim-guard.md`（动词确定性梯子 + 7 替换表 + 陷阱句式 + 与 `CLAIM_EVIDENCE_CONTRACT.md` 边界小节互链）。paper-audit 视角措辞（"as a reviewer, flag …"）。

### 5.2 lane / agent 接线

- `references/SUBAGENT_TEMPLATES.md` 的 `claims_vs_evidence` lane 指令：新增 DO 项"flag over-claim wording (causal/firstness/universality/application) per OVER_CLAIM_GUARD.md，发 `claim_accuracy` issue，给 `allowed_wording`/`forbidden_wording`"。
- `agents/claims_evidence_reviewer_agent.md`：同向补充（该 agent 现仅 354B，扩成显式核查 over-claim）。
- `references/CHECKLIST.md`：新增 over-claim 判据条目（与 claim-evidence 并列）。

### 5.3 与既有暗线的关系

deai 脚本的 `overclaim` 信号已经 deai 模块流入 → scholar_eval clarity。本项**不改这条**，只在 claims-evidence 侧加 LLM 判断力维度（issue `comment_type: claim_accuracy`，经 consolidate 进 final_issues）。两条互补：脚本抓无歧义短语（clarity），LLM lane 抓语境化 over-claim（claims-vs-evidence）。

## 六、边界与兼容性

- ⑤ 新增 `category:"tense"` trace：paper-audit deai 模块对 deai JSON 是**泛型解析**（按 module/severity 聚合），新 category 不需特判；implement 阶段实跑一次确认。
- ⑤ 与 `_check_overclaim`/`term_thresholds` 词集无交集。
- ⑥① 纯文档 + 文案接线，不改任何脚本逻辑、不改 issue schema、不改打分。
- `enabled: false`（tense/overclaim 各自）可独立停用对应脚本检查。

## 七、回滚形态

- ⑤ 脚本：回滚 `deai_check.py`×3 + YAML tense 段×3 + `tests/test_deai_tense.py`；`enabled` 开关与 YAML 回退保证半完成态不破坏既有 deai 流程。
- ⑤/⑥/① 文档：纯新增，`git checkout` 对应文件即回滚，无副作用。
- agent/lane 文案：纯文本追加，回滚即删段。

## 八、风险

| 风险 | 缓解 |
|---|---|
| ⑤ 时态正则误报（尤其 zh 中英混排） | 高精度词集 + FP 过滤 + zh 区域门控 + English-line 门控；LOW 级；充分反例测试 |
| 三副本 deai_check.py 漂移 | EN 基准逐份 diff；zh 差异仅 2.4 区域门控一处，显式标注 |
| 既有 deai 测试快照被新 tense trace 打破 | 先 `just test -k deai` 摸清，确认是预期新增再更新期望 |
| paper-audit deai 解析不认 `tense` category | implement 实跑 audit deai 模块验证；泛型解析预期无碍 |
| references 新文件触发 SKILL.md 契约/布局测试 | 用既有目录；登记到 SKILL.md references 清单；跑 `test_*_layout` 确认 |
| 误 bump SKILL.md version | 只改 last_updated；提交前 grep version 四处与 pyproject 比对 |
