# References Module Reference

Purpose: Check figure/table/equation cross-reference integrity across the
multi-file thesis project (\input/\include resolved automatically).

## Checks

| Check                       | Severity      | 说明                                                  |
| --------------------------- | ------------- | ----------------------------------------------------- |
| Undefined reference         | Critical / P0 | `\ref{x}` 没有任何 `\label{x}` 定义（盲审高频扣分点） |
| Unreferenced label          | Minor / P2    | `fig:`/`tab:`/`eq:` 标签从未被正文引用                |
| Missing caption             | Major / P1    | figure/table 环境含 label 但无 `\caption` / `\bicaption` |
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
- 注释行中的 label/ref/caption 不计入；`\fakecaption`、`\captionsetup` 等相似命令不算题注。
- 题注存在性识别支持 `\caption` / `\bicaption` 的可选短标题和命令后的空白、换行；这里只检查真实题注命令是否存在，不验证题注内容或模板排版。
- 跨文件 ordering 检查不做（无意义），仅同文件内检查先引用后定义。

题注措辞、续图、子图和编译页验收见 [caption-guide.md](../formatting/caption-guide.md)。

`--school yanshan-ee-2025` 只为非表浮动体（`figure` 及其同类）的中文题注末标点增加 `CAP-PUNCT`。表浮动体不在本脚本重复报告。可选短题注、`\bicaption` 第二参数、英文句点，以及代码、数学、引用键中的标点都不算。认不出中文主参数时留人工。本模式不增加引文位置、页码或文献著录规则。默认和 `--school generic` 不启用。候选为 `[Script]`、Info/P3、`Meaning-Check: NEEDS-LLM`。

## 可选引文位置与重复页码

`--author-cite` 与 `--repeat-cite` 相互独立，也可与 `--school` 组合。不传这两个开关时不建立新扫描，原输出不变。

`--author-cite` 只报告同一完整句内、明确作者短语之后的滞后引用。支持 `\cite`、`\citep`、`\citet`、`\parencite`、`\textcite`、`\autocite`、`\footcite` 及其星号。命令与参数之间可以有空白、注释和 0 到 2 个平衡可选参数。`\textcite` 与 `\citet` 不另报作者位置，因为渲染出的作者不在源码里。文献和已有研究不是作者主语。紧跟作者短语的引用不报告。不确定的中文姓名只给 `RC-AUTHOR-UNCERTAIN` 或覆盖说明，并写明作者主语不确定。不拆开 ASCII 点号缩写，也不跨不完整句或段落猜测。报告文件、行、短片段和引用键，不改写句子或键。

`--repeat-cite` 对每个受支持命令里的每个键计一次，同一命令中的重复键只计一次。一个可选参数是 postnote；两个可选参数时，第一个是 prenote，第二个是 postnote；空白 postnote 为空。题注里的可见引用计入，没有学校豁免，也没有单独的图豁免。参考文献数据、注释、宏定义、`verbatim` 和 `\nocite` 不计。同一键至少两次且至少一次缺少 postnote 时给出 `RC-REPEATPAGE`。两次都有字面页码，或只有一次，不报告。多键共享 postnote 时即使非空也只给一条 `NEEDS-LLM`，不能证明每个键的页码。自然语言 postnote 不是页码证据，不据此通过学院规则，也不发明页码。字面页码包括整数、罗马数字和明确页段；这仍不证明该页支持当前句。`\cites` 及其他多重命令、自定义宏传键和未展开参数未覆盖，该模式会说明覆盖不足。

候选均为 `[Script]`、Info/P3、`Meaning-Check: NEEDS-LLM`。与 `--school yanshan-ee-2025` 同时使用时，中文题注末标点和本模式的候选都保留，同一题注的 `CAP-PUNCT` 不重复报告。
