# 中文学位论文术语治理、缩写体例与程度词契约

## 1. Scope / Trigger

维护 `latex-thesis-zh` 的 `check_consistency.py` 可选术语治理与缩写体例、
`check_style_zh.py` 的 `--degree-wording`，以及对应公开指南、示例、路由和合成
fixture 时适用。面向作者的规则由技能内
`references/modules/consistency.md`、`references/modules/expression.md` 与
`references/writing/academic-style-zh.md` 拥有。复制安装后的技能不得依赖本
spec 或私有论文语料。

## 2. Signatures

```text
uv run python scripts/check_consistency.py INPUT
    [--terms] [--abbreviations] [--custom-terms FILE]
    [--governance] [--abbreviation-style] [--json]
uv run python scripts/check_style_zh.py INPUT [--degree-wording] [--json]
```

`--governance` 必须同时给出 `--custom-terms`。它扩展现有 JSON，不新增第二份配置、
schema 版本或迁移层。`zh` / `en` 仍由原同义组路径加载。未启用治理时不读取
`banned`、`locked`、`exempt`。

```json
{
  "zh": [["合成甲", "合成乙"]],
  "en": [],
  "banned": {
    "旧称": {
      "candidates": [
        {"text": "候选甲", "slot": "过程"},
        {"text": "候选乙", "slot": "对象"}
      ]
    }
  },
  "locked": {"标准名": ["旧别名"]},
  "exempt": {"environments": ["localterms"]}
}
```

## 3. Contracts

- 三个新开关默认关闭。不传开关时，consistency 的默认 / `--terms` /
  `--abbreviations` / 旧 `--custom-terms` 输出，以及 `check_style_zh.py` 的默认
  输出，逐字节保持。`--help` 不属于旧输出基线。
- `banned` 每个词至少一条非空 `text`；`slot` 可省略。一次命中列出全部候选和
  slot，不按候选数复制 finding。`locked` 把规范名映射到禁用变体，报告该规范名，
  不按词频推断。`exempt` 只增加环境名，不能取消固定保护。
- 治理与缩写体例扫描装配后的可见文本，并用 origin 回指源位置。屏蔽注释、前导区、
  数学、cite/ref/label 载荷、路径、`verbatim` / `lstlisting` / `minted`、
  `thebibliography` 和用户指定环境。缩略词表只豁免名为 `abbreviation` /
  `abbreviations` / `acronym` 的环境，或标题恰好为 `缩略词表` / `缩略词对照表`
  的区域。普通 table 不整表豁免。不扫描外置 `.bib`，不把题名写入治理候选。
  中文按字面匹配；ASCII 词使用标识符边界。
- 未知自定义宏使覆盖不完整。此时不得宣称没有问题。
- `--abbreviation-style` 独立于 `--governance`。合格首现是句内边界清楚的
  `中文名称（英文全称，缩写）`。中英文逗号都可识别，报告中的项目形式为
  `（英文全称，缩写）`。边界不清只给一条 `NEEDS-LLM` 覆盖说明，不发虚假 XOR。
  缩写可含大小写、数字和内部连字符，合成例使用 `ZX` / `AbX` / `X-2`。
  已登记对之后的 `中文名（缩写）` 或 `中文名 缩写` 才是候选。首次只有
  `中文名（缩写）` 不是合格展开，不发二次结论。完整括注中的 Title Case 只作候选，
  不改写专名大小写。数学括注和 `X 为中文名` 不是 XOR 问题。与旧
  `--terms` / `--abbreviations` 合用时，同位置同类候选去重，不替换旧定义识别器。
  新 JSON 字段只在新模式出现。
- `ChineseStyleChecker` 接受显式 `degree_wording`，默认 `False`。打开后新增
  `极易`、`极低`、`完全忽略`、`高度贴合` 候选，Info/P3，`[Script]`，
  `Meaning-Check: NEEDS-LLM`。`绝对` 只跳过 `绝对误差`、`绝对值`、`绝对温度`、
  `绝对湿度`、`绝对压力`、`绝对坐标` 的命中跨度，不因一处合法搭配跳过整句或其他
  绝对化词。`完全忽略` 若已有 `完全` 候选，该位置只保留一条。沿用引述排除、
  可见文本和章节路由。不提供整句替换，不新增自动替换模板。
- 新发现只报告局部词、字段和位置。无效输入走现有 CLI 错误路径、非零退出，
  不得伪装成零发现或通过结论。既有严重度不批量修改。

## 4. Validation & Error Matrix

| 条件 | 必须行为 |
| --- | --- |
| `--governance` 缺少 `--custom-terms`、文件缺失、JSON 损坏或治理字段类型错误 | 非零退出，stderr 为 `[ERROR]`，stdout 不出现通过结论 |
| 治理关闭，JSON 含 `banned` / `locked` / `exempt` | 不消费这些字段；旧 zh/en 行为不变 |
| 空治理配置且无未知自定义宏 | 零条新候选 |
| 存在未展开自定义宏且无命中 | 状态不是干净通过，并说明不能据此认为没有问题 |
| 固定保护区、缩略词表区域、用户豁免环境 | 无治理命中；普通表和更长标题不因此豁免 |
| 无合格首现、边界不清、数学括注、符号解释 | 不发二次 XOR；边界不清只有一条 `NEEDS-LLM` 说明 |
| 跨文件顺序 | 由入口装配决定；反向 include 不把更早的短形式当成二次出现 |
| `--degree-wording` 关闭 | `绝对误差` 仍可触发旧 `E-ABSOLUTE`；不出现 `E-DEGREE` |
| `--degree-wording` 打开 | `绝对误差为0.3` 无 `E-ABSOLUTE`；`极易` 有候选；同句第二个绝对化词仍报 |

## 5. Good / Base / Bad Cases

- Good：显式配置下报告 `旧称` 的全部候选和 slot，以及 locked 规范名；合格首现之后才报告二次括注、并列和 Title Case。
- Base：不传新开关时旧报告与退出码逐字节不变；空配置不产生新候选。
- Bad：按词频挑选规范名；把普通表整表豁免；把仅有 `中文名（缩写）` 的首次出现当成二次结论；用整句替换模板自动改写；把损坏配置报成零发现。

## 6. Tests Required

`tests/skills/latex_thesis_zh/test_term_governance.py` 按路径加载 ZH 脚本并恢复
`sys.path` / `sys.modules`。Windows 子进程设置 `PYTHONIOENCODING=utf-8`，并使用
`python -X utf8`。覆盖治理正反例、缩写体例三类与四类零命中、跨 include 顺序、
CLI 错误、旧 JSON 键，以及程度词 CLI。`test_consistency_semantics.py` 锁定旧
加载器不消费治理字段。`test_check_style_zh.py` 锁定程度词词位豁免、去重、
旧模式和报告字段。`test_polish_unit_zh.py` 只更新 `check_style_zh.py` 的实际
LF sha256。

公开资源同步同语言镜像、另一语言译文和 manifest。最终运行目标测试、
`just ci`、资源检查和 `just doc-build`。

## 7. Wrong vs Correct

错误：未传 `--governance` 时根据 JSON 里的 `banned` 报候选，或把自定义宏未展开的
零命中写成全文没有问题。

正确：新字段只在对应开关下读取；覆盖不完整时明确说明，不输出通过结论。
合成示例不得复制真实论文专名、原句或实验数字。
