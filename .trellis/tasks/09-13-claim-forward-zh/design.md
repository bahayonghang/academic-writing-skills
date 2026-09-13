# C2 技术设计：check_claim_forward.py（ZH）

## 边界

- 新脚本，与 EN 版同名不同实现；不入 TIER1 / deai / parsers 任何哈希组。
- import：`parsers`（ZH 副本，无 `clean_text`）、`tex_loader`（展开 `\input` / `\include`）、标准库；`yaml` 可选。
- 输出到 stdout；`--json` 结构与 EN 一致。

## 数据流

```
main.tex -> tex_loader 展开 -> LatexParser.split_sections() -> {section_key: body}
  -> (--section 过滤) -> 段落切分（空行 / \par）-> 句子切分（。！？；后断句；保留引号内句号不断）
  -> 每句打标：claim | limitation | disclaim | other
  -> 段内规则 + 句内规则 + 结论末段规则
  -> Finding -> 文本 / JSON
```

## 句子功能启发式（中文）

| 标签 | 触发 |
|---|---|
| `claim` | 主语 本文 / 本章 / 本研究 / 所提方法 / 提出的 + 动词 提出 / 实现 / 达到 / 验证 / 表明 / 优于 / 提升 / 降低；或含百分比、倍数、"相比…提高" |
| `limitation` | 起始 然而 / 但 / 尽管 / 虽然 / 需要指出，或含 局限 / 不足 / 未能 / 无法 / 难以 / 受限于 |
| `disclaim` | 句首 本文不试图 / 本文并不主张 / 本文无意 / 本研究不涉及 / 本文并未 |
| `other` | 其余 |

## 五码规则（与 EN 差异）

| 码 | ZH 差异点 |
|---|---|
| `CF-DISCLAIM` | 同 EN；`related` 段与"研究范围"小节（标题含"范围 / 界定"）跳过 |
| `CF-SELFWEAK` | 词表见 prd R1；`未能` 需上下文门控：句含引用或主语为"现有 / 上述 / 传统 / 文献"时豁免；`仅能` 只在主语为本文/所提方法时报 |
| `CF-CAVEAT-POS` | 同 EN；Limitations 对应"不足 / 局限"小节（标题匹配）跳过 |
| `CF-HEDGE-STACK` | 词表见 prd R1；`有望` 只在结论展望段不计（展望段允许） |
| `CF-CLOSE-NEG` | 结论末段负面判定且后文无 `direction_markers`；承接句（`CC-OUTLOOK-TRANS` 要求）合法：负面句后同段或下一段有展望标记即不报 |

Severity / Priority 与 EN 相同（高影响段 `CF-DISCLAIM` Minor/P2；`CF-SELFWEAK` Minor/P2；`CF-CAVEAT-POS` Info/P3；`CF-HEDGE-STACK` Info/P3；`CF-CLOSE-NEG` Minor/P2）。

## 与 ZH 现有检查的边界

| 现有 | 关系 |
|---|---|
| `analyze_abstract.py` T-PAIN / T-OPEN | `尚未` 等痛点词是摘要合法用语，不入 `self_weakening`；`CF-DISCLAIM` 在 abstract 段只报"本文不试图"类免责，不报痛点陈述 |
| `analyze_conclusion.py` CC-OUTLOOK-TRANS / CC-OUTLOOK-EMPTY | `CF-CLOSE-NEG` 不与 CC-OUTLOOK-TRANS 冲突：前者查"负面后无方向"，后者查"展望前有承接"。两者同时通过 = 负面判定 + 承接 + 展望 |
| `check_style_zh.py` ABSOLUTE_TERMS | 方向相反（绝对化 vs 自贬），词表零交集；模块文档写明 |
| `deai_check.py` ZH `FAKE_INSIGHT` / 连接词 | "值得注意的是 / 需要指出的是" 归 deai；本脚本不收 |
| `over-claim-guard.md` | 向上校准节：候选升级措辞标 "对照过度声明阶梯" |

## terms YAML（ZH）

```yaml
version: 1
self_weakening:
  - match: "遗憾的是"
    prefer: ""            # 删除引导词，保留事实句
  - match: "仍明显落后"
    prefer: "与{baseline}相差{gap}"
  - match: "效果有限"
    prefer: "在{scope}上提升{value}"
  - match: "存在严重不足"
    prefer: "在{aspect}上受限于{cause}"
  - match: "仅能"
    prefer: "能够"
    subject_gate: ["本文", "本章", "所提", "本方法"]
  - match: "未能"
    prefer: "尚未在{scope}上"
    cite_exempt: true
hedges: [可能, 或许, 在一定程度上, 某种程度, 大致, 基本, 相对, 似乎, 有望]
disclaim_openers: [本文不试图, 本文并不主张, 本文无意, 本研究不涉及, 本文并未]
direction_markers: [展望, 未来, 下一步, 有待, 后续, 进一步研究, 将]
limitation_section_titles: [不足, 局限, 研究范围, 界定]
```

`subject_gate` / `cite_exempt` 是 ZH 特有字段；EN YAML 不含，契约测试对两份 YAML 只锁顶层键集合的交集。

## 兼容与回滚

- 全新文件 + 增行；删除即回滚。
- `SMOKE_COMMANDS` 增一条会让覆盖测试跑脚本，脚本必须在无 finding 时也 exit 0。

## 取舍

- 不复用 EN 脚本做语言分支：EN 断句、主语识别、引用命令集合均不同；两份实现 < 一份双语分支的复杂度（`paper-audit-zh-profile` 任务已否决过按语言拆 skill，本处是同一 skill 内新脚本，不冲突）。
- `未能` 保留但门控：基线 3/5 篇，全部是引用他人工作；门控后预期 0 误报（待实现时用私有语料复核，不进测试）。
