# 技术设计 (C3)

## 1. EN 密度数据与计数契约

旧每篇绝对上限 A 只在 5000 个可见词基线换算：

```text
density = A / 5000 * 10000 = 2A
allowance(words) = ceil(density * max(words, 1500) / 10000)
```

因此 `words=5000` 时 allowance=A；其他长度有意按密度缩放。阈值表由
`5,3,5,4,...` 变为 `10,6,10,8,...`。这不是 EN 语料标定。

分母唯一来源为 C1 运行时 `_corpus_size`：先遍历 `_iter_visible_lines`，再用
`\b[A-Za-z][A-Za-z'-]*\b` 计数。不得在测试或说明里另用 `\S+`。

`DEFAULT_THRESHOLDS` 与 `references/deai/tone-thresholds.yaml` 同步：

- `threshold_unit: per_10k_words`
- `density_fallback.min_corpus: 1500`
- `throat_clearing.budget_per_10k: 2.0`, `min_budget: 1`
- `section_factors.organization: 6.6`, `summary/default: 1.0`
- `sequence_terms: first, second, then, finally, next`

organization 系数借用 ZH，保持 UNVERIFIED。EN parser 已由 C1 支持 organization 标题；
不新增段落级伪 section。

### 序列词匹配

仅 `sequence_terms` 使用大小写敏感、排除连字符后缀的独立词正则；其他 term threshold
继续 case-insensitive。建议形态：

```python
rf"\b{re.escape(term)}\b(?![-‐‑‒–—][A-Za-z])"
```

共享 `_check_term_threshold` 先改 EN canonical，再同步 Typst 字节副本和 ZH 可执行逻辑，
并更新 alignment relationship：EN density 值等于 Typst 旧绝对值的 2 倍，Typst 数据不改。

## 2. P-ARC runtime

主入口：`latex-paper-en/scripts/analyze_logic.py`。新增末尾参数
`paragraph_arc: bool = False` 和 CLI `--paragraph-arc`，关闭时不调用新路径。

复用 C2 的已固化开发契约：段落切分、prose segment、原始相邻关系、四位 Jaccard、
结构化 finding 与私有/真实语料证据边界。EN 差异如下：

- `PARAGRAPH_ARC_MIN_WORDS=40`
- `PARAGRAPH_ARC_LINK_THRESHOLD=0.0200`（provisional, UNVERIFIED）
- `PARAGRAPH_ARC_DOUBLE_MISSING_RUN=2`（provisional, UNVERIFIED）
- 标题后首段不豁免；标题仍结束 segment
- 专用 section 豁免为 abstract/conclusion/acknowledgment/appendix

### 段落与章节所有权

边界为空行、纯注释、`\par`、标题、公式/图/表/算法/代码/列表环境。环境变体与 C2
contract 同步。LINK 只比较同一 segment 中原始相邻的合格段；不能过滤后重新 zip。
section 先取最具体识别范围，子节结束后回退到所属顶层 section。

### 四项判据

- LEAD：首句少于 8 个可见词且无判断谓词；空过渡剥离后少于 6 词；引用剥离后少于
  5 词；或仅数字/单位/符号。
- CLOSE：末句无 retrospective marker 且无 prospective pattern。
- LINK：后段首句无显式承接标记，且端点均至少 8 词、四位 Jaccard `<0.0200`；短端点
  只检查显式标记并报告为待复核。
- FLAT：单句成段，或全部句子为 author/year enumeration；related 中后者交给既有检查。

词表置于 `references/writing/paragraph-arc-terms.yaml`，至少包含
`judgment_predicates/empty_transitions/retrospective_patterns/prospective_patterns/
explicit_link_patterns`；逐字段非法时回退同值默认。

## 3. Output, baseline, and evidence

每个 finding 使用：

```text
% PARAGRAPH-ARC (...) [Severity: Info] [Priority: P3]: [Script] P-ARC-* ...
% Current: ...
% Suggested: Please verify ...
% Rationale: This heuristic observes form and does not decide semantic quality.
% Meaning-Check: NEEDS-LLM
```

不复制完整段落，不生成 rewrite。激活前在 task research 固化受控 EN sample 和改造前输出；
激活后先复制到 `tests/fixtures/paragraph_arc_en/`。产品测试不依赖 task 路径。

G2 只用受控样本人工核读，不称真实论文验证。5–10 篇目标 venue 语料缺失，准确率、召回率、
N/τ 与 organization 因子的外部有效性均为 UNVERIFIED。

## 4. Rollback

- 删除 `threshold_unit` 恢复 legacy per-document；同时恢复旧 DEFAULT/YAML 数据。
- 删除 `--paragraph-arc` 参数与调用恢复旧逻辑输出。
- 不迁移用户数据。
