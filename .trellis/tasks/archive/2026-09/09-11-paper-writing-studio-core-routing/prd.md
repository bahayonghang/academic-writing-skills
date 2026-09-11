# paper-writing-studio 核心路由与输出契约

## Goal

实现父任务批准的统一输入、venue 选择、section 别名、共享证据不变量和规范化输出，不实现具体刊物规则。

## Requirements

- 显式 venue 优先于 journal、domain；冲突可解释。
- 无安全映射时使用父任务确认的 unspecified 行为，不猜测。
- 统一输出 text、text_compact、summary，并保留 protected-token、untraceable-token、degraded 字段。
- candidate/core 和统计 opener 门槛在可信边界执行一次。

## Acceptance Criteria

- [ ] 核心模块单元测试覆盖 precedence、冲突、别名、unspecified、候选行和保护 token。
- [ ] 接口文档与父任务 R1/R4 一致，且不加载任何 venue TSV。
- [ ] validate_skill.py 与相关项目测试通过。

## Dependency and scope

这是父任务的第一个实现子任务。只写 academic-writing-skills/paper-writing-studio/ 的核心入口与契约文件；不修改三套来源材料。
