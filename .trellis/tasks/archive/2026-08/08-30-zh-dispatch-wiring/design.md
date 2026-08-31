# Design — zh 检查调度修复与专属检查器接通

范围：`academic-writing-skills/paper-audit/scripts/audit.py` 与 `tests/skills/paper_audit/`。
不修改 `latex-thesis-zh/scripts/` 与 `latex-paper-en/scripts/` 任何文件。

## 0. 真实入口可达性矩阵（TPR-01 前置）

任何"按模式差异化"的设计都必须先落在真实入口上。实测四条入口：

| # | 入口链 | 传给 `run_audit` 的 mode | 是否进检查循环 |
|---|---|---|---|
| E1 | `main()` else 分支（`audit.py:3225`） | `args.mode`（唯一透传处） | 是 |
| E2 | `run_audit:2441` → `run_deep_review` → `run_audit`（`:1737`） | 硬编码 `"quick-audit"` | 是 |
| E3 | `main()` re-audit 分支 → `run_reaudit` → `run_audit`（`:2963`） | 硬编码 `"quick-audit"` | 是 |
| E4 | `run_audit:2431` → `run_polish_precheck`（`:2254`） | 不传 mode | **否**，早退后直接 `_resolve_script("logic"/"sentences", ...)` |

推论，均为本设计的硬约束：

1. **不做按模式的 zh 附加检查集合。** E2 把 `:1737` 改成 `mode="deep-review"` 会与 `:2441` 的委派形成无限递归；E3 同理无法区分。若强行写 `ZH_EXTRA_CHECKS["deep-review"]` / `["re-audit"]`，这两个键永不被读取，是死配置。阻断资格改由 §7 的 `gateEligible` 规则控制——它与 mode 无关，只看检查项本身的性质。
2. **zh 替换必须挂在 `sentences` 键上。** E4 只解析 `logic` 与 `sentences`。挂 `grammar` 并抑制 `sentences` 会让中文 polish 丢掉表达检查。
3. **格式面必须显式。** `.typ` 独占 `SCRIPTS_TYPST`（`:420`-`:421`），zh 检查器不可达 → 显式豁免；`.pdf` 需 TeX 源 → 进既有跳过清单（`:2492` 附近）。

## 1. 三档判定（R6-R8 定档）

| check | 脚本 | zh 现状 | 判定 | 依据 |
|---|---|---|---|---|
| `sentences` | `analyze_sentences.py`(EN) | 回退 | **替换** → `check_style_zh.py` | `CLAUSE_MARKERS`(`:27`) 是英文从句标记且按词计数；`check_style_zh.py` 的字符级句长与中文词表是对位替代。挂此键而非 `grammar`，使 E4（polish）自动获得替代（§0 推论 2） |
| `grammar` | `analyze_grammar.py`(EN) | 回退 | **抑制** | 英文语法规则对中文正文无判定力；职能已由上一行的 `check_style_zh.py` 覆盖，两键同挂会重复调用同一脚本 |
| `figures` | `check_figures.py`(EN) | 回退 | **有意复用** | DPI / 图片格式 / 编号序列，只读 LaTeX 正则与图片文件元数据，不涉正文语言 |
| `pseudocode` | `check_pseudocode.py`(EN) | 回退 | **抑制** | **非语言中性**（TPR-05）：`_count_words` 是 `len(re.findall(r"[A-Za-z0-9_+-]+", text))`，纯中文注释恒为 0，`> 12` 长注释阈值永不触发；`re.match(r"^(?:The\|A\|An)\b", caption)` 查英文冠词；`:194`-`:195` 要求字面量 `"Input:"` / `"Output:"`。中文本地化需独立定义标记、度量与中英混排策略，是能力而非接线，本期不做 |

`check_style_zh.py` 一次调用覆盖原 `grammar` + `sentences` 两键职能：中文口语词 `COLLOQ_MAP`(`:50`)、绝对化词 `ABSOLUTE_TERMS`(`:61`)、搭配错误 `COLLOC_ERRORS`(`:76`)、残缺主语 `SUBJECT_MARKERS`(`:88`)、中西文标点、数字单位、字符级句长。

**module 名副效应**：替换挂在 `sentences` 键上，`_parse_script_output` 得到的 module 是 `SENTENCES`，它已在 `MODULE_DIMENSION_MAP` 中映射到 `clarity`，无需扩展映射。这是选 `sentences` 键的第二个理由。

`check_style_zh.py` 一次调用覆盖原 `grammar` + `sentences` 两键职能：中文口语词 `COLLOQ_MAP`(`:50`)、绝对化词 `ABSOLUTE_TERMS`(`:61`)、搭配错误 `COLLOC_ERRORS`(`:76`)、残缺主语 `SUBJECT_MARKERS`(`:88`)、中西文标点、数字单位、字符级句长。因此 `sentences` 在 zh 下抑制而非替换。

## 2. 语言覆盖表（新增数据结构）

```python
# 值为脚本名 = 按语言替换；值为 None = 按语言抑制（区别于"找不到脚本"）
LANG_SCRIPT_OVERRIDES: dict[str, dict[str, str | None]] = {
    "zh": {
        "sentences": "check_style_zh.py",   # §0 推论 2：挂此键，E4(polish) 才能拿到替代
        "grammar": None,                    # 职能并入上一行，避免重复调用
        "pseudocode": None,                 # TPR-05：非语言中性，本期不做中文本地化
    },
}

# 语言无关、在 zh 下有意复用英文副本的 check
LANG_NEUTRAL_REUSE: dict[str, frozenset[str]] = {
    "zh": frozenset({"figures"}),
}

# zh 专属检查器：只适用于 .tex；.typ 与 .pdf 显式豁免（§0 推论 3）
ZH_ONLY_TEX_CHECKS: frozenset[str] = frozenset(
    {"spec", "blind", "abstract", "conclusion", "literature", "tables"}
)
```

格式面规则：

| fmt | 行为 |
|---|---|
| `.tex` | 覆盖表生效；`ZH_ONLY_TEX_CHECKS` 生效 |
| `.typ` | 覆盖表**不生效**（`audit.py:420`-`:421` 独占 `SCRIPTS_TYPST`）；`ZH_ONLY_TEX_CHECKS` 全部豁免，日志 reason = `format-exempt` |
| `.pdf` | `ZH_ONLY_TEX_CHECKS` 全部加入既有跳过清单（`audit.py:2492` 附近，与 `format` / `figures` / `references` / `citations` 同列），日志 reason = `format-skipped` |

## 3. 解析结果显式化（R9）

`_resolve_script` 的签名与行为契约**保持不变**。它被 `tests/skills/paper_audit/test_method_narrative_audit_integration.py:29`、`:42`、`:49`、`:75` 直接调用，且 `:49` 用 `monkeypatch.setattr` 替换该函数。改签名会破坏这四处。

新增一层包装：

```python
@dataclass(frozen=True)
class ScriptResolution:
    path: Path | None
    origin: str   # "audit" | "zh" | "en" | "typst" | "none"
    reason: str   # "own" | "lang-native" | "lang-neutral-reuse" | "override"
                  # | "suppressed" | "format-exempt" | "format-skipped" | "missing"

def _resolve_check(check_name: str, lang: str, fmt: str) -> ScriptResolution:
    path = _resolve_script(check_name, lang, fmt)   # 保持 monkeypatch 可见
    origin, reason = _classify_resolution(check_name, lang, fmt, path)
    return ScriptResolution(path, origin, reason)
```

生产代码（`audit.py:2486` 附近）改调 `_resolve_check`；`_resolve_script` 内部承载覆盖表逻辑，因此 monkeypatch 替换它时旧测试行为不变。

日志分化：

| reason | 输出 |
|---|---|
| `own` / `lang-native` / `override` | `[audit] RUN {check}: {script.name} (origin={origin}, {reason})` |
| `lang-neutral-reuse` | `[audit] RUN {check}: {script.name} (origin=en, lang-neutral reuse for lang={lang})` |
| `suppressed` | `[audit] SKIP {check}: suppressed for lang={lang} ({note})` |
| `format-exempt` | `[audit] SKIP {check}: not applicable to {fmt}` |
| `format-skipped` | `[audit] SKIP {check}: requires TeX source, {fmt} input` |
| `missing` | `[audit] SKIP {check}: script not found` |

当前四种情形共用两条不可分辨输出的问题由此消除（R9、AC2-3）。

## 4. bib 输入修复（R2）

`_load_bibliography_content(path, content, fmt) -> str` 返回内容字符串，被 `tests/skills/paper_audit/test_literature_search.py:484`-`:499` 断言，签名不动。抽出路径解析：

```python
def _resolve_bibliography_paths(path: Path, content: str, fmt: str) -> list[Path]:
    """解析 \\bibliography / \\addbibresource / Typst bibliography() 得到存在的 .bib 绝对路径。"""
    # 由 audit.py:62-95 的现有逻辑原样抽出，去掉读文件那一步

def _load_bibliography_content(path: Path, content: str, fmt: str) -> str:
    return "\n\n".join(_read_source(p) for p in _resolve_bibliography_paths(path, content, fmt) ...)
```

`bib` 检查的调度改为：

- 有解析结果：第一个 `.bib` 路径作为位置参数（`verify_bib.py:459` 的位置参数是 `bib_file`）。多个 `.bib` 时逐个调度，findings 合并。
- 无解析结果：`[audit] SKIP bib: no .bib resolved from {source_hint}`，不发起调用。当前对 `.tex` 输入返回 `Status: PASS / Total entries: 0`（EN 与 ZH 副本实测均如此）的空通过由此消除。

`_run_check_script(script_path, file_path, extra_args)` 的 `file_path` 参数即位置参数，无需改签名，只需在 `tasks` 构造处替换传入值。

**GB 标准取值**：`fmt == ".tex"` 且（`lang == "zh"` 或 `--venue thesis-zh`）时追加 `--standard gb7714`。不选 `gb7714-2025`，依据：

- `latex-thesis-zh/scripts/check_spec.py:173` 的规范清单命令本身用 `--standard gb7714`，这是仓库内的现行推荐值。
- `verify_bib.py:406`-`:413` 在 `standard == "gb7714"` 时会主动产出 `gb_standard_transition` 提示，内容是"答辩在 2026-07-01 之后建议与学校确认是否切换新国标，可改用 `--standard gb7714-2025`"。选 `gb7714` 让脚本把标准切换决定交回作者，而不是由 `paper-audit` 单方面替学校定标。
- 切换默认标准是 `latex-thesis-zh` 的决定，不在本任务范围。

**Typst 不适用（TPR-02）**：`typst-paper/scripts/verify_bib.py` 没有 `--standard`，只有 `--style`（3 处命中，取值形如 `gb-7714-2015-numeric`）。`.typ` 输入不追加 `--standard`���否则 argparse 以退出码 2 失败。该组合进 §8 的退出码回归用例。

`UNVERIFIED`：本任务未用 GB/T 7714 原文核验 `verify_bib.py` 内置规则本身是否符合国标。设计只保证开关被正确传递，不保证规则内容正确。

不新增 `--bib-standard` CLI 开关：`audit.py` 现有 27 个 flag，用户需要 2025 标准时直接跑 `latex-thesis-zh` 的 `verify_bib.py`。

## 5. zh 专属检查器接入与 adapter registry（TPR-02）

**禁止"优先 JSON、否则文本"的通用猜测式解析。** 每个脚本一个具名 adapter，登记实测 CLI、输出协议与 issue 映射。下表的 `--json` 列为实测值。

| 新 key | 脚本 | `--json` | 传入参数 | 输出协议 | adapter |
|---|---|---|---|---|---|
| `spec` | `latex-thesis-zh/check_spec.py` | 有 | `--json`；有 `.bib` 时加 `--bib <path>` | JSON | `SpecJsonAdapter` |
| `abstract` | `latex-thesis-zh/analyze_abstract.py` | 有 | `--json` | JSON | `AbstractJsonAdapter` |
| `conclusion` | `latex-thesis-zh/analyze_conclusion.py` | 有 | `--json` | JSON | `ConclusionJsonAdapter` |
| `tables` | `latex-thesis-zh/check_tables.py` | 有 | `--json` | JSON | `TablesJsonAdapter` |
| （`sentences` 覆盖）| `latex-thesis-zh/check_style_zh.py` | 有 | `--json`；可选 `--section` | JSON，含 `severity` ∈ {Info, Warning}（`:132`、`:253`、`:277`） | `StyleZhJsonAdapter` |
| `blind` | `latex-thesis-zh/blind_review.py` | **无** | `--check`；按可用元数据可选 `--author` / `--supervisor`。**绝不传 `--generate`** | Markdown 标题 + `[HIGH]` / `[P0]` 标记，不符合审计器既有 `[Severity: ...][Priority: ...]` 文本协议 | `BlindReviewTextAdapter`（专用解析器） |
| `literature` | `latex-thesis-zh/analyze_literature.py` | **无** | 有 `.bib` 时加 `--bib <path>` | 文本 | `LiteratureTextAdapter` |

各 JSON 脚本的对象结构并不统一，因此每个 JSON adapter 也要各自登记字段路径，不共用一个通用 JSON 解码器。

**只读边界（TPR-09 修正）**：写回触发分支是 `if args.generate:`（`blind_review.py:794`）。契约是**绝不传 `--generate`**。`--author` / `--supervisor` 是只读扫描输入，缺失时会跳过部分姓名检测，因此**不禁用**，按可用元数据决定是否传。验收方式改为文件 sha256 与 mtime 不变（AC4-1），不用参数黑名单代理。

**不接入的两项**：

- `optimize_title.py`：优化取向，产出的是标题改写建议。`paper-audit` 的红线是不改写论文（`SKILL.md:61`），把改写建议塞进审阅报告会混淆 reviewer 与 editor 角色。
- `map_structure.py`：工具性脚本，产出结构映射。`prepare_review_workspace.py` 已产出 `artifacts/data/section_index.json`（`audit.py:2530` 附近的 `REQUIRED_REVIEW_WORKSPACE_FILES`），职能重复。

这两项不进 `script_map`，避免留下新的死键。

## 6. `ZH_EXTRA_CHECKS` 保持扁平（TPR-01、TPR-11）

**放弃按模式改成 dict。** 两条理由：

1. §0 的可达性矩阵证明 `deep-review` / `re-audit` / `polish` 三个键没有读取入口，会成为死配置。
2. `tests/skills/paper_audit/test_paper_audit.py:419`-`:422` 的 `test_zh_extra_checks` 直接 `from audit import ZH_EXTRA_CHECKS` 并断言 `"consistency" in ZH_EXTRA_CHECKS`。改成 dict 后该断言变为查键，结果为 False，测试直接红。此前 design 写"`tests/` 中无引用"是取证错误——当时的 grep 被 `head` 截断。

保留扁平列表，只扩内容：

```python
ZH_EXTRA_CHECKS: list[str] = [
    "consistency",          # 保留，test_paper_audit.py:422 依赖
    "spec", "blind", "abstract", "conclusion", "literature", "tables",
]                            # "gbt7714" 删除（死条目，能力改由 §4 的 --standard gb7714 承载）
```

`audit.py:2476`-`:2477` 的 `checks.extend(ZH_EXTRA_CHECKS)` 不改。模式差异不再由这里表达——阻断资格改由 §7 的 `gateEligible` 控制，格式适用性由 §2 的 `ZH_ONLY_TEX_CHECKS` 控制。

`test_zh_extra_checks` 因此保持绿。同时按 AC7 补一条断言：`"gbt7714" not in ZH_EXTRA_CHECKS`。

## 7. `gateEligible` 规则（TPR-03）

唯一的阻断资格判据。一个检查项进入 gate 阻断候选集，当且仅当三条全部满足：

| 判据 | 含义 |
|---|---|
| G1 有明确规范依据 | 能指到学校模板或国标条款 |
| G2 对当前模板必需 | 模板未把该项标为"可省"或"条件项" |
| G3 可确定检测 | 检查器产出确定性失败态，不是提示或警告 |

逐项裁定：

| 检查项 | G1 | G2 | G3 | gateEligible |
|---|---|---|---|---|
| `spec`（规范终检失败项） | ✓ | ✓ | ✓ | **是** |
| `blind`（作者信息可识别） | ✓ | ✓ | ✓ 静态检测，确定性 | **是** |
| `consistency` | ✓ | ✓ | ✗ 状态只有 `PASS` / `WARNING`（`check_consistency.py:237`、`:304`） | **否** |
| 附录存在性 | ✓ | ✗ `templates/yanshan.md:53` 标"（可省）" | ✓ | **否** |
| 符号表存在性 | ✓ | ✗ `templates/pkuthss.md:25`、`:106` 标"条件项、非必备章节"；`yanshan.md:52` 标"（可省）" | ✓ | **否** |
| `abstract` / `conclusion` / `literature` / `tables` | ✓ | ✓ | ✗ 质量类 | **否** |

不合格项一律留在报告层，不进 gate，也不进 `VENUE_CONFIG["thesis-zh"]["extra_checks"]`——后者的未命中文案是 `"Not found — required for {VENUE} submission"`（`audit.py:2213`-`:2221`），会把可选章节标成必需项。

`blind` 的 gate 决策在此直接定为**是**，依据是 `blind_review.py --check` 当前就是确定性静态作者信息检测，不推迟到实现阶段再定。

## 8. 语言轴与 venue 轴分工

| 轴 | 作用 |
|---|---|
| `lang == "zh"` | 决定**可用性**：这些检查器只能处理中文正文 |
| `fmt` | 决定**格式适用性**：见 §2 的 `.typ` / `.pdf` 规则 |
| `--venue thesis-zh` | 决定**严格度**：`spec` / `blind` 的失败项在 gate 下升为阻断 |

`pseudocode` 的 IEEE 降级条目已删除——该检查在 zh 下整体抑制（§1），不存在降级场景。

不引入第四个开关。`--venue thesis-zh` 而 `lang == "en"` 的组合仍走 en 检查集，只应用严格度调整。

## 9. 输出解析与退出码（TPR-02、TPR-06）

### 9.1 退出码语义收紧

现状（`audit.py:2528`-`:2545`）：只有 `returncode == -1` 生成错误项；其余分支按 `stdout.strip()` 是否非空二分，空则打印 `clean`。未知参数导致 argparse 退出码 2 且 stdout 为空时，失败被报成无发现。

改为：

| 条件 | 行为 |
|---|---|
| `returncode == -1`（启动失败/超时） | 生成 `Check script failed` 错误项（保持现状） |
| `returncode != 0` 且无可解析输出 | **生成错误项**，消息含 returncode 与 stderr 前 200 字符；不打印 `clean` |
| `returncode != 0` 但 adapter 成功解析出 issue | 正常并入，附加一条 `Minor` 提示说明退出码非零 |
| `returncode == 0` 且输出可解析 | 正常并入 |
| `returncode == 0` 且输出为空 | `clean` |

### 9.2 module 到评分维度的映射

`_parse_script_output` 用 `check_name.upper()` 作 module 名。`scholar_eval.MODULE_DIMENSION_MAP`（`scripts/scholar_eval.py:65`）现有 14 键，不含新键；边界规范的错误矩阵写明未知模块被忽略（`paper-audit-boundary-contracts.md:53`）。

采用 Route 的第一方案——**扩展稳定映射**，不做别名伪装：

| 新 module | 维度 | 理由 |
|---|---|---|
| `SPEC` | `presentation` | 规范终检属格式呈现 |
| `BLIND` | `ethics` | 匿名化属学术规范 |
| `ABSTRACT` | `clarity` | 摘要结构属表达清晰度 |
| `CONCLUSION` | `soundness` | 结论可靠性属论证健全度 |
| `LITERATURE` | `literature_grounding` | 直接对位 |
| `TABLES` | `presentation` | 三线表属格式呈现 |

`check_style_zh.py` 走 `sentences` 键 → module `SENTENCES` → 已映射 `clarity`，不需新增。

同步项，缺一不可：

1. `tests/skills/paper_audit/test_literature_search.py:578` 的 `MODULE_DIMENSION_MAP == {...}` 是**精确相等锁**，必须同步补齐 6 键。
2. `.trellis/spec/academic-writing-skills/paper-audit-boundary-contracts.md:53` 的错误矩阵行补一句：新增 audit module 必须先入映射再上线。
3. **不改** 8 个基础维度与权重。
4. **去重计分**：同一 finding 只归属一个 module，不得同时计入两个维度。adapter 产出时即固定 module，后续 consolidation 不重新归类。
5. **fail-closed**：新增一条测试，构造一个不在映射内的 module 名，断言 guard 断言失败（而不是静默按 0 分处理），使"新模块未登记"成为可见的红。

### 9.3 severity 映射

各 adapter 把脚本自有的 severity 词汇映射到 `AuditIssue` 既有档位，按 `.trellis/spec/academic-writing-skills/paper-audit-boundary-contracts.md` 的既有 severity 契约执行，不新增档位。`check_style_zh.py` 的 `Info` / `Warning` 分别映射到 `Minor` / `Major` 之外的既有档位由 adapter 单独登记，映射表进测试。

不改 `latex-thesis-zh` 脚本的输出格式（它们有各自的测试与 `tests/contracts/test_writing_modules_alignment.py` 的哈希约束）。

## 10. 兼容性与回滚

| 项 | 影响 |
|---|---|
| `_resolve_script` 签名 | 不变；4 处既有测试与 1 处 monkeypatch 保持有效 |
| `_load_bibliography_content` 签名 | 不变；`test_literature_search.py:484` 保持有效 |
| `MODE_CHECKS` | 不改 |
| `ZH_EXTRA_CHECKS` | **保持 `list[str]`**，只扩内容并删 `gbt7714`；`test_paper_audit.py:419`-`:422` 保持绿（TPR-11） |
| `MODULE_DIMENSION_MAP` | 增 6 键；`test_literature_search.py:578` 的相等锁必须同步（TPR-06） |
| `run_polish_precheck` | 不改代码；zh 行为经 `_resolve_script("sentences", ...)` 的覆盖自动变更为 `check_style_zh.py`，需专门测试证明（AC2-2） |
| EN 侧 `bib` 检查 | 首次收到真实 `.bib`，会产出此前不存在的 finding。既有 EN 测试期望值可能需更新，属预期结果 |
| issue schema / severity 档位 / 8 个基础维度与权重 | 不变 |
| `latex-thesis-zh` / `latex-paper-en` 脚本 | 零改动（AC6 用 `git diff --stat` 验证） |

回滚点：本子任务的改动集中在 `audit.py` 的 4 个区域（`script_map` / `ZH_EXTRA_CHECKS` / `_resolve_script` 及新包装 / `run_audit` 的 tasks 构造），可按区域分次提交，任一区域可独立 revert。
