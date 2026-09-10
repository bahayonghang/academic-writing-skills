# CI、部署与测试发现范围审查

日期：2026-09-07。审查过程只读取本地仓库、Git 历史和 GitHub Actions 状态；没有修改远端状态，也没有把历史失败解释成当前提交失败。

## 结论

当前本地 `HEAD` 与 `origin/dev` 均为 `f32fa909971b6975820dc4ad5565c278d5496b62`，但最近十次 GitHub Actions 运行没有任何一条针对该 SHA。`origin/main` 当前为 `6928c0a5e01367cfe08fa6732d090cb0fe113e5c`，最近十次运行也没有覆盖该 SHA。当前仓库唯一自定义 workflow 是文档部署；它只在 release published 时运行，没有 pull request 或普通 push 的 Python 质量门禁。

近十次运行中唯一失败是 2026-06-13 的旧提交 `73e428da403bcf9dd8579a1167c39a09e36f26f1`。失败原因为 VitePress 检出两个死链；提交 `7913cbb47f1a6bc408e52af25daeb58be7ecf0ff` 已修复这些链接，随后同一 workflow 成功。因此该运行是已修复的历史故障，不是当前 checkout 的失败。

## 只读取证命令

以下命令均在仓库根目录执行；`gh` 操作仅查询状态或日志。

```powershell
rtk git rev-parse HEAD
rtk git status --short --branch
rtk git ls-remote origin refs/heads/dev refs/heads/main refs/tags/v6.0.0

rtk gh workflow list --all
rtk gh run list --limit 10 --json databaseId,name,displayTitle,event,status,conclusion,workflowName,headBranch,headSha,createdAt,updatedAt,url
rtk gh run view 27467312342 --log-failed
rtk gh run view 27467312342 --json databaseId,name,displayTitle,event,status,conclusion,headBranch,headSha,jobs,url

rtk git show 73e428da403bcf9dd8579a1167c39a09e36f26f1:.github/workflows/deploy.yml
rtk git diff --unified=20 73e428da403bcf9dd8579a1167c39a09e36f26f1 7913cbb47f1a6bc408e52af25daeb58be7ecf0ff -- academic-writing-skills/latex-thesis-zh/references/modules/template.md docs/skills/latex-thesis-zh/resources/modules/template.md docs/zh/skills/latex-thesis-zh/resources/modules/template.md

rtk gh api repos/bahayonghang/academic-writing-skills/branches/dev/protection
rtk gh api repos/bahayonghang/academic-writing-skills/branches/main/protection
rtk gh api repos/bahayonghang/academic-writing-skills/pages
```

测试发现范围使用下列只读收集命令复核：

```powershell
rtk uv run --extra dev python -m pytest --collect-only -q
rtk uv run --extra dev python -m pytest --collect-only -q academic-writing-skills/bib-search-citation/tests
```

结果分别为 1714 项和 42 项；主线程执行 `just ci` 时共运行 1756 项并全部通过。差额正好是 skill-local 的 42 项测试。

## 历史失败及修复证据

失败运行：<https://github.com/bahayonghang/academic-writing-skills/actions/runs/27467312342>

- event：`push`
- branch：`main`
- head SHA：`73e428da403bcf9dd8579a1167c39a09e36f26f1`
- conclusion：`failure`
- 失败步骤：`Build with VitePress`
- 日志中的直接原因：
  - `skills/latex-thesis-zh/resources/modules/template.md` 包含死链 `./../templates/index`
  - `zh/skills/latex-thesis-zh/resources/modules/template.md` 包含同一死链
  - VitePress 汇总为 `2 dead link(s) found`，构建以退出码 1 结束
- 后果：artifact upload 和 Deploy job 均被跳过。

修复后运行：<https://github.com/bahayonghang/academic-writing-skills/actions/runs/27467927802>

- head SHA：`7913cbb47f1a6bc408e52af25daeb58be7ecf0ff`
- conclusion：`success`
- 修复 diff 将目录式 `../templates/` 链接替换为 `generic.md`、`thuthesis.md`、`pkuthss.md` 和 `yanshan.md` 四个实际文件链接，并同步修改源文件、中英文文档副本。

最近一次自定义部署运行：<https://github.com/bahayonghang/academic-writing-skills/actions/runs/29483875195>

- event：`release`
- head SHA：`f59ac75cfdf9b85d647dae043b6deade5c292cf6`
- conclusion：`success`
- 该 SHA 与当前 `dev`、`main` 均不同，只能证明 v6.0.0 发布时的文档部署成功。

GitHub Pages API 当前返回 `status=built`、`build_type=workflow`、`https_enforced=true`。这证明站点当前已构建，不证明当前仓库 SHA 已通过部署或 Python 门禁。

## 优先级与根因

### P1：缺少当前提交的 hosted CI

证据锚点：

- `.github/workflows/deploy.yml:3-6`：当前只监听 `release.types: [published]`。
- `.github/workflows/deploy.yml:40-44`：workflow 只执行文档依赖安装和 VitePress 构建。
- `justfile:49-65`：`just ci` 在本地组合版本、Ruff、Pyright 和 pytest，但没有任何 GitHub workflow 调用它。

根因不是“当前 Actions 失败”，而是没有 workflow 为 pull request、`dev` 或 `main` 的普通提交运行项目门禁。当前本地门禁虽然全绿，但无法作为 hosted、同 SHA 证据。历史死链失败说明仅在部署阶段发现文档问题会使 artifact 和部署一起中断。

本轮最小改造范围：新增 `.github/workflows/ci.yml`，在 pull request 以及 `dev`/`main` push 上运行：

1. 锁定安装 Python 依赖并执行 `just ci`；
2. 执行 `uv run --extra dev python docs/scripts/check_resource_sync.py`；
3. 使用 `npm ci --prefix docs` 后执行 `npm --prefix docs run docs:build`。

不改变现有 release 部署触发和部署行为。workflow 合入后，还必须以 GitHub Actions 页面中的相同 head SHA 成功运行作为 hosted 验收证据；本地通过不能替代该证据。

必须通过：

```powershell
just ci
uv run --extra dev python docs/scripts/check_resource_sync.py
npm ci --prefix docs
npm --prefix docs run docs:build
```

并核对 GitHub Actions 成功运行的 `headSha` 等于待验收提交 SHA。

### P2：默认 pytest 与项目完整门禁发现范围不同

证据锚点：

- `pyproject.toml:88-92`：`testpaths = ["tests"]`。
- `justfile:107-110`：`just test` 额外枚举 `academic-writing-skills/*/tests`。
- `tests/conftest.py:20-21`：注释明确说明 `bib-search-citation` 的测试依靠 `just test` 的额外 glob 才被发现。
- `docs/installation.md:52-59`：贡献者说明推荐直接运行 `uv run pytest`，该命令当前只收集 1714 项。

根因是 pytest 配置和 `just test` 分别维护测试根目录。直接 pytest 成功时，`bib-search-citation` 的 42 项测试并未运行。

本轮最小改造范围：只修改 `pyproject.toml` 的 `testpaths`，把现有 skill-local 测试目录纳入默认发现范围；不移动测试文件，也不提取新的测试发现脚本。

必须通过：

```powershell
uv run --extra dev python -m pytest --collect-only -q
just test
just ci
```

验收要求：默认 pytest 和 `just test` 均收集 1756 项；全量执行仍为 1756 passed，且没有 collection error。

### P2 后续独立提议：部署 job 权限下沉

证据锚点：`.github/workflows/deploy.yml:8-12` 在 workflow 顶层授予 `contents: read`、`pages: write`、`id-token: write`，因此 build job 也继承后两项权限。最小权限设计应让 build job 只有 `contents: read`，只在 deploy job 授予 Pages 与 OIDC 权限。

该项涉及现有部署行为，本轮选定的“新 CI + testpaths”计划不修改 `deploy.yml`。应作为后续独立改造，在专门审查 Pages environment 与 hosted deploy 后实施。

### P2 后续外部配置提议：分支规则

`dev` 与 `main` 的 branch protection 查询均返回 HTTP 404 `Branch not protected`。新增 CI 后，可另行决定是否把对应检查设为 required status check。该操作属于 GitHub 远端配置，不在本轮仓库文件改造范围内，也不能把未配置的规则记为已验证门禁。

## 状态边界

PASS：当前本地 `HEAD` 与 `origin/dev` 同 SHA；主线程记录 `just ci` 为 1756 passed、Pyright 0 errors/75 warnings、文档构建成功、资源同步 271 项通过；历史死链修复后的 workflow 成功。

FAIL：当前 `dev` 和 `main` 没有同 SHA hosted CI；默认 pytest 少收集 42 项测试。

SKIPPED：没有重复运行全量门禁；没有触发、重跑或修改任何 GitHub workflow；没有修改分支保护、Pages 或 release 状态。

UNVERIFIED：新增 workflow 尚未实施，因而其 YAML 可解析性、Linux runner 行为及同 SHA hosted 结果仍未验证；release tag 是否只能指向已通过检查的提交也未验证。
