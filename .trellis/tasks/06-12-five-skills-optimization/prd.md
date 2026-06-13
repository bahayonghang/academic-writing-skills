# PRD: 五技能审计与优化（父任务）

> 审计日期：2026-06-12/13 · 审计范围：除 latex-thesis-zh 外的五个 skill
> （latex-paper-en 87 文件/13.2k 行、typst-paper 70/12.4k、paper-audit 90/17.0k、
> cover-letter 39/4.5k、bib-search-citation 13/2.2k）
> 方法：全量脚本代码审读 + 内容文件审计 + 临时目录投喂实测取证 + 网络调研
> （venue 2026 事实、ICMJE/出版商 AI 政策、Typst 生态、BibTeX/biblatex 现状、API 现状）。
> 方法论与任务树结构沿用 `06-12-latex-thesis-zh-optimization`（F1-F24，已全量修复）。
> 各 skill 完整审计报告在本任务 `research/` 目录（共 7 份文件，含 2 份外部事实基线）。

## 1. 背景与动机

latex-thesis-zh 的 F1-F24 审计修复（2026-06-12，7 commits）只覆盖了六技能套件
之一。本次对其余五个 skill 的同方法审计证实：**ZH 发现的 18 类系统性模式在
姊妹 skill 中大面积复现**（typst-paper 复现 14 类、latex-paper-en 复现约 12 类），
且 ZH 当时的修复（split_sections 重写、tex_loader 多文件装配、PyYAML 降级、
read_text_robust）**从未回灌到 EN 规范拷贝**——四份 parsers.py 拷贝
（EN/typst/audit/cover-letter）至今共享同一套已知坏行为。

### 跨 skill 系统性结论（按危害排序）

1. **解析底座统一塌方**：EN 系 `split_sections` 对 `\section*{}`、复数标题
   （Methods/Experiments）、`%` 注释行、同名章节全部失效（E2/T21/C10）；
   全部脚本只读单文件不解析 `\input`/`#include`（E6/T6/C3）。这是其余一切
   章节级检查假阴性的根源，对应地基子任务 `06-13-en-family-parsers`。
2. **检查器静默假通过**（最危险类别）：EN format 模块对任何输入永远 PASS
   （chktex 解析正则错位，E1）；typst check_references 对任何带引用论文 100%
   误报 Critical（T1）；deai 未知章节名静默 0 检出（E4/T19）；bib 解析器
   静默吞条目（B1/B2）。
3. **路由表/模块文档与脚本契约错位**：照 SKILL.md 或模块文档原样执行即报错
   或静默关闭检查（E5/T3/T12-T15/C9——typst 约半数模块文档描述的是 LaTeX
   姊妹版 CLI；cover-letter MODE_GUIDE 有 5 个幽灵 flag）。
4. **知识层过时/错误**（网络调研证实）：venue 事实 9 处错误（NeurIPS +0 页、
   AAAI +1 页、arXiv 1500 字符、"LaTeX required for all venues" 等，E20）；
   Typst 推荐配置含不存在的参数照抄必编译失败（T9/T10/T11）；包版本钉死过时
   （charged-ieee 0.1.0 vs 现行 0.1.4，T30）。
5. **2025-26 政策合规缺口**：ICMJE 2026.1 明文要求 AI 使用在 cover letter 披露
   而 skill 声明体系无此项（C5）；EN deai 模块帮用户消 AI 痕迹却无任何 venue
   披露义务知识（E21）；推荐审稿人机制行业收紧未对接（C7）。
6. **PyYAML 硬依赖崩溃面**（ZH F8 同病未同修）：EN/typst deai_check 构造函数
   无条件 import yaml（E3/T23）；cover-letter presubmission/journal-fit 同病（C16）。
7. **evals 形同虚设**：EN 19 条、typst 12 条全部 `"files": []` 无 fixture
   （E24/T27）；bib evals 断言恒真（B23）。cover-letter 是唯一例外（4 个真实
   fixture，健康）。

### 外部环境变化要点（全部有来源，详见 research/ 各文件）

- **venue 2026 事实**：NeurIPS 9+1 页（样式按年命名）、ICML "Impact Statement"
  正式名、AAAI 取消免费 camera-ready 加页（$300/页购买）、arXiv 摘要 1920 字符、
  arXiv CS 2025-10-31 起综述/立场文须同行评审证明、ACL/AAAI 接受 Word、
  acmart v2.18 八合一模板（2026-05-31）、ACM 2026-01-01 全面 OA。
- **AI 披露政策**：ICMJE 2026-01 版新增 Section V（cover letter + 稿内双重披露，
  未披露可构成不端）；Science/APS/NEJM 明文要求 cover letter 披露；Elsevier 稿内
  声明段、IEEE 致谢节、ACM 纯写作辅助免披露；ICLR/COLM 重大使用专节披露否则
  desk reject；CVPR 虚构引用可不经评审直接拒。
- **Typst 生态**：现行 0.14.2（0.15-rc1 已出）；`page` 无 `column-gutter` 参数；
  内置 GB/T 7714 样式 id 为 `gb-7714-2015-numeric` 等（无 2025 版）；charged-ieee
  0.1.4；algorithmic 1.0.7 / lovelace 0.3.1 API 已变；IJIMAI 成为首个官方接受
  Typst 投稿的 JCR 期刊，IEEE/ACM/arXiv 仍不收 Typst 源。
- **biblatex/检索生态**：`journaltitle`/`date` 是 biblatex 原生字段（Better
  BibLaTeX 默认导出）；GB/T 7714-2025 对检索层影响间接（@dataset/@online 条目
  增多）；OpenAlex 2026-02-13 起强制 API key；Crossref 2025-12 新限流。

## 2. 发现编号索引

| 系列 | skill | 数量 | 报告文件 |
|------|-------|------|----------|
| E1-E29 | latex-paper-en | 29 | `research/latex-paper-en-audit.md`（+ `latex-paper-en-venue-factcheck.md`） |
| T1-T40 | typst-paper | 40 | `research/typst-paper-audit.md` |
| B1-B26 | bib-search-citation | 26 | `research/bib-search-citation-audit.md` |
| C1-C23 | cover-letter | 23 | `research/cover-letter-audit.md`（+ `cover-letter-policy-research.md`） |
| A1-A8 | paper-audit | 8 | `research/paper-audit-audit.md`（主会话补做，含 §5 覆盖声明） |

## 3. 子任务映射

| 子任务 | 优先级 | 覆盖发现 | 依赖 |
|--------|--------|----------|------|
| `06-13-en-family-parsers` | P0 | E2/E4(土壤)/E5(脚本侧)/E6/E9、T6/T7/T21、C2/C3/C10 的 parsers 拷贝层 | 无（**最先做**） |
| `06-13-bib-robustness` | P0 | B1-B26 | 无（可与地基并行） |
| `06-13-en-paper-precision` | P0 | E1/E3-E29（消费地基 API） | en-family-parsers |
| `06-13-typst-reality` | P0 | T1-T5/T8-T40（消费地基 API） | en-family-parsers |
| `06-13-cover-letter-compliance` | P1 | C1/C4-C23（消费地基 API） | en-family-parsers |
| `06-13-paper-audit-integrity` | P1 | A1-A8 | en-family-parsers（仅 A8） |

执行顺序建议：en-family-parsers → bib-robustness（并行无依赖）→
en-paper-precision / typst-reality / cover-letter-compliance / paper-audit-integrity
（地基落地后可并行，注意多个任务都会改 conftest/contract 测试，建议串行合并或
分批提交避免冲突）。每个子任务一个 commit，scope 按 skill（仓库提交惯例）。

paper-audit 是六技能中最健康的（无 P0），其 A 系列以学术诚信与文档校正为主，
可作为低风险先行试点验证修复流程。

## 4. 跨子任务验收标准（父任务集成验收）

1. **路由表全量可执行**：五个 skill 的 SKILL.md 路由表主命令对各自 fixture
   工程按文档原样执行（仅替换 `$SKILL_DIR` 与入口文件）即产生非空、正确诊断；
   不存在照抄报错或静默假通过。
2. **多文件工程生效**：EN（\input）与 Typst（#include）的多文件 fixture 上，
   章节级检查、bib 一致性、align-check 产出与单文件等价的结果。
3. **模板工程生效**：charged-ieee fixture 的 title/abstract 提取、版式检查
   零误报。
4. **事实单源**：同一 venue/模板事实（页数、样式文件名、包版本）在每个 skill
   内只有一处权威定义；全仓事实抽查与 research/ 基线一致。
5. **裸环境可运行**：模拟无 PyYAML 环境下，全部脚本可运行或优雅降级
   （无 ImportError 崩溃）。
6. **四拷贝哈希锁更新且 ZH 零改动**：test_parsers_alignment 全绿，
   latex-thesis-zh 目录 diff 为空。
7. `just ci` 全绿；SKILL.md version 不 bump，只改 last_updated。

## 5. 范围外（明确不做）

- 不动 latex-thesis-zh（已完成 F1-F24 修复，有意分化受 [[latex-thesis-zh-audit-2026-06]] 保护）；
- 不新增"从零写论文"能力（各 skill Do Not Use 边界保持）；
- deai/AI 披露相关改动仅做政策事实对接与可读性导向，不提供任何规避检测能力；
- 不引入新的第三方运行时依赖（PyYAML 一律降级为可选，与 ZH F8 同解法）；
- bib-search-citation 不扩展在线校验（OpenAlex/Crossref 新政仅记录为未来约束）。

## 6. 调研来源汇总

详见 `research/` 各报告的 §1 与两份外部基线文件。核心来源：CTAN（ieeetran/
acmart）、NeurIPS/ICML/ICLR/ACL/AAAI/CVPR/COLM 2026 官方 CFP 与 Author Guide、
arXiv blog/help、ICMJE 2026-01 Recommendations、Science/Elsevier/Springer/IEEE/
ACM/Wiley AI 政策页、Typst changelog/Universe/hayagriva issues、biblatex 手册、
Better BibTeX 文档、Retraction Watch（Cureus 事件）、JIBS desk-reject 社论。
