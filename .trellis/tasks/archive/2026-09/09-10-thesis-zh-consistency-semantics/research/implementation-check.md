# C2 一致性检查器实施证据

日期：2026-09-10。授权：用户要求实施父任务及关联子任务；父任务已启动 C2。
本记录仅证明当前 ZH Python 实现、合成输入及本地命令结果，不证明真实论文总体语义质量。

## 基线及回归反证

可复跑探针：`research/probe_consistency.py`。探针通过 importlib 加载 shipped ZH 文件，
临时输入退出时自动清理；不依赖私人论文。修前执行：

```powershell
rtk python -X utf8 .trellis/tasks/09-10-thesis-zh-consistency-semantics/research/probe_consistency.py
rtk uv run --no-sync python -m pytest tests/skills/latex_thesis_zh/test_consistency_semantics.py -q
```

| 探针 | 旧行为 [Script] | 当前行为 [Script] |
| --- | --- | --- |
| G4：深度学习与深度神经网络共现 | WARNING，要求统一使用“深度学习” | PASS，无合并候选 |
| G5：两次 CNN 使用后才定义 | PASS；定义括号也计作第三次使用 | WARNING/undefined；首用 main.tex:1，定义 main.tex:3；独立使用计数为 2 |
| G5：两章同一个 CNN 释义 | multiple_definitions；全称吞入章标题及前一段 | PASS，definitions.CNN=2，issues=[] |

初始新文件 30 项回归对旧实现结果为 **27 failed, 3 passed**，包含用户可观察的 API
结果、真实 CLI、独立硬编码坐标，而不是仅复算内部位置列表。

主线程补充的中文紧邻边界以真实 ZH API 复现：

```text
someCNN CNN2 CNN_layer xCNN xCNN CNN2 CNN_layer。
使用CNN进行分析。卷积神经网络（CNN）用于分类。
```

`-k chinese_adjacent` 修前 **1 failed, 30 deselected**：实际 `usages={}`，
独立预期 `usages={"CNN": 1}` 且 first_usage 为 main.tex 第 2 行。
原因是 Unicode 词边界把汉字也视为词字符。现有两处缩写边界改为 ASCII 标识符边界，
同一个回归同时保证嵌入 ASCII 单词、数字或下划线标识符的片段不被误计。

## 实施边界

- 只消费既有 `assemble` 和 `origin`：入口模式装配一次，术语/缩写使用同一顺序文本；
  无入口时按文件分别判断，不猜文件列表首项，不创建章状态。无入口报告及 CLI 明示
  “文件内顺序已检查，跨文件顺序未验证”。源位置保留不同目录。
- 两种检查共用有界、同物理行的定义片段采集。句末、结构命令、跨行和超过局部窗口
  的不可靠片段不被猜成完整名称；缺少可靠边界时输出 NEEDS-LLM。
- 相同明确片段重复出现不报冲突；不同片段，包括中英文，输出可定位 NEEDS-LLM 候选。
  这不证明相同文字在全文必然同义，也不证明不同文字不同义。
- 删除三个中文概念混组和英文 deep learning/deep neural network 配对；保留其余现有
  分组作为候选，不新增词典。custom-terms 分组顺序与次数均不决定规范名。
- `full_after_abbrev` 保留为明确的可选风格候选，不要求全部换缩写；重新定义本身不算
  定义后全称反复使用。现有 WARNING/PASS 与模式退出码保留。
- 定义括号内缩写不计入独立使用；没有任何定义的缩写沿用阈值 2 和停用词。
  有后置定义时，即使此前只用一次也报告顺序问题。
- 多行引用键的既有遮蔽现在保留换行及字符偏移，避免源行号变短。
  读取失败可见且抛出，不将失败或部分文件缓存成空内容 PASS；缺 include 沿用 loader 警告。

## 改动文件

- `academic-writing-skills/latex-thesis-zh/scripts/check_consistency.py`
- `academic-writing-skills/latex-thesis-zh/references/modules/consistency.md`
- `docs/skills/latex-thesis-zh/resources/references/modules/consistency.md`
- `docs/zh/skills/latex-thesis-zh/resources/references/modules/consistency.md`
- `tests/skills/latex_thesis_zh/test_consistency_semantics.py`（32 个新测试实例）
- `tests/skills/latex_thesis_zh/test_latex_thesis_zh_checker_precision.py`（仅错误概念正例、候选及 full_after_abbrev 断言）
- `tests/skills/latex_thesis_zh/test_latex_thesis_zh_scripts.py`（仅 TestCheckConsistency 的 3 条语义断言）
- 本子任务 `research/probe_consistency.py` 与本记录。

共享 scripts 测试文件已明确交接 C3，交接后 C2 未再编辑或格式化该文件。
parser/loader、任务状态、manifest、maintainer spec、其他技能未由 C2 修改。
源 consistency.md 继续使用英文，EN 镜像与源一致，ZH 为完整译文。

## 检查结果

| 命令范围 | 结果 |
| --- | --- |
| 新 semantics + 存量 checker_precision + scripts 首轮 | 147 passed |
| 上述三文件 + test_parsers_alignment.py + test_skill_contracts.py | 208 passed，39.16s |
| 最后补入读取失败不缓存半成品回归后的完整新 semantics 文件 | 32 passed，3.06s |
| check_consistency.py + 新 semantics + checker_precision：Ruff check | passed |
| 同三文件：Ruff format --check | 3 files already formatted |
| 同三文件：Pyright | 0 errors, 0 warnings |
| C2 tracked 产品/文档/precision 文件 git diff --check | passed |
| G4/G5 当前探针 | 三项行为均符合上表 |

组合 pytest 的完整命令：

```powershell
rtk uv run --no-sync python -m pytest tests/skills/latex_thesis_zh/test_consistency_semantics.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_checker_precision.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_scripts.py tests/contracts/test_parsers_alignment.py tests/contracts/test_skill_contracts.py -q
```

读取失败的最终补充只改变初始化失败后的缓存行为；补充后新文件全量回归通过。
新增测试完整快照并恢复 sys.path/sys.modules，并断言加载文件的真实 ZH 路径。
CLI 子进程使用 UTF-8 输出和父端 UTF-8 解码配对，未给 pytest 设全局编码变量。

## 默认行为变化及待父任务收口

默认行为变化属于误报/假绿修复：不同概念不再合并；定义后重复全称只给可选候选；
同章或跨章合法重引不再报冲突；先用后定义、中文紧邻首用现在可定位；定义括号不再
增加独立使用次数；散文件结果明确覆盖限制；多行遮蔽不再破坏行号。
后续若获提交授权，提交正文须保留“默认行为变化”及原因声明。

父任务负责 manifest、公开资源门禁、文档构建、完整 CI、独立审阅与状态收口。
真实论文语义一致性、数学/单位等价、五宿主运行、provider 或人工盲评仍为
**UNVERIFIED / missing evidence**。本子任务未提交、归档、推送或执行 GUI 操作。


## 父任务集成完成（2026-09-10）

上述交接时待执行门禁现已完成：最终完整CI为1908 passed、2项平台条件skip，
Pyright0 errors/75既有warnings；单技能和全量资源271项、docs build与独立审阅均通过。
本任务AC已全部回填；未提交或归档。最终状态与证据以
[父级集成验收](../../09-10-thesis-zh-spec-gap-optimization/research/integration-validation.md)为准。
