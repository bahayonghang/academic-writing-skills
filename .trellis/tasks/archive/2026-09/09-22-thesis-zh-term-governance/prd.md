# C1：项目术语治理、缩写体例与程度词

## Goal / Dependencies
承担父任务的术语需求与通用约束，执行序列 C1；无前置子。C2 在本子交付后接手 check_style_zh.py。
规则仅定位候选，不选择同义词、不自动替换。

## Confirmed Facts
- academic-writing-skills/latex-thesis-zh/scripts/check_consistency.py:106 只加载 zh/en 分组；
  academic-writing-skills/latex-thesis-zh/scripts/check_consistency.py:135 已有装配顺序与源映射。
- academic-writing-skills/latex-thesis-zh/scripts/check_style_zh.py:312 对“绝对”裸子串命中，
  不区分“绝对误差”；旧默认保持，新模式处理该问题。
- tests/skills/latex_thesis_zh/test_polish_unit_zh.py:25 冻结 style 哈希；
  .trellis/spec/academic-writing-skills/unit-polish-contract.md 允许其他任务变更后更新对应哈希。
- 用户2026-09-22确认：新增程度词与合法搭配豁免均 opt-in，旧输出不因误报修复改变。

## Requirements
- R1: 显式 --governance --custom-terms JSON 加载 banned/locked/exempt；zh/en 仍由原同义组路径读取。
  不设置新文件版本或迁移层；未启用治理时不消费新增字段。
- R2: 明确 --abbreviation-style 检查合格首现后的二次括注/并列，以及明确全称括注的 Title Case 候选。
  合格首现、数学括注、缩略词表和不明边界不误报；不自动认定所有英文名必须小写。
- R3: --degree-wording 下新增“极易/极低/完全忽略/高度贴合”候选，豁免“绝对误差/绝对值/
  绝对温度/绝对湿度/绝对压力/绝对坐标”；只豁免对应词位，句中其他绝对化词仍检查。
- R4: 公开格式、合成例、豁免与局限写入 consistency/style 文档、example、路由、相应 spec；
  同步双语镜像及父设计列明的公共入口。
- R5: 无新开关的旧 JSON/--terms/--abbreviations/style 输出保持；只更新 style 对应冻结哈希；
  新输入错误显式报错，source 定位、报告格式及候选语义有回归测试。

## Acceptance Criteria
- [ ] AC1 (R1): banned 输出全部候选和 slot、locked 输出规范名；固定保护区/自定义环境无治理命中；
  空配置零新候选，损坏配置非零退出且不输出已通过结论。
- [ ] AC2 (R2): 二次括注、Title Case、并列各命中；完整首现、符号契约、数学括注、缩略词表四类零命中；
  无合格首现不擅自触发后续 XOR，跨 include 顺序由入口装配决定。
- [ ] AC3 (R3): 新模式“绝对误差为0.3”无 E-ABSOLUTE，“极易发散”有候选；
  “绝对误差很小，结论绝对可靠”仍提示后一个词；旧模式输出相同；不输出替换整句。
- [ ] AC4 (R4): 格式/例子/限制/路由同步且无论文具体词表；复制安装仅依赖 skill 内资源；
  新 term-governance-contract 与公开语义一致。
- [ ] AC5 (R5): 正反例、源位置、CLI错误和旧输出测试通过；style哈希仅按实际新内容更新；
  父 design §4 全部门禁通过，其余冻结文件不变。

## Out of Scope
不改旧同义漂移逻辑、FORBIDDEN_TERMS、polish治理行为，不为每个论文建立词表；
不把数学与引文键作为治理文本，不改 parsers/loader/deai。
旧需求编号映射：R1.1→R1；R1.2→R1；R1.3→R2；R1.4→R3；R1.5/R1.7→R4；R1.6→R5。
