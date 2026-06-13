# cover-letter 提取精度与 2026 投稿合规更新

> 父任务：`06-12-five-skills-optimization`（完整审计见其 `research/cover-letter-audit.md`
> C1-C23 + `research/cover-letter-policy-research.md` 政策基线）
> 优先级：P1 · 依赖：`06-13-en-family-parsers`（C2 标题平衡括号 / C3 多文件装配 /
> C10 章节切分由地基任务在 parsers.py 拷贝层修复，本任务消费其 API）。
> 其余发现不依赖地基，可并行。

## Goal

修复"提取 → 对齐校验"主链路在标准 LaTeX 模板（含 `\thanks` 的 \author、多文件
工程）上的系统性失效，消除 align-check 的误报+漏报双重失真；并把 2025-2026
投稿合规现实（ICMJE 2026.1 AI 披露、推荐审稿人收紧、ML 会议无 cover letter）
接入模板与检查器知识层。

## Requirements

### R1 稿件事实提取修复（C1/C2 — P0）

- C1 作者提取重写：`AUTHOR_COMMAND_PATTERNS` 的 `[^}]+` 换平衡括号捕获
  （parsers.py 已有 `_extract_balanced_block` 可复用）；`_clean` 的 `\thanks`
  剥离移到平衡捕获之后、丢弃判定之前；删除会从 thanks 文本抓 email 局部名的
  corresponding 回退正则（或限定在显式 `\corresponding` 类命令）。
  回归：NeurIPS 样式 `\author{X\thanks{...} \\ Dept...}` 与
  `\author{A\thanks{Corresponding author: a@u.edu} \and B}` 提取出正确作者列表，
  不再伪造通讯作者。
- C2 标题提取：`extract_title` 换平衡括号（地基任务在 parsers 层修复后接线），
  `\thanks` 资助声明不得泄入标题。

### R2 align-check 精度（C3/C4/C12/C14 — P0/P1）

- C3 多文件：extract_manuscript_facts / align_check 接入地基任务的 tex_loader，
  多文件工程下 facts 不再为空、真实有据主张不再全量误报。
- C4 `_has_numeric_match` 收紧到段落/滑动窗口共现（与 docstring "within the
  same paragraph" 对齐）；做不到窗口级的至少把全文档命中降级 `confidence: low`。
  回归：稿件他处分别出现 "73%" 与 "reduction" 时，信中 "73% reduction in memory"
  不得 verified。
- C12 claim 提取 12 条硬上限：取消或在 claim_map 输出 `truncated: true` + 总数。
- C14 `STRONG_CLAIM_PATTERN` 双副本失同步：提为单一常量模块，align_check 与
  build_letter_claim_map 共同导入。

### R3 2026 投稿合规知识（C5/C6/C7/C13/C22/C23 — P0/P1）

- C5 AI 披露体系（ICMJE 2026.1 Section V：AI 使用须在 cover letter + 稿内双重披露）：
  - 模板 frontmatter 新增 `ai_disclosure` 声明类型：nature/science/cell 系按
    ICMJE/出版商要求设 required（Science 明文要求 cover letter 披露），
    IEEE/ACM 标注"披露位置在稿内（致谢/Work 内）而非信中"；
  - `DECLARATION_PATTERNS` 同步加 ai_disclosure 匹配模式；
  - `LETTER_STRUCTURE.md` 声明清单补该项；
  - SKILL.md Safety Boundaries 加一条："本 skill 产出为 AI 辅助文本，提交前
    须核对目标期刊 AI 披露政策（部分期刊要求在 cover letter 中声明）"。
- C6 ML 会议边界：icml.md / cvpr.md 头部加 neurips.md 同款免责
  （"该 venue 主赛道无 cover letter 环节，OpenReview 表单替代"）；
  JOURNAL_TIERS.md conference 节同步说明。
- C7 suggested_reviewers 从 7 个模板的默认 optional 降为模板正文中的条件提示，
  附 2025-26 收紧背景（Cureus 取消、PLOS ONE 取消、Wiley/IOP 加固核验）。
- C13 nature/science 模板 data_availability 降为 optional，模板正文注明
  "Nature 系 cover letter 为机密渠道：COI/在审相关工作可在此沟通；
  data availability 走投稿系统/稿内"。
- C22 期刊知识补 2025-26 编辑实务：IEEE 期刊两极化（Proc. IEEE 强制 vs TIM
  "没事别交"）、双盲场景"曾读过稿件人员名单"、被拒重投说明（Wiley Small /
  IEEE ToN 强制）、Springer 固定声明句式。
- C23 禁语三方对齐：FORBIDDEN_PHRASES Tier1/3/4 与 presubmission_check J1 与
  PRESUBMISSION_RULES.md 统一为单一来源；Tier 4 要么实现要么删除"由脚本使用"声明。
  回归：optimize fixture 信中的 "your prestigious journal" 必须被命中。

### R4 检查器健壮性（C8/C9/C11/C16/C19/C20 — P1/P2）

- C8 `_scan_required_declarations` 对无 DECLARATION_PATTERNS 模式的 kind
  跳过并输出 `unknown-declaration-kind` info（不再无条件报 absent）。
- C9 MODE_GUIDE 按脚本真实 `--help` 重写：删 5 个幽灵 flag（`--out-format`、
  generate `--output`、`--strict`、optimize `--section`、journal-fit
  `--manuscript`），补 presubmission 章节与集成矩阵行，"four modes"改五模式。
- C11 `_read_letter` 加 `errors="replace"`（与套件其余读文件一致）。
- C16 PyYAML 去依赖：手写极简 frontmatter 解析（纯 list/str/int）或
  try-import 降级。
- C19 journal-fit 启发式局限在 SKILL.md/MODE_GUIDE 显式披露（scope_fit 关键词法、
  第一人称 claim 计数），输出标注 [Script] 置信度。
- C20 杂项：`--json` 空 flag 删除；生成稿 venue slug 改显示名；
  G1 em-dash severity 与 ISSUE_SCHEMA 对齐；examples 改用统一 CLI。

### R5 测试与触发（C15/C17/C18/C21 — P2）

- C17 `tests/test_cover_letter_scripts.py` 的 `_load` 修正：加载前后
  `sys.modules.pop("parsers")` + finally 恢复 sys.path；conftest 注释如实描述。
- C18 测试临时文件改用 `tmp_path`，不再写入仓库 fixtures 目录。
- C21 中文触发：description/when_to_use 增补"投稿信、致编辑信"等 token；
  trigger_eval 补 3-4 条中文正/负例。
- C15 死代码清理（`del contrib_str` 等）。

## Constraints

- parsers.py 拷贝改动一律走 `06-13-en-family-parsers`，本任务只动
  cover-letter 自有脚本与知识文件。
- align-check 的安全定位不变："Never disable align-check"、不可信数据声明、
  不联网边界保持。
- 不 bump version，只改 last_updated。

## Acceptance Criteria

- [ ] NeurIPS/article 两种 `\author{...\thanks{...}}` fixture：作者列表正确、
      无伪造 corresponding；`\title` 含嵌套花括号/\thanks 时标题完整且干净。
- [ ] 多文件工程 fixture：align-check 对稿件真实支持的 47%/2.1x 主张零误报。
- [ ] 伪主张（数字与度量词分处两段）不再 verified；claim>12 时输出 truncated 标记。
- [ ] 含 "We suggest the following reviewers" 的信不再误报 suggested_reviewers 缺失；
      含 "previously presented as a poster" 不再误报 prior_presentation 缺失。
- [ ] nature 模板 required 集含 ai_disclosure；含 AI 声明段的信通过，缺失时报 major
      并给出 ICMJE 出处提示。
- [ ] icml/cvpr 模板头部有"无 cover letter 环节"免责。
- [ ] "your prestigious journal" 被 presubmission_check 命中（Tier 4 对齐）。
- [ ] MODE_GUIDE 出现的每个 flag 都在对应脚本 `--help` 中存在（契约测试）。
- [ ] GBK 编码信件不再崩溃；缺 PyYAML 环境（monkeypatch）三脚本可运行。
- [ ] `just ci` 全绿且运行后仓库 fixtures 目录无残留临时文件。
