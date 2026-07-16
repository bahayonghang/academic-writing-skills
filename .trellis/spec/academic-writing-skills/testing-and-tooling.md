# 测试与工具链约定

> 来源：07-05-zh-abstract-tense-gating / 07-05-typst-deai-sync 两任务的实现与质检（2026-07-06）。

---

## Convention: zh/typst 副本脚本的测试必须 importlib 按路径加载

**What**：测试 `latex-thesis-zh/scripts/deai_check.py` 或 `typst-paper/scripts/deai_check.py`（以及任何非 EN/AUDIT 的按技能副本脚本）时，必须用 `importlib.util.spec_from_file_location` 按文件路径加载，并在 try/finally 中全量恢复 `sys.path` 与 `sys.modules`。

**Why**：`tests/conftest.py` 把 EN 与 AUDIT 的 scripts 目录放在 `sys.path` 前排，bare `import deai_check` **静默解析到 EN 副本**——测试全绿但根本没测到目标副本（XC-3b；zh/typst 的时态与结构壳逻辑曾因此长期零覆盖）。不对称恢复则会污染后续裸 import 的 EN/AUDIT 测试。

**Example**（canonical 模式，见 `tests/skills/latex_thesis_zh/test_deai_tense_zh.py::_load_zh`，与 cover-letter 测试同源）：

```python
def _load_zh():
    saved_path = list(sys.path)                      # 全量快照
    saved = {m: sys.modules.pop(m, None) for m in ("parsers", "tex_loader")}
    try:
        spec = importlib.util.spec_from_file_location(
            "zh_deai_check", ZH_SCRIPTS / "deai_check.py"   # 命名空间名，勿用 "deai_check"
        )
        module = importlib.util.module_from_spec(spec)
        sys.path.insert(0, str(ZH_SCRIPTS))
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = saved_path                     # 全量恢复
        for name, mod in saved.items():              # 对称还原：缺失则 pop、存在则还原
            if mod is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = mod
```

**Wrong vs Correct**：

```python
# Wrong：解析到 EN 副本，zh 逻辑零覆盖还全绿
import deai_check
checker = deai_check.ChineseAITraceChecker(...)   # AttributeError 或更糟——静默测错对象

# Correct：按路径加载 + 守卫断言确认加载到目标副本
module = _load_zh()
assert hasattr(module, "ChineseAITraceChecker")   # 守卫：不是 EN 的 AITraceChecker
```

**Tests Required**：新测试文件应含一条"加载守卫"用例（断言副本特有类/常量存在），防止加载器改坏后静默退化成 EN 副本。

---

## Convention: 测试路径常量只从 `tests.support.paths` 导入

**What**：测试需要仓库根、skill 根或各 skill 的 `scripts/` 目录时，统一从 `tests.support.paths` 导入：

```python
from tests.support.paths import SCRIPT_DIR_ZH, SKILLS_ROOT

_ZH_DIR = SCRIPT_DIR_ZH
_SKILL_DIR = SKILLS_ROOT / "latex-thesis-zh"
```

**Why**：测试文件已按 `tests/skills/`、`tests/contracts/`、`tests/shared/` 分组；如果继续写 `Path(__file__).parent.parent`，移动一层目录就会把仓库根误算成 `tests/`。`tests/conftest.py` 只负责 pytest 副作用（`sys.path` 顺序、runtime artifact cleanup），不要把它当普通路径模块 import。

**Wrong vs Correct**：

```python
# Wrong：目录层级变动后会指到 tests/，并且把 conftest 当普通模块使用
from conftest import SCRIPT_DIR_ZH
SKILLS_ROOT = Path(__file__).parent.parent / "academic-writing-skills"

# Correct：路径入口稳定，pytest 副作用仍留在 conftest.py
from tests.support.paths import SCRIPT_DIR_ZH, SKILLS_ROOT
```

**Tests Required**：移动或新增测试目录后至少跑：

- `uv run --extra dev python -m pytest --collect-only -q`（根 `tests/` 应保持可收集）
- 目标 skill 的 importlib loader 测试（例如 zh/typst/cover-letter）
- `rg -n "from conftest import|Path\\(__file__\\).*parent\\.parent" tests`（除 `tests/support/paths.py` 外应无命中）

---

## Convention: zh 时态阈值是双层配置，改 pattern 必须两处同改

**What**：`latex-thesis-zh` 的时态信号 pattern 同时存在于 `scripts/deai_check.py` 的 `DEFAULT_THRESHOLDS`（:116 附近）与 `references/deai/tone-thresholds.yaml`（覆盖层）。改任何 pattern（如 `\bpresents\b`）必须两处同步。

**Why**：YAML 是 DEFAULT 之上的覆盖层，**PyYAML 缺失时走 DEFAULT**——只改 YAML 会在无 PyYAML 环境静默回退到旧行为；只改 DEFAULT 会被 YAML 覆盖掉。SH-1 修复时曾差点漏掉 DEFAULT 层。

**Validation**：改完 grep 全仓确认无旧 pattern 残留：`grep -rn "presents?" academic-writing-skills/*/scripts academic-writing-skills/*/references`（应零命中）。

---

## Gotcha: evals.json 禁用 Edit/Write，走 Bash python 写入

> **Warning**：PostToolUse 的 JSON 格式化 hook 会在 Edit/Write 后把 `academic-writing-skills/*/evals/evals.json` 的多行 `files: [...]` 数组压成单行，造成与改动无关的大面积重排。

**Fix**：改 evals.json 一律用 Bash 跑 python 写入（不触发 Edit/Write hook）。**写入前先看目标文件的既有风格**——各技能的 evals.json 风格不统一：

- typst-paper 等：canonical `json.dumps(data, indent=2, ensure_ascii=False) + "\n"` 可 round-trip；
- paper-audit：仓库已接受**压平数组**的紧凑格式（`files`/单条 assertion 各占一行），对它整文件 `json.dumps(indent=2)` 会重排数百行（实测 +479/-91）。此类文件走**文本级拼接**：在关闭 `]` 前 splice 新条目、逐 assertion 用 `json.dumps(obj, ensure_ascii=False)` 内联、保留原换行符（CRLF），写完 `json.loads` 校验 + `git diff --stat` 应为纯增量（参考 07-05-paper-audit-scoring-fixes 收敛到 +24/-0 的做法）。

若已被 hook 重排：`git checkout` 还原后用上式重写，diff 应只剩语义新增（参考 typst-deai-sync 收敛到 +35/-0 的做法）。

**同类陷阱**：SKILL.md 的表格被全局 hook 重新对齐会触发 `ROUTER_ROW_RE` contract 测试——改 SKILL.md 表格后必须跑 `tests/contracts/test_skill_contracts.py`。

---

## Gotcha: paper-audit/SKILL.md 正文标题版本号受 contract 测试跟随 frontmatter

> 来源：07-15-audit-fix-version-ci（2026-07-15）。

**What**：`tests/contracts/test_skill_contracts.py::test_paper_audit_skill_argument_hint_matches_cli_contract` 会从 paper-audit/SKILL.md frontmatter 的 `version` 字段动态提取 `major.minor`，断言正文标题字面等于 `# Paper Audit Skill v{major}.{minor}`。这是六个 SKILL.md 里**唯一**在正文重复版本号的技能——只改 frontmatter（如全仓版本 bump）会让该测试红，且失败信息不会直接指向"正文标题没跟着改"。

**Fix**：改 paper-audit `version` frontmatter 时，同 commit 检查并同步正文标题行；验证走 `uv run --extra dev python -m pytest tests/contracts/test_skill_contracts.py -q`（`test_skill_versions.py` 不检查正文标题，只跑它会漏掉这个坑）。

**Why**：其余五个 SKILL.md 无此重复，版本 bump 时最容易漏改的就是这一个特例。

---

## Gotcha: 别给 pytest 命令加 PYTHONIOENCODING=utf-8

> 来源：07-10-thesis-zh-intro-optimization（2026-07-11）。

**What**：`PYTHONIOENCODING=utf-8 uv run pytest tests/contracts/` 会让
`test_skill_contracts.py` 里 subprocess 跑 `script --help` 的用例炸出
`TypeError: NoneType + str`（reader 线程按 locale/cp936 解码 UTF-8 输出失败，
`result.stdout` 变 None）。该环境变量只用于**重定向 JSON 输出到文件**的场景
（见 yanshan 任务记录），跑 pytest 一律不要加。

**补充**：latex-thesis-zh 的 `evals/evals.json` 是 CRLF + `json.dumps(indent=2,
ensure_ascii=False)` 的 canonical round-trip（typst 同构但 LF）；追加条目走
Bash python 读-改-写全量 dump 即可得到纯增量 diff（07-10 任务实测 +35/-0）。

---

## Gotcha: 检查器适配新结构形态要跑完整输出回归并扫兄弟检查器

> 来源：07-11-thesis-zh-process-chapter（2026-07-12）。

**What**：给 `_check_chapter_intro`（R2）适配“编号引言节”形态（`\chapter` 后直接
`\section{引言}`）后，同文件的 `_check_heading_leads`（S1）仍对同一结构报
“标题后未发现导语段落” Major——只跑目标检查器的单测，看不见兄弟检查器的同型误报。

**Fix**：新结构形态落地时：(1) 用合成 fixture 跑**完整 analyze 输出**做回归断言，
不只跑目标检查器单测；(2) grep 同文件里消费同一结构信号（标题层级/首子内容）的
其余检查器逐个核对。07-11 修法：抽 `_has_numbered_intro_section` 帮助函数，S1 仅
豁免章标题层（下级标题不受影响），`test_chapter_intro_forms.py` 两条守卫用例锁定。

---

## Gotcha: check_format 渲染报告每组截断 10 条，验证与断言走 issues 列表

> 来源：07-12-thesis-zh-method-chapters(2026-07-12)。

**What**:`check_format.py` 的 `generate_report` 对每个 source 组只渲染前 10 条 +
"... and N more"——Major 级命中(如 F-PLACEHOLDER)会被排在前面的 Info 级(如
F-NOTE-HEDGE)挤进截断区,grep 渲染报告会得出"未命中"的错误结论(07-12 实测两次
误判,险些把已正确实现的 F-PLACEHOLDER 当作缺陷返工)。

**Fix**:验证/测试断言一律走 python API 数 `res["issues"]`(按 `code` 字段过滤),
或 JSON 输出;grep 渲染报告只用于人读预览。后续如做"按 severity 排序渲染"的小任务
可根治此坑(已记 memory)。

---

## Convention: 检查器默认行为变化只允许"误报/假绿修复"例外,且须双声明

**What**:latex-thesis-zh 检查器的新增能力默认藏在新 flag 后(默认输出零变化);
**唯一允许改变默认行为的例外是误报修复与假绿修复**(用户已有工作流依赖默认输出,
误报清除与静默失效提示不算破坏)。每处例外必须:(1) 同步更新受影响的存量单测;
(2) 在 commit message 正文显式声明"默认行为变化"及原因。

**Why**:07-11(R2 章引言形态适配)与 07-12(R2 五连修/R3a P-PAPER 默认全章/
R4a analyze_experiment 结构提示)两任务沿用此模式,已成为事实约定;不声明会让
后续会话把行为差异当回归 bug 排查。

**Example**:07-12 的 P-PAPER 从 `--process-chapter` 门后迁到默认管线并逐处报告
(commit cc73b07),存量 P-PAPER 单测同 commit 迁移并在 message 声明。

---

## Convention: latex-thesis-zh 的 BibTeX 解析必须走平衡扫描器

**What**：`latex-thesis-zh/scripts/verify_bib.py` 必须通过技能内的
`bib_scan.parse_bib_entries(content)` 解析条目，并用 `tex_loader.read_text_robust(path)`
读取文件。禁止恢复为 `[^@]` 条目正则或 `[^{}]` 字段正则；这些表达式无法表达 BibTeX
的平衡括号、引号、`@string` 宏和截断条目重同步语义。

**Why**：正则旧实现会静默吞掉值内含 `@` 的后续条目、丢弃含 `^` 或多层花括号的字段，
并把 GB18030 文献库乱码当成无中文条目的 PASS。各 skill 独立安装，不能从
`bib-search-citation` 跨技能 import，因此 zh 侧保留 vendored `bib_scan.py`；修改扫描语义时
须对照 `bib-search-citation/scripts/search_bib.py` 的同名函数，并保留 zh 所需的 warning 映射。

**Tests Required**：运行
`tests/skills/latex_thesis_zh/test_verify_bib_scanner.py`，至少锁定 `^`、值内 `@`、多层花括号、
引号内花括号、未闭合条目 warning+resync、`@comment`/`@preamble` 跳过、`@string` 展开与
GB18030 编码 warning；同时跑既有 gb7714 与 scripts 回归，确认 entry dict 仍为
`type/key/fields/raw`。

---

## Gotcha: 批次拟提交分组遇到跨批次同文件累积 diff 时不能照搬原分组

> 来源：07-15-audit-fix-latex-paper-en（2026-07-16）。

**What**：implement.md 常按 finding-ID 把工作拆成多个批次（G1/G2/...），每批各自登记"拟提交分组"，但按本任务树的约定 Phase 3.4 才统一提交（批内不 `git commit`）。若后续批次改动了前面批次已改过的同一文件（如某批次加别名解析、另一批次在同文件加 assemble 接入），工作树里该文件已是**累积 diff**——原计划的逐批 whole-file `git add` 无法再干净复现（实测：`analyze_logic.py` 被三个不同批次共同触碰，`analyze_literature.py`/`deai_batch.py`/`check_figures.py` 各被两个批次触碰）。

**Fix**：Phase 3.4 不要用 `git add -p` 做 hunk 级手术拆分（风险高、易切错、且这批改动本就不需要"人类考古级"可逐 commit 回溯）。改为按**实际文件重叠边界**重新分组提交（分组数通常比原计划少）：(1) 每个新分组的 commit message 列全它覆盖的原 finding-ID；(2) 原计划里任何"默认行为变化"双声明随文件一起迁入新分组的 message，不能丢；(3) 提交前用"临时移出后续批次专属的文件+测试、重跑套件"的方式验证每个中间提交仍然绿。

**Why**：本任务树全部 8 个子任务共享"批内不提交、Phase 3.4 统一呈报"的约定；只要 implement.md 是多批次计划，批次间文件重叠就几乎必然发生。遇到时按此法直接重新分组，不必重新论证是否该做 hunk 拆分。
