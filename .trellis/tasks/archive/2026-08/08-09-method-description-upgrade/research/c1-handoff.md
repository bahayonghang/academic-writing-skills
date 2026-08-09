# C1 交接：latex-thesis-zh 方法叙述检查

> 这是已实现接口的交接快照；M-* 判据仍以父任务 `design.md` §2 为唯一权威。

## Runtime surface

- CLI：`analyze_logic.py <file> --method-narrative --section <章名>`；缺少 `--section` 时输出
  候选章并以状态码 2 退出。
- Python：`analyze(file_path, section=None, cross_section=False, motivation_thread=False,
  intro_mainline=False, process_chapter=False, first_chapter=None, method_narrative=False) -> list[str]`。
- 默认兼容性：未传 `--method-narrative` 时沿用既有 logic 检查路径。

## Shared symbols

- 结构常量：`MN_HEADING_RUN=3`、`MN_HEADING_HITS=2`、`MN_EQUATION_LOOKAHEAD=3`。
- 中文正则：`MN_ANNOUNCE_RE_ZH`、`MN_SEQ_OPEN_RE_ZH`、`MN_CAUSE_EXEMPT_RE_ZH`、
  `MN_EQ_GLOSS_RE_ZH`。
- 检查入口：`_check_method_heading`、`_check_method_sequence`、
  `_check_method_equations`、`_method_edge_table`、`_check_method_narrative`。

## Validation evidence

- 方法叙述专项：11 passed；`latex-thesis-zh`：474 passed。
- 最终 `just ci`：1424 passed；Ruff 通过；变更文件 Pyright 0 errors / 0 warnings。
- 单技能资源同步：255 entries；全量资源检查、`just doc-build`、`git diff --check` 通过。
- 检查代理修复并锁定：通用 logic 路由保留、行内注释/受保护 token、公式组/小节边界、
  含 LaTeX 间距命令的章标题规范化。

## Remaining evidence

真实论文语料上的启发式查准率仍未验证；当前证据仅覆盖合成病例、合规例与合法标题负例。
