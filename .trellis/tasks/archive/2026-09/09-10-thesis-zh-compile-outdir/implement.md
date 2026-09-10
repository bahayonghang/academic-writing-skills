# C3 执行计划

依赖：父任务审批；C2 先交接共用 scripts 测试文件。
1. 复跑父任务 G6 探针，保存当前 outdir 假失败/旧 PDF 假成功证据。
2. 新增真实 wrapper 路径矩阵回归，确认当前实现失败。
3. 统一目录计算、两条 latexmk 传参和成功检查；显式拒绝手动 recipe+outdir。
4. 同步 compile/compilation 两份说明及镜像，保留 shell-escape 与编译/视觉区分。
5. 执行局部回归；若已有工具，执行 design 的隔离实际 wrapper smoke。
6. 父任务更新 manifest 后完成资源门禁；在 research/validation.md 标明 mock/TeX/未验证项。
7. 交付时注明默认行为变化与不支持组合；提交/归档按后续授权，不自动推送。

```powershell
rtk uv run --no-sync python -m pytest tests/skills/latex_thesis_zh/test_compile_outdir.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_scripts.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_coverage.py -q
rtk uv run --no-sync python -m pytest tests/contracts/test_skill_contracts.py -q
```

实施后实际 smoke 命令：用脚本创建的临时目录绝对路径替换 <isolated>/main.tex，
从仓库根通过
`uv run --no-sync python academic-writing-skills/latex-thesis-zh/scripts/compile.py <isolated>/main.tex --recipe latexmk --outdir build`
运行。不直接运行 TeX 二进制，不调用 --clean，不覆盖用户论文。
先检查可用工具，不安装依赖；工具缺失不阻碍软件回归，但必须保留真实 TeX 缺口。

若需支持任意 latexmkrc、jobname、auxdir 或手动 Bib 后端 output path，返回规划，
不得以通用编译系统取代本次修复。
