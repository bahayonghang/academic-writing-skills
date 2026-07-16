# 模块：摘要

**触发**：摘要、摘要、摘要结构、摘要结构、检查摘要、润色摘要、摘要诊断、润色摘要、摘要评审

## 命令

```bash
uv run python -B scripts/analyze_abstract.py main.tex
uv run python -B scripts/analyze_abstract.py main.tex --lang en --max-words 250
uv run python -B scripts/analyze_abstract.py main.tex --lang zh --max-chars 300
uv run python -B scripts/analyze_abstract.py main.tex --json
```

## 细节

诊断摘要中的五个结构要素：背景、目的、方法、结果、结论。

每个元素的输出：`PRESENT` / `VAGUE` / `MISSING`并附有证据引用和建议。

还根据可配置的限制验证字数 (EN) 或字符数 (ZH)。

技能层响应：
1. 将诊断格式化为带有 ✅ / ⚠️ / ❌ 标记的结构化报告
2. 针对VAGUE或MISSING元素提供具体修改建议
3. 如果用户请求润色，则生成带有 [REVISED: ...] 注释的修订摘要
4. 切勿捏造数据或添加原始数据之外的声明

另请参阅：[abstract-struct.md](../writing/abstract-structure.md) 了解完整的五元素模型和检测启发式。
