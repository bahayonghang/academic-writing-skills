# paper-writing-studio 评估文档与资源同步

## Goal

为统一 skill 建立 Production 级触发/输出评估、README/interface、Skill IR、来源报告和资源同步证据。

## Requirements

- 正触发：三种 venue、section/整稿、中译英和学术英文润色。
- 负触发：排版、编译、Zotero 写入、格式检查和未授权文件输出。
- 输出案例覆盖 unspecified、显式 venue 与 journal 冲突、别名、candidate 行、保护 token、anti-AI、degraded 和 text_compact 差异。
- README 解释三种 profile 的差异、来源、限制和 missing evidence；不把 catalog 指标写成质量评分。

## Acceptance Criteria

- [ ] trigger_eval 与 output eval 通过，且报告记录 fixture 局限。
- [ ] Skill IR、README、interface、资源 manifest/docs 镜像一致。
- [ ] release_check 的本地包门通过；provider、真实论文、人审和干净安装仍单独标记。

## Dependency and scope

在 core 与 profiles 契约冻结后实施。只写 evals、reports、README/interface 和必要的资源同步文件。
