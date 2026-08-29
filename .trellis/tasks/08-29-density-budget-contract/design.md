# 技术设计 (C1)

## 现状

`deai_check.py` 三副本（`latex-paper-en` 为 canonical，`latex-thesis-zh`、`typst-paper` 跟随）。

- `_check_term_threshold()`（zh 副本约 888 行）：`_iter_visible_lines()` 全文 substring 计数，
  `count > cap` 即产一条痕迹。`cap` 来自 `thresholds["term_thresholds"][word]`，是绝对数。
- `_check_throat_clearing(section_name)`（约 736 行）：逐段匹配 `self._throat_clearing_re`，
  每次命中产一条痕迹。该方法在 `ALIGNMENTS` 中锁定为 en/zh/typst 字节一致。
- `_apply_tier()`（约 208 行）：`light/medium/heavy` 按 `_TIER_FACTORS` 缩放阈值，
  对 `term_thresholds` 做 `max(1, round(cap * term_factor))`。`_TIER_FACTORS` 三副本锁定。
- 阈值来源：`references/deai/tone-thresholds.yaml`，缺失或无 PyYAML 时回退 `DEFAULT_THRESHOLDS`。
- 章节识别：`parsers.py` 的 `SECTION_PATTERNS` / `SECTION_TITLE_RULES`，
  现有类型 `abstract / introduction / contribution / related / method / experiment /
  result / discussion / conclusion`，无「组织结构安排」类型。

## 边界与契约

| 项                                   | 变更 | 说明                                        |
| ------------------------------------ | ---- | ------------------------------------------- |
| `_check_term_threshold`              | 改   | 当前未登记锁；本次新增登记为三副本逻辑锁    |
| `_check_throat_clearing`             | 改   | 已登记字节锁，三副本同改                    |
| `_apply_tier`                        | 改   | 缩放对象从绝对上限变为密度上限，语义不变    |
| `_TIER_FACTORS`                      | 不动 | 倍率语义在密度制下仍成立                    |
| `DEFAULT_THRESHOLDS["term_thresholds"]` | 改   | 已登记为分歧项，各副本独立标定              |
| `DEFAULT_THRESHOLDS["throat_clearing"]` | 改   | 增加 `budget_per_10k` 与 `min_budget` 字段  |
| `overclaim`/`punctuation`/`sentence_length`/`tense` | 不动 | 三副本已锁定且与本次无关                    |
| `burstiness`                         | 不动 | 既有取舍                                    |

## 数据模型

### 阈值文件新增字段

```yaml
# 单位：每万汉字（EN 副本为每万词）。标定来源与日期见文件头注释。
threshold_unit: per_10k_chars
threshold_calibration:
  source: ref/thesis 五篇博士学位论文正文
  method: P90(密度) * 1.3, floor 2.0
  calibrated: 2026-08-29
  review_due: 2027-02

density_fallback:
  # 可见正文量低于该值时回退绝对计数判定
  min_corpus: 3000

term_thresholds:
  首先: 8.8
  # ...按 research/calibration.md 全表填入

throat_clearing:
  budget_per_10k: 2.6
  min_budget: 1
  patterns: [...]   # 保持现状

section_factors:
  # 章节类型 -> 序列词密度系数。1.0 为基准。
  organization: 6.6
  summary: 2.5
  default: 1.0
sequence_terms: [首先, 其次, 然后, 最后]
```

`section_factors` 与 `sequence_terms` 只作用于 `sequence_terms` 列出的词，
不影响 `显著/全面/深入` 一类内容模板词——那批词在任何章节都不该放宽。

### 密度判定

```
corpus = len(可见正文)                      # zh 按汉字数，en 按词数
if corpus < min_corpus:
    cap_abs = ceil(threshold_density * min_corpus / 10000)
    mode = "fallback"
else:
    cap_abs = ceil(threshold_density * corpus / 10000)
    mode = "density"
超阈 when count > cap_abs
```

回退口径用 `min_corpus` 而非真实 `corpus` 做分母，避免 800 字的片段把上限压到 1 次。
其含义是「短文档按 3000 字的额度给」。

### 章节系数

序列词的有效上限按章节分摊：

```
cap_abs = ceil(sum over sections( density * factor(section) * corpus(section) ) / 10000)
```

这样一篇论文里「组织结构安排」占的字数越多，序列词额度越高，而不是整篇统一放宽。
非序列词的 `factor` 恒为 1.0，退化为全文密度判定。

### 预算制清嗓子

```
budget = max(min_budget, round(budget_per_10k * corpus / 10000))
命中列表按 (section, line) 排序，第 budget+1 项起产痕迹
痕迹文本："段首套话命中 M 次（预算 N 次），此处为第 K 处"
```

预算是文档级的，不能在每个 section 内重新发放。保留
`_check_throat_clearing(section_name)` 的调用形态，但该方法每次都先按全文收集并按行号排序，
计算唯一的全文预算、裁掉前 N 处，再只返回属于 `section_name` 的超额命中。
因此 `check_section()`、整篇 `analyze_document()` 与 `--section` 都共享同一份全文预算语义，
不会出现“每节一份预算”。报告字段同时携带全文命中 M、预算 N 与全局序号 K。

预算值来自五篇 PDF 文本提取产物的段首代理计数密度
`[2.64, 0.77, 1.21, 3.79, 2.17]`，inclusive P75=2.64，写入配置时取 2.6。
该选择允许低于 P75 的单篇不报警；验收看语料集总体仍有超额痕迹，不为满足测试降低预算。

## 章节类型识别增量

`parsers.py` 的 `SECTION_TITLE_RULES` 追加两条，插在 `method` 之前
（`method` 是 "包含匹配" 且限章级，会吞掉标题里含"方法"的组织安排节）：

```python
("organization", 3, r"(?:组织结构|结构安排|内容安排|技术路线|论文结构)"),
("summary", 3, r"^本章小结$"),
```

`SECTION_PATTERNS` 同步追加对应正则。EN 副本对应
`organization`: `paper (?:is )?organized|roadmap|outline of this`。

真实锁面不是“en / zh / typst 三副本”：ZH 的中文规则不在该数据锁内；EN family 的
`LatexParser.SECTION_TITLE_RULES` 锁定 `latex-paper-en / paper-audit / cover-letter`，
`TypstParser.SECTION_TITLE_RULES` 还包含 `typst-paper`。因此 EN 规则须同步到这四个 family
副本的对应 parser，ZH 规则单独落地；deprecated `SECTION_PATTERNS` 未锁，但与各自规则同步更新。

## 兼容性

- 旧 yaml（无 `threshold_unit`）被读到时：值是 4/5/6 这样的小整数，
  在密度制下等于极严。必须显式处理——检测到缺 `threshold_unit` 时
  按旧语义（绝对计数）运行并在 stderr 提示升级，不静默改判定。
  这条保护让用户自己定制过的 yaml 不会因为升级而突然全量误报。
- `--tier` 行为不变：仍缩放阈值数值，只是数值单位变了。
- 报告格式：痕迹文本从「全文出现 N 次（上限 M）」改为
  「全文出现 N 次，密度 X.X/万字（上限 Y.Y/万字）」。
  下游 `deai_batch.py` 若解析该文本需同步；执行时先确认。

## 可见正文与标定适配器

- runtime 源代码分母与词频计数统一基于增强后的 `_iter_visible_lines()`：
  该函数在 `deai_check.py` 内状态化跳过公式/图表/表格/算法等多行环境与整行/行内注释，
  再逐行调用 `parser.extract_visible_text()` 去掉 `cite/ref/label`、行内数学和命令载荷。
  ZH 计 `[一-鿿]`，EN 计英文词元；同一规范化行流同时服务计数、分母、section 加权和定位。
- 不使用 `parser.clean_text()`：ZH `LatexParser` 当前没有该方法；EN family 的现实现会保留
  `cite/ref/label` 参数，且该方法不在三份 deai runtime 的统一契约面内。
- `ref/thesis/decrypted/*.txt` 是 PDF 文本提取产物，不存在 LaTeX/Typst parser 所需的源结构；
  复算脚本使用独立、显式记录的 PDF-text adapter 剥离页标、目录、页眉页码与参考文献。
- 两个 adapter 共享“只计规范化可见正文单位”的契约，但不声称字节级同流。
  runtime fixture 负责锁定 `_iter_visible_lines()` 的公式/引用/注释/图表排除，标定脚本负责 AC9 的可复算性。

## 回滚

单 commit 粒度分离：先阈值文件与语义开关，再机制代码，最后章节系数。
任一步失败可 `git revert` 到上一步，不留半改状态。
`threshold_unit` 缺省即旧行为，是天然的回滚开关。
