# C3 实施与验证记录

日期：2026-09-10。任务：`09-10-thesis-zh-compile-outdir`。

## 实施结果

`LaTeXCompiler._output_pdf()` 统一解析源入口目录、相对输出目录和绝对输出目录。
compiler 和 recipe 路径均使用同一个结果传递 latexmk 输出目录、检查产物并报告路径。
原有内部 latexmk XeLaTeX/LuaLaTeX step 共用输出参数追加位置，没有新增 recipe。

正常结束的 latexmk 进程仅在 exit 0 且目标 PDF 存在时成功；非 0 保留真实返回码，
目标缺失返回 1。指定输出目录后，源目录旧 PDF 不能替代缺失目标。已有目标被 latexmk
判为无需更新仍为合法成功，不用时间戳强制重编译。

默认行为变化：

- 显式 compiler 路径现在传递 `--outdir`，并在 exit 0 但 PDF 缺失时返回 1，包括无
  `--outdir` 的情况。这修复原来的假成功。
- recipe 输出目录中的有效 PDF 现在能被找到，修复原来的假失败和源目录旧 PDF 假成功。
- 六种手动 recipe 与非空 `--outdir` 同用时，在任何 TeX/Bib subprocess 前返回 1，提示
  受支持的 latexmk/compiler 路径，不再静默忽略参数，也不替换用户选择的 recipe。
- 无输出目录的手动 recipe 保持原有执行次序，以及 BibTeX/Biber 非 0 警告后继续的行为。
  shell-escape 信任门禁、watch 中断处理和清理路径保持现状。

公开 `references/modules/compile.md`、`references/latex/compilation.md` 及对应 EN/ZH
四份镜像已同步路径基准、支持/拒绝组合、成功判据和产物/视觉证据边界。原配置例子的
隐式输出目录建议改为显式 wrapper 参数，不承诺解析任意 latexmkrc/jobname/auxdir。

## 修复前证据

- [baseline-g6.json](baseline-g6.json)：重新运行父任务 `reproduce_probes.py` 的 G6
  两个探针。仅目标目录 PDF 时原 wrapper 返回 1；仅源目录旧 PDF 时返回 0。
- [regression-before.txt](regression-before.txt)：新建真实 wrapper 回归在修改源码前运行，
  `66 failed, 17 passed`。测试只 mock 外部进程与工具发现，真实文件创建在 pytest 临时目录，
  调用实际 `LaTeXCompiler.compile()` 和 CLI `main()`。

## 自动化验证

新测试 `test_compile_outdir.py` 共 83 项，覆盖：

- 默认、显式 latexmk recipe、显式 XeLaTeX/LuaLaTeX compiler；
- 无输出目录、相对目录、绝对目录、中文空格目录；
- exit 0 + 目标存在、exit 0 + 目标缺失、非 0 + 目标存在、仅源目录旧 PDF；
- CLI 参数传递和退出码、六种手动组合零 subprocess 拒绝、shell-escape 引擎参数。

在 C2 交接后，仅扩展共享文件 `TestCompileZh.test_recipe_selection` 为六种手动配方，
用 Bib 后端 exit 2 验证后续引擎步骤仍执行并保留成功路径。C2 的四行语义断言完整保留；
Ruff 仅规范化累计改动的格式/换行。

最终局部命令：

```powershell
rtk uv run --no-sync python -m pytest tests/skills/latex_thesis_zh/test_compile_outdir.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_scripts.py::TestCompileZh tests/skills/latex_thesis_zh/test_latex_thesis_zh_coverage.py tests/contracts/test_skill_contracts.py -q
```

结果：**156 passed，0 failed，0 skipped**，32.81 秒。

```powershell
rtk uv run --no-sync ruff check academic-writing-skills/latex-thesis-zh/scripts/compile.py tests/skills/latex_thesis_zh/test_compile_outdir.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_scripts.py
rtk uv run --no-sync ruff format --check academic-writing-skills/latex-thesis-zh/scripts/compile.py tests/skills/latex_thesis_zh/test_compile_outdir.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_scripts.py
rtk uv run --no-sync pyright academic-writing-skills/latex-thesis-zh/scripts/compile.py tests/skills/latex_thesis_zh/test_compile_outdir.py
```

Ruff check/format 均通过。Pyright 为 **0 errors, 2 warnings**：两条均位于未改动的
`compile.py:134`，即 `_check_tools_for_recipe()` 对 optional recipe 调用 `dict.get`。
本任务没有扩大范围清理既有类型告警。C3 所有跟踪文件的 `git diff --check` 通过。

首次运行包含整个共享 scripts 文件的组合为 **202 passed, 2 failed**，两条失败是 C2
正在实施期间的 `TestCheckConsistency.test_detects_term_inconsistency` 和
`test_custom_terms_loading` 新语义断言，已报告主线程。它们不是 C3 编译回归失败；最终
共享套件由主线程在 C2 完成后重跑。

## 真实 TeX wrapper smoke

执行入口：

```powershell
rtk uv run --no-sync python -X utf8 .trellis/tasks/09-10-thesis-zh-compile-outdir/research/run_smoke.py
```

该脚本只在 `tempfile.mkdtemp()` 新目录写入最小合成 article，通过
`uv run --no-sync python <wrapper> <isolated entry> ...` 编译，不直接运行 TeX 二进制构建，
不操作用户论文或 GUI，不清理产物，不安装依赖。工具二进制仅直接查询 `--version`。
子 wrapper 明确使用 UTF-8 stdout；TeX 文本不能按 UTF-8 解码的字节以转义形式保留在日志。
记录文件的 CRLF 写入已修正为原样保留，没有因日志格式重跑构建。

所有精确 argv、cwd、工具路径/版本、退出码、目标路径、大小与时间戳保存在
[tex-smoke/results.json](tex-smoke/results.json)，每次 stdout/stderr 文件也由该 JSON 关联。
隔离根目录为 `C:\Users\lyh\AppData\Local\Temp\c3-wrapper-m7q0chtc`。
工具为 latexmk 4.86a、XeTeX 0.999997、LuaHBTeX 1.21.0（TeX Live 2025）。

| 场景 | wrapper 参数 | exit | 目标 PDF 字节 | 结果 |
| --- | --- | --- | --- | --- |
| recipe 相对目录 | `--recipe latexmk --outdir build` | 0 | 4245 | 目标在源入口的 build 下，源目录无 PDF |
| compiler 绝对空格目录 | `--compiler xelatex --outdir <isolated>/external output` | 0 | 4246 | 目标在绝对输出目录，源目录无 PDF |
| compiler 中文空格目录 | `--compiler lualatex --outdir 构建 目录` | 0 | 4584 | 目标在指定中文目录，源目录无 PDF |
| 默认相对目录 | `--outdir build` | 0 | 4246 | 目标在源入口的 build 下，源目录无 PDF |
| 默认无输出目录 | 无 | 0 | 4249 | 目标在源入口旁 |
| 已有目标无需重建 | 与首行同一命令/输入 | 0 | 4245 | latexmk 报 up-to-date，mtime 前后相等 |

版本查询与运行 stderr 中有当前环境的 Perl locale 回退警告，原文保留。六次运行均正常
完成且产物路径正确，没有为消除此环境警告修改用户全局设置。

## 父任务待执行与证据限制

- 父任务统一刷新 `docs/resource-manifest.json` 后执行单技能与全量资源检查、docs build、
  全量 CI，以及最终共享套件；C3 不独占 manifest，不重复执行已通过的局部验证。
- 本地 mock/CLI 与六次合成 article 构建证明本任务的进程结果和输出位置行为。实际论文、
  学校模板、文献后端完整排版和页面目视验收仍为 **UNVERIFIED / missing evidence**。
- 任意 latexmkrc/jobname/auxdir 和手动 Bib 后端 outdir 协同不在本任务范围。
- 本子代理未提交、归档、推送、修改 task.json/spec 或安装依赖。


## 父任务集成完成（2026-09-10）

上述交接时待执行门禁现已完成：最终完整CI为1908 passed、2项平台条件skip，
Pyright0 errors/75既有warnings；单技能和全量资源271项、docs build与独立审阅均通过。
本任务AC已全部回填；未提交或归档。最终状态与证据以
[父级集成验收](../../09-10-thesis-zh-spec-gap-optimization/research/integration-validation.md)为准。

独立审阅额外修复了工具缺失掩盖不支持组合提示的顺序问题：六种手动recipe的拒绝
现在先于工具发现。最终outdir新测试由83增至89项，含既有TestCompileZh的修后组合
为98 passed，并在新隔离目录验证最终wrapper生成4178字节目标PDF。
原六组smoke保留为输出路径证据；最终控制流补丁的独立实测和失败前记录见父级验收链接。
