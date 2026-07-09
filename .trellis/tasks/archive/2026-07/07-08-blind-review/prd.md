# 盲审匿名化检查与盲审版tex生成

## Goal

为 latex-thesis-zh 新增 `blind-review` 模块：检查学位论文中的个人信息泄露点（盲审隐匿要求），
并**生成盲审版本 tex 副本**（原文件一字不动），把用户提供的燕山大学盲审通知规则逐字落进
`templates/yanshan.md` 与模块参考文档。

## Requirements

1. **规则集（核心，用户提供的校方通知原文，逐字保真）**：
   - R1 隐去作者及导师姓名、致谢等；
   - R2 "攻读学位期间取得的成果"部分，删除姓名、成果名称和期刊页码，只保留本人署名次序和
     期刊名称、年份。如：`[1]第一作者，机械工程学报，2024`。
   - 扩展隐匿点（R3，常见惯例，须标注"以学校盲审通知为准"，不与 R1/R2 混淆）：
     原创性声明/授权说明签名、封面与题名页个人字段、英文题名页 By/Supervisor 行、
     基金项目编号、正文中自指身份的表述（如"作者在×××课题组"）。
2. **脚本 `scripts/blind_review.py`**：
   - `--check`：定位泄露点并输出 findings（文件:行号、规则编号 R1/R2/R3、severity、证据）；
     可选 `--author 姓名 --supervisor 姓名` 时全文扫描该姓名字符串（不提供时跳过并提示）。
   - `--generate [--suffix _blind] [--dry-run]`：生成盲审副本：
     - 只创建新文件（入口 `main_blind.tex` + 受影响的被 include 文件的 `_blind` 副本，
       入口中对应 `\input`/`\include` 引用同步改指副本），**原文件字节不变**；
     - 机械可安全处理项：作者/导师字段值 → `□□□`；致谢内容 → "（盲审版本，致谢内容略）"；
     - 成果条目（R2）**不做自动改写**：在副本条目上方插入
       `% TODO-BLIND(R2): 改写为 [n] 署名次序，期刊名称，年份` 注释并在报告中列出，
       由 LLM 按模块文档给出 diff 建议、用户确认后落入副本（防止脚本误删署名次序等事实）。
   - 红线：不触碰 `\cite`/`\ref`/`\label`/数学环境；不改变成果条目的署名次序事实。
3. **`references/modules/blind-review.md`**：规则集全文（R1/R2 逐字 + R3 标注来源性质）、
   工作流（check → generate → LLM 改写成果条目 → 用户确认 → 复查）、R2 改写示例
   （改写前后对照）、输出契约（`[Script]`/`[LLM]` 标注）。
4. **`templates/yanshan.md`**：填充 `## 盲审` 节（R1/R2 原文 + 示例 + 指向 blind-review 模块）。
5. **SKILL.md**：router 增 `blind-review` 行、路由规则（触发词：盲审/匿名/隐名/送审版本/
   外审版本）、Example 一条；trigger evals 同步加正例。
6. **测试**：`tests/skills/latex_thesis_zh/test_blind_review.py`（importlib 加载 + 守卫），
   fixture 预埋致谢章、成果章（含姓名/成果名/页码）、`\author`/导师字段。

## Acceptance Criteria

- [ ] fixture 上 `--check` 检出：作者字段、导师字段、非空致谢、成果条目页码 pattern、
      （提供 --author 时）正文姓名出现处；各带正确 文件:行号。
- [ ] `--generate` 后：原文件内容哈希不变；`main_blind.tex` 存在且可被 tex_loader 组装；
      副本中作者/导师字段为 `□□□`、致谢为占位文本、成果条目带 TODO-BLIND 注释；
      `\cite`/`\ref`/`\label` 与数学环境在副本中与原文逐字一致。
- [ ] `--dry-run` 只输出计划不写任何文件。
- [ ] yanshan.md 盲审节收录 R1/R2 用户原文（含 `[1]第一作者，机械工程学报，2024` 示例），
      R3 明确标注"常见惯例，以学校通知为准"。
- [ ] SKILL.md 契约测试 + trigger evals + `just ci` 全绿；`version` 不动。

## Constraints

- 在 07-08-spec-final-check 完成后执行（共享 yanshan.md / SKILL.md，避免冲突）。
- 生成逻辑对未识别的模板字段（非 thuthesis/pkuthss/generic 常见宏）宁可漏改并报告
  NEEDS-LLM，也不做启发式大面积替换。
