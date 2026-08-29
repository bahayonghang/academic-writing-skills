# latex-thesis-zh 段落弧线诊断 (C2)

## Goal

在现有标题级、章级逻辑检查之间补上段落级观察：首句是否承载总领、末句是否形成
收束、相邻段是否存在可见接口、段内是否只有单句或纯罗列。脚本只报告可复算的形态
信号，语义判断仍交给作者或 LLM。

父任务：`08-29-writing-rhythm-arc`。依赖 C1，固定基线为 `dev` 上的
`4b37ddf`（章节类型与密度机制）和 `62f74a0`（C1 归档）。

## 标定证据与边界

标定只读使用本机真实论文 `chapter1.tex`，正文不进入仓库；研究材料仅保存源文件散列、
行号、句子散列、人工标签和聚合统计：

- 源文件 SHA-256：`077748f01dafb2d010e7d3e7c914820b9fb9bebfb9faa0171f4a46468d61f158`
- 42 个段落，33 个符合长度要求，9 个标题导语豁免
- 首句形态误报 0 段；连续“首句+末句双缺”最大长度 0
- 收束标记覆盖 7/33（21.21%）；该低覆盖说明不能按全章收束比例升级
- 11 个人工正接口、8 个人工负控；在“优质接口误报不超过 2 处”约束下，候选
  `τ=0.0200`，命中 4/8 个负控

作者已在 G1 确认人工接口标签边界与 `N=3`、`τ=0.0200`。单章跨学科代表性仍为
**UNVERIFIED**。

## Requirements

- R1：新增 `P-ARC-LEAD` / `P-ARC-CLOSE` / `P-ARC-LINK` / `P-ARC-FLAT`，
  每项判据都能由测试复算并写入 references（父任务 R2.1）。
- R2：默认 Info/P3；仅 `introduction` 与 `related` 内连续 N 个合格段同时缺失
  LEAD+CLOSE 时汇总升级为 Minor/P2（父任务 R2.2）。
- R3：公式图表/算法/列表边界、列表项、标题导语，以及 abstract、conclusion、
  acknowledgment、appendix、organization、summary 一律豁免；LINK 不跨标题或环境边界
  （父任务 R2.3）。
- R4：输出为 `[Script]` 观察，恒含 `Meaning-Check: NEEDS-LLM`；不产出改写文本，
  不给 `logic` 模块增加改写契约（父任务 R2.4）。
- R5：新增段落弧线判据表、范式和与 AXES 的关系说明；范例仅做原创抽象，不复制
  私有论文正文（父任务 R2.5）。
- R6：新增 `--paragraph-arc` 附加开关；默认关闭时输出逐字节不变。`--section`
  只缩小已有章节作用域；不借用语义无关的 `--first-chapter`。

## 四项观察

- `P-ARC-LEAD`：合格段首句为短空转、纯引用、纯数值/单位，或短句且无判断谓词。
- `P-ARC-CLOSE`：合格段末句既无回指式标记，也无前瞻式标记，且不以受保护环境收尾。
- `P-ARC-LINK`：同一 prose segment 的相邻合格段之间，后段首句既无显式承接标记，
  前段末句与后段首句的 token Jaccard 又低于 `τ`。
- `P-ARC-FLAT`：单句成段，或全部句子都是作者罗列；`related` 内与 A1 重叠时不重复报。

## 非目标

- 不判断句子是否“真正构成论点”，不自动改写正文。
- 不改 S1、E-*、P-PAPER、`analyze_abstract.py` 或 `analyze_conclusion.py`。
- 不把私有论文正文、整段引用或出版物全文放入仓库。

## Constraints

- 不改 `\cite{}` / `\ref{}` / `\label{}` / 数学环境，不新增论断、引用或数据。
- Info 输出不得使用“错误”“必须”等断言词。
- SKILL.md 只改 `last_updated`；不改 `justfile`、`pyproject.toml`。
- 产品测试只能依赖 `tests/fixtures/paragraph_arc/`，不能依赖归档后会移动的任务目录。

## Acceptance Criteria

- [x] AC1（R1）构造的缺总领/缺收束段分别只产生对应 finding，并定位首句/末句行。
- [x] AC2（R3）公式图表/算法/列表边界、列表项、标题导语及专用章节均不误报；
      LINK 不跨标题、公式、图表、算法、列表或表格边界。
- [x] AC3（R2）默认均为 Info/P3；绪论/相关工作连续 N 段双缺时只产生一条 Minor/P2
      汇总痕迹。N 已由 G1 冻结为 3。
- [x] AC4（R6）不带 `--paragraph-arc` 时，稳定 fixture 的输出与改造前基线逐字节一致。
- [x] AC5（R2）`research/arc-coverage.md`、标签 JSON、标定脚本和匿名快照可复算，
      并记录 G1 确认后的 N 与 τ。
- [x] AC6（R5）references 的每条判据均对应脚本分支；术语表 key 有 contract 测试。
- [x] AC7（R5）`just ci` 全绿，manifest 散列与中英文 docs 同步。
- [x] AC8（R4）每个 P-ARC finding 同时含 `[Script] P-ARC-*` 与
      `Meaning-Check: NEEDS-LLM`；`logic` 模块无改写契约段。
- [x] AC9（R1）LINK 的显式标记、重叠阈值两条通过路径及 FLAT 的单句/罗列两条路径
      均有正反例。
- [x] AC10（R1/R3）Jaccard 空集合为 0.0，先四舍五入到 4 位再比较，`score == τ`
      不报、`score < τ` 才报，且只比较同一 prose segment 的原始相邻段。

## Gates

- G1：已通过；作者确认人工接口标签边界及 `N=3`、`τ=0.0200`。
- G2：实现后在同一私有章节只读复跑；人工判为优质却被报告的接口不超过 2 处。
  私有语料代表性仍保留为 `UNVERIFIED`。
