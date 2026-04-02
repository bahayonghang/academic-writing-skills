# 常见问题

## 我运行了 `audit.py --mode deep-review`，但没有 `final_issues.json`

这是正常的。该命令只执行 Phase 0 自动审查。

完整 deep review 还需要：

1. workspace 准备
2. reviewer lanes
3. consolidation
4. quote verification
5. final report rendering

## 我只有 PDF

可以用，但以下方面置信度较低：

- 公式
- 符号一致性
- 精细结构

有源文件时优先用 `.tex` 或 `.typ`。

## 为什么 deep review 里还有分数？

分数被保留为 summary indicator 和兼容层。主产物已经不是分数，而是结构化 issue bundle 和 revision roadmap。

## 什么时候用 `quick-audit`，什么时候用 `deep-review`？

用 `quick-audit`：

- 想快速筛查
- 只需要 script-backed 发现
- 想决定是否值得做更深审查

用 `deep-review`：

- 想模拟审稿人
- 关心 claim validity、comparison fairness、global consistency
- 需要 revision planning

## 为什么 `self-check` 和 `review` 还可以用？

它们是兼容别名：

- `self-check` -> `quick-audit`
- `review` -> `deep-review`

新文档和新脚本都应使用 canonical 名称。

## 报告里没有 reviewer lanes

通常意味着外层 workflow 没有派发 section lanes / cross-cutting lanes，或者这些 lanes 的 JSON 没有写进 `comments/`。

## deep-review 输出里没有 `committee/consensus.md`

现在 deep-review 会自动写出 `committee/consensus.md`。

如果缺失，优先检查：

- 流程是否完整跑完（中途是否中断）
- 你查看的是否是本次运行对应的 workspace
- `committee/` 目录是否有写权限问题

## 为什么委员会总分被封顶到 `4.0`？

当 editor verdict 为 `Desk Reject` 时，总分会强制封顶 `4.0`。
这是为了防止“细项分数看起来不差”掩盖了主编预筛的硬拒风险。

## Quote verification 失败了

优先检查：

- quote 是否其实来自 OCR 噪声
- reviewer 是否做了意译而不是 exact quote
- workspace 内文本是否就是 reviewer 实际阅读的那份文本
