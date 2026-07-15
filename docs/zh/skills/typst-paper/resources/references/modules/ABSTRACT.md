# 模块：摘要

**触发**：摘要、摘要、摘要结构、摘要结构、检查摘要、润色摘要、摘要诊断、润色摘要、摘要评审

## 命令

```bash
uv run python -B $SKILL_DIR/scripts/analyze_abstract.py main.typ
uv run python -B $SKILL_DIR/scripts/analyze_abstract.py main.typ --lang en --max-words 250
uv run python -B $SKILL_DIR/scripts/analyze_abstract.py main.typ --lang zh --max-chars 300
uv run python -B $SKILL_DIR/scripts/analyze_abstract.py main.typ --json
```

## 细节

诊断摘要中的五个结构要素：背景、目的、方法、结果、结论。

每个元素的输出：`PRESENT` / `VAGUE` / `MISSING`并附有证据引用和建议。

还验证字数（EN、`--max-words`) 或字符数 (ZH,`--max-chars`）针对配置的限制。语言是自动检测的，除非`--lang {en,zh,auto}`被给出。摘要提取支持`#abstract[..]`, `#show: ieee.with(abstract: [..])`，和一个`= Abstract` / `= 摘要`标题。

技能层响应：

1. 将诊断格式化为带有 ✅ / ⚠️ / ❌ 标记的结构化报告
2. 针对VAGUE或MISSING元素提供具体修改建议
3. 如果用户请求润色，则生成带有 [REVISED: ...] 注释的修订摘要
4. 切勿捏造数据或添加原始数据之外的声明

另请参阅：[ABSTRACT_STRUCTURE.md](../ABSTRACT_STRUCTURE.md) 了解完整的五元素模型和检测启发式。
