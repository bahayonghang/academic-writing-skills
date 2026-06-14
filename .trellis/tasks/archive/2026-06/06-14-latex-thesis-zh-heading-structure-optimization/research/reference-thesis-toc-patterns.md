# Reference Thesis TOC Patterns

Source PDFs inspected locally:

- `D:\Documents\LYH\200-Learning\00博士毕业\毕业论文\thesis\ref\thesis\复杂非平稳工业过程异常监测与诊断_张志鹏_学位论文.pdf`
- `D:\Documents\LYH\200-Learning\00博士毕业\毕业论文\thesis\ref\thesis\水泥粉磨过程关键指标预测模型与运行优化算法研究.pdf`

Extraction method: PyMuPDF `doc.get_toc(simple=True)`; no PDF content was modified.

## Zhang Thesis: Complex Non-Stationary Industrial Process Monitoring

Core chapter title pattern:

- 第 2 章：高维动态耦合的非平稳工业过程自适应异常监测方法
  - Object: 非平稳工业过程
  - Problem: 高维动态耦合、异常监测
  - Method: 自适应异常监测方法
- 第 3 章：考虑过渡模态的非平稳工业过程异常监测方法
  - Object: 非平稳工业过程
  - Problem: 过渡模态异常监测
  - Method: 考虑过渡模态的方法
- 第 4 章：基于 CVAE-SFA 的双通道多指标综合运行工况评估
  - Object: 运行工况
  - Problem: 多指标综合评估
  - Method: CVAE-SFA 双通道
- 第 5 章：基于因果强度对比的异常路径辨识与根因诊断
  - Object: 异常路径/根因
  - Problem: 路径辨识与根因诊断
  - Method: 因果强度对比
- 第 6 章：水泥煅烧过程异常监测与诊断系统设计及应用
  - Object: 水泥煅烧过程
  - Problem: 异常监测与诊断
  - Method/path: 系统设计及应用

Section-count pattern:

- Core chapters 2-5 each use 5 direct sections:
  - 引言
  - 基础理论与问题描述
  - 模型建立 / 方法建立
  - 案例研究与结果分析
  - 本章小结
- Chapter 6 uses 4 direct sections:
  - 引言
  - 系统架构与功能设计
  - 系统应用
  - 本章小结
- This supports a "five direct sections by default" thesis-writing heuristic.

Section anchoring pattern:

- Direct sections repeat chapter-level roles rather than unrelated keywords:
  - `基础理论与问题描述` establishes the chapter problem.
  - `模型建立` or `策略` carries the method.
  - `案例研究与结果分析` verifies the chapter method against the object.
  - `本章小结` closes the chapter.

## Cement Grinding Thesis

Core chapter title pattern:

- 第 2 章：水泥粉磨过程工艺分析与运行优化框架
  - Object: 水泥粉磨过程
  - Problem: 运行优化
  - Method/path: 工艺分析与优化框架
- 第 3 章：基于异构数据融合的水泥比表面积软测量模型
  - Object: 水泥比表面积
  - Problem: 软测量
  - Method: 异构数据融合模型
- 第 4 章：水泥粉磨过程单位电耗时间序列预测模型
  - Object: 水泥粉磨过程单位电耗
  - Problem: 时间序列预测
  - Method: 预测模型
- 第 5 章：基于 CIE-MOCS 的水泥粉磨过程单步决策算法
  - Object: 水泥粉磨过程
  - Problem: 单步决策
  - Method: CIE-MOCS 算法
- 第 6 章：基于多步优化的水泥粉磨过程稳定调控算法
  - Object: 水泥粉磨过程
  - Problem: 稳定调控
  - Method: 多步优化算法

Section-count pattern:

- Chapters 3-6 follow a compact 5-section shape:
  - 引言
  - 框架/问题/算法基础
  - 建模/方法
  - 实验/验证
  - 本章小结
- Chapter 2 has 7 direct sections, which is useful as a counterexample for this task:
  - It separates 工艺分析、数据预处理、优化问题、优化框架、多目标模型 into multiple direct sections.
  - Under the user's requested rule, these would likely be merged into at most 5 larger sections.

## Derived Rules For latex-thesis-zh

1. Body chapter titles should expose object + problem + method/path.
2. The default direct-section budget should be <= 5 per chapter.
3. Conventional chapter roles can be exempt from object-problem-method:
   - 绪论
   - 相关工作 / 文献综述
   - 结论 / 总结与展望
   - 参考文献 / 致谢 / 附录
4. Direct sections should map to chapter roles, not arbitrary procedure fragments:
   - 引言
   - 基础/问题描述
   - 方法/模型/算法/框架
   - 实验/案例/应用/结果分析
   - 本章小结
5. If a chapter needs more than 5 direct sections, the skill should suggest consolidation:
   - Put detailed modules under `\subsection`.
   - Merge adjacent setup sections into "问题描述与建模基础".
   - Merge validation sections into "实验设计与结果分析" or domain-appropriate equivalents.
