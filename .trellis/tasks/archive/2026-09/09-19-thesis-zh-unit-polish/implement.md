# 执行计划：`polish` 模块

前置：用户于 2026-09-19 明确确认 prd.md 的 D1–D5 全部采用现有建议。完成最终规划摘要评审及 `task.py start 09-19-thesis-zh-unit-polish` 之后开始实施。所有命令在仓库根目录运行。

## 顺序

1. spec：新建 `.trellis/spec/academic-writing-skills/unit-polish-contract.md`（单元定义、`UP-*` 语义与分档、退出码、禁改清单、与 S-CTX / P-ARC / 改写契约 / claim-forward 的关系、私有语料边界）；`index.md` 加一行。
2. fixture：`academic-writing-skills/latex-thesis-zh/evals/fixtures/unit-polish/main.tex`（ctexbook；≥2 章、含 depth-3 小节；样本句覆盖 S2 垫话、`不仅…而且`、免责句先于主张、方法段多步骤长句、`\cite` / `\ref` / `\label` / 行内公式 / 数值单位）；`revised-ok.tex`（同一单元的合规润色稿）；`revised-drift.tex`（删一个 cite 键、改一个数字、`可能`→`证明`、多出 `next.head` 首句、多出 `\subsection`）。全部合成文本。
3. 脚本：`scripts/polish_unit_zh.py`（design §3）。`--help` 列出 `--plan --verify --section --unit --first-chapter --original --revised --terms --max-growth --json`。
4. 测试：`tests/skills/latex_thesis_zh/test_polish_unit_zh.py`（prd R5.2 全部用例 + 六脚本 sha256 锁 + `test_reused_logic_helpers_exist`）；`test_latex_thesis_zh_coverage.py` `SMOKE_COMMANDS` 加行；`test_skill_contracts.py` `modules` 加 `polish`；`test_polish_contract_alignment.py` `POLISH_MODULE_DOCS` 加 zh `polish.md`；`test_subsection_context_contract.py` 同步 ZH 的实施日期断言，保留 paper-audit 原日期。
5. 文档：`references/modules/polish.md`；`references/writing/unit-polish-zh.md`（design §5，含 S1/S2 归属）；`routing-rules.md`（三分法 + 判据 + 顺序）；`expression.md` / `deai.md` 各一行；`examples/unit-polish.md`。
6. SKILL.md：路由行（`uv run python $SKILL_DIR/scripts/polish_unit_zh.py main.tex --plan`）、路由规则一条、Rewrite Contract 段"仅 `[LLM]` 层"加 `polish`、Reference Map 加协议文件、description 加触发词（润色这段/这一节/单元润色/核对润色）且 ≤400、`last_updated`。改完立即跑 `tests/contracts/test_skill_contracts.py`（格式化 hook 会重排表格）。
7. evals：Bash python 追加 `evals.json` id 50（绑定 `evals/fixtures/unit-polish/main.tex`、`revised-ok.tex`、`revised-drift.tex`；assertions 含 `UP-CITE`、`UP-NUM`、`UP-STRENGTH`、`not_contains "Meaning-Check: PRESERVED"`、`regex (修改说明|待补证)`）；`trigger_eval.json` 追加 ≥2 正例 ≥1 负例。写入前读原文件风格（CRLF、`json.dumps(indent=2, ensure_ascii=False)` round-trip），写后 `git diff --stat` 应为纯增量。
8. docs：`docs/skills/latex-thesis-zh/index.md` 与 `docs/zh/skills/latex-thesis-zh/index.md` 路由表行、Module References、写作参考、Examples；`docs/usage.md` / `docs/zh/usage.md` token；`uv run python docs/scripts/check_resource_sync.py --write-manifest --inventory-only` 后补三对镜像页（zh 源页原样 + en 译页，链接目标同步），再单独运行 `--skill latex-thesis-zh` 校验（`--skill` 与 `--inventory-only` 不能组合）。

   按仓库 Documentation & Contributor Notes，同步 `README.md` 与 `README_CN.md` 中该技能的一行能力说明，补充带核对的段落/小节润色。
9. D2 已确认不修改 `references/writing/academic-style-zh.md` §3；无需该项变更。
10. 私有语料复核（不进仓库）：对 `ref/thesis/decrypted/` 任意一篇的一个小节，用 LLM 按协议润色后跑 `--verify`，只把各 `UP-*` 命中数记入本任务 `research/verify-baseline.md`（不贴原文、不贴润色稿）。

## 验证命令

```bash
uv run python academic-writing-skills/latex-thesis-zh/scripts/polish_unit_zh.py academic-writing-skills/latex-thesis-zh/evals/fixtures/subsection-context/main.tex --plan
uv run python academic-writing-skills/latex-thesis-zh/scripts/polish_unit_zh.py academic-writing-skills/latex-thesis-zh/evals/fixtures/thesis-project/main.tex --plan
uv run python academic-writing-skills/latex-thesis-zh/scripts/polish_unit_zh.py academic-writing-skills/latex-thesis-zh/evals/fixtures/unit-polish/main.tex --verify --unit 1.1.1 --revised academic-writing-skills/latex-thesis-zh/evals/fixtures/unit-polish/revised-ok.tex
uv run python academic-writing-skills/latex-thesis-zh/scripts/polish_unit_zh.py academic-writing-skills/latex-thesis-zh/evals/fixtures/unit-polish/main.tex --verify --unit 1.1.1 --revised academic-writing-skills/latex-thesis-zh/evals/fixtures/unit-polish/revised-drift.tex --json
uv run pytest tests/skills/latex_thesis_zh/test_polish_unit_zh.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_coverage.py tests/skills/latex_thesis_zh/test_subsection_context.py -q
uv run pytest tests/contracts/test_skill_contracts.py tests/contracts/test_polish_contract_alignment.py tests/contracts/test_deai_alignment.py tests/contracts/test_parsers_alignment.py tests/contracts/test_subsection_context_contract.py tests/contracts/test_claim_forward_contract.py tests/contracts/test_thesis_zh_guidance_fidelity.py tests/contracts/test_trigger_evals.py tests/contracts/test_docs_bilingual_resources.py -q
uv run python docs/scripts/check_resource_sync.py --skill latex-thesis-zh
just ci
just doc-build
```

Windows 下 `--json` 重定向需 `PYTHONIOENCODING=utf-8` 内联；不给 pytest 命令加该变量。

## 评审门

- 门 1（步骤 4 后）：`--plan` 在 subsection-context fixture 上 id 集合 = 9 个预期 id；drift 稿触发 `UP-CITE` / `UP-NUM` / `UP-STRENGTH` / `UP-SCOPE`，ok 稿零 Error；`git diff --stat` 不含六个禁改脚本。
- 门 2（步骤 6 后）：`test_skill_contracts.py`、`test_polish_contract_alignment.py`、`test_latex_thesis_zh_coverage.py` 绿；description ≤400；`version` 仍 6.0.0。
- 门 3（步骤 10 后）：`check_resource_sync.py --skill latex-thesis-zh`、`just ci`、`just doc-build` 绿；evals 前缀哈希测试绿；`research/verify-baseline.md` 只含核对码与命中数。

## 回滚点

- 每门一个 commit（`feat(latex-thesis-zh): ...` / `docs(latex-thesis-zh): ...`）；`git revert` 任一门。
- 步骤 9 无变更，不产生 commit。

## Fable 复审补充实施（2026-09-19）

用户已授权按复审结果继续完善。本轮保持原任务与文件边界，不修改六个禁改脚本，
不新增依赖，不提交、推送或归档。

1. 脚本与核心测试：补齐有本地 biblatex 定义依据的引用命令和大写交叉引用，统一
   键抽取与载荷屏蔽；明确术语只影响强度计数的屏蔽；完善候选上下文、CLI 帮助、
   人类可读差异与 plan 输出；使用异于内置回退的 YAML 哨兵词验证加载。
2. 文档与注册表：整理 Reference Map、逐类判据、双语索引和模块/SMOKE 顺序，
   同步术语屏蔽与子串启发式限制及引用命令边界；刷新 manifest 与双语镜像。
3. 集成核对：更新本 spec/设计/需求记录，运行核心与契约测试、独立复审、完整
   `just ci`、资源门和 docs build，将本轮结果写入 `research/implementation-validation.md`。

标题空白的严格比较与模板宏参数的覆盖限制沿用既定设计。未配置术语的普通用法
仍需人工辨别，不为消除单个示例增加硬编码例外表。
