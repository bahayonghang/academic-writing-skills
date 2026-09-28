# 安装告警原因分析

## 结论与证据边界

核查日期：2026-09-27。本地基线：`dev`，`a9d2d32cf2e51a055a70496772b10e5a314d0267`，开始时工作区干净。
远端 main：`00fc942c32fd7e8922a3e3382478f98c6b84d308`；远端 dev：`13d7743d00dfd7f14d9d0901046f75c79f3e4b76`。
未 fetch、checkout、安装或执行远端代码。仅 HTTP 读取公共源码和扫描结果。

两条告警都有本地代码依据：include 解析缺少根目录包含检查。合成复现确认五个 loader 的两个公开接口可读取项目外 `.tex` 内容。尚无本次调查证据表明发生真实数据泄露、网络外传或命令执行。

## 在线扫描证据

| 技能 | Socket 扫描时间 UTC | 类别 | 位置 | 页面等级 |
| --- | --- | --- | --- | --- |
| latex-thesis-zh | 2026-09-25T07:31:52.299Z | gptAnomaly / Anomaly | scripts/tex_loader.py | LOW |
| latex-defense-zh | 2026-09-26T03:46:34.166Z | gptAnomaly / Anomaly | scripts/tex_loader.py | LOW |

扫描正文说明该文件承担本地文档组合，没有明显恶意载荷或外传机制，但 include 可能跨越项目根目录。两页都显示 confidence 98%、severity 58%；这些数值属于扫描器输出，不转换成漏洞利用概率。

来源与本地快照：

- [thesis Socket 正文](https://www.skills.sh/bahayonghang/academic-writing-skills/latex-thesis-zh/security/socket)：`latex-thesis-zh-socket.txt`。
- [defense Socket 正文](https://www.skills.sh/bahayonghang/academic-writing-skills/latex-defense-zh/security/socket)：`latex-defense-zh-socket.txt`。
- [thesis audit API](https://www.skills.sh/api/v1/skills/audit/bahayonghang/academic-writing-skills/latex-thesis-zh)：`latex-thesis-zh-audit.json`。
- [defense audit API](https://www.skills.sh/api/v1/skills/audit/bahayonghang/academic-writing-skills/latex-defense-zh)：`latex-defense-zh-audit.json`。
- [CLI 摘要 API](https://add-skill.vercel.sh/audit?source=bahayonghang/academic-writing-skills&skills=bib-search-citation,latex-defense-zh,latex-thesis-zh,paper-audit,paper-writing-studio,latex-paper-en,cover-letter)：`cli-audit.json`。

Socket 包标识后缀分别为 `9c8b2bd2910da7c3786270698aabaae99951c94fe5d41dea81cab9f244294691`、`8a507cb7e07cbb6f23a98a2e50ff72adca895c02614c1b6d978284cddf4de3cb`。完整 PURL 保存在正文快照；未证明该摘要与 Git commit 的映射。

Gen 与 Snyk 对两个技能分别返回 SAFE、LOW / No issues。三个供应商的评估独立，不能用其中一个供应商的通过覆盖其他告警。

### 显示链路

核读上游 skills commit `7407f3893ad4dceab546ac002c3ef806e4000c73`：

- `src/telemetry.ts:110-133` 的 `fetchAuditData` 按仓库和 skill slug 请求服务端结果。
- `src/add.ts:132-135` 的 `socketLabel` 将大于 0 的 alerts 数量显示为红色。
- `src/add.ts:1907-1923` 读取并显示评估表。
- 源片段已保存为 `add.ts-excerpt.txt`、`telemetry.ts-excerpt.txt`。原用户使用的 CLI 版本未知，上游当前实现仅用于解释匹配的显示机制。

用户粘贴的表格提供安全评估数量，未提供安装退出码，不能据此判定安装失败。
在线摘要把两个 Socket 风险写为 `critical`，详情页标为 `LOW`，通用 audit API 标为 `warn`。三个字段层级不同，映射原因未查明。不得把摘要字段直接解释为已证实的 Critical 漏洞。

## 源码与复现

| 副本完整路径 | 解析 | 读取/递归 | 当前复现 |
| --- | --- | --- | --- |
| academic-writing-skills/latex-thesis-zh/scripts/tex_loader.py | 65-75 | 98、114、204、223-230 | 受影响 |
| academic-writing-skills/latex-defense-zh/scripts/tex_loader.py | 65-75 | 98、114、204、223-230 | 受影响 |
| academic-writing-skills/latex-paper-en/scripts/tex_loader.py | 68-78 | 101、117、200、219-226 | 受影响 |
| academic-writing-skills/paper-audit/scripts/tex_loader.py | 68-78 | 101、117、200、219-226 | 受影响 |
| academic-writing-skills/cover-letter/scripts/tex_loader.py | 68-78 | 101、117、200、219-226 | 受影响 |

因果链：文档中的 include 参数 → `current_dir / name` 或 `root / name` → `resolve()` → `exists()` → `read_text_robust()` → 合并文本或 IncludeNode.content。`resolve()` 规范化路径，但不会限制读取范围。`_display_rel()` 的路径显示回退也不构成访问控制。

当前行为会给不以 `.tex` 结尾的 include 参数补后缀。已证明的内容读取限于可访问的目标 `.tex` 文件以及指向外部目标的链接；不据此声称任意后缀文件都能直接通过 include 读取。

运行：

```text
uv run python -B .trellis/tasks/09-27-skills-install-security/research/reproduce_include_boundary.py
```

探针只创建临时合成文件，通过 importlib 加载五个本地副本；临时目录自动清理，未读取真实项目外文档。输出保存在 `reproduction.json`。

结果：五副本 × 三种越界（父目录、绝对路径、符号链接）= 15 个场景；每个场景中 `assemble` 与 `iter_files` 均读到外部标记，合计 30 次接口观察。五个目录内对照场景全部正确读取内部标记。所有场景 warnings/missing 为 0。符号链接场景在本机实际运行，无跳过。

附加基线：`uv run --extra dev python -B -m pytest tests/skills/latex_thesis_zh/test_latex_thesis_zh_multifile.py::TestTexLoader -q`，6 passed。该结果说明已有正常路径测试通过；不能证明边界安全。

### 扫描截断说法

Socket 同时提到 `return do`。本地两个 ZH 副本在第 239 行以完整 `return doc` 结束；五副本 `ast.parse` 全通过。通过固定远端 main commit 的 raw URL 核对，两个 ZH loader 在 LF 规范化后分别与本地相同。

原扫描输入未公开，扫描器输入截断或呈现截断均为假设，原因未查明。修复不应添加无意义尾注或改名来影响扫描文本截断。

## 修改关联面

- defense 原 C2 计划要求从 ZH 复制 loader，仅改变 docstring：`.trellis/tasks/09-23-defense-zh-extract-build/implement.md:13`。说明两个 ZH 副本应同步维护；执行前重读实时行号。
- `academic-writing-skills/latex-defense-zh/scripts/extract_thesis.py:274-279` 已接收 main 与 root，但只向 assemble 传 main；`:1104-1107` 把全部 doc.warnings 标为 W-ENCODING。把边界拒绝塞进 warnings 会产生语义错误。
- `academic-writing-skills/latex-thesis-zh/scripts/check_references.py:412-416` 只收集已读取节点的 warning；`check_consistency.py:1020` 只筛选存在的节点。仅追加未读取节点的 warning 不能保证下游可见。
- `tests/skills/latex_thesis_zh/test_polish_unit_zh.py:25-32` 冻结 loader 哈希。`.trellis/spec/academic-writing-skills/unit-polish-contract.md` 明确允许其他任务改这些文件后同步更新 LF 哈希。
- 本地 defense 尚无 SKILL.md；其目录已有 scripts/references/tests。公开 main 入口已存在，不能把线上完整包状态套到本地工作树。

## qiaomu-meta-skill 的应用

本次属于已有 skill 的诊断与优化规划，采用 Library 的 portability/trust/install evidence，并对公开安全声明采用 Governed 的 claim guard。未生产新 skill，不运行 Scaffold，不更改作者、名称或许可证，不调用 publisher。

| 机制 | 处置 | 本任务落点 |
| --- | --- | --- |
| Generalization Gate | keep | 五个独立安装副本重复同一缺陷，形成可执行 include 边界合同 |
| Trust / permissions | adapt | 路径检查落到实际文件读取之前，宿主明确的根目录为授权边界 |
| Output eval | adapt | 真实 loader 的越界拒绝、正常解析和 CLI 失败输出测试 |
| Resource boundaries | keep | SKILL 只写简短边界，证据留在 task research，安装排障写双语 docs |
| Install evidence / claim guard | keep | 记录包版本和文件哈希，区分本地通过、安装验证与扫描刷新 |
| 新 skill prior-art 搜索 | not applicable | 没有新建或大幅重设计技能；用既有 sibling 实现及上游 CLI 作为参照 |
| 改名、藏关键字、重复安全承诺、MIT/作者模板、自动发布 | reject | 不解决文件访问缺陷，且会超出本轮授权 |

设计优势：统一行为测试与读取前边界。已验证事实：缺陷可在五副本复现。未验证假设：修复后 Socket 告警将消失，须等待针对新包的扫描。

## 未执行或未验证

未运行原始 npx 安装、完整 CI、文档构建、五工具运行、junction/UNC/链接并发替换、真实外部文档读取、网络外传、远端重新扫描。修复尚未实施。保存的网络响应可能随上游刷新发生变化。
