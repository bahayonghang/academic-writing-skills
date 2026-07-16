# 模块：伪代码审查

**触发器**：伪代码、α代码、算法块、algorithmicx、algpseudocodex、algorithm2e、算法 1、要求/确保

## 命令

```bash
uv run python -B scripts/check_pseudocode.py main.tex --venue ieee
uv run python -B scripts/check_pseudocode.py main.tex --venue ieee --json
```

## IEEE 安全默认值

- 将 IEEE 伪代码视为类似图形的对象，而不是专用的浮动 `algorithm` 环境。
- 更喜欢`figure` + `algorithmicx` / `algpseudocodex`用于 IEEE 提交。
- 不要默认为`algorithm.sty` / `algorithm2e`IEEE 论文的浮动环境。
- 使用直接标题，而不是文章主导的标题，例如 `The proposed algorithm...`。
- 更喜欢明确的输入/输出标记，例如`\Require`和`\Ensure`.
- 保持内嵌注释简短。将长解释移回到正文中，或者当不可避免地需要较长的附注时使用 `\LComment`。
- 建议行号是为了方便审查，但它们并不被视为硬性 IEEE 要求。

## 该模块检查什么

- IEEE 硬违规：浮动`algorithm` / `algorithm2e`用法
- 伪代码周围缺少图形标题或标签
- 伪代码图之后出现的第一个文本引用
- 开头为的字幕`A`, `An`， 或者`The`
- 缺少显式输入/输出标记
- 长内嵌注释或散文长度的算法步骤
- 行号缺失（仅供参考）

## 产出政策

- 与建议分开报告硬约束。
- 除非用户明确要求进行源代码编辑，否则不要自动重写伪代码块。
- 在建议修复时，请解释它是否：
  - IEEE 硬约束
  - IEEE 安全默认值
  - 可读性推荐
