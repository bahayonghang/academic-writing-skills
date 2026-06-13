# Design: deai/consistency/format 精度修复

## deai_check.py（F5/F6/F7/F8）

- F5：`_check_punctuation` 破折号按"连续 run"计数：`len(re.findall(r"—+|-{3,}", text))`，
  "——"（两个 U+2014）计 1 处。
- F6：`__init__` 中用 `parser.chapter_ranges()` 把未命中关键词的正文章并入
  `section_ranges`（键回退为标题文本），`--analyze`/`--score`/JSON 全覆盖。
- F7：`_is_false_positive` 让 `context_before` 真正参与：显著/大幅 模式在
  **前文** 20 字内出现 `\d+%` 同样视为已量化（"误差降低了12.5%，显著提升…"）。
- F8：`import yaml` 移入 try/except；ImportError 时回落 DEFAULT_THRESHOLDS 并
  stderr 打一行 info；tone-thresholds.yaml 头部注释同步说明。

## check_consistency.py（F16/F17 余项）

- 术语组语义重设计：组内成员分为"全称变体"（含 CJK/小写词）与"缩写"（全大写 ASCII）。
  - 仅 ≥2 个全称变体并存时报 variant_mix（深度神经网络 vs 深层学习照报）；
  - 全称+缩写并存不再视为不一致；
  - 缩写已定义（全称（缩写）模式）且**定义之后**全称仍出现 ≥3 次 →
    full_after_abbrev 提示，建议语"首次出现用全称（缩写），后文统一用缩写"；
  - 缩写未定义就使用 → 不在 check_terms 重复报告（check_abbreviations 已有 undefined）。
- visible-text 过滤：匹配前 `_sanitize()` 去掉注释、\cite/\ref/\label/\input 等
  参数与路径（等长空格替换，行号不变）；check_abbreviations 同样过滤。
- F17 文件集（include 图 + --all-files）已在 parsers-multifile 任务落地。

## check_format.py（F23）

- oral_expression 拆分：`oral_pronoun`（我们/你们 → info，消息注明"部分院校要求
  用'本文/笔者'"）+ `oral_vague`（很多/一些/非常/特别 → warning）。
- 口语检查仅对 `extract_visible_text` 后的正文匹配（数学/引用键不再误中），
  并跳过 verbatim/lstlisting 环境。
- status：仅 warning/error 计入 WARNING；info-only → PASS（exit 0）。

## optimize_title.py

- 删除从未被消费的 `--interactive` 旗标（router 任务同步文档）。

## deai/guide.md（F24）

新增"高校 AIGC 检测政策与本模块定位"一节（约 35 行）：知网检测通道普及与
校级阈值案例（川大文 20%/理 15%、中国民航大学 30%、中国海洋大学 40%、华东师大
20%+标注）、误判现实（公式/法条/访谈误报、同文跨平台 7%-70% 波动）、教育部
"允许辅助、禁止代写"边界、deai 输出定位为可读性建议而非过检测保证、
--tier 与校级红线的对应建议（heavy ≈ 红线 ≤20% 的学校）。零"规避检测"措辞。

## 测试

新建 tests/test_latex_thesis_zh_checker_precision.py 覆盖各验收项；
更新 TestCheckConsistency.test_custom_terms_loading 适配新语义。
