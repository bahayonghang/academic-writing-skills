# 父任务及三个子任务实施验收

日期：2026-09-10。基线：`dev` / `dd9f1e2a7f9bef164889df7016ffa942dd33d963`。
结论：**已完成批准范围内的实施与验证，父子24项AC均通过；无遗留实施阻断。**
实施验收时四任务保留 `in_progress`，以 `meta.implementation_complete=true` 标记完成。
2026-09-10 后续用户明确要求先提交和归档已有任务，再创建 paper-audit 优化任务；
据此授权执行本地定向提交、四任务归档与 journal 收口。未授权远程推送。
工作区原有三份文件保持原字节，见 [execution-start.md](execution-start.md)。

## 交付行为

| 子任务 | 最终行为与证据 |
| --- | --- |
| C1 指南保真 | 修正五份旧指南/示例的数字、因果、首次资格与体裁冲突，补现有逆向提纲示例；五源及十份镜像同步。八场景新版原始响应通过独立五维核读。 |
| C2 一致性语义 | 不再要求合并不同概念；按真实入口装配顺序检查首用，允许合法同义重引；散文件明示覆盖限制，不确定释义保留 NEEDS-LLM。32项新回归覆盖真实API/CLI及坐标。 |
| C3 输出目录 | 命令与PDF检查共用目标目录，进程非0或目标缺失不能报成功；manual recipe + outdir 在工具发现前明确拒绝。最终89项新回归，六组真实TeX路径验证及审阅修复后的单次真实构建通过。 |

源规则仍由技能内 references 拥有。父任务仅同步两份 maintainer spec、manifest 和
验收材料；根SKILL、README、版本、学校阈值、其他技能、共享parser/loader、依赖均未改。
manifest仍为271项，仅8个现有公开source散列变化；没有新增公开资源目录。
历史47条eval与49条trigger逐对象前缀完整保留，当前分别48/50条。

## 最终共享门禁

| 门禁 | 结果 | 证据与限制 |
| --- | --- | --- |
| 最终 `just ci` | PASS，exit0 | [ci-final.txt](ci-final.txt)：版本1 passed；Ruff206文件通过；Pyright0 errors/75既有warnings；pytest1908 passed、2 skipped，180.14s |
| manifest重建及清单检查 | PASS，exit0 | `check_resource_sync.py --write-manifest --inventory-only`，271项，8个source散列更新 |
| 单技能资源检查 | PASS，exit0 | `check_resource_sync.py --skill latex-thesis-zh` |
| 全量资源检查 | PASS，exit0 | `check_resource_sync.py`，271项；完整双语/技术token/链接结构门禁 |
| 文档构建 | PASS，exit0 | [docs-build.txt](docs-build.txt)，20.27s；新增导航均为文件链接，无新增fragment；后续仅编译Python/测试修复，不影响文档构建结果 |
| 独立全树审查 | PASS，遗留问题0 | [implementation-review.md](implementation-review.md)，18项子AC和6项父AC逐项核对，一项C3 P2已修复 |
| C1实际响应 | PASS，8场景五维 | [output-review.md](../../09-10-thesis-zh-guidance-fidelity/research/output-review.md)，raw、输入/规则散列和隔离派发记录齐全 |
| C3实际TeX | PASS，六组路径与最终补丁一次构建 | [原六组](../../09-10-thesis-zh-compile-outdir/research/tex-smoke/results.json)；[修后一次](review-tex-smoke.json)，目标4178字节，源码目录无PDF |
| 差异与原有工作保护 | PASS | 全树 `git diff --check` exit0；原3文件SHA-256与启动记录一致；无用户论文/GUI/安装/提交/归档/远程操作 |

最终CI精确调用（只设置当前命令环境，禁止同步/安装依赖）：

```powershell
$env:UV_NO_SYNC = '1'
rtk proxy just ci
```

资源三个命令通过 `rtk proxy uv run --no-sync python docs/scripts/check_resource_sync.py`
执行；文档命令为 `rtk proxy just doc-build`。完整输出分别保存于上表文件。
`just ci` 保留 check-versions、lint、typecheck、test 四步，没有只以pytest替代全门禁。

两项SKIPPED来自 `tests/skills/paper_audit/test_paper_audit_integration.py:216` 的
`non-Windows Unicode protocol path`：本机win32，returncode为0/3的两例按条件跳过。
相应Windows专用协议回归实际运行；这不是本轮功能失败，也不声称已验证非Windows运行。
既有Pyright告警和TeX的Perl locale回退警告保留，没有扩张到全局设置或无关清理。

## 修前反证与审查修复

- C2初始新增回归在旧实现上27 failed/3 passed；中文紧邻CNN的补充回归另有1 failed
  反证。最终真实API/CLI、32项新回归均已纳入全量CI。
- C3初始回归在旧实现上66 failed/17 passed，直接复现目标目录假失败及源码旧PDF假成功。
  初次组合中的两条C2在途断言失败，在双方完成后已由完整CI验证通过。
- 第一轮全量CI为1902 passed/2 skipped（[ci.txt](ci.txt)）。独立审查另发现
  缺TeX时不支持组合被“安装工具”提示遮蔽；扩展六种配方的工具存在/缺失矩阵，
  修前6 failed/6 passed，见 [review-regression-before.txt](review-regression-before.txt)。
  将组合检查移到工具发现之前后，98项编译回归通过，并重新执行一次真实wrapper构建。
  **最终验收使用修复后的ci-final.txt，不拿第一轮绿色替代最终版本。**
- C1旧版多数保真边界已通过，场景8仅有合法综合引用被要求加强逐篇解释的Minor/P2
  倾向；新版保留该段。不把这个局部观察称作统计质量提升或因果效果。

## 子任务记录与证据边界

- [C1实施记录](../../09-10-thesis-zh-guidance-fidelity/research/validation.md)
- [C2实施记录](../../09-10-thesis-zh-consistency-semantics/research/implementation-check.md)
- [C3实施记录](../../09-10-thesis-zh-compile-outdir/research/validation.md)
- [先例采用与拒绝](../reports/prior-art-research.md)

本轮复用research-paper-writing的逆向提纲及PaperSpine的原稿证据映射，仅落到现有示例；
writing-anti-ai的事实保护经验沿用现有规则，没有引入词典、IR、评分或额外编排。
已验证优势限于这些合成输入的保真与已复现脚本缺陷的消除，不宣称整体优于候选技能。

**UNVERIFIED / missing evidence**：真实论文总体质量、学校class与页面视觉/印刷、
数学符号/单位的完整语义等价、provider benchmark、人工盲评、跨领域泛化、五宿主
fresh-session/权限/安装握手及托管CI矩阵。本地native采样是两个新agent各回答八场景，
不是十六次独立运行或未见样本测试；实际模型/用量遥测未返回，保持null。
原58份spec清单是规划基线；实施新增两份spec约定后，不宣称旧行数/散列仍是现状。
