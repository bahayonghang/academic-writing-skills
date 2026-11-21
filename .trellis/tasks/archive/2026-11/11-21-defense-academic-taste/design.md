# 技术设计：academic-defense-beamer 学术品味与结构化版式升级

本设计对应用户已确认的方案 A（D1–D3），并将所有改动锁定到具体文件与代码位置。

---

## 1. 阶段划分与白名单文件归属

按 P1 → P2 → P3 顺序推进，每阶段均可独立运行单测验证：

### P1：Beamer 现代学术视觉体系升级
| 文件 | 具体改动 |
| :--- | :--- |
| `templates/beamer/defense-layouts.sty` | 新增 `defenseTint`/`defenseLine`/`defenseMuted` 三色定义；升级页眉 `frametitle`（章节面包屑 + 主标题 + 底细灰线配短砖红条）；`\DefenseHighlight` 保持 `defenseRed` 粗体并新增 `\DefenseTerm`（`defenseNavy` 粗体）、`\DefenseLead`（圆角浅蓝底深蓝字维度签）、`\DefenseGridCard`（多列等宽标题签卡片）、`\DefenseKPI`（顶部 `2.5pt` 深蓝粗线指标块）；升级 `\DefenseTakeaway`（按页角色区分问题红签/结论深蓝签浅底收束条）、`\DefenseFigure`（细灰衬底面板 + `defenseMuted` 题注）、`\DefensePaperBox`（左深蓝签 + `defenseTint` 浅底卡）及封面/目录/致谢层次 |
| `templates/beamer/beamerthemeYanshanDefense.sty` | `defenseRed` 由 `FF0000` 更新为 `B42318`，补齐 `defenseTint` (`F2F4F9`)、`defenseLine` (`D9DCE5`)、`defenseMuted` (`5A6072`) |
| `templates/beamer/beamerthemeGenericDefense.sty` | `defenseRed` 更新为 `A93226`，补齐 `defenseTint` (`F4F6F9`)、`defenseLine` (`D5DCE4`)、`defenseMuted` (`5D6773`) |
| `templates/beamer/demo-deck.tex` | 展示升级后的双层强调、`短签｜正文`、2×2 卡片宫格与 `\DefenseKPI` 宏，确保 12 个 `% layout:` 标记完整保留 |
| `references/visual-spec.md`、`tests/skills/academic_defense_beamer/test_defense_theme_assets.py` | 同步颜色表与 `LAYOUT_API` 集合，保持 `test_demo_deck_compiles` 零纵向溢出 |

### P2：双后端结构化微排版与可选规划字段
| 文件 | 具体改动 |
| :--- | :--- |
| `scripts/build_deck.py` | `tex_escape`（L185）同时解析 `**词**`（`\DefenseHighlight`）与 `*词*`（`\DefenseTerm`，备注模式均映射 `\textbf`）；`item_text`（L200）识别 `2–8 字前缀｜正文` 输出 `\DefenseLead{短签} 正文`；`validate_frame`（L280）校验可选字段 `columns`（`cards` 帧 `1/2/3`）、`metrics`（至多 3 项 `{label, value, basis, key?}`）、`highlight_rows`（`table` 帧非负整数列表）；`frame_context`（L471）与 `typst_frame_context`（L886）注入渲染上下文（`cards` 帧缺省 `len(bullets)==4` 时 `columns=2`，其余 `1`） |
| `scripts/typst_backend.py` | `ty_text`（L100）解析 `**词**` → `#key("…")`、`*词*` → `#hl("…")`（`emphasis="strong"` 时二者均输出 `#strong("…")`）；新增 `ty_bullet` 支持 `短签｜正文` 输出 `[#tag("短签")#h(0.45em)#…]`（使用 `tag` 默认 `kind: "navy"`，不输出 `"navy"` 字符串字面量，防止污染 `check_typst.visible_lines`）；新增 `ty_metric` 构造 `#kpi(...)` 参数 |
| `templates/jinja/frames/{bullets,figure-bullets,equations-figure,paper-summary,cards,figure,figure-grid,table}.tex.j2` | `cards.tex.j2` 支持 `columns` 1/2/3 网格（用 `\begingroup...\endgroup` 包裹 `minipage`，严禁紧跟 `\begin{frame}{title}` 写裸 `{...}`）；内容帧支持可选 `metrics` 行 |
| `templates/typst/frames/{cards,table,bullets,figure-bullets,equations-figure,paper-summary,figure,figure-grid}.typ.j2` | `cards.typ.j2` 在 `columns > 1` 时渲染 `#grid(columns: k, gutter: 0.35cm)` + `#title-box(title: ...)[...]`，单列保持 `#side-card`；`table.typ.j2` 在有 `highlight_rows` 时输出 `mark: (0, ...)`；内容帧支持可选 `#grid` + `#kpi(...)` |
| `tests/skills/academic_defense_beamer/{test_defense_build,test_defense_typst_backend,test_defense_build_typst}.py` | 更新 Touying `**词**` → `#key` 断言（`test_defense_typst_backend.py:28-29`、`test_defense_build_typst.py:81`），新增 `*词*`、`短签｜正文`、`columns`、`metrics`、`highlight_rows` 与特殊字符转义测试 |

### P3：质量门、文案规范、双语镜像与交付证据
| 文件 | 具体改动 |
| :--- | :--- |
| `scripts/check_deck.py`、`scripts/check_typst.py` | `check_deck.py:192` 的 `COUNT_RES["card"]` 覆盖 `\Defense(?:Grid)?Card`；`check_deck.py:1402` 的 Touying `"card"` 同时统计 `side-card` 与 `title-box`（保证 `D-CHAIN` L971 与 `D-DENSITY` L1413 准确）；`HIDDEN_ARGS` 对新增非正文参数（如有）精确排除，确保 `\DefenseKPI` 的 `label`/`value`/`basis` 保留为可见文本以接受 `D-NUM-SRC` 核验；`check_density` / `check_density_typst` 新增单帧砖红强调（`\DefenseHighlight` / `#key`）> 3 处报 `D-DENSITY` Minor |
| `tests/skills/academic_defense_beamer/{test_defense_check,test_defense_check_typst}.py` | 新增单帧强调 > 3 处、多列卡片 `D-CHAIN`、`metrics` 触发 `D-NUM-SRC`、Touying `mark:` 不触发 `D-TAB-SRC` 的正反例测试 |
| `references/{content-rules,slide-layouts,plan-schema,quality-gate,touying-backend}.md`、`examples/*.md`、`SKILL.md` | 补齐短语化断言与禁套话/禁漏译外文守则，同步新可选字段、宏表、组件映射与 `D-DENSITY` 判据，更新 `SKILL.md` 的 `last_updated` |
| `.trellis/spec/academic-writing-skills/defense-deck-contract.md`、`README.md`、`README_CN.md`、`docs/**`、`docs/resource-manifest.json` | 更新跨脚本契约说明，同步中英文文档站镜像并重算资源散列 |

---

## 2. 关键不变量与边缘情况核对

1. **`check_typst.visible_lines` 字面量洁净性（`scripts/check_typst.py:389`）**：
   - `visible_lines` 扫描帧内所有非隐藏行的 `"..."` 字符串字面量。因此 Touying 渲染短签用 `#tag("短签")`（依赖 `simply-ysu-touying` 默认 `kind: "navy"`），`#kpi` 的 `size`/`key` 只传标识符与字面布尔/长度，绝不写入非正文配置字符串（如 `"navy"`），保证可见字数与 `D-NUM-SRC` 100% 精确。
2. **`check_typst.tables` 单元格提取零干扰（`scripts/check_typst.py:458`）**：
   - `tables()` 通过扫描 `result-table(...)` 内的顶层 `[...]` 提取单元格文本。`mark: (0, 2)` 仅含圆括号与整数，不含 `[...]`，故 `D-TAB-SRC` 逐格比对完全不受影响。
3. **星号解析优先级与未配对回退**：
   - 正则按 `\*\*(.+?)\*\*|\*(?!\*)(.+?)(?<!\*)\*` 单趟扫描：先匹配双星号 `**...**`，再匹配不相邻星号的单星号 `*...*`；未闭合的孤立 `*` 或 `**` 原样走普通字符转义（保持 `test_defense_build.py:83` `escape("**a** 与 **b") == "\\DefenseHighlight{a} 与 **b"` 完全兼容）。
4. **向后兼容**：
   - 既有测试 fixture 的 `slide_plan.yaml` 若含 3 个研究章（`challenges`/`innovation` 卡片数为 3），默认 `columns=1`，输出结构与旧版一致，既有单测无需为无关用例改快照；4 个研究章时默认 `columns=2` 自动呈现 `2×2` 宫格，且可显式设 `columns: 1` 覆盖。
