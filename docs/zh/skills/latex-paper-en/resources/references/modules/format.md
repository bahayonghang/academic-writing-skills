# 模块：格式检查

**触发器**：格式、chktex、lint、格式检查

## 命令

```bash
uv run python -B scripts/check_format.py main.tex
uv run python -B scripts/check_format.py main.tex --strict
```

## 细节
原始脚本输出：通过/警告/失败，并分类问题。
技能层响应：将可操作的发现总结为 LaTeX 友好的评审意见。
在迭代检查格式之前确保文档已编译。

