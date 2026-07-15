# 投稿信预提交规则

`presubmission_check.py` 的确定性规则。改编自 `paper-audit/references/PRE_SUBMISSION_RULES.md`，添加了特定于投稿信的内容并删除了仅限 LaTeX 源代码的规则。

## 禁止的 AI 音模式 (G4-AI\*)

每项阶梯：**相同**项出现 2 次为 `minor`，出现 3 次以上为
`major`。 （以前，一个术语出现次数低于 3 次时不发音，因此词汇多样化
草稿中使用过的每个促销词都被完全漏掉了——参见 `AI-DIV`
如下。）继承自论文审核规范列表。

```python
BANNED_TONE_PATTERNS = (
    ("AI1", r"\binnovative\b"),
    ("AI2", r"\bpioneering\b"),
    ("AI3", r"\brevolutionary\b"),
    ("AI4", r"\btransformative\b"),
    ("AI5", r"\bbreakthrough\b"),
    ("AI6", r"\bunprecedented\b"),
    ("AI7", r"\bremarkable\b"),
    ("AI8", r"\bsuperior\b"),
    ("AI9", r"\bsurpass(?:es|ed|ing)?\b"),
    ("AI10", r"\bstate[- ]of[- ]the[- ]art\b"),
    ("AI11", r"\bhighlights? the potential of\b"),
    ("AI12", r"\bpaves? the way\b"),
    ("AI13", r"\bprofound challenges?\b"),
    ("AI14", r"\bat its essence\b"),
)
```

## 投稿信特定的开场陈词滥调（L2）

在信函正文的第一行非空行（称呼后）触发：

```python
LETTER_OPENER_CLICHES = (
    r"^\s*we are (?:pleased|excited|delighted|honored) to (?:submit|share)\b",
    r"^\s*we hereby submit\b",
    r"^\s*please find (?:enclosed|attached)\b",
    r"^\s*it is our (?:great )?pleasure to submit\b",
    r"^\s*enclosed please find\b",
)
```

严重性：`minor`。这些开头表明这封信对顶级期刊的编辑来说是不费力气的。

## 投稿信特定禁用短语 (J1)

零编辑器信号的营销或人工智能模板语言：

- “新颖、创新”
- “开创性的”
- “史无前例”
- “改变游戏规则”
- “范式转变”
- “前沿”
- “非常感兴趣”
- “将引起广泛的兴趣”
- “这个领域需要”

出现 1 次以上时触发。严重性：`minor`（3+ 时为 `major`）。

## 通用短语 (J4)

`FORBIDDEN_PHRASES.md` 第 4 层：表明作者未阅读的措辞
场地。出现 1 次以上时触发，`minor` / `P3`，每个都有一个“名称
具体的X”替换提示：

- “你的期刊”/“你著名的期刊”→ 为期刊命名
- “适合（很好）范围” → 命名范围尺寸
- “广泛的读者群”→命名读者档案
- “对该领域的重要贡献”→ 命名贡献类别

## 机械规则

| ID | 严重性 | 检查 |
| --- | ----------------- | ------------------------------------------------------------------------------------------------------------------ |
| G1 | `minor` | 读者可见散文中的 Em 破折号（AI 色调表面信号，与 ISSUE_SCHEMA 次要层对齐）。             |
| G2 | `minor` | 段落长度超过 120 个单词或 6 个句子（投稿信比论文短 - 段落上限更紧）。 |
| G3 | `minor` | 段落以弱过渡开始（然而，此外，此外，此外，也）。                         |
| G4 | `minor` / `major` | 相同的禁用 AI 音术语出现 2 次 (`minor`) 或 3 次以上 (`major`)。                                          |
| L1 | `major` / `minor` | 信函超出模板的 `word_limit` ≥20% (`major`) 或最多 20% (`minor`)。                                   |
| L2 | `minor` | 第一个内容行与已知的开场陈词滥调相匹配。                                                                  |
| J1 | `minor` / `major` | 投稿信特定禁止短语出现 (`minor`) 或出现 3 次以上 (`major`)。                               |
| J4 | `minor` | 出现通用匹配措辞（第 4 层）；发出“命名特定 X”替换提示。                             |
| AI-DIV | `minor` / `major` | `minor` 当 3 个**不同**禁止的 AI-tone 术语出现时（每个可能出现一次），`major` 为 4+。捕捉不同的人工智能在每学期 G4 梯子上的失误。 |
| S1 | `minor` | 3 个连续的正文段落以相同的前两个单词标记打开（并行/模板化节奏）。               |
| S2 | `minor` | ≥8 个句子的句子长度变异系数 < 0.25（节奏均匀/突发性低）。 |

## 结构 AI 跟踪检查（AI-DIV、S1、S2）

这三项检查移植了 `latex-paper-en` / 使用的结构 AI-trace 思想
`typst-paper`（deai）进入投稿信类型。它们都是 `minor`/`P2`
AI-DIV 除外，它在 4 个以上不同的术语下升级为 `major`，并且他们报告
只是——没有重写。

阈值是 `presubmission_check.py` 中的固定模块常量
（`AI_TONE_DIVERSITY_*`、`PARALLEL_OPENING_*`、`SENTENCE_UNIFORMITY_*`），不是
每层 YAML：投稿信是一个简短的类型，扫描必须运行
即使没有 `--journal`（因此不存在 `word_limit` 基线）。长度自适应
阈值会添加“没有模板时的基线是什么？”没有真实维度
增益，所以我们选择零误报固定装置的确定性常数
(`evals/fixtures/human_letter.md`) 守卫。

参数（字母域调整与纸面默认值）：

- **AI-DIV** — 计算至少有多少个不同的 `BANNED_TONE_PATTERNS` 开火
一次。与 G4 不同（重复与多样性）；两者都可能对一封信开火。
- **S1（平行开口）** — 3 个连续段落的窗口，打开键 =
前 2 个字令牌（与纸面 `_check_burstiness` 的引脚相同）。这
`Dear …` 称呼段落被跳过；声明段落（“我们确认
…”、“我们声明…”）在 2 个令牌密钥下有所不同，因此它们不会误报。
- **S2（句子长度均匀性）** — 全信（投稿信没有
部分），门控为 ≥8 个句子且 CV < 0.25。纸面默认为
分钟 5 / CV < 0.30 且分级门控；字母样本很短并且简历有噪音，所以
提高门槛，收紧门槛，抑制误报。

未从纸端 deai 结构壳移植：

- **清嗓子的段落开头**——字母类型已经有了对应的内容
（`L2` 开头陈词滥调 + `G3` 弱过渡段落开头）；添加它会
双报。
- **低信息密度** - 投稿信的声明段落是
合法模板化且无证据标记，因此此检查将
≤400 个单词的格式正确的字母出现误报。

## 必需的声明规则 (D-\<kind\>)

由活动模板的 `required_declarations` frontmatter 列表驱动。支票是：

1. 解析模板的 `required_declarations` 和 `optional_declarations` 数组。
2. 对于具有已知探测器的每个 `required_declarations` 商品，扫描信函正文以查找规范措辞之一（见下文）。
3. 如果不存在，则发出带有声明名称的 `major` 结果 (`D-<kind>`)。
4. 对于具有已知检测器的 `optional_declarations`，如果不存在，则发出 `minor` 建议 (`D-<kind>-opt`)。
5. 具有**无**检测器的所需类型会发出信息性 `D-<kind>-unknown`（`minor`/`P3`，“手动验证”），而不是错误的“缺席”专业；没有检测器的可选类型会被静默跳过。

规范短语（正则表达式，不区分大小写）：

```text
originality:
  - not (?:been )?published elsewhere
  - not under (?:concurrent )?(?:consideration|review|submission)
  - original (?:research|work|manuscript)

dual_submission:
  - not (?:currently )?(?:under (?:concurrent )?(?:consideration|submission|review)|submitted)(?:\s+elsewhere)?
  - single submission policy
  - (?:dual|multiple) submission
  - not (?:been )?submitted (?:to|elsewhere)
  - concurrent consideration

competing_interests:
  - (?:no |declare(?:s)? (?:no |the following )?)?competing interests?
  - conflicts? of interest
  - declare(?:s)? no (?:competing|conflict)

data_availability:
  - data (?:will be |are |is )?(?:made )?available
  - code (?:will be |is )?(?:made )?available
  - materials (?:are|will be) available
  - data and code
  - data availability statement

ethics_irb:
  - institutional review board
  - \bIRB\b
  - \bIACUC\b
  - ethics? (?:committee|approval|board)
  - clinical trial (?:registration|number|identifier)
  - informed consent

authorship:
  - all authors (?:have )?approved
  - all authors (?:have )?read and approved
  - authorship agreement

ai_disclosure:
  - generative ai
  - \bgen[- ]?ai\b
  - (?:used|use of|using|employed|with|disclos\w+|assisted by) (?:a |an |the )?(?:large language model|llms?|generative ai|ai (?:tool|assistant|writing))
  - no (?:generative )?ai (?:tool|assistance|was|were|used)
  - ai[- ](?:assisted|generated) (?:writing|text|content|editing)
  - \b(?:chatgpt|gpt-\d|copilot|gemini)\b

prior_presentation:
  - (?:previously |earlier )?(?:presented|published|appeared) (?:as |in )?(?:a |an )?(?:poster|abstract|preprint|workshop|preliminary|short version)
  - \ba (?:preliminary|prior|earlier|conference) version\b
  - \bpresented at\b
  - \bextends? (?:our|a) (?:prior|earlier|previous) (?:conference |workshop )?(?:paper|version)
```

Nature / Science / Cell 模板需要 `ai_disclosure` (ICMJE Jan
2026 第五节；科学在投稿信中明确要求它）。 IEEE/ACM
将 AI 披露放在论文稿件中，因此他们的模板不会列出它。
不带检测器的申报种类（`excluded_reviewers`、
`artifact_evaluation`、`reproducibility_statement`）按上述规则 5 处理。

## 长度检查 (L1)

从模板中读取 `word_limit`。计算可见单词（不包括称呼、地址块、签名）。严重程度阶梯：

- 限制的 0-100%：可以。
- 限制的 100-120%：`minor`。
- 限制的 120%+：`major`。

## 段落形状（G2、G3）

比纸质审核更严格，因为投稿信更短：

- 长段落：>120 个单词或 >6 个句子（相对于论文的 180/8）。
- 弱主题开头：≥60 个单词且≥2 个句子且以弱过渡开头。

## 标题/方程式/标签/引用规则 - 不适用

投稿信不包含 LaTeX 标题、编号方程或标签/参考对。纸质审核的相应规则被故意省略。
