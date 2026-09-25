# paper-writing-studio catalog 登记执行计划

## Entry

2026-09-23 用户要求先登记本技能再实施 latex-defense-zh 任务树；本任务 `task.py start` 后执行。
文件边界：design §1、§2 所列文件。其他路径的改动先停下上报。

## Steps

1. 重写 `SKILL.md`（design §3）；改 `agents/interface.yaml`、`manifest.json` 版本；重建 `reports/skill-ir.json`；改 README 两处。
2. 写三份 examples；用 Python 脚本写 `evals/evals.json` 与 `evals/trigger_eval.json`。
3. 改契约测试与安装器列表（design §2 前六行），运行 `tests/contracts`。
4. docs：资源页（examples 的 zh/en）→ 重建 manifest → 总览页 → 索引、首页、快速开始、usage、安装页 → config.ts 侧栏 →
   README、README_CN → CHANGELOG → AGENTS、CLAUDE → spec 技能数。
5. 执行下列命令；全部通过后，按父任务 `09-23-latex-defense-zh` 的顺序启动 C1。

## Commands

```bash
rtk proxy uv run --extra dev python -m pytest -q tests/contracts academic-writing-skills/paper-writing-studio/tests
rtk proxy uv run python .agents/skills/qiaomu-meta-skill/scripts/validate_skill.py academic-writing-skills/paper-writing-studio
rtk proxy uv run python docs/scripts/check_resource_sync.py --write-manifest --inventory-only
rtk proxy uv run python docs/scripts/check_resource_sync.py
rtk proxy just skills-install --list
rtk proxy just ci
rtk proxy just doc-build
```

## Rollback

`git checkout` 还原 design §2 中的已有文件与 `SKILL.md`、`interface.yaml`、`manifest.json`、`README.md`、`reports/skill-ir.json`；
删除新增的 examples、evals 两个 JSON、总览页与资源页，再运行 `--write-manifest --inventory-only`。
本计划不授权 commit、archive 或 push。
