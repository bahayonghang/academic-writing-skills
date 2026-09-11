# Implementation Plan

1. 依据 core schema 写三份 profile manifest。
2. 建立 target alias 到各 profile section 的映射。
3. 接入 profile-local references/TSV 和 provenance。
4. 编写跨 profile isolation、candidate/core、degraded 测试。
5. 运行 profile focused checks，并交由独立 reviewer 检查来源边界。
