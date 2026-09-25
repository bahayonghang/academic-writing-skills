# 2026-09-22 规划取证与收敛

## 基线与用户决定
产品基线 dev 88bd045；当前七个任务目录为未跟踪规划。没有产品改动。
来源论文HEAD 510ab906，writing目录35文件（34 Markdown+1 JSON），学院材料799行、111项。
源位置沿用gap-analysis，只读核对，不成为产品/CI依赖。
用户确认：保守opt-in；页底MANUAL、歧义数字NEEDS-LLM；程度词和误报豁免也opt-in。
只完善规划，不运行start/finish/archive，不代表实施批准。

## 本仓库核验
| 事实 | 证据 | 规划修订 |
| --- | --- | --- |
| module是提示不是执行 | academic-writing-skills/latex-thesis-zh/scripts/check_spec.py:742 | C5新模板提示携带C2/C3 flags，不宣称自动检查 |
| format路由存在 | academic-writing-skills/latex-thesis-zh/scripts/check_spec.py:169 | 纠正“空路由”，缺的是学院专项 |
| 数字单位正则不含百分号 | academic-writing-skills/latex-thesis-zh/scripts/check_style_zh.py:105 | 不能只改UNIT_NO_SPACE常量；新增学院候选路径 |
| 绝对词裸子串匹配 | academic-writing-skills/latex-thesis-zh/scripts/check_style_zh.py:312 | --degree-wording里做词位豁免，不整句跳过 |
| Bib扫描是BibTeX层 | academic-writing-skills/latex-thesis-zh/scripts/bib_scan.py:160 | 正文cite扫描留check_references |
| 姓名应交样式显示 | academic-writing-skills/latex-thesis-zh/scripts/verify_bib.py:315 | 完整姓名不报格式违规，不改成缩写数据 |
| CF脚本码固定 | tests/contracts/test_claim_forward_contract.py:21 | C6全部文档层，不因能读YAML新增码 |
| style有哈希锁 | tests/skills/latex_thesis_zh/test_polish_unit_zh.py:25 | C1/C2按unit-polish-contract仅更新该脚本实际LF哈希 |
| 摘要/文献阈值存在缓冲 | academic-writing-skills/latex-thesis-zh/scripts/check_spec.py:380；academic-writing-skills/latex-thesis-zh/scripts/check_spec.py:589 | 学院10/92用LLM，不复制旧阈值 |
| 近年占比分母仅有年份条目 | academic-writing-skills/latex-thesis-zh/scripts/check_spec.py:604 | 学院93人工核全部参考文献分母 |
| formula示例有学校优先前提 | academic-writing-skills/latex-thesis-zh/references/formatting/formula-guide.md:3 | 分清AMS推导链与学院源码，不判所有重复等号错误 |

## 外部源材料（路径相对来源论文仓库）
materials/电气工程学院-研究生学位论文格式审查清单-2025.md：
第1/3/10/12/86/89/109项多子句，来源行73–78、99–102、155–158、167–169、
599–600、617–619、742–744。111项第759–765行为开放记录栏，不得自动PASS。
第10/47/66/92项含硕士和博士要求；74/90按博士专项。详细111行见C5 research/checklist-map.md。
第40项337–338行规定空白与平面角；41项346–347行规定千分空，
不是明确指定TeX的~或\,。
第87项604行“页底≤2行，各章结尾除外”，未定义自动PDF版心与行距，用户同意人工。

来源 .trellis/spec/writing/symbols-and-numbers.md 第187–220行区分学校和源码落实；
citations-and-bibliography.md 第34、110–116、156行图内引用豁免是项目决定；
第203、231–232行要求完整姓名和最终渲染核验。
progression-diversity-guide.md 的5/7是论文标定，迁入仅为UNVERIFIED opt-in候选。

## 上一轮审阅的纠偏与完整性
上一轮没有持久化TPR报告，不虚构TPR编号。
14条_example去重为一个清单占位问题；PRD-only不是所有任务的错误，本轮确有新接口和数据路径，
因此补足各子design/implement。父任务原已写明串行，新增的是精确交接/回滚，而非声称原无顺序。
旧“工作树干净”限定为任务创建前历史基线。
C2原改YS条目与C5冻结旧模板冲突已统一为旧模板冻结。
默认回归按每个受影响CLI采集，paragraph_arc单快照不能证明其他入口不变。
引用消歧用源资源全路径；公共学校名称可作规范出处，不能把私有论文专名混入示例。

## 证据边界
来源规范转录可公开，私有论文原句/数字/作者不进测试或产品。
结构校验不证明实现质量，合成测试不证明真实论文、PDF、学校接受或五宿主效果。
这些外部效果与provider评估均UNVERIFIED；未来实施需执行各子门禁并逐项核验公开条款。
