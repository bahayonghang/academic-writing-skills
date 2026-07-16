# 示例：编译和参考书目

用户请求：
编译我的 IEEE 论文，然后告诉我为什么 `main.tex` 中的两个引用未得到解决。

推荐模块顺序：
1. `compile`
2. `bibliography`

命令：
```bash
uv run python -B $SKILL_DIR/scripts/compile.py main.tex
uv run python -B $SKILL_DIR/scripts/verify_bib.py references.bib --tex main.tex
```

预期输出：
- 如果编译中断，则使用确切的失败命令构建结果。
- `% COMPILE ...`或者`% BIBLIOGRAPHY ...`指向未解决的引用或缺少 BibTeX 键的注释。
