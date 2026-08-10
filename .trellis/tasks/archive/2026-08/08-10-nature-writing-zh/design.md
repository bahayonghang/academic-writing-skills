# design — 08-10-nature-writing-zh

## 边界

- 脚本改动仅限 `latex-thesis-zh/scripts/analyze_abstract.py` 的 `_run_bilingual()` 一处追加;该文件 2026-06 已退出 en+typst 哈希组,独立可改。
- 文档改动:conclusion-guide-zh.md、results-analysis-guide-zh.md(视核对结果)、abstract-structure.md、docs/ 双语页面。
- 不碰 deai 对齐锁、CC-* 既有判定、tex_loader、check_style_zh。

## 1. D-ZH-1:B-NAT 提示项

实现模式 = 现有 B-SEM(analyze_abstract.py `_run_bilingual` 末尾):

```python
# B-NAT nature-writing N3 — journal-style abstract diagnostics are an LLM-lane task.
checks.append(
    self._finding(
        "B-NAT", "Info", "[LLM]", flagged=False,
        message="期刊式摘要修辞候选提示(需 LLM 复核,非判定):(1) 英文摘要开头即 "
        "'Here, we / In this paper, we' 且前面没有上下文句,可能缺少领域背景;"
        "(2) 末句为宽泛前景承诺且无范围限定,可能需要收束范围;"
        "(3) 全文无数字、比较或具体测试,可能缺乏落地感",
        ref="nature-writing N3",
    )
)
```

- 仅在 `english_found` 为真时追加(无英文摘要不提示)。
- ID 冲突预检:`grep -n "B-NAT" scripts/ references/ tests/`。
- 文案与 EN 侧 article-architecture.md N3 节一致(父级共享契约)。

测试:`tests/skills/` 对应 analyze_abstract 测试文件加两条——含英文摘要 fixture 输出含 B-NAT
且 severity=Info、source=[LLM];无英文摘要 fixture 不含 B-NAT。fixture 复用既有 bilingual 用例。

文档:abstract-structure.md B-* 检查项表加一行(标注 [LLM]、ref nature-writing N3)。

## 2. D-ZH-2:conclusion-guide-zh.md 新节

插入位置:既有局限相关小节之后(实现时按文档现有目录序定)。内容四要素:

1. 两类定义表:范围局限(数据范围/假设/部署场景,设定内有竞争力)vs 技术缺陷(关键指标落后强基线/不可接受权衡)
2. 组织顺序:局限段**优先围绕**范围边界组织
3. 红线段:技术缺陷类不利结果必须如实陈述,本节不构成弱化或省略依据;链接 over-claim-guard.md
4. 归属声明一行(nature-writing conclusion.md N17,社区归纳启发式)

不加 CC-* 项;analyze_conclusion.py 零改动。

## 3. D-ZH-3:核对流程

1. 通读 results-analysis-guide-zh.md 全文,定位是否已有"结果章小节叙事顺序 / claim-first 开头"等价指导
2. 已有 → verification.md 落档锚点,结束
3. 缺失 → 在 §七之前或之后加「结果叙事顺序(与证据强度分级的区别)」小节:六层顺序中文化 + claim-first 开头中文模式("为验证X,本节…")+ 显式声明"本节管叙事顺序,§七管证据强度,互不替代" + 交叉引用
4. 判定标准:若既有指南已按"图表事实→…→组件贡献"隐含顺序覆盖,视为已覆盖,勿加节

## 4. 双语资源契约

同 EN 任务 design §5;单项校验 `--skill latex-thesis-zh`。**前置:EN 任务已合入**(manifest 串行)。

## 风险与回退

- 风险:analyze_abstract.py 46K 大文件,追加位置错误影响 JSON schema → 只在 `_run_bilingual` checks 列表追加,跑既有 bilingual 测试回归。
- 风险:文档表格被格式化 hook 重排 → 提交前跑契约测试。
- 回退:单提交 revert;manifest 重建。

## 验证命令

```bash
uv run --extra dev python -m pytest tests/skills/ tests/contracts/ -q -k "abstract or bilingual or resources"
PYTHONIOENCODING=utf-8 uv run python -B academic-writing-skills/latex-thesis-zh/scripts/analyze_abstract.py <fixture> --bilingual --json
uv run python docs/scripts/check_resource_sync.py --skill latex-thesis-zh
just ci
just doc-build
git diff --stat -- 'academic-writing-skills/latex-thesis-zh/scripts/' | grep -v analyze_abstract   # 应为空
```
