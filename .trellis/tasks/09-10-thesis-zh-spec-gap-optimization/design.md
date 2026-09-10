# 总体设计与边界

## 现状到目标
本库 spec → 现行公开规则/脚本 → 缺口与反例 → 三个最小修复 → 各自验证 → 双语/共享门禁。
不把 .trellis/spec 注入安装后的论文工作流；可复用规则仍由 skill 内 references 拥有，
维护约定留在 .trellis/spec/academic-writing-skills。

采用 qiaomu-meta-skill 的 Production 级思路评估既有项目内增量；
不是生产一个新 package，因此不生成无用途的 interface、README、IR 或 release 目录。
完整先例/泛化/拒绝记录见 reports/prior-art-research.md；只声明 design advantage，
未实施的效果为 hypothesis。

## 需求与机制映射
| 父需求 | 机制 owner | 验收 |
| --- | --- | --- |
| R1 | 本任务 research/spec-coverage.md 与 spec-inventory.json；引用路径核对 | AC1 |
| R2 | C1 条件化旧示例、指向专用规则、8例输出核读 | AC2 |
| R3 | C2 语义候选、装配全文首次顺序、重复释义与来源定位 | AC3 |
| R4 | C3 单点输出路径、进程+产物判据、显式拒绝不支持组合 | AC4 |
| R5 | 子任务 focused tests；父任务双语 manifest/CI/docs 与证据分类 | AC5 |
| R6 | 各 child 独占文件；已授权实施范围；禁止面与最终 diff 核对 | AC6 |

## 所有权与执行顺序
建议 C1 → C2 → C3 → 父任务集成。C1 与其他子任务源码无重叠，可在批准后独立并行；
但 C2/C3 都涉及 test_latex_thesis_zh_scripts.py，必须串行交接，不并发编辑。
每个 worker 必须知道其他工作可能并发，只更改自己名下文件，不恢复全工作树。

父任务独占：
- docs/resource-manifest.json：每个 child 完成公开资源同步后，由主会话串行更新，
  允许该 child 运行单技能 gate；全部 child 完成后再执行一次全量 gate。
- .trellis/spec/academic-writing-skills/testing-and-tooling.md：在实施证据成立后，
  增量记录术语/缩写语义边界、编译 outdir 判据和旧指南示例需受事实保护的经验，
  指向 canonical 公开资源，不复制写作规则。
- .trellis/spec/academic-writing-skills/index.md：仅更新本次新增约定的索引说明。
- 本任务 research/reports 与共享验收记录。

C1 独占 evals 和新语义案例；C2/C3 用专项 pytest 回归，不再各建评估框架。
双语镜像各由拥有其 source 的 child 同步；目标路径由当前 manifest 推导，
不在旧 resources/modules 目录另造副本。
根 SKILL、README、版本不改变，因为不增加对外模块/触发范围。
如发现需要改变这些边界，先修订规划再取得新增实施授权。

## 运行、效果与学校规范边界
- 静态 contract/fixture 只证明规则和样例；C1 实际回答核读单独记录。
- C2/C3 单测须调用产品代码；Mock 不证明 TeX 安装/排版正确。
- C3 如有现成 TeX 则执行隔离 smoke；缺工具可交付软件修复，必须标记真实构建 UNVERIFIED。
- 五工具 fresh session、provider 对比、人工盲评、跨学科准确率、学校 class、打印和
  真实论文质量均不能由本轮 gates 代替。
- 不从参考 snapshot 推出当前学校法定字数或新国标；C1 只明确权威优先级和旧表适用性。

## 兼容性与回滚
不新增兼容 shim 或迁移层。C2/C3 允许纠正现有误报/假绿，明确记录具体行为变化。
C3 明确手动 recipe+outdir 暂不支持，禁止伪装成功；完整支持不是当前承诺。
检查时分别保存本任务 diff 和原有用户脏文件；回滚仅用批准范围的逆向补丁。
共享测试文件按实际累积 diff 交接，禁止整文件 checkout 或 git reset/clean。
