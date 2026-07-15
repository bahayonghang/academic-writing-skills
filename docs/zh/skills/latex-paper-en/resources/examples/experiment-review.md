# 示例：实验回顾

用户请求：
检查实验部分是否存在弱基线、缺失的消融和不受支持的主张，但不要重写论文文本。

推荐模块顺序：
1. `experiment`

命令：
```bash
uv run python -B $SKILL_DIR/scripts/analyze_experiment.py main.tex --section experiments
```

预期输出：
- 审稿人风格的 `% EXPERIMENT ...` 结果与混凝土线相关。
- 关于通用基线、缺失指标、缺失消融/统计证据或夸大其词的警告。
