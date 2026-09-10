# 工作流复现与根因

日期：2026-09-07。没有修改产品代码。探针只写本任务取证文件，隔离副本位于 Python TemporaryDirectory，结束后自动清理。

复现命令：`uv run --extra dev python .trellis/tasks/09-07-five-harness-evergreen-audit/research/probe_isolated_audit.py`。输入是已提交的 `tests/fixtures/paper_audit/sample_paper.tex`，主路径是真实 `audit.py --mode quick-audit --lang en --format json`，不是 mocked checker。

## F1 / P1：Windows UTF-8 输出与默认 GBK 管道解码不匹配

| 场景 | 子进程环境 | 结果 |
|---|---|---|
| 当前完整 checkout | 去除 PYTHONIOENCODING/PYTHONUTF8 | exit 0，RUN 11，missing 0 |
| 当前完整 checkout | 仅 PYTHONIOENCODING=utf-8 | **exit 1，UnicodeDecodeError 后 AttributeError** |
| 当前完整 checkout | PYTHONIOENCODING=utf-8 且 PYTHONUTF8=1 | exit 0，RUN 11，missing 0 |

最初的 UTF-8 输出场景和再次对照均复现同一异常。假设比较：H1 输出编码与读取编码不一致（只切 UTF-8 mode 应修复）；H2 缺少 sibling checker（完整 checkout 不该触发，且 missing 应非零）；H3 fixture 内容导致检查器一般性错误（切换编码不应改变结果）。对照支持 H1，排除 H2/H3 作为这次崩溃的主因。

调用链：`audit.py:677-693` 的 `_run_check_script` 使用 `subprocess.run(text=True)`，没有约定 encoding 或成对子进程环境。PYTHONIOENCODING 改变 checker 输出流，但没有改变外层 Python text pipe 的 locale 解码。Windows reader thread 因 UTF-8 中的字节无法按 GBK 解码而失败；`result.stdout` 为 None，`audit.py:618` 调用 `.strip()` 再崩溃。现场完整栈见 [UTF-8 stream 输出](probe-checkout-stream-utf8.txt)。这不是所有环境的必现错误，默认环境和完整 UTF-8 模式均通过。

建议：只在此 Python checker 子进程边界约定 UTF-8 输出与读取协议，保留其他环境变量、现有超时/退出码/问题解析语义。不要仅加 `stdout or ''` 吞掉解码失败，也不要改用户全局编码配置。为实际 subprocess 增加 Unicode 输出回归与 Windows locale 场景；强模型审查协议，低成本模型可在该单函数与限定测试内执行。

## F2 / P1：单独安装 paper-audit 缺少完整检查集

同一 UTF-8 mode 下，完整 checkout RUN 11、missing 0；只有完整 paper-audit 目录的隔离副本 RUN 3、missing 8，**exit 0**。跳过项目为 format、grammar、logic、experiment、sentences、deai、figures、pseudocode。见 [对照摘要](isolated-audit-output.txt)、[隔离输出](probe-standalone-utf8-mode.txt)。这是“命令成功但检查覆盖下降”，不能称为真实检查全部通过，也不能泛化为所有模式都会成功。

根因：`audit.py:398-402` 基于安装树寻找 sibling skill，`:495-507` 按格式/语言解析检查器；`:549-566` 输出 SKIP，`:2757-2760` 在不存在时继续。`docs/installation.md:24-40` 的单技能安装与目录自包含说明没有提前指出这项依赖；`references/TROUBLESHOOTING.md:9` 才说明同级技能需存在。现有契约测试 `tests/contracts/test_docs_bilingual_resources.py:196-205` 主要验证安装命令字面，没有执行隔离安装后的 checker 解析。

建议最小修复：明确 paper-audit 完整检查所需同级 writing skill，给出已验证的完整集合安装/复制布局；做临时隔离安装的真实 CLI smoke，并区分单技能受限运行和完整集合覆盖。此次不把缺失变成新的 gate 失败语义、不引入依赖安装器或跨技能共享包。若要将 standalone 完全自包含，另行决策和规划。

## 证据限制

探针验证了手工复制目录布局，没有执行 `npx skills add`，因此不能声称验证 installer 的软链接布局或五种 harness 的实际安装发现。后续验收需要单列安装器、版本、symlink/复制布局及检查器覆盖。
