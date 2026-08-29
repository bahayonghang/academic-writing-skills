# 执行计划 (C3)

## 前置研究（激活前）

- [x] P1 C1 已完成：`4b37ddf` / `62f74a0`。
- [x] P2 C2 已完成：`af84e4a` / `401ee53`；可复用稳定 P-ARC contract。
- [x] P3 写 `research/en-density-conversion.md`，锁定 canonical word regex、5000 词等价点、
      1500/10000 词缩放 truth table 和 UNVERIFIED 边界。
- [x] P4 建立受控 EN fixture，覆盖 introduction、related、method 环境/list 与 clean/bad arc。
- [x] P5 在改产品前生成 `research/baseline-sample.tex` 和 `baseline-before.txt`。

## S0 激活与稳定基线

- [x] 校验并激活 C3，加载 Phase 2.1。
- [x] 先把 research baseline 逐字节复制到 `tests/fixtures/paragraph_arc_en/`。

## S1 密度数据与共享计数

- [x] EN YAML 与 DEFAULT 切换 `per_10k_words`，全部 term 值 ×2；写明仅 5000 词基线等价。
- [x] throat-clearing 换算为 2.0/万词、min 1；organization=6.6 借用值标 UNVERIFIED。
- [x] sequence terms 增加 second/next；共享匹配排除 uppercase 与连字符复合词，按锁同步
      EN/Typst/ZH 可执行逻辑，不改 Typst 数据。
- [x] AC1 truth table、AC2 word-count、AC3 sequence boundary tests；更新 alignment relationship。
- [x] G1：验证 5000 词等价和其他长度预期缩放。

## S2 英文段落弧线

- [x] 实现段落/segment/章节所有权与全部硬边界；标题首段参与但标题仍重置邻接。
- [x] 新增 EN terms YAML 与逐字段 fallback。
- [x] 实现 LEAD/CLOSE/LINK/FLAT、N=2 汇总、Info/P3 和结构化输出。
- [x] 接入 `analyze(..., paragraph_arc=False)` 与 CLI `--paragraph-arc`。

## S3 tests and G2

- [x] `test_deai_density.py` 覆盖 AC1–AC3、DEFAULT/YAML 同步、clean-clone 独立。
- [x] `test_paragraph_arc.py` 覆盖 AC4–AC6、AC9–AC10、section ownership、硬边界、run reset。
- [x] 默认基线逐字节测试；所有测试只读稳定 fixture。
- [x] G2 人工读受控 sample findings；结果标 synthetic-only，真实论文精度 UNVERIFIED。

## S4 references/docs/spec

- [x] 新建 `paragraph-arc.md` 与 terms YAML；更新 article architecture、logic、routing、
      tone-threshold 说明。
- [x] 新增/扩展可执行 EN paragraph-arc spec；同步中英文 docs 和 manifest。
- [x] SKILL.md 如需更新只改 `last_updated`（本任务无需触碰 SKILL.md）。

## S5 final gates and closeout

- [x] 聚焦 EN/deai/alignment/paragraph-arc tests。
- [x] 单技能与全量资源同步、双语 contract、docs build、`just ci`、task validate、diff check。
- [x] 独立 Phase 2.2 检查无未修 finding。
- [ ] 只提交 C3 语义范围；随后归档 C3 并单独记录归档提交，不推送。

## 禁止事项

- 不宣称真实 EN 语料标定；不把 synthetic fixture 当 precision/recall 证据。
- 不改变既有 funnel/tri-section/cross-section/motivation-thread/method-narrative 默认行为。
- 不改 Typst 阈值数据，不绕过三副本锁，不改构建依赖。
