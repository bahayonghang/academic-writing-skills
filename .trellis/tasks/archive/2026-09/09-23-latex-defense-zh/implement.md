# latex-defense-zh 父执行计划

## Entry

前置：`09-23-pws-catalog-register` 已通过其门。父任务不直接写产品文件。用户明确授权实施后，按 C1 → C2 → C3 → C4 顺序逐个 `task.py start` 子任务；
前一子任务通过其质量门并记录证据后，才启动下一子任务。

## Order and gates

1. C1 框架与主题：交付 references（7 份）、两主题 + 宏包 + 合成演示稿、本技能 docs 资源登记；
   门：演示稿两主题编译、主题常量测试、`check_resource_sync.py --skill latex-defense-zh`、`just ci`。
2. C2 提取/规划/构建：交付 tex_loader 副本、四个脚本、Jinja2 模板、fixture、plan-schema 双语页；
   门：AC2/AC4/AC5/AC6 测试、fixture 生成稿编译、`check_resource_sync.py --skill latex-defense-zh`、`just ci`。
3. C3 质量门：交付 check_deck、render_preview、quality-gate 参考与双语页；门：AC7/AC8 测试、资源检查、`just ci`。
4. C4 入口与集成：交付 SKILL.md、examples、evals、agents、其余登记点、双语 docs 入口页、spec 契约；门：AC1/AC9/AC10；
   随后执行 AC11 真实论文验收。
5. 父集成复审：逐条核对 AC1–AC11 证据；确认 `git diff --stat` 只含父 design §1、§7、C4 登记清单与 pws 登记任务 design §1、§2 内文件。

## Commands

```bash
rtk proxy uv run --extra dev python -m pytest -q tests/skills/latex_defense_zh
rtk proxy just ci
rtk proxy uv run python docs/scripts/check_resource_sync.py --write-manifest --inventory-only
rtk proxy uv run python docs/scripts/check_resource_sync.py --skill latex-defense-zh
rtk proxy uv run python docs/scripts/check_resource_sync.py
rtk proxy just doc-build
```

AC11 流程（C4 末尾）：以用户给出的论文仓库路径为 `--thesis`，输出目录由用户指定或使用会话 scratchpad；
依次执行 extract → plan → LLM 填写 → outline 确认 → build --compile → check → preview → 目视。
证据写入 C4 `research/acceptance-real-thesis.md`，只记录页数、D-* 计数、退出码和人工结论，不记录论文内容。

## Rollback

C4 登记改动可整体还原（契约列表、installer、docs、README、AGENTS、CLAUDE、CHANGELOG、spec 索引）。
C1–C3 的产品文件为纯新增；docs 侧改动为 `docs/{,zh/}skills/latex-defense-zh/`、`docs/resource-manifest.json`、
两份安装页与 `tests/contracts/test_docs_bilingual_resources.py` 一行。删除新增目录、`git checkout` 这四个已有文件即回到基线。
本计划不授权 commit、archive 或 push。
