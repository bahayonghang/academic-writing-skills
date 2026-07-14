# 模板模块参考

用途：检测并验证正在使用的高校学位论文模板/文档类。

## 模板检测流程

1. **扫描文档类**：查找 `\documentclass{thuthesis}`、`\documentclass{pkuthss}`、`\documentclass[...]{ctexbook}` 等
2. **检查宏包导入**：识别 `ctex`、`xeCJK`、`fontspec` 和其他模板专用宏包
3. **匹配模板**：与 `templates/` 中的已知模板（唯一事实来源）比较
4. **报告**：输出检测到的模板名称、版本（如可用）以及所有配置警告

## 支持的模板

| 模板 | 高校 | 文档类 |
| ------------------ | ---------- | ------------------------------- |
| thuthesis | 清华大学 | `\documentclass{thuthesis}` |
| pkuthss | 北京大学 | `\documentclass{pkuthss}` |
| ctexbook（通用） | 多所高校 | `\documentclass[...]{ctexbook}` |

## 关键配置文件

- `.latexmkrc` - 编译器设置
- `*.cls` - 模板类文件
- `*.cfg` - 模板配置
- `refs.bib` / `references.bib` - 参考文献数据库

## 检测后处理

识别模板后，从以下位置加载对应模板快照：

- `templates/{template}.md`（thuthesis.md / pkuthss.md）提供各模板约束
- 未知模板使用 `templates/generic.md` 作为回退（ustcthesis / fduthesis 暂同）
- `templates/yanshan.md` 提供燕山大学规范获取指引（无可检测的 documentclass）

> 各模板的权威快照参见 [`generic.md`](../../templates/generic.md)、
> [`thuthesis.md`](../../templates/thuthesis.md)、[`pkuthss.md`](../../templates/pkuthss.md)
> 和 [`yanshan.md`](../../templates/yanshan.md)。
