# LaTeX include 读取边界

## 适用范围

五个独立安装副本：`latex-paper-en`、`latex-thesis-zh`、`paper-audit`、`cover-letter`、
`latex-defense-zh` 的 `scripts/tex_loader.py`。论文中的 include 参数是不可信数据。
宿主明确选择的入口和项目目录决定读取边界。

## 接口

```python
iter_files(entry: Path, *, project_root: Path | None = None) -> list[IncludeNode]
assemble(entry: Path, *, project_root: Path | None = None) -> AssembledDocument
```

保留 positional entry 与返回结构。默认根目录为解析后的 entry.parent；显式
project_root 必须是包含 entry 的现有目录，在读取 entry 前验证。递归期间不得扩大根目录。
defense 的 Source.load 将既有 `--thesis` 根目录传入 assemble。

## 验证与错误矩阵

| 输入或状态 | 行为 |
| --- | --- |
| 项目外 `..`、绝对路径、符号链接 | 在外部目标 exists/read 前拒绝 |
| 目录名前缀相似但位于外部 | 拒绝；不用字符串 startswith 判断包含 |
| 一级候选越界且根目录存在同名文件 | 拒绝；不得静默回退 |
| 合法候选缺失，合法根目录回退存在 | 沿用当前目录优先、根目录回退 |
| 项目内 `..`、绝对路径、中文和空格目录 | 保留有效引用及源位置 |
| 编码、注释、循环、项目内缺失目标 | 沿用既有处理和诊断 |
| 无效路径、无法解析的链接环、错误显式 root | 明确失败，不返回部分成功结果 |

`IncludeBoundaryError(ValueError)` 通过 `E-INCLUDE-BOUNDARY`、原始参数、源相对路径
和行号标识失败。不得读取后再过滤；不得用可被调用方忽略的普通 warning 代替失败。
诊断不包含被拒文件正文，也不主动补出解析后的私有绝对路径。

defense 将异常转换为 ExtractError，CLI 退出 2，不新建或覆盖 inventory。
其他调用方保留异常传播和非 0 失败；不因为增加此边界而添加新的 CLI 选项。
ZH `check_format` 与 audit `prepare_review_workspace` 须在原通用异常回退前
重新抛出 `IncludeBoundaryError`。不得将边界错误转换为空问题列表或 unsupported_format。
`read_text_robust` 仍承担显式文件读取与解码，不持有全局项目根目录。

## 合同与默认行为变化

五副本分别携带实现，不跨技能 import。保留 ZH/EN 的格式和定位差异；安全行为
由按路径加载的五副本测试保证。`parsers.py` 的 ALIGNMENTS 不因本改动而更新。

本安全修复显式改变项目外 include 的默认行为。公开安装说明须记录该变化；未来提交正文
须写明默认行为变化及原因。更新 ZH loader 时，按 unit-polish-contract 审阅 diff 后
只更新对应 FROZEN_HASHES，保留其他冻结脚本。

## 必须测试

- `tests/shared/test_tex_loader_security.py`：真实五副本、两个接口、三个命令；
  断言外部 read 调用为零、明确异常、正常路径内容和定位。
- `tests/contracts/test_tex_loader_alignment.py`：安全接口和必要语义保持一致，保留合法副本差异。
- 既有 EN/ZH multifile、ZH polish、defense extract：正常行为、根目录传递、CLI 失败与输出保护。
- `just ci` 四步、资源同步、docs build；安装目录执行测试与仓库源码测试分别记录。

符号链接不具备创建权限时显式 skip 并报告；不要把跳过写为通过。Windows 实际网络
共享、其他操作系统与五宿主运行证据分别记录。稳定文件树上的 resolve + 包含检查
不提供并发链接替换的完整防护，也不构成 TeX 执行沙箱。

## 公开结论

源码修复、隔离安装、远端发布、第三方扫描是四项独立状态。没有新包标识与扫描时间，
不得宣称安装告警已消除。其他扫描器的通过结果不能替代某个供应商的待处理告警。

## 正例、基线和反例

- 正例：显式 project_root 包含嵌套主文件和同级章节，保留源相对路径与行号。
- 基线：入口父目录内的正常相对 include 继续组合，原缺失文件 warning 保留。
- 反例：文档含外部绝对路径，先读取再从输出中删掉外部标记，仍已突破读取边界。

## 错误与正确实现

错误：`read_text_robust(target)` 后检查 target 是否在 root 内，或用
`str(target).startswith(str(root))` 放行目录名前缀相似的外部目录。

正确：先规范化并验证目录包含关系与链接目标；在外部 read 之前抛出
`IncludeBoundaryError`。行为测试监测实际 read 调用，不能只断言输出中没有外部正文。
