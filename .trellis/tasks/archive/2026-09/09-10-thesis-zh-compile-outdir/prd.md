# 修复中文论文编译输出目录与产物判断

## Goal
使现有 latexmk 编译路径把 --outdir 传给工具，并按同一目录验证和报告 PDF，避免假失败/假成功。

## Background
父任务 G6：
`academic-writing-skills/latex-thesis-zh/scripts/compile.py:278`
将 outdir 传给 latexmk，但第 330 行仍查源码目录；
第 203–239 行的显式 compiler 路径忽略 outdir。
父任务保存了当前 mock 复现，以及09-05任务的真实 TeX 记录指针。

## Requirements
- R1：默认/显式 latexmk recipe 和显式 compiler 路径使用一致的输出目录规则。
- R2：正常完成的 latexmk 路径（含无 outdir）需进程成功且目标目录 PDF 存在；别处旧 PDF 不可替代目标产物。
- R3：不支持的手动 recipe+outdir 组合明确失败，不静默忽略参数。
- R4：保留无 outdir 工作流、shell-escape 保护和错误传播，并给出有边界的验证证据。

## Acceptance Criteria
- [x] AC1（R1）：相对 build、绝对目录、含空格/中文目录在默认 latexmk、显式 --recipe latexmk 和 --compiler xelatex/lualatex 路径均传递正确，报告一致的目标 PDF。
- [x] AC2（R2）：正常完成的 latexmk 路径只有进程 exit 0 且目标 PDF 存在时返回0；有 outdir 时源码目录旧 PDF 不能替代缺失目标；无 outdir 的显式 compiler 在 exit0但PDF缺失时也必须失败；latexmk 非0时即使有 PDF 也不能报成功。
- [x] AC3（R3）：手动单次/多步 recipe 加 outdir 时，在运行任何 TeX/Bib 工具前明确拒绝并给支持的 latexmk 路径提示；不新增 recipe/旗标。
- [x] AC4（R4）：无 outdir 的有效编译、已就绪且无需重建的目标 PDF、既有手动 recipe、shell-escape 信任门禁和失败分支仍有回归。
- [x] AC5（R4）：mock 测试真实调用 ZH wrapper；环境已有 TeX 时在新建隔离目录执行实际 wrapper smoke 并检查目标路径；缺工具时写明 missing evidence，不能声称真实 TeX 已验收。
- [x] AC6（R4）：compile 两个公开说明及双语镜像写明路径相对基准、支持/拒绝组合与成功边界，相关门禁通过。

## Non-goals
不实现手动 BibTeX/Biber recipe 的完整 outdir 协同，不改 --clean、压缩、字体/工具安装、
GUI、watch 生命周期、其他技能编译器、任意 latexmkrc/jobname/auxdir 解析。
本任务检查位置与进程结果，不以 mtime 强制重编译，不保证 PDF 排版或内容正确。
2026-09-10 用户已授权随父任务实施；提交、归档和发布仍按单独授权处理。
