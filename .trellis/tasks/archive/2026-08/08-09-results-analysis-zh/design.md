# Design — latex-thesis-zh 实验结果分析深度审查能力（父任务实施蓝图）

> 定位：**实施蓝图**。子任务实现以本文件为依据；子 1 交付 guide 后，运行时 LLM 判据
> 权威移交 guide，冲突时以 guide 为准并在本文件"变更记录"节回写。
> 原文权威：`research/user-spec-results-analysis.md`；外部佐证：`research/best-practices-web.md`。
> 2026-08-10：按 Codex 审阅修订（P1×5、P2×3 全部采纳，见 prd 审阅记录）。

## 1. 变更面与边界

| 文件 | 动作 | 子任务 |
| --- | --- | --- |
| `references/writing/results-analysis-guide-zh.md` | 新建（运行时判据权威） | 子 1 |
| `references/modules/experiment.md` | 追加 RA-* 表 + guide 路由；B3/B4/B5 语义不变 | 子 1 |
| `docs/resource-manifest.json` + en/zh 资源页 | 联动 | 子 1 |
| `scripts/analyze_experiment.py` | 新增 `--results-analysis` + RA-* | 子 2 |
| `SKILL.md`、`references/modules/routing-rules.md` | experiment 行/条目 + 歧义速判 | 子 2 |
| `evals/evals.json`、`trigger_eval.json` | 追加用例 | 子 2 |
| `tests/skills/latex_thesis_zh/`（新文件 + fixtures） | 新建 | 子 2 |
| 可能：`tests/contracts/test_defensive_ai_rhetoric_contract.py` | 仅当锁覆盖被改区段 | 子 1 |

不动：`deai_check.py`、`parsers.py`/`tex_loader.py`、B3/B4/B5 与 E-* 逻辑、M-* 方法叙述
检查与 `method-description-guide-zh.md`（只互链）、EN/Typst 副本、justfile 与构建配置。

基线声明（2026-08-10）：method-desc 任务树已实施归档——
`method-description-guide-zh.md` 与 `.trellis/spec/academic-writing-skills/method-narrative-contract.md`
已存在，本设计以其为既成基线；实现前必读后者确认 M-*/RA-* 分界不越界。

## 2. 泛化闸门与证据分级映射（spec → guide 转写规则）

三分类同前：核心机制（域中立判据全部进 guide 正文）；可选适配层（生成/增强类章节保真度
整节，声明适用条件）；示例层（R2R、PFG-CDM、水泥论文书名只作示例注）。
核对程序：guide 完稿后逐节对照原文产出 `research/spec-mapping.md`（每条 spec 判据 →
guide 落点或互链目标），无损才算过。

**证据分级映射（新增，修复基线过时）**：仓库现已有两套分级，必须分工互链、不得重复：

| 维度 | method-description-guide §六（四级主张表） | results-analysis-guide §证据阶梯（五级） |
| --- | --- | --- |
| 视角 | 主张类型 → 所需证据（写方法收益时选措辞） | 证据等级 → 可写内容 + 谓词（写结果解释时定级） |
| 映射 | 定义事实 ≈ 结构事实；机制级作用 ≈ 结构事实→一致性解释；经验性能 ≈ 图表事实 + 组件贡献；因果归因 = 因果归因 | 同左（表格双向给出） |

guide 证据阶梯节开头声明："方法章按主张类型选证据用四级表；结果章按已有证据定措辞用
五级阶梯"，附上表并互链 `method-description-guide-zh.md` 与 `over-claim-guard.md`，
词表与合规示例不复述。

## 3. RA-* 判据定义（脚本实现依据）

### 3.0 公共约定

- 新 CLI 旗标 `--results-analysis`，与 `--per-chapter`、`--section`、`--generate` 正交；
  不改默认模式与 `--per-chapter` 输出。
- **段落对象（修复 P1-5）**：`{start_line, raw_text, visible_text}` 三元组。以空行分隔
  raw 行块；`visible_text` 由逐行 `extract_visible_text` 拼接。`\ref{fig:`/`\ref{tab:`
  探针一律查 `raw_text`（extract_visible_text 会剔除 `\ref`）；语言词面探针一律查
  `visible_text`。
- **RA 专用指标词表（修复 P1-5）**：`RA_METRIC_TERM_RE = METRIC_TERM_RE 词集 ∪
  {KS, W1, MMD, SWD, C2ST, ACF, PSD, AUC}`（独立常量，负向断言 `(?<![A-Za-z])...(?![A-Za-z])`
  同现有写法）。不修改 `METRIC_TERM_RE`（E-METRIC 行为不变）。
- **区间收集算法（修复 P1-2）**：
  1. 逐章通道：`chapter_ranges()` 遍历正文章（`NON_METHOD_CHAPTER_RE` 排除），取
     `EXP_SEC_RE` 命中的二级节区间，记录所属章区间（章级窗口供证据线索查询）。
  2. 全局通道：`split_sections()` 取键名匹配 `^(discussion|result)(_\d+)?$` 的全部区间
     （含 `_N` 后缀族）。
  3. 去重合并：全部候选按 `(start, end)` 排序；两区间行区间重叠即视为同一区间，保留
     逐章通道版本（因其带章上下文），丢弃全局通道重复项。
  4. `--results-analysis --section X`：只取 `^X(_\d+)?$` 后缀族区间，不做逐章收集；X 经
     `SECTION_KEY_ALIASES` 归一化。
  5. 章级窗口定义：逐章通道区间 = 所属章全行；全局通道区间（未被去重合并的）= 该区间
     自身（无章上下文时线索查询窗口即区间本身，宁缺勿越章）。
- **输出定性（审阅接口建议）**：所有消息模板为
  `[Script] RA-XXX（启发式线索，须 LLM 按证据阶梯复核）：...`；guide 与 routing-rules
  中明确 RA-* 不是 R-* 清单的覆盖实现。
- 词表/阈值为模块级常量，登记 guide §阈值与出处。

### 3.1 检查项

最终运行时检查族固定为以下八项。

**RA-EQUIV（Major/P1）等价断言无检验线索**
- 触发：区间 visible 命中 `统计(上)?等价|与.{0,8}等价`；且章级窗口无
  `等价检验|等效性检验|TOST|等价包络|等价界`。
- 排除：`等价类|等价变换|等价形式|等价转换|等价于下式` 数学用语。

**RA-CAUSAL（分档，修复 P1-4）越级因果归因**
- 谓词：`主要归因于|归功于|保证了|确保了|由[^，。]{1,12}(带来|贡献|驱动)|(提升|改善|增益)(完全|全部|均)?来自`。
- 组件证据线索：`ABLATION_RE` ∪ `组件记录|中间输出|逐项(移除|添加)|受控对比`。
- 分档判定（谓词句所在段 ±1 段为"段级窗口"）：
  - 段级窗口内有组件证据线索 → 不报（局部绑定成立，句级实质判读交 LLM）。
  - 段级窗口无、章级窗口有 → **Minor/P2**：报"章内存在组件证据但未绑定到该论断对象，
    须 LLM 核对归因对象与证据是否同指"。
  - 两级窗口均无 → **Major/P1**。
- 排除：一致性谓词 `与.{0,12}(一致|相符)|支持.{0,12}关联` 永不触发；`归因分析|误差归因`
  名词用法不触发。
- 与 defensive-ai-rhetoric 契约分界（代码注释 + guide 双写）：本检查只做"单句因果谓词 ×
  窗口内组件证据线索"的词面组合；"多机制堆叠 + 逐项无证据 + 末句撤回"的防御性推测解释
  仍为 C 档 llm-only，不在任何脚本新增正则或阈值。

**RA-SECONDBEST（Minor/P2）缺次优比较**
- 触发：区间 visible 同时有对比语境（`基线|对比方法|各(模型|方法)`）与最优断言
  （`最优|最低|最高|优于`）；且无 `次优|第二|仅次于|次佳|最接近的(基线|方法)`。
- 防误报：区间可见行 < 8 不检；区间 raw 无 `\ref{tab:` 不检。

**RA-SHALLOW（Minor/P2）浅层图表描述**
- 触发：段落 raw 含 `\ref{fig:` 且 visible 命中
  `更(加)?贴合|更(加)?吻合|基本一致|基本吻合|箱体更小|曲线更(平滑|接近|贴近)|效果(更|较)好|明显(更|较)好`；
  且同段 visible 无 `\d` 且无 `RA_METRIC_TERM_RE`。

**RA-DISTVOCAB（Minor/P2）箱线分析缺主体/尾部词汇**
- 触发：段落 visible 含 `箱线|箱型|箱式`；且该段与后一段 visible 均无
  `中位数|四分位|上须|下须|离群|尾部|最大(绝对)?误差`。

**RA-UNIVERSAL（Info/P3）全称优势断言**
- 触发：`(在)?(所有|全部|各项|全体)(指标|子集|工况)(上|中)?(均|都|皆)?(优于|领先|最优)|全面(优于|领先)|一致优于`。
- 防误报：句内含 `除|但|然而|反转|并未` 让步/转折不报。定性：needs-verify 线索（对照
  表格核对排序反转的 LLM 入口）。

**RA-STAGE（Info/P3，保真度门控；修复 P1-3）评价对象命名混用**
- 门控：章级窗口命中 `RA_METRIC_TERM_RE` 中保真度子集（KS/W1/MMD/SWD/C2ST/ACF/PSD）
  ≥ 2 种才激活。
- 触发：同一区间内，词组 A（`选定集|筛选后`）与词组 B（`生成样本|原始候选|合成样本`）
  **各自出现在至少一个陈述句**且不在同一句。
- 规范性语境排除（关键修复）：句内含 `不得|不能|避免|不应|应统一|简称|外推|区别于|
  不同于|注意` 的句子**不计入**并存统计——spec 合规写法本身就要求写"选定集不得简称为
  生成样本并外推到原始候选池"，这类声明句是合规证据而非混用证据。
- 定性：一致性线索，提示核对标题/表/图/正文同名同对象。

**RA-TRANSITION（Info/P3）章末无实验接口**
- 触发：结果分析区间最后可见段无
  `下一(章|节|小节)|后续(实验|章节)|第[0-9一二三四五六七八九]+章|[0-9]\.[0-9]+ ?节|据此`。
- 避让：所属章存在 `小结` 节时本项静默（不与 method-chapter-guide §六启下句口径双报）。

**已裁决候选：RA-INTERLEAVE**
- 子 2 的 PDF-TXT proxy 标定中 4/4 次命中均由分页、表格行或原段落边界丢失造成，已从
  脚本、公开路由与双语资源删除，不属于运行时检查族。
- 合成正例仅作为“不得再次命中”的回归样例；真实 LaTeX 论文效果仍为
  `UNVERIFIED / missing evidence`。

### 3.2 防误报红线（检查器不得报）

1. 一致性谓词（证据阶梯第三级）不触发 RA-CAUSAL。
2. 因果谓词段级窗口内有组件证据线索 → 不报；章级有段级无 → 只降档报 Minor，不报 Major。
3. 规范性/否定语境句（不得/避免/应统一/简称/外推等）不计入 RA-STAGE 并存统计。
4. 无保真度指标词门控的章节，保真度族全部静默。
5. 数学用语"等价类/等价变换"不触发 RA-EQUIV。
6. 无对比语境或无表引用的小节不报 RA-SECONDBEST。
7. "接近参照/上界内/区间内/描述性记录"规范结果术语不是任何 RA-* 触发词。
8. 沿用 method-chapter-guide 红线：无显著性检验/无均值±方差不报；"人工经验"基线合法。
9. 本章小结存在时 RA-TRANSITION 静默。
10. 同一物理区间经双通道收集必须去重，禁止重复报告（P1-2）。

### 3.3 R-* ↔ RA-* 映射（guide 收录；RA 为线索非覆盖）

| spec 清单项 | 脚本线索 | LLM 判读 |
| --- | --- | --- |
| R-NUMERIC | RA-SECONDBEST | 百分比复算、逐指标次优点名 |
| R-CRITERION | RA-EQUIV | 判据三分、端点方向逐行核对 |
| R-REVERSAL / R-COMPETING | RA-UNIVERSAL | 对照表格核对交叉结果 |
| R-LOCALIZE / R-DISTRIBUTION | RA-SHALLOW / RA-DISTVOCAB | 误差位置与主体/尾部实质判读 |
| R-STAGE / R-BATCH | RA-STAGE | 标题/表/图/正文同名核对 |
| R-CAUSALITY / R-MECHANISM | RA-CAUSAL | 证据阶梯逐项定级 |
| R-TRANSITION | RA-TRANSITION | 接口句实质性判断 |
| R-PROTOCOL / R-TITLE / R-FIGSEM / R-TABLE-VISUAL / R-SCOPE / R-UTILITY | 无 | 纯 LLM 检查项 |

## 4. 契约与兼容性

- **method-narrative-contract.md（新增基线）**：实现前必读；M-*（方法叙述）与 RA-*（结果
  分析）作用区间不同（方法/设计节 vs 结果分析区间），词表不得交叉复制；若该契约锁定
  guide 互链格式，按其执行。
- **defensive-ai-rhetoric**：同前版；RA-CAUSAL 分界注释双写（代码 + guide）。
- **over-claim-guard**：互链不复制词表。
- **router 锁**：SKILL.md 只改 experiment 行与 Reference Map；提交前跑 contracts 测试。
- **双语文档**：guide sourceLocale=zh；experiment.md 改动更新散列 + 双页面。
- **版本**：version 保持与 pyproject 一致，仅 last_updated（由后归档子任务统一改）。
- **回归面**：默认模式与 `--per-chapter` 既有测试原样通过。

## 5. 数据流

```text
main.tex → assemble() → chapter_ranges()/split_sections()
  → 区间收集（逐章 EXP_SEC_RE ∪ 全局 discussion/result 后缀族）→ (start,end) 重叠去重
  → 逐区间：段落三元组切分 {start_line, raw, visible}
  → RA-* 词面组合判定（段级窗口 ±1 段；章级窗口 = 所属章或区间自身）
  → _format_issue()（源文件:行号）
  → % EXPERIMENT (loc) [Severity] [Priority]: [Script] RA-…（启发式线索，须 LLM 复核）
```

## 6. 权衡记录

- 独立旗标而非并入 `--per-chapter`：回归风险最低；路由文档写清两命令分工。
- RA-* 与 R-* 编号分离：避免"脚本已覆盖清单"错觉；映射表显式分工。
- RA-CAUSAL 三档而非二档：章级证据存在时静默会产生系统性假阴性（审阅 P1-4），全报
  Major 又会淹没真阳性；降档 + 绑定提示是折中。
- RA-STAGE 用语境排除而非放弃：合规声明句是可词面识别的（规范性标记词封闭集），保留
  检查价值；若真实语料标定仍误报，子 2 有权降为纯 LLM 检查项（裁决进 guide）。
- 不做百分比自动复算：需表格数值解析联动，误报面大；LLM 必查项。
- 保真度族只做 RA-STAGE 一项脚本线索：其余判据依赖表格语义，词面不可判。

## 7. 效果证据口径（修复 P2-6）

- 合成 fixture 只证明**样例契约与回归行为**，不证明真实效果。
- 真实论文上的查准率/召回率在两子任务归档时一律标 **UNVERIFIED / missing evidence**；
  R8 标定报告只记录"命中数/人工判定误报数"的当次观察，不外推。
- 对外文档（guide、routing-rules）不得出现"已验证/准确识别"类效果声明。

## 8. 回滚

新旗标不进默认路径。改动收敛面同 §1 表；任一子任务失败按其提交序逆向 revert，另一子
任务不受影响（子 1 文档层与子 2 脚本层无共享文件——experiment.md 归子 1，SKILL.md/
routing-rules 归子 2，唯一衔接是子 2 完成后回核子 1 的 RA 映射表文字，若需改动由子 2
提交）。

## 变更记录

- 2026-08-09 初版。
- 2026-08-10 按 Codex 审阅修订：区间收集算法（后缀族 + 去重 + --section 语义）、段落
  三元组、RA_METRIC_TERM_RE、RA-CAUSAL 三档、RA-STAGE 规范性语境排除、启发式定性
  统一、证据分级映射、效果证据口径、method-narrative-contract 基线。
- 2026-08-10 子任务 2 标定收口：RA-INTERLEAVE 因 4/4 次 PDF-TXT proxy 命中均为提取
  结构误报而裁掉；最终运行时检查族为八项。
