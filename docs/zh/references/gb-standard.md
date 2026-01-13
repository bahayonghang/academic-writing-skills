# GB/T 7714 标准

GB/T 7714-2015 信息与文献 参考文献著录规则。

## 概述

GB/T 7714-2015 是中国国家标准，规定了各类文献的著录格式。

## 基本要求

### 必需字段

| 文献类型 | 必需字段 |
|----------|----------|
| 期刊文章 | author, title, journal, year, volume, pages |
| 会议论文 | author, title, booktitle, year, pages |
| 书籍 | author, title, publisher, year |
| 学位论文 | author, title, school, year |

### language 字段

所有条目必须包含 `language` 字段：

```bibtex
language = {zh}  % 中文
language = {en}  % 英文
```

## 著录格式

### 期刊文章

**格式**：
```
作者. 题名[J]. 刊名, 年, 卷(期): 起止页码.
```

**BibTeX**：
```bibtex
@article{zhang2024deep,
  author = {张三 and 李四},
  title = {深度学习在自然语言处理中的应用},
  journal = {计算机学报},
  year = {2024},
  volume = {47},
  number = {3},
  pages = {123--145},
  language = {zh}
}
```

### 会议论文

**格式**：
```
作者. 题名[C]//会议名. 出版地: 出版者, 年: 起止页码.
```

**BibTeX**：
```bibtex
@inproceedings{wang2024neural,
  author = {王五 and 赵六},
  title = {神经网络优化方法研究},
  booktitle = {中国计算机大会论文集},
  year = {2024},
  pages = {45--52},
  address = {北京},
  language = {zh}
}
```

### 书籍

**格式**：
```
作者. 书名[M]. 版本. 出版地: 出版者, 年.
```

**BibTeX**：
```bibtex
@book{liu2023machine,
  author = {刘七},
  title = {机器学习基础},
  publisher = {清华大学出版社},
  year = {2023},
  address = {北京},
  language = {zh}
}
```

### 学位论文

**格式**：
```
作者. 题名[D]. 保存地: 保存单位, 年.
```

**BibTeX**：
```bibtex
@phdthesis{chen2023research,
  author = {陈八},
  title = {深度强化学习理论与应用研究},
  school = {清华大学},
  year = {2023},
  address = {北京},
  language = {zh}
}
```

### 电子资源

**格式**：
```
作者. 题名[EB/OL]. (更新日期)[引用日期]. 网址.
```

**BibTeX**：
```bibtex
@misc{web2024,
  author = {作者},
  title = {网页标题},
  howpublished = {\url{https://example.com}},
  year = {2024},
  note = {[2024-01-15]},
  language = {zh}
}
```

## 作者著录

### 中文作者

- 姓名之间用 "and" 连接
- 使用中文字符

```bibtex
author = {张三 and 李四 and 王五}
```

### 英文作者

- 姓在前，名在后
- 用逗号分隔

```bibtex
author = {Smith, John and Doe, Jane}
```

### 多作者

- 3 人以下全部列出
- 3 人以上可用 "等" 或 "et al."

```bibtex
% 中文
author = {张三 and 李四 and 王五 and others}

% 英文
author = {Smith, John and Doe, Jane and others}
```

## 标点符号

### 中文文献

- 题名后用 `[J]`、`[C]`、`[M]` 等标识文献类型
- 各项之间用 `. ` 分隔
- 页码用 `--` 连接

### 英文文献

- 同中文文献
- 注意大小写规范

## 文献类型标识

| 标识 | 类型 |
|------|------|
| [J] | 期刊文章 |
| [C] | 会议论文 |
| [M] | 专著/书籍 |
| [D] | 学位论文 |
| [R] | 报告 |
| [S] | 标准 |
| [P] | 专利 |
| [EB/OL] | 电子资源 |

## LaTeX 配置

### 使用 gbt7714 宏包

```latex
% BibLaTeX + Biber（推荐）
\usepackage[backend=biber,style=gb7714-2015]{biblatex}
\addbibresource{references.bib}

% 文档末尾
\printbibliography
```

### 使用 BibTeX

```latex
\bibliographystyle{gbt7714-numerical}
\bibliography{references}
```

## 验证

使用 Academic Writing Skills 验证 GB/T 7714 合规性：

```bash
python verify_bib.py references.bib --standard gbt7714
```

**检查内容**：
- language 字段存在
- 必需字段完整
- 作者格式正确
- 页码格式正确

## 常见问题

### 缺少 language 字段

```bibtex
% 错误
@article{zhang2024,
  author = {张三},
  title = {深度学习},
  journal = {计算机学报},
  year = {2024}
}

% 正确
@article{zhang2024,
  author = {张三},
  title = {深度学习},
  journal = {计算机学报},
  year = {2024},
  language = {zh}
}
```

### 作者格式错误

```bibtex
% 错误
author = {San Zhang}  % 西方顺序

% 正确
author = {张三}  % 中文字符
author = {Zhang, San}  % 拼音，姓在前
```

### 页码格式错误

```bibtex
% 错误
pages = {123-145}  % 单破折号

% 正确
pages = {123--145}  % 双破折号
```

## 下一步

- [参考文献管理](/zh/guides/bibliography)
- [常见错误](/zh/references/common-errors)
