# C3 设计

## 单点输出位置规则（R1/R2）
LaTeXCompiler.work_dir 是源入口父目录。无 outdir 时目标为 work_dir/stem.pdf；
相对 outdir 相对 work_dir 解析；绝对路径原样规范化。
同一计算结果同时用于传参和最终 exists/成功报告，避免命令与验收分叉。
必要时仅在现有类内提取一个小帮助函数；不建立 build config 或跨技能抽象。

现有默认 recipe=latexmk 与显式 compiler 走 latexmk；
在这两条路径都传 -outdir=<resolved_directory>。
已有内部 latexmk step 共用同一处理，不引入未公开的新 recipe。
上述正常完成的 latexmk 路径只有 subprocess returncode=0 且目标 PDF exists 才报告 SUCCESS/return0；
失败保留真实非0；目标缺失以现有错误返回1。
目标已存在且 latexmk 判定无需重建是合法成功，不拿时间戳相等当错误。
只防止“别处旧 PDF 替代目标”，不声称强制证明文件新鲜度或排版。
无 outdir 的显式 compiler 当前在 exit0但PDF缺失时也会报成功，本任务一并修复这条假绿，
并在变更记录明确声明。watch 中断处理不受本规则扩展。

## 手动 recipe 边界（R3）
当前 xelatex/lualatex 单次及 bibtex/biber 多步 recipe 未转交 outdir。
为保持本任务最小，只要 recipe 是非 latexmk 手动步骤且 outdir 非空，
在任何 subprocess 前返回1，提示当前组合不支持以及可用的 latexmk/显式 compiler 路径。
不静默把用户指定 recipe 改成另一种 recipe。无 outdir 的手动步骤仍照旧工作，
包括现有 BibTeX/Biber 非0警告后继续的行为；本任务不把 latexmk 非0判据推广到这些步骤。
这属于既有静默忽略的假绿修复，公开说明和默认行为变化记录须同步。

## 文件所有权
C3 owner：agent_skill_architect；其他工作可能并行，不撤销他人改动。
- academic-writing-skills/latex-thesis-zh/scripts/compile.py
- academic-writing-skills/latex-thesis-zh/references/modules/compile.md
- academic-writing-skills/latex-thesis-zh/references/latex/compilation.md
- 上述两公开文件对应的 docs/skills/latex-thesis-zh/resources/ 与 docs/zh/skills/latex-thesis-zh/resources/ 镜像
- tests/skills/latex_thesis_zh/test_compile_outdir.py（新增）
- tests/skills/latex_thesis_zh/test_latex_thesis_zh_scripts.py（仅 TestCompileZh/现有 compile 区段，等 C2 交接后编辑）
- 本子任务 research/ 和隔离 smoke 产物（实际构建在临时目录，不把二进制提交为公共 fixture）。
父任务拥有 manifest 和最终 spec/集成检查。其他技能的 compile.py 不受本任务影响。

## 验证设计（R4）
mock 只替代外部进程/工具发现，测试调用真实 LaTeXCompiler.compile 和 CLI main，
在 tmp_path 创建独立 source/build 和可区分的 PDF，验证实际命令、cwd、退出码与报告。
矩阵：no outdir/relative/absolute/Unicode-space × recipe/compiler；
return0+target/return0+missing/return非0+target；source-only stale PDF；
所有手动 recipe + outdir 在零 subprocess 下拒绝。
shell-escape 及无 outdir 手动配方复用原回归，不扩展清理/watch。

环境已有 latexmk+XeLaTeX 时，以最小合成 article 和新隔离目录运行 wrapper，
记录精确命令、exit、stdout/stderr、工具版本、目标 PDF 路径及大小。
不需要 GUI 或页面渲染；此处证明构建产物定位，不是学位论文模板/视觉验收。
若不具备 TeX，则软件修复的 mock 验证可交付，但真实 TeX 行标 UNVERIFIED。

AC1→路径规则/命令矩阵；AC2→成功判据/三态测试；AC3→手动组合拒绝；
AC4→已有有效路径回归；AC5→真实函数测试+环境条件 smoke；AC6→公开契约与资源门禁。
回滚只撤本任务精确 diff，不能整份覆盖与 C2 共用的测试文件或清理原论文产物。
