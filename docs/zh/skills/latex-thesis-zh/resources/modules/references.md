# References Module Reference

Purpose: Check figure/table/equation cross-reference integrity across the
multi-file thesis project (\input/\include resolved automatically).

## Checks

| Check                       | Severity      | 说明                                                  |
| --------------------------- | ------------- | ----------------------------------------------------- |
| Undefined reference         | Critical / P0 | `\ref{x}` 没有任何 `\label{x}` 定义（盲审高频扣分点） |
| Unreferenced label          | Minor / P2    | `fig:`/`tab:`/`eq:` 标签从未被正文引用                |
| Missing caption             | Major / P1    | figure/table 环境含 label 但无 `\caption`             |
| Reference before definition | Minor / P2    | 同文件内 `\ref` 出现在 `\label` 之前                  |
| Numbering gap               | Minor / P2    | 数字后缀标签断档（fig:a1、fig:a3 缺 fig:a2）          |

## Command

```bash
uv run python $SKILL_DIR/scripts/check_references.py main.tex
uv run python $SKILL_DIR/scripts/check_references.py main.tex --json
```

支持 `\ref` / `\eqref` / `\autoref` / `\cref` / `\Cref` / `\pageref` /
`\hyperref[]{}`。退出码：存在 Critical（undefined reference）时为 1，否则 0。

## Notes

- 多文件解析自动跟随 `\input{}` / `\include{}`，循环引用安全。
- 注释行中的 label/ref 不计入。
- 跨文件 ordering 检查不做（无意义），仅同文件内检查先引用后定义。
