# Creation Handoff：academic-defense-beamer 学术视觉与信息架构升级

日期：2026-11-21

## 1. Result

- **Skill 名称与版本**：`academic-defense-beamer` `6.0.0`（许可证：`PolyForm Noncommercial 1.0.0`，非商业学术科研与教学用途）
- **一句话定位（Job to be done）**：从已有中文 XeLaTeX 学位论文仓库只读提取章节、图表、公式、贡献与成果，按答辩时长预算及双后端现代学术视觉体系生成零编造的 Beamer 或 Typst Touying 答辩/预答辩幻灯片、逐页讲稿与双屏备注版 PDF，并通过 22 码保真与密度质量门验证。
- **本地路径与发布状态**：`academic-writing-skills/academic-defense-beamer/`；已完成仓库本地实现、双语文档站镜像同步与本机实编验收，待用户确认后提交本地分支（未对外独立发布，不直接推送默认分支）。

## 2. Reference skills studied

仅列出本次会话实际检视过源码或成稿结构的参考对象；仅出现在目录搜索结果中但未拉取外部源码的条目单独说明并标注 `missing evidence`。

1. **`@preview/simply-ysu-touying:0.2.0`**（本机 Typst 包缓存源码实测检视：`themes/tokens.typ`、`themes/components.typ`、`themes/ysu-beamer.typ`）
   - **入选原因**：本技能 Touying 后端直接依赖的上游公开主题包，已具备成熟的 v3 现代学术色彩令牌与 30 个结构化排版原语。
   - **采用与可信信号（2026-11-21）**：Typst Universe 正式发布包 `0.2.0`，本机包缓存源码逐文件核验；`rating evidence unavailable`。
   - **学习到的具体机制**：`ysu-navy (#1F296A)` + `ysu-red (#B42318)` + `ysu-tint (#F2F4F9)` / `ysu-line (#D9DCE5)` / `ysu-muted (#5A6072)` 语义色阶、双层强调 `#key`（砖红粗体）/ `#hl`（深蓝粗体）、`#tag` 维度短签、`#kpi` 顶部粗线关键指标块、`#title-box` 多列网格卡片、`#result-table(mark:)` 重点行高亮。
   - **落点位置**：`templates/beamer/{defense-layouts,beamerthemeYanshanDefense,beamerthemeGenericDefense}.sty`、`scripts/{build_deck,typst_backend}.py`、`templates/jinja/frames/*.tex.j2`、`templates/typst/frames/*.typ.j2`。

2. **`bahayonghang/academic-writing-skills@academic-defense-beamer` 既有基线与署名先例**（仓库内源码检视；致谢源含 `claude-skill-academic-ppt` MIT 与 `thesis-defense-pptx-skill` Apache-2.0）
   - **入选原因**：本仓库唯一覆盖中文学位论文 LaTeX 源只读提取、双后端生成与 22 码事实保真门禁的生产技能基线。
   - **采用与可信信号（2026-11-21）**：`skills.sh` 记录 `academic-defense-beamer` `69 installs`、旧名 `latex-defense-zh` `116 installs`；`rating evidence unavailable`（注：`installs` 仅代表安装采用频次，不等同质量评分）。
   - **学习到的具体机制**：五脚本解耦流水线（`extract` → `plan` → `build` → `check` → `preview`）、`DefenseSource` 原文逐字保护区、双屏备注 PDF 页标签契约（Beamer 32:9 / Touying `notes:N`）。
   - **落点位置**：完整保留 `.trellis/spec/academic-writing-skills/defense-deck-contract.md` 锁定的 CLI 签名、退出码与 22 个 `D-*` 码闭集，在不新增 `D-*` 码的前提下将多列卡片计数与单帧强调上限融入 `D-CHAIN` 和 `D-DENSITY`。

3. **跨体裁答辩汇报版面拆解样本**（2026-11-21 经 `ego-browser` 抓取并逐页检视 12 张 16:9 幻灯片成图，详见 `research/source-article.md`）
   - **入选原因**：用户指定的视觉与信息架构参考样本，展示了高可读性的中文学术汇报块面组织与微排版密度控制。
   - **采用与可信信号（2026-11-21）**：公众号公开案例成图直接目视拆解（无组件源码，所有版式与示例文本均独立自写合成）。
   - **学习到的具体机制**：三段式页面视觉锚点、16:9 画布下的 2×2 / 三列卡片矩阵、`维度短签｜核心短句` 微排版、带比较基准的独立指标块，以及第 9 页中英夹杂漏译词反例带来的纯正学术中文警示。
   - **落点位置**：`templates/beamer/defense-layouts.sty`、`templates/beamer/demo-deck.tex`、`references/{visual-spec,slide-layouts,plan-schema,content-rules}.md`。

- **目录检索未检视外部源码说明**：2026-11-21 检索 `skills.sh` 命中 `k-dense-ai/scientific-agent-skills@scientific-slides`（`2.5K installs`，`rating evidence unavailable`），检索 `SkillsMP` 命中 `nexu-io/open-design`（`108,512 repo_stars`，`rating evidence unavailable`；`repo_stars` 为源仓库星标而非单技能评分）。因本次任务未拉取外部仓库源码检视，统一记 `missing evidence`，不作跨技能优劣断言。

## 3. Absorbed and rejected

- **`keep`（保留）**：
  - 五脚本流水线 CLI、退出码、12 个固定 `layout` 名称与 22 个 `D-*` 码闭集；
  - 学位论文事实保护红线（`D-FIG-ALLOW` 仅用论文原图、`D-EQ-SRC` 公式逐字一致、`D-TAB-SRC` 表格逐格一致、`D-NUM-SRC` 论文外数字预警）；
  - 双屏备注版 PDF 的 FerroStage / pympress 兼容契约及既有 `slide_plan.yaml` 100% 向后兼容。
- **`adapt`（面向学位论文答辩改编）**：
  - 将 Beamer `yanshan` 的荧光纯红 `#FF0000` 校准为沉稳砖红 `#B42318`（`generic` 为 `#A93226`），补齐 `defenseTint`、`defenseLine`、`defenseMuted` 块面色阶；
  - 统一双后端双层强调语法：`**关键结论**` 渲染为砖红粗体（Beamer `\DefenseHighlight`、Touying `#key`，单帧上限 3 处，超限报 `D-DENSITY` Minor），`*结构术语*` 渲染为深蓝粗体（Beamer `\DefenseTerm`、Touying `#hl`），演讲备注中统一退化为无色粗体；
  - 扩展 `cards` 可选 `columns: 1 | 2 | 3`（4 卡缺省 `2×2` 宫格，3 卡缺省单列以保持既有快照兼容）、`bullets` 可选 `短签｜正文` 拆分、内容帧可选 `metrics`（≤ 3 项，全量纳入 `D-NUM-SRC`）与 `table` 可选 `highlight_rows`（Touying 透传整数元组 `mark: (...)`，零字符串/方括号泄漏）。
- **`reject`（否决及原因）**：
  - 否决引入论文清单外的商业实景照片、重绘机理流程图与获奖证书扫描墙（违反 `D-FIG-ALLOW` 与学术事实保真边界）；
  - 否决科技奖「经济社会效益」套路章节与任何「规避 AI 检测器」承诺（体裁不符且违背仓库学术诚信规范）；
  - 否决新增第三个 `--theme` 枚举（避免双后端矩阵膨胀与维护分叉）。
- **`invent`（本技能原创连接）**：
  - 在 Typst Touying 代码生成与静态检查器之间建立「零配置字面量泄漏」渲染约定：`ty_bullet` 调用 `#tag("短签")` 复用主题默认 `kind: "navy"`、`result-table` 透传纯整数元组 `mark: (0, ...)`，使微排版组件扩展与 `check_typst.visible_lines` / `check_typst.tables` 静态保真检查严格正交（已固化入 `.trellis/spec/academic-writing-skills/defense-deck-contract.md` 第 7 节 `Wrong vs Correct`）。

## 4. Advantages and highlights

- **`[design advantage]` 双后端视觉与语义同构升级**：相比升级前 Beamer 第 1 代纯白裸排 + `#FF0000` 纯红框样式，升级后的 Beamer 与 Touying 共享深海蓝/沉稳砖红/浅灰蓝块面层级、双层强调语法（`**…**` 与 `*…*`）、多列卡片矩阵、维度短签与带基准 KPI 指标块（证据：`academic-writing-skills/academic-defense-beamer/templates/beamer/defense-layouts.sty:275-435`、`scripts/build_deck.py:199-230`、`scripts/typst_backend.py:101-141`）。
- **`[design advantage]` 可执行的学术答辩文风与强调克制门禁**：`references/content-rules.md` 明确要求首屏可核查判断句、`2–4 字维度签｜12–28 字动宾短语`、禁用空洞评价套话及非专业缩写的未译外文残留词，并由 `scripts/check_deck.py:1363-1442` 在双后端自动拦截单帧超过 3 处的砖红关键强调。
- **`[validated advantage]` 全仓契约、双后端实编与异构模型闭环复核**：
  - 全仓 `just ci` 四步通过：版本对齐 `1 passed`、`ruff format --check`（257 文件）与 `ruff check` 全通过、`pyright` `0 errors`、全仓 pytest `2967 passed`（含 `academic-defense-beamer/evals/trigger_eval.json` 全部 21/21 正负触发评估契约）；
  - 开启 `DEFENSE_COMPILE=1` 与 `DEFENSE_TYPST_COMPILE=1` 的答辩技能全量实编测试 `268 passed, 0 skipped`（覆盖 15 页 `demo-deck.tex` 三种主题配置双遍 `xelatex` 编译、54 页合成论文 Beamer/Touying 投屏版与双屏备注版 PDF 编译及 `D-NOTES-PDF` 校验）；
  - 双语文档站 `uv run python docs/scripts/check_resource_sync.py`（310 条资源清单）与 `just doc-build` 全站构建通过；
  - 经独立异构模型 `Gemini 4 Hydrogen`（`taste-verifier`）两轮目视与代码审计：首轮精准检出 `demo-deck` 单遍 `xelatex` 编译导致封面/目录视口偏移及 `\DefensePaperBox` 背景填充遮盖正文两处缺陷；修复为 `on background layer` 圆角裁切与双遍编译 + 像素级防遮挡单测后，二轮复核确认 15 页预览画面与单测 100% 通过。
- **`[hypothesis]` 跨外部大模型开放式生成质量提升**：`content-rules.md` 的短语化断言、维度短签与禁漏译外文规则预期能显著降低大模型填写真实长篇论文 `slide_plan.yaml` 时的散文化与套话率，但跨不同外部 LLM provider 的盲测对比尚未在本次本地会话执行（`UNVERIFIED` / `missing evidence`）。

## 5. Verification and limits

- **已完成验证（`VERIFIED`）**：
  - `just ci`：4 步全通过（`test_skill_versions.py` 1 passed、`ruff` 全通过、`pyright` 0 errors、全仓 `pytest` 2967 passed）；
  - 双后端真实编译测试（`DEFENSE_COMPILE=1` + `DEFENSE_TYPST_COMPILE=1` + `pymupdf`）：`tests/skills/academic_defense_beamer` `268 passed, 0 skipped`（含 `test_defense_theme_assets.py` 双遍 `xelatex` 视口包含与像素防遮挡断言 `7 passed`）；
  - 文档同步与构建：`uv run python docs/scripts/check_resource_sync.py`（310 manifest entries passed）、`just doc-build`（VitePress 构建通过）、`git diff --check`（0 错误）；
  - 视觉预览与独立审计：`render_preview.py` 生成 15 页单页 PNG 与 `contact-sheet.png`，由 `Gemini 4 Hydrogen` 独立复核通过。
- **未验证边界（`UNVERIFIED` / `missing evidence`）**：
  - 真机物理双显示器下人工打开 `FerroStage` 或 `pympress` 放映 `defense-notes.pdf` 的交互体验（自动化测试已通过 PyMuPDF 核验页数、32:9 宽高比及 `notes:N` 页标签契约，真机窗口交互标 `UNVERIFIED`）；
  - 外部多模型 provider 端到端填写完整真实博士论文 `slide_plan.yaml` 的主观审美对比评测（标 `UNVERIFIED`）；
  - 未拉取源码的外部目录检索条目（`scientific-slides`、`open-design`）标 `missing evidence`。
- **主动排除的权限与动作**：
  - 严禁修改用户学位论文源仓库文件；
  - 构建脚本离线运行，严禁自动联网下载 Typst 包或外部图片；
  - 严禁编造或换算论文中不存在的实验指标，严禁承诺规避任何检测器；
  - 严禁直接推送默认分支或覆盖维护者无关配置。
