# 词频密度制与预算制清嗓子 (C1)

## Goal

把 `deai_check.py` 的两个判负机制从"绝对计数 / 命中即扣分"改为"密度 / 预算"，
并引入章节类型系数。机制代码在 en / zh / typst 三副本保持字节一致，阈值与词表数据各自标定。

父任务：`08-29-writing-rhythm-arc`。证据基线与标定口径见父任务 `prd.md` 与 `research/calibration.md`。

## Requirements

本任务需求 ID 与父任务的对应关系：

- R1：`term_thresholds` 语义改为每万汉字密度上限，按 `ref/thesis` 五篇实测标定并写明来源与复审节律（父任务 R1.1、R1.5）
- R2：密度分母口径与短文档回退，分母抖动不得产生假阳性（父任务 R1.2）
- R3：`throat_clearing` 改预算制，超额部分才记痕迹（父任务 R1.3）
- R4：序列词按章节类型分配额度（父任务 R1.4）
- R5：机制代码三副本一致，不绕对齐锁（父任务 R1.6）

### R1 密度制词频阈值（父任务 R1.1、R1.5）

- `term_thresholds` 的值从"每篇绝对上限"改为"每万汉字（EN 为每万词）密度上限"。
- 配置文件与脚本内 `DEFAULT_THRESHOLDS` 同步改语义，且必须能从字面看出单位，
  避免旧值被误读成新语义。
- zh 阈值表按 `ref/thesis` 五篇实测 `P90 × 1.3`（下限 2.0）标定，写入 `tone-thresholds.yaml`。
- 阈值表内注明来源、标定日期、复算方法，并接入既有半年复审节律。

### R2 分母口径与短文档回退（父任务 R1.2）

- 分母与词频计数共用 `deai_check.py` 的 runtime visible-prose adapter：该 adapter
  先状态化跳过公式/图表/算法等多行环境与注释，再逐行调用
  `parser.extract_visible_text` 剥离引用、标签、行内数学与命令载荷；ZH 计汉字、EN 计词数。
  不依赖各 parser 不对称且不满足本契约的 `clean_text()`。
- 分母小于下限（建议 3000 汉字 / 1500 词）时，密度估计不稳定。
  此时回退为绝对计数判定，用 `阈值密度 × 下限 / 10000` 向上取整作为绝对上限，
  并在痕迹里注明使用了回退口径。
- 回退边界必须有测试，避免 5000 字的短稿因分母抖动产生假阳性。

### R3 预算制清嗓子（父任务 R1.3）

- `throat_clearing` 由"每次命中记一条痕迹"改为"全文预算 N 次，超出部分才记痕迹"。
- 痕迹指向超额的那几处（按出现顺序，第 N+1 处起），不是全部命中处。
- 预算本身也是密度量：`预算 = max(下限, round(密度预算 × 正文量 / 10000))`。
- 报告需给出「命中 M 次 / 预算 N 次」的计数，让作者看到自己离边界多远。

### R4 章节类型系数（父任务 R1.4）

- 序列词（`首先/其次/然后/最后` 与 EN 的 `first/then/finally` 族）在
  「论文组织结构安排 / 本章小结 / 技术路线」一类章节按系数放宽。
- 「研究背景 / 文献综述」一类维持基准系数 1.0。
- 系数值需要按章节分段重算实测密度后确定，不得凭印象取整数。
- 章节类型识别复用 `parsers.py` 既有 `SECTION_TITLE_RULES`；
  需要新增的类型（如 `organization`）作为该表的增量，不重写既有条目。

### R5 三副本一致性（父任务 R1.6）

- `_apply_tier`、`Checker._check_throat_clearing` 等已在
  `tests/contracts/test_deai_alignment.py` 登记的成员保持锁定关系不变。
- 新增的密度计算、预算计算、章节系数应用函数一并纳入 `ALIGNMENTS` 或 `LOGIC_ALIGNMENTS`。
- **不得**通过把成员从锁里摘出来的方式绕过冲突。
- typst 副本获得同一份机制代码，阈值与词表沿用其现有数据（本任务不为 typst 重新标定）。

## 非目标

- 不新增段落弧线检查（C2 / C3 负责）。
- 不改 `burstiness` 的 2/4/8 配置（既有取舍）。
- 不改 `overclaim`、`tense`、`sentence_length` 子表（三副本已锁定且与本次无关）。
- 不为 typst 重新标定阈值。

## Constraints

- `[Script]` 层恒 `Meaning-Check: NEEDS-LLM`。
- 痕迹等级维持 `LOW`；本任务不调整 D1–D5 维度映射。
- PyYAML 缺失时回退内置默认阈值的既有行为不变，回退后语义也必须是密度制。
- 不改 `justfile`、`pyproject.toml` 等构建配置。
- SKILL.md 只改 `last_updated`，不改 `version`。

## Acceptance Criteria

- [x] AC1（R1） 五篇 `ref/thesis` 正文各自触发的 `term_threshold` 痕迹数降至个位数，
      具体数值以回归测试固化（fixture 存放实测正文片段，不是整篇论文）。
- [x] AC2（R1） 构造密度超阈值 2 倍的样本，`term_threshold` 仍稳定触发。
- [x] AC3（R2） 短文档（< 3000 汉字）走回退口径，痕迹文本含回退标注；
      同一内容扩写到 3 倍长度后判定结果不发生方向性翻转。
- [x] AC4（R3） `throat_clearing` 预算按五篇命中密度 P75=2.6 次/万字标定；
      五篇语料合计仍有超额痕迹，且每篇痕迹数均不等于原始命中总数；
      低于 P75 的单篇允许 0 条超额痕迹。报告含「命中 M / 预算 N」计数。
- [x] AC5（R4） 序列词在「论文组织结构安排」样本上不触发，在同等密度的「研究背景」样本上触发。
- [x] AC6（R5） `tests/contracts/test_deai_alignment.py` 全绿，且 `ALIGNMENTS` /
      `LOGIC_ALIGNMENTS` 没有新增豁免项（可新增锁定项）。
- [x] AC7（R1、R2、R3、R4、R5） `just ci` 全绿。
- [x] AC8（R1） `tone-thresholds.yaml` 与 `tone-terms-zh.md` 语义一致，
      均写明密度单位、标定来源与日期；EN 侧同名文件同步。
- [x] AC9（R1） 按 `research/calibration.md` 记录的口径重跑 `ref/thesis`，
      得到与 yaml 内一致的阈值。
