# C6 设计

## 1. Exact resource owners
skill=academic-writing-skills/latex-thesis-zh。
references/writing/method-description-guide-zh.md、claim-forward-zh.md、paragraph-roles-zh.md、
abstract-structure.md、structure-guide.md、introduction-guide-zh.md；
references/modules/logic.md、claim-forward.md、abstract.md、structure.md、routing-rules.md；SKILL.md。
不同时再改over-claim-guard重复三类真源；必要链接指向claim-forward-zh。
测试tests/contracts/test_thesis_zh_guidance_fidelity.py只增加独立保真断言，不改历史保护句。
更新.trellis/spec/academic-writing-skills/method-narrative-contract.md文档边界，
其余已存在owner spec必要小节：claim-forward-contract.md、paragraph-roles-contract.md。
公开两语镜像/manifest/evals/README/usage等按父design§3。
无scripts写权限，无新claim-forward-terms YAML，现有词表和CF码表保持。

## 2. Topic mechanisms and output examples
| 主题 / AC | 文档机制 | 反例防护 |
| --- | --- | --- |
| 方法 AC1 | 每条8码分别定义范围、问题例、改写例、风险及LLM责任 | 保留必要超参数与复現信息，不将程序术语一律删掉 |
| 三类 AC2 | 对方法/证据边界、否定定义、未验证弱点分别给建议 | 不删不利实验、不从未验证推导优越性；比喻不机械替词 |
| 桥接 AC3 | 删除预告前后对照，展示指代先行词与最短桥接 | 不复制删掉的内容，不改合法首先/其次 |
| 引号 AC4 | 中文U+201C/U+201D配对、英文独立标点 | 原文引述内容不擅改，数学/键原样 |
| 标题/安排 AC4 | 两文件各写适用位置与无公式标题例 | 术语名称、正文公式、模型名不静默改 |

指南输出用现有Severity/Priority/[LLM] suggestion块；只展示合成短例。
方法8码是文档检查标签，不扩展脚本M码集合；
M-FORMDUPE负责语义复述，PR-EQ-NARR只定位算子逐步翻译信号，同位置去重后由LLM裁定。
M-SEMICOLON指向expression已有LLM层；N-ISOLATE不得删除复现所需参数，先核是否放错段落职责。
拆句核对token多重集指路UP-MATH，只承诺不变性，不声称语义已保持。

## 3. Routing and evidence (AC5)
SKILL/reference map沿用现有模块，不新增module行。
触发词：张量/交换轴/Concat→logic方法指南；正文与架构图叫法→方法一致核读；
弱点写成优点→claim-forward；删预告后“上述”无所指→logic职责；
摘要引号→abstract；标题/章节安排公式符号→structure。
文档中逐一说明LLM-only，不保留“若实现脚本则...”待选分支。
新增合成eval项保留历史前缀并覆盖正确路由和不应改写例；
只验证文件格式/事实保真，未实际运行的provider输出明确UNVERIFIED。
全量CI、资源检查和docs build按父design§4执行；无独立私有语料测试。
回滚本子资源+对应规范/测试差异，不涉及产品脚本。
