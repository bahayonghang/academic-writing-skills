# 中文学位论文段落职责与结构去重契约

## 1. Scope / Trigger

修改 `latex-thesis-zh/scripts/analyze_logic.py` 的 `--paragraph-roles`、PR-* 判据、
`paragraph-roles-terms.yaml`、相关 fixture 或公开段落职责资源时，必须遵守本文。
面向写作者的语义说明以 `references/writing/paragraph-roles-zh.md` 为权威；本文锁定开发接口、
六码契约、豁免、私有标定边界和防回归门禁。

## 2. Signatures and Constants

```text
uv run python scripts/analyze_logic.py INPUT [--section SECTION] [--first-chapter N] [--paragraph-roles]
```

```python
analyze(file_path: Path, ..., paragraph_roles: bool = False) -> list[str]

PR_INTRO_BG_MIN_HITS = 3
PR_INTRO_TOC_MIN_ITEMS = 5
PR_LEAD_DUP_JACCARD = 0.3500
PR_LEAD_MIN_HAN = 40
PR_SUB_CHAL_MIN_HITS = 2
PR_EQ_NARR_MIN_HITS = 3
```

所有阈值常量标注为**未标定 / UNVERIFIED**。
术语表固定包含 `background_markers`、`roadmap_markers`、`challenge_markers`、
`enumeration_markers`、`operator_markers`、`summary_new_argument_envs` 六个字段。
运行时逐字段读取 YAML；缺失、类型错误或非法值只回退该字段，内置默认与 YAML 及两个 neutral docs 副本
必须相等。

## 3. Contracts

- `--paragraph-roles` 是可选附加开关，默认关闭；未传 flag 时输出必须逐字节不变。
- 所有 finding 均为 `[Script]` 观察，默认 `[Severity: Info] [Priority: P3]`，块内必须含 `Meaning-Check: NEEDS-LLM`。
  不得输出 `Meaning-Check: PRESERVED`，不得复制完整原句，不得给 `logic` 增加自动改写契约。
- `--method-narrative` 在未指定 `--section` 时的提前返回路径保持不变；在该路径下 `--paragraph-roles` 不运行。
- 六码判定与豁免契约：
  1. `PR-INTRO-BG`：正文章引言块中 `background_markers` 去重命中 $\ge 3$。
     块内与“第X章”承接句处于同一句的不计入；第 2 章（概述式引言）豁免；引言块为空时不报（由默认检查覆盖）。
  2. `PR-INTRO-TOC`：章引言块内节号目录（`\d+\.\d+\s*节`）$\ge 1$ 且路线词（首先/其次/最后）$\ge 2$（双写），
     或节号目录条目 $\ge 5$（详列展开）。单独合规节号目录或单独路线预告不报。
  3. `PR-LEAD-DUP`：含 level-3 子节的 level-2 标题后首个 `ArcParagraph`（导语且汉字 $\ge 40$）与本章章引言
     的 bigram Jaccard $\ge 0.3500$ 时报告。导语 $< 40$ 汉字、本章无章引言块、或无 level-3 子节时豁免。
  4. `PR-SUB-CHAL`：正文具体方法章的 level-3 小节首个 `ArcParagraph`（汉字 $\ge 40$）命中挑战词 $\ge 2$
     且列举序词 $\ge 2$ 时报告。绪论/结论/相关工作章、标题含“引言/概述”的小节豁免。
  5. `PR-EQ-NARR`：正文章编号公式组后首个可见段落（汉字 $\ge 40$）命中算子翻译词 $\ge 3$ 时报告。
     段落以“式中/其中”开头且只含符号释义（无算子词）时不报。
  6. `PR-SUM-NEW`：规范化标题为“本章小结”的区间内出现 `\cite{}`、数学环境、`\[` 或图表/算法环境任一时报告。
     `\ref`/`\eqref`/`\autoref` 回指已有图表合法通过；注释行排除。
- 架构回滚承诺：章引言块定位从 `_check_chapter_intro` 抽为 helper `_chapter_intro_block`；
  抽取后必须保证默认输出与 `baseline-before.txt` 逐字节相等。若基线锁红，回退为原内联实现并改用复制逻辑的私有 helper（在 spec 记录两处同步义务）。
- 删预告后的指代是文档层 LLM 判断，写在 `paragraph-roles-zh.md`，不新增 PR 码。
  删除预告句之后，代词仍须有先行词，桥接取最短的一句。不得把删掉的预告贴回去。
  不得改写合法的「首先 / 其次」。换词后再重复主张不是去重。
  `PR-EQ-NARR` 仍只定位逐算子翻译，与方法指南的 `M-FORMDUPE` 不是同一缺陷。

## 4. Private Calibration Boundary

私有论文或内部语料仅可用于阈值研究，不得成为常规 CI 的隐式前置条件。
常规测试与 CI 仅使用已提交的合成 fixture；公开测试和样例中不得出现真实私有论文语句、作者信息或本机绝对路径。
六项阈值常量未经全量跨学科跨校抽样标定前，始终标为 `UNVERIFIED`，不宣称误报率或漏报率。

## 5. Tests Required

- zh 脚本按 `testing-and-tooling.md` 的 importlib 模式加载并锁定 `__file__` 为 zh 副本。
- 锁定六码正反例：第 2 章豁免 `PR-INTRO-BG`；单独节号目录与单独路线预告豁免 `PR-INTRO-TOC`；
  阅读地图式导语豁免 `PR-LEAD-DUP`；“式中”释义段豁免 `PR-EQ-NARR`；小结 `\ref` 回指豁免 `PR-SUM-NEW`。
- 锁定 finding 格式包含 `[Script] PR-`、`[Severity: Info] [Priority: P3]`、`Meaning-Check: NEEDS-LLM`，
  且报告中不出现 fixture 整句。
- 锁定 YAML 字段与内置默认等价，以及逐字段降级回退能力。
- 锁定 `SMOKE_COMMANDS` 包含 `--paragraph-roles`，且默认输出基线 `baseline-before.txt` 逐字节不变。
- 改 `analyze_logic.py` 后必须同步更新 `tests/skills/latex_thesis_zh/test_polish_unit_zh.py` 的 `FROZEN_HASHES["analyze_logic.py"]`（LF 规范化 sha256）；漏改会让 `just ci` 在无关的单元润色冻结哈希上红。
- `--section` 作用域测试必须用 `resolve_section_keys` 能命中的键（如 `method`/`experiment`）。传入 `"2"` 会走“未找到章节”ERROR 路径，断言“无 PR-INTRO-BG”会假绿。
- 锁定公开资源同步、双语镜像相等以及 VitePress 构建。
