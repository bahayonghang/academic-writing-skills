# nature-writing 写作技巧整合到 latex-paper-en 与 latex-thesis-zh

## Goal

将 `ref/claude-scholar/skills/nature-writing`(SKILL.md + references/ 全部内容)中**尚未被本仓库吸收的写作技巧增量**,整合进 `latex-paper-en` 与 `latex-thesis-zh` 两个技能,并做针对性优化。

## 规划工件索引(父任务持有,子任务勿重复调研)

- `research/source-basis.md` — 来源权威性定级:**社区归纳的 Nature-leaning 修辞启发式**,非 Nature 官方规则;来源对摘要诊断仅 "may" 级置信。
- `research/delta-matrix.md` — N1-N19 逐项判定(来源锚点 / 现有实现锚点 / keep-adapt-reject / owner / D-* 映射),含 N3 共享措辞契约。

### 同源判定(关键)

nature-writing 的 abstract/introduction/method 核心模板与 `ref/Research-Paper-Writing-Skills`(Peng Sida 笔记,MIT)同源;latex-paper-en 的 `references/writing/section-writing/`(index.md 有归属声明)已完整吸收该源。**本任务是差量整合(仅 delta-matrix 中 adapt 项),不是移植。**

## 已定架构决策(2026-08-10 审阅后)

1. **不引入脚本级 Nature profile;摘要 nature 式诊断全部 LLM-only。**
   原因:EN `analyze_abstract.py` 与 Typst 副本受整文件哈希契约锁定(`tests/contracts/test_writing_modules_alignment.py` TIER1_HASH_GROUPS),脚本改动必然把范围扩大到 typst-paper;且来源置信仅 "may" 级、无词表,不具备硬性 [Script] 规则依据。EN 侧零脚本改动;ZH 侧唯一脚本改动为一条 [LLM] Info 提示项(analyze_abstract.py 未被哈希锁,B-SEM 已有同模式先例)。
2. **新架构参考放 `references/writing/article-architecture.md`(独立文件),不放 section-writing/ 目录内。**
   原因:section-writing 渐进加载契约要求一次只装载一个活动章节指南;全文多章节架构放入该目录会形成第二并行入口。路由经 routing-rules.md;section-writing/index.md 仅加一行交叉引用。
3. **optimize_title.py 词表不动。** `optimize_title()` 无条件删除 INEFFECTIVE_WORDS(optimize_title.py:212-218),加入 green/efficient/advanced 会破坏合法术语。prestige 词告诫为 doc-only + LLM 判断。
4. **执行 DAG 为串行:EN 子任务 → ZH 子任务 → 父任务终检。**
   原因:两子任务都会增改 references,而 `docs/scripts/check_resource_sync.py --write-manifest` 重写整份 `docs/resource-manifest.json`,并行会互相覆盖。每个子任务在自己的提交内完成 manifest 重建 + 双语页面(保持该提交 CI 绿);父任务终检最后重建一次并验证零漂移。
5. **N3 共享措辞契约由父级持有**(见 delta-matrix.md),EN/ZH 两侧文档措辞一致,消除跨子任务脚本 schema 依赖。

## 任务图与依赖

| 顺序 | 任务 | 交付物 |
| --- | --- | --- |
| 1 | 08-10-nature-writing-en | D-EN-1 期刊式架构参考(N1/N2/N3/N4/N5);D-EN-3 翻译意图分解(N15/N16);D-EN-4 标题/表格 doc-only 微补(N7/N11) |
| 2 | 08-10-nature-writing-zh | D-ZH-1 英文摘要 [LLM] 提示项(N3);D-ZH-2 结论局限组织顺序(N17);D-ZH-3 结果章叙事顺序核对(N19) |
| 3 | 父任务终检 | 跨子任务验收 + manifest 零漂移验证 + 归档 |

依赖已写入子任务 PRD:ZH 在 EN 合入后开始(manifest 串行);D-ZH-1 措辞遵循父级 N3 契约。

## 跨子任务验收标准(父任务终检执行)

- [ ] delta-matrix 每条 adapt 项在对应子任务落地;reject 项零重复实现
- [ ] 新增/修改检查项沿用所属检查器的既有输出 schema：EN 文档诊断表使用
  `[LLM]` + Severity `Info` + Priority `P3`；ZH `B-NAT` 沿用 `B-SEM` 的
  `[LLM]` + `level=Info` schema（概念优先级 P3），不为单项扩展全部 `B-*` JSON 字段
- [ ] 新增 references 带归属声明(社区归纳来源 + 同源说明,措辞遵循 source-basis.md;不得称"Nature 官方规则")
- [ ] `uv run python docs/scripts/check_resource_sync.py --skill latex-paper-en` 与 `--skill latex-thesis-zh` 通过;全量校验通过;终检重建 manifest 零漂移
- [ ] `just ci` 全绿 **且** `just doc-build` 成功(ci 不含 doc-build,需单独跑)
- [ ] 行为 eval:各子任务至少一组正反用例(应路由/不应路由、应提示/不应提示);未执行的 provider-backed 与真实论文精确率评估在收尾报告标 **UNVERIFIED**
- [ ] SKILL.md 只改 last_updated,version 保持与 pyproject 一致
- [ ] 不触碰 deai 对齐锁、parsers 对齐契约、en+typst TIER1 哈希组

## Constraints

- 红线:不修改 `\cite{}`/`\ref{}`/`\label{}`/数学环境内容;不虚构文献与实验数据;不改保护术语
- paper-audit 边界:本任务不向 paper-audit 技能引入任何内容(N14 已 reject)
- evals.json 若需修改,走 Bash python 写入(格式化 hook 陷阱)
- 仓库不存在 `latex-paper-zh`;用户指的是 `latex-thesis-zh`,已按此理解
- 父任务不做直接实现

## 修订记录

- 2026-08-10 初版:含两处事实错误(EN 定位、ZH 英摘检查覆盖),任务图误标"任意顺序"。
- 2026-08-10 二版:按外部审阅 11 条意见修订(全部核验成立);补 research 工件、架构决策、串行 DAG、验收强化。
