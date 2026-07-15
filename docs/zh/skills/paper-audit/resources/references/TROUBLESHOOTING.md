# 故障排除

## 操作错误

|问题|解决方案|
| ------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
|未提供文件路径|询问用户有效的`.tex`, `.typ`， 或者`.pdf`文件|
|脚本执行失败|报告命令、退出代码和 stderr 输出|
|缺少兄弟姐妹技能脚本|检查一下`latex-paper-en/scripts/`, `latex-thesis-zh/scripts/`， 或者`typst-paper/scripts/`存在|
|PDF 检查有限|PDF 模式跳过格式/书目/数字检查；仅提供视觉和内容分析|
| `--venue`不被认可|使用以下之一：`neurips`, `iclr`, `icml`, `ieee`, `acm`, `thesis-zh`                                                                                    |
|ScholarEval LLM 维度显示 N/A|运行与`--scholar-eval`，然后通过提供 LLM 分数`--llm-json`                                                                                  |
|重新审核缺失的先前报告|提供`--previous-report PATH`指向先前的审计输出|
|文献检索未返回结果|检查 API 密钥； Semantic Sc​​holar无需密钥即可工作，但速度较慢； arXiv 始终可用|
| `TAVILY_API_KEY`未设置|设置环境变量或传递`--tavily-key`; Tavilly 是可选的 — S2 + arXiv 无需它即可工作|
|语义学者速率有限|放`S2_API_KEY`对于更高的限制；客户端有内置的指数退避|
|文献基础显示 N/A|运行与`--literature-search`启用自动文献验证|
|评分模型（`--regression`) 给出意想不到的分数|查看`scripts/models/scoring_model.json`;默认系数近似加权平均值|
|“找不到`final_issues.json`在工作区根目录”|该神器移至`artifacts/data/final_issues.json`新布局下；重新运行`--overwrite-workspace`在旧版 v5.1 工作区上|
|“找不到`revision_roadmap.md`"                    |重命名为`revision_suggestions.md`并保存在工作区根目录下|
|未生成 HTML 报告| `Jinja2`必须安装（`uv sync --extra dev`）；审计打印会抑制 HTML 失败，因此请检查 stderr|
|中文报告显示英文标题|经过`--lang zh`明确地`audit.py` / `render_html_report.py`;自动检测仅在以下情况下启动`metadata.json`已经记录`language: "zh"` |

## 审查质量故障路径

这些故障在期间或之后出现`deep-review`和`re-audit`运行。每个
ID稳定；测试和下游自动化可以参考它们。

### F1——审稿人严重分歧

**信号**：对于同一问题类别，各审查通道之间的分数差异 > 2.0，或者
对于相同的发现，一条通道报告“严重”，而另一条通道报告“轻微”。

**诊断步骤**：

1. 打开`committee/consensus.md`并找到`[SPLIT]`项目
2. 对照纸质文本交叉检查每条通道的证据引用
3. 验证审查通道焦点对齐`references/REVIEW_LANE_GUIDE.md`

**处理**：应用仲裁优先级 1-3
`references/editorial_decision_standards.md`。证据 > 专业知识 > 保守
偏见。将仲裁理由记录在`overall_assessment.txt`.

**涉及文件**：`committee/consensus.md`, `editorial_decision_standards.md`,
`synthesis_agent.md`.

### F2 — 轻量级审阅器输出空 JSON 或缺失字段

**信号**：其中之一`claims_evidence_reviewer`, `notation_consistency_reviewer`,
`self_consistency_reviewer`, `evaluation_fairness_reviewer`， 或者
`section_reviewer`回报`[]`或省略必填字段`ISSUE_SCHEMA.md`.

**诊断步骤**：

1. 查看`references/SUBAGENT_TEMPLATES.md`对于特定于审查通道的块
2. 检查通道分配的论文部分 - 仅当空时才有效
该部分非常干净
3. 使用规范模板重新调度审查通道

**处理**：重新派发后如果为空，记录`[Script]`注解
综合输出中“已检查审查通道，未发现问题”。不要合成
问题。

**涉及文件**：`SUBAGENT_TEMPLATES.md`, `ISSUE_SCHEMA.md`，空审查通道
输出文件。

### F3 — 报价验证失败集群

**信号**：`verify_quotes.py`将超过 20% 的问题报价标记为
`quote_verified=false`.

**诊断步骤**：

1. 根据来源检查失败的报价`.tex` / `.typ`/ 提取的 PDF
2. 检查 LaTeX 宏扩展不匹配（逐字 vs 渲染）
3. 确认论文在审查通道调度和验证之间没有被修改

**处理**：删除未经验证的发现或将其降级为次要
`[Script]`警告。列出故障计数`overall_assessment.txt`.

**涉及文件**：`scripts/verify_quotes.py`, `final_issues.json`.

### F4 — 阶段 3A/3B 检查点运行中失败

**信号**：`prepare_review_workspace.py`成功，但审查通道调度崩溃
中途离开`review_results/`部分人口。

**诊断步骤**：

1. 检查`review_results/manifest.json`（如果存在）最后完成的
审查通道
2. 查看`committee/`和部分输出的通道子目录

**处理**：仅重新运行失败的审查通道；不要重新启动整个管道。
合成步骤对于已完成的通道输出是幂等的。

**涉及文件**：`scripts/prepare_review_workspace.py`,
`scripts/consolidate_review_findings.py`.

### F5 — PDF 模式误报 LaTeX 特定问题

**信号**：`--mode deep-review`与一个`.pdf`输入产生的结果是
参考 LaTeX 宏，`.bib`条目或编译警告。

**诊断步骤**：

1. 确认`audit.py`正确检测到 PDF 模式（检查日志标题）
2. 验证格式特定的审查通道门禁用参考书目并编译
审查通道

**处理**：丢弃 PDF 运行中特定于 LaTeX 的结果。询问用户
对于来源`.tex`如果需要这些检查。

**涉及文件**：`scripts/audit.py`，审查通道门逻辑。

### F6 — 重新审核 root_cause_key 漂移

**信号**：`--previous-report PATH`已提供，但比较器报告
零重叠问题，尽管该论文似乎已部分修订。

**诊断步骤**：

1. 打开之前的报告并确认`root_cause_key`每个字段都存在
问题
2. 检查架构版本是否不匹配`ISSUE_SCHEMA.md`
3. 如果旧报告早于`root_cause_key`，通过重新派生密钥
迁移助手

**处理**：重新运行`consolidate_review_findings.py`反对旧报告
重新生成稳定密钥，然后重新调度比较器。

**涉及文件**：`ISSUE_SCHEMA.md`, `scripts/consolidate_review_findings.py`.

### F7 — 分数差异 > 2.0 但问题列表收敛

**信号**：审查通道在问题列表上达成一致，但他们的每个维度得分
急剧分歧。

**诊断步骤**：

1. 检查每个通道的校准`references/quality_rubrics.md`
等级定义
2. 检查一个泳道是否使用 ScholarEval 而另一个泳道是否使用默认评分

**处理**：标准化`quality_rubrics.md`加权公式。表面
校准增量`overall_assessment.txt`.

**涉及文件**：`quality_rubrics.md`, `scripts/scoring_model.py`.

### F8 — 直接拒稿分数与深度审查结论相冲突

**信号**：`editor_in_chief_agent`回报`Desk Reject`但`synthesis_agent`
仅产生次要发现，反之亦然。

**诊断步骤**：

1. 重新阅读两个特工的角色边界——EIC 是一个 90 秒的音调筛选器，
不是深度审稿人
2. 确认 EIC 仅在元数据 + 开头部分上运行
3. 交叉检查致命缺陷信号（第 3 节`editor_in_chief_agent.md`)
反对委员会的调查结果

**处理**：EIC 裁决仅适用于`gate`模式。在`deep-review`,
将 EIC 问题表面化为`pitch_quality`注释但推迟判决
到合成。

**涉及文件**：`editor_in_chief_agent.md`, `synthesis_agent.md`,
`MODE_GUIDE.md`.
