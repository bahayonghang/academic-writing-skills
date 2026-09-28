# Include 读取边界设计

状态：2026-09-27 用户批准实施，当前 in_progress。需求来源为 `prd.md`，根因与当前接口见 `research/diagnosis.md`。

## 1. 所有权与文件边界

loader 拥有递归 include 的路径解析、边界判定和定位；宿主调用方拥有项目根目录；文档内容不能扩大该目录。

| 文件 | 允许变更 |
| --- | --- |
| academic-writing-skills/{latex-thesis-zh,latex-defense-zh,latex-paper-en,paper-audit,cover-letter}/scripts/tex_loader.py | 同一边界规则、异常、可选 project_root；保留既有副本差异 |
| academic-writing-skills/latex-defense-zh/scripts/extract_thesis.py | Source.load 传递既有 root；边界异常转换为 ExtractError |
| academic-writing-skills/latex-thesis-zh/scripts/check_format.py | 已获补充批准：边界异常在通用异常回退前传播，避免 PASS |
| academic-writing-skills/paper-audit/scripts/prepare_review_workspace.py | 已获补充批准：边界异常在 ValueError 格式回退前传播 |
| tests/shared/test_tex_loader_security.py（新增） | 五个真实副本的行为矩阵，按路径隔离加载 |
| tests/contracts/test_tex_loader_alignment.py（新增） | 五副本安全接口与核心边界语义契约，保留合法差异，不锁整文件相同 |
| tests/skills/latex_thesis_zh/test_latex_thesis_zh_multifile.py | 必要的项目内兼容性用例 |
| tests/skills/latex_thesis_zh/test_polish_unit_zh.py | 仅更新被修改 loader 的 LF 哈希及必要回归 |
| tests/skills/latex_defense_zh/test_defense_extract.py | 嵌套 main 与 CLI 失败/输出保护 |
| academic-writing-skills/{latex-thesis-zh,latex-paper-en,paper-audit,cover-letter}/SKILL.md | 简短 include 安全边界；不改触发路由 |
| academic-writing-skills/latex-defense-zh/SKILL.md | 仅 C4 已创建/集成后的安全边界增量；本任务不创建入口 |
| README.md、README_CN.md、docs/installation.md、docs/zh/installation.md | 安装告警、默认边界变化、验证范围；README 只放短说明及链接 |
| .trellis/spec/academic-writing-skills/include-boundary-contract.md（新增）、index.md | 行为合同与测试入口 |
| 当前任务目录 | 证据、计划、检查结果 |

不修改 parsers、compile、清理脚本、catalog、主题模板或已有 task 状态。若调查出现新的读取路径或需修改其他调用方，先更新边界并呈报，不顺带扩展。

## 2. 接口与执行规则

计划增加向后兼容的关键字参数，保留现有 positional entry：

```python
iter_files(entry: Path, *, project_root: Path | None = None) -> list[IncludeNode]
assemble(entry: Path, *, project_root: Path | None = None) -> AssembledDocument
```

两个函数先解析 entry 和 root。未给 project_root 时使用已解析 entry.parent；给定时必须是包含 entry 的现有目录。root 在一次调用内固定，不随子文件变更。defense `Source.load(main, root)` 将既有 `--thesis` 的 root 传入 assemble。

私有解析器沿用当前目录优先、根目录回退和补 `.tex` 后缀的行为；增加包含判断：

1. 解析候选路径，包括 `..` 和符号链接。
2. 使用 Path 的目录包含判断，禁止字符串 startswith。外部 Windows 盘符、根路径与 UNC 不得通过拼接绕过。
3. 候选越界立即拒绝；不得用一个项目内同名回退文件遮盖显式越界。
4. 合法候选不存在时检查合法根目录回退；回退也须先检查边界再 exists/read。
5. 对候选解析错误、无效路径和链接环给明确失败。未找到但路径合法时沿用原有 missing 行为。
6. 读取处保留防御性包含检查，避免一个递归入口遗漏检查。`read_text_robust` 仍为通用显式文件读取函数，不把全局根目录状态塞入该函数。

项目内绝对路径可以使用；项目内子章节的 `../sibling` 可以使用。显式根目录外的路径拒绝。默认 entry.parent 不自动上溯到 Git 根目录，也不自动信任论文声明的更大目录。

此设计覆盖稳定文件树上的路径越界。常规 resolve + 检查无法提供对并发链接替换的完整操作系统隔离保证；不声明该实现是 TeX 或文件系统沙箱。

## 3. 失败契约

新增 `IncludeBoundaryError(ValueError)`，在两个公开入口传播。错误携带稳定码 `E-INCLUDE-BOUNDARY`、include 原始参数、调用源相对路径、源行号和拒绝原因。诊断不包含被拒文件内容，也不主动展示解析后的私人绝对路径。显式 project_root 与 entry 不匹配同样失败，不能先读 entry 再验证。

拒绝后不返回 IncludeNode 列表或 AssembledDocument 的部分成功结果。不伪装成 missing，不新增仍会继续分析的普通 warning。已有编码 warning、missing 列表和源位置结构保持不变。

选择明确异常的依据：`check_references.py` 只在成功节点上收集 warning，`check_consistency.py` 按 exists 过滤，defense 把 doc.warnings 全部归类为 W-ENCODING。仅增加 warning 会被忽略或误分类。

defense 把该异常转换为既有 ExtractError，沿用 CLI 的 exit 2，并在输出文件写入之前失败。ZH check_format 与 audit prepare_review_workspace 的通用异常回退会吞掉边界错误；2026-09-27 用户已批准这两处特定异常重新抛出。其余 CLI 保留异常传播导致非 0 的基本行为；代表性回归须看见错误码与来源。若后续需要统一无堆栈用户输出，另行评估调用方边界，不修改数十个无关入口。

## 4. 副本与兼容性

- 两个 ZH loader 仅有 docstring 技能名差异；三个 EN-family loader 当前 LF 内容相同。保持各组已有差异，不改造成跨技能 import。
- 新测试按文件路径加载五个模块，隔离 sys.modules，避免 tests/conftest.py 的 EN 默认路径掩盖 ZH/defense 缺陷。
- 共享行为测试负责安全结论；轻量接口合同负责发现遗漏副本。已有 `parsers.py` 的 ALIGNMENTS 不涉及此次改动，不修改该哈希表。
- 更新 ZH loader 后，审阅源码 diff，再更新 `test_polish_unit_zh.py` 的对应 FROZEN_HASHES；其他五个哈希保持不变。
- 越界拒绝是明确的默认行为变化。批准本计划即包含该变化；双语说明和未来提交正文须写明。需要多个外部目录的工程不添加宽松开关，本任务只支持一个明确项目根目录。

## 5. 验证矩阵

| 类别 | 输入 | 要求 | 对应 AC |
| --- | --- | --- | --- |
| 越界 | `../outside`、外部绝对路径、外部符号链接、目录名前缀相近 | read_text_robust 对外部目标调用次数为 0，抛稳定异常 | AC2 |
| 命令与入口 | input/include/subfile；assemble/iter_files；五副本 | 相同边界，不漏遍历路径 | AC2 |
| 回退绕过 | 一级候选越界、根目录存在同名文件 | 拒绝，不能静默回退 | AC2/3 |
| 合法目录 | 项目内 `..`、相对/绝对路径、中文/空格、嵌套 main 与显式 root | 内容顺序与源位置正确 | AC4 |
| 既有行为 | 缺失 include、注释、循环、GB18030、源行映射、单文件及既有 .typ passthrough | 与原合同一致 | AC4 |
| CLI | 论文分析入口、defense extract，新/已有 inventory | 非 0、有定位、不写或覆盖输出 | AC3 |
| 独立安装 | 四个现存入口 + C4 集成后的 defense | 从隔离安装目录执行同一行为测试；不依赖仓库 sys.path | AC5/6 |
| 第三方 | 新扫描时间与包标识 | 未更新则 pending；与本地结论分列 | AC7 |

Windows 路径用平台可执行的用例验证；不支持创建符号链接的环境须记录 skip，不能把跳过计为已测。UNC 测试可在解析边界使用无网络探测的断言；实际网络共享行为仍须单独标未验证。

## 6. 发布、安装和回滚

代码修复不代表线上扫描刷新。实施阶段先做本地目录来源的隔离安装验证，固定并记录 skills CLI 版本；只写新临时目录，不覆盖用户已安装技能。命令依据所固定 CLI 的 help 生成，不假定主分支版本等于原用户版本。

defense 的完整安装验证依赖 C4 入口集成；不为了过门禁临时伪造 SKILL.md。四个其他技能可先验证，defense 状态保持未验证。远端发布、公开扫描申请和原安装告警消除不在本轮执行授权内。

回滚仅撤销本任务的实际 diff、对应测试和说明，保留其他任务的新增内容。回滚会重新开放已验证的 include 越界路径，交付必须说明这一后果，不做全仓 reset。
