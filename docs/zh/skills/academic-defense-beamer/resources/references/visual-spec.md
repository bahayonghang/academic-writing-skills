# 视觉规格

本文件给出 `yanshan` 与 `generic` 两个主题的颜色、版位、字号层级、字体回退和校徽规则。`yanshan` 主题采用与 Touying 后端（`simply-ysu-touying`）同源的现代深海蓝、沉稳砖红与浅灰蓝块面体系；`generic` 主题使用相同版位和中性学院配色，不显示校徽。主题文件为 `templates/beamer/beamerthemeYanshanDefense.sty` 与 `templates/beamer/beamerthemeGenericDefense.sty`，共用宏包为 `templates/beamer/defense-layouts.sty`。

## 页面

- 文档类：`\documentclass[aspectratio=169,11pt]{ctexbeamer}`，页面 16 cm × 9 cm。
- 左右文字边距各 1 cm；页脚预留 0.3 cm；帧内容顶端对齐。
- 不显示 Beamer 导航符号；正文采用柔和深色墨阶（`black!88!defenseNavy`），普通列表项采用圆角小方块符号。

## 颜色

| 颜色名           | `yanshan` | `generic` | 用途                                                     |
| ---------------- | --------- | --------- | -------------------------------------------------------- |
| `defenseNavy`    | `#1F296A` | `#1F3A5F` | 封面基座与题牌顶边、帧标题、结构术语加粗、指标块顶边     |
| `defenseBlue`    | `#2F5597` | `#2E5E8C` | 页码平行四边形渐变终点                                   |
| `defenseAccent`  | `#2F5597` | `#2E5E8C` | 小节条竖标、列表符号、单列卡片左侧边条、封面基座顶边     |
| `defenseBoxHead` | `#1F296A` | `#1F3A5F` | 框标题底色、单列与多列卡片标题栏底色                     |
| `defensePaper`   | `#162052` | `#182D4A` | 「论文」框左侧标签底色、封面基座渐变终点                 |
| `defenseRed`     | `#B42318` | `#A93226` | 关键结论强调词（`**…**`）、页眉锚点横条、结论收束条边标 |
| `defenseTint`    | `#F2F4F9` | `#F4F6F9` | 卡片、结论收束条、维度短签、指标块与「论文」框的浅色衬底 |
| `defenseLine`    | `#D9DCE5` | `#D5DCE4` | 页眉分隔细线、图片衬底框、卡片与收束条柔和细边框         |
| `defenseMuted`   | `#5A6072` | `#5D6773` | 图表题注、目录序号签、指标块名称与对照基准文字           |

目录当前章：两个主题均以 `defenseTint` 浅底条配左侧 `defenseRed` 竖标与 `defenseNavy` 粗体突出当前章。

## 换算与字号下限

页面宽 16 cm（对应 16:9 宽屏 pptx 33.867 cm × 19.05 cm，缩放系数 0.4724）。Beamer 正文 11 pt 等效于 pptx 中的 23.3 pt。本技能取 Beamer 文字下限 8 pt（`\scriptsize`），推荐正文 `\small`（10 pt）。

## 版位

坐标原点在页面左上角，单位为 cm。内容区严格对齐左右 1.0 cm 网格（x = 1.0 cm 至 15.0 cm）。

| 元素             | Beamer 实现                                                    | 字号                        |
| ---------------- | -------------------------------------------------------------- | --------------------------- |
| 帧标题           | 左对齐于 (1.0, 0.42)，高 0.80                                  | `\Large` 粗体 `defenseNavy` |
| 页眉分隔线与红标 | 细线 (1.0, 0.77)–(15.0, 0.77)，左侧红标宽 0.95                 | 无                          |
| 内容页校徽       | 右对齐于 (14.12, 0.42)，高 0.52                                | 无                          |
| 页码平行四边形   | (14.30, 0.21)–(15.00, 0.63)，深蓝渐变                          | 页码 `\scriptsize` 粗体白字 |
| 小节条           | 正文首行左边距处，左侧圆角竖标 0.12 × 0.36                     | `\normalsize` 粗体          |
| 封面阶段胶囊     | 右对齐于 (15.0, 0.92)，`defenseTint` 衬底                      | `\small` 粗体               |
| 封面校徽         | (1.0, 0.48)，高 0.92                                           | 无                          |
| 封面悬浮题牌     | (1.0, 1.70)–(15.0, 5.00)，白底细框带微阴影与顶边双色条         | `\huge` 粗体 `defenseNavy`  |
| 封面深蓝基座     | (0, 5.75)–(16.0, 9.00)，分界线居中骑跨白底胶囊「汇报人」       | 信息栏 `\small`             |
| 目录页           | 左侧 0.32 宽深蓝边带，顶栏「目录 / CONTENTS」，章行带两位序号签 | `\normalsize`               |

- 帧标题区总高 0.80 cm。帧标题宽度不超过约 11.5 cm；节题更长时优先取论文目录中的短题。

## 字号层级

| 层级                           | Beamer 实现               |
| ------------------------------ | ------------------------- |
| 目录页主标题                   | `\Huge` 粗体（24.88 pt）  |
| 封面题牌、致谢页主句           | `\huge` 粗体（20.74 pt）  |
| 帧标题                         | `\Large` 粗体（14.4 pt）  |
| 小节条、目录行、骑跨汇报人胶囊 | `\normalsize`（10.95 pt） |
| 正文、要点、单列卡片、结论收束 | `\small`（10 pt）         |
| 维度短签、多列宫格卡、题注     | `\footnotesize`（9 pt）   |
| 指标块基准说明、文字下限       | `\scriptsize`（8 pt）     |

双层强调规则：`**关键结论词**` 渲染为 `defenseRed` 粗体（`\DefenseHighlight`，每页不超过 3 处）；`*结构术语*` 渲染为 `defenseNavy` 粗体（`\DefenseTerm`）。

## 字体回退

| 类别 | 依次尝试                                         |
| ---- | ------------------------------------------------ |
| 中文 | Microsoft YaHei → Source Han Sans SC → FandolHei |
| 西文 | Arial → TeX Gyre Heros                           |

宏包用 `\IfFontExistsTF` 按顺序选择第一个可用字体。FandolHei 与 TeX Gyre Heros 随 TeX Live 提供。

## 校徽

- 校徽文件从论文仓库读取，路径写入 `\DefenseSetup{logo=<path>}`。技能包不含校徽文件。
- 内容页校徽高 0.52 cm，封面与致谢页校徽高 0.92 cm，宽度按原图比例。
- `yanshan` 主题：校徽路径为空或文件不存在时，显示文字标识，默认「燕山大学」，粗体，颜色 `defenseNavy`。`\DefenseSetup{logo-text=<文字>}` 可以修改文字标识。
- `generic` 主题：不显示校徽，也不显示文字标识。

## Touying 后端

- Touying 后端的颜色、版位、字号、字体回退与校标全部来自已安装的主题包 simply-ysu-touying，本技能不定义，也不复制主题源码与校标位图。本文件上述版位只适用于 Beamer 主题，色阶与双层强调语义与 simply-ysu-touying 对齐。
- 页面为 16:9（16 cm × 9 cm）；备注版的备注页为 16 cm × 13.5 cm，见 [放映与演讲备注](presenting.md)。
- 构建脚本只设置 `aspect-ratio: "16-9"`、`nav-labels` 与 `config-info`，不传颜色、字体或 `icon:` 参数。图的默认高度见 [Typst Touying 后端](touying-backend.md) 的版式映射。
- 只有 `yanshan` 一个主题；`generic` 主题只用于 Beamer 后端。
