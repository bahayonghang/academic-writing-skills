# 示例：生成 Nature 投稿信

用户请求：
从我的 LaTeX 论文 `main.tex` 生成一封 Nature 投稿投稿信。

推荐模块顺序：

1. `generate`（默认对齐检查+提交前集成）

命令：

```bash
uv run python -B $SKILL_DIR/scripts/cover_letter.py --mode generate --manuscript main.tex --journal nature --json
# After saving the synthesized prose to draft.md, verify it:
uv run python -B $SKILL_DIR/scripts/cover_letter.py --mode align-check --letter draft.md --manuscript main.tex --json
uv run python -B $SKILL_DIR/scripts/cover_letter.py --mode presubmission --letter draft.md --journal nature --json
```

预期输出：

- `generate` 有效负载携带事实 blob（标题、摘要、作者、贡献、标题数字）和确定性草稿支架。
- 使用 `templates/nature.md` 合成投稿信散文（350 字上限，范式转换框架）。
- `% ALIGNCHECK` 阻止草稿中出现任何未追溯到论文稿件的权利要求。
- `% PRESUBMISSION` 阻止列表缺少必需的声明（原创性、双重提交、利益冲突、人工智能使用披露；数据可用性对于 Nature 是可选的，并通过提交系统传送）。
