# 研究：先例调研、泛化门禁与差距矩阵（案例特质 × 技能现状 × 判定）

日期：2026-11-21。本文件遵循 `qiaomu-meta-skill` 的内置双目录先例检索与泛化门禁（Generalization Gate），并对照 `academic-defense-beamer` 现有实现与契约给出逐项取舍。

---

## 1. 仓库基线核对（`academic-writing-skills/academic-defense-beamer` v6.0.0）

- **流水线与契约**：`extract_thesis.py` → `plan_deck.py` → `build_deck.py` → `check_deck.py`（固定 22 个 `D-*` 码）→ `render_preview.py`，跨脚本接口由 `.trellis/spec/academic-writing-skills/defense-deck-contract.md` 锁定。
- **双后端视觉代差（核心现状事实）**：
  1. **Touying 后端**导入 `@preview/simply-ysu-touying:0.2.0`。实测核对本机已安装主题包的公开 API（`themes/tokens.typ`、`themes/components.typ`、`themes/ysu-beamer.typ`）：主题已经是现代 v3 设计——采用深海蓝 `ysu-navy (#1F296A)`、沉稳砖红 `ysu-red (#B42318)`、浅灰蓝块面 `ysu-tint (#F2F4F9)`、柔和细线 `ysu-line (#D9DCE5)`、次级灰 `ysu-muted (#5A6072)`；页眉将 `#takeaway` 作为首屏粗体主标题（Assertion-Evidence 顶栏导语），并公开提供 `hl`（深蓝粗体）、`key`（砖红粗体）、`conclude`（深蓝通栏收束带）、`red-frame`（红框问题签）、`title-box`、`group-box`、`card`、`side-card`、`label-row`、`points`（`01/02` 编号要点）、`kpi`（顶部粗线关键指标块）、`figure-box`、`result-table(mark:)` 等 30 个组件。**但当前 `templates/typst/frames/*.typ.j2` 仅使用了其中最基础的子集**（未用 `kpi`、`title-box` 多列网格、`key`、`red-frame`、`conclude`、`result-table(mark:)`）。
  2. **Beamer 后端**（`defense-layouts.sty` + `beamerthemeYanshanDefense.sty` / `beamerthemeGenericDefense.sty`）仍停留在早期复刻某份旧预答辩 pptx 的第 1 代样式：`yanshan` 的 `defenseRed` 为刺眼纯红 `#FF0000`；所有 `**词**` 一律渲染为 `#FF0000` 红粗体；页眉是旧式双横线居中节题，结论句 `\DefenseTakeaway` 每页机械塞在底部细红线框内；无浅色块面衬底（`tint`），`cards` 只能单列全宽竖排，`bullets` 只是裸圆点列表，图片裸贴白底。
- **`qiaomu-meta-skill` 结构基线核对**：运行 `validate_skill.py` 显示本仓库采用多技能统一目录约定（`agents/openai.yaml`、`evals/trigger_eval.json`、顶层 `README.md`/`README_CN.md` 与 `docs/skills/academic-defense-beamer/` 双语镜像），不在子技能根下重复放置独立仓库用的 `README.md`、`agents/interface.yaml` 与 `manifest.json`；许可证保持仓库统一的 `PolyForm Noncommercial 1.0.0`，版本号保持 `6.0.0`（与 `10-15-thesis-zh-rebuttal-correction` 先例一致）。

---

## 2. 内置双目录先例检索（2026-11-21）

遵循 `qiaomu-meta-skill` 指标分离原则：`skills.sh` 的 `installs` 为安装采用量，`SkillsMP` 的 `repo_stars` 为源仓库 GitHub 星标，均不代表质量评分。

| 来源目录 | 查询词 | 命中候选 | 指标（严格分离） | 评注与采纳边界 |
| :--- | :--- | :--- | :--- | :--- |
| `skills.sh` | `beamer defense` | `bahayonghang/academic-writing-skills@academic-defense-beamer`（含旧名 `latex-defense-zh`） | `69 installs`（旧名 `116 installs`）；`rating evidence unavailable` | 本技能自身，唯一覆盖中文学位论文 LaTeX 源只读提取 + Beamer/Touying 双后端 + 22 码保真门禁的包 |
| `skills.sh` | `beamer defense` | `k-dense-ai/scientific-agent-skills@scientific-slides`（及 `jaechang-hits`、`alterlab-ieu` 同族派生） | `2.5K installs`；`rating evidence unavailable` | 通用科研幻灯片技能；未在本次会话拉取外部源码（记 `missing evidence`），仅确认定位为通用英文学术报告而非中文学位论文源保真流水线 |
| `SkillsMP` | `academic presentation` | `nexu-io/open-design` 下 `hps-academic-paper`、`kami-deck`、`html-ppt-zhangzara-*` | `108,512 repo_stars`；`rating evidence unavailable` | HTML 演示模板家族（非 Beamer/Touying），其描述强调「decision-grade academic deck: field map, gap, evidence, caveats」的断言驱动叙事；未检视外部源码，记 `missing evidence` |
| 本机已检视锚点 | 本地主题与既有署名源 | `@preview/simply-ysu-touying:0.2.0`、`claude-skill-academic-ppt`（MIT）、`thesis-defense-pptx-skill`（Apache-2.0） | 本机包缓存已核验源码 | `simply-ysu-touying:0.2.0` 已具备完整现代学术色阶与组件原语，可直接作为 Beamer 升级与双后端对齐的权威公开基准 |

---

## 3. 泛化门禁（Generalization Gate）与差距矩阵（G1–G12）

先区分**体裁差异**：微信案例属于「科技奖申报答辩 PPT」，而 `academic-defense-beamer` 服务于「中文硕博学位论文预答辩/答辩」。凡违反学位论文体裁或学术事实保护红线（`D-FIG-ALLOW`、`D-EQ-SRC`、`D-TAB-SRC`、`D-NUM-SRC`）的要素一律**否决**；跨学科通用的视觉层级、容器布局与精炼表达机制予以**采纳或改编**。

判定取值：**采纳** / **改编** / **已覆盖** / **否决**。

| 编号 | 案例特质（领域中立表述） | 仓库现状 | 判定 | 落点与机制映射 |
| :--- | :--- | :--- | :--- | :--- |
| **G1** | **沉稳学术色阶与浅色块面（Surface Tint）**：用极浅灰蓝块面与细灰线替代纯白裸排和刺眼纯红 `#FF0000` | Touying 已是 `#1F296A` + 砖红 `#B42318` + 浅底 `#F2F4F9`；Beamer `yanshan` 仍用 `#FF0000` 且无 `tint`/`line`/`muted` 语义色 | **采纳** | Beamer 新增浅底/细线/次级灰色阶并将强调红校准为沉稳砖红（或提供现代色阶并同步 `visual-spec.md` 与主题单测），消除荧光红廉价感 |
| **G2** | **双层克制强调**：普通结构术语用深蓝/深色加粗，仅核心瓶颈或突破指标用砖红（每页 ≤ 3 处），且双后端语义一致 | Beamer 把所有 `**词**` 染成红粗体；Touying 把 `**词**` 映射为 `#hl`（深蓝粗体，无法标红关键结论）；`check_deck.py` 未检查每页强调上限 | **改编** | 对齐双后端强调语法（区分深蓝结构加粗与砖红关键强调，或明确唯一标记与标签分工），并在 `D-DENSITY` 中实装「单页红字强调 > 3 处报 Minor」 |
| **G3** | **首屏断言导语（Assertion Lead）与页眉现代层级**：视线首落点先给核心结论/定位句，而非把唯一结论句藏在页底 | Touying 已把 `#takeaway` 升至页眉主标题（上方配章节面包屑与底红短横线）；Beamer 仍是旧式双横线节题 + 页底细红框 | **采纳** | 升级 Beamer 页眉与导语/收束视觉骨架，向现代学术风（章节面包屑 + 醒目主标题/首屏导语条）对齐，告别旧式页页底部套细红框 |
| **G4** | **底栏按需收束与「关键科学问题」签条分化**：问题页用红签问题框，总结页用深蓝收束带，矩阵/大图页不堆叠双倍底栏 | Beamer 所有 `takeaway` 一律同款细红线框；Touying 有 `conclude` 与 `red-frame` 组件但模板未调用 | **改编** | 按页角色语义分化收束组件（例如 `problem`/`challenges` 可用科学问题警示框，小结/实验页可用深蓝收束条，首屏已有结论主标题时不重复堆砌同文底框） |
| **G5** | **多列/宫格卡片矩阵（2×2 Grid / 3-Column Pillars）**：3–4 个问题、创新点或并列模块采用二维网格，充分利用 16:9 横向空间 | `cards` 版式在 Beamer 与 Touying 中均为全宽单列竖向堆叠，3–4 张卡时扁长单调 | **采纳** | 扩展 `cards`（或支持 `columns: 1|2|3` 可选布局参数）：4 项默认/可选 2×2 矩阵，3 项可选三联等宽立柱（Touying 映射 `grid` + `title-box`/`side-card`，Beamer 升级 `\DefenseCard` 网格宏） |
| **G6** | **「维度短签｜精炼短语」微排版消灭裸圆点墙**：列表项带 2–4 字色块/胶囊维度签，形成左侧整齐视觉锚列 | `bullets` 与 `figure-bullets` 仅输出普通圆点或纯序号，文字易写成 35 字散文段落 | **采纳** | 支持要点文本中的结构化短签语法（如 `维度签｜核心短句` 或对象字段，向后兼容纯字符串列表）：渲染为色块标签 + 对齐短句；无短签时使用现代编号要点（`01/02`） |
| **G7** | **论文源保真 KPI 关键指标块**：实验核心提升指标独立成带对照基准的醒目数字块 | Touying 组件库已有 `#kpi(label:, value:, basis:, key:)`，但规划 schema 与 Beamer 均未接入 | **采纳** | 在规划帧增加可选 `metrics` 列表（每项含 `label`、`value`、`basis`），双后端分别渲染 `\DefenseKPI` 与 `#kpi`，且全部数值严格纳入 `D-NUM-SRC` 核验与可见字符统计 |
| **G8** | **图文同构面板化与结果表高亮**：图片置于柔和边框衬底容器、题注次级灰且图号加粗；表格突出本文方法行 | Beamer 图片裸放、题注纯黑无区分；Touying `result-table` 支持 `mark: ()` 参数但构建脚本未透传 | **改编** | Beamer `\DefenseFigure` 增加细灰衬底框与灰字题注美学优化；规划 `table` 帧支持可选 `highlight_rows`（Touying 传 `mark`，Beamer 保持 `DefenseSource` 内表体逐字不变以确保 `D-TAB-SRC` 100% 零回归） |
| **G9** | **短语化断言文风与去 AI 套话规范（含禁中英夹杂漏译词）** | `content-rules.md` 仅有字数上限（40 字/条、180 字/页），无句式结构、禁水词与禁外文残留规则 | **采纳** | 在 `references/content-rules.md` 增补「断言化结论句、短签+动宾短语、禁空洞评价套话、禁非专业术语的中英夹杂词（反例警示）」细则 |
| **G10** | **庄重层次感封面与致谢页** | Beamer 封面为纯平涂矩形色带 + 裸四行表 | **改编** | 在不引入外部位图的前提下，优化 Beamer 封面/目录/致谢的留白比例、标题背板层次、汇报人胶囊签与信息栏排版质感 |
| **G11** | **手工重绘工艺流程图、商业实景照片（储氢罐/公交/轮船）、获奖证书与专利扫描墙** | `D-FIG-ALLOW` 严格禁止清单外图片，且明确不生成新图、不重绘数据图 | **否决** | 违反学位论文事实保真红线；学位论文答辩只允许引用论文仓库清单内的原图 |
| **G12** | **科技奖「经济社会效益」套路页与「去 AI 检测」规避承诺** | 学位论文答辩框架为「绪论—基础—研究章—应用—创新点与展望（+攻读学位成果）」，且仓库严禁承诺规避检测器 | **否决** | 体裁不符且触碰合规边界；只吸收其高可读性的信息组织与精炼文风，绝不引入科技奖效益套话或任何检测规避表述 |
