# 调用方异常传播补充方案（已批准）

2026-09-27 用户明确批准纳入两处最小修复。

实施中发现原规划“其余 CLI 沿用异常传播”的前提不完整。

| 文件 | 已确认行为 | 最小修改 |
| --- | --- | --- |
| academic-writing-skills/latex-thesis-zh/scripts/check_format.py:236-239 | 捕获所有异常后返回空 issues，边界拒绝可被显示为 PASS/exit 0 | 显式导入 IncludeBoundaryError，在普通异常回退之前重新抛出 |
| academic-writing-skills/paper-audit/scripts/prepare_review_workspace.py:700-703 | 捕获 ValueError 后将边界拒绝降为 unsupported_format，丢失边界错误信息 | 显式导入 IncludeBoundaryError，在普通格式回退之前重新抛出 |

只增加两个调用方的特定异常传播，不改变原有其他读取错误和格式回退。回归加入已批准的
tests/shared/test_tex_loader_security.py，断言边界错误码可见且不返回正常成功。
EN verify_bib 已将异常转为明确 error，ZH polish 已有 ValueError 失败路径，不修改这两个脚本。

两个新增产品文件已加入 design 白名单。只修复异常传播，不扩大到其他调用方重构。
