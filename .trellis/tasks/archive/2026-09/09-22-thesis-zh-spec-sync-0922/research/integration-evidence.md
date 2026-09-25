# 父任务集成证据

日期：2026-09-22。产品改动未提交。111 个清单状态不是 111 项合规。静态测试通过不是真实论文、PDF 或五宿主验收。

## 跨子核对

| 核对项 | 结果 |
| --- | --- |
| 学院 MODULE 提示对应真实 CLI | 合成 `main.tex` 上，`check_style_zh.py --school yanshan-ee-2025`、`check_format.py`、`check_tables.py`、`check_references.py --author-cite --repeat-cite`、`check_consistency.py --abbreviation-style` 均被 argparse 接受。`verify_bib.py --standard gb7714 --college-details` 被接受，缺字段时 exit 1。`--school yanshan` exit 2。`--college-details` 不带 GB standard exit 2。`--governance` 不带 `--custom-terms` exit 1。 |
| 学院清单不借用旧阈值 | `TEMPLATE_THRESHOLDS` 只有 `yanshan`、`thuthesis`、`pkuthss`、`generic`。博士学院清单 111 行：MANUAL 67、NEEDS-LLM 22、MODULE 22、PASS 0。exit 0 只表示没有 FAIL。 |
| `--degree-wording` 与 `--school yanshan-ee-2025` | `test_degree_wording_and_school_do_not_swallow_each_other` 通过。同一句 `极易达到50\%。` 各出现一次 `E-DEGREE` 与 `NUM-SPACE`，不互相吞掉。 |
| 公开入口 | `SKILL.md`、`README.md`、`README_CN.md`、`docs/usage.md`、`docs/zh/usage.md`、两个技能索引都保留 C1–C6 事实句。Reference Map 补上 `yanshan-ee-2025.md`，并写明与 `yanshan.md` 并存。 |

学院清单提示里的命令只打印，证据含「未检查」。一致性提示没有 `--governance`。

## 本轮新增命令

解释器：当前 `uv run --extra dev python -X utf8`。探针脚本在临时目录，未写入仓库。

| 命令 | exit |
| --- | --- |
| 上述 CLI 探针 | 0 |
| `pytest -q tests/contracts/test_skill_contracts.py tests/contracts/test_thesis_zh_guidance_fidelity.py` 与 degree/school 组合用例 | 0，40 passed |

这次只改了 `SKILL.md` 的模板列表一句。没有重跑 `just ci` 和 `just doc-build`。C6 检查之后的资源同步退出码是 0。

## 各子交付与未验收

各子 `research/implementation-evidence.md` 记录本子门禁。下表只区分交付和未验收。

| 子任务 | 已交付 | 未验收 |
| --- | --- | --- |
| C1 术语治理 | `--governance`、`--abbreviation-style`、`--degree-wording`；五条旧命令基线 MATCH | 真实论文、PDF、五宿主 |
| C2 数字公式表 | `--school yanshan-ee-2025`；六条旧命令基线 MATCH；旧四模板无差异 | 版面、视觉对齐、学校接受 |
| C3 引文文献 | `--author-cite`、`--repeat-cite`、`--college-details`、`--progression-density`；六条旧命令基线 MATCH | 页码是否支撑句子、出版事实、学校接受 |
| C4 跨表面数字 | `--cross-surface`；默认与 `--results-analysis` 基线 MATCH | 真实论文、显示层复算 |
| C5 学院清单 | YSE-001..111 子句缺失数 0；八条旧模板 JSON 基线 MATCH | PDF 页底留白、111 项合规、学校接受 |
| C6 指南 | 五主题文档与保真测试；未改脚本码 | 真实 LLM 输出、真实论文 |

提交、归档和 push 不在本轮授权内。

## 2026-09-23 复审修复：R7 私有语料替换

替换项（公开文件；.trellis/tasks 与 ref/ 不改）：

| 类别 | 旧 | 新 | 文件 |
| --- | --- | --- | --- |
| 真实作者姓 | Atmaca / atmaca2020 | Example / example2020 | evals/fixtures/citation-literature/chapters/review.tex；tests/skills/latex_thesis_zh/test_citation_literature.py；.trellis/spec/academic-writing-skills/citation-placement-contract.md |
| 私有短语 | 经验阈值用于分布筛查。设备限值由现场配置另行给定 | 归一化阈值用于初筛。硬件限值由部署环境单独给定 | claim-forward-zh.md（源、docs/zh、docs 英文镜像） |
| 私有短语 | 有效抑制虚假振荡并保证单调性 | 有效抑制数值抖动并保持单调 | claim-forward-zh.md；evals.json id 58 prompt |
| 私有短语 | 越界率高于基线 / 条件均值 | 误检率高于基线 / 分组均值 | claim-forward-zh.md |
| 私有短语 | 时序投影 / 时间投影 | 时间步映射 / 时步映射 | method-description-guide-zh.md |
| 私有短语 | 将时间维与变量维转置 | 交换时间轴与特征轴 | method-description-guide-zh.md |
| 稿件符号 | $S_{\theta}$ / $M_{\phi}$ | $G_{\alpha}$ / $H_{\beta}$ | structure-guide.md；introduction-guide-zh.md |

保留授权语境词：门禁、筑牢、本质安全、理论性能上界。references.bib 无 Atmaca 条目。

| 命令 | exit |
| --- | --- |
| 全仓 grep 旧词/旧符号（排除 .trellis/tasks、ref/） | 1（零命中） |
| check_resource_sync.py --write-manifest --inventory-only | 0 |
| check_resource_sync.py（全量） | 0；manifest 仅 sourceSha256 变化，sourceLocale 不变 |
| pytest test_citation_literature / guidance_fidelity / skill_contracts / claim_forward_contract | 0（91 passed） |
| just lint | 1：tests/skills/latex_thesis_zh/test_check_spec.py:898 字节串内含裸换行，属其他子任务工作树改动，本次未触及 |

evals.json 经 json.loads/dumps（indent=2，ensure_ascii=False，CRLF）回写，git diff 无删除行。
真实论文、五宿主与 provider 评估仍 UNVERIFIED。

## 2026-09-23 复审修复：基线迁入 tests/fixtures

三个测试文件原先读取未跟踪的 `.trellis/tasks/09-22-*/research/baseline/`，归档后路径消失。现改为读取已提交 fixture。

新路径：`tests/fixtures/thesis-zh-baselines/{term-governance,number-equation-table,citation-literature,college-checklist-2025}/`。68 个文件用 `shutil.copy2` 逐字节复制，原目录保留。`.gitattributes` 追加 `tests/fixtures/thesis-zh-baselines/** -text`。

改动的测试：`test_number_equation_table.py`（BASELINE/C1_STYLE）、`test_citation_literature.py`（BASELINE/C2_REFERENCES）、`test_check_spec.py`（_OLD_BASELINE）。比较逻辑不变。

`test_check_spec.py::test_old_four_templates_unchanged` 由 `git diff` 改为 LF 规范化 sha256 锁：

| 模板 | sha256 |
| --- | --- |
| yanshan.md | 6c72cf9f6002d9da8a2d678a98875edffe994a8563a1d18aa0331db848c07b26 |
| thuthesis.md | 9ebb084e70d3dbb6306596144efa7a7027d48be3aaaa899f47634e1eb9b97d61 |
| pkuthss.md | baaa30ac2fb08064db15d650f82bf82af2eac59d47e5d53366d231a23b3d5fe7 |
| generic.md | f3f5835b3692c92e4d04309aac9cc080186be5900ad55788e1143700c8f2d6cb |

| 命令 | exit |
| --- | --- |
| `pytest -q` 四个目标文件（157 passed） | 0 |
| `just lint` | 0 |

未重跑 `just ci` 与 `just doc-build`。

## 2026-09-23 复审修复：次要项

所有改动只影响 opt-in 路径；四个基线测试（term-governance / number-equation-table / citation-literature / check_spec 旧四模板）逐字节通过。路径缩写 S=academic-writing-skills/latex-thesis-zh，T=tests/skills/latex_thesis_zh。

| 项 | 改动位置 | 回归测试 | 结果 |
| --- | --- | --- | --- |
| 1 biblatex/cleveref 载荷屏蔽 | S/scripts/check_consistency.py:108 `_CITE_PAYLOAD_RE` | T/test_term_governance.py::test_biblatex_and_cleveref_payloads_are_masked_from_new_scans | pass |
| 2 行内 verb/lstinline/texttt 仍扫描 | S/references/modules/consistency.md:86（en 源）+ docs 两语镜像 | 资源同步 | exit 0 |
| 3 完全忽略 归 E-ABSOLUTE 文档口径 | S/references/modules/expression.md:100,102；S/references/writing/academic-style-zh.md:168,170 + 两语镜像；脚本不改 | 既有 T/test_check_style_zh.py（完全忽略→E-ABSOLUTE）；guidance-fidelity 全绿 | pass |
| 4 NUM-GROUP 版式长度与点号标识 | S/scripts/check_style_zh.py:122 lookbehind 加 `.`；:889-891 屏蔽 resizebox/rule/scalebox/hspace/vspace/minipage | T/test_number_equation_table.py::test_layout_lengths_and_dotted_identifiers_are_not_group_hits | pass |
| 5 裸 mathrm{C} 不是摄氏度 | S/scripts/check_style_zh.py:127（移除裸 mathrm{C}，增 °C、celsius） | T/test_number_equation_table.py::test_bare_mathrm_c_is_not_celsius | pass |
| 6 longtable/sidewaystable/tabularx/第二个 tabular 覆盖说明 | S/scripts/check_tables.py:429-450；S/references/formatting/table-guide.md:138 + 两语镜像 | T/test_number_equation_table.py::test_unscanned_table_floats_get_one_coverage_note | pass |
| 7 check_style_zh 哈希 | T/test_polish_unit_zh.py:29 → 48410bce2947d080393654e03fe67616398f6def998ed11721ce385cb8be1f26 | test_frozen_scripts_keep_lf_normalized_hash | pass |
| 8 footcite 进入支持集 | S/scripts/check_references.py:656；S/references/modules/references.md:41 + 两语镜像；.trellis/spec/.../citation-placement-contract.md:31 | T/test_citation_literature.py::test_footcite_is_supported_by_author_and_repeat_scans | pass |
| 9 RC-AUTHOR 大写非作者词 | S/scripts/check_references.py:1266-1270 与 :1324-1340（无 等/等人/et al. 时须紧跟作者动词） | T/test_citation_literature.py::test_capitalized_non_author_words_do_not_hit（四条探针零命中，Smith等 仍命中） | pass |
| 10 _PERSON_RE 非人称复合词 | S/scripts/check_spec.py:739；S/references/modules/spec-check.md:111 + 两语镜像；C5 design.md:32 | T/test_check_spec.py::TestThirdPerson::test_common_non_person_compounds_are_not_candidates | pass |
| 11 url/href/includegraphics/path 屏蔽 | S/scripts/check_spec.py:726 `_KEY_CMD_RE` | T/test_check_spec.py::TestThirdPerson::test_url_href_graphics_and_path_payloads_are_masked | pass |

| 命令 | exit |
| --- | --- |
| `pytest -q tests/skills/latex_thesis_zh tests/contracts/test_thesis_zh_guidance_fidelity.py tests/contracts/test_skill_contracts.py tests/contracts/test_spec_checklists.py`（1140 passed） | 0 |
| `just lint`（ruff format 后） | 0 |
| `just typecheck` | 0 |
| `check_resource_sync.py --write-manifest --inventory-only` | 0 |
| `check_resource_sync.py`（285 entries；sourceLocale 无变化，另补入 literature-progression-zh.md 与 yanshan-ee-2025.md 两条此前缺失记录） | 0 |

未做：check_spec.py 第 992 行零命中文案仍写「独立“我”」（脚本输出未改，只改文档口径）；未跑 `just ci` 与 `just doc-build`（由主会话执行）。
