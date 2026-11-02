# PR #35 评审记录（2026-11-02）

## 状态

- GitHub：`MERGEABLE` / `CLEAN`，CI 5 项（ubuntu/windows × py3.10/3.13 + Docs）全部 SUCCESS。
- PR 基点 `8183f08`；此后 `main` 只改过 `docs/resource-manifest.json`，未动 paper-audit 代码。

## 本地合并验证（`origin/main` adbd849 + `pr-35` 607f696，临时 worktree）

- `just ci`：check-versions / lint / typecheck 通过；pytest 2937 passed, 26 skipped。
- `uv run python docs/scripts/check_resource_sync.py`：resource contract passed（308 entries）。
- `test_claim_forward_contract.py` 冻结哈希在合并结果上通过。

## 代码评审

- [LLM] `FirecrawlClient` 与 `TavilyClient` 结构一致：无 key 不发请求、401/403 打 stderr 提示、其余异常返回 `[]`、`limit` 上限 20、结果 `source="firecrawl"`。
- [LLM] `firecrawl_key` 追加为各函数最后一个参数，位置调用兼容；有测试锁定参数顺序。
- [LLM] 默认路径不变：只有提供 key 才创建 client 并提交线程任务。
- [LLM] 低（nit）：`--literature-search` 的 help 文案写成 "Tavily + Firecrawl + Semantic Scholar + arXiv"，没标出前两者需要 key；现有 Tavily 文案本来就这样，不阻塞。
- [LLM] 低（nit）：若 Firecrawl 返回结构变化（如 `data` 为 list），`.get` 会在 `try` 外抛 `AttributeError`；`search_literature` 的 `as_completed` 循环会捕获，不会崩溃。
- 学术事实保护：不涉及 `\cite{}` / 数学 / 术语改动。

## 需维护者决定（非技术）

1. 请求体固定带 `origin: "academic-writing-skills"`，供 Firecrawl 统计来源；不含论文内容。
2. 这是供应商贡献的商业服务集成；项目是 Academic Use Only。PR 正文中的 utm 推广链接不进入仓库。

## 结论

技术上可合并。

## 处理结果（2026-11-02）

- 维护者决定：squash 合并。`gh pr merge 35 --squash --match-head-commit 607f696` → `main` 上 `7d3faea`。
- 核对：`7d3faea^..7d3faea` 为 12 files, +202/-11；与 PR diff 内容一致，仅 `resource-manifest.json` hunk 行号偏移（main 已有新增条目）。
