# design — 08-10-nature-writing-en

## 边界

- 改动仅限 `academic-writing-skills/latex-paper-en/references/` 与 `docs/`(双语页面 + manifest)。
- `scripts/` 零改动。受 en+typst TIER1 哈希锁保护的文件(analyze_abstract.py 等)一律不碰。
- 不改 SKILL.md 正文结构(字符串锁测试分布在 tests/contracts 与 tests/skills),只改 last_updated。

## 文件级设计

### 1. 新文件 `references/writing/article-architecture.md`

结构(五节 + 头尾):

```
# Journal-Style Article Architecture
> 归属声明(社区归纳 Nature-leaning 启发式;同源说明;非官方规则)
## Full-Paper Argument Chain      (N1)
## Journal-Style Abstract Moves   (N2;注明与 section-writing/abstract.md 三模板并列,按论文类型选)
## Abstract Diagnostics (LLM)     (N3;三条候选提示,措辞抄父级契约;注明无数字项已有脚本检查)
## Results Evidence Ladder        (N4;六层 + `To test [question], we [action].` 开头模式)
## Discussion Widening            (N5;六步;交叉引用 section-writing/experiments.md Discussion Layering)
```

写作纪律:英文正文遵循 ASD-STE100;不复制 section-writing 文件内容,重叠处
`See references/writing/section-writing/xxx.md`;体量目标 ≤ 6KB(对齐同目录文件粒度)。

### 2. 路由接入(三处,最小改动)

- `references/modules/routing-rules.md`:在现有路由表加一行(触发词:journal narrative /
  Nature-style / Results narrative / Discussion structure / full-paper argument / 期刊式)→
  指向 article-architecture.md。格式对齐现有行(注意 SKILL.md/references 的表格行有
  ROUTER_ROW_RE 类契约,改前 grep tests/ 确认锁定范围)。
- `references/writing/section-writing/index.md`:Loading Rule 节后加一行交叉引用
  ("full-paper / journal-style architecture → ../article-architecture.md"),不改装载规则本体。
- `references/modules/section-writing.md`:Progressive Loading 表后加一句何时改读
  article-architecture.md。

### 3. 翻译 lane(D-EN-3)

位置判定:`references/writing/translation-guide.md`(11.8K,主体)加两节;
`references/modules/translation.md`(1.9K,路由页)加两行索引。不新建文件。

- 「意图翻译六分解」:分解表 + 按目标章节序重写的操作步骤(N15)。
- 「结构级修复」:两类新修复(宽泛重要性先于对象 / 方法列表先于 gap),
  表尾注明其余四类见 over-claim-guard(交叉引用,零复制)。

### 4. doc-only 微补(D-EN-4)

- `references/modules/title.md`:加「标题公式与 prestige 词」小节,标注 [LLM]。
- `references/modules/tables.md`:方向标注一句(三种可接受形式 + 非强制)。

### 5. 双语资源契约

按 `.trellis/spec/academic-writing-skills/docs-bilingual-resources.md`:

1. 内容全部就位后 `uv run python docs/scripts/check_resource_sync.py --write-manifest --inventory-only`
2. 校正新条目 sourceLocale;写 EN 页(完整英文译文)与 zh 页;侧栏注册
3. `--skill latex-paper-en` 单项校验 + 全量校验 + `just doc-build`

## 风险与回退

- 风险:routing-rules.md 表格行被契约测试锁定 → 改前先跑
  `grep -rn "routing" tests/contracts tests/skills`,命中则按测试期望格式写。
- 风险:全局格式化 hook 对齐 markdown 表格触发契约失败(历史教训)→ 提交前跑受影响契约测试。
- 回退:全部改动为文档新增/小节追加,`git revert` 单提交即可回退;manifest 可随时重建。

## 验证命令

```bash
uv run --extra dev python -m pytest tests/contracts/ -q
uv run python docs/scripts/check_resource_sync.py --skill latex-paper-en
uv run python docs/scripts/check_resource_sync.py
just ci
just doc-build
git diff --stat -- 'academic-writing-skills/latex-paper-en/scripts/'   # 必须为空
```
