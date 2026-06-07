# 模块：Figures

**触发**：figures、figure、缺图、DPI、分辨率、栅格图、graphicspath、图片资源

## 命令

```bash
uv run python -B scripts/check_figures.py main.tex
uv run python -B scripts/check_figures.py main.tex --min-dpi 300
```

## 说明

`check_figures.py` 会扫描 `\includegraphics` 调用，解析项目内图片路径，并报告：

- 图片文件缺失；
- 不理想的栅格格式，通常优先考虑可改成矢量图；
- 低 DPI 或疑似低分辨率资源。

这个模块关注图像资源质量，不负责 caption 文案。如果问题是 caption 话术或证据边界，请改用 `caption`。

技能层响应：

1. 把缺图和低质量图的问题整理成简洁的 diff 风格评论。
2. 保留行号、资源路径和严重级别。
3. 若用户实际在问 caption 写法，应标明超出当前模块范围。
