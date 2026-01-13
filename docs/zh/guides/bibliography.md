# 参考文献管理指南

Academic Writing Skills 中参考文献管理的完整指南。

## 概述

Academic Writing Skills 为英文论文（BibTeX/Biber）和中文论文（GB/T 7714-2015）提供全面的参考文献管理。

## BibTeX 基础

### 条目结构

```bibtex
@条目类型{键,
  字段1 = {值1},
  字段2 = {值2},
  ...
}
```

### 常见条目类型

#### @article（期刊文章）

```bibtex
@article{Smith2024-ml,
  author = {Smith, John and Doe, Jane},
  title = {Machine Learning for NLP},
  journal = {Journal of Machine Learning Research},
  year = {2024},
  volume = {25},
  pages = {123--145},
  doi = {10.1234/jmlr.2024.001}
}
```

**必需字段**：author, title, journal, year

#### @inproceedings（会议论文）

```bibtex
@inproceedings{Wang2024-neural,
  author = {Wang, Alice and Zhang, Bob},
  title = {Neural Network Optimization},
  booktitle = {Proceedings of ICML},
  year = {2024},
  pages = {456--467}
}
```

**必需字段**：author, title, booktitle, year

#### @book（书籍）

```bibtex
@book{Johnson2023-deep,
  author = {Johnson, Michael},
  title = {Deep Learning Fundamentals},
  publisher = {MIT Press},
  year = {2023}
}
```

**必需字段**：author, title, publisher, year

## 参考文献验证

### 基本验证

```bash
python verify_bib.py references.bib
```

**检查内容**：
- 必需字段存在
- 条目格式有效
- 无重复键
- DOI 格式有效

### 样式特定验证

```bash
# IEEE 样式
python verify_bib.py references.bib --style ieee

# ACM 样式
python verify_bib.py references.bib --style acm

# GB/T 7714（中文）
python verify_bib.py references.bib --standard gbt7714
```

## 常见问题

### 1. 缺少必需字段

```bibtex
% 错误
@article{Smith2024,
  author = {Smith, John},
  title = {Machine Learning}
  % 缺少：journal, year
}

% 正确
@article{Smith2024,
  author = {Smith, John},
  title = {Machine Learning},
  journal = {Journal of ML},
  year = {2024}
}
```

### 2. 重复键

```bibtex
@article{Smith2024, ...}
@inproceedings{Smith2024, ...}  % 重复！
```

**修复**：重命名为唯一键
```bibtex
@article{Smith2024-journal, ...}
@inproceedings{Smith2024-conf, ...}
```

### 3. 页码格式

```bibtex
% 错误
pages = {123-145}  % 单破折号

% 正确
pages = {123--145}  % 双破折号
```

### 4. 作者格式

```bibtex
% 错误
author = {John Smith and Jane Doe}  % 名在前

% 正确
author = {Smith, John and Doe, Jane}  % 姓在前
```

## GB/T 7714-2015（中文标准）

### 关键要求

1. **language 字段**：所有条目必需
2. **作者姓名**：使用原语言
3. **标题**：使用原语言
4. **特定标点**：中英文不同

### 条目示例

#### 中文期刊文章

```bibtex
@article{zhang2024deep,
  author = {张三 and 李四},
  title = {深度学习在自然语言处理中的应用},
  journal = {计算机学报},
  year = {2024},
  volume = {47},
  number = {3},
  pages = {123--145},
  language = {zh},
  doi = {10.11897/SP.J.1016.2024.00123}
}
```

#### 中文会议论文

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

#### 中文学位论文

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

### 常见 GB/T 7714 问题

#### 缺少 language 字段

```bibtex
% 错误
@article{zhang2024,
  author = {张三},
  title = {深度学习},
  ...
  % 缺少 language！
}

% 正确
@article{zhang2024,
  author = {张三},
  title = {深度学习},
  ...,
  language = {zh}
}
```

## BibTeX vs. Biber

### BibTeX（传统）

| 优点 | 缺点 |
|------|------|
| 兼容性广 | 仅 ASCII |
| 稳定成熟 | 排序有限 |
| 支持旧 .bst 样式 | 无 Unicode |

**用途**：纯英文论文、旧模板

### Biber（现代）

| 优点 | 缺点 |
|------|------|
| 完整 Unicode 支持 | 需要 BibLaTeX |
| 高级排序 | 与旧模板兼容性差 |
| 更好的本地化 | |

**用途**：现代论文、中文论文、Unicode

## 自动修复

```bash
python verify_bib.py references.bib --fix
```

**可自动修复**：
- 页码格式
- 尾随逗号
- 空白规范化

**需手动审查**：
- 缺少必需字段
- 重复键
- 作者姓名格式
- language 字段

## 最佳实践

### 1. 一致的键命名

```bibtex
% 模式：作者年份-关键词
@article{Smith2024-ml, ...}
@inproceedings{Wang2024-neural, ...}
```

### 2. 始终包含 DOI

```bibtex
@article{Smith2024,
  ...,
  doi = {10.1234/journal.2024.001}
}
```

### 3. 使用正确的条目类型

```bibtex
@article{...}         % 期刊文章
@inproceedings{...}   % 会议论文
@book{...}            % 书籍
@phdthesis{...}       % 博士论文
@mastersthesis{...}   % 硕士论文
```

### 4. 定期验证

```bash
# 添加条目后验证
python verify_bib.py references.bib

# 提交前完整检查
python verify_bib.py references.bib --style ieee --require-doi
```

## 故障排除

### 参考文献未显示

**解决**：使用完整编译配置
```bash
python compile.py paper.tex --recipe pdflatex-biber
```

### 编码问题

**问题**：中文字符不显示

**解决**：确保 UTF-8 编码
```bash
# 检查编码
file -i references.bib

# 转换
iconv -f GBK -t UTF-8 references.bib > references_utf8.bib
```

## 下一步

- [编译配置指南](/zh/guides/compilation)
- [格式检查指南](/zh/guides/format-checking)
