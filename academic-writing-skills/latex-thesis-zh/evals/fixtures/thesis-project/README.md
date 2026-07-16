# thesis-project fixture（虚构示例论文工程）

> 本工程内的研究内容、数据、作者与文献条目**全部为虚构占位**，仅服务于
> latex-thesis-zh 的测试与评测；LaTeX 结构（documentclass / include 骨架 /
> 环境用法）按真实 thuthesis 风格组织。不要求可真实编译。

## 结构

```
main.tex                  # thuthesis 骨架，仅 \include 各章（另含盲审字段埋点）
chapters/intro.tex        # 绪论
chapters/related.tex      # 相关工作
chapters/method-a.tex     # 占位对齐方法（与 method-b 同含"方法"）
chapters/method-b.tex     # 占位融合方法
chapters/experiment.tex   # 实验与分析
chapters/conclusion.tex   # 总结与展望
chapters/appendix-gbk.tex # GB18030 编码边角文件
chapters/achievements.tex # 攻读学位期间成果（盲审 R2 埋点）
chapters/acknowledgement.tex # 致谢（盲审 R1 埋点）
references.bib            # 含缺字段条目的虚构文献库
references-gbk.bib        # GB18030 编码的虚构中文文献库（编码回退埋点）
```

## 埋点清单（已知问题 → 预期检出）

| # | 埋点位置 | 已知问题 | 预期检出模块 / 输出标记 |
|---|----------|----------|------------------------|
| 1 | intro.tex L2-L3 | 绪论从背景直接跳到本文方案（无瓶颈铺垫） | `logic` → `绪论结构 ... 缺少技术瓶颈铺垫` |
| 2 | intro.tex 研究背景节 | 标题后直接进入 itemize，缺导语 | `logic` → `缺少导语段落`（定位 `chapters/intro.tex`） |
| 3 | intro.tex L3 | `\ref{fig:ghost}` 未定义 | `references` → `Undefined reference`（Critical） |
| 4 | intro.tex / related.tex | `近年来` ×2（模板化表达） | `deai` → template_expr |
| 5 | intro.tex 研究背景 | `具有重要意义`（空话） | `deai` → empty_phrase |
| 6 | related.tex L3-L6 | 作者（年份）罗列连续 4 条 | `logic`/`literature` → A1 罗列模式 |
| 7 | related.tex 末尾 | 无研究空白推导 | `logic`/`literature` → A3 `未发现研究空白` |
| 8 | intro vs related | `深度学习` vs `深层学习` 同义混用 | `consistency` → variant_mix |
| 9 | method-a / method-b 章标题 | 两章标题均含"方法" | split_sections → `method` + `method_2`（均被检查） |
| 10 | method-a.tex L2 | `本文采用...` 无选择理由 | `logic` → `方法选择缺乏论证` |
| 11 | method-a.tex 章引言 | 单句过简 + 缺承上启下 | `logic` → `章引言过简/缺少承上/缺少启下` |
| 12 | method-b.tex L2 | 相对指代"上一章" | `logic` → `相对指代`（Minor） |
| 13 | experiment.tex L5-L8 | `本系统` 开头连续 4 行排比 | `deai` → parallel_structure |
| 14 | experiment.tex L5-L6 | `显著提升` ×2（空话） | `deai` → empty_phrase |
| 15 | experiment.tex L8 | `非常好`（口语表达） | `format` → oral_vague（warning） |
| 16 | experiment.tex L9 | `——` 破折号 6 处（默认上限 5） | `deai` → punctuation:em_dash_overuse |
| 17 | experiment.tex 表格 | 竖线列规格 + \hline + caption 在 tabular 后 | `tables` → vertical_lines（FAIL）/hline/caption_position |
| 18 | experiment.tex 图环境 | `fig:orphan` 无 caption 且未被引用 | `references` → missing caption + unreferenced label |
| 19 | conclusion.tex | `综上所述` 段首套话 | `deai` → throat_clearing / filler_connector |
| 20 | intro 承诺 vs conclusion | 绪论有"本文提出/主要贡献"，结论无回应 | `logic` → C3 `跨章节逻辑链可能不完整` |
| 21 | conclusion.tex | 缺局限与未来工作/缺核心发现 | `experiment` → `Conclusion lacks ...` |
| 22 | appendix-gbk.tex | GB18030 编码 | 各脚本 → `WARN ... GB18030` 且内容被正确解析 |
| 23 | references.bib | @phdthesis 缺 school / @online 缺 urldate / @techreport 缺 institution / @article 缺 volume+pages | `bibliography --standard gb7714` → 对应 Missing field |
| 24 | 全工程（未新增文件） | 天然规模性违规：文献仅 5 篇、无 2025+ 文献、摘要约 90 字、正文约 918 字、无关键词宏、method/experiment 三章无“本章小结”、附录章无 `\appendix` | `spec-check --template yanshan --degree doctor --year 2026` → YS-11/18/19/24/25/26/47 FAIL，YS-01/13/14/17/29/30/31/33 PASS（断言见 `tests/skills/latex_thesis_zh/test_check_spec.py`）；同批违规在新清单下：`--template thuthesis\|pkuthss` → THU-02/PKU-02（摘要 800–1000）FAIL，THU-24/PKU-22/GEN-21（附录无 `\appendix`）FAIL，THU-01/PKU-01/GEN-01（题名 13 字）PASS，generic 摘要字数只报数（GEN-05 NEEDS-LLM）（断言同文件） |
| 25 | main.tex preamble | `\author{测试作者}` 与 `\thusetup{supervisor = {测试导师}}` 字段（带 `% seed:`） | `blind-review --check` → R1 作者/导师字段 HIGH；`--generate` → 副本中字段值→`□□□` |
| 26 | achievements.tex 条目一 | 成果条目含作者列表 + 成果名称 + 期刊页码（条目二已合规，预期不检出） | `blind-review --check` → R2 HIGH；`--generate` → 副本条目上方插 `% TODO-BLIND(R2)`，条目零改写 |
| 27 | acknowledgement.tex | 非空致谢，正文含“测试导师/测试作者”姓名 | `blind-review --check` → R1 致谢 HIGH；`--author/--supervisor` 全文姓名扫描命中；`--generate` → 正文→“（盲审版本，致谢内容略）” |

注：致谢/成果两章标题命中 `check_spec.py` 的 `FRONT_BACK_TITLE_RE`，不计入正文字数与
“本章小结”检查，埋点 #24 的 spec-check 断言不受影响。

## 使用

- pytest 冒烟测试：`tests/skills/latex_thesis_zh/test_latex_thesis_zh_coverage.py`（SKILL.md 全部路由主命令）。
- evals：`evals/evals.json` 中 files 指向本工程的用例。
- 修改本工程任何埋点时，须同步更新本清单与相关断言。
