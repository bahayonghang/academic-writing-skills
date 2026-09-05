# 设计

## 唯一规则落点

- abstract-structure.md：增加短小的多组件依赖/并行判断。
- thesis-writing-guide.md：只扩现有章末小结；保持既有模块指针，勿新建第二份小结指南。
- references/modules/literature.md：补主题簇—归因—综合接口；examples/literature-review-rewrite.md 补重新构造例。
- results-analysis-guide-zh.md：增加展示/统计范围的自然语言核对清单；不新增字段 schema、R-/RA-码或强制持久记录。
- over-claim-guard.md 仍是论断强度 owner；其现有规则足以裁决，不复制规则表。

以上路径均位于 academic-writing-skills/latex-thesis-zh/。必要同步其 SKILL 资源说明、
相关 module/routing 指针、docs 对应两语资源和 usage；行为介绍变化同步 README.md/README_CN.md。
只在现有 evals/evals.json、trigger_eval.json 追加具名用例，不换格式、不跑 generic skill-creator。

## 语义边界

数值来源优先于润色效果。展示删除不等于统计重算；排除缺测必须说明样本/分母，只有同一
评估集合和协议可比，不能把“各自重算”误当共同集合。不替用户执行重算。
合法限定和联合任务目标保持；单段、字数、固定图数与全英文缩写禁令不升级为通用硬规则。
源码保护与既有 polish/deai 规范同源，不新增保真引擎。

## 输出评估

至少七个新 output 场景：串行摘要、并行摘要、三类小结（可一例含三段）、综述作者流水账、
主题综合正例、展示/冻结聚合、缺失率/共同样本。每例明确输入事实、允许变更与禁止断言。
在当前 Agent 内加载修改后的指南回答合成用例，把实际响应、来源范围、protected token 对照和
逐项裁决保存于本任务 research/output-evidence.md；这属于本地 Agent 输出观察，
不称 provider A/B 或独立人类盲评。既有 JSON 静态检查只能证明语料形状。
