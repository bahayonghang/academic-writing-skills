# 文档与元数据一致性清理

## Goal

清理本轮审计发现的所有纯文档/元数据/仓库卫生问题：SKILL.md 描述漂移、docs 站镜像缺口、CLAUDE.md 过期描述、git 跟踪冗余。不改任何脚本逻辑。

证据详情：父任务 `research/` 下 crosscut-findings.md、paper-audit-findings.md、zh-findings.md。

## 问题清单

- **XC-5 [medium]** 项目 `CLAUDE.md:104` 写 pyright `"off"`，实际 `pyproject.toml:78` 是 `"basic"`。
- **XC-6 [medium]** `docs/.vitepress/dist/` 既在 `.gitignore:97` 又被 git 跟踪（26 文件），每次文档改动重复提交编译产物；deploy.yml 部署时会重新 build。修法：`git rm -r --cached docs/.vitepress/dist`。
- **XC-4 [low]** 手工 docs 镜像缺 tense-guide（全无）及 paper-audit 的 OVER_CLAIM_GUARD / REVIEWER_PSYCHOLOGY 条目；over-claim-guard 只进了写作 skill 镜像，处理不一致。EN 与 zh/ locale 需同步补。
- **PA-4 [low]** `paper-audit/SKILL.md:326` 称 scoring model "regression-based"，脚本 docstring 明确声明非回归/手调权重，自相矛盾。
- **PA-5 [low]** SKILL.md argument-hint 漏登记 `--regression` / `--tavily-key` / `--s2-key`（audit.py argparse 实际支持）。
- **PA-6 [low]** `critical_reviewer_agent.md:45` 标题 "8 Challenges" 实际 11 维度。
- **XC-1 [low]** en/zh/typst 的 SKILL.md `last_updated` 停在 2026-06-20，未随 07-05 的 deai_check 改动更新。
- **XC-1b [low]** bib-search-citation 的 category=`docs-writing-publishing`，其余五个 skill 均为 `academic-writing`，统一之。
- **XC-6b [low]** `docs/report/csw-vs-aws-analysis.md` 疑似孤儿，确认后删除或归档。

## Requirements

- R1 逐条修正上述文档/元数据项；docs 站 EN 与 zh/ locale 同步。
- R2 XC-6 只解除跟踪不删除本地文件；确认 deploy.yml 不依赖仓库内 dist。
- R3 XC-6b 先确认无引用再处理；有引用则保留并在报告中说明。
- R4 不 bump SKILL.md version（须与 pyproject 同步的全仓约定）；只更新 last_updated。
- R5 注意 SKILL.md 格式化陷阱：全局 hook 对齐表格会触发 ROUTER_ROW_RE contract 测试，改表格后必须跑测试确认。

## Acceptance Criteria

- [ ] CLAUDE.md pyright 描述与 pyproject 一致。
- [ ] `git ls-files docs/.vitepress/dist` 为空；docs 部署流程说明不受影响。
- [ ] docs 站（EN+zh）包含 tense-guide 与 paper-audit 新功能条目。
- [ ] 六个 SKILL.md category 一致；PA-4/PA-5/PA-6 措辞与实现一致。
- [ ] `just ci` 全绿（含 SKILL.md contract 测试）。

## Notes

- 建议在 zh/typst 两个修复任务落地后执行，last_updated 一次性更新到位。
- 本任务零脚本逻辑改动；若发现需要改脚本才能一致，回报父任务另行立项。
