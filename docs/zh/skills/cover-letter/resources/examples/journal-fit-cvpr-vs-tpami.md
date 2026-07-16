# 示例：Journal-Fit CVPR 与 TPAMI

用户请求：
我的投稿信是针对 CVPR 还是应该重新定位到 TPAMI？

推荐模块顺序：

1. 两个场地均为 `journal-fit`；比较判决。

命令：

```bash
uv run python -B $SKILL_DIR/scripts/cover_letter.py --mode journal-fit --letter cover_letter.md --venue cvpr --json
uv run python -B $SKILL_DIR/scripts/cover_letter.py --mode journal-fit --letter cover_letter.md --venue ieee-trans --json
```

预期输出：

- `scope_fit`、`novelty_framing`、`evidence_density`、`format_compliance` 每个场地的每轴高/中/低。
- 每个轴的具体报价级证据。
- 每轴建议可将判决提升一个层次。
- 每个场地的总体结论+关于哪个场地更符合当前字母框架的建议。
