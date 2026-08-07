# 模块：实验回顾

**触发**：实验、评估、基线、消融、显着性、效率比较

**目的**：审查现有的实验或评估部分并发布审稿人风格的发现，而无需起草替换段落。

## 命令

```bash
uv run python -B scripts/analyze_experiment.py main.tex --section experiments
uv run python -B scripts/analyze_experiment.py main.tex --section results
```

## 回顾焦点

- 基线/比较特异性
- 度量和数字证据
- 夸大其辞或促销措辞
- 缺失消融证据
- 缺少统计显着性或方差报告
- 缺少效率比较
- 结论超出了所显示的证据

## 声明-证据图

对于任何结果、比较、消融、重要性或效率声明，请发出
有用时紧凑的声明-证据图：

- `claim`：确切的句子或标题声明。
- `evidence_anchor`：表格、图形、公制、截面或`missing`.
- `claim_strength`：
  - 当没有本地结果、指标、图形、表格或方法锚时，`unsupported`
支持该主张。
  - `observed` 当指标出现但数据集/基线/分析单位为
不完整。
  - `supported` 当声明与可见结果锚相关联但仍然
需要边界检查。
  - `strong` 仅当公制加图形/表格/工件支持可见并且
设置是有界的。
- `missing_evidence`：所需的基线、消融、方差、源表或
数据工件。
- `allowed_wording`：受报告设置限制的措辞。
- `forbidden_wording`：获胜者、重要性或需要的通用声明
更有力的证据。

## 原始脚本输出

```latex
% EXPERIMENT (Line 42) [Severity: Major] [Priority: P1]: Comparison claim names only generic baselines; cite or name the exact comparator.
% EXPERIMENT (Line 42) [Severity: Major] [Priority: P1]: Performance claim is not tied to a concrete metric or numeric result.
```

## 技能层响应

- 保留 LaTeX 友好的评论评论风格的最终回复。
- 除非用户明确要求修改文章，否则不要重写实验部分。
- 切勿发明基线、指标、重要性声明或效率数字。
- 不要将仅度量的观察结果推广为通用结果。保留数据集，
样品、基线和测量边界可见。

---

## 讨论与结果-文献整合（B3-B4）

### B3：讨论深度——归因胜于重复

**规则**：讨论部分不能止于重述数字。它应解释结果*为什么*发生，但不能把因果或归因语言本身当作证据。只复述表格是浅层讨论；堆叠没有支持的机制同样没有增加解释深度。

**检测启发式**（脚本自动化）：
- 扫描 `discussion` 部分中的所有可见线
- 计数包含归因标记的行：`because|due to|owing to|as a result of|attributed to|caused by|mechanism|explains|explanation|reason|hypothesis|interpret|stems from|arises from|driven by|suggests that|indicates that`
- 如果比率 < 总可见线的 15%（至少 5 条线）→ Major/P1

|图案|判决|
|---------|---------|
|“模型 A 达到了 95%。模型 B 达到了 90%。”|浅重复（标志）|
|“模型 A 优于模型 B，可能是因为它能够捕获远程依赖关系。”|仅有归因线索；须由 `[LLM]` 核对证据锚点|

**LLM 证据边界**：保留的每项机制都应对应可见指标、图表、消融、受控对比、引用或区分性检验。若连续列出两个及以上具体机制，却没有逐项支持，末尾又统一声明当前数据无法验证，应标记为防御性推测解释。证据不能区分时直接说明机制尚未确定；不得删掉限制语或增强无证据支持的推断。

### B4：结果-文学回响

**规则**：讨论应参考相关工作中引用的先前工作来比较研究结果。相关工作的引文关键词应重新出现在讨论中，以表明作者已将其结果置于上下文中。

**检测启发式**（脚本自动化）：
- 提取引文关键字（`\cite{...}`） 从`related`截面范围
- 从 `discussion` 部分范围中提取引文关键字
- 如果零重叠→Major/P1

**修复**：添加诸如“与史密斯等人的发现一致”之类的句子。\cite{smith2020}，我们的结果证实......”或“与琼斯的方法不同\cite{jones2019}，我们的方法表明......”

---

## 结论完整性检查（B5）

**规则**：完整的结论必须包含三个要素：
1. **核心发现摘要** - 明确重述所证明的内容
2. **影响** — 更广泛的影响或实际意义
3. **限制/未来的工作** - 公认的界限和后续步骤

**检测启发式**（脚本自动化）：
- 扫描 `conclusion` 部分以获取三个关键字类别：
  - 结果：`we have shown|we demonstrated|results show|this paper has presented|our experiments confirm|we proposed|findings indicate|key finding|main result`
  - 影响：`implication|suggests that.*practical|enables|opens|paves the way|facilitates|contributes to|advance|potential for|applicable to`
  - 限制：`limitation|future work|future direction|remain|challenge|could be extended|further research|further investigation|not addressed|beyond the scope|caveat`
- 缺少限制 → 主要/P1
- 缺失的影响 → 次要/P2
- 缺失的发现摘要 → 次要/P2
