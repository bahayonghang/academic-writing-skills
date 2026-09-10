# C1 八场景实际响应独立保真核读

日期：2026-09-10。Reviewer：`/root/quality`（已派发的 `trellis-check`）。
证据类型：**local native agent response review**。本报告核读原始回答，不改写回答、不替
实施者补造结果。新旧各为一个隔离 agent 对八场景的一次批量响应，不能计作十六次独立运行。

## 结论

新版八例均通过本任务的五维保真核读，AC1–AC4 的指定场景行为成立；AC5 的八例响应、
输入隔离和历史前缀保留条件通过。旧版同样守住数字、因果和首次资格等主要边界，不能
预设旧版必须失败。旧版场景8对合法综合引用给出不必要的风格修改倾向；新版保留该段。
这是一项局部观察，不构成统计质量提升、因果效果或跨领域泛化结论。

当前新版回答没有需返回修复的 P1/P2 保真失败。AC6 的双语/manifest/构建由父任务
集成审查另行验收，本报告不以响应通过替代这些门禁。

## 方法与可追溯性

先读 C1 PRD/design/implement、check.jsonl 指向的相关规范，再按固定 fixture 对照
`output-before.md`、`output-after.md` 原始回答逐例核读。检查数字及其来源、范围与确定性、
术语实体、引用/标签/公式、授权范围。severity/priority 是问题分级，不把回答中的 P1
诊断标记误作回答本身失败。

独立脚本核对结果：

- 两个 packet 的 `# User requests and inputs` 内 LaTeX 输入逐字符相同，与
  `evals/fixtures/guidance_fidelity.tex` 一致，均含八个场景。
- `sampling-common-rules.md` 在每个 packet 中出现一次且完全相同，内容为未改动的
  results-analysis 证据阶梯及 routing 总则。没有把不同共同规则混入前后比较。
- `before-rules/` 五份快照逐字节匹配 `baseline-hashes.json`，内容均存在于 before packet。
  当前五份源规则的 UTF-8/LF 散列匹配 `after-hashes.json`，内容均存在于 after packet。
- 已重新计算 `sampling-metadata.json` 的 packet、rules、input、fixture、common 与 raw
  散列，全部匹配。input-section 散列对应标题后文本去掉前导空行，fixture 散列仅对应
  LaTeX 正文文件；两者对象不同，数值不应直接比较。
- `evals.json` 原47条对象按顺序完整保留，当前48条；`trigger_eval.json` 原49条按顺序
  完整保留，当前50条。比较依据是保存的 baseline JSON 对象前缀，而非文件格式。
- 两个 packet 均无 `expected_output`、`assertions` 或前一轮回答。

`sampling-dispatch.md` 保存完整 spawn message、参数及 after 轮的 follow-up。
两个请求只允许读取各自 packet、写入各自 raw 文件；未给评分 rubric、eval 断言、前轮
答案。记录的 `fork_turns=none` 隔离会话历史；主线程另确认两个 canonical agent 均完成。
该记录来自实际调用的转录及 sampler 自述，不是底层访问日志或沙箱独立审计。
after sampler 的角色疑问及跟进指令完整保留；跟进只确认输入限制，没有添加解题提示。

| 项目 | before | after |
| --- | --- | --- |
| canonical agent | `/root/guidance/sample_before` | `/root/guidance/sample_after` |
| spawn | `agent_type=default`, `fork_turns=none` | `agent_type=default`, `fork_turns=none` |
| 请求模型 / effort | `gpt-6-astra` / `high` | `gpt-6-astra` / `high` |
| 实际模型 / 用量遥测 | 未返回，null | 未返回，null |
| raw 最后写入 UTC | `2026-09-10T12:44:06.516036+00:00` | `2026-09-10T12:49:40.683633+00:00` |

写入时间不是 provider 开始/结束时间；未获取独立 UUID、随机种子、temperature 或
token/cost 数据，不推测这些元数据。`fork_turns=none` 也不会消除共享 system/developer
政策。采样输入包含公开教学示例，其中场景1/2和场景8与示例重合，因此不是未见样本测试。

### 文件散列

以下 raw/packet 使用 SHA-256 原始字节；fixture 是 UTF-8/LF 文件。完整五源规则散列见
`baseline-hashes.json`、`after-hashes.json`，已逐项复算。

| 对象 | SHA-256 |
| --- | --- |
| fixture | `4959ec3c0aa9b64848970194b3ec2efe135c045940bb6dae2040cde97344b269` |
| before packet | `8aa4f28f0aa7dd1dac4ad7f96a727ac45fc400b1ecabc6c8f4b8a2191b95aa57` |
| after packet | `dcc06bcbec52d8741644c8723fed9d9d66ddf5a354ab4e2a784091f0bab096f9` |
| 共同规则 | `78b2fc2ab98e7dfac0efa72fbbd3b4fd0e557d4451eef966e75d93bbcc831737` |
| before raw | `57157dd2e802a91e57bfebc715e4a41da79acb6005b262bd95eee314aeebde93` |
| after raw | `57197fd751601b3a9e1fba5c5463e3e2dd48ff31cad6e4dd71232015e345dc57` |
| 两轮相同 input section（UTF-8/LF） | `790134ae22d2ab59c162d698003e9b5936199e9a00c53d6d2ff22c61338ec5a8` |

## 逐例五维核读

下文 before/after 行号分别指同目录原始回答文件。没有受保护 token 的维度标为
“无输入载荷”，不把未出现的语法形态当作通过了压力测试。

| 场景 / 原始响应锚点 | 数字及来源 | 范围/确定性 | 术语实体 | 引用/标签/公式 | 授权范围 | before / after 结论 |
| --- | --- | --- | --- | --- | --- | --- |
| 1：before:7–9；after:6–9 | 两轮均不添加数字或指标 | 两轮保留“可能”，不声称已提升 | 两轮保留“该方法”“预测性能”，不擅自改成准确率 | 无输入载荷；未新增引用/公式 | 请求允许替换句，两轮仅给局部建议 | 五维均通过 / 五维均通过 |
| 2：before:19–30；after:17–28 | 两轮保留95%，不创造基线或增幅 | 限于测试集T，明确不能由孤立数值推导提升/长程依赖机制 | 注意力模型、T、长程依赖均保持原对象 | 两轮保留 `\ref{tab:single}` 的内容 | 请求允许 AXES 检查和改写，两轮均为当前段提案 | 五维均通过 / 五维均通过 |
| 3：before:36–44；after:32–40 | 两轮保留95%、91%、100/50轮；before 的4个百分点为95−91，来源明确，不是新增实验 | 两轮指出预算混杂与未记录条件，不把“消融”标签当组件/因果证据 | 完整模型、模块A及噪声抑制对象均不变 | 无引用/标签/公式输入；百分比值保持 | 请求局部建议，两轮未补实验记录 | 五维均通过 / 五维均通过 |
| 4：before:50–58；after:44–52 | 两轮保留平均95%/91%及配对记录；before 的4个百分点可直接复算；均未加显著性 | 保留当前设置下组件贡献，拒绝无测量的噪声抑制归因，不一律降为无依据猜测 | 模块A、预算、优化器、种子集合与具体机制均不换义 | 无引用/标签/公式输入；百分比值保持 | 请求局部建议，两轮只收窄机制主张 | 五维均通过 / 五维均通过 |
| 5：before:64–66；after:56–58 | 无增补样本数、效应值或统计量 | 两轮认可给定区分性证据并保留强因果表述，严格限于协议P/测试块T | 噪声通路N、中介/恢复试验及所列替代解释保持 | 两轮原样保留 `$z=x+\epsilon$`、`\ref{tab:intervention}` | 用户不要求重写，两轮明确保留原句 | 五维均通过 / 五维均通过 |
| 6：before:74–76；after:65–68 | 无新增优先权检索数据或年份 | 两轮删除“首次”，明确 hedge 不能替代检索，没有伪造创新资格 | 两轮保留 X 用于 Y，不改变对象关系 | 无输入载荷；未添文献 | 润色请求允许局部删去无依据资格，两轮不宣称完成检索 | 五维均通过 / 五维均通过 |
| 7：before:80–89；after:72–82 | 两轮以输入的1100字、本校1000—1500字、两个工作段及章号为依据，没有外推学校数值 | 限于假设H、CPU及离线回放；不宣称现场/在线/操作者验收；承认未见全文 | 理论工作与工程工作保持，没有强加 GPU、超参数或实验 | 两轮保留 `$0<\eta<1$`、`\cite{definition}` | 只作诊断，未扩写摘要或自动调整章节 | 五维均通过 / 五维均通过 |
| 8：before:93–103；after:86–94 | 两轮只使用输入的95%、方法B/数据集D和源位置，无新结果 | 两轮拦截“所有缺失条件”及重建主张；新版保留已成立段落及无显式过渡词关系 | 两轮保持固定采样/掩码建模、B/D及界面实体，无造因果衔接 | 原样保留 `\cite{regular,masked,survey}`、`\ref{fig:ui}`；before:97虽未改键，却建议因三个引用加强逐项解释 | 两轮仅诊断/移位提案，不执行正文修改；prev.tail/next.head仅作证据 | 五维载荷通过但 AC3/AC4 合法综合保护有偏差 / 五维及场景要求均通过 |

场景8的旧版问题为 **Minor/P2 [LLM]**：`output-before.md:97` 将三个引用本身视为
需要加强逐项解释的理由。这不等于已经删改 citation key，也不应夸大成引用被破坏；但它对
已成立的主题综合提出了无必要的风格处置。对应旧规则是 before snapshot
`references/writing/writing-philosophy-zh.md:94、104` 的逐篇展开要求。当前源的同文件:117
允许主题综合，`examples/logic-and-experiment.md:52` 明确保留，`output-after.md:90`
正确执行。旧 raw 保留，未为制造通过而润色或删除该发现。

## AC 对照

| AC | 实际证据与判断 |
| --- | --- |
| AC1 | after 场景1不创造量化事实，场景2不由95%推导改善/机制，场景5保留充分证据的强结论；通过。源规则见 philosophy:65–75、logic:9–20。 |
| AC2 | after 场景3指出预算混杂，场景4区分组件贡献与机制归因，场景6移除未检索首次；通过。源规则见 over-claim-guard:43–58、122、129–130。 |
| AC3 | after 场景7服从给定学校要求，保护理论/CPU工程工作；场景8保留综合引用；通过。源规则见 philosophy:101–123、abstract-structure:3、133–134。 |
| AC4 | 源示例:29–60提供章目标、三个源段的主题/证据/处置映射及 current-only 授权边界；after 场景8实际只诊断且保留合法段落。通过；本次没有另做“获准改写 current”分支采样，不能宣称该额外分支已运行。 |
| AC5 | 新旧各八例原始回答已逐项核读；输入/断言隔离记录及47/49条历史前缀保留均已核验；通过。该结论以本地调用记录/自述为证，不冒称 provider trace。 |
| AC6 | 本报告已分离静态规则、实际响应和真实论文效果；双语/manifest/链接/构建门禁由父集成报告负责，本报告不独立宣布 AC6 完成。 |

## 未验证范围

- provider benchmark、模型间比较、重复采样统计、人工盲评、真实论文总体质量、跨领域准确率：**UNVERIFIED**。
- 五工具 fresh session 与权限/安装握手：**UNVERIFIED**，本地 native child 不代表五工具验收。
- 新旧 packet 含共同政策/教学例子，未排除模型常识及 system/developer 指令的影响；不能将
  前后差异归因于规则修改，也不能声称对未见输入的泛化改善。
- fixture 没有独立 `\label{}` 定义或其他数学环境形态，当前核读只证明实际出现的 citation/
  ref/inline math 保持，不覆盖完整 LaTeX 语法或论文表格原件真实性。
- 本报告只新增核读文档，没有修改产品或 raw 回答；lint/typecheck/tests 的最终状态见父任务
  `research/implementation-review.md` 与 `research/integration-validation.md`。
