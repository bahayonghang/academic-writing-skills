# 设计

## 文件与路径

新增（规划路径，不是现有文件）：academic-writing-skills/latex-thesis-zh/references/writing/engineering-application-chapter-guide-zh.md。
修改同 skill 的 SKILL.md、references/modules/logic.md、references/modules/routing-rules.md，
在 method-chapter-guide-zh.md 既有工程验证放置说明补一条指针，避免第二份正文规则。
同步 evals 两 JSON、docs 两语对应资源/usage、README.md/README_CN.md、docs/resource-manifest.json。
不改 scripts、agents schema、parser 或章节分类器。

## 判断与执行

优先判定“论文材料+章内容”，不能仅凭第六章/平台两词。
新指南：章首研究工件→工程约束；架构选择→系统属性；服务→数据/时间语义、生命周期、
资源与失败边界；界面→操作任务；验证→环境/时长/样本/比较对象/覆盖限制；章末→贡献。
这些是检查角度，材料不支持时省略或标缺证据，不能要求论文新建状态机、公式或接口。
工程章走 logic 与指南。只有明确请求或确有定量结果小节才追加已有 experiment
--results-analysis；不凭章号对整章运行 --per-chapter。若脚本产生方法类无关候选，
按章型注明不适用，不声称本任务修改了 analyzer 默认分类。

## 评测

追加三个 output 场景：架构/UI清单且证据仅回放、真实失败回退边界、同编号方法/工程对照。
trigger 追加工程论文正例与无论文语境 API README 负例；保留英文/Typst/audit负例。
保存修改后指南下的实际合成响应与逐项评审于 research/output-evidence.md，
记录输入可证事实和未证事实，不用关键字正则代替“未虚构”语义审阅。
