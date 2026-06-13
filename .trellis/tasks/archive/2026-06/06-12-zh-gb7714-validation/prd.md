# 实现真实 GB/T 7714 校验并适配 2025 新国标

> 父任务：`06-12-latex-thesis-zh-optimization`（见其 prd.md §1 调研、§2 发现 F1/F2/F12/F18）
> 优先级：P0 —— skill 名片级功能（description 首屏宣传 GB/T 7714）目前是空壳。

## Goal

把 `verify_bib.py --standard gb7714` 从空操作变成真实的 GB/T 7714 结构校验，
并让 skill 在 GB/T 7714-2025（2025-12-02 发布，**2026-07-01 实施**，全面代替 2015 版）
过渡期内给出正确的双版本指引。

## Requirements

### R1 让 `--standard gb7714` 真正生效（F1）

- `BibTeXVerifier` 消费 `self.standard`：传入 gb7714 时启用国标增量检查；
  default 行为保持现状（向后兼容）。
- 国标增量检查最小集：
  - 期刊：缺 volume/pages 给 warning（国标著录格式需要 卷(期):页码）；
  - 电子文献：缺 url 或 urldate（引用日期）给 warning；
  - 中文条目作者使用 "等"、英文条目使用 "et al." 的混用提示（仅当 .bib 内出现
    字面 "等"/"et al." 时检查，不改写内容）；
  - 4 名及以上作者未截断的提示（信息级，biblatex 样式会自动处理，提示仅针对手写场景）。

### R2 补全 GB/T 7714 高频文献类型（F2）

- `REQUIRED_FIELDS` 增加：`phdthesis`/`mastersthesis`（school, year — 对应 [D]）、
  `techreport`（institution, year — [R]）、`patent`（如有此 entry type，number/year — [P]）、
  `standard`/`misc`+note 形式的标准文献（[S]）、`online`/`electronic`（url — [EB/OL]）。
- biblatex-gb7714-2015 特有字段做信息级提示：中英混排排序常用的 `langid`。

### R3 GB/T 7714-2025 过渡期适配（调研结论 §1.1）

- `--standard` 增加 `gb7714-2025` 取值：在 2015 检查之上调整差异点
  （非网络文献不再要求访问日期；新增 preprint/dataset 类型的著录提示）。
- `references/citations/gb-standard.md` 增补"2025 版要点与过渡期建议"小节：
  发布/实施时间线、与 2015 版的主要差异（预印本、数据集、统一著录符号、
  取消非网络文献访问日期、个人责任者规则调整）、biblatex-gb7714-2025 社区实现状态、
  "答辩在 2026-07-01 之后的论文建议确认学校是否切换新国标"的提示。
- SKILL.md description 中"GB/T 7714"措辞保持版本中立（不写死 2015）。

### R4 清理失实输出（F12, F18 国标部分）

- `verify_bib.py:265` 的 "google_web_search" 改为与 Claude Code 一致的表述
  （如"使用 WebSearch 工具检索标题获取 DOI"）。
- `gb-standard.md` 第五节（图表编号）、第六节（章节标题字体）移出本文件
  （归属见 zh-template-knowledge 任务），文件内保留指向说明；确保
  `modules/format.md` 与 `modules/bibliography.md` 的链接仍有效。

## Constraints

- 校验只读不改写：发现问题输出建议，不自动修 .bib（Critical Rules #2 零捏造）。
- 不引入第三方 bib 解析依赖；沿用现有正则解析器（其 `[^@]*?` 对含 @ 字段的
  已知局限可记录为 known issue，不在本任务修复）。
- 在线校验（online_bib_verify）边界不变：仍需用户显式开启。

## Acceptance Criteria

- [ ] fixture .bib（含 @phdthesis 缺 school、@online 缺 urldate、@techreport 缺
      institution、正常 @article 各若干条）：`--standard gb7714` 报出全部缺字段
      条目，`--standard default` 行为与现状一致（回归）。
- [ ] `--standard gb7714-2025` 可用，且对同一 fixture 的输出差异符合 R3 规则。
- [ ] 输出中不再出现 "google_web_search"。
- [ ] gb-standard.md 更新后，从 SKILL.md / modules 出发的全部链接可达（无死链）。
- [ ] 新增检查均有 pytest 用例；`just ci` 全绿。
