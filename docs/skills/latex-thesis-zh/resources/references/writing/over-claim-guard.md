# Conservative Wording Guard (Over-Claim Protection)

A reference for conservative wording in Chinese degree theses. The goal is **not** to make statements
weak, but to **state evidence strength precisely**: strong evidence permits strong wording; weak evidence
requires weak wording. Blind-review experts are highly alert to over-claiming, so proactive calibration
is easier than revising after questioning.

## Boundary with “Is the Evidence Sufficient?”

This file governs **how strong the wording should be once evidence strength is known**: which verb or
qualifier keeps the sentence within the evidence. First determine whether figures/tables/metrics/citations
actually support the claim, then use this file to choose wording. Substance takes priority when it conflicts with wording.

## Certainty Ladder (Strong to Weak)

```
证明 / 表明（强）                 ← 干预实验（消融/受控对比）
  ↓
揭示 / 发现 / 识别出               ← 强效应，多方法或可复现
  ↓
表明 / 提示                       ← 显著但单一方法
  ↓
支持 / 与……一致                  ← 趋势性，与前人一致
  ↓
可能表明 / 或许提示 / 似乎         ← 边缘显著或预测性
  ↓
暗示 / 倾向于                     ← 极弱信号或假说
```

Match the rung to the evidence; do not climb above what the data can reach.

## Replacement Tables

### 1. Causality (Most Common Over-Claim: Calling Correlation Causation)

| ❌ Over-Claim | ✅ Conservative Wording |
|---|---|
| 由……导致 / 引起 | 与……相关 / 关联 |
| 驱动 / 决定 | 影响 / 与……相关 |
| 是……的根本原因 | 与……有关 / 可能与……有关 |
| 证明了 | 表明 / 提供了……的证据 |
| 造成了 | 伴随出现 / 与……同时出现 |

Use causal wording only for controlled interventions (ablation, randomized grouping, A/B comparison),
instrumental-variable designs, or reproduction of an established mechanism. Otherwise use correlational wording.

### 2. First/Unique Claims (Reviewers Will Search Immediately)

| ❌ Over-Claim | ✅ Conservative Wording |
|---|---|
| 首次 / 第一个 | 据我们所知，首次 / 最早的工作之一 |
| 新颖的（自我标榜） | Directly state what is new; delete the “novel” label |
| 前所未有的 | 显著的 / 值得注意的 |
| 此前未知的 | 此前研究不充分的 |

### 3. Universality (One Scenario Cannot Support Every Scenario)

| ❌ Over-Claim | ✅ Conservative Wording |
|---|---|
| 总是 / 永远 / 从不 | 通常 / 很少 |
| 在所有情况下 | 在所研究的情形中 |
| 普遍地 | 在所评测的基准上 |
| 任意数据集 | 所采样的数据集 |

### 4. Effect Size (“Significant/Large” Without Numbers)

| ❌ Over-Claim | ✅ Conservative Wording |
|---|---|
| 大幅提升 | 误差降低了 X% |
| 显著的效应 | β = X.XX（95% CI：…） |
| 明显改善 | 从 X 提升到 Y（p = …） |
| 高度显著 | p < 1 × 10⁻¹⁰ |
| 鲁棒 / 稳健 | 在 N 次独立运行中一致 / 在[扰动]下稳定 |

If the number already tells the story, remove the adjective and let the number speak.

### 5. Time/Inference Order (Inferring Historical Causality from Contemporary Data)

| ❌ Over-Claim | ✅ Conservative Wording |
|---|---|
| X 驱动了该变化 | 该变化与 X 一致 |
| 发生在 T 时刻 | 估计约为 T（置信区间：…） |
| 从 A 迁移到 B | 数据与 A→B 的路径一致 |

### 6. Application Prospects (Downstream Use Not Demonstrated Here)

| ❌ Over-Claim | ✅ Conservative Wording |
|---|---|
| 将带来变革 | 对……具有潜在意义 |
| 将被广泛使用 | 可能有助于 / 可为……提供参考 |
| 解决了 X 问题 | 处理了 X 的一个方面 |
| 可直接落地部署 | 为[场景]提供了候选方法 |

### 7. Comparison (Disparaging Prior Work)

| ❌ Over-Claim | ✅ Conservative Wording |
|---|---|
| 前人方法未能…… | 前人方法受限于…… |
| 优于所有已有方法 | 与[具体方法]相比具有优势 |
| 终结了长期争论 | 为该争论的一方补充了证据 |

## Frequent Trap Sentences

| Trap | Safe Alternative |
|---|---|
| “本文结果证明了 X。”（X 是因果） | “本文结果与 X 一致。” |
| “这是首个……的工作。” | “据我们所知，是最早……的工作之一。” |
| “X 在 Y 中起关键作用。” | “X 与 Y 有关 / 可能对 Y 有贡献。” |
| “这些发现对……具有重要意义。” | “这些发现为进一步研究……提供了基础。” |
| “X 是 Y 的关键驱动因素。” | “X 与 Y 相关。” |
| “强烈支持” | “与……一致 / 提供了与……一致的证据” |

## Reverse Calibration: When **Not** to Be Conservative

Weak evidence requires caution, but cautious wording for strong evidence becomes timid. Use strong wording when:

- a controlled intervention (ablation / randomized control / A-B) yields a causal result -> use “证明”;
- multiple methods/datasets/random seeds reproduce the result -> use “稳健” and state the evidence;
- an established mechanism is reproduced -> “确认 / 验证” is appropriate;
- a large effect has strong statistics -> use strong wording **with the number**.

## Self-Check After Each Paragraph

- [ ] Used “首次/新颖”? Was the literature actually searched? If not, add “据我们所知”
- [ ] Used “导致/驱动/决定”? Is there an intervention? If not, change to “与……相关”
- [ ] Used “所有/总是/普遍”? Is the scope limited to the actual study?
- [ ] Used “显著/大幅/明显”? Is a number attached?
- [ ] Listed an application not demonstrated here? Add “可能/或许”
- [ ] Disparaged prior work? Use “受限于” instead of “未能/失败”

## Script Support

`deai_check.py` emits a `[Script]` LOW trace for a small set of unambiguous over-claim phrases in
causality/first/universality/application categories and points back here. The script catches only obvious
cases; the tables above cover judgments the script cannot make.
