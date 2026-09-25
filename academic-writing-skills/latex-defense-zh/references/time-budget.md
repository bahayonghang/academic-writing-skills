# 时长预算

本文件规定汇报分钟数与页数、每页秒数之间的换算。默认汇报时长为 40 分钟（2400 秒）。规划脚本与质量门使用同一套公式。页角色见 [答辩稿框架](defense-framework.md)。

## 口径

- 内容页：除 `cover`、总目录、章前目录、`thanks` 与 `backup` 以外的页。
- 全稿帧数 = 内容页数 + 章数 + 2（封面、总目录、各章前目录与致谢页）。
- 适用范围：15–90 分钟；至少一个 `research` 章；第 1 章为 `intro`，最后一章为 `conclusion`。

## 40 分钟分配

页角色分为两类：

- 固定 1 页的角色：`challenges`、`organization`、研究章的 `intro`、`problem`、`summary`、应用章的 `intro`、`innovation`、`outlook`、`achievements`。
- 按时长缩放的角色（括号内为 40 分钟基数）：`background`（2）、`status`（2）、`foundation`（3）、`architecture`（1）、`application`（2）。

| 段               | 页角色 × 页数 × 每页秒数（40 分钟）                                              | 小计（秒）              |
| ---------------- | -------------------------------------------------------------------------------- | ----------------------- |
| 固定段           | `cover` 1 × 30；总目录 1 × 20；章前目录（章数 − 1）× 8；`thanks` 1 × 10          | 108（7 章），不缩放     |
| `intro` 章       | `background` 2 × 50；`status` 2 × 50；`challenges` 1 × 50；`organization` 1 × 50 | 300                     |
| `foundation` 章  | `foundation` 3 × 50                                                              | 150                     |
| `application` 章 | `intro` 1 × 40；`architecture` 1 × 50；`application` 2 × 45                      | 180                     |
| `conclusion` 章  | `innovation` 1 × 90；`outlook` 1 × 45；defense 阶段另加 `achievements` 1 × 45    | 135（defense 阶段 180） |
| `research` 章    | 余量 R 平均分给各研究章，见下文公式                                              | 1527（3 个研究章）      |

## 公式

记汇报时长为 M 分钟，k = M / 40，r(x) = ⌊x + 0.5⌋（逢 0.5 进位）。

1. 缩放角色页数 = max(1, r(基数 × k))。
2. `intro`、`foundation`、`application`、`conclusion` 各段秒数 = 该段 40 分钟小计 × k。固定段不缩放。
3. 余量 R = 60M − 固定段秒数 − 第 2 步各段秒数之和。
4. 每个研究章的时长 T = R / 研究章数；页数 n = max(6, r(T / 53))。
5. 研究章内 `intro`、`problem`、`summary` 各 1 页；`method` 页数 = max(2, r((n − 3) × 3 / 7))；`experiment` 页数 = max(1, n − 3 − `method` 页数)。
6. 每页秒数：非研究章各段取 r(段秒数 / 段页数)；研究章取 r(T / n)；固定段各页取上表的值。
7. 内容页数为 N 时，质量门接受的内容页区间为 [r(0.85N), r(1.15N)]。

各页秒数之和应接近 60M。质量门在偏差超过 10% 时提示。

## 参考值

章结构：`intro`、`foundation`、3 个 `research`、`application`、`conclusion`，共 7 章；阶段为 predefense。

| 时长 M（分钟） | 每个研究章页数 n（method/experiment） | 内容页数 N | 内容页区间 | 全稿帧数 |
| -------------- | ------------------------------------- | ---------- | ---------- | -------- |
| 30             | 7（2/2）                              | 35         | [30, 40]   | 44       |
| 40             | 10（3/4）                             | 45         | [38, 52]   | 54       |
| 60             | 15（5/7）                             | 66         | [56, 76]   | 75       |

另两种情况的 40 分钟取值：

- 4 个研究章、无基础章（共 7 章）：每个研究章 8 页，N = 44。
- 默认 7 章结构、defense 阶段：每个研究章 9 页，N = 43。

## 计算示例

40 分钟、默认 7 章结构、predefense 阶段：

1. k = 1。固定段 108 秒；`intro` 章 300 秒、`foundation` 章 150 秒、`application` 章 180 秒、`conclusion` 章 135 秒，合计 765 秒。
2. R = 2400 − 108 − 765 = 1527 秒；T = 1527 / 3 = 509 秒；n = max(6, r(509 / 53)) = r(9.60) = 10。
3. `method` = max(2, r(7 × 3 / 7)) = 3；`experiment` = 10 − 3 − 3 = 4。研究章每页 r(509 / 10) = 51 秒。
4. N = 6（`intro` 章）+ 3（`foundation` 章）+ 30（研究章）+ 4（`application` 章）+ 2（`conclusion` 章）= 45；区间 [38, 52]；全稿帧数 = 45 + 7 + 2 = 54。
