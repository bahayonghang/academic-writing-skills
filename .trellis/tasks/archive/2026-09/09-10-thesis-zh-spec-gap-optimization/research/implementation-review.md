# 中文论文 spec 差距优化独立实施审查

日期：2026-09-10。Reviewer：`/root/quality`，native delegated `trellis-check`。
基线：`dev` / `dd9f1e2a7f9bef164889df7016ffa942dd33d963`。
范围：父任务及 C1 guidance-fidelity、C2 consistency-semantics、C3 compile-outdir 的
PRD/design/implement、实际 check.jsonl、相关 spec、累计产品/测试/双语资源 diff 和运行证据。

## 结论

源码、公开规则及独立回归审查通过。审查发现一项 **Minor/P2** 的 C3 不支持组合诊断
顺序问题，已直接修复；修后98项编译回归、作用域 Ruff/Pyright 和一次新隔离真实 wrapper
构建通过。C1 八例新版原始响应的五维保真要求通过，C2 的顺序、释义候选和覆盖边界与
实际代码路径一致。没有遗留的本任务范围内阻断问题。

父任务共享资源门禁、docs build 和最终完整 CI 均已通过。主线程在本次修复后补跑
完整 CI：**1908 passed、2 skipped，0 errors、75条既有warnings**；Reviewer已读取
`research/ci-final.txt` 核对结果。第一次CI的1902条通过只保留为修复前记录，不代替
最终补丁验证。完整集成命令和退出码由 `research/integration-validation.md` 汇总。

## Findings (fixed)

- **File**：`academic-writing-skills/latex-thesis-zh/scripts/compile.py:191`、`:264`；
  `tests/skills/latex_thesis_zh/test_compile_outdir.py:147`。
- **Severity / priority / source**：Minor / P2 / [Script]。
- **Issue**：`compile()` 原先先发现手动 recipe 所需工具，随后才检查 manual recipe
  与 `outdir` 是否支持。缺少 xelatex 时，`--recipe xelatex-biber --outdir build` 返回
  `xelatex not found. Install TeX Live or MiKTeX.`，未说明参数组合不支持，也没有
  latexmk 支持路径提示。安装工具仍无法让该组合成功，违反 C3 AC3 的明确拒绝要求。
- **复现**：真实 ZH wrapper，Mock 只把工具发现设为不可用；exit 1、subprocess 0次，
  原错误消息可稳定重现。将原有六种 manual recipe 的拒绝测试扩为工具存在/缺失两种
  参数后，修前命令得到 **6 failed, 6 passed, 77 deselected**。完整输出保存在
  `research/review-regression-before.txt`，失败点均为缺少 `--outdir` 诊断。
- **Fix**：recipe 路径先进入既有 `_compile_with_recipe()`，由其检查 recipe 和不支持的
  outdir 组合，再进行原有工具发现。没有复制验证、替换 recipe、新建配置/接口或改变
  支持路径的命令。compiler 路径仍在原位置检查工具。
- **修后证据**：新增参数测试与全部 compile_outdir/既有 TestCompileZh 合计
  **98 passed**；七个本轮 Python 文件 Ruff check、最终 format check 通过；Pyright
  0 errors、2条原有 warnings。新隔离 `--recipe latexmk --outdir build` 真实构建 exit 0，
  `build/main.pdf` 为4178字节，源目录无 PDF。见 `research/review-tex-smoke.json` 及两份
  原始 stdout/stderr。

同时纠正了本 reviewer 新建 `output-review.md` 中旧规则的行号引用，指向实际
before snapshot 的:94、104；该文档修正没有触碰采样 raw 或产品规则。

## Findings (not fixed)

无本轮范围内未修复问题。既有 `compile.py:134` Optional recipe 类型告警保留；它与本次
控制流修复无新增关系。私有标定、provider、学校模板和真实论文未验项目列在证据边界，
不将“未验证”混报为产品失败。

## 实际路径审查

- **C1**：逐项读取五份源规则及对应 EN/ZH 改动。结果资格仍指向既有
  `results-analysis-guide-zh.md`；philosophy/AXES 不再直接替入数字，over-claim 区分
  预算混杂、组件贡献与具体机制，未检索首次不靠 hedge 保留。摘要与工程建议服从
  输入要求和实际证据；没有修改学校阈值、根 SKILL 或新增语义扫描器。
- **C1 实际输出**：详见 `../../09-10-thesis-zh-guidance-fidelity/research/output-review.md`。
  两个 native child 各完成八场景一次批量响应；fixture相同、五源快照/当前散列一致、
  历史47/49条前缀完整保留。新版八例五维通过；旧版大多数已通过，仅场景8出现不必要
  的逐篇解释倾向。没有从少量样例推导总体质量改善。
- **C2 输入与顺序**：`ConsistencyChecker._get_documents():135` 在有真实入口时调用
  一次既有 assemble；terms/abbreviations 共享装配文本，origin 投影回源坐标。无入口
  时每文件独立建阅读范围，API/目录/--all-files 不猜全局顺序；CLI 入口选择在:465。
  读取失败不缓存部分成功范围，缺 include 继续显示 loader 警告。
- **C2 定义与使用**：同一个 `_find_abbrev_definitions():188` 提取同物理行的有界
  片段；定义括号中的缩写不计独立使用。`:311` 用字符位置检测同一行先用后定义，
  汉字紧邻缩写可识别，ASCII 单词/数字/下划线内部片段不被截取。相同可见释义可重复，
  不同片段只给 `NEEDS-LLM` 候选，名称频率不决定规范名。
- **C3 命令与产物**：`_output_pdf():172` 的同一次目录计算驱动参数与最终PDF检查。
  compiler 与 latexmk recipe 均保留非0退出码；exit0但目标缺失返回1。指定outdir后源
  目录旧PDF不替代目标；已有目标且无需重建仍合法。不扩张 watch/clean、任意
  latexmkrc/jobname/auxdir 或手动 Bib 后端 outdir 协同。
- **测试真实性**：新测试通过 importlib 加载实际ZH副本并保护模块/路径状态，fixture
  位于仓库或 tmp_path；新增产品测试不依赖活动Trellis目录。C2 CLI测试确实调用
  shipped main，C3 Mock只替代外部进程/工具发现；无使用 kwargs-only 假wrapper取代
  行为。共享 scripts 测试中的C2断言和C3手动配方顺序均保留。
- **公开资源**：8份修改source各有两语镜像，源语言保持正文，另一语言没有反转学校
  优先、因果强度、candidate、current-only或outdir语义。新增导航均为文件级链接，
  未新增fragment；不需要伪造锚点验收。父manifest记录271条、8个source散列变化，
  单技能/full资源门禁已通过。
- **Spec 同步**：`testing-and-tooling.md` 新增输出目录、缩写顺序和教学保真三项
  维护约定，index只更新导航；公共写作资格仍归技能内references。没有新依赖、
  新CLI旗标、词典、评分/路由、兼容shim或其他技能实现。

## 子任务 AC 逐项对照

下表中的“通过”由实际产品、当前作用域证据及修复后的最终共享CI共同支持；不以较早
运行代替修改后验证。

| 子任务 AC | 机制、测试与实际判断 |
| --- | --- |
| C1 AC1 | after场景1/2/5分别保护未知量、孤立95%和有证据强结论；philosophy、AXES源规则同步。通过。 |
| C1 AC2 | after场景3/4/6区分预算混杂/组件贡献/区分性因果证据，并移除未检索首次；强结论不一律改成相关。通过。 |
| C1 AC3 | after场景7采用给定学校1000—1500字要求和1100字材料，保留理论/CPU/离线回放；场景8保留主题综合。通过。 |
| C1 AC4 | 源示例给出段主题、章目标、证据、保留/收窄/移位的定位映射；after场景8只诊断、不改邻段；source明确current改写需授权。通过；本轮未另采样授权current改写分支。 |
| C1 AC5 | 新旧八例raw、输入/规则散列、`fork_turns=none`调用转录及独立五维核读齐全；47条eval和49条trigger前缀逐对象保留。通过；非provider trace或盲评。 |
| C1 AC6 | 五源/双语/manifest资源门禁与docs build通过；无新增fragment；静态/response/真实论文明确分层。通过。 |
| C2 AC1 | 删除深度学习/深度神经网络、机器学习/机器智能、循环/递归错误混组及英文错误配对；`test_distinct_concepts_are_not_variant_mix`四反例和custom-terms真变体覆盖。通过。 |
| C2 AC2 | 同行/多行首用、include前后顺序、后章复用、定义不吞章标题均由实际API/CLI回归独立硬编码坐标验证；包括中文紧邻缩写。通过。 |
| C2 AC3 | 同章/跨章同释义重引、正常全称缩写使用不判语义冲突；不同释义含中英文保留源坐标和NEEDS-LLM建议。通过。 |
| C2 AC4 | 目录/--all-files/list API只报告文件内顺序并显示跨文件未验；入口排除无关草稿；同名目录路径可区分，缺include/读取失败可见。通过。 |
| C2 AC5 | 32项semantics新回归及旧precision/scripts验证注释、多行引用键、停用词、一次性缩写、定义后使用、源坐标；原错误概念正例已更正；main退出协议保留。通过。 |
| C2 AC6 | consistency源/EN/ZH区分terms与abbreviations覆盖、数学/单位人工复核及默认行为变化；相关资源门禁通过。通过。 |
| C3 AC1 | 路径矩阵覆盖default/显式latexmk recipe/XeLaTeX/LuaLaTeX与无outdir/相对/绝对/中文空格目录，命令cwd和目标报告独立断言；原6组真实构建路径已核读。通过。 |
| C3 AC2 | exit0+target、exit0+missing、非0+target、仅source旧PDF覆盖；无outdir显式compiler目标缺失也失败。通过。 |
| C3 AC3 | 六种manual recipe+outdir在工具存在和缺失两种状态均明确拒绝、零subprocess、有支持路径提示；本review自修复6个缺工具失败。通过。 |
| C3 AC4 | 无outdir有效手动六recipe、Bib后端警告后继续、shell-escape保护、非0传播，以及无需重建目标已覆盖；没修改watch/clean语义。通过。 |
| C3 AC5 | 新旧Mock均调用真实ZH wrapper；已核读原6组真实日志并复算现存PDF大小；本次改控制流后再新建隔离目录，真实latexmk wrapper生成4178字节目标PDF，exit0。通过。 |
| C3 AC6 | compile/compilation两源及四镜像写明相对基准、支持/拒绝组合、目标存在和进程成功边界；资源/docs门禁通过。通过。 |

## 父任务 AC 对照

| AC | 结论与证据 |
| --- | --- |
| AC1 | 58份spec覆盖清单、3,787行基线及16/3/39分类来自规划研究，已读取覆盖/散列记录及适用性裁决；不是实施后重新统计所有spec行数。通过。 |
| AC2 | C1全部条款的指定范围如上，八例输出独立核读完成。通过。 |
| AC3 | C2源码、32项新增语义回归及保留的旧合同覆盖全部条款。通过。 |
| AC4 | C3输出路径、三态、manual拒绝及真实wrapper证据齐全；新增诊断顺序问题已修复。通过。 |
| AC5 | 单技能/full资源271条和docs build通过；修后独立98项回归及最终全量CI1908 passed/2 skipped、0errors/75warnings通过。两个skip为当前Windows不适用的非Windows编码协议路径；TeX/provider/人工/真实论文证据分开。通过。 |
| AC6 | 仅批准产品/镜像/测试/父spec/任务证据变化；无新配置/依赖/路由/其他技能实现；三份原有dirty文件SHA256与execution-start逐字节一致；未提交归档发布或操作真实论文。通过。 |

## Verification

- **Lint: pass**。Reviewer实际运行全部7个本轮Python文件的 `ruff check`，exit0。
  首轮 `ruff format --check` 发现compile.py需格式化，运行formatter后再次检查，
  **7 files already formatted**、exit0；未忽略中间失败。
- **TypeCheck: pass**。Reviewer对同7文件实际运行Pyright，exit0，**0 errors, 2 warnings**；
  两条均为原有compile.py:134的Optional recipe参数告警，无新warning。
- **Tests: pass（当前作用域）**。修前12项拒绝测试为6失败/6通过，修后命令
  `rtk uv run --no-sync python -m pytest tests/skills/latex_thesis_zh/test_compile_outdir.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_scripts.py::TestCompileZh -q`
  得到 **98 passed in 8.30s**，无skip。没有为了绕开失败更改raw响应或放宽产品断言。
- **真实TeX: pass（输出位置）**。2026-09-10 13:02:38–13:02:41 UTC，通过真实wrapper
  `--recipe latexmk --outdir build` 编译新建临时article，目标存在、4178字节、源目录无PDF。
  wrapper字节SHA256为 `f8bd4f96650797dfb3d252afa5744616b48357fd64bcd112b75403954a8d518d`。
  原始过程见 `review-tex-smoke.json` 和关联日志；没有新跑原6组矩阵或执行GUI。
- **Diff: pass**。修后 `rtk git diff --check` exit0。
- **Shared gates: pass**。主线程最终完整CI exit0，**1908 passed / 2 skipped in 180.14s**；
  版本gate **1 passed**，Ruff **206 files already formatted / All checks passed**，
  Pyright **0 errors / 75 warnings**。Reviewer已读取 `research/ci-final.txt:8、13、15、192、335`
  核对，不把第一次CI的1902项通过当作最终结果。资源与docs均exit0，详见
  `integration-validation.md`。

两项skip均来自 `tests/skills/paper_audit/test_paper_audit_integration.py:216` 的
`skipif(sys.platform == "win32", reason="non-Windows Unicode protocol path")`，
对应 `returncode=[0,3]` 两例；当前为Windows，专用Windows编码协议测试实际运行。
这是平台适用性跳过，不是本轮新增失败或未执行的C1/C2/C3验收用例。docs build为
**20.27s、exit0**；后续只改编译Python和测试，未无故重跑不受影响的docs/采样。

原有用户文件保护已重新计算SHA256：`.gitignore`、`.trellis/.template-hashes.json`、
`skills-lock.json` 全部等于 `research/execution-start.md` 的三条启动值。

## 证据边界

本地native响应与合成API/CLI/TeX构建分别证明本次规则执行、检查器行为和产物定位。
它们不证明provider benchmark、人类盲评、真实论文总体质量、跨学科准确率、五工具
fresh session/权限、学校class、页面视觉、印刷、现场/操作者或长期部署效果；这些仍为
**UNVERIFIED / missing evidence**。已有TeX日志的Perl locale警告原样保留，没有改用户
全局配置消除它。没有付费provider调用、新依赖安装、发布或任务归档。
