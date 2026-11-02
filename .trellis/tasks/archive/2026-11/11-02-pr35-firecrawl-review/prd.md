# Review and merge PR #35 (Firecrawl literature search)

## Goal

评审外部贡献 PR [#35](https://github.com/bahayonghang/academic-writing-skills/pull/35)（作者 JuampiHernandez / Firecrawl，分支 `add-firecrawl-search` → `main`），判断能否合并，并按维护者决定处理（合并 / 请求修改 / 关闭）。

## Scope

PR 改动 12 个文件（+202 / -11）：

- `paper-audit/scripts/literature_search.py`：新增 `FirecrawlClient`，`search_literature()` / `build_literature_context()` / CLI 增加 `firecrawl_key`。
- `paper-audit/scripts/audit.py`：仅透传 `--firecrawl-key` / `FIRECRAWL_API_KEY`，参数追加在 `run_audit()` / `run_deep_review()` 末尾。
- `SKILL.md` argument-hint、`references/TROUBLESHOOTING.md`、`references/scripts-map.md` 及 en/zh docs 镜像、`docs/resource-manifest.json`。
- `tests/contracts/test_claim_forward_contract.py` 冻结哈希更新；`test_literature_search.py` 新增 5 个测试。

## Requirements

- 合并后结果（PR head + 当前 `main`）本地通过 `just ci` 与 `docs/scripts/check_resource_sync.py`。
- 无 key 时行为不变：S2 + arXiv 仍为默认源，不发起 Firecrawl 请求。
- 不破坏 `run_audit()` / `run_deep_review()` 的位置参数调用。
- 冻结哈希更新只覆盖本 PR 对 `audit.py` 的改动。
- 维护者须对非技术问题做决定：请求里带的 `origin: "academic-writing-skills"` 遥测标签，以及 PR 正文中的 utm 推广链接（不进入仓库）。

## Acceptance Criteria

- [ ] 记录本地合并验证结果（CI 步骤、测试数、资源同步门）。
- [ ] 记录代码评审发现（含严重级别）。
- [ ] 给出合并结论；按维护者决定执行合并或在 PR 上留言。

## Out of Scope

- 不在本任务里重构现有 Tavily 客户端或文献检索流程。
- 不使用真实 Firecrawl key 做线上验证。
