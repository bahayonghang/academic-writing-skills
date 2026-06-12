# 补全 ZH fixture 论文工程与评测/测试覆盖

> 父任务：`06-12-latex-thesis-zh-optimization`（见其 prd.md §2 发现 F19/F20/F21）
> 优先级：P2 · 依赖：其余五个子任务（本任务是验收层，固化它们的成果）。

## Goal

给 latex-thesis-zh 一个可真实执行的端到端验收基础：仓库内置多文件中文学位论文
fixture 工程、与之绑定的 evals、未测脚本的单测补全，以及孤儿文件清理。

## Requirements

### R1 fixture 论文工程（F19 基础）

- 在 `tests/fixtures/latex_thesis_zh/`（与 paper_audit fixture 并列）创建一个
  最小但真实的多文件工程：
  - `main.tex`：thuthesis 风格骨架（`\documentclass{thuthesis}` 可不真实编译，
    但 documentclass/include 结构真实），`\include` 5 个章节文件；
  - `chapters/`：绪论（含可检出的漏斗问题）、相关工作（含作者年份罗列 + 缺研究
    空白推导）、两个方法章（标题均含"方法"，覆盖同名 section 回归）、实验章
    （含项目汇报式写法）、结论（不回应绪论承诺，触发 C3）；
  - `references.bib`：含 @phdthesis/@online/@techreport/@article 的缺字段条目
    （服务 gb7714 验收）；
  - 一个 GB18030 编码的边角文件（服务编码验收）；
  - 章节正文埋入已知数量的 deai 痕迹（空话/破折号/排比），数量写入 fixture README
    作为断言基准。
- fixture 总规模控制在 ~300 行以内正文，README 列出"埋点清单"
  （每个已知问题 → 预期被哪个模块检出）。

### R2 evals 升级（F19）

- `evals/evals.json` 至少 6 条核心用例的 `files` 字段指向 fixture 工程
  （compile 类除外——不要求 CI 装 TeX），`expected_output` 与埋点清单对齐；
- 断言从"输出提到模块名"升级为可验证事实（如"报出 chapters/related.tex 的
  罗列模式行号""报出 @phdthesis 缺 school"）；
- trigger_eval.json 不动（已是高质量基线，避免触发率漂移）。

### R3 单测补全（F21）

- 为以下脚本补 pytest（沿用 `_load_zh()` 模式）：`check_format`（中文标点/
  oral_expression 过滤行为）、`check_references`（undefined ref/多文件 include）、
  `deai_batch`（章节切分与报告路径）、`generate_table`（CSV→三线表）、
  `online_bib_verify`（仅离线部分：entry 解析与 mismatch 判定，网络调用 mock）。
- 用 fixture 工程跑 SKILL.md 全部 13 条路由主命令的冒烟测试（subprocess，
  断言 exit code 与输出非空/含预期标记），固化"文档命令可执行"这一父任务验收。

### R4 孤儿清理（F20）

- `references/formatting/caption-guide.md`：并入 `formatting/table-guide.md`
  或被 modules/tables.md 引用（内容尚可用），二选一；
- `references/writing/writing-philosophy-zh.md`：评估内容价值——有价值则从
  deai/guide.md 或 thesis-writing-guide.md 建立入链，无增量则删除；
- `references/university-templates/yanshan.md`：已由 zh-template-knowledge
  任务处理，本任务只做最终孤儿扫描复核（无入链文件清零）。

## Constraints

- fixture 中的"论文内容"必须是显然虚构的占位研究（避免被当成真实学术内容），
  但 LaTeX 结构必须真实；不得包含真实人名/真实文献条目（.bib 用虚构键名+
  虚构标题，符合 Critical Rules 零捏造的反向要求：fixture 明示虚构）。
- 冒烟测试不得依赖系统 TeX 安装（compile 模块只测 `--help`/工具缺失提示路径）。
- 不 bump version，只改 last_updated。

## Acceptance Criteria

- [ ] fixture 工程落盘且 README 埋点清单与各模块检出结果一一对应。
- [ ] 13 条路由主命令冒烟测试在 CI 通过（无 TeX 环境）。
- [ ] 5 个未测脚本各有 ≥3 个有效断言的测试；`just test` 通过。
- [ ] evals.json 核心用例可被 skill-creator 评测流程真实执行（files 可达）。
- [ ] 全仓孤儿扫描：references/ 下无任何文件缺少入链。
