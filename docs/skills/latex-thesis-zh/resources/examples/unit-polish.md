# Example: Unit-by-Unit Polishing and Verification

This example is synthetic. The user asks: “Polish this subsection while preserving citations, numbers, and claim strength.” Read the [unit-polishing protocol](../references/writing/unit-polish-zh.md) first.

## 1. Locate and Read

```bash
uv run python $SKILL_DIR/scripts/polish_unit_zh.py main.tex --plan
uv run python $SKILL_DIR/scripts/polish_unit_zh.py main.tex --plan --unit 1.1.1
```

Use the listed source ranges to read the current subsection and read-only neighbors. Suppose the current subsection is as follows; keep the neighbors out of the revision.

```latex
\subsection{误差比较}
值得注意的是，本研究比较了模型 A 和模型 B 的预测误差。模型 A 的 MAE 为 0.12，模型 B 的 MAE 为 0.15。该结果可能支持模型 A 在当前样本上的误差优势\cite{demo2026}。
```

## 2. Proposed Unit Revision

Run the protocol's pre-rewrite diagnoses on the entry file and filter them to the current line range, then provide the complete revision:

```latex
\subsection{误差比较}
本研究比较了模型 A 和模型 B 的预测误差。模型 A 的 MAE 为 0.12，模型 B 的 MAE 为 0.15。该结果可能支持模型 A 在当前样本上的误差优势\cite{demo2026}。
```

Change notes:

- Empty expressions removed: deleted the opening “值得注意的是”.
- Sentence logic or structure adjusted: none.
- Evidence the author needs to supply: none.

```latex
% POLISH (main.tex:L10-L11) [Severity: Info] [Priority: P3] [LLM]: 单元润色提案
% Changed:       删除段首垫话
% Protected:     标题、MAE、0.12、0.15、\cite{demo2026}、可能、当前样本
% Meaning-Check: NEEDS-LLM
% Risk-Flags:    none
```

## 3. Verify Before Delivery

Save the revision to a temporary file, then run:

```bash
uv run python $SKILL_DIR/scripts/polish_unit_zh.py main.tex --verify --unit 1.1.1 --revised revised.tex
```

The expected result is `PASS-SCRIPT`, with semantic review still required. Actual delivery includes the executed command, exit code, and finding counts; never claim a pass before running it. Changing 0.12 to 0.10 triggers `UP-NUM` and blocks the proposal. Replacing “可能支持” with “证明” produces an `UP-STRENGTH` candidate. Removing the citation key triggers `UP-CITE`. Preserving the existing heading verbatim does not trigger `UP-SCOPE`; an added heading or copied first sentence from read-only context requires correction and another verification run.
