# 示例：40 分钟预答辩稿（完整一轮）

本示例以合成论文 `evals/fixtures/mini-thesis/`（交通流量预测，7 章）为对象。论文题目、姓名与数字均为合成内容。

## 用户请求

> 我的博士论文仓库在 `mini-thesis/`，帮我做一份 40 分钟的预答辩 Beamer 幻灯片，用燕山主题。输出放到 `defense-work/`。

## 1. 提取与检查点 1

```bash
uv run python -B $SKILL_DIR/scripts/extract_thesis.py --thesis mini-thesis --out defense-work/inventory.json --json
```

输出摘要（退出码 0）：章 7、图 17、表 5、公式 7、算法 1、成果 4、贡献 3、展望 2；告警 `W-MAIN`：
存在 `document.tex` 与 `document_blind.tex` 两个主文件候选，已选择正式版 `document.tex`。

向用户确认：

| 章  | 章题（节选）                         | 建议角色      |
| --- | ------------------------------------ | ------------- |
| 1   | 绪论                                 | `intro`       |
| 2   | ……理论基础与问题框架                 | `foundation`  |
| 3–5 | 三个研究章                           | `research`    |
| 6   | 交通流量预测平台设计与应用           | `application` |
| 7   | 总结与展望                           | `conclusion`  |

> 章角色如上，阶段预答辩，40 分钟，燕山主题，输出目录 `defense-work/`。确认后生成规划骨架。

## 2. 规划骨架与填写

```bash
uv run python -B $SKILL_DIR/scripts/plan_deck.py --inventory defense-work/inventory.json --out defense-work/slide_plan.yaml --minutes 40 --stage predefense --theme yanshan
```

输出：帧数 54，内容页数 45，占位符 279。LLM 按 `references/content-rules.md` 逐帧填写 `〔待填写〕`。一帧填写后的样子：

```yaml
- id: c3-problem
  role: problem
  layout: figure-bullets
  chapter: 3
  section: 3.2 问题描述
  takeaway: 缺失观测在时间和空间上都不规则
  bullets:
    - 缺失位置不固定，传统插值难以利用**空间相关性**
  figures:
    - label: fig:c3-missing
  notes:
    say: 图3-2给出了示例检测器的缺失模式。缺失在时间和空间上都不规则……（150–250 字）
    key: 缺失模式不规则
    transition: 下面介绍时空图构建。
    questions:
      - 缺失率多高时方法失效？
```

填写要点：结论句不超过 40 字且不重复帧标题；数字只抄论文；文字字段不写 `$…$` 或 LaTeX 命令；
创新点逐条取自结论章并注明章号。

## 3. 串读与检查点 2

```bash
uv run python -B $SKILL_DIR/scripts/plan_deck.py --plan defense-work/slide_plan.yaml --outline
```

```text
13  c3-intro  3.1 引言 | 本章通过时空图卷积补全稀疏观测
14  c3-problem  3.2 问题描述 | 缺失观测在时间和空间上都不规则
15  c3-method-1  3.3 时空图卷积补全模型 | 以距离高斯核构建时空图的邻接矩阵
……
帧数 54，内容页数 45，占位符 0
```

> 请按页序读一遍结论句，确认主线后我再构建。

## 4. 构建、检查与修复

```bash
uv run python -B $SKILL_DIR/scripts/build_deck.py --plan defense-work/slide_plan.yaml --inventory defense-work/inventory.json --out defense-work/deck --compile
uv run python -B $SKILL_DIR/scripts/check_deck.py --deck defense-work/deck/defense.tex --inventory defense-work/inventory.json --plan defense-work/slide_plan.yaml
```

第一轮检查常见结果是讲稿偏短（输出节选，行号与计数随规划变化）：

```text
% D-NOTES (frame=c3-intro, notes.md:<行>) [Severity: Minor] [Priority: P2]: [Script] 「说什么」115 字，内容页应为 150–250 字
% 汇总：Critical 0，Major 0，Minor <n>，Info 0；skipped：无
```

补写讲稿（只用论文事实），`build_deck.py --force --compile` 重建后再检查，直到 Critical 与 Major 为 0；最多 3 轮。

## 5. 预览与检查点 3

```bash
uv run python -B $SKILL_DIR/scripts/render_preview.py --pdf defense-work/deck/defense.pdf --out defense-work/deck/preview
```

逐页看 `contact-sheet.png`：章前目录高亮当前章；子图网格三幅子图都显示；强调色每页不超过 3 处；页脚不遮挡正文。

交付说明示例：

> 答辩稿 54 页，编译通过；质量门 Critical 0、Major 0、Minor 0。需要您确认：封面上的导师职称与答辩日期；
> 第 6 章应用效果页的数字与论文表6-1一致。讲稿在 `defense-work/deck/notes.md`。
