# latex-thesis-zh 结果分析写作指南与文档联动（子任务 1）

## Goal

新建 `references/writing/results-analysis-guide-zh.md`（结果分析运行时 LLM 判据权威），
更新 `references/modules/experiment.md`，完成 spec 无损核对与双语文档联动。
判据与泛化规则唯一依据 = 父 `08-09-results-analysis-zh/design.md` §2/§3.3（不复述）；
需求原文 = 父 `research/user-spec-results-analysis.md`。

## Requirements（认领父 prd R1 / R3 / R7）

### R1 新参考 guide `results-analysis-guide-zh.md`

十一小节：目标与事实边界；强制论证顺序（模型对比 + 生成保真度两条 8 步链）；数值比较
规则；参照与判据绑定（三分命名 + 端点方向 + "等价"红线 + 结果术语闭集）；图表分工表；
生成/增强类章节统计保真度规范（适配层，声明适用条件）；证据阶梯五级 + 与
`method-description-guide-zh.md` §六四级主张表的分工声明和双向映射表（父 design §2）；
基线解释四轴；正反例（含持平/预期外结果写法）；R-*↔RA-* 映射表（父 design §3.3，注明
RA 为启发式线索非覆盖）；阈值与出处。

约束：域名词（R2R、PFG-CDM、水泥论文书名）只作示例；与 method-chapter-guide-zh.md §五、
over-claim-guard.md、method-description-guide-zh.md、experiment.md、tables.md 重叠内容
一律互链；不得出现"已验证/准确识别"类效果声明（父 design §7）。

### R3 `references/modules/experiment.md` 更新

追加"结果分析深度检查 (--results-analysis)"节（RA-* 表 + guide 路由行）；B3/B4/B5 与
防御性推测契约文本语义不变；contract test 锁不过时同步更新期望（不弱化判据）。

### R-MAP spec 无损核对

产出父任务 `research/spec-mapping.md`：spec 每条判据 → guide 落点或互链目标。

### R7 双语文档联动

manifest 重建 + sourceLocale 校正；guide 与 experiment.md 的 en/zh 页面（en 为完整译文）；
resource sync 单技能校验 + docs build。

## 边界

- 不改任何 `scripts/*.py`、SKILL.md、routing-rules.md、evals（归子任务 2）。
- guide 中 RA-* 表按父 design §3 行文；子 2 实现后若行为有出入，由子 2 回改文档。

## Acceptance Criteria

- [x] guide 十一小节齐备；`research/spec-mapping.md` 逐条核对通过（泛化允许改名词，不允许
      丢判据）。
- [x] 证据阶梯与四级主张表的分工声明 + 映射表落位，词表零复制。
- [x] `uv run --extra dev python -m pytest tests/contracts/ -q` 通过（defensive-ai-rhetoric
      与 docs bilingual 契约）。
- [x] `uv run python docs/scripts/check_resource_sync.py --skill latex-thesis-zh` 通过；
      `just doc-build` 通过。
- [x] `just ci` 全绿（文档任务零代码回归）。
