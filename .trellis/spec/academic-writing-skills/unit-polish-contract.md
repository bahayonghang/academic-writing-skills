# 中文学位论文单元润色契约

## 1. Scope / Trigger

维护 `latex-thesis-zh` 的 `polish` 路由、`polish_unit_zh.py`、单元润色协议、
fixture、eval 或相关文档时适用。面向作者的规则由技能内
`references/modules/polish.md` 与 `references/writing/unit-polish-zh.md` 拥有；
复制安装后的技能不得依赖本开发仓库的 spec 或私有语料。

## 2. Signatures

```text
uv run python scripts/polish_unit_zh.py INPUT --plan
    [--section SECTION] [--unit ID] [--first-chapter N] [--json]
uv run python scripts/polish_unit_zh.py INPUT --verify
    (--unit ID | --original FILE) --revised FILE
    [--terms JSON] [--max-growth RATIO] [--first-chapter N] [--json]
```

`--terms` 复用 consistency 的 `{"zh": [[...]], "en": [[...]]}` 格式。
显式术语的原文片段仅在 `UP-STRENGTH` 计数时屏蔽；`UP-TERM` 仍比较术语出现次数，
其他核对不受影响。没有术语表时不猜测术语边界。
`--max-growth` 默认 0.20，是未标定的长度变化提示阈值，不是润色质量标准。

## 3. Contracts

- 小节沿用 S-CTX 的 depth-3 编号与装配行坐标，范围包含标题；邻域沿用
  `prev.tail`、`parent_lead`、`next.head`。自然段沿用 P-ARC 切分；无 depth-3
  时仅列自然段，不回退到 depth-2。清单只给坐标、标题和约字数，不输出正文。
  复用切分前按原行数屏蔽前导区与纯文档结构命令，不能把模板配置当作自然段；
  不能用“汉字数为零”排除真实英文或数值正文。
- 每次只改一个单元。超过 1200 字的小节按内部段落逐个改写；只读邻域只供理解。
  章节和全文请求先列清单。单元 id 是当前源码快照，下一轮编辑前重新生成。
- `--verify` 比较原文与用户/LLM 提供的润色稿，不生成替换文本。
  每个发现及零发现结论均为 `Meaning-Check: NEEDS-LLM`；脚本不输出
  `Risk-Flags`，不宣称 `PRESERVED`。四字段改写契约由 `[LLM]` 层负责。
- 原有标题原样保留合法；标题增删改属于范围漂移。邻域首句的确定性检查仅比较
  至少 12 个汉字的精确子串，且必须是相对原文新增；原文已有重复句不能误报。
- 引用、交叉引用、标签、公式、数字的差异为阻塞项；术语、强度、否定和长度
  只是候选。脚本通过不能替代因果、对象、适用范围和结论强度的语义核读。
- 引用键抽取与可见文本中的引用载荷屏蔽共用同一命令识别边界，覆盖明确支持的
  natbib/biblatex 单次、多次引用及大小写、星号和可选注记形式。不得把任意名字
  包含 `cite` 的自定义宏自动当作引用。交叉引用也覆盖支持命令的首字母大写形式。
- `--plan` 的文本报告只列单元，不附核对结论或语义复核结论；`--verify` 的 A 档
  原文/润色稿差异应可直接阅读，不泄露 Python 容器表示法。JSON 结构不受影响。
- 既有 `analyze_logic.py`、`deai_check.py`、`parsers.py`、`check_style_zh.py`、
  `check_claim_forward.py`、`tex_loader.py` 在**本模块**保持不变；通过 import 复用游标、
  段落切分、窗口及 loader，hedges 来源保持为 claim-forward 词表。其他任务若改这些文件，必须同步更新 `test_polish_unit_zh.py` 的 `FROZEN_HASHES`（LF 规范化 sha256）。
- 导语保留；连接词按位置与证据判断；结论强度保持；不引入论文指纹。
  不新增 deai 类别，不为语言改写调整论文中的实验事实或受保护载荷。

## 4. Validation & Error Matrix

| 检查 | 判定 | 结果 |
| --- | --- | --- |
| UP-SCOPE | 标题增删改、新增输入/文档结构命令、新增只读邻域句子 | Error / P1 |
| UP-CITE / UP-REF | 引用键或引用目标多重集变化 | Error / P1 |
| UP-LABEL | 标签集合变化 | Error / P1 |
| UP-MATH | 受保护数学片段变化 | Error / P1 |
| UP-NUM | 可见数字及数值单位 token 多重集变化 | Error / P1 |
| UP-TOKEN | 受保护标识符候选集合变化 | Warning / P2 |
| UP-TERM | 显式术语表的术语计数变化；无表不检查 | Warning / P2 |
| UP-STRENGTH | 屏蔽显式术语后比较强度词或 hedge 计数，附命中上下文；方向仅为疑似 | Warning / P2 |
| UP-NEG | 否定标记计数变化 | Info / P3 |
| UP-LENGTH | 可见汉字数变化超过未标定阈值 | Info / P3 |

`--plan` 无单元或 section 未命中时给出可见说明，退出 0；参数错误退出 2。
`--verify` 有 Error 退出 1，其余退出 0；缺少润色稿、缺少或同时提供两种原文来源
属于参数错误。读取失败不可伪装成无发现的成功。可见文本提取不保证覆盖所有
模板宏参数，模板宏仍须按协议原样保留并由 LLM 核读。
普通词语中的子串命中仍可能是误报，例如未配置术语时的“支持向量机”或“相关研究”。
候选报告须提示先辨别术语/普通用法，再判断结论强度，不得仅凭计数断言语义变化。

## 5. Good / Base / Bad Cases

- Good：只拆分单元内过长句，引用、公式、标题与事实不变；核对后给润色稿、
  三类修改说明、四字段块及核对摘要。
- Base：原文逐字节副本零发现但仍需语义复核；没有 depth-3 时仅列自然段。
- Bad：把原有小节标题判越界；复制邻节句子；删除引文；把“可能”改成“证明”；
  以 `PASS-SCRIPT` 代替语义保真结论，或整章生成未经逐单元核对的替换稿。

## 6. Tests Required

`tests/skills/latex_thesis_zh/test_polish_unit_zh.py` 按路径加载 ZH 脚本，
对称恢复 `sys.path` 和 `parsers` / `tex_loader` / `analyze_logic` sidecar。
断言既有 subsection-context fixture 的九个 id、无 depth-3 自然段、各检查码
正反例、原文不变、邻域边界、术语输入、JSON 和退出码，以及六脚本 LF 规范化哈希。
数学环境的合法空白形式、数值单位的维度变化，以及双反斜杠后的注释边界也须
覆盖；不能让普通合法 LaTeX 拼写绕过红线检查或把注释当成引文变更。
引用回归覆盖 biblatex 单次/多次引用、可选注记、大小写与星号、相似宏名不误命中、
以及载荷不进入强度/数字候选；交叉引用覆盖首字母大写形式。术语屏蔽测试须同时
证明术语频次仍受保护、术语外的“可能→证明”仍告警。YAML 读取测试使用与内置
回退不同的词，分别证明实际加载和回退路径；CLI 帮助及两模式报告各自有覆盖。
星号前也允许 LaTeX 合法空白；须覆盖空格、换行及去除注释后留下的换行，不能
只测试命令名与星号紧邻的拼写。

路由增加时同步 `SMOKE_COMMANDS`、模块清单及 `POLISH_MODULE_DOCS`。
eval/trigger 只追加并保留原前缀。公开资源同步源文件、英文译页、中文镜像及
manifest。最终运行目标测试、资源同步、`just ci` 和 `just doc-build`。

私有语料只用于本地核读，原文和润色稿不进 fixture、测试或公开文档。
任务内复核记录只保存核对码与命中数；合成测试和一次本地复核均不能证明误报率
或所有宿主平台的运行质量。

## 7. Wrong vs Correct

错误：润色稿包含任何 `\subsection` 就阻塞，即使该标题来自原始单元。

正确：比较原文和润色稿的标题命令序列与标题文本；原样保留通过，增删改阻塞。
只读邻域也比较新增内容，不能把原文已有的同句判成越界复制。
