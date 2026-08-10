# latex-paper-en 整合 nature-writing 增量

## Goal

按父任务 `research/delta-matrix.md` 的 adapt 判定,将 nature-writing 增量整合进 latex-paper-en。实现前先读父任务 prd.md、source-basis.md、delta-matrix.md。

## 范围(delta-matrix 映射)

### D-EN-1 期刊式文章架构参考 [P0, LLM-only] — N1/N2/N3/N4/N5

现状:latex-paper-en 支持 journal 与 conference 论文(SKILL.md description),但 section-writing 参考库按会议式结构组织(Experiments+Discussion 合并);期刊式 Results 叙事 / Discussion 扩展 / 全文论证链缺失。

新增 `references/writing/article-architecture.md`(独立文件,**不放** section-writing/ 目录内——渐进加载契约):

- N1 全文论证链(boundary 为一等要素)
- N2 期刊式摘要六步(与既有三模板并列,按论文类型选择,不替代)
- N3 摘要 LLM-only 诊断三条(措辞遵循父级共享契约:候选提示 + "可能",非判定;无数字项注明脚本 Results-VAGUE 已有)
- N4 Results 证据阶梯六层 + claim-first 小节开头模式
- N5 Discussion 六步扩展(与 experiments.md 既有四步链交叉引用,不重复)
- 归属声明:社区归纳 Nature-leaning 启发式 + 同源说明(措辞见 source-basis.md)

接入:routing-rules.md 新触发词(journal narrative、Nature-style、Results narrative、Discussion structure 等);section-writing/index.md 仅加一行交叉引用;modules/section-writing.md 提示何时改读本文件。

**零脚本改动**(en+typst 哈希锁 + 来源置信不足,父任务架构决策 1)。

### D-EN-3 翻译模块:意图翻译分解 [P1, LLM-only] — N15/N16

增强翻译 lane 参考(translation-guide.md 或 modules/translation.md,design 阶段定位置):

- N15 意图六分解:中文长句拆 claim/evidence/condition/comparison/implication/limitation,按目标章节要求的顺序重写英文
- N16 修复表**只补两类**:宽泛重要性先于对象 → 提前点名系统/问题;方法列表先于 gap → gap 前置。其余四类(显著无基线/首次无范围/相关性推机制/结果混含义)交叉引用 over-claim guard,禁止重复实现

### D-EN-4 标题/表格 doc-only 微补 [P2] — N7/N11

- title.md:补标题公式(system+capability+application)与 prestige 词告诫(novel/advanced/powerful/green/efficient 需被标题其余部分具体化),标注 [LLM] 判断;**optimize_title.py 词表与逻辑不动**(无条件删词会破坏合法术语)
- tables.md:补一句方向标注建议(接受 Unicode ↑/↓、LaTeX 命令、文字说明三种形式;可读性建议非强制)
- 其余表格规则已覆盖,在收尾报告落档"已覆盖不改"

## 非增量(禁止重复实现)

delta-matrix N6/N8/N9/N10/N12/N13/N14/N18 均 reject;不向 paper-audit 引入内容。

## Acceptance Criteria

- [ ] article-architecture.md 存在,含 N1-N5 五节 + 归属声明;不复制 section-writing 既有内容(只交叉引用)
- [ ] 路由接入:routing-rules.md 触发词 + section-writing/index.md 交叉引用一行 + modules/section-writing.md 提示
- [ ] 翻译参考含六分解与两类新修复,四类重叠项为交叉引用
- [ ] title.md/tables.md 微补落地;optimize_title.py、check_tables.py、analyze_abstract.py 零改动(git diff 验证)
- [ ] `uv run python docs/scripts/check_resource_sync.py --write-manifest --inventory-only` 重建后 `--skill latex-paper-en` 与全量校验通过;新文件双语页面(EN 完整译文 + zh 页)就位
- [ ] 行为 eval(正反各≥1):期刊式重构请求应路由到新参考;普通会议论文润色请求不应加载它。结果记录在任务 verification 或收尾报告;未执行 provider-backed 评估标 UNVERIFIED
- [ ] `just ci` 全绿 + `just doc-build` 成功
- [ ] SKILL.md 只改 last_updated

## Constraints / 依赖

- 本任务先于 08-10-nature-writing-zh 执行(manifest 串行,父任务架构决策 4)
- 红线与全仓约束见父任务 prd.md
