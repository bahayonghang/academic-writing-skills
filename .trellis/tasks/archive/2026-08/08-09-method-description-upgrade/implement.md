# 父任务执行图（parent 不直接实现，本文件管排序、集成与提交纪律）

## 1. 子任务排序

```text
C1 08-09-method-desc-zh        —— 先行：M-* 判据首个实现（判据以父 design §2 为唯一权威）
C2 08-09-method-desc-en-typst  —— C1 后或并行（若并行，任何判据疑义回父 design 裁决，不得各自解释）
C3 08-09-method-desc-audit-sync —— 必须在 C1、C2 归档后启动（依赖判据定稿与契约测试到位）
```

完成状态：C1、C2、C3 均已完成并归档。

每个子任务独立走 Phase 1.4 激活（review 已在父级完成，子任务 start 前只需确认工件未过期）→
Phase 2 实现 → Phase 3 收口归档。启动前把会话目标切到对应子任务
（`python ./.trellis/scripts/task.py` 目标机制，勿在 audit-sync 上误启 C1 的实现）。

## 2. 集成点（C3 步骤 4 执行，判据见父 prd 跨子验收）

- [x] 契约测试 `test_method_narrative_alignment.py` 绿（替代人工判据 diff）。
- [x] 红线负例三条在三技能 fixture 锁定情况核对。
- [x] spec §9 病例端到端：三技能检查器 + paper-audit Phase 0 输出摘要存 C3 research/。
- [x] 评分链验收：块解析计数 + Info 不扣分 + soundness 分差来源核对。
- [x] 全仓 `just ci`、四技能 `check_resource_sync.py --skill`、全量 checker、`just doc-build`。

## 3. 提交纪律（全体子任务适用）

- 实施代理（trellis-implement）不执行 git commit（其定义禁止）。
- 所有 commit 在各子任务 Phase 3.4 由主会话执行；子任务 implement.md 中"提交分组建议"
  仅规划 commit 边界（回滚粒度），不授权中途提交。
- 分组建议惯例：脚本+测试一组、参考文件+文档同步一组；Conventional Commits 按技能 scope。

## 4. 材料清单（子任务 jsonl 已挂）

- `research/user-spec-method-description.md` —— 用户 spec 原文（§9/§10 无损转写核对源）。
- `research/repo-recon.md` —— 机制事实、行号证据、审阅核验判定、遗留清单。
- `research/external-sources.md` —— 引用来源与先行技能取舍。
- `.trellis/spec/academic-writing-skills/docs-bilingual-resources.md` —— 双语资源契约。

## 5. 归档条件

- [x] 三个子任务全部归档，集成点 5 项全过。
- [x] hypothesis 结论已定稿并纳入父任务 journal：合成 fixture 支持候选检查行为，真实论文
      语料的查准率与召回率保持 `UNVERIFIED`。
