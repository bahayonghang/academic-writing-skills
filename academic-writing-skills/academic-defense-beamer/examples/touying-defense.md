# 示例：Typst Touying 预答辩稿与 FerroStage 备注

本示例以合成论文 `evals/fixtures/mini-thesis/`（交通流量预测，7 章）为对象，用 Touying 后端生成答辩稿。论文题目、姓名与数字均为合成内容。提取与填写规划的步骤同 [40 分钟预答辩稿](predefense-40min.md)，本示例只写 Touying 后端的不同之处。

## 用户请求

> 论文仓库在 `mini-thesis/`。预答辩 40 分钟，想用 Typst Touying 和 simply-ysu-touying 主题做答辩稿，放映时要能在 FerroStage 里看到备注。输出放到 `defense-work/`。

## 1. 依赖检查

先确认本机有 Typst 0.15.1 或更高版本，并已缓存三个 Typst 包（安装方法见 [Typst Touying 后端](../references/touying-backend.md)）：

| 依赖     | 规格                                |
| -------- | ----------------------------------- |
| 主题包   | `@preview/simply-ysu-touying:0.2.0` |
| Touying  | `@preview/touying:0.8.0`            |
| mitex    | `@preview/mitex:0.2.6`              |

论文的图须为 PDF、PNG、JPG 或 SVG；EPS 图不能用于 Touying 后端。

## 2. 规划骨架

提取清单后（检查点 1 同 Beamer 流程），生成 Touying 规划：

```bash
uv run python -B $SKILL_DIR/scripts/plan_deck.py --inventory defense-work/inventory.json --out defense-work/slide_plan.yaml --minutes 40 --stage predefense --theme yanshan --backend touying
```

输出摘要：

```text
已写入 defense-work/slide_plan.yaml：帧数 54，内容页数 45，占位符 279
  提示（c2-toc）：Touying 页脚导航：章题超过 6 字，nav_label 暂写「第2章」；建议改成不超过 6 字的短名
  提示（c3-toc）：Touying 页脚导航：章题超过 6 字，nav_label 暂写「第3章」；建议改成不超过 6 字的短名
  ……
```

规划顶层多出 `deck.backend: touying`，每章多出 `nav_label`。把过长的章题改成短名，例如：

```yaml
meta:
  chapters:
    - number: 3
      title: 基于时空图卷积的流量补全方法研究
      role: research
      nav_label: 流量补全
deck:
  backend: touying
```

短名只用于页脚导航栏，不改目录页与章扉页中的章题，也不改论文内容。其余字段按 `references/content-rules.md` 填写，写法与 Beamer 规划相同。规划中以「Touying」开头的提示（EPS 图、复杂表、不能翻译的宏）须在构建前处理：换图表或版式，或改用 Beamer 后端。

## 3. 串读与构建

`--outline` 串读、检查点 2 同 Beamer 流程。确认后构建并编译：

```bash
uv run python -B $SKILL_DIR/scripts/build_deck.py --plan defense-work/slide_plan.yaml --inventory defense-work/inventory.json --out defense-work/deck --compile
```

输出目录 `defense-work/deck/` 中有 `defense.typ`、`notes.md`、`build_manifest.json`、`img/`（规划引用的论文原图副本）、`defense.pdf`、`defense-notes.pdf` 与 `defense.log`。

缺少 Typst 包时，构建脚本已写出 `defense.typ`，但不调用 typst，退出 6：

```text
错误：以下 Typst 包未安装在本机：
  - @preview/mitex:0.2.6：在有网络的环境运行一次 typst compile 让 typst 缓存它，或按 references/touying-backend.md 以 @local 方式安装；本脚本不下载包
```

请用户按参考文档安装后，用 `build_deck.py --force --compile` 重新构建。

## 4. 质量门

```bash
uv run python -B $SKILL_DIR/scripts/check_deck.py --deck defense-work/deck/defense.typ --inventory defense-work/inventory.json --plan defense-work/slide_plan.yaml
```

输出节选（行号与计数随规划变化）：

```text
% D-OVERFLOW-V (frame=c3-method-1, defense.typ:<行>) [Severity: Major] [Priority: P1]: [Script] 帧内容溢出，自动续出 1 页（第 <页> 页起）；精简内容或拆页
% 汇总：Critical 0，Major 1，Minor 0，Info 0；skipped：D-OVERFLOW-H
```

- Touying 主题在内容超出页面时自动续页。D-OVERFLOW-V 按每帧的页数定位溢出帧，处置顺序同 Beamer：删减文字、拆为两页、换用其他版式、缩小图宽。
- D-OVERFLOW-H 始终记入 `skipped`：typst 不报告横向溢出，以预览目视检查代替。
- 修规划后用 `build_deck.py --force --compile` 重建，最多 3 轮。不直接改 `defense.typ`。

## 5. 预览、放映与检查点 3

```bash
uv run python -B $SKILL_DIR/scripts/render_preview.py --pdf defense-work/deck/defense.pdf --out defense-work/deck/preview
```

交付说明示例：

> 答辩稿 54 页，两份 PDF 都已编译；质量门 Critical 0、Major 0、Minor 0。备注版 `defense-notes.pdf` 共 108 页：每页幻灯片后跟一页 `notes:N` 备注页。
> 双屏放映请用 FerroStage 打开 `defense-work/deck/defense-notes.pdf`：它按页标签自动配对幻灯片与备注，不需要选择拼合布局；投影只显示幻灯片。
> macOS 或 Linux 上用 pympress 打开同一文件。提交与打印用 `defense.pdf`。
