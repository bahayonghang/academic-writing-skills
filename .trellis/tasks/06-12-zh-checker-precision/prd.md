# 修复 deai/consistency/format 检查器精度缺陷

> 父任务：`06-12-latex-thesis-zh-optimization`（见其 prd.md §2 发现 F5/F6/F7/F8/F16/F17/F23/F24）
> 优先级：P1 · 依赖：`06-12-zh-parsers-multifile`（章节切分与多文件地基）。

## Goal

消除三个检查器的确定性误报/漏报缺陷，使脚本诊断（[Script] 标签）的可信度
配得上输出契约中的 Severity/Priority 字段；并让 deai 模块与 2025-2026 高校
AIGC 检测政策现实对接。

## Requirements

### R1 deai_check.py 缺陷（F5/F6/F7/F8）

- F5 破折号计数去重："——"（两个 U+2014）应计 1 处；建议先以 "———?|---" 整段
  匹配再计数，加回归测试（2 处"——"在默认阈值 5 下不得告警）。
- F6 全文档覆盖：`analyze_document()` 对未命中 SECTION_PATTERNS 的正文章
  也要执行章节级检查（依赖 parsers-multifile 任务提供的全章节枚举 API），
  章节名回退为标题文本。
- F7 修复 `_is_false_positive` 死代码：`context_before` 要么真正参与判断
  （如"提升了 12%"在前文的场景），要么删除该行——不允许保留无效计算。
- F8 PyYAML 降级为可选：`import yaml` 失败时回落 DEFAULT_THRESHOLDS 并打印
  一行 info（阈值定制不可用），脚本不得因缺 yaml 而崩溃；同步更新
  `tone-thresholds.yaml` 头部注释说明该行为。

### R2 check_consistency.py 设计修正（F16/F17）

- F16 术语组语义重设计："全称(缩写)首次定义 + 后文用缩写"是国标推荐写法，
  不是不一致。改为检查真正的漂移信号：
  - 同义中文全称混用（深度神经网络 vs 深层学习）仍然报告；
  - 全称与缩写并存时，只在"缩写已定义后正文仍大量使用全称"或"缩写从未定义
    就直接使用"时提示（与 check_abbreviations 的 undefined 检查联动，去重输出）；
  - 建议语不再是"统一使用 'CNN'"，而是"首次出现用全称（缩写），后文统一用缩写"。
- F17 文件集合改为 include 图：默认仅分析从 main.tex 可达的文件
  （复用 parsers-multifile 的装配 API），`--all-files` 保留 rglob 旧行为作显式选项。
- 术语/缩写统计加 visible-text 过滤（排除注释、\cite 键、文件路径内的伪命中）。

### R3 check_format.py 降噪（F23）

- oral_expression 检查加 visible-text 过滤与白名单上下文（"我们"在
  thuthesis 等模板许可的表述里常见，降为 info 并在消息中说明"部分院校
  要求用'本文/笔者'"）；"很多/一些/非常/特别"仅在正文（非数学/代码环境）标记。
- `optimize_title.py --interactive` 标注为人工模式（agent 路径不使用），
  或从 argparse help 中隐藏。

### R4 deai 模块对接 AIGC 政策现实（F24）

- `references/deai/guide.md` 增补一节（约 30-40 行）：
  - 2025 届起高校 AIGC 检测格局：知网检测通道普及，校级阈值集中在 15%-40%
    （列 3-4 个公开案例：川大文 20/理 15、民航大 30、海大 40、华师大 20+标注）；
  - 检测误判现实（公式、法条、访谈整段误报案例；同文不同平台 7%-70% 波动），
    引导用户把 deai 输出当作可读性改进建议而非"过检测保证"；
  - 政策边界重申：教育部"允许辅助、禁止代写"，本模块只做语言风格审阅，
    不提供任何"规避检测"承诺（与 skill Safety Boundaries 一致）。
- `--tier` 文档说明与校级阈值的对应建议（heavy ≈ 红线 ≤20% 的学校）——
  仅作指引措辞，不改变阈值缩放逻辑。

## Constraints

- deai 维度框架（D1-D5）保持"面向可读性、不针对具体平台"的定位，不得加入
  任何对抗特定检测器的特征工程。
- 所有阈值/规则调整必须配 pytest 回归（现有 TestDeaiCheck 风格）。
- 不 bump version，只改 last_updated。

## Acceptance Criteria

- [ ] 含 2 处"——"的 fixture 不再触发破折号告警；6 处则触发（边界测试）。
- [ ] 标题为"多模态情感识别模型研究"的章在 `--analyze` 输出中出现。
- [ ] 缺 PyYAML 的环境（测试中 monkeypatch 模拟 ImportError）跑通 deai_check。
- [ ] 规范论文 fixture（首次"卷积神经网络（CNN）"后文全用 CNN）在
      check_consistency 中零误报；真实漂移（深度神经网络/深层学习混用）仍报。
- [ ] check_consistency 默认不再统计未被 include 的 .tex。
- [ ] deai/guide.md 新增小节包含校级阈值案例与误判提示，且无"包过检测"类措辞。
- [ ] `just ci` 全绿。
