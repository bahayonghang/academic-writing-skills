# 设计

## 改动面

`academic-writing-skills/paper-audit/evals/trigger_eval.json`、
`academic-writing-skills/paper-audit/evals/evals.json`、
`docs/skills/paper-audit/index.md`、
`docs/zh/skills/paper-audit/index.md`。

四份文件在本任务树中由本子任务唯一写入。
两份 index.md 是手写页，不在 `docs/resource-manifest.json` 中，
因此不涉及 sha256 同步，但仍须通过 `just doc-build`。

## eval 用例设计

trigger 层只验路由边界，不验内容：新增 query 仍应触发 paper-audit，
`should_trigger: true`，`category` 沿用现有取值。

行为层用现有 assertion 类型表达：

- 已指定模式 + 存在旧报告：断言输出含 `quick-audit`，
  且用 `regex` 反向断言不含模式选择措辞。现有 assertion 类型是否支持否定断言
  需先读实际 runner 确认；不支持时改为断言正向陈述串，并在用例说明中记录该限制。
- T3 不落盘：断言不含 `review_results`、含 `missing evidence`、
  provenance 正则只匹配 `[LLM]`。

`evals.json` 通过 Bash 里的 python 读—改—写，`json.dump` 保持
`ensure_ascii=False` 与现有缩进；写后 `git diff` 核对未改动条目零 diff。

## 双语说明页

在两份 index.md 的输出小节（第 63 行附近）之后新增一节，
说明三级交付形态与 T3 下的可用路径。
表述直接引用源文件措辞，不另起一套说法。
中文页与英文页内容对应，不做单侧扩写。

## 一致性核对

逐句比对 `MODE_GUIDE.md` 门控段与 `SKILL.md` 三级边界段，
检查三类冲突：同一概念两处定义不同、同一动作两处归属不同级别、
提问触发条件两处不一致。核对结果写入 `research/consistency-check.md`。
发现冲突不在本子任务修，回退到 intake-gating 或 delivery-tiers 修正。

## 证据分层

- design advantage：仅由文档结构支持的改进（三级定义完整、门控分支齐全）。
- validated advantage：有实跑或测试支持的改进（落盘行为实跑、eval 用例通过、CI 绿）。
- hypothesis：未验证的预期（复问次数下降、审查效率提升）。

本轮不做的验证一律写 missing evidence：真实论文盲评、跨平台安装、独立第三方复核。

## 回退

四份文件各自独立可回退。
`evals.json` 回退后须复核 JSON 格式未被 hook 压平。
