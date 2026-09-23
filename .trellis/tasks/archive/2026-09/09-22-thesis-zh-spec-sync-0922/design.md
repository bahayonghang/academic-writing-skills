# 集成设计与共享边界

## 1. Architecture / authority

来源材料 → 条款与适用范围核读 → skill 公开指南/模板 → 可判定的局部 opt-in checker。
学院原文、论文作者约定、脚本启发式三者必须分别归因；脚本零发现不等于学术或学院验收通过。
事实核对见 research/planning-evidence.md；原始21项差距保留，但冲突处以此次修订证据与 PRD 为准。

不生成新的公共配置平台。C1 仅用现有 custom-terms JSON 的扩展字段；C2 用单个学院模式；
C3 的候选阈值为 opt-in 常量；C4 只允许小型指标/评价集词表输入，不用 YAML 构造规则语言。
C5 继续五列清单；C6 文档层完成全部五主题。

## 2. Interfaces and data flow

- C1：check_consistency.py --governance --custom-terms FILE；--abbreviation-style 独立开关；
  check_style_zh.py --degree-wording。未选这些开关时旧路径原样运行。
- C2：check_style_zh.py / check_format.py / check_tables.py / check_references.py
  --school yanshan-ee-2025；缺省或 --school generic 关闭新增学院规则。不使用宽泛 yanshan 别名。
- C3：check_references.py --author-cite / --repeat-cite；verify_bib.py --college-details
  与现有 GB standard 一起使用；analyze_literature.py --progression-density，复用 --section。
- C4：analyze_experiment.py --cross-surface [--cross-surface-terms FILE]，后者只覆盖词表；
  与 --results-analysis 组合时保留已有9码，不改原阈值。
- C5：check_spec.py --template yanshan-ee-2025 --degree doctor|master --year 2026；
  新模板的 MODULE 提示显式追加对应模式，不自动执行模块。
- C6：无新脚本开关或码集；按指南进行 LLM 判读。

新增候选用 [Script]、Info/P3、Meaning-Check: NEEDS-LLM；只报告局部定位/词/字段，
不输出可直接套用的整句替换。输入无效不能伪装成“零发现”：显式新配置读取/类型错误
走现有 CLI 错误机制并非零退出；不为未启用功能加载配置。保持旧错误路径与报告格式。
既有严重度不批量修改；C5 的 MANUAL/MODULE/NEEDS-LLM 沿用现有清单状态。

## 3. File ownership and handoff

下表目录缩写 S=academic-writing-skills/latex-thesis-zh；路径均相对仓库根。
各子 design 列出精确文件；新增辅助实现限定为对应脚本内局部函数。

| 所有者 | 主要实现面 | 前后移交 |
| --- | --- | --- |
| C1 | S/scripts/check_consistency.py、check_style_zh.py；consistency/style指南 | check_style_zh 移交 C2 |
| C2 | check_style_zh.py、check_format.py、check_tables.py、check_references.py；formatting指南 | check_references 移交 C3；CLI 移交 C5 |
| C3 | check_references.py、verify_bib.py、analyze_literature.py；citation/literature指南 | CLI 移交 C5 |
| C4 | analyze_experiment.py；experiment/results指南 | 无共享脚本写入 |
| C5 | check_spec.py；新学院模板；spec-check指南 | 不改旧 yanshan.md，不回改 C2/C3 算法 |
| C6 | 五主题写作指南；logic/routing说明 | 收口文档；不改 checker |

每子只可修改自己的源码、配套测试/合成 fixture、相应 .trellis/spec 文件及索引、
该公开资源的 docs/skills 与 docs/zh/skills 同路径镜像。
SKILL.md、evals/evals.json、.trellis/spec/academic-writing-skills/index.md、
docs/resource-manifest.json、README.md、README_CN.md、docs/usage.md、docs/zh/usage.md、
docs/skills/latex-thesis-zh/index.md、docs/zh/skills/latex-thesis-zh/index.md 为串行共享文件：
当前子拥有自己的段落/条目，完成验证后再移交，后续不得覆盖前子已接受内容。
evals 只追加合成条目；遵守现有写入方式，不重排历史条目。
tests/skills/latex_thesis_zh/test_polish_unit_zh.py 的 check_style_zh 哈希由 C1/C2
各自按本次真实 LF 内容更新一次，其他冻结条目不改；依据 unit-polish-contract。
扩写公开行为时同步上述用户入口中受影响的句子，不强制改无关页面。

## 4. Baseline and verification mechanism

在未来实施的每个子开始前，对该子将触及的入口使用固定合成 fixture、固定路径、相同解释器、
固定 --year、UTF-8 环境采集旧命令 stdout/stderr/exit 到该子 research/baseline/。
修改后以相同参数逐字节比对；不能用 paragraph_arc 单一 baseline 代表所有模块。
--help 新增选项以及显式新选项调用不属于旧输出基线。新 fixture 无私有数据。
稳定代码回归测试覆盖相同不变量；本地 baseline 只证明采样命令，不宣称所有输入完全相同。
命令清单：C1 consistency default/--terms/--abbreviations/旧 --custom-terms/style；
C2 style/format(strict与非strict)/tables/references 的无新参数路径；
C3 references/verify_bib(default、两GB standard)/literature(普通及intro-citations)；
C4 experiment 普通/--results-analysis；C5 四个旧模板的两学位 JSON 输出与新模板111行；
C6 指南语义核读+CF/abstract旧测试，不新增脚本行为。

每子：先新增有意义正反例回归，再跑目标测试 → just ci（版本、lint、typecheck、pytest）
→ uv run python docs/scripts/check_resource_sync.py → just doc-build。
构建与测试通过即完成该子验证；无新问题不重复全量门禁。
资源新增/修改时用 checker --write-manifest --inventory-only 重建清单并核对语言字段，
此命令不替代完整资源检查；镜像翻译需人工核对。
最终父集成沿用各子证据，新增跨子验收后如有变更才重跑相关门禁。

## 5. AC traceability

| 父 AC / 子句 | 机制与验收真源 |
| --- | --- |
| AC1：治理/锁定/豁免、XOR三类、程度/反例、旧路径 | C1 design §2–§5 与 AC1–AC5 |
| AC2：四模块、学校隔离、旧模板、指南 | C2 design 的学校模式、扫描边界、矩阵 |
| AC3：位置/页码/字段/姓名/阈值 | C3 design §2–§5；不允许把原始作者显示化 |
| AC4：同对象终值/缺表面/误匹配/不可判断 | C4 design 绑定键和状态规则及矩阵 |
| AC5：111行/两学位/子句/MODULE/人工 | C5 来源逐项矩阵、完整项路由和人工范围 |
| AC6：五主题/8码/分工/双语/冻结 | C6 主题表与文档核读矩阵 |
| AC7：各门禁/默认基线/冻结/隐私 | 本文§3–§4 + 每子 implement 验证步骤 |

## 6. Rejected additions / rollback / evidence boundary

不新增 PDF 自动化、复合清单规则引擎、BibTeX 姓名改写、全局术语替换；
不把研究生院2024与学院2025合成同一个配置，也不把私有豁免当普遍标准。
按子交付可独立回退；涉及共享脚本时逆序回退子提交/补丁及对应文档、测试和 manifest，
不可恢复整文件而覆盖后续子修改。提交、归档、push 不由此计划授权。
合成测试仅证明静态候选和分流；真实论文、PDF、学校接受、作者满意、五宿主运行均 UNVERIFIED。
