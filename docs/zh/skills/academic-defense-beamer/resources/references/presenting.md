# 放映与演讲备注

本文件说明投屏版与备注版两份 PDF 的区别、备注页的内容，以及用 FerroStage 或 pympress 双屏放映的方法。讲稿五栏见 [讲稿格式](speaker-notes.md)，备注版的检查见 [质量门](quality-gate.md) 的 D-NOTES-PDF。

## 两份 PDF

| 文件                | 来源                                  | 页面                                                     | 用途                                 |
| ------------------- | ------------------------------------- | -------------------------------------------------------- | ------------------------------------ |
| `defense.pdf`       | `defense.tex`                         | 16:9 幻灯片，每帧一页                                    | 提交、打印、单屏放映、`preview` 预览 |
| `defense-notes.pdf` | `defense-notes.tex`（载入 `defense.tex`） | 每页左半为幻灯片，右半为该帧的演讲备注；页面比例 32:9    | 双屏演讲者模式                       |

- `build_deck.py --compile` 先编译投屏版，再编译备注版；`--no-notes-pdf` 只编译投屏版，`build_manifest.json` 的 `notes_pdf` 记为 `null`。
- 两份 PDF 页数相同，页标签都是 `1, 2, 3, …`。备注版的每一页都有唯一页标签，演示器不会把相邻两帧当作同一帧的分步页。
- 讲稿改动后运行 `build_deck.py --force --compile`，两份 PDF 一起重编。不手改 `defense.tex` 或 `defense-notes.tex`。

## 备注页内容

每帧的备注来自规划中该帧的 `notes`，由 `\DefenseNote` 写在帧内，顺序为：

1. **要点**（加粗一行）。
2. **说什么**（正文）。
3. **过渡**（灰色一行，以「→」开头），行尾为本页秒数。

- 「可能提问」不进入备注页，只在 `notes.md` 与答辩提问准备中使用。演讲者屏空间有限，提问是答辩前的准备材料。
- 文字中的 `**关键词**` 在备注页只加粗，不着色。空栏目渲染为空，不写「无」。
- 未填写的占位符「〔待填写〕」原样出现在备注页；质量门在 `notes.md` 中报告 D-PLACEHOLDER。
- 备注字号为 `\small`。250 字左右的「说什么」约占备注半页的一半。

## FerroStage（推荐，Windows）

[FerroStage](https://github.com/bahayonghang/ferrostage) 是离线运行的 PDF 双屏演示器，识别 Beamer 同页备注。

- 平台：Windows 10 1903 及以上的 x64 系统，或 Windows 11。没有 macOS 与 Linux 版本。
- 安装：当前没有 GitHub Release 安装包。从源码仓库运行 `just release`，生成 `FerroStage-<version>-windows-x64-Setup.exe` 后双击安装（需要 Rust 工具链）；
  开发者也可以用 `just build` 后直接运行 `target\release\ferrostage.exe`。具体要求以该仓库 README 为准。
- 放映步骤：
  1. 用 FerroStage 打开 `defense-notes.pdf`（不是 `defense.pdf`）。
  2. 全部页面同尺寸且宽高比约 3.56 时，FerroStage 自动给出 `Right` 布局候选：左半为幻灯片，右半为备注。界面会标出这是按比例推断的结果。
  3. 未自动识别或识别错误时，在布局菜单中手动选择 `Right`。
  4. 演讲者窗口显示幻灯片与备注；观众窗口（投影）只显示左半的幻灯片。
- FerroStage 只从 PDF 读取备注，不读取 `notes.md`。
- FerroStage 监听 PDF 文件变化。放映前重编备注版后，它会重新载入并保留当前页。

## pympress（跨平台）

macOS 与 Linux 用户使用 [pympress](https://github.com/Cimbali/pympress)（GPL-2.0+，也支持 Windows）。打开 `defense-notes.pdf`，它同样识别 Beamer 右侧备注；
未自动识别时，在备注位置菜单中选择右侧。

## 没有双屏时

- 单屏放映 `defense.pdf`，演讲者手持打印的 `notes.md`，或在另一台设备上打开 `defense-notes.pdf`。
- 不把备注版投到观众屏幕上：观众会看到讲稿。
