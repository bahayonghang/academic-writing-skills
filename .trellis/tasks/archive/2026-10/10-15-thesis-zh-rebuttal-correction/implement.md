# 执行计划

用户已明确批准最终计划并要求开始实施（2026-10-15）。

## 执行顺序

- [x] 用户批准后核对工作树、运行 task.py start；主会话按 Trellis 分派 implement 子代理，首行 Active task 路径，明确共享工作区和禁止覆盖他人改动。
- [x] 迁移四个回复脚本，解除 extract_thesis/check_deck 依赖，保留 CLI/schema/R-*。
- [x] 迁移合成输入、台账、最小论文 fixture 与三组回复测试；添加独立复制 thesis 包的端到端测试。
- [x] 将 defense 包和入口测试恢复到 53c2ab5 内容，验证基线差异为空，保留更早修复。
- [x] 按 qiaomu 触发优先和渐进披露更新 thesis 入口、适配、eval、reference/example。
- [x] 迁移双语资源，更新 README/usage/首页/manifest/CHANGELOG/spec。
- [x] 生成 task reports：prior-art 适用性、skill-ir、触发 smoke、输出/安装证据、creation-handoff。
- [x] 分派 Trellis check 子代理完成范围审查与质量门，修复本次引入的问题。
- [x] 主会话复核 diff 和 AC，交付结果；提交、归档、journal、发布需另行明确授权。

## 验证命令与证据

1. 定向 pytest：两技能测试、skill contracts、trigger eval、docs bilingual、include/parser 对齐。
2. 隔离复制 thesis 包，在包外 cwd、移除 PYTHONPATH 的子进程运行三条 CLI；完成态 fixture 有真实测试 git 修改证据；比对输入哈希和输出。
3. git diff 53c2ab5 -- academic-writing-skills/latex-defense-zh 为空；检索当前公开资源无错误 defense 回复路径。历史 task/journal/CHANGELOG 条目排除。
4. qiaomu validate_skill.py、export_skill_ir.py 与适配当前 schema 的 trigger smoke；记录结构限制，静态结果不声称 provider-backed。
5. uv run python docs/scripts/check_resource_sync.py。
6. just ci：check-versions → lint → typecheck → test；just doc-build；git diff --check。
7. 真实编译/五工具/provider/私有评阅书未执行时登记 NOT_RUN/UNVERIFIED。

## 文件边界

两技能 SKILL.md、agents/openai.yaml、evals；回复专属 scripts/reference/example；必要的合成论文 fixture；对应 tests/skills 子目录及必要契约测试；README 双语、docs CHANGELOG/usage 双语、两技能首页与回复镜像、manifest；spec 的 rebuttal/deck 契约和 index；当前任务产物。

不修改 .agents 技能、公共 parser/loader、依赖配置、归档任务或其他技能。发现必要超界变更先报告。

## 规划收敛

- [x] 用户目标、范围、基线和依赖已确认。
- [x] PRD 已整理为最终结构，验收可观察，无阻塞性需求问题。
- [x] design/implement 与真实 spec/research manifests 已准备。
- [x] 用户批准最终计划。


## 最终结果

2026-10-15：完整 just ci 通过（2847 passed / 11 skipped），资源同步 305 项通过，文档构建和 diff 检查通过；defense 53 个基线文件一致。已保留所有运行与依赖限制，未提交、归档、写 journal 或发布。
