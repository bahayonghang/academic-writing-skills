# 通用中文论文模板

## 目录

- [适用场景](#适用场景)
- [基础配置](#基础配置)
- [章节设置](#章节设置)
- [图表编号](#图表编号)
- [常见校级排版约定](#常见校级排版约定)
- [字体配置](#字体配置)
- [编译方式](#编译方式)
- [注意事项](#注意事项)

---

## 适用场景

- 没有学校专用模板时使用
- 符合国家标准 GB/T 7713.1-2006

## 基础配置

```latex
\documentclass[12pt, a4paper]{ctexbook}

% 页面设置
\usepackage[
  top=3cm,
  bottom=2.5cm,
  left=3cm,
  right=2.5cm,
]{geometry}

% 参考文献
\usepackage[backend=biber, style=gb7714-2015]{biblatex}

% 图表标题
\usepackage{caption}
\captionsetup{
  font=small,
  labelsep=space,
  format=hang,
}

% 页眉页脚
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[C]{\leftmark}
\fancyfoot[C]{\thepage}
```

## 章节设置

```latex
% 章节标题格式
\ctexset{
  chapter = {
    format = \centering\heiti\zihao{3},
    nameformat = {},
    titleformat = {},
    number = \chinese{chapter},
    name = {第,章},
    aftername = \quad,
    beforeskip = 20pt,
    afterskip = 20pt,
  },
  section = {
    format = \heiti\zihao{4},
    aftername = \quad,
    beforeskip = 10pt,
    afterskip = 10pt,
  },
  subsection = {
    format = \heiti\zihao{-4},
    aftername = \quad,
    beforeskip = 8pt,
    afterskip = 8pt,
  },
}
```

## 图表编号

```latex
% 按章编号
\usepackage{amsmath}
\numberwithin{equation}{chapter}
\numberwithin{figure}{chapter}
\numberwithin{table}{chapter}

% 编号格式：3.1
\renewcommand{\thefigure}{\thechapter.\arabic{figure}}
\renewcommand{\thetable}{\thechapter.\arabic{table}}
\renewcommand{\theequation}{\thechapter.\arabic{equation}}
```

## 常见校级排版约定

> 以下是国内高校学位论文**常见**的排版约定（自 GB/T 7713.1 衍生的校级规定，
> **非 GB/T 7714 国标强制内容**），各校细节不同，**一律以本校最新格式规范为准**。
> 已知模板时改读 `thuthesis.md` / `pkuthss.md`，模板会自动处理这些格式。

### 图表与公式编号

- **图题**：图下方，"图 3-1 图题内容"（连字符）或 "图3.1 图题内容"（点号），常见宋体五号
- **表题**：表上方，格式同图题（"表 3-1" / "表3.1"），常见宋体五号
- **公式编号**：公式右侧右对齐，常见 (3.1) 或 (3-1)（第 3 章第 1 个公式）
- 连字符还是点号取决于学校模板：thuthesis 用 "图 3-1"，pkuthss 用 "图3.1"

### 章节标题字体（常见设定）

| 级别 | 字体 | 字号 | 对齐 |
|------|------|------|------|
| 章标题 | 黑体 | 三号 | 居中 |
| 节标题 | 黑体 | 四号 | 左对齐 |
| 小节标题 | 黑体 | 小四 | 左对齐 |
| 段落标题 | 黑体 | 五号 | 左对齐 |

## 字体配置

```latex
% 确保系统有这些字体
\setCJKmainfont{SimSun}[
  BoldFont=SimHei,
  ItalicFont=KaiTi,
]
\setCJKsansfont{SimHei}
\setCJKmonofont{FangSong}

% 英文字体
\setmainfont{Times New Roman}
\setsansfont{Arial}
\setmonofont{Courier New}
```

## 编译方式

```bash
xelatex main
biber main
xelatex main
xelatex main
```

## 注意事项

1. 必须使用 XeLaTeX
2. 确保安装所需字体
3. 参考文献使用 biblatex + biber
4. 根据具体学校要求调整格式
