# C1 技术设计：zh 方法叙述检查器与参考文件

判据唯一权威 = 父 design §2（本文件不复述判据，只写 zh 实现落点）。机制事实见父
research/repo-recon.md。实现前通读 `analyze_logic.py` 现有结构（S1/_check_heading_leads、
_check_chapter_intro、--process-chapter 的 --section 配合方式、finding 输出惯例）。

## 1. 检查器实现落点

### 1.1 入口与作用域

- argparse 增 `--method-narrative`（store_true），help 写明"须配 --section 显式选章"。
- 主流程：开关开启时——
  1) 无 `--section`：收集候选章（父 design §2.5 三线索并集，复用 parser 的章标题正则与
     analyze_experiment 的 EXP_SEC_RE/NON_METHOD_CHAPTER_RE 同源模式常量，常量在本脚本内
     定义并注释出处，不跨脚本 import——保持技能可独立安装），打印清单，`return 2`。
  2) 有 `--section`：用现有 `--section` 解析机制定位章区间，仅对该区间跑四项；
     `--first-chapter` 语义不变。
- 文本处理一律走 parser visible text 通道；`\cite`/`\ref`/数学环境保护不变。

### 1.2 四项检查

- M-HEADING / M-SEQWORD / M-EQUATION：各一函数，判据常量（阈值 3/2、后视 3 行、正则源串）
  以模块级常量定义，命名带 `MN_` 前缀（method-narrative），注释标注"唯一权威=父任务
  design §2，由 tests/contracts/test_method_narrative_alignment.py 锁定（C2 交付）"。
- 常量组织（供契约测试 import 断言）：
  `MN_HEADING_RUN = 3`、`MN_HEADING_HITS = 2`、`MN_EQUATION_LOOKAHEAD = 3`、
  `MN_ANNOUNCE_RE_ZH`、`MN_SEQ_OPEN_RE_ZH`、`MN_CAUSE_EXEMPT_RE_ZH`、`MN_EQ_GLOSS_RE_ZH`。
- M-EDGETABLE：从选中章区间的 `\subsection`/`\subsubsection` 标题序列生成逐边空白表，
  追加在诊断输出尾部，标 `[LLM] 待填写`。

### 1.3 输出

- finding 格式对齐现有：`% <位置> [Severity: X] [Priority: Y]: [Script] M-XXX <消息>` +
  Current/Suggested/Rationale 续行 + Meaning-Check: NEEDS-LLM。
- M-HEADING 只报一条（首命中处，含计数）；M-SEQWORD/M-EQUATION 逐处报。

## 2. 参考文件结构

- 内容清单 = prd R1（十项），转写核对源 = 父 research/user-spec-method-description.md。
- 开头诊断入口代码块（对齐 method-chapter-guide-zh.md 惯例）：
  `uv run python $SKILL_DIR/scripts/analyze_logic.py document.tex --method-narrative --section 〈章名〉`。
- 六角色/连接类型/四类主张三张表沿 spec 结构，措辞按仓库文风重写；豁免清单独立小节。
- 篇幅 ≤ method-chapter-guide-zh.md（265 行）。

## 3. 测试设计

新文件 `tests/skills/latex_thesis_zh/test_method_narrative.py`：

- `_load_zh()` 照抄 `test_body_chapters.py:23-46`（sys.modules 保存恢复）。
- fixture 常量（合成通用流程工业样本，脱敏）：`_SICK_METHOD`、`_COMPLIANT_METHOD`、
  `_EXP_PARAGRAPH_OK`（实验节 `\paragraph{核心结论概括}`）。
- 断言组 = prd R3 五组（含"有开关无 --section 非零退出 + 候选清单"与"--section 只扫选中章"）。

## 4. 风险与回滚边界

- 风险：`--section` 中文章名匹配对 `\chapter{基于XX的YY方法}` 类长标题的鲁棒性——实现时沿用
  现有 `--section` 的匹配语义不另造；测试加一条长章名定位断言。
- 提交分组建议（Phase 3.4 由主会话执行，实施代理不 commit）：
  A 组＝检查器 + 测试（`feat(latex-thesis-zh): 方法叙述候选检查 --method-narrative`）；
  B 组＝参考文件 + modules/logic.md + SKILL.md + manifest + 双语页（`feat(latex-thesis-zh):
  方法描述规范参考与文档同步`）。A/B 均可独立回滚；finding 中引用参考文件路径的字符串
  须落在 B 组之后仍自洽（实现时 finding 建议文案不写死尚未存在的文件路径，A 组先用模块名指路）。
