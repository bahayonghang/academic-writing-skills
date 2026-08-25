# 设计：re-audit 与 gate 语义

## 改造前基线

无根因级复审脚本。换词即可让人工以为「已解决」。脚本静默没有独立状态名。

## 变更清单

| 文件 | 变更 |
| --- | --- |
| `academic-writing-skills/latex-thesis-zh/scripts/re_audit.py` | 只读状态 diff |
| `academic-writing-skills/latex-thesis-zh/references/workflow/controlled-rewrite.md` | 增 re-audit 段：identity、转移表、stale_patch |
| `tests/skills/latex_thesis_zh/test_re_audit.py` | 五态 fixture |
| 相关 `references/modules/*.md` | gate 五态说明 |
| docs 镜像 + manifest | 本提交内重建 |

## Identity（TPR-08）

```
identity_key = (root_cause_key, span_family)
span_family =
    node_id               若新旧 finding 都有 node_id 且相等
    else (relpath, bucket)
bucket = 行区间重叠，或中心点相差 ≤ 5 行
```

输入版本：`findings_schema_version` 与 `ir_version` 写入输出头。版本不匹配时
退出码 3，不猜测映射。

## 状态转移表（TPR-08）

版本头：输出写入 `findings_schema_version` 与 `ir_version`。任一不匹配则
退出码 3，不猜测映射、不输出五态。

拆分/合并在逐条判定之前完成：

- 一旧 identity 对应两个新 span family：仍开放的 family 进入下表；多出的
  family 视为无旧侧匹配（`new`）。
- 两个旧 identity 同一 `root_cause_key` 合成一个新节点：按该新节点走下表。

每个旧 identity 只得一态。按下列顺序取**第一条命中**（禁止并行多态）：

| 序 | 条件 | 态 |
| --- | --- | --- |
| 1 | ledger 中该 identity 曾为 `addressed`，且新侧再次匹配 | `regressed` |
| 2 | 新侧匹配，且 severity 上升，或 `evidence_status` 变差，或 `claim_snapshot.claim_strength` 下降 | `regressed` |
| 3 | 新侧匹配，`missing_evidence` 为空，且 claim-evidence 缺口已关闭或 ledger 已完成 `allowed_action` 且当前源 hash 等于 ledger 最终 hash | `addressed` |
| 4 | 新侧匹配，`missing_evidence` 为旧集合的真子集且非空 | `partial` |
| 5 | 新侧匹配（含只换 quote、证据强度未变） | `unresolved` |
| 6 | 新侧无匹配，当前源 hash ≠ ledger.`source_hash_before`，且无法按 span_family 重匹配 | `unresolved`，并标 `stale_patch=true`、`gate_blocker=true` |
| 7 | 新侧无匹配，且缺口关闭或 ledger 完成 | `addressed` |
| 8 | 新侧无匹配，且无修复证据 | `unresolved` |

全部旧 identity 判定结束后：新侧 identity 无旧侧匹配 → `new`。

证据强度升降：只读 `claim_snapshot.claim_strength`（owner 在 claim-evidence）。
finding 不得另存可写强度。强度阶梯
`unsupported < observed < supported < strong`。

Ledger 只用于只读对照。`re_audit.py` 不得 import 或调用 `thesis_workflow.py`
的写函数。`stale_patch` 供 mode 层阻断自动应用；本脚本不执行 patch。

## 七例 fixture gold

| 例 | 输入要点 | gold |
| --- | --- | --- |
| F1 | 只换连接词，root_cause_key 与 missing_evidence 不变 | `unresolved` |
| F2 | 新侧仍匹配；补上接口与证据锚点；`missing_evidence` 空；缺口关闭 | `addressed` |
| F3 | 清掉部分 missing_evidence，仍非空 | `partial` |
| F4 | 新 root_cause_key，无旧侧匹配 | `new` |
| F5 | 在 F2 之后再次引入原 identity，或 `claim_snapshot.claim_strength` 下降 | `regressed` |
| F6 | 同行文件、中心点相差 5 行或同一 `node_id`，证据未变 | 保持原 identity，态为 `unresolved`，不标 `new` |
| F7 | 当前源 hash ≠ `source_hash_before`，无法 span_family 重匹配 | `unresolved` + `stale_patch` + `gate_blocker`；源文件字节不变 |

## Gate 五态

`pass` / `fail` / `skipped` / `missing evidence` / `no_script_finding`。
`no_script_finding` 不得升为 `pass`。缺视觉证据 → `missing evidence`。
编译走既有 `scripts/compile.py`，默认禁 shell escape。

## 兼容

严格不变面：既有 analyzer CLI。
已批准差异：新脚本与新 JSON；人类可读 analyzer 行不变。

## 验证边界

自动化：七例 gold、措辞不变判定、hash mismatch 不写源、compile wrapper 被调用。
不自动化：PDF 视觉抽样（missing evidence）。

## 回滚

删除 `re_audit.py` 与测试；`git restore` controlled-rewrite.md 与模块说明。

## 已考虑不做

- 在 re-audit 内应用旧 patch：会形成第二个写入 owner。
- 只按 quote 匹配：与根因复审目标相反。
- 把 `partial` 并入 `unresolved`：无法回归「部分修复」。
