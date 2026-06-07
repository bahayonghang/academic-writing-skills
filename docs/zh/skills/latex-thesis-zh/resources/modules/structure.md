# 模块：Structure

**触发**：structure、chapter map、thesis structure、结构映射、章节地图、模板检测、completeness、processing order

## 命令

```bash
uv run python -B scripts/map_structure.py thesis.tex
uv run python -B scripts/map_structure.py thesis.tex --json
uv run python -B scripts/map_structure.py thesis.tex --detect-template
uv run python -B scripts/map_structure.py thesis.tex --order
uv run python -B scripts/detect_template.py thesis.tex
```

## 说明

`map_structure.py` 会映射学位论文文件树，并报告：

- 被包含文件及其嵌套层级；
- 识别到的文件类型，例如封面、摘要、章节、附录、参考文献、致谢；
- thuthesis、pkuthss、ustcthesis、fduthesis 和 generic ctexbook 等模板检测结果；
- 结构完整性信号，例如缺少必需的前置/后置部分。

当用户想看论文章节地图、论文骨架或模板感知的总览时，优先使用这个模块。
如果任务重点是段落逻辑、章节递进或跨章节闭合，再在结构信息基础上交给 `logic`。

技能层响应：

1. 按需返回树状结构视图或 JSON 输出。
2. 标出缺失的必要部分和可能的章节顺序问题。
3. 将模板检测与正文改写分开处理。
