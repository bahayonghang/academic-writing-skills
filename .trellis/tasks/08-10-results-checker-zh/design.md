# Design — 子任务 2（检查器实现与校准）

> 薄设计：判据唯一权威 = 父 `08-09-results-analysis-zh/design.md` §3（含 3.0 区间收集
> 算法与段落三元组、3.1 九项判据、3.2 十条防误报红线）。本文件只记录实现结构与测试
> 结构要点，不复述判据。

## 代码结构要点

1. 新增区间收集函数（返回 `[{start, end, chapter_start, chapter_end, source}]`）：
   双通道 + 排序 + 重叠去重（保留逐章通道项）；`--section` 走后缀族过滤分支。
   复用 `chapter_ranges()` / `split_sections()` / `EXP_SEC_RE` / `NON_METHOD_CHAPTER_RE`，
   不改 parsers.py。
2. 段落切分函数：raw 行块（空行分隔）→ `{start_line, raw_text, visible_text}`；
   `\ref` 探针查 raw，词面探针查 visible（父 design §3.0）。
3. RA-* 各为独立函数，签名统一 `(paragraphs, interval, chapter_window_raw/visible) ->
list[str]`；词表/阈值为模块级常量，常量名带 `RA_` 前缀（与 E-*/B3 常量隔离，
   `RA_METRIC_TERM_RE` 不改 `METRIC_TERM_RE`）。
4. `analyze()` 中 `--results-analysis` 为独立分支（与 `per_chapter` 同层），先执行区间
   收集，空区间时输出结构提示 Info（对齐既有 R4a 风格）。
5. RA-CAUSAL 分档与 RA-STAGE 语境排除的实现，各配一条指向父 design 判据号的注释；
   RA-CAUSAL 处另写 defensive-ai-rhetoric llm-only 分界注释。

## 测试结构要点

- 新测试文件 `tests/skills/latex_thesis_zh/test_results_analysis.py`（加载约定按
  testing-and-tooling.md，bare import 注意 conftest 只前置 EN/AUDIT 路径——zh 脚本用
  既有 zh 测试文件的导入方式）。
- fixtures 放既有 zh fixture 目录约定处；边界矩阵每格一个独立 fixture 或章节，测试名
  即矩阵格名（可追溯审阅 P2-6 六项）。
- 回归断言：默认模式与 `--per-chapter` 在既有 fixture 上输出不变（快照或关键行断言）。

## 标定流程要点（R8）

1. `decrypted/` 论文列表 → 逐篇 `--results-analysis` 只读运行（不落盘中间产物到仓库）。
2. 命中清单人工逐条标注 真/误报/存疑，写入本任务 `research/calibration-report.md`。
3. 裁决规则：单项检查在标定集上误报占多数 → 降级（Info 或纯 LLM 检查项）或裁掉；
   RA-INTERLEAVE 默认按此裁决；结果回写 guide §阈值与出处（文档改动随本任务提交）。

## 回滚

新旗标独立分支，revert 脚本+测试 commit 即恢复；路由/evals commit 独立可单撤。
