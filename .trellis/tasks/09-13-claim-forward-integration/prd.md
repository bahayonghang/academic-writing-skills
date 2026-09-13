# 防御性写作（自我削弱）检查与改写整合到 EN/ZH/paper-audit（父任务）

## Goal

把 `ref/defensive/` 中两个"对抗防御式写作"参考 skill 的可采纳规则，以 **claim-forward（主张前置）** 为名整合进三个 skill：

- `latex-paper-en`：新增 `claim-forward` 路由模块（脚本检查 + `[LLM]` 改写规则）。
- `latex-thesis-zh`：同名模块的中文实现（词表、门控、结论章规则均按学位论文语境重做）。
- `paper-audit`：只加审稿信号（文档 + agent + 固定观察码集合），不加脚本、不改评分。

本父任务持有需求源、术语、任务图、跨子任务验收标准与最终集成复查；不直接承担实现。

## 需求来源

- 来源 A：`ref/defensive/anti-defensive-writing/`（Kiterlin，MIT，句子/段落级）。
- 来源 B：`ref/defensive/anti-defensive-writing-Skill/`（Adkid-Zephyr，MIT，叙事级）。
- 来源事实与红线兼容性：`research/source-basis.md`。
- 逐条采纳/否决：`research/delta-matrix.md`（S1–S24）。

## 术语与命名冲突

- 仓库已有 `defensive-ai-rhetoric-contract.md`（"defensive speculative explanation"，08-05）。本任务概念不同，**禁止**复用 "defensive" 作模块名或代码前缀。
- 统一术语：英文 `claim-forward`，代码前缀 `CF-`；中文"主张前置"（目标）/"自我削弱"（对象）。
- 观察码集合：`CF-DISCLAIM`、`CF-SELFWEAK`、`CF-CAVEAT-POS`、`CF-HEDGE-STACK`、`CF-CLOSE-NEG`（脚本）；`CF-LOSS-FRAME`（LLM only）。

## 已定架构决策

1. **独立脚本而非现有脚本加 flag**：EN/ZH 各新增 `scripts/check_claim_forward.py`。理由：TIER1 哈希锁禁改 `analyze_abstract`/`improve_expression`；deai 契约禁加 hedge 正则；`analyze_conclusion.py` 结果流入 paper-audit 评分。新脚本不入任何哈希锁，注册 `EXPECTED_ABSENCES["check_claim_forward.py"] = ["typst"]`。
2. **typst-paper 不在范围**：本轮不做 typst 副本；docs 与 SKILL.md 不宣称 typst 支持。
3. **改写走 polish contract**：`claim-forward` 归入 routing-rules 三分列表的"`[LLM]` layer only"组（与 deai 同组）；`[Script]` 输出恒 `Meaning-Check: NEEDS-LLM`；`--strength minimal` 为默认建议。
4. **over-claim-guard 增"向上校准"节**：over-claim 阶梯是上限，claim-forward 只把 hedge 降到证据已支撑的那一档；不得为显得果断而删 caveat。
5. **否决来源 B 的选择性呈现规则**（S16–S18、"不说输"①③⑤、决策级 1/3/5/6、自查 #6）：与 `conclusion-guide-zh.md`、`OVER_CLAIM_GUARD.md`、critical_reviewer cherry-picking 冲突。三个子任务的参考文档必须写明否决理由。
6. **paper-audit 仅文档层**：沿用 paragraph-arc-audit-contract 先例；不改 `audit.py`、`scholar_eval.py`、rubric、ISSUE_SCHEMA、lane 数；固定 5 码集合由契约测试锁定。
7. **段落门控**：用 `split_sections` 的 section key；abstract/introduction/contribution/conclusion 为高影响段（`CF-DISCLAIM` 升 Minor）；`CF-CLOSE-NEG` 只看 conclusion/summary 末段。
8. **执行顺序串行**：C1（EN）→ C2（ZH）→ C3（audit）→ 父任务集成复查。理由：C1 建 spec `claim-forward-contract.md` 与契约测试骨架，C2/C3 只扩展；docs manifest 单写者。

## 任务图

| 子任务 | 目录 | 交付 |
|---|---|---|
| C1 | `09-13-claim-forward-en` | EN 脚本、模块文档、参考文档、terms YAML、SKILL.md 路由、spec + 契约测试、evals、docs |
| C2 | `09-13-claim-forward-zh` | ZH 脚本（词表/门控重做）、模块文档、参考文档、SKILL.md 路由、SMOKE_COMMANDS、evals、docs |
| C3 | `09-13-claim-forward-audit` | OVER_CLAIM_GUARD / CLAIM_EVIDENCE_CONTRACT / SUBAGENT_TEMPLATES / REVIEW_LANE_GUIDE / REVIEWER_PSYCHOLOGY / 5 个 agent 文档、契约测试扩展、eval + fixture |

## 跨子任务验收标准

- [ ] 三个 skill 的术语一致：`claim-forward` / 主张前置 / `CF-*`；无 "defensive" 命名的新模块或代码。
- [ ] `.trellis/spec/academic-writing-skills/claim-forward-contract.md` 存在，`index.md` 有索引行；`tests/contracts/test_claim_forward_contract.py` 覆盖 EN/ZH/audit 三方。
- [ ] EN 与 ZH 脚本对同一 5 码集合输出格式一致：`% CLAIM-FORWARD (Line N) [Severity: …] [Priority: …]: [Script] CF-… ` + `% Original:` + `% Candidate:` + `% Meaning-Check: NEEDS-LLM`；exit 0。
- [ ] `deai_check.py` 三副本、TIER1 哈希组、`analyze_conclusion.py`、`audit.py`、`scholar_eval.py` 字节不变。
- [ ] paper-audit 观察码集合恰为 5 个，契约测试锁定。
- [ ] 三份 evals.json 各追加 1 条（EN id 24、ZH id 49、PA id 26），trigger_eval 各加正向查询；`test_trigger_evals.py` 绿。
- [ ] `docs/` 双语页面 + `resource-manifest.json` 同步；`uv run python docs/scripts/check_resource_sync.py` 绿；`just doc-build` 绿。
- [ ] `just ci` 四步全绿。
- [ ] 三个子任务的参考文档均含来源归属（两仓库 URL + MIT）与否决说明。

## Constraints

- 不 bump `version`（保持 6.0.0），只改各 SKILL.md `last_updated`。
- description 长度 ≤400 字符（现 EN 335 / ZH 176 / PA 304）。
- evals.json 通过 Bash python 写入（EN/ZH CRLF 规范化 round-trip；PA 紧凑格式文本拼接）。
- 私有语料 `ref/thesis/decrypted/` 只做研究基线，不进测试与 fixture。
- 不改 `justfile`、`pyproject.toml`、`uv.lock`。
- 实现前需 `task.py start`；本父任务不 start，只在三个子任务归档后做集成复查。

## 修订记录

- 2026-09-13 v1：初版；来源分析与 S1–S24 判定完成。
