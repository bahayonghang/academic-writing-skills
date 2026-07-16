# 示例：优化和对齐检查投稿信

用户请求：
完善我的草案 `cover_letter.md` 以提交 IEEE TPAMI，并验证它相对于 `main.tex` 没有过度声明。

推荐模块顺序：

1. `optimize`（默认集成运行对齐检查+预提交）

命令：

```bash
uv run python -B $SKILL_DIR/scripts/cover_letter.py --mode optimize --letter cover_letter.md --manuscript main.tex --journal ieee-trans --json
```

预期输出：

- `% PRESUBMISSION` 调查结果：声明缺失、长度违规、禁止短语命中。
- `% ALIGNCHECK` 结果：`claim_strength`、`allowed_wording` 建议和 `manuscript_section_anchor` 指针的声明准确性问题。
- LaTeX 注释格式的节级差异建议：`% OPTIMIZE (Line N) [Severity: Major] [Priority: P1]: ...`
- 对提议的重写重新运行 `--mode align-check`，以验证没有引入新的不受支持的声明。
