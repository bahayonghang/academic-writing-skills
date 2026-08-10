# 仓库摸底与审阅核验结论（实施代理必读）

> 来源：本会话三路 Explore 摸底 + Codex 审阅报告逐条核验（2026-08-09）。所有行号已在当期
> HEAD 实证，实施时如遇偏移以符号名定位。

## 1. 现状差距（为什么做）

- zh `references/writing/method-chapter-guide-zh.md`：章级骨架完备（章引言承上启下、实验 E-* 八项、
  P-PAPER 拼接感），模块级叙述契约缺位；§四只管框架图/公式量/"式中"释义。
- EN `references/writing/section-writing/method.md`：有 Module Triad（动机/设计/优势）与逐模块
  预写表；缺逐边接口、连接类型、M-NONDIRECT、公式闭环、报幕反模式。
- typst：无方法节参考（无 section-writing 对应物）；镜像惯例 = EN 权威 + 注记
  （`modules/LOGIC.md:86`、`modules/EXPERIMENT.md:46`）。
- 三边脚本层零覆盖：模块间数据流检查、报幕句检测（deai throat_clearing 只匹配
  `^In this (section|chapter|paper|work), we`）。
- paper-audit：C5 段落级邻接（critical_reviewer_agent.md:98-114）与 C3 章级闭合之间存在
  模块级空隙；`REVIEW_LANE_GUIDE.md:9-10` section_methods 只有一行定义；
  `SUBAGENT_TEMPLATES.md:58-62` section lane 无专属 focus block。

## 2. 关键机制事实（怎么接）

### 2.1 audit Phase 0 委托与解析（C3 核心）

- `paper-audit/scripts/audit.py:372-425` `_resolve_script`：logic 检查按 fmt/lang 委托
  EN/ZH/TYPST 的 `analyze_logic.py`（.typ→typst；lang=zh→zh 优先；否则 en）。
- `audit.py:2465`：logic 的 extra_args 只有 `["--cross-section"]`，单次调用。
- EN/typst `analyze_logic.py:750-767`：节级检查 `if not section` 门控；`--section` 存在时
  cross-section/tri-section/motivation-thread 全部关闭。**推论：给现有调用直接加
  `--section methods` 会关掉全文检查，必须双调用（原调用不动 + 新增方法节调用）。**
- `audit.py:458-514` `_parse_script_output`：逐行成 issue；结构化正则只认
  `Critical|Major|Minor` 与 `P[012]`；finding 块的续行（Current/Suggested/Rationale/
  Meaning-Check）各自成 Minor/P2 issue。**既有膨胀缺陷**：一条 4 续行 finding → 5 条 issue；
  Info/P3 头行落回 Minor/P2。ScholarEval 扣分 Minor -0.5（`scholar_eval.py:59-63`），
  5 条 Minor = soundness 10→7.5。修解析会改变现有委托检查的分数基线，回归须显式处理。
- `audit.py:2586-2593`：只有 Phase 0 脚本 issue 进 `evaluate_from_audit`；LLM 车道发现不进分数。
- `audit.py:517-529` `_lane_from_section`：method/methods/approach/model → section_methods。

### 2.2 zh 方法章判别（C1 核心）

- zh `parsers.py:107-109,168,185`：method 章 = 标题含 `方法|原理|设计`（章级正则）。
- zh `analyze_experiment.py:105,107,466-484`：`--per-chapter` 章集合 = level-1 章 −
  `NON_METHOD_CHAPTER_RE`（绪论|引言|结论|总结|展望|综述）且**含实验节**（EXP_SEC_RE：
  实验|案例研究|仿真验证|结果分析|应用验证）。
- **两套机制口径不同**（正向关键词 vs 负筛+实验节），都不适合直接当 M-* 作用域 → 已决策：
  显式选章。zh `analyze_logic.py:1873-1903` 已有 `--section`（接受中文章名/英文键）与
  `--process-chapter`"开关 + --section 选章"先例，`--method-narrative` 沿用同型。

### 2.3 双语资源契约（C1/C2/C3 全部涉及）

见 `.trellis/spec/academic-writing-skills/docs-bilingual-resources.md`（jsonl 已挂）：

- 公开源范围含 `references/**/*.{md,yaml,yml}` 与 `agents/**/*.md` → **paper-audit 的
  references 与 agents 改动同样触发 manifest + 双语义务**。
- 方向：`sourceLocale` 同语言页面与源一致（仅链接目标可重写）；**另一语言页面做完整翻译**。
  zh 源 → docs/zh 一致镜像 + docs/（英文站）完整英文译文；en 源反之。
- 动作链：`check_resource_sync.py --write-manifest` → 双语页 → `--skill <skill>` →
  全量 checker + VitePress build（`just doc-build`）。双语校验不在 `just ci` 内。

### 2.4 其他契约锁

- `tests/contracts/test_skill_contracts.py`：SKILLS 硬编码模块字典（不加新模块名即不触碰）、
  ROUTER_ROW_RE + 子进程 `--help` 校验（路由行展示的开关必须在 help 里）、REFERENCE_LAYOUTS
  目录闭集（zh `references/writing/` 合法；paper-audit 不受此锁）。
- `test_skill_versions.py`：version 等于 pyproject，本任务只改 last_updated。
- `test_writing_modules_alignment.py`：EN/typst analyze_logic 为 Tier-2 同构副本（手工镜像，
  无散列锁）；Tier-1 组散列锁不涉及本任务改动面。
- zh 测试规范写法：`tests/skills/latex_thesis_zh/test_body_chapters.py:23-51`（importlib 加载、
  字符串常量合成 fixture、三断言形态：病例全触发/合规零发现/无开关不触发）。
- evals JSON 改动走 Bash python 写入（格式化 hook 会压平数组）。

### 2.5 行内小标题的三处合法用法（M-HEADING 红线负例）

1. EN `style-guide.md:160-167` / typst `STYLE_GUIDE.md:174`：Related Work 分组
   `\textbf{X methods.}` / `*X methods.*` 为正面范式。
2. typst `modules/EXPERIMENT.md:21-25`：实验分析段强制 `*Title Case Heading.*` lead-in。
3. zh `analyze_experiment.py:44`：要求 `\paragraph{核心结论概括}`。

### 2.6 agent 职责边界（C3 措辞约束）

- `methodology_reviewer_agent.md:7`（"do NOT evaluate writing quality"）与
  `critical_reviewer_agent.md:27`（DON'T "Comment on writing quality or formatting"）。
- **审计侧一律以"方法论接口与论证完整性"命名本能力**，不用"写作质量/叙述质量"措辞；
  报幕句式等风格判据只留 Phase 0 脚本车道。

## 3. Codex 审阅 9 条的核验判定（2026-08-09）

| # | 判定 | 处置 |
| --- | --- | --- |
| 1 解析膨胀/Info 语义 | 属实（audit.py:458-514 实证） | C3 增块感知解析 + Info/P3 设计 |
| 2 双调用缺失 | 属实（audit.py:2465 + EN:750-767） | C3 设计定稿为双调用，A/B 留白删除 |
| 3 zh 作用域不可执行 | 属实（两套判别机制实证） | C1 改显式 `--section` 选章 |
| 4 双语方向反了/审计资源漏同步 | 属实（spec §3 实证） | C1 方向改正；C3 补全链 |
| 5 Phase 1 工件不全 | 属实 | 本目录 research/ 三文件 + 父 implement.md + jsonl 已补 |
| 6 lane 归属冲突 | 部分属实（section lane 由通用 lane 子代理执行，非 methodology 角色；但两 agent 的 writing-quality DON'T 冲突成立） | 措辞框架改"接口与论证完整性"（§2.6） |
| 7 判据无锁/typst 公式留白 | 属实（父 design 与 C1 已有 3 vs 3+2 漂移） | 父 design §2 为唯一权威表 + C2 增契约测试；typst M-EQUATION 决策=仅 labeled 块公式 |
| 8 中途 commit 违流程 | 属实（trellis-implement 禁 commit） | 三份 implement.md 改为"提交分组建议（Phase 3.4）" |
| 9 C2 范围混入 | 属实 | sequence 扩类保留（M-SEQWORD 依赖）；example 扩类与 LOGIC.md:86 大小写修复移出，登记遗留清单 |

## 4. 遗留清单（本任务不做，待另行小任务）

1. EN/typst `TRANSITIONS` example 类扩充（文档五类 vs 脚本三类的剩余缺口）。
2. typst `references/modules/LOGIC.md:86` 引用大小写错误（`LOGIC.md` → `logic.md`，Linux 解析不到）。
3. audit `_parse_script_output` 膨胀缺陷对**其余**委托模块的影响面清理（C3 只保证 logic 链正确；
   若解析修复自然惠及其他模块，回归调整范围以 C3 设计为准）。
