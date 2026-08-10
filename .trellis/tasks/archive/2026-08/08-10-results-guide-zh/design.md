# Design — 子任务 1（guide 与文档联动）

> 薄设计：判据与泛化规则唯一权威 = 父 `08-09-results-analysis-zh/design.md`（§2 泛化闸门
> 与证据分级映射、§3.3 R-*↔RA-* 映射、§7 效果证据口径）。本文件只记录子任务范围内的
> 落地要点，不复述父判据。

## 文件级要点

1. **guide 小节顺序**即父 prd R1 十一小节序；每节判据出处标注（spec §号或外部来源 #号，
   来源表在父 research/best-practices-web.md）。
2. **互链格式**遵循 `method-narrative-contract.md` 对 guide 互链的既有约定（Step 0 核对；
   若该契约未约束互链格式，沿用 method-description-guide-zh.md 的相对链接写法）。
3. **experiment.md 追加节**放在 `--per-chapter` 节之后，格式对齐既有 E-* 表
   （Check/Rule/Severity 三列）；表后一行注明"全部为启发式线索，判据与词表见 guide"。
4. **翻译顺序**：先锁中文源，再产 en 页（完整译文，保留标题层级/代码块/表格形状/链接
   目标双语同步），最后 `--write-manifest` + 人工校 sourceLocale=zh。
5. **spec-mapping.md 结构**：三列表（spec 判据条目 | guide 落点小节 | 处理方式：正文/
   示例/互链），末尾附"未收录项 + 理由"（预期为空）。

## 顺序与回滚

guide → experiment.md → spec-mapping → contracts 测试 → docs 联动。全部为文档改动，
revert 单层即可；docs 联动失败不阻塞 guide 定稿（可分 commit）。
