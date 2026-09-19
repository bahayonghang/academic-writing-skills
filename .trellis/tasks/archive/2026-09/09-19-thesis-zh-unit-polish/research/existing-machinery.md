# 可复用机制与锁清单（实施前必读）

日期：2026-09-19。路径均相对仓库根。技能根 `academic-writing-skills/latex-thesis-zh/`（下记 `$Z`）。

## 1. 复用 API（import，不复制）

| 符号 | 位置 | 说明 |
|---|---|---|
| `assemble(entry) -> AssembledDocument` | `$Z/scripts/tex_loader.py` | `.lines` / `.content` / `.origin(line_no)->(file,line)` / `.lineref(start,end)` / `.multi_file` / `.warning_lines(prefix)` |
| `read_text_robust(path)` | 同上 | 编码鲁棒读取 |
| `get_parser(path)`、`resolve_section_keys(section, sections)` | `$Z/scripts/parsers.py` | `LatexParser.split_sections(content)->{key:(start,end)}`、`extract_visible_text(line)`、`extract_headings(content)` |
| `_build_subsection_cursor(doc, parser, sections, first_chapter=None) -> list[SubsectionUnit]` | `$Z/scripts/analyze_logic.py:1352` | depth-3 游标；`SubsectionUnit(subsection_id,title,depth,parent_id,source_file,source_start,source_end,assembled_start,assembled_end,section_scope)` |
| `_split_arc_paragraphs(content, parser, sections) -> list[ArcParagraph]` | `analyze_logic.py:1449` | `ArcParagraph(start,end,visible,raw,sentences,section,segment_id,is_heading_lead,in_item,ends_with_env)` |
| `_build_context_window(units, index, paragraphs) -> dict` | `analyze_logic.py:1650` | 依赖模块级 `_DOC`（`analyze()` 在 :3298-3301 设置）；`_parent_context_for_unit` / `_context_part` 读 `_DOC` |
| `_render_context_window(window) -> list[str]` | `analyze_logic.py` | 打印 `% 小节窗口 …` / `% current : file Ls-Le [可改]` / `[只读]` |
| `_has_numbered_depth3(doc, parser)`、`SUBSECTION_CONTEXT_NO_DEPTH3` | `analyze_logic.py:1316`、`:1047` | 无 depth-3 声明句原文：`% 小节级：本文档无 depth-3 标题，未产出小节级观察。` |
| 常量 `PARAGRAPH_ARC_MIN_HAN=40`、`SUBSECTION_CONTEXT_MIN_HAN=20`、`SUBSECTION_CONTEXT_MIN_HAN_RATIO=0.30` | `analyze_logic.py` | 只读参考，不改 |
| `hedges` 字段 | `$Z/references/writing/claim-forward-terms-zh.yaml` | `UP-STRENGTH` hedge 计数来源；`check_claim_forward.py` 的 YAML 读取与内置回退策略可仿照 |
| `--custom-terms` JSON `{"zh": [[...]], "en": [[...]]}` | `$Z/scripts/check_consistency.py` | `--terms` 格式复用 |

`emit-window` 实测输出（fixture subsection-context，单元 1.2.1）：

```text
% 小节窗口 1.2.1《缺口单元甲》
% current    : chapters/method-a.tex L15-L19 [可改]
% prev.tail  : chapters/method-a.tex L10-L10 [只读]
% parent_lead: chapters/method-a.tex L12-L13 [只读]
% next.head  : chapters/method-a.tex L21-L21 [只读]
```

## 2. 既有脚本输出形态（单元前诊断的解析目标）

- `check_style_zh.py --json`：`{entry, goal, strength, findings[{code,tier,loc,severity,priority,title,original,suggestion,candidate,basis,changed,protected,risk_flags}], warnings, routed_to}`；`loc` 形如 `chapters/experiment.tex:8`。
- `check_claim_forward.py --json`：`{file, section, terms_source, errors, findings[{code,line,location,severity,priority,section,original,candidate,note}], summary}`。
- `deai_check.py --section <key> --analyze`：文本报告 `第N行 [category]` + `-> 建议:`；`--fix-suggestions` 出 JSON。裸片段（无章节键）不产出。
- 报告头格式：`中文表达检查（expression）`、`% CONTRACT [Script]: goal=… strength=…`；`% MODULE (loc) [Severity: X] [Priority: Pn] [Script]: CODE title`。

## 3. 锁与联动（改一处查其余）

| 锁 | 位置 | 影响 |
|---|---|---|
| deai 三副本哈希/AST 锁 | `tests/contracts/test_deai_alignment.py` | `deai_check.py` 不改 |
| parsers 哈希锁 | `tests/contracts/test_parsers_alignment.py` | `parsers.py` 不改 |
| claim-forward `NO_LEAK_FILES`（含 `check_style_zh.py`）与 `LEAK_RE` | `tests/contracts/test_claim_forward_contract.py:40-60` | 新脚本可引用 claim-forward 词表文件，但 `check_style_zh.py` 等不得出现 `CF-*` / `claim-forward` 字样 |
| S-CTX 契约块镜像 | `tests/contracts/test_subsection_context_contract.py` | 不改 `subsection-context-zh.md` 契约块 |
| 路由行正则 `ROUTER_ROW_RE` + `--help` 匹配 | `tests/contracts/test_skill_contracts.py:165,485` | 路由命令中每个 `--flag` 须出现在脚本 `--help` |
| `SKILLS["latex-thesis-zh"]["modules"]` | `test_skill_contracts.py:74-92` | 加 `polish` |
| `REFERENCE_LAYOUTS` 子目录白名单 + kebab-case | `test_skill_contracts.py:141,275` | 新文件放 `modules/` 或 `writing/` |
| description 120–400 字符 | `test_skill_contracts.py:311` | 当前约 195（需实测） |
| 命令示例必须含 `uv run python` | `test_skill_contracts.py:322` | 文档示例 |
| `SMOKE_COMMANDS` 覆盖路由表全部脚本 | `tests/skills/latex_thesis_zh/test_latex_thesis_zh_coverage.py:90-135` | 加 `polish_unit_zh.py`；cwd = `evals/fixtures/thesis-project` |
| 孤儿扫描 | 同文件 `test_no_orphan_reference_files` | 新 references 文件须被 SKILL.md / 其他文档 / 脚本按文件名引用 |
| `POLISH_MODULE_DOCS` / `OVER_CLAIM_GUARD` | `tests/contracts/test_polish_contract_alignment.py:59-79` | 新 `polish.md` 需含四字段、`NEEDS-LLM`、`../writing/over-claim-guard.md` |
| 排除列表 `**排除` ≥8 且不含 `expression` | 同文件 :175 | `polish` 加到"仅 `[LLM]` 层"组，不进排除组 |
| `--tier` 不得与 `--goal` / `--strength` 同行 | 同文件 :210 | 新文档写 `--tier` 时单独成行并声明属 `deai` |
| evals 前缀哈希（前 49 条 / 前 53 条） | `tests/contracts/test_thesis_zh_guidance_fidelity.py:154` | 只追加 |
| trigger_eval 健康规则 | `tests/contracts/test_trigger_evals.py` | 三字段、query 唯一 |
| usage 页 token | `tests/contracts/test_docs_bilingual_resources.py:176` | `docs/usage.md`、`docs/zh/usage.md` 加 `` `polish` `` |
| manifest / 双语页 | `docs/scripts/check_resource_sync.py`、`docs/resource-manifest.json` | 新 references / examples 文件各一行 + en/zh 两页 |
| `version` 全仓同步 | `tests/contracts/test_skill_versions.py` | 只改 `last_updated` |

## 4. 既有文件现状（实施时的编辑锚点）

- `$Z/SKILL.md`：路由表 L61–81（`claim-forward` 行 L74）；路由规则 L83–89；Rewrite Contract L107–124（"`claim-forward` 同属仅 LLM 层"句在 L124）；Reference Map L151–178；CRLF。
- `$Z/references/modules/routing-rules.md`：三分法 L16–18（`**排除` 锚点 L18）；逐类判据在"## 逐类判据"节末尾追加。
- `$Z/references/modules/expression.md`：末段"交给 claim-forward.md"之后加一行。
- `$Z/references/modules/deai.md`：末段"留在本模块"之后加一行。
- `docs/skills/latex-thesis-zh/index.md` 路由表 L28–45、Module References L84–100；`docs/zh/...` 路由表 L37 附近、Module References L84–100、写作参考 L102–120。
- `docs/usage.md:42-46`、`docs/zh/usage.md:42-46`。
- `$Z/evals/evals.json`：`{"skill_name","evals"}`，49 条，末 id 49，CRLF；`trigger_eval.json`：`{"skill_name","queries"}`，53 条，CRLF。
- `$Z/examples/`：5 个 md；`logic-and-experiment.md` 受 guidance-fidelity 测试锁定，勿改。

## 5. 归档先例

- `.trellis/tasks/archive/2026-09/09-13-claim-forward-zh/`：新增"仅 `[LLM]` 层"模块的完整落地样板（脚本 + 词表 + 模块文档 + 路由 + evals + docs）。
- `.trellis/tasks/archive/2026-08/08-30-subsection-cursor-zh/`：小节游标与窗口的设计取舍（无 depth-3 不回退、`_ctx_is_eligible`、装配后枚举标题）。
- `.trellis/tasks/archive/2026-08/08-25-thesis-zh-quality-closure/`：**未实现**（评审"需返回规划"），不存在 `thesis_workflow.py` / `visible_prose.py`，勿假设。
