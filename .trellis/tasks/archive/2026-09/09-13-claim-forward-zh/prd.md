# latex-thesis-zh 主张前置检查与改写 (C2)

父任务：`.trellis/tasks/09-13-claim-forward-integration/`。前置：C1（`09-13-claim-forward-en`）已归档，spec `claim-forward-contract.md` 与 `tests/contracts/test_claim_forward_contract.py` 已存在。

## Goal

在 `latex-thesis-zh` 新增路由模块 `claim-forward`（中文名"主张前置"），按学位论文语境重做词表、门控与结论章规则；脚本与 EN 同 5 码、同输出格式，实现独立（不做哈希对齐）。

## Requirements

### R1 脚本 `scripts/check_claim_forward.py`（ZH）

- 输入 `main.tex`（含 `\input`/`\include` 展开，沿用 `tex_loader.py`），`--section <key>`、`--json`。
- 5 码同 C1：`CF-DISCLAIM`、`CF-SELFWEAK`、`CF-CAVEAT-POS`、`CF-HEDGE-STACK`、`CF-CLOSE-NEG`；输出格式与 C1 一致（前缀 `% CLAIM-FORWARD`，`% Original:` / `% Candidate:` / `% Meaning-Check: NEEDS-LLM`）。
- 中文词表（基线依据父任务 `research/source-basis.md`）：
  - `self_weakening`：遗憾的是、仍明显落后、存在严重不足、效果有限、仅能、仅…而已、未能（引用上下文豁免）、并不理想、差强人意、略显不足。
  - 排除：裸 `仅`（`仅为`/`不仅` 占绝大多数）、`尚未`（T-PAIN 痛点词）、`有待`（展望合法用词）。
  - `disclaim_openers`：本文不试图、本文并不主张、本文无意、本研究不涉及、需要说明的是本文并未。
  - `hedges`：可能、或许、在一定程度上、某种程度、大致、基本、相对、似乎、有望（计数，≥3 报 `CF-HEDGE-STACK`）。
  - `direction_markers`：展望、未来、下一步、有待、后续、进一步研究。
  - `process_openers`：起初、最初尝试、经过多次尝试、我们曾（仅入文档，脚本不检）。
- 段落门控：abstract / introduction / contribution / conclusion 为高影响段（`CF-DISCLAIM` Minor）；`CF-CLOSE-NEG` 只看 conclusion / summary 末段。
- ZH 特有豁免：结论章"展望"前的承接句（`CC-OUTLOOK-TRANS` 要求存在）不报 `CF-CLOSE-NEG`；判定方法：负面句之后同段或下一段出现 `direction_markers` 即视为有方向。
- 引用豁免：句含 `\cite`、`\upcite`、`\citep`、`\citet` 或前句含引用且本句主语为"该方法 / 上述方法 / 现有方法 / 文献[”。
- 词表外置 `references/writing/claim-forward-terms-zh.yaml`，内置 fallback。

### R2 文档

- `references/modules/claim-forward.md`（ZH 版）：命令、5 码、豁免、与 `deai` / `over-claim-guard` / `abstract`(T-*) / `conclusion`(CC-*) / `expression` 边界。
- `references/writing/claim-forward-zh.md`：主张前置 5 步、优选 / 不推荐句式对照（中文）、`CF-LOSS-FRAME` 判断、自查四问、来源归属、否决说明（引用 `conclusion-guide-zh.md` 不利结果必须如实陈述条款）。
- `references/writing/over-claim-guard.md` 新增"向上校准"节。
- `references/modules/routing-rules.md`：三分列表 `[LLM]` layer only 组加 `claim-forward`；执行顺序在 `deai` 之后。
- `references/modules/expression.md`、`deai.md`、`conclusion.md` 各加一行指路。

### R3 SKILL.md

- 路由表加 `claim-forward` 行；路由规则段加一条；Rewrite Contract 纳入范围列表加 `claim-forward`（`[LLM]` 层）。
- description 加"主张前置 / 自我削弱 / 防御性表述"触发词，≤400。
- `last_updated` 更新；`version` 不动。

### R4 spec 与测试

- `claim-forward-contract.md` 增 "ZH 实现" 节（词表差异、承接句豁免、`tex_loader` 展开）。
- `tests/contracts/test_claim_forward_contract.py` 增 ZH 用例（脚本存在、5 码、`--help`、SKILL.md 路由行、routing-rules、deai 三副本哈希不变、`analyze_conclusion.py` 哈希不变）。
- 新建 `tests/skills/latex_thesis_zh/test_claim_forward_zh.py`（importlib 加载；每码正例 + 反例；裸"仅"不报；"尚未"不报；承接句不报 `CF-CLOSE-NEG`；引用豁免）。
- `SKILLS["latex-thesis-zh"]["modules"]` 加 `claim-forward`；`tests/skills/latex_thesis_zh/test_latex_thesis_zh_coverage.py` `SMOKE_COMMANDS` 加一条。
- `EXPECTED_ABSENCES` 已由 C1 注册 typst 缺失；ZH 不入任何哈希组。

### R5 evals 与 docs

- `evals/evals.json` 追加 id 49（fixture `evals/fixtures/claim_forward_cases_zh.tex`）。
- `evals/trigger_eval.json` 追加 ≥2 positive、≥1 negative。
- `docs/zh/` 与 `docs/` 镜像页加模块段；`docs/usage.md` / `docs/zh/usage.md` token；manifest 重生成。

## Acceptance Criteria

- [ ] fixture 上 5 码正例全部命中；裸"仅"、"尚未"、承接句、引用句 0 误报；exit 0。
- [ ] `test_claim_forward_contract.py`（ZH 用例）、`test_claim_forward_zh.py`、`test_latex_thesis_zh_coverage.py`、`test_skill_contracts.py`、`test_deai_alignment.py`、`test_trigger_evals.py`、`test_docs_bilingual_resources.py` 绿。
- [ ] `analyze_conclusion.py`、`analyze_abstract.py`、`check_style_zh.py`、`deai_check.py` 字节不变。
- [ ] 私有语料不出现在 fixture / 测试 / 文档中。
- [ ] `check_resource_sync.py`、`just ci`、`just doc-build` 绿。

## Constraints

- 不改 `analyze_conclusion.py`（其结果经 `zh_check_adapters.py` 流入 paper-audit）。
- 不改 `check_style_zh.py`（ABSOLUTE_TERMS 语义是绝对化词，与自我削弱相反，不混入）。
- 词表精度基于 5 篇私有学位论文基线，标 "研究基线 n=5"，不宣称普适。
- typst 不在范围。

## 依赖

- 依赖 C1 的 spec 与契约测试骨架；C1 未归档不得 start。
