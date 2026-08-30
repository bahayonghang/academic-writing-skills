# 执行计划：latex-thesis-zh 小节游标与跨标题接口检查

前置：本子任务先于 `.trellis/tasks/08-30-subsection-lane-audit` 执行。契约在这里落地并被
测试固化后，paper-audit 侧才对齐用词。

变更清单见 `prd.md`「变更清单」表；下面每个步骤对应表中的一到多行（TPR-09）。

## 步骤

### S1 前置确认（不改代码）

- 读 `academic-writing-skills/latex-thesis-zh/scripts/parsers.py:147` 附近的 `HEADING_RE` 与
  `extract_headings`，确认无编号标记（`*`）是否可得；不可得则在调用侧按行号回读原始行。
- 读 `academic-writing-skills/latex-thesis-zh/scripts/tex_loader.py`，确认 origin map 的字段名
  与 `assemble` 入口签名。
- 不改 `parsers.py`（`tests/contracts/test_parsers_alignment.py` 锁四副本）。

验证：`uv run --extra dev python -m pytest tests/contracts/test_parsers_alignment.py`

### S2 基线快照 + 抽出 `_endpoint_jaccard`

- 先对全部既有 fixture 跑一遍 `analyze_logic.py`（各既有开关组合），把输出存为基线快照，
  供 AC-A-04 比对。
- 把 `_arc_link_missing` 内联的端点 token Jaccard 提成 `_endpoint_jaccard`，
  `_arc_link_missing` 改为调用它。

验证（回归门）：`uv run --extra dev python -m pytest tests/ -k "paragraph_arc or arc"`
既有 `P-ARC` 用例全绿，且输出与基线快照逐字一致。

### S3 小节游标

- 实现 `SubsectionUnit` 与 `_build_subsection_cursor`：装配、depth 计算、**无 depth-3 返回空
  列表 + 声明**（不回退）、编号计数器、`--first-chapter` 覆盖、`*` 标题跳过、排除区过滤、
  assembled → source 坐标映射。
- 相邻关系不进 dataclass。

验证：新增单测覆盖 depth-3 正常、无 depth-3 声明、`\section*`、`--first-chapter`、
article 类根标题为 `\section`、多文件 `source_file` 正确。

对应 AC-A-01 / AC-A-02 / AC-A-03。

### S4 fixture

- 新增 `academic-writing-skills/latex-thesis-zh/evals/fixtures/subsection-context/`：
  多文件工程（`main.tex` + `chapters/*.tex`，用 `\include`），含三级标题、同父节连续三小节
  缺进出接口、一处跨父节交接、一处单段小节、一处短段（汉字数 `< 20`）小节、一处以列表
  结尾的小节。
- 新增 `academic-writing-skills/latex-thesis-zh/evals/fixtures/subsection-context-article.tex`：
  article 类，根标题 `\section`。
- 既有 `evals/fixtures/thesis-project/main.tex` 直接用作无 depth-3 的负向 fixture，不改动它。
- fixture 内容为原创抽象文本，不含真实论文事实、数据或引用。
- 为每个 fixture 写下**期望编号序列**常量，供 AC-A-01 / AC-A-02 断言。

### S5 术语 YAML 与加载

- 新增 `references/writing/subsection-context-terms.yaml`。
- `_load_subsection_context_terms` 仿 `_load_paragraph_arc_terms`，缺字段回退内置表。

验证：单测覆盖 YAML 缺失、字段缺失、字段类型非法三种回退（AC-A-10）。

### S6 eligibility、窗口与三个检查器

- 实现 `_ctx_is_eligible`（不排除 `is_heading_lead`）与 `_build_context_window`
  （`*_status` 与部件缺省语义）。
- 实现 `_check_subsection_context`，三码 + 升级汇总。**不实现 `S-CTX-DUP`**。

验证：三码各一条命中 + 一条不命中；升级阈值边界（2 个不升级、3 个升级）；
单段 / 短段 / 列表结尾三种 `no_eligible_paragraph` 用例；跨父节 `context_sides` 取值。

对应 AC-A-05 / AC-A-06 / AC-A-07 / AC-A-09。

### S7 CLI 与 `--emit-window`

- 加三个开关，接入 `analyze()` 尾部形参。
- `--emit-window` 缺 `--subsection` 时 `parser.error`。
- 窗口输出只含部件、源坐标与只读/可改标记。

验证：与 S2 基线快照比对，不传新开关时输出逐字不变（AC-A-04）；
窗口输出不含正文原句（AC-A-08）。

### S8 references 与路由

- 新增 `references/writing/subsection-context-zh.md`，含
  `<!-- S-CTX-CONTRACT:BEGIN -->` / `<!-- S-CTX-CONTRACT:END -->` 契约块，
  块内含三码表、协议句、depth 定义句、「无 depth-3 不回退」声明句、
  `SUBSECTION_CONTEXT_MIN_HAN = 20` 的取值理由，以及与 `_arc_is_eligible` 的有意分歧说明。
- `references/modules/logic.md` 增入口与边界。
- `SKILL.md` 的 `logic` 路由行补新旗标；只改 `last_updated`，**不改 `version`**。
- `references/writing/paragraph-arc-zh.md` 补一句：跨标题接口由 `S-CTX-*` 负责。

注意：`SKILL.md` 的对齐表格会被全局格式化 hook 触碰，可能踩 `ROUTER_ROW_RE` 契约测试。
改完立刻跑 `tests/contracts/test_skill_contracts.py`。

对应 AC-A-11。

### S9 manifest 与双语页面

- 用 Bash python 计算新增两个 references 文件的 `sha256`，写入 `docs/resource-manifest.json`。
- 生成 `docs/skills/latex-thesis-zh/resources/writing/` 与 `docs/zh/...` 两侧页面。

验证：`uv run --extra dev python -m pytest tests/contracts/test_docs_bilingual_resources.py`（AC-A-12）

### S10 evals.json

- 用 Bash python 写入新条目，**不用 Edit/Write**（JSON 格式化 hook 会压平数组）。

验证：`uv run --extra dev python -m pytest tests/contracts/test_trigger_evals.py`

### S11 全量校验

```bash
just fix
just ci
```

pyright error 数不得增加（AC-A-13）。

## 回滚点

回滚只在**不撤销任何 R** 的前提下允许在本执行计划内透明进行；任何会撤销或收窄一条 R 的
处置，必须停止并走父 `prd.md` 的「合同变更 gate」（TPR-07 / TPR-09）。

| 触发 | 处置 | 是否需回父规划 |
| --- | --- | --- |
| S2 抽取 `_endpoint_jaccard` 导致 `P-ARC` 输出漂移 | 回退抽取，在新代码中复制一份独立实现，不动 `_arc_link_missing` | 否——R 不变 |
| S3 `tex_loader` origin map 字段与预期不符 | 按实际字段调整映射代码 | 否——R 不变 |
| S6 `_ctx_is_eligible` 的 `MIN_HAN = 20` 在 fixture 上误伤合法首段 | 调整常量并同步 references 中的取值理由 | 否——R 不变，但须同步 S8 文档 |
| 发现三码中任一码在本轮无法交付 | **停止**，返回父任务同步修订父 R1/R4、A 的 R-A2/AC 与 B 的前置 | 是 |
| 发现需要恢复 `S-CTX-DUP` | **停止**，返回父任务（该码本轮已按 TPR-07 移除） | 是 |

## 完成定义

`prd.md` 的 AC-A-01 ~ AC-A-13 全部勾选完成，`just ci` 全绿，父 `design.md` 的契约在 zh 侧
逐项可指到代码或 references 的具体位置。
