# 期刊或会议特定规则

什么时候`--venue`（或者`--journal`) 指定后，审计添加了特定于期刊或会议的检查：

|期刊或会议|关键规则|
|-------|-----------|
| `neurips` |9 页限制、更广泛的影响陈述、纸质清单、双盲|
| `iclr` |10 页限制、再现性声明、双盲|
| `icml` |8 页限制、影响陈述、50MB 补充限制|
| `ieee` |摘要<=250字，3-5个关键词，>=300DPI数字，无浮动`algorithm` / `algorithm2e`伪代码，图形样式伪代码标题/标签/参考检查|
| `acm` |所需的 CCS 概念、acmart 类、权限管理|
| `thesis-zh` | 见下方「中文学位论文」小节。不设 `page_limit`：学位论文按字数计，校际差异大。 |

### 中文学位论文（`thesis-zh`）

机械 `extra_checks` 使用稳定 ID `TZ-EC-*`。每个 ID 必须作为
`TZ-CL-*` 出现在 `CHECKLIST.md` 中。反向不要求集合相等。
- `TZ-EC-bilingual-abstract` / `TZ-CL-bilingual-abstract`：中英文摘要均为必需（GB/T 7713.1 与学校模板）。
- `TZ-EC-bilingual-keywords` / `TZ-CL-bilingual-keywords`：中英文关键词均为必需。
- `TZ-EC-originality` / `TZ-CL-originality`：原创性声明为必需。
- `TZ-EC-acknowledgments` / `TZ-CL-acknowledgments`：致谢为必需。
- **不设** `page_limit`。硕士与博士字数因校而异（约 3–5 万与 8–15 万字量级），设一个数会误报。
- 保持 `blind_review: False`。该字段只追加会议双盲清单项（`audit.py` 的 `_run_checklist`）。学位论文盲审由 `blind` 检查键（`blind_review.py --check`）承载。
- 附录与符号表存在性只作为清单人工项（`TZ-CL-appendix-optional`、`TZ-CL-symbols-optional`）。燕山标注可省，北大标注符号表为条件项。它们不得进入 `extra_checks` 或 gate。

没有`--venue`，仅通用清单项目适用。
