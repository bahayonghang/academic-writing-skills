# 示例：逐单元润色与核对

以下为合成示例。用户请求：“把这一小节语言润色一下，保持引用、数字和结论强度。”先读 [单元润色协议](../references/writing/unit-polish-zh.md)。

## 1. 定位与读取

```bash
uv run python $SKILL_DIR/scripts/polish_unit_zh.py main.tex --plan
uv run python $SKILL_DIR/scripts/polish_unit_zh.py main.tex --plan --unit 1.1.1
```

按清单源文件行区间读取当前小节与只读邻域。假设当前小节原文如下；邻域不放进稿件。

```latex
\subsection{误差比较}
值得注意的是，本研究比较了模型 A 和模型 B 的预测误差。模型 A 的 MAE 为 0.12，模型 B 的 MAE 为 0.15。该结果可能支持模型 A 在当前样本上的误差优势\cite{demo2026}。
```

## 2. 单元润色提案

先在入口文件运行协议中的单元前诊断并筛选当前行区间，再交付完整润色稿：

```latex
\subsection{误差比较}
本研究比较了模型 A 和模型 B 的预测误差。模型 A 的 MAE 为 0.12，模型 B 的 MAE 为 0.15。该结果可能支持模型 A 在当前样本上的误差优势\cite{demo2026}。
```

修改说明：

- 删除了哪些无信息表达：删除段首“值得注意的是”。
- 调整了哪些句子逻辑或结构：无。
- 哪些位置缺证据需作者补充：无。

```latex
% POLISH (main.tex:L10-L11) [Severity: Info] [Priority: P3] [LLM]: 单元润色提案
% Changed:       删除段首垫话
% Protected:     标题、MAE、0.12、0.15、\cite{demo2026}、可能、当前样本
% Meaning-Check: NEEDS-LLM
% Risk-Flags:    none
```

## 3. 核对后交付

将润色稿保存为临时文件，再运行：

```bash
uv run python $SKILL_DIR/scripts/polish_unit_zh.py main.tex --verify --unit 1.1.1 --revised revised.tex
```

预期为 `PASS-SCRIPT`，仍需语义核对。实际交付附运行命令、退出码与命中数，未运行不得声称通过。把 0.12 改成 0.10 会触发 `UP-NUM` 并阻塞；把“可能支持”改成“证明”会产生 `UP-STRENGTH` 候选；删除引用键会触发 `UP-CITE`。原有标题原样保留不触发 `UP-SCOPE`，新增标题或复制只读邻域首句则需修正后重新核对。
