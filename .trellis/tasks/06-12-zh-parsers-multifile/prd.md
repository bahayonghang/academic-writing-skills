# 修复 parsers 章节切分与多文件论文解析

> 父任务：`06-12-latex-thesis-zh-optimization`（见其 prd.md §2 发现 F3/F4/F11/F22）
> 优先级：P0 —— 这是其余子任务的地基，必须最先执行。

## Goal

让 latex-thesis-zh 的全部分析脚本在**真实的多文件中文学位论文工程**（thuthesis/pkuthss
风格：main.tex 只含 `\include{chapters/chap01}` 骨架）上产生正确、完整的诊断，
并修复 `parsers.LatexParser.split_sections` 的三个静默漏检缺陷。

## Requirements

### R1 多文件解析（F3）

- 提供一个共享的"内容装配"能力：从入口 .tex 递归解析 `\input{}`/`\include{}`/`\subfile{}`，
  按文档顺序拼接内容，并维护"拼接行号 → (源文件, 源行号)"映射，使诊断输出仍能报告
  `文件:行号`。可参考并统一 `map_structure.py:78-140` 与
  `check_references.py:346-369` 已有的两套实现（消除第三套重复）。
- 接入对象（当前全部单文件直读）：`analyze_logic.py`、`deai_check.py`、
  `analyze_abstract.py`、`analyze_experiment.py`、`analyze_literature.py`、
  `check_tables.py`、`check_format.py`、`optimize_title.py`、`check_consistency.py`
  （后者改用 include 图替代 rglob，见 checker-precision 任务 F17 的接口约定）。
- 循环 include 防护、缺失文件提示（不静默跳过——`% WARN` 列出未找到的 include）。

### R2 split_sections 缺陷修复（F4）

- (a) 同名 section key 不再互相覆盖：值改为区间列表或 `method_1/method_2` 形式
  （需评估对现有调用方的影响并同步修改，所有调用方在本 skill 内部）。
- (b) 跳过 `%` 注释行（与 TypstParser 行为对齐，注意 `\%` 转义）。
- (c) 标题匹配容错：`\chapter*{}`、标题内空格/`\quad`/`~`（如 `绪\quad 论`）、
  可选参数 `\chapter[短标题]{长标题}`。
- 未匹配任何 SECTION_PATTERNS 的正文章不得从全文档检查中消失：
  split_sections 之外提供"全部章节区间"的枚举途径（基于 extract_headings level-1）。

### R3 `--section` 用户体验（F11）

- `--section` 同时接受英文键与中文章节名（绪论/相关工作/结论等，做同义映射）。
- 找不到章节时，错误信息列出本文档实际可用的 section 键与对应标题，而非只报"未找到"。

### R4 编码健壮性（F22）

- 读取 .tex 时先按 utf-8 严格解码；失败则尝试 GB18030；仍失败才回退
  `errors="replace"` 并在输出头部加 `% WARN: 编码异常` 提示。不允许静默乱码后报"无问题"。

## Constraints

- ZH parsers.py 是文档化的特化变体，受 `tests/test_parsers_alignment.py` 哈希锁定：
  `LatexParser.PRESERVE_PATTERNS`、`TypstParser.PRESERVE_PATTERNS`、`_normalize_whitespace`
  必须与 EN 拷贝保持哈希一致；若本任务需要改这些共享成员，必须按测试文件头部说明
  先改 latex-paper-en canonical 再镜像，且单独评估对兄弟 skill 的影响。
- 不 bump SKILL.md version（与 pyproject 同步规则），只改 last_updated。
- 输出契约不变：`% MODULE (L##) [Severity] [Priority]: ...`。

## Acceptance Criteria

- [ ] 对 fixture 多文件工程（main.tex + 5 个 include 章节，见 zh-fixtures-evals 任务；
      本任务可先放最小版 fixture）运行 `analyze_logic.py main.tex`，能报出位于
      include 文件内的导语缺失/章引言问题，且行号指向源文件。
- [ ] 构造"两章标题均含'方法'"的文档，两章都出现在章节级检查范围内（回归测试）。
- [ ] 注释掉的 `%\chapter{结论}` 不再产生 conclusion 区间（回归测试）。
- [ ] `\chapter*{摘要}` 与 `绪\quad 论` 均被正确识别（回归测试）。
- [ ] `--section 绪论` 与 `--section introduction` 等效；非法值时输出可用列表。
- [ ] GB18030 编码的 fixture 文件可正常分析或显式告警，无静默乱码。
- [ ] `just ci` 全绿，`test_parsers_alignment.py` 不被破坏。
