# latex-thesis-zh 规范逐项终检与盲审支持（父任务）

## Goal

让 latex-thesis-zh 在论文定稿阶段能**对照一份学校规范文件逐项检查**（终检），机制做成通用的
（清单格式标准化，可扩展到 PKU/THU/任意学校），并以《燕山大学研究生学位论文撰写规范（2024版）》
为第一个完整落地实例；同时新增**盲审个人信息隐匿**能力：检查泄露点 + 生成盲审版本 tex（不动原文件）。

## 需求来源

1. 用户请求（2026-07-08）：
   - 基于 `ref/关于印发《燕山大学研究生学位论文撰写规范（2024版）》的通知（附件）.pdf`
     优化 `templates/yanshan.md` 的检查功能，支持最后对照规范文件逐项检查；
   - 机制要通用，可搜索添加 PKU、THU 等学校撰写规范放进去逐项检查；
   - 盲审个人信息隐匿要求（用户原文，须逐字保真收录）：
     1. 隐去作者及导师姓名、致谢等；
     2. "攻读学位期间取得的成果"部分，删除姓名、成果名称和期刊页码，
        只保留本人署名次序和期刊名称、年份。如：`[1]第一作者，机械工程学报，2024`；
   - 盲审的修改规范落地方式：新建一个盲审版本的 tex 即可（不修改原文件）。
2. 规范原文：PDF 已用 pypdf 提取全文（35 页，无密码障碍），存于本任务
   `research/yanshan-2024-spec-extracted.txt`，实现时以此为清单条目唯一事实来源，逐条标注 § 依据。

## 子任务地图

| 子任务 | 交付物 | 依赖 |
| --- | --- | --- |
| 07-08-spec-final-check | 通用「逐项检查清单」格式约定 + `check_spec.py` 终检脚本 + yanshan.md 重写为 2024 规范快照与全量清单 + SKILL.md 路由 + 契约测试 | 无（先行） |
| 07-08-blind-review | `blind_review.py`（--check / --generate）+ `references/modules/blind-review.md` + yanshan.md 盲审节 + SKILL.md 路由 + 测试 | 弱依赖 spec-final-check 的 yanshan.md 重写（避免同文件冲突，顺序执行） |
| 07-08-template-checklists | thuthesis.md / pkuthss.md / generic.md 增加逐项检查清单（网络核实官方规范，不可靠来源不编造） | 强依赖 spec-final-check 定义的清单格式与检查器注册表 |

执行顺序：spec-final-check → blind-review → template-checklists（后两者理论可并行，但都改
yanshan.md/SKILL.md，串行避免冲突）。

## 跨子任务验收标准

- [x] `just ci` 全绿（lint + pyright + 全部 tests）。
- [x] 集成验收 1：对 `academic-writing-skills/latex-thesis-zh/evals/fixtures/thesis-project/main.tex`
      运行 `check_spec.py --template yanshan --degree doctor`，输出逐项报告
      （每条含 ID / 规范依据 § / PASS-FAIL-NEEDS-LLM-MANUAL 状态 / 证据）。
- [x] 集成验收 2：同一 fixture 运行 `blind_review.py --check` 能检出预埋泄露点；
      `--generate` 产出 `*_blind.tex` 副本且原文件字节不变。
- [x] 集成验收 3：`--spec-file` 传入自定义清单 md 可完成同样的逐项检查（通用性证明）。
- [x] 三个模板清单（yanshan/thuthesis 或 pkuthss/generic）都能被同一契约测试解析通过。
- [x] SKILL.md 路由契约测试（ROUTER_ROW_RE）与 trigger evals 通过。

## 红线约束（全程适用）

- 不修改 `\cite{}` / `\ref{}` / `\label{}` / 数学环境内容；盲审生成同样不触碰。
- 不编造规范条目：yanshan 清单每条必须能对应 research 提取文本中的 § 章节；
  THU/PKU 搜索不到可靠官方来源的条目标注 missing evidence，不臆造。
- 输出建议一律带 `[Script]` / `[LLM]` 来源标注与 severity。
- SKILL.md `version` 保持与 pyproject 一致（5.2.0），只改 `last_updated`；不做单任务版本 bump。

## 非目标

- 不实现「编译 PDF 后的版式测量」（页边距实测、字体渲染核对等归 manual 项，提示用户自查）。
- 不为燕山大学新造 LaTeX 文档类/模板文件；仍是规范快照 + 检查，排版实现以学校官方模板为准。
- 不改动 latex-paper-en / typst-paper 等兄弟技能（parsers 对齐锁不受影响时不动）。
