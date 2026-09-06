# 意图门控行为验收记录

验收日期 2026-09-06。

## 方法

由独立 subagent 执行，不由改动作者自评。
subagent 的行为规则只来自
`academic-writing-skills/paper-audit/references/MODE_GUIDE.md` 的
`## Input Resolution` 与 `### Auto-Detection at Intake`，
以及 `SKILL.md` 的 `## Mode Selection`（仅取模式名）。
禁止运行审计命令、禁止读论文、禁止改文件，只产出 intake 响应文本。
要求逐场景引用决定"提问还是陈述"的原句。

## 场景与结果

| 场景 | 输入 | 目录信号 | 期望 | 实际 | 判定 |
| --- | --- | --- | --- | --- | --- |
| S1 | 明确 `quick-audit` | `audit_report_2026-08.md` | 只陈述，不提问 | 只陈述 | 通过 |
| S2 | 未指定模式 | 同上 | 提问 re-audit | 提问 | 通过 |
| S3 | 明确 `quick-audit` | 审稿信 `reviewer_comments.txt` | 提问（实质冲突） | 提问 | 通过 |
| S4 | 明确 `re-audit`，缺 `--previous-report` | 恰一个候选 | 陈述解析路径并继续 | 陈述并继续 | 通过 |

## 实际响应

S1：

> Found `audit_report_2026-08.md` next to the paper; running `quick-audit` as requested.
>
> Locked before running: mode `quick-audit` (you stated it), report style `deep-review` (inferred, default), focus `full` (inferred), output language `en` (inferred from your request), venue not specified.

无模式选择题。检测信号为一句陈述。

S2：

> Found `audit_report_2026-08.md` next to the paper — this looks like a re-audit.
>
> You did not name a mode, so I inferred `deep-review`. Do you want `re-audit` against `audit_report_2026-08.md` instead, or `deep-review` as inferred?

未指定模式时提问行为保持不变。

S3：

> Found `reviewer_comments.txt` next to the paper, containing the markers `Reviewer 1` and `Editor's Comments` — this looks like a reviewer letter.
>
> A reviewer letter adds review scope, so I am not running `quick-audit` past it without your decision. Do you want me to dispatch `agents/revision_coach_agent.md` first to parse `reviewer_comments.txt` into a structured roadmap and feed that roadmap into `re-audit`, or run `quick-audit` as you asked and ignore the letter?

已指定模式但存在实质冲突时仍提问，并显式给出"增加审查范围"的理由。

S4：

> `--previous-report` was not given. I searched the paper's directory and the current working directory for `*audit_report*` / `*review_report*` / `*final_issues*.json` and found exactly one candidate: `audit_report_2026-08.md`. Resolving `--previous-report` to `audit_report_2026-08.md` and continuing in `re-audit`.

唯一候选时自行解析并陈述，未停下提问；零个或多个候选的停问分支未被本次场景覆盖。

## 规则溯源

subagent 对四个场景各引用了决定分支的原句，引用与 `MODE_GUIDE.md` 现文一致：

- S1 命中 "**Mode stated by the user**: … Report the detected signal as a one-sentence statement and run the stated mode. Do not offer a mode choice."
  及 "A stale artifact that this run will not read is not a material conflict."
- S2 命中 "**Mode inferred by you**: no decision has been made yet, so ask."
- S3 命中 "A reviewer letter always adds review scope, so this is a material conflict: ask even when the user stated a different mode."
- S4 命中 "With exactly one candidate, state the resolved path and continue."

## 证据档位

S1-S4 均为 validated advantage（有实际响应且规则溯源可核对）。

未覆盖、记为 missing evidence：

- `--previous-report` 零候选与多候选两个停问分支。
- 修订标记检测（`\added{` 等）与长文 polish 阈值两条 bullet 的已指定模式分支。
- 真实论文上的门控表现。
