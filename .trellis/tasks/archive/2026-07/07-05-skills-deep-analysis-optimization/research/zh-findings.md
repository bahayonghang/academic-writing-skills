# Research: latex-thesis-zh 深度审计发现

- **Query**: 深入分析 latex-thesis-zh skill 现存问题，重点是 2026-06-20 后新增且未独立审计的代码（ChineseAITraceChecker、英文摘要区域门控时态检测）
- **Scope**: internal
- **Date**: 2026-07-05
- **约束遵守**: 未重复 F1-F24 已修结论；未把 parsers.py 有意副本差异当 bug

## 汇总表（按严重度）

| 编号 | 严重度 | 位置 | 一句话 |
|---|---|---|---|
| ZH-1 | **high** | `scripts/deai_check.py:774-791` | 英文摘要区域检测漏掉 thuthesis(`abstract*`) 与 pkuthss(`eabstract`)，时态检查在两大旗舰模板上静默失效；代码注释把 thuthesis 中文摘要环境写错成 `cabstract` |
| ZH-2 | medium | `scripts/deai_check.py:778-782` | 多个 `\begin{abstract}` 环境只取第一个，中文在前、英文在后的第二个摘要被漏检 |
| ZH-3 | medium | `tests/test_deai_tense.py` | zh 版 `_check_tense`/`_english_abstract_range` 零测试覆盖；无任何 fixture 演练摘要环境，ZH-1/ZH-2 因此长期未被发现 |
| ZH-4 | low-medium | `references/modules/deai.md`, `references/deai/guide.md`, `SKILL.md` | 时态检查器在用户可见文档中完全无记载，`tense-guide-zh.md` 成孤儿文件；路由 agent 无从得知该功能存在 |
| ZH-5 | low | `scripts/deai_check.py` 全部中文正则 | 繁体字变体不检测（仅简体）；学位论文多为简体，影响小，属已知局限 |

各维度结论：脚本正确性=发现 ZH-1/ZH-2；GB/T 7714 合规=**未发现问题**；模板适配=ZH-1（核心）；SKILL契约/references漂移=ZH-4；测试盲区=ZH-3/ZH-5；红线合规=**未发现问题**。

## Findings

### ZH-1 [high] 英文摘要区域检测在 thuthesis / pkuthss 上静默失效

**位置**: `scripts/deai_check.py:774-791` `_english_abstract_range()`

**证据（已实测）**: 用三种模板真实摘要结构跑 `deai_check.py --fix-suggestions`：

| 输入 | 英文摘要环境 | 时态命中 |
|---|---|---|
| thuthesis | `\begin{abstract*}`（中文用 `\begin{abstract}`） | **无**（功能 no-op） |
| pkuthss | `\begin{eabstract}`（中文用 `\begin{cabstract}`） | **无**（功能 no-op） |
| generic ctexbook | 明文 `\begin{abstract}` 含英文 | 正常命中 `shows`/`outperforms` |

根因：区域正则只认

```python
m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", self.content, re.DOTALL)  # 分支1
m = re.search(r"\\(?:chapter|section)\*?\{\s*Abstract\s*\}", self.content)            # 分支2
```

- thuthesis 的中文摘要正是明文 `\begin{abstract}`（见 `templates/thuthesis.md:59-65`），英文摘要是 `\begin{abstract*}`。分支1 精确匹配把**中文摘要**识别为"英文摘要区域"，随后 `_is_english_line` 过滤掉中文行 → 零命中，真正的 `abstract*` 英文摘要从不被检查。
- pkuthss 中文=`cabstract`、英文=`eabstract`，两者都带前缀，分支1 完全不匹配；分支2 也没有 `\section{Abstract}` → 返回 None → 整体 no-op。
- 只有当明文 `\begin{abstract}` 里恰好是英文时才生效——而这正是 thuthesis 里的中文摘要位置。

**注释与事实不符**: `deai_check.py:378` 与 `tone-thresholds.yaml:89-90` 注释称"thuthesis 中文摘要是 `\begin{cabstract}`，已排除"。事实上 `cabstract` 是 pkuthss 的中文环境；thuthesis 中文摘要是明文 `abstract`、英文是 `abstract*`（`templates/thuthesis.md`、`parsers.py:429-453 extract_abstract` 也印证 thuthesis 走明文 `abstract`）。开发者混淆了两模板的环境名。

**无误报风险**（仅漏检）：thuthesis 场景区域指向中文摘要，`_is_english_line`（`deai_check.py:793-798`）按行门控过滤中文，不产生假阳性，只是彻底漏掉英文摘要。

**次生影响**: thuthesis/pkuthss 的摘要是**环境**而非 `\chapter`/`\section` 标题，不进 `split_sections`，因此 overclaim 等 section 级检查也不覆盖英文摘要；叠加 tense 漏检，thuthesis 英文摘要基本得不到任何英文专项去AI检查。

**建议修复方向**: 区域正则同时匹配 `\begin{abstract*}`（thuthesis 英文）与 `\begin{eabstract}`（pkuthss 英文）；当中文明文 `abstract` 与英文 `abstract*` 并存时，优先选带星/英文环境；修正 `deai_check.py:378`、`tone-thresholds.yaml:89-90` 的错误注释。

### ZH-2 [medium] 多个 abstract 环境只取第一个

**位置**: `scripts/deai_check.py:778-782`

**证据（已实测）**: 两个明文 `\begin{abstract}`（第一个中文、第二个英文）时，`re.search` 非贪婪只命中第一个（中文）区域，第二个英文摘要漏检，时态零命中。

某些工程用两个明文 `abstract` 环境分置中英文摘要，此时英文摘要被系统性漏检。与 ZH-1 同一函数、同一根因（区域检测未枚举全部候选、未按语种择优）。

**建议修复方向**: 枚举所有 `abstract`/`abstract*`/`eabstract` 候选区间，用 `_is_english_line` 占比选出英文那一个，而非首个匹配。

### ZH-3 [medium] zh 版时态检查零测试覆盖

**位置**: `tests/test_deai_tense.py`

**证据**: 该文件（92 行）全部导入 **latex-paper-en 的 `AITraceChecker`**（section 门控 Methods/Results），文件头注释自承"the zh copy gates to the English-abstract region instead of method/result sections (see that skill's own behavior)"——但**没有任何测试实际演练 zh 的 `ChineseAITraceChecker._check_tense` / `_english_abstract_range`**。全仓 grep（tests/ + evals/）无一处 fixture 含 `\begin{abstract}`、`abstract*`、`eabstract`、`cabstract`。ZH-1/ZH-2 正是因此从未被测试捕获。

**建议修复方向**: 为 zh 版补 tense 测试，覆盖 thuthesis(`abstract*`)、pkuthss(`eabstract`)、明文英文 `abstract`、双 abstract、中文摘要不误报 五种结构。

### ZH-4 [low-medium] 时态检查器在用户可见文档中无记载

**位置**: `references/modules/deai.md`、`references/deai/guide.md`、`SKILL.md`

**证据**:
- `references/modules/deai.md` 章节为 Core Principles / Humanization Contract / High-Priority AI Patterns / AI Density Scoring / Edit Types——**无时态、无 overclaim**。
- `references/deai/guide.md` 仅在 `:128` 提及 over-claim-guard，**未提时态**。
- `SKILL.md` 的 deai 行（`:90`）与路由（`:114`）只讲 `--tier`/D1-D5，从不提 tense/英文摘要。
- `references/writing/tense-guide-zh.md` 存在，但只被 `tone-thresholds.yaml` 注释与 `deai_check.py` 的 instruction 字符串引用，**未从任何模块文档链接** → 孤儿文件。

后果：路由 agent 读 deai.md 无从得知时态检查存在，也不知其只作用于英文摘要——功能不可发现。（over-claim-guard 已被 guide.md 正确链接，可作为对照修法。）

**建议修复方向**: 在 `references/modules/deai.md` 补时态检查段落并链接 `tense-guide-zh.md`，说明仅英文摘要区域生效；SKILL.md deai 描述补一句。

### ZH-5 [low] 繁体字变体不检测

**位置**: `scripts/deai_check.py` 全部中文正则（EMPTY_PHRASES / OVER_CONFIDENT / term_thresholds 等）

**证据（已实测）**: `顯著`×6（繁体）零命中，`显著`（简体）才会计数。模式全简体。中国大陆学位论文一律简体，实际影响很低，建议作为显式局限记录而非必修。

## 未发现问题的维度（明确记录）

- **GB/T 7714 合规逻辑**：`verify_bib.py:237-412` 的 2015 与 2025 分支分离干净、无互相污染。2015 额外提示"非电子文献著录 url 需补 urldate"（`:278-291`，`self.standard=="gb7714"` 门控），2025 取消该要求并新增 preprint/dataset 提示（`:395-412`）；电子文献 urldate 两版皆要求（`:265-274`），符合国标。`--standard` choices=`default/gb7714/gb7714-2025`（`:441`）一致。
- **红线合规**：deai_check.py 只读，通过 `extract_visible_text`（parsers.py `PRESERVE_PATTERNS`）把 `\cite/\ref/\label/\eqref/\autoref/$...$/equation/align` 挖空后再匹配，从不改写源；deai_batch.py 仅在被标记行**上方插入 `% 去AI化:` 注释行**，原行逐字保留（`:220-234`），不触碰 cite/ref/math 内部。无红线改动风险。

## Caveats / Not Found

- 全角/半角标点：throat_clearing 模式已含 `[,，]`（如 `^首先[,，]`），全角逗号已覆盖；未发现全角标点相关缺陷。
- 多文件工程行号：`_english_abstract_range` 基于 assemble 后的 `self.content` 计行，与 `self.lines` 一致；`\include` 分离摘要时定位仍正确，未发现偏移。
- 本次聚焦新增代码 + 模板适配；未逐行复核 analyze_logic.py(45K)、check_tables.py 等 F1-F24 覆盖过的旧脚本。
