# Claude Code 审阅意见核验

## 核验范围

本轮逐条核对审阅报告提出的 P1-1、P1-2、P2-1、P2-2、P3-1、P3-2。证据来自当前
任务工件、实际 runtime 路径、现行 Trellis spec、contract test 与当前 PowerShell 进程；
任务保持 `planning`，未修改产品文件。

## 裁决

| ID | 裁决 | 仓库证据 | 规划修订 |
| --- | --- | --- | --- |
| P1-1 | 成立 | Typst 实际读取 `references/AI_TONE_THRESHOLDS.yaml`；EN/ZH 读取 `references/deai/tone-thresholds.yaml` | PRD 与 implement 的零改动守卫列出三个确切路径，并登记 Typst flat-layout 差异；同时保护三方 tone-term reference，落实“不扩词表” |
| P1-2 | 成立 | 原 A-F 设计只有 A 覆盖 H-ING/H-PROMO/H-ATTR/H-SCOPE/H-OUTLOOK；H-PRED/H-TERM 只有 E 反例 | fixture 扩展为 A-H；B/C 分别提供 H-PRED/H-TERM 独立正例，D-H 保存七类边界反例 |
| P2-1 | 成立 | defensive-rhetoric 契约处理“机制堆叠 + 逐项证据缺口 + terminal caveat”；H-OUTLOOK 处理 limitation/challenge 后的空泛积极回弹，同一 Discussion 段可能同时出现 | 新增 owner/merge 规则：同一根因合并；满足 defensive 组合判据时以 evidence finding 为 primary，H-OUTLOOK 只作 secondary facet；可分离 span/repair 才拆 finding |
| P2-2 | 成立 | `testing-and-tooling.md` 明确 `evals.json` 禁用 Edit/Write，必须由 shell Python 写入，以避免 formatter hook 重排 | Phase 3 改成事前强制；写前识别每个文件格式/换行，写后 `json.loads` 与纯追加 diff 校验 |
| P3-1 | 前提不成立，建议可采纳 | 当前会话是 PowerShell Core 7.6.4，`$env:SHELL=pwsh`，不是 Git Bash | 不改成 Bash 续行；所有 checkpoint 改为无续行符的单行命令，兼容 PowerShell 与 Git Bash |
| P3-2 | 部分成立 | `test_polish_contract_alignment.py` 只扫描 SKILL、routing 与既有 polish module docs，不会自动扫描新 pattern-clusters reference | Phase 3 提前运行该测试作为既有契约兼容回归；新 reference 的四字段和七类命中仍由 `test_deai_pattern_cluster_contract.py` 直接锁定 |

## 审阅报告其余结论

审阅报告对 W1-W22 完整性、参考示例捏造、现有模式覆盖、prose gate、四字段闭集、9 个
public source / 18 个 docs target、append-only eval 和命名零冲突的判断，与本轮仓库核验一致。
这些结论不改变既有 scope。

## Review Gate 影响

上述修订属于规划精化，不改变用户目标、三 surface 范围、LLM-only 路线、无产品脚本改动
边界或验收成本等级。修订完成后仍需向用户展示最新最终规划摘要；只有后续明确批准才能运行
`task.py start`。
