# Implementation Plan

## Gate

- [ ] 用户明确批准开始实施
- [ ] 运行 `python -X utf8 ./.trellis/scripts/task.py start 08-10-deai-anti-ai-integration`
- [ ] 加载 `trellis-before-dev` 并复核 task/spec/research 上下文
- [ ] 保存基线：`git status --short`，确认任务外 dirty paths 并从提交范围排除

## Phase 1: Contract And Canonical EN

- [ ] 新增 `.trellis/spec/academic-writing-skills/deai-pattern-cluster-contract.md`，固化 H-*、F-*、
  作者样本优先级、C 档边界、H-OUTLOOK/defensive 去重和缺失证据声明
- [ ] 在 `.trellis/spec/academic-writing-skills/index.md` 登记新契约
- [ ] 新增 EN `references/deai/pattern-clusters.md`，按 `research/delta-matrix.md` 写七模式、反例、
  fidelity loop 与 attribution
- [ ] 更新 EN guide/module，只加渐进加载路由、简短共同边界与“非 AI 身份判定”声明
- [ ] 自审：不得复制参考 skill 的虚构示例、50 分评分或 Personality and Soul 内容

Checkpoint:

```powershell
rg -n "H-ING|H-PROMO|H-ATTR|H-PRED|H-TERM|H-SCOPE|H-OUTLOOK|Fidelity" .trellis/spec/academic-writing-skills academic-writing-skills/latex-paper-en/references
git diff --check
```

## Phase 2: ZH And Typst Adaptation

- [ ] 新增 ZH `references/deai/pattern-clusters.md`，使用中文学术反例，保持 H-* 语义等价
- [ ] 更新 ZH guide/module 路由；保留合法限定、学位论文语域和 LaTeX anchors
- [ ] 新增 Typst `references/DEAI_PATTERN_CLUSTERS.md`，覆盖中英文正文并保护 `@cite`、`<label>`、
  math、code、`#set/#show/#let`
- [ ] 更新 Typst guide/module 路由
- [ ] 保持阈值/术语文件原路径和内容：EN/ZH 使用 `references/deai/tone-*.{yaml,md}`，Typst 使用
  flat-layout `references/AI_TONE_THRESHOLDS.yaml` 与 `references/AI_TONE_TERMS.md`
- [ ] 逐项核对 EN canonical、ZH 与 Typst 的七模式、反例和 fidelity 字段一致；允许语言自然差异，
  不允许 contract drift

Checkpoint:

```powershell
git diff --exit-code -- academic-writing-skills/*/scripts/deai_check.py academic-writing-skills/*/scripts/deai_batch.py academic-writing-skills/latex-paper-en/references/deai/tone-thresholds.yaml academic-writing-skills/latex-thesis-zh/references/deai/tone-thresholds.yaml academic-writing-skills/typst-paper/references/AI_TONE_THRESHOLDS.yaml academic-writing-skills/latex-paper-en/references/deai/tone-terms-en.md academic-writing-skills/latex-thesis-zh/references/deai/tone-terms-zh.md academic-writing-skills/typst-paper/references/AI_TONE_TERMS.md
uv run --extra dev python -m pytest tests/contracts/test_deai_alignment.py -q
```

## Phase 3: Fixtures, Evals, Contract Test

- [ ] 为 EN、ZH、Typst 各新增一个 `anti_ai_pattern_clusters` composite fixture，包含 A-H 八个本地
  case：A 覆盖五类组合正例，B/C 分别覆盖 H-PRED/H-TERM 正例，D-H 覆盖七类反例，并保留
  引用/公式/标签保护 token
- [ ] 在三份 `evals/evals.json` 以“当前最大 ID + 1”追加 eval，绑定真实 fixture。禁止通过
  Edit/Write/apply_patch 修改这些 JSON；必须由 shell 调用 `python -X utf8` 按各文件现有格式和
  换行写入，写后用 `json.loads` 校验并确认 diff 纯追加，事前规避 formatter hook 重排
- [ ] 新增 `tests/contracts/test_deai_pattern_cluster_contract.py`，断言：
  - 9 个 runtime source 的渐进路由和统一契约；
  - 七个 H-* 的命中组合与证据充分反例；
  - explicit rewrite gate、F-* 四字段、作者样本优先级和禁用评分/AI 概率；
  - H-OUTLOOK 与 defensive-rhetoric 的 owner/合并规则；
  - 三个 fixture/eval 的唯一绑定、append-only ID 与 A-H 本地边界；
  - 新类别未进入三份脚本 threshold/DIMENSION_MAP/pattern tables；
  - Trellis spec 可发现。
- [ ] 检查 eval diff 为纯追加，JSON 均可解析

Checkpoint:

```powershell
uv run --extra dev python -m pytest tests/contracts/test_deai_pattern_cluster_contract.py tests/contracts/test_deai_alignment.py tests/contracts/test_polish_contract_alignment.py -q
uv run --extra dev python -m pytest tests/skills/latex_paper_en tests/skills/latex_thesis_zh tests/skills/typst_paper -q
```

## Phase 4: Bilingual Resource Sync

- [ ] 为 3 个新增 source 和 6 个修改 source 更新 18 个 EN/ZH docs target
- [ ] 运行 manifest 重建，逐条审查 9 项 `sourceLocale`、目标路径、技术 token 与链接
- [ ] 运行 affected skill 和全量 resource checker
- [ ] 再次重建 manifest 并确认 `git diff` 零新增漂移

Commands:

```powershell
uv run python docs/scripts/check_resource_sync.py --write-manifest --inventory-only
uv run python docs/scripts/check_resource_sync.py --skill latex-paper-en
uv run python docs/scripts/check_resource_sync.py --skill latex-thesis-zh
uv run python docs/scripts/check_resource_sync.py --skill typst-paper
uv run python docs/scripts/check_resource_sync.py
```

## Phase 5: Full Verification And Review Gate

- [ ] `git diff --check`
- [ ] `uv run --extra dev python -m pytest tests/contracts -q`
- [ ] `just ci`
- [ ] `just doc-build`
- [ ] 重跑 Phase 2 的完整 `git diff --exit-code -- ...` 守卫，确认三方脚本、batch、threshold 与
  tone-term reference 零变化
- [ ] 审查最终 diff 只含 task 计划内 source/spec/eval/test/docs/manifest；保留用户其他改动
- [ ] 在 verification 记录静态通过项和未执行证据；provider/盲评/真实论文效果标
  `missing evidence / UNVERIFIED`

## Rollback Points

1. EN contract 发现语义不稳：先回滚 Phase 1，不继续复制到 ZH/Typst。
2. 任一反例误报：修订 H-* 判据和三方 fixture，不用词表例外堆叠补洞。
3. docs sync 漂移：按单个 source + 两个 target + manifest 记录成组回滚。
4. eval 写入前先确认 shell Python 路径、格式和换行；若仍发生非语义重排，恢复该文件后按
   repository JSON 写入约定重新追加。
5. 任何实现需要脚本/依赖/schema：停止并回到规划，作为 material scope expansion 请求批准。
