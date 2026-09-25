# C5 设计

## 1. Files
skill=academic-writing-skills/latex-thesis-zh。
新增templates/yanshan-ee-2025.md；改scripts/check_spec.py、references/modules/spec-check.md、
routing-rules.md和SKILL。测试扩展tests/skills/latex_thesis_zh/test_check_spec.py、
test_latex_thesis_zh_coverage.py及tests/contracts/test_spec_checklists.py（只增加确有价值的覆盖，保留双向锁）。
模板源条款矩阵作为合成/公开规范fixture随测试落在tests/fixtures/college-checklist/，
不使CI依赖外部论文目录。公开规则资料可转录，私有论文批注不转录。
改.trellis/spec/academic-writing-skills/spec-checklist-convention.md记录学院并存/完整项覆盖规则；
公共资源面按父design§3。旧templates四文件禁止编辑。

## 2. Full-item mapping (AC1–AC2)
research/checklist-map.md给出111项来源行号、全部规范子句、学位、检查方式和残余责任。
实现时从此映射转写模板，不从历史YS编号推导新YSE编号。
复合条款的说明必须逐子句核读；测试锁ID/条数/方法/学位只能证明结构，另做逐行人工对照记录。
单条scope不能表达混合博士/硕士规则时用通用，在正文明确degree区别。
47/66/92和10均通用；74/90按来源博士专项，见矩阵。
第45项采用module:references并明确源码与渲染覆盖限制；现有cite_in_heading可辅助人工，
不将其有限命令识别冒充全部标题引用覆盖。

没有学院阈值表：10摘要长度还含第三人称且非对称上下限，92是实际列出文献数硬下限，
93是全部参考文献作为分母；现有检查只提供辅助观察，不能以旧阈值作为学院PASS。
保留原文数值和来源，不在模板中伪造区间、豁免或学校容忍度。
新模板全部状态来自现有模型，MODULE/MANUAL/NEEDS-LLM必须在总评明确仍未验收。

## 3. Third-person candidates (AC3)
新增check_third_person(ctx)注册CHECKERS["third_person"]，且仅YSE-088引用。
适用范围为全文可见作者叙述，排除前导区、致谢、文献数据、代码、数学和键载荷；
致谢必须由标题/标准环境确定起止，不能因上一行含致谢二字屏蔽后文全部。
复用parser/assemble，不新增抽象visitor或词法平台。
定位“我们”“笔者”、含“我”的词位（已排除常见非人称复合词）与明确“我认为/我提出”等短语；
不使用裸“我”子串匹配，排除我国/我校等普通词和明确引述他人话语。
存在命中→NEEDS-LLM并列位置/短片段及人工核读说明；无命中→NEEDS-LLM说明未发现所列候选，
不声称第三人称全文成立。这是有意保守的语义checker，不是永远PASS。
其余学校清单不引用该checker，BANNED_NON_YS_METHODS补隔离断言。

## 4. MODULE hint routing (AC4)
当前MODULE_COMMANDS保持不变。在run_checklist生成学院模板module提示时使用局部函数，
仅template_id=="yanshan-ee-2025"分支：
expression / format / tables → 对应脚本 --school yanshan-ee-2025；
references → check_references --school yanshan-ee-2025 --author-cite --repeat-cite；
bibliography → verify_bib references.bib --standard gb7714 --college-details；
consistency → check_consistency main.tex --abbreviation-style（不得无配置暗启governance）。
commands是人工后续调用提示，不自动执行；bibliography命令占位输入需用户换实际bib路径。
其他模块保留已有提示；只有新模板实际引用的模块才加相关提示，避免死配置。
reference/doc说明author-cite是作者写作约定，不冒充学院第42条原文。
对于多子句的MODULE行，同一行检查项文字明确“脚本仅辅助，余项人工”，不新加表列/状态。

## 5. Evidence and rollback (AC5)
doctor/master固定--year 2026调用fixture，比较111个ID/scope/method/status与来源预期，
不是仅断言status非空；测试原始模板未改和旧输出相同。
本轮第87始终manual，无--pdf参数、无lazy pymupdf路径。
schema/注册双向锁通过只证明接线；111项人工对照表和PDF未核实单独报告。
新增template/third_person/学院命令分支可作为一子差异回退，不影响C2/C3独立CLI。
