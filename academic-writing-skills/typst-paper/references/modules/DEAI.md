# 模块：去AI化编辑
**触发词**: deai, 去AI化, humanize, reduce AI traces, 降低AI痕迹

**目标**：在保持 Typst 语法和技术准确性的前提下，降低 AI 写作痕迹。

**输入要求**：
1. **源码类型**（必填）：Typst
2. **章节**（必填）：Abstract / Introduction / Related Work / Methods / Experiments / Results / Discussion / Conclusion
3. **源码片段**（必填）：直接粘贴（保留原缩进与换行）

**工作流程**：

**1. 语法结构识别**
检测 Typst 语法，完整保留：
- 函数调用：`#set`, `#show`, `#let`
- 引用：`@cite`, `@ref`, `@label`
- 数学：`$...$`, `$ ... $`（块级）
- 标记：`*bold*`, `_italic_`, `` `code` ``
- 自定义函数（默认不改）

**2. AI 痕迹检测**:
| 类型 | 示例 | 问题 |
|------|------|------|
| 空话口号 | significant, comprehensive, effective | 缺乏具体性 |
| 过度确定 | obviously, necessarily, completely | 过于绝对 |
| 机械排比 | 无实质内容的三段式 | 缺乏深度 |
| 模板表达 | in recent years, more and more | 陈词滥调 |
| 结构壳 | 不是 A 而是 B, not merely A but B | 没有说明比较轴、基线和证据 |
| 伪洞察/讲义腔 | 真正的问题, essentially, The conclusion is: | 用提示词替代证据支撑的判断 |
| 时态信号 | shows / presents（方法/实验/结果章） | 应改用过去时叙述 |
| 过度声明 | caused by, for the first time, universally | 因果/首创/普适性越界 |

时态与过度声明的判定表见 [TENSE_GUIDE.md](../TENSE_GUIDE.md) 与 [OVER_CLAIM_GUARD.md](../OVER_CLAIM_GUARD.md)。

**学术人味契约**：
先保护四类内容，再降低 AI 味：
- **事实/证据**：数据、实验设置、图表、指标、`@cite`、`<label>`、数学和宏；
- **主张/立场**：论文真实结论、方法选择、不确定性和局限；
- **逻辑**：段落角色、章节角色、claim-evidence 映射；
- **边界**：适用条件、假设、缺少证据处和 `待补证`。

默认输出诊断、风险摘要或改写蓝图。只有用户明确要求改写正文时，才给 prose proposal；不得承诺降低某个检测平台分数。

**3. 文本改写**（仅改可见文本）：
- 拆分长句（英文 >50 词，中文 >50 字）
- 调整词序以符合自然表达
- 用具体主张替换空泛表述
- 删除冗余短语
- 补充必要主语（不引入新事实）

**4. 输出生成**：
```typst
// ============================================================
// 去AI化编辑（第23行 - Introduction）
// ============================================================
// 原文：This method achieves significant performance improvement.
// 修改后：The proposed method improves performance in the experiments.
//
// 改动说明：
// 1. 删除空话："significant" -> 删除
// 2. 保留原有主张，避免新增具体指标
//
// ⚠️ 【待补证：需要实验数据支撑，补充具体指标】
// ============================================================

= Introduction
The proposed method improves performance in the experiments...
```

**硬性约束**：
- **绝不修改**：`@cite`, `@ref`, `@label`, 数学环境
- **绝不新增**：事实、数据、结论、指标、实验设置、引用编号
- **仅修改**：普通段落文字、标题文本

**分章节准则**：
| 章节 | 重点 | 约束 |
|------|------|------|
| Abstract | 目的/方法/关键结果（带数字）/结论 | 禁泛泛贡献 |
| Introduction | 重要性->空白->贡献（可核查） | 克制措辞 |
| Related Work | 按路线分组，差异点具体化 | 具体对比 |
| Methods | 可复现优先（流程、参数、指标定义） | 实现细节 |
| Results | 仅报告事实与数值 | 不解释原因 |
| Discussion | 讲机制、边界、失败、局限 | 批判性分析 |
| Conclusion | 回答研究问题，不引入新实验 | 可执行未来工作 |

参考：[DEAI_GUIDE.md](../references/DEAI_GUIDE.md)

## 分级模式（`--tier`）与 D1-D5 维度

`--tier {light|medium|heavy}` 为**可选开关**。不传时输出与原来完全一致；传入时：

- **缩放阈值**：`light` 报得更少（放宽上限），`heavy` 报得更多（收紧上限），`medium` 保持现有阈值；
- **启用 D1 句长检查**：标记句长变异系数过低（机械均匀节奏）的章节，中英双语；
- **为每条结论标注 AIGC 维度** D1-D5 并附一句 teaching note（检测器为何标记该模式）。

```bash
uv run python scripts/deai_check.py main.typ --analyze --tier heavy
```

五个维度面向可读性，**不针对任何具体检测平台**：D1 句长变化、D2 段落结构、D3 信息密度、D4 连接词频率、D5 术语-语境匹配。阈值（含 `sentence_length.cv_threshold`）仍可经 `references/AI_TONE_THRESHOLDS.yaml` 覆盖。
