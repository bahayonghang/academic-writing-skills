# 脚本地图

完整剧本名单如下`scripts/`. `SKILL.md`保持简洁的摘要；
该文件是权威地图。

|脚本|目的|
| ---------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `scripts/audit.py`                       |阶段 0 审核和模式入口点|
| `scripts/paths.py`                       | `WorkspaceLayout`- 工件路径的单一事实来源|
| `scripts/i18n.py`                        |用于报表渲染的英文/中文字符串字典|
| `scripts/pre_submission_check.py`        |确定性的`PRESUBMISSION`机械审核层|
| `scripts/prepare_review_workspace.py`    |创建深度审查工作区|
| `scripts/build_claim_map.py`             |提取标题声明、关闭目标和附加内容`claim_candidates`                                                                                |
| `scripts/consolidate_review_findings.py` |删除重复评论 JSON|
| `scripts/verify_quotes.py`               |验证准确的报价是否存在|
| `scripts/render_deep_review_report.py`   |渲染最终 Markdown 报告|
| `scripts/render_html_report.py`          |渲染 review_report 和 revision_suggestions 的 HTML 双胞胎|
| `scripts/diff_review_issues.py`          |比较新旧发行捆绑包|
| `scripts/scholar_eval.py`                |九维 ScholarEval 评分（`--scholar-eval`)                                                                                                    |
| `scripts/scoring_model.py`               |加权加总分`--regression`（手动调整权重+交互/惩罚项，而不是经过训练的回归）具有加权平均回退|
| `scripts/literature_search.py`           |可选的外部文献搜索后端（`--literature-search`;塔维利通过`--tavily-key`/语义学者来自`--s2-key`，或 env 键）|
| `scripts/literature_compare.py`          |将论文稿件引用与外部文献证据进行比较|
