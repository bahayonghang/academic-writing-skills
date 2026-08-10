# qiaomu 先例检索与取舍

## 检索过程

按 `qiaomu-meta-skill` 的“先找先例，再决定 keep/adapt/reject”流程进行了两组检索：

- `remove AI writing patterns`
- `humanize scholarly prose evidence preservation`

统一检索脚本在 Windows 上因不能解析 `npx` 报 `WinError 2`，随后用 `npx.cmd` 和
SkillsMP 客户端完成降级检索。原始结果保存在：

- `research/skillsmp-remove-ai-writing.json`
- `research/skillsmp-humanize-scholarly.json`

SkillsMP 的第一页结果混入大量无关高 star 仓库，`repo_stars` 是仓库 star，不是 skill 安装量、
评分或质量证据；搜索结果只能用于候选发现。没有安装任何第三方 skill。

## 已审阅先例

| 先例 | 可借鉴 | 不采用 |
| --- | --- | --- |
| `Galaxy-Dawn/claude-scholar@writing-anti-ai` | 双语模式索引、渐进加载、先审阅再改写 | 人格/观点注入、强制改三项数量、全禁破折号、50 分真实性评分、含捏造事实的改写例 |
| `blader/humanizer` 及同源移植 | Wikipedia 模式聚类，强调不是单一词面问题 | 通用内容营销语境直接套入学术论文；把词表当检测器 |
| `AIScientists-Dev/academic-humanizer` | 面向 scholarly prose 的语域保持和分阶段复核思路 | 仅凭“更像人写”作为验收；缺少本仓库 claim-evidence 与语法锚点契约 |
| `op7418/Humanizer-zh` | 中文本地化模式，不把英文短语逐字翻译 | 将中文高频学术连接词一律视为 AI 痕迹 |
| SkillsMP 中其他 humanizer 变体 | 说明审计-改写-复核和 pattern cluster 是常见架构 | 仓库 star、主观分数、AI 概率和“过检测”承诺 |

## 与本仓库现状的关系

当前 EN/ZH/Typst de-AI 已经覆盖空话、过度确定、模糊量化、模板开头、机械结构、低信息
密度、段首重复、填充连接词、破折号过度使用、overclaim、时态和句长均匀度。2026-08-05
的 defensive-rhetoric 契约还证明了一个关键边界：需要 claim-evidence 映射的段落级模式应为
C 档 `llm-only`，不能被 hedge 词或句式正则替代。

先例的真正增量不是更长的禁词表，而是：

1. 按模式簇审阅，而不是按单词给文本贴 AI 标签；
2. `audit -> rewrite -> fidelity audit` 闭环；
3. 允许删除修辞壳和局部重组，但逐项证明 claim、数字、引用、术语与边界仍在；
4. 可选作者样本校准，但学术体裁、venue、证据边界和保护术语优先级更高；
5. 补足当前未显式建模的七类 LLM-only 模式：无依据的分词尾句、宣传性评价、模糊归因、
   间接谓词堆叠、同义词循环、虚假范围、空泛挑战/积极结尾。

## 统一取舍

### Keep

- 保持现有三个 de-AI module，不创建第四个 skill。
- 保持默认先诊断/蓝图，用户明确请求正文改写后才给 prose proposal。
- 保持 EN 为跨副本 canonical、ZH/Typst 做语言适配、公开资源双语同步。

### Adapt

- 将通用 pattern list 改造成 claim-local、evidence-aware 的七个 LLM-only 模式簇。
- 将“preserve meaning”升级为可见的 fidelity ledger，并复用四字段输出契约。
- 将“match voice”改成可选作者样本校准；样本只影响语气与节奏，不覆盖术语、体裁和证据。
- 每个模式同时提供正例、证据充分反例和语法/引用保护用例。

### Reject

- 第一人称、观点、幽默、情绪或“灵魂”的自动注入；
- 为打破 rule of three 强制改成两项或四项；
- 删除合法 hedge，或把不确定结论写得更确定；
- 全面禁止 em dash；
- 把粗体、列表、标题大小写等格式责任重复塞进 de-AI；
- 50/100 分“真实性”、AI 概率、AI 检测通过率或 detector-evasion 承诺；
- 复制任何没有事实来源的 `After` 示例。

## 结论

推荐以文档、eval 和 contract test 为主要交付，不修改三份 `deai_check.py`。只有未来独立任务
先用真实学术语料证明某个规则具备高精度、可解释排除条件和默认兼容性后，才考虑显式 flag
后的 B 档 candidate 检查；`--tier` 仍只表示检测灵敏度，不能承担编辑强度。
