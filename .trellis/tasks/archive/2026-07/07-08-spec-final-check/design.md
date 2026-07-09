# design — 通用规范逐项终检机制与燕山2024清单

## 1. 边界与数据流

```
templates/<school>.md ──(解析 ## 逐项检查清单 表格)──> ChecklistItem[]
main.tex ──tex_loader.assemble()──> 全工程行流 + origin 映射
          ──parsers.LatexParser──> split_sections / extract_visible_text
ChecklistItem + 文档 ──check_spec.py 注册表──> ItemResult[] (PASS/FAIL/NEEDS-LLM/MANUAL/SKIP)
ItemResult[] ──report──> 逐项报告（文本 / --json）──> LLM 按 module 文档处理 NEEDS-LLM → 汇总
```

复用既有设施：`tex_loader.assemble`（多文件拼装 + origin）、`parsers.get_parser`（可见文本提取，
保证不误伤 `\cite`/math）、`map_structure.ThesisStructureMapper`（模板识别、章节定位）。
不新增第三方依赖。

## 2. 清单表格解析（通用契约）

- 定位 `## 逐项检查清单` 二级标题，收集其下第一个 markdown 表格的数据行（跳过表头与 `---` 行）。
- 每行 `|` split → strip；容忍格式化 hook 对表格做的空格重排（解析基于单元格内容，不依赖对齐）。
- 校验：5 列；ID 匹配 `^[A-Z]{2,4}-\d{2,3}$`；检查方式匹配
  `^(script:[a-z0-9_]+|module:[a-z-]+|llm|manual)$`；适用 ∈ {通用, 硕士, 博士}。
- 解析器作为 check_spec.py 内的独立函数 `parse_checklist(md_path) -> list[ChecklistItem]`，
  供脚本与契约测试共用（测试用 importlib 按路径加载 zh 副本）。

## 3. check_spec.py 架构

```python
@dataclass
class ChecklistItem: id, requirement, basis, method, scope
@dataclass
class ItemResult: item, status, evidence  # status: PASS|FAIL|NEEDS-LLM|MANUAL|SKIP

CHECKERS: dict[str, Callable[[Ctx], CheckOutcome]]   # checker key -> 实现
TEMPLATE_THRESHOLDS: dict[str, dict]                  # 模板 id -> 学位分档阈值
```

- `Ctx` 一次性预计算：assemble 文档、章节切分（绪论/结论/致谢/成果按标题正则识别）、
  可见文本、bib 条目（`--bib` 或自动发现 `\bibliography`/`\addbibresource`）、degree、模板 id。
- 状态判定：`script:` 有检查器 → PASS/FAIL(+证据)；检查器缺前置输入（如无 bib、无摘要环境）→
  NEEDS-LLM 并说明缺什么；`--spec-file` 引用未知检查器 → NEEDS-LLM（降级不中断）。
  `module:`/`llm`/`manual` 原样透传状态（module 状态文案附既有模块命令）。
  `适用` 与 `--degree` 不符 → SKIP。
- 退出码：有 FAIL → 1，否则 0（与 check_format.py 语义一致）。

### v1 内建检查器（约 16 个，全部为源码静态可判定）

| checker key | 判定 | 依据 |
| --- | --- | --- |
| title_len | 题名 ≤25 字 / 含副题名合计 ≤35 字（\title 或封面字段可得时） | §1.1 |
| abstract_no_cite | 摘要环境内无 `\cite`/figure/table/公式环境 | §1.3.1 |
| kw_count | 中文关键词 3~8 个、分号分隔 | §1.3.2 |
| kw_zh_en_match | 中英关键词数量一致 | §2.2 |
| abstract_len | 摘要字数 硕 500~650 / 博 900~1200（±10% 缓冲报 WARN 级 FAIL 说明） | §2.2 |
| abstract_order | 中文摘要在前、英文在后 | §2.2 |
| chapter_summary | 各正文章含「本章小结」节（绪论/结论豁免；缺失列章名，方法/材料章豁免留给 LLM 复核） | §1.5.2 |
| conclusion_no_cite | 结论章无 `\cite` | §1.5.3 |
| conclusion_len | 结论 ≤2000 字 | §1.5.3 |
| conclusion_hedge | 结论无「大概/或许/可能是」 | §1.5.3 |
| bib_count | 参考文献总数 博 ≥100 / 硕 ≥40 | §1.6 |
| bib_recency | 近五年 ≥1/3 且含近两年文献（bib year 字段统计） | §1.6 |
| wordcount | 正文/绪论字数区间（可见文本近似，报告注明口径） | §2.1 |
| heading_len | 各级标题 ≤15 字 | §2.4 |
| heading_depth | 层次 ≤4 级（paragraph 以下即超） | §2.4 |
| cite_in_heading | 标题参数内出现 `\cite` | §2.5 |
| new_page_chapter | 章使用 `\chapter`（另起一页由文档类保证）；手写大标题告警 | §2.4 |
| appendix_letter | 附录用 `\appendix`/大写字母编号 | §2.14 |

（title_len 若入口无 `\title` 类字段 → NEEDS-LLM；wordcount 阈值取
TEMPLATE_THRESHOLDS[template][degree]，未知模板用 GB/T 7713.1 无阈值 → 只报数不判定。）

## 4. yanshan.md 清单条目映射（写作蓝图）

ID 分配按规范章号排布，全部以 research 提取文本为准（约 45~55 条）：

- `YS-01~08` 内容要求 §1.1~1.4：题名长度/中英对照、副题名规则、摘要写法（llm）、
  摘要禁项（script:abstract_no_cite）、关键词数量（script:kw_count）、目次到三级标题。
- `YS-09~18` §1.5~1.8：绪论要素（llm）、研究内容将来时/忌目次式（llm）、本章小结
  （script:chapter_summary）、结论不引文献/≤2000字/分条创新点/忌模糊词
  （script + llm）、参考文献数量与近五年占比（script:bib_count / bib_recency）、
  教材不宜引用与本人论文不列入（llm）、成果类型（llm）、致谢简朴（llm）。
- `YS-19~45` 书写要求 §2.1~2.18：正文字数（script:wordcount）、摘要字数（script:abstract_len）、
  中英摘要顺序（script:abstract_order）、每章另起页（script:new_page_chapter）、
  标题长度/层次（script:heading_len / heading_depth）、引用标注形态与不得入标题
  （script:cite_in_heading + llm）、术语统一（module:consistency）、物理量斜体/法定单位（llm）、
  数字用法（llm）、公式居中编号(1-1)/断行规则/式中注释（llm+manual）、
  三线表（module:tables）、图表编号"图1-1/表1-1"与提示语"见图/如表所示"
  （module:references + llm）、续表/跨页/旋转（manual）、GB/T 7714 著录
  （module:bibliography）、脚注每页从①（manual）、附录编号（script:appendix_letter）、
  成果格式同参考文献（llm）、书脊（manual）。
- `YS-46~55` 排版打印 §3.1~3.9：字体/字号/行距（manual，附 §3.2 数值表）、封面题名页要素
  （学校代码 10216、分类号、UDC、密级；llm/manual）、页码罗马-阿拉伯分段（llm）、
  页眉双线与奇偶内容（manual）、摘要页/目次页版式（manual）、正文层次"第1章"阿拉伯数字
  （llm）、A4 与页边距上下 3.0cm 左右 2.8cm、页眉页脚距边 2.5cm（geometry 显式时 script 可判，
  v1 标 manual+说明）、双面印刷/右页起章/彩打/热胶装（manual）。

manual 项不是摆设：报告末尾按「打印前自查单」输出，这正是"对照规范逐项检查"的用户价值。

## 5. 对齐锁（契约测试）

新文件 `tests/contracts/test_spec_checklists.py`：

1. 对每个含 `## 逐项检查清单` 的 `templates/*.md`：可解析、ID 唯一且前缀统一、
   检查方式/适用枚举合法。
2. `script:` 引用的 checker key ⊆ check_spec.py `CHECKERS`（zh 副本 importlib 加载）；
   反向：CHECKERS 中每个 key 至少被一个清单或测试 fixture 引用（防死代码）。
3. `module:` 引用的模块名 ⊆ SKILL.md Module Router 的 Module 列。
4. yanshan.md 清单条目数下限断言（≥40），防止误删。

## 6. 集成点与风险

- SKILL.md：新增 router 行 `spec-check`（命令示例 `check_spec.py main.tex --template yanshan --degree doctor`，
  Read next `references/modules/spec-check.md`）+ 路由规则一条 + Example 一条 +
  `when_to_use` 补「对照学校规范逐项终检」短语。
  风险 1：全局 hook 重排表格 → 改完必跑 `tests/contracts/test_skill_contracts.py`。
  风险 2：`description`/`when_to_use` 属路由边界 → 同步在 `evals/trigger_eval.json` 增加
  1~2 条正例（用 Bash python 写入，规避 JSON hook；契约测试 test_trigger_evals.py 会校验）。
- detect_template.py：`TEMPLATE_REFERENCE_FILES` 不含 yanshan（无 documentclass 可检测），
  维持现状；spec-check 模块文档写明「模板未识别时向用户确认学校，yanshan 用 --template yanshan 显式指定」。
- 报告输出遵循仓库 Output Contract：`% SPEC-CHECK (file:Lxx) [Severity] [Priority] [Script|LLM]: YS-xx ...`。

## 7. 取舍记录

- **不做** 清单条目内联参数（如 `script:kw_count(3,8)`）：阈值进 TEMPLATE_THRESHOLDS，
  避免把 md 变成 DSL；自定义 --spec-file 遇阈值类检查器按模板缺省或报 NEEDS-LLM。
- **不做** 编译产物（PDF/aux）分析：v1 全部静态源码判定，保持零额外依赖与快速反馈。
- **不改** check_format.py：终检是"汇总 + 阈值"层，与 format 的 chktex/标点检查职责分离。
