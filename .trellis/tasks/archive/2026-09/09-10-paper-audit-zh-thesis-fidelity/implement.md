# Implementation Plan

## Preconditions

当前仅授权规划。未来实施前读取 PRD/design、研究探针、场景合同和 JSONL，核对工作树/HEAD，保护原有 `.gitignore`、`.trellis/.template-hashes.json`、`skills-lock.json`。独立计划审阅完成、用户明确指令实施本任务后再运行 `task.py start`。

## Ordered Work

1. 冻结24条历史eval/20条trigger对象、当前源码及reviewer规则hash；从旧C1材料提取纯输入。在改产品前收集 E01—E08/E12/E15 的旧审查实际响应，不用写作侧旧答案代替。
2. 先补有反证价值的 D2 回归：clean伪问题、正常exit1追加Minor、Info四维扣分、首用清单假通过。修具名adapter、stderr覆盖、Info评分和zh清单；验证非法JSON/exit2/超时仍显式失败。
3. 修 D3：正文只在子文件的工作区缺证据反证；实现一次装配/所有消费者共用，保存来源与警告。验证单/多文件、缺include/includeonly、原subsection坐标、英文tex及Typst/PDF/overwrite。
4. 修 D1/D4：校准guard和中文准则、实际共用模板/agent/workflow路径，复制两份必要规则。验证按文档路径写评论→真实consolidation→quote核验。
5. 追加绑定合成fixture的eval与中文审查trigger正例、直接润色/compile repair负例。用相同输入收集新版实际响应，独立核读 E01—E08/E12/E15；至少一例真实reviewer JSON进入消费链。按lane max8分批，不扩大配额。冻结源后同步两语资源、manifest和最小spec。
6. 执行集成门禁、保护面diff和独立checker审阅；修任务内问题后只重跑受影响检查。所有AC有证据才标记实施完成，未来提交/归档遵循届时授权，不推送发布。

## Validation Commands

使用已存在环境，`--no-sync` 防止隐式安装；工具缺失记录并暂停依赖步骤，不装新依赖。

```powershell
rtk proxy uv run --no-sync python -m pytest tests/skills/paper_audit/test_zh_check_adapters.py tests/skills/paper_audit/test_zh_dispatch_integration.py tests/skills/paper_audit/test_zh_thesis_lane_wiring.py tests/skills/paper_audit/test_workspace_layout.py tests/skills/paper_audit/test_paper_audit.py tests/skills/paper_audit/test_paper_audit_deep_review.py -q
rtk proxy uv run --no-sync python -m pytest tests/skills/paper_audit tests/contracts -q
rtk proxy uv run --no-sync python docs/scripts/check_resource_sync.py --write-manifest --inventory-only
rtk proxy uv run --no-sync python docs/scripts/check_resource_sync.py --skill paper-audit
rtk proxy uv run --no-sync python docs/scripts/check_resource_sync.py
rtk proxy just doc-build
$env:UV_NO_SYNC = '1'
rtk proxy just ci
rtk proxy git diff --check
```

`just ci`必须保留 check-versions、lint、typecheck、test 四步。链接使用文件级或两语一致显式锚点，build不代替fragment检查。当前探针保留为before反证，after另存，不覆盖。

| Gate | 保存证据 |
| --- | --- |
| AC1/AC4 | 输入/旧新规则hash、实际模式和可见模型信息、每批调用与原始响应、独立逐例核读；未知遥测null |
| AC2 | 真producer→adapter→Phase0/JSON；clean0缺陷、Info两套评分不扣分、exit1无额外Minor，错误路径未被吞掉 |
| AC3 | 子文件在full_text/sections/claim-map、一次装配、原句quote_verified、原坐标和覆盖警告，源码hash不变 |
| AC5 | eval/trigger历史对象前缀、tests/CI、资源/docs命令及exit、白名单/保护面diff和原3文件hash |

使用当前可用native agent或如实标识的sequential单agent采样，不以scripted fallback冒充，不新建provider客户端。synthetic输入只写任务research或测试tmp_path；清理前核对具体路径，不访问真实论文和UI。

## Completion Boundary

本任务验证本地审查链与合成正反例。任何语义AC未执行就保持未完成，不能以eval JSON、词命中或旧写作CI替代。真实学位盲评、学校版式、人工收益和五宿主/provider benchmark继续UNVERIFIED。交付列明通过、失败、跳过与未验证。
