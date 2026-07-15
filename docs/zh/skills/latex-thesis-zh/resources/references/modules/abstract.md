# Module: Abstract

**Trigger**: abstract, 摘要, abstract structure, 摘要结构, check abstract, polish abstract, abstract diagnosis, 润色摘要, abstract review

## Commands

```bash
uv run python -B scripts/analyze_abstract.py main.tex                       # thesis 骨架诊断（默认）
uv run python -B scripts/analyze_abstract.py main.tex --degree master       # 硕士字数阈值
uv run python -B scripts/analyze_abstract.py main.tex --bilingual           # + 中英摘要一致性
uv run python -B scripts/analyze_abstract.py main.tex --max-chars 1500      # 覆盖字数上界
uv run python -B scripts/analyze_abstract.py main.tex --model five --lang en --max-words 250
uv run python -B scripts/analyze_abstract.py main.tex --json
```

## Details

**默认 `--model thesis`**：诊断中文学位论文摘要**骨架**（对象定位首句 → 痛点段 → 总起句冒号
收束 → 编号工作段 → 可选收尾段），13 项 T-* 检查见
`../writing/abstract-structure.md` 的「学位论文摘要骨架（thesis 模型）」节。本技能只服务学位
论文，故 thesis 为默认；`--model five` 保留会议论文口径的**五要素模型**（Background/Objective/
Methods/Results/Conclusion）作后备（五要素对博士摘要会系统性误报，如 Results 无数值判 MISSING，
而合规博士摘要常定性收口）。

**字数阈值**对齐 check_spec 的燕山校规常量：`--degree doctor`（默认）900~1200 字、
`--degree master` 500~650 字；`--max-chars` 显式传入时覆盖上界。两处常量一致性由单测锁定。

**中英摘要一致性（`--bilingual`）**：thesis 模式下额外比对英文 Abstract 与中文摘要——
B-ORD（序词对齐）/ B-NUM（数值集合一致，Error）/ B-ENUM（编号条数一致）/ B-LEN（英摘缺失
过短）为 [Script]；B-SEM（逐句语义对应）为 [LLM] lane。**时态/语态不在此实现**，报告尾注
指路 `deai` 模块的英文摘要区域门控时态检测（deai trace 不流入本模块）。

For Chinese thesis writing, also check whether abstract, innovation/contribution claims, and conclusion form a three-way closure. See `../writing/thesis-writing-guide.md`.

thesis 模式逐项输出检查码 + 级别 + 证据引文 + 建议；`--model five` 逐要素输出
`PRESENT` / `VAGUE` / `MISSING`。

Skill-layer response:
1. Format the diagnosis as a structured report with ✅ / ⚠️ / ❌ markers
2. Provide specific revision suggestions for VAGUE or MISSING elements
3. If the user requests polishing, generate a revised abstract with [REVISED: ...] annotations
4. Never fabricate data or add claims not in the original

Thesis-specific closure:

- 摘要：研究问题、方法、结果、意义是否完整。
- 创新点/主要贡献：是否与摘要中的方法和结果一致。
- 总结与展望：是否回应摘要和绪论中的贡献，并给出局限边界。

See also: [abstract-structure.md](../writing/abstract-structure.md) for the 学位论文摘要骨架（thesis 模型）section (T-*/B-* checks) and the legacy five-element model with detection heuristics. 结论章内容检查见 [conclusion.md](conclusion.md)。
