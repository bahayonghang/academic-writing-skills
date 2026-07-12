# Module: Conclusion

**Trigger**: 结论, 总结与展望, 结论与展望, 展望, 结论章, conclusion, 结论检查, conclusion check

## Commands

```bash
uv run python -B scripts/analyze_conclusion.py main.tex
uv run python -B scripts/analyze_conclusion.py main.tex --json
```

多文件工程传入口 `main.tex`，脚本自动 `\input`/`\include` 装配并定位结论章
（结论/结论与展望/总结与展望）；结论↔中文摘要比对复用已抽取的摘要文本。

## Details

对结论章做**章内内容结构诊断 + 结论↔摘要比对**，13 项 CC-* 检查（详见
`../writing/conclusion-guide-zh.md` 的 checker 映射表与分级说明）：

- **三段式（CC-TRIAD）**：总结主体 + 创新表述 + 展望三要素齐全；缺展望/总结 → Error，
  缺创新表述 → Warning。
- **开篇承上（CC-OPEN）**、**编号贡献（CC-ENUM）**、**贡献骨架（CC-SKELETON）**：开篇序词
  串研究链、贡献 (1)(2)(3) 编号 3~4 条、每条"针对…提出…表明…"骨架。
- **展望（CC-OUTLOOK-EMPTY/TRANS/COUNT）**：空话黑名单 + 局限承接过渡句 + 条数 2~3。
- **结论 ≠ 摘要（CC-VERBATIM）**：difflib 逐句比对，逐字重复占比 ≥30% → Warning。
- **数值一致（CC-QUANT）**：结论数值须能在正文找到；缺失出 NEEDS-LLM 软提示。
- **禁忌（CC-NO-FIG / CC-NEW-CONCEPT）**：结论不新插图表（Error）、不引新概念（[LLM]）。
- **风格 Info（CC-RATIO / CC-SUBSEC）**：总结:展望篇幅比、子节号/章编号风格只提示不判对错。

### Lane 区分

- `[Script]`：CC-TRIAD/OPEN/ENUM/OUTLOOK-*/VERBATIM/QUANT/NO-FIG/RATIO/SUBSEC 由脚本判定，
  输出 `% CONCLUSION (源文件:L##) [Severity] [Priority] [Script]: CC-码 说明`。
- `[LLM]`：CC-SKELETON（贡献骨架语义完整性）、CC-NEW-CONCEPT（新概念识别）走 LLM lane，
  脚本只给提示词/粗筛计数，由 agent 判读。

### 与其他模块的边界（勿重复报告）

- **`\cite`、字数上限（≤2000）、模糊措辞** → 走 `spec-check`（`check_spec.py`），本脚本
  报告尾注指路，不重复检查结论格式硬规则。
- **过度声明**（"首次/彻底解决/全面超越"）→ 走 `../writing/over-claim-guard.md` 流程。
- **英文摘要时态/AI 腔** → 走 `deai` 模块。

Skill-layer response:

1. 以 `% CONCLUSION (L##) [Severity] [Priority]` 格式返回问题，"检查结果"与"建议改写"分开；
2. 对 Error（缺展望/总结、结论插图表）优先给出结构性修复建议；
3. 对 CC-OUTLOOK-EMPTY 空话项，给出具体技术方向的改写示例；
4. Never fabricate results or add contributions not in the original text；
   `\cite`/`\ref`/`\label`/数学环境默认不动。

See also: [../writing/conclusion-guide-zh.md](../writing/conclusion-guide-zh.md) 结论章写作专章指南
（结构模板 + 正反例 + checker 映射表）。
