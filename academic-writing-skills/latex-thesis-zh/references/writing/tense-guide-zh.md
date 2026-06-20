# 时态指南（英文摘要时态）

中文学位论文的**正文用中文，中文没有时态**，因此本指南与脚本检查只针对**英文摘要（Abstract）**。
英文摘要须遵循英文论文的时态惯例：目的不是一律用过去时，而是每个部分有各自约定，
最常见的错误是把"方法/结果"的叙述写成现在时。

脚本（`deai_check.py`）**仅在英文摘要区域**（`\begin{abstract}`，不含中文摘要 `\begin{cabstract}`）
内运行，对其中的现在时**报告动词**发 `[Script]` LOW 痕迹；定位不到英文摘要则不检查。

## 英文摘要的时态

| 部分 | 默认时态 | 例 |
|---|---|---|
| 背景（Background） | 现在时 | "Long-context inference *is* expensive ..." |
| 方法（Methods） | 过去时 | "We *trained* ... / Models *were evaluated* on ..." |
| 结果（Results） | 过去时 | "The model *achieved* 92.3% / We *observed* ..." |
| 结论（Conclusion） | 现在时 | "These results *provide* a basis for ..." |

> 正文各章（绪论/方法/实验/结论）用中文撰写，遵循中文写作规范，不在时态脚本检查范围内。
> 若学位论文要求英文版章节，按英文论文时态惯例（同上扩展：方法/结果绝对过去时，图表说明用现在时）。

## 信号词（扫英文摘要的方法/结果句）

最常见的错误是该用过去时的地方用了现在时的报告动词：

- `shows / reveals / demonstrates / indicates / presents / confirms / achieves / outperforms`
  出现在方法/结果叙述里 → 一般应改为 `showed / revealed / demonstrated / …`。脚本会标记这些。

### `is` / `are` —— 人工判断（脚本不标记）

英文摘要方法/结果里的现在时 `is` / `are` **常常**是时态错误，但合法用法太多，不宜自动标记。
下列情况保留现在时：

- **定义**："Let *G* be ... / The loss *is defined as* ..."；
- **通论性事实**："Cross-entropy *is* convex ..."；
- **描述图表本身**："Table 2 *is* organized by ..."；
- **软件能力**："The toolkit *supports* ..."。

其余情况优先过去时："The threshold *was set* to 0.5"（而非 *is* set）。

## 脚本跳过的例外（现在时正确）

1. **图/表/公式作主语**："Figure 3 *shows* ...", "as *shown* in Fig. 4", "Table 1 *lists* ..."。
2. **软件/工具能力**："The library *provides* ..."。
3. 夹在方法段里的**定义或通论**。

命中以上情形属误报，保留即可。

## 与其他指南的边界

- 本指南管**时态**。措辞强度（因果/首创/普适）见 [over-claim-guard.md](over-claim-guard.md)。
- 中文学术风格见 [academic-style-zh.md](academic-style-zh.md)。

## 脚本支持

`deai_check.py`（`ChineseAITraceChecker`）只在英文摘要区域对现在时报告动词发 `[Script]` LOW 痕迹
（配置：`references/deai/tone-thresholds.yaml` 的 `tense:` 段，`enabled` 开关）。
脚本会过滤图表/软件假阳性，但不判断 `is` / `are`——那些用上面的清单人工核。
