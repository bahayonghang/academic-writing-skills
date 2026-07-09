# Research: 缺证清单（missing evidence）

- **Query**: 检索过但拿不到可靠官方原文的候选条目汇总
- **Scope**: external
- **检索日期**: 2026-07-09
- **抓取方式**: MCP exa 工具在本会话不可用；检索用 DuckDuckGo HTML 端点 + Bing（被 bot
  检测拦截，未获结果）+ 官方站点直接 curl；PDF 用 pypdf 抽取。
- **处置规则**: 下列条目一律**不得**写入 thuthesis/pkuthss/generic 清单的规范依据；
  相关条目降级 generic 通用项（标"以本校规范为准"）或写 llm/manual，或不写。

## 缺证条目

### M1. 清华《研究生学位论文写作指南》2026 年 5 月版原文

- **条目内容**: 2026-05 版指南全文（thuthesis CHANGELOG v7.7.1 称该版改动为"统一博士、硕士
  授权页的措辞"）。
- **搜索词**: `清华大学 研究生学位论文写作指南 2026`；并核对 dhs.tsinghua.edu.cn 已托管文件
  （仅 2025-03 版 2025032107444819.pdf 与更早的 2024031107044595.pdf）。
- **访问过的 URL**:
  - `https://info2021.tsinghua.edu.cn/f/info/xxfb_fg/xnzx/template/detail?xxid=fa880bdf60102a29fbe3c31f36b76c7e`（正式发布渠道）
  - `https://www.dhs.tsinghua.edu.cn/wp-content/uploads/2023/12/2025032107444819.pdf`（公开副本，2025-03 版）
- **失败原因**: 正式渠道**限校内网络访问**（thuthesis.dtx 行 77 明示）；公开网络仅见 2025-03
  版副本。
- **影响与处置**: 清华条目以 2025-03 版为准（差异点仅授权页措辞，属 manual 检查范围）；
  清单头部注明版本基线为 2025-03 公开副本。

### M2. 清华指南英文版 *Guide to Thesis Writing for Graduate Students*

- **条目内容**: 英文版指南（thuthesis.dtx 摘要节提及为编写依据之一）。
- **搜索词**: 未单独深挖（中文版已覆盖全部量化条目）。
- **访问过的 URL**: 无直接命中。
- **失败原因**: 校内发布，公开网络未见。
- **影响与处置**: 不影响中文清单；英文书写论文场景不在本次清单范围。

### M3. 清华正文字数 / 绪论字数 / 结论字数 / 参考文献最低条数与年限占比

- **条目内容**: 若存在，应写入 TEMPLATE_THRESHOLDS['thuthesis']。
- **搜索词**: 在 2025-03 版指南全文（53 页 pypdf 全文）内检索"字以内/字左右/不超过/不少于/
  以内/万字/篇"。
- **访问过的 URL**: dhs.tsinghua.edu.cn 2025-03 版 PDF（全文已抽取）。
- **失败原因**: **官方指南根本没有这些规定**（命中仅：题目 25 字、关键词 5 个、摘要 800–1000、
  致谢一页、姓名 4 字排版规则、责任者著录 3 个）。属"规定不存在"而非"没搜到"。
- **影响与处置**: thuthesis 清单不得含 wordcount/intro_len/conclusion_len/bib_count/
  bib_recency 的 script 条目；THU 阈值只配 title_len/abstract_len/kw_count（上限5）。

### M4. 北大正文字数 / 绪论字数 / 结论字数 / 参考文献最低条数与年限占比

- **条目内容**: 若存在，应写入 TEMPLATE_THRESHOLDS['pkuthss']。
- **搜索词**: 在《研究生学位论文写作指南》（V2.0/2014-05，24 页全文）内检索同上关键词。
- **访问过的 URL**: grs.pku.edu.cn 两个官方 PDF（已抽取全文，MD5 一致）。
- **失败原因**: 官方指南无这些规定（命中仅：题目 20 字、摘要博 800–1000/硕 600 左右、
  关键词 3~5、致谢 1000 字）。属"规定不存在"。
- **影响与处置**: pkuthss 清单同上不得写这些 script 条目。

### M5. 北大"2022 年研究生学位论文格式审核要求"原文

- **条目内容**: 社区模板（iofu728 的 Overleaf 适配版，仓库 pkuthss.md 快照亦提及）宣称
  "符合 2022 研究生格式审核"，如有官方通知原文可校准 pkuthss 与现行审核差异。
- **搜索词**: `北京大学 2022 研究生学位论文格式审核`。
- **访问过的 URL**:
  - `https://grs.pku.edu.cn/xwgz11/xwsy11/ssxw111/clxz08/index.htm`（硕士材料下载页）
  - `https://grs.pku.edu.cn/xwgz11/xwsy11/bsxw111/clxz09/index.htm`（博士材料下载页）
  - `https://cn.overleaf.com/latex/templates/2022-peking-university-master-thesis-template-iofu728-pkuthss/rwfvbkpzydpf`（仅有转载源）
- **失败原因**: 研究生院公开页面无该通知；**仅有 Overleaf 模板描述这一二手转载源**。
- **影响与处置**: 清单不引用"2022 格式审核"任何具体要求；北大条目全部以 V2.0 指南 +
  2024 官方模板为据。

### M6. 仓库 pkuthss.md 快照"必须包含'符号说明'章节"的官方出处

- **条目内容**: 快照声称符号说明为必备章节且"符号表格式有特定要求"。
- **搜索词**: 官方指南全文检索"符号"；pkuthss 说明文档/示例全文核对。
- **访问过的 URL**: grs.pku.edu.cn V2.0 指南 PDF；codeberg pkuthss doc/example。
- **失败原因**: 官方指南 §1.6 为**条件式**（"如果论文中使用了大量的符号……应编写'主要符号
  对照表'。如果……数量不多，可以不设"）；pkuthss 模板与示例根本没有该章。未找到"必须包含"
  的任何官方出处。
- **影响与处置**: PKU 清单该条应写成条件项（llm），并建议实现任务顺带修正 pkuthss.md 快照
  表述。

### M7. GB/T 7713.1-2025 全文条文（题名/摘要/关键词等数值是否调整）

- **条目内容**: 2025 版逐条内容，用于判断 generic 条目是否需按新国标更新数值。
- **搜索词**: `GB/T 7713.1-2025 学位论文 发布 代替 7713.1-2006`、openstd 标准号检索 `7713.1`。
- **访问过的 URL**:
  - `https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=36C05B5738C54D42B4B262525320B52F`
    （官方详情，原文提示："该标准采用了ISO、IEC等国际国外组织的标准，由于涉及版权保护问题，
    本系统暂不提供在线阅读服务"）
  - `https://library.fudan.edu.cn/_upload/article/files/29/7c/99065ad94d508eaaae49a22de9ff/5f7e7b14-3c37-4497-9ea2-d03c2d4e720a.pdf`
    （复旦图书馆托管扫描件，25 页图像 PDF，pypdf 抽取 0 字符，无 OCR 手段）
  - 商业/非官方下载站（biaozhun.org、foodmate.net 等）**未采用**（非官方来源）。
- **失败原因**: 官方平台因 ISO 采标版权不提供在线阅读；公开托管件为图像扫描无文本层。
- **影响与处置**: generic 清单条文只引 2006 版（标注"已废止、2026-02-01 起由 2025 版代替，
  以本校规范为准"）；不得转述任何"2025 版规定了××"的博客/知乎数值（检索结果中的知乎/搜狐/
  CSDN 帖仅作线索，未采信）。

### M8. GB/T 7713.1-2006 文本的多源交叉验证

- **条目内容**: 2006 版条文摘录的第二个可机读来源（xxmu 副本孤证问题）。
- **搜索词**: `GB/T 7713.1-2006 学位论文编写规则 pdf site:edu.cn`。
- **访问过的 URL**:
  - `https://www.xxmu.edu.cn/qks/GB_T7713.1-2006.pdf`（文本层完整，已采用）
  - `https://gs.xauat.edu.cn/gbzxbz.pdf`（图像版，0 字符）
  - `https://www.suibe.edu.cn/_upload/article/files/ee/fd/.../18c20ee9-....pdf`（图像版，0 字符）
  - `http://jiaowu.ruc.edu.cn/xsym/bylwsj/93ae7ac1aabc4c178af27d0df5c0dd5b_mobile.htm`、
    `https://www.scfai.edu.cn/yjsc/info/1004/2032.htm`（页面为 JS/附件壳，无正文文本）
- **失败原因**: 其余大学副本均为扫描图或空壳页。
- **影响与处置**: 摘录条目均含标准自身章条号（§5.1.6 等），且与清华指南参考文献、燕山规范
  引用互洽；落地时保留"以本校规范为准"限定即可，风险可控。xxmu 副本 §4.4 有
  "210×197mm"笔误，A4 尺寸引 §6.7。

### M9. 北大 2024 官方 Word 模板的逐页版式数值

- **条目内容**: 博士/硕士模板（.doc，2024-02-29）内的精确字号/间距设定，可用于核对 V2.0
  指南是否有 2024 微调。
- **访问过的 URL**:
  - `https://grs.pku.edu.cn/docs/2024-02/20240229092001843564.doc`（博士，已下载）
  - `https://grs.pku.edu.cn/docs/2024-02/20240229092055895909.doc`（硕士，未逐页解析）
  - `https://grs.pku.edu.cn/docs/2024-02/20240229092536846432.doc`（匿名评阅封面）
- **失败原因**: .doc 为 OLE2 二进制，本环境无 Word/antiword/OCR；仅做 UTF-16 字符串粗扫
  （能确认章名中文数字、图表点号编号、附录 A、声明页文本，无法读出字号数值）。
- **影响与处置**: 版式数值类条目以 V2.0 指南文字为准（manual 检查）；模板细节留给用户比照
  官方 doc。

### M10. pkuthss 原 Gitea 仓库的归档时间戳佐证

- **条目内容**: 仓库快照 pkuthss.md 写"原 Gitea 仓库已于 2024-08 归档迁出"；本次未复核
  Gitea 侧状态。
- **访问过的 URL**: 仅访问 codeberg.org（master 可用，README.txt 的 Homepage 仍写
  gitea.com/CasperVector/pkuthss）。
- **失败原因**: 未逐一访问 gitea.com 验证归档横幅（优先级低，未占检索预算）。
- **影响与处置**: 清单不涉及仓库托管地；维持快照现有表述即可。

## 汇总

- 缺证条目共 10 项；其中 M3/M4 实为"官方规定不存在"（防止套用别校阈值的负面证据），
  M6 为仓库既有快照的无出处表述（建议实现时修正），M7 为最关键缺证（新国标全文），
  其余为次要或已规避。
