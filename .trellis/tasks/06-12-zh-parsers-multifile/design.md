# Design: parsers 多文件解析与章节切分修复

## 1. 新模块 `scripts/tex_loader.py`（共享装配能力，R1+R4）

单一权威的 include 解析器，替代 map_structure / check_references 各自的实现（消除第三套重复）。

### 数据结构

```python
@dataclass
class IncludeNode:           # iter_files() 的遍历记录
    path: Path               # 解析后的绝对路径
    rel: str                 # 相对入口目录的显示路径（posix 风格）
    level: int               # include 嵌套深度（入口=0）
    exists: bool
    content: str | None      # robust 读取结果（missing 时为 None）
    warning: str | None      # 编码告警

class AssembledDocument:
    entry: Path
    content: str             # 按文档顺序拼接的全文
    lines: list[str]
    origins: list[tuple[str, int]]   # 拼接行号-1 → (源文件 rel, 源行号 1-based)
    missing: list[tuple[str, str, int]]  # (include 参数, 所在文件 rel, 行号)
    warnings: list[str]      # 编码异常等
    multi_file: bool         # 是否实际展开了 include

    def origin(self, line_no) -> (rel, src_line)
    def lineref(self, start, end=None) -> str
        # 单文件: "第15行" / "第15-20行"
        # 多文件: "chapters/ch1.tex:15" / "chapters/ch1.tex:15-20"（跨文件时只标起点文件）
    def lineref_en(self, start) -> str   # "Line 15" / "chapters/ch1.tex:15"
    def warning_lines(self, comment_prefix) -> list[str]  # "% WARN: ..." 头部告警
```

### 函数

- `read_text_robust(path) -> (text, warning|None)`：utf-8 严格 → GB18030 → utf-8 replace+告警（R4）。
- `iter_files(entry) -> list[IncludeNode]`：递归解析 `\input/\include/\subfile`（跳过 `%` 注释行，
  respect `\%` 转义；`\includegraphics` 不会误匹配）。循环防护用 visited set；
  缺失文件产出 exists=False 节点。路径解析：先相对当前文件目录，再相对入口目录，自动补 `.tex`。
- `assemble(entry) -> AssembledDocument`：基于 iter_files 在 include 命令处内联展开，
  维护行号映射。include 行上的前后缀文本各占一行映射回原行。`.typ` 入口不展开（单文件直读）。

## 2. parsers.py（ZH 专化变体，R2+R3）

哈希锁定项（PRESERVE_PATTERNS、ABC 签名、_normalize_whitespace）不动。

### split_sections 重写（两个 Parser 共用模块级辅助）

1. 基于 extract_headings（天然跳过注释行；ZH extract_headings 增加 inline `%` 剥离）。
2. 标题归一化 `_normalize_heading_title`：去除 `\quad/\qquad/\hspace{..}/~/空白`，
   使 `绪\quad 论`、`\chapter*{摘要}`、`\chapter[短]{长}` 均可识别。
3. 分类规则 `SECTION_TITLE_RULES`：per-key (允许级别, 标题正则)，语义与旧 SECTION_PATTERNS 一致
   （method 仅 chapter 级、abstract/introduction 等精确匹配、experiment/result 等包含匹配）。
4. 区间边界：匹配标题开启新区间；遇到 **任何 level ≤ 当前区间级别** 的标题即关闭当前区间
   （未匹配的正文章不再被并入前一区间）。
5. 同 key 去重：第二次出现记为 `method_2`、`method_3`…（值仍是 tuple，ABC 签名不变）。
6. 旧 SECTION_PATTERNS 保留为兼容别名（标注 deprecated，仍有外部引用风险）。

### 新增 API

- `DocumentParser.chapter_ranges(content) -> list[dict]`：全部 level-1 章节区间
  `{"title","start","end","key"|None}`（F6 全章节枚举途径）。
- `resolve_section_keys(query, sections) -> (keys, available)`：中英同义映射
  （绪论/引言→introduction 等），支持 `method` 命中 `method/method_2`；
  未命中时返回可用 key 列表供错误信息使用（R3）。

## 3. 脚本接入（R1）

| 脚本 | 接入方式 |
|------|----------|
| analyze_logic | `assemble()`；模块级 `_fmt_line/_fmt_range` 由 analyze() 注入；`--section` 走 resolve_section_keys；头部输出 doc 告警 |
| deai_check / deai_batch | 构造函数改 `assemble()`；报告行号经 `doc.lineref`；JSON 建议的 file/line 改为源文件定位；`--section` 同上 |
| analyze_experiment / analyze_literature | 同 analyze_logic 模式 |
| analyze_abstract / optimize_title | 仅需全文内容：`assemble().content` + 告警输出 |
| check_tables / check_format | issues 增加 file 字段（origin 映射），行号映射回源文件；chktex 仍只跑入口文件（外部工具限制，文档说明） |
| check_consistency | find_tex_files 默认改 include 图（iter_files），`--all-files` 保留 rglob（F17 接口约定）|
| check_references | `_resolve_includes` 删除，改用 iter_files + robust read |
| map_structure | `_parse_file` 递归删除，改用 iter_files 记录重建 structure |

## 4. 兼容性

- 单文件输入时所有输出与现状逐字符一致（lineref 退化为旧格式）→ 现有测试不破。
- sections dict 仍为 `dict[str, tuple[int,int]]`；调用方 `"related" in sections` 语义不变。
- test_parsers_alignment.py 锁定成员零改动。

## 5. 回滚

纯新增模块 + 各脚本入口处小改；回滚 = revert 单个 commit。
