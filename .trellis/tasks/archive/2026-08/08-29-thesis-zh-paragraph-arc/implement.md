# 执行计划 (C2)

## 前置与标定

- [x] P1 C1 已在 `dev` 完成：`4b37ddf`，归档 `62f74a0`。
- [x] P2 私有真实 `chapter1.tex` 只读标定；仓库仅保存匿名标签和统计。
- [x] P3 激活前生成受控 `baseline-sample.tex` 与改造前 `baseline-before.txt`；激活后
      首先将二者复制到 `tests/fixtures/paragraph_arc/`，产品测试不得读任务目录。
- [x] T1 可执行脚本统计 42/33 个段落、收束覆盖 21.21%、双缺最大连续长度 0；
      候选 N=3。
- [x] T2 11 个正接口和 8 个负控按四位 Jaccard 标定；候选 τ=0.0200。
- [x] G1 作者确认 N=3、τ=0.0200 与人工标签边界。

## S0 激活与稳定基线

- [x] `task.py validate` 后激活 C2，并加载 Phase 2.1 上下文。
- [x] 用 `apply_patch` 新增 `tests/fixtures/paragraph_arc/baseline-sample.tex` 与
      `baseline-before.txt`，内容逐字节等于激活前任务 research 版本。
- [x] 将 G1 确认值冻结到 PRD、design、research；测试常量在 S3 固化。

## S1 段落切分与术语表

- [x] 新增段落/segment 数据结构和 `_split_arc_paragraphs`；标题及环境为硬边界。
- [x] 新增 `references/writing/paragraph-arc-terms.yaml` 与同值 fallback。
- [x] 实现章节归属、标题导语、item、环境收尾和专用章节豁免。
- [x] 聚焦验证：paragraph arc parser/terms contract tests。

## S2 四项检查与 CLI

- [x] 实现 LEAD、CLOSE、LINK、FLAT；LINK 严格采用四位小数和 `< τ`。
- [x] 实现默认 Info/P3 与 introduction/related 连续 N 双缺的一条 Minor/P2 汇总。
- [x] `analyze(..., paragraph_arc=False)` 与 CLI `--paragraph-arc` 接入；`--section`
      仅缩小章节作用域，不复用 `--first-chapter`。
- [x] 所有 finding 使用 `[Script] P-ARC-*` 且包含 `Meaning-Check: NEEDS-LLM`。

## S3 回归测试

- [x] AC1 LEAD/CLOSE 缺失定位与无误报正例。
- [x] AC2 全部豁免及标题/环境 segment 邻接边界。
- [x] AC3 默认 Info 与连续 N 双缺单条升级。
- [x] AC4 稳定 fixture 默认输出逐字节基线。
- [x] AC6 YAML/fallback/代码分支 contract。
- [x] AC8 输出字段与 logic 无改写契约。
- [x] AC9 LINK 显式/重叠、FLAT 单句/罗列正反例。
- [x] AC10 空 token、四位舍入、等于阈值和小于阈值边界。
- [x] 聚焦测试后运行全部 thesis tests。

## S4 references、docs 与 manifest

- [x] 新建 `references/writing/paragraph-arc-zh.md`：判据、背景/问题/方案段范式、
      回指/前瞻收束、原创抽象范例、与 AXES 的关系。
- [x] 更新 `logic-coherence.md`、`introduction-guide-zh.md`、`modules/logic.md`、
      `modules/routing-rules.md`。
- [x] 同步中英文 docs、资源 manifest；SKILL.md 只改 `last_updated`。

## S5 质量门与归档

- [x] G2 在同一私有章节只读复跑，优质接口误报不超过 2；代表性保留 UNVERIFIED。
- [x] `just ci`、资源散列/文档同步、`git diff --check`、`task.py validate` 全部通过。
- [ ] 按 C2 语义边界提交产品改动；随后归档 C2 并单独提交归档记录，不推送。

## 禁止事项

- 不改 S1、E-*、P-PAPER 既有行为；不给 logic 增加改写契约。
- 不提交私有论文正文，不让测试依赖任务目录或本机私有路径。
- 不改 `justfile`、`pyproject.toml`；观察级输出不用断言措辞。
