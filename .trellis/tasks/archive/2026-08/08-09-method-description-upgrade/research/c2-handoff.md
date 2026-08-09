# C2 交接：EN/Typst 方法节检查与参考

> 这是已实现接口的交接快照；M-* 判据仍以父任务 `design.md` §2 为唯一权威。

## Audit invocation

```text
analyze_logic.py main.tex --section methods
analyze_logic.py main.typ --section methods
```

两种调用只运行方法节 M-* 分支；无 `--section` 时沿用既有全文检查。C3 必须保留原
`--cross-section` 调用，并把上述调用作为第二个 logic task。

## Output contract

- Finding 头行含 `METHOD-NARRATIVE`、severity 与 priority；续行依次使用 `Current`、
  `Suggested`、`Rationale`、`Meaning-Check: NEEDS-LLM`。
- LaTeX 注释前缀为 `%`，Typst 为 `//`。
- `M-EDGETABLE` 位于输出末尾并带 `[LLM] 待填写`，属于骨架输出，不是 finding。

## Shared runtime surface

- 结构常量：`MN_HEADING_RUN=3`、`MN_HEADING_HITS=2`、`MN_EQUATION_LOOKAHEAD=3`。
- EN/Typst 公开正则：`MN_ANNOUNCE_RE`、`MN_SEQ_OPEN_RE`、`MN_CAUSE_EXEMPT_RE`、
  `MN_EQ_GLOSS_RE`；源串由 `tests/contracts/test_method_narrative_alignment.py` 锁定。
- `TRANSITIONS["sequence"]` 是顺序词运行时单一来源；未扩展 `example` 类。
- Typst 公式只检查带 `<label>` 的块公式；支持 delimiter-only 与内容位于 delimiter 行的
  多行形式，并屏蔽 `@eq:where` / `<eq:where>` 等受保护锚点。

## Validation evidence

- 方法/契约专项：41 passed；最终 `just ci`：1445 passed。
- Ruff 通过；Pyright 0 errors；全量资源检查 256 entries；`just doc-build` 通过。
- 检查代理确认原 `if not section` 分支不变、EN/Typst 公开 MN_ 表面一致、接口表不计 finding、
  双语页面与 manifest 一致。

## Remaining evidence

真实论文语料上的启发式查准率仍未验证；当前证据仅覆盖合成病例、合规例和合法标题负例。
