# paper-writing-studio Nature IEEE Elsevier profiles

## Goal

把三套现有知识包接入核心 profile 接口，保持各自规则、证据和 provenance 隔离。

## Requirements

- Nature 复用 section prompts、multi-section context、反编造与 em-dash 机制。
- IEEE 复用按节 references/TSV、core/statistical 门、Transactions 自称和节序。
- Elsevier 复用按节 references/TSV、core/statistical 门、领域刊自称和节序。
- 任何 profile 不得读取其他 profile 的 TSV 行或把其局部规则提升为全局规则。

## Acceptance Criteria

- [ ] 三个显式 venue 输出均加载正确 profile 并在 summary 标记版本与 evidence rows。
- [ ] Nature Here we/methods-last、IEEE/Elsevier self-reference 和 Related Work 选择的隔离测试通过。
- [ ] 缺失 source row 或 degraded observation 会显式降级，不静默补写。

## Dependency and scope

依赖 core-routing 子任务先冻结接口。只写新 skill 的 profile adapter/metadata；来源材料保持只读。
