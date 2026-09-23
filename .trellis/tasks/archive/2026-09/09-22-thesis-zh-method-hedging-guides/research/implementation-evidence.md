# C6 实施证据

本子只改文档、测试、eval 与公开镜像。没有新 CLI 基线。没有改 `task.json`。没有 commit。

## 脚本差异

实施前与实施后，`git diff --name-only -- academic-writing-skills/latex-thesis-zh/scripts` 都是下面 9 个路径。它们属于已在工作树中的 C1–C5，本子没有打开、暂存或改写这些文件，也没有回退它们：

- `academic-writing-skills/latex-thesis-zh/scripts/analyze_experiment.py`
- `academic-writing-skills/latex-thesis-zh/scripts/analyze_literature.py`
- `academic-writing-skills/latex-thesis-zh/scripts/check_consistency.py`
- `academic-writing-skills/latex-thesis-zh/scripts/check_format.py`
- `academic-writing-skills/latex-thesis-zh/scripts/check_references.py`
- `academic-writing-skills/latex-thesis-zh/scripts/check_spec.py`
- `academic-writing-skills/latex-thesis-zh/scripts/check_style_zh.py`
- `academic-writing-skills/latex-thesis-zh/scripts/check_tables.py`
- `academic-writing-skills/latex-thesis-zh/scripts/verify_bib.py`

其余 `latex-thesis-zh/scripts` 路径相对 HEAD 无差异。`analyze_abstract.py`、`check_claim_forward.py`、`analyze_logic.py` 不在上述列表中。

`references/modules/structure.md` 在本技能中不存在。标题与章节安排的路由写在 `SKILL.md`、`references/modules/routing-rules.md`、`structure-guide.md` 与 `introduction-guide-zh.md`。没有新建模块页，也没有新增模块表行。

## 命令与退出码

| 命令 | 退出码 |
| --- | --- |
| `rtk proxy uv run --extra dev python -m pytest -q tests/contracts/test_thesis_zh_guidance_fidelity.py tests/contracts/test_claim_forward_contract.py tests/contracts/test_skill_contracts.py` | 0（70 passed）。更早一次同命令因测试草稿中的 `assert spec` 失败，退出码 1；删掉该行后重跑为 0。 |
| `rtk proxy uv run python docs/scripts/check_resource_sync.py --write-manifest --inventory-only` | 0（285 entries） |
| `rtk proxy just ci` | 0（版本、Ruff、Pyright 0 errors / 86 warnings、pytest 2341 passed / 2 skipped） |
| `rtk proxy uv run python docs/scripts/check_resource_sync.py` | 0（285 entries） |
| `rtk proxy just doc-build` | 0（VitePress build complete） |

改过的 10 个公开源在 manifest 中 `sourceLocale` 仍为 `zh`。对应 `docs/zh/skills/latex-thesis-zh/resources/` 镜像与源文件在 CRLF 规范化后一致。英文镜像保留标题层级、代码块、行内代码与链接目标。`--inventory-only` 不是最终资源通过证明；完整检查随后退出码为 0。

## AC 映射

| AC | 位置 | 测试 |
| --- | --- | --- |
| AC1 | `method-description-guide-zh.md`「十二、方法叙述表达约束」。八个文档标签各有范围、问题例、改写例、风险与仅 LLM 所有者。`M-FORMDUPE` 与 `PR-EQ-NARR` 不得报成同一缺陷。`N-ISOLATE` 与 `M-REPRO` 不得删除复现信息。拆句只承诺数学记号多重集，并指向 `polish_unit_zh.py --verify` / `UP-MATH`。 | `test_method_expression_labels_are_llm_document_checks` |
| AC2 | `claim-forward-zh.md`「防御性说明的三类处置」。每类有可保留例与不可改例。未验证弱点不得写成设计优点。比喻词不是禁词正则。文件中无 `CF-METAPHOR`。 | `test_claim_forward_three_dispositions_keep_and_reject_examples` |
| AC3 | `paragraph-roles-zh.md`「删预告后的指代桥接」。最短桥接写出对象，并保留「上述」指向该对象；不贴回已删预告。合法「首先 / 其次」不改。换词复述不是去重。 | `test_deleted_preview_keeps_an_antecedent_and_legal_sequence_words` |
| AC4 | `abstract-structure.md`「摘要引号与英文标点」含中文 U+201C/U+201D 与英文标点的通过/不通过例，引语措辞、数学与键不变，无 `T-QUOTE`。`structure-guide.md`「六、标题不堆公式符号」与 `introduction-guide-zh.md`「章节安排句不堆公式符号」各有一例，且写明不授权改正文数学、受保护术语或模型名。 | `test_abstract_quotes_and_english_punctuation_keep_payload`；`test_title_and_arrangement_examples_do_not_authorize_body_edits` |
| AC5 | `SKILL.md` 在 C1–C5 句子之后增加六条触发，不新增模块行。`routing-rules.md`、`logic.md`、`claim-forward.md`、`abstract.md` 指向既有模块。eval id 58 只检查路由与不应改写例，并写明不代表已运行的模型输出。两语 README、usage、技能索引与 manifest 已同步。规范见 `method-narrative-contract.md` §3.5、`claim-forward-contract.md` §3.1、`paragraph-roles-contract.md` 第 3 节末条。 | `test_c6_routes_stay_on_existing_modules`；`test_c6_eval_checks_route_and_do_not_rewrite_without_a_live_run`；上表门禁 |

## 质检修订

最短桥接与建议块的「修改后」原先删掉「上述」，代词没有留下先行词。已改为「本节完成采样时钟对齐与任务调度。上述两项完成后，系统才输出设定值。」「不得贴回」仍是被删预告原句。中文镜像与源文件在换行规范化后一致。英文页只改对应散文，代码块与源文件相同。manifest 中该源的 `sourceSha256` 改为 `eac13c2eb5dd26eb6cb0920d8c062f5d93cd885d282bf7c4f8291edc87108a59`。

| 命令 | 退出码 |
| --- | --- |
| `uv run --extra dev python -m pytest -q tests/contracts/test_thesis_zh_guidance_fidelity.py tests/contracts/test_claim_forward_contract.py tests/contracts/test_skill_contracts.py` | 0（70 passed） |
| `uv run python docs/scripts/check_resource_sync.py` | 0（285 entries） |

本次质检没有重跑 `just ci` 或 `just doc-build`。上文实施表里的这两项仍是实施时记录，不是本次复跑结果。

## UNVERIFIED

真实论文、现场 LLM 输出、五宿主运行均为 UNVERIFIED。合成测试与文档合同不证明这些外部效果。
