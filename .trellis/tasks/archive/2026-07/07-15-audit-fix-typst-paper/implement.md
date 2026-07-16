# 实施计划 — typst可见文本解析修复

> 前置：若 07-15-audit-fix-latex-paper-en 已开工/已合，先 rebase 到其后再开始（父任务顺序约束 3）。
> 回滚点：实现开始前记录 `git rev-parse HEAD`（dev 分支），写入本文件末尾。

## Phase 0 — 前置检查

- [x] 确认 07-15-audit-fix-version-ci 已合（绿基线）：`uv run --extra dev python -m pytest tests/contracts/test_skill_versions.py -q`
- [x] 确认 en 任务状态；若其已改 `latex-paper-en/scripts/parsers.py`，先 rebase 本分支 — en 任务（07-15-audit-fix-latex-paper-en）已在基线 commit 之前合并归档，无需 rebase
- [x] 记录回滚点 commit hash
- [x] 基线全绿：`uv run --extra dev python -m pytest tests/skills/typst_paper tests/contracts tests/shared -q`（266 passed）

## Phase 1 — A-TY-1 测试先行（预期红）

- [x] `tests/shared/test_parsers.py`（EN canonical，bare import）新增：
  - [x] extract_visible_text：`http://` / `https://` 行内 URL——URL 本体与其后散文均可见
  - [x] extract_visible_text：`https://host//path more prose` → URL（含路径双斜杠）与散文完整可见（单一所有权锁定用例）
  - [x] extract_visible_text：`#link("https://…") hosts the code.` → 散文可见、#link 挖空
  - [x] extract_visible_text：`#link("//cdn.example.com/l.js") text` → #link 挖空、`text` 可见
  - [x] extract_visible_text：整行 `// c` → `""`；行尾 ` // c` 只剥注释；`a: // c` 正常剥
  - [x] extract_visible_text：裸 `//cdn.example.com` → `""`（协议相对=注释，决策锁定）
  - [x] extract_visible_text：反引号 raw 内 `//` 不剥且保持可见
  - [x] extract_visible_text：`/* hidden */ prose // note` → 块注释挖空、行注释剥除、`prose` 可见
  - [x] clean_text：多行（URL 行 + 注释行 + 含 `//` 的多行块注释）词数/文本精确断言
  - [x] extract_abstract 相关用例留到 Phase 3
- [x] `tests/skills/typst_paper/test_typst_paper_scripts.py`（沿用既有 importlib loader）新增 typst 副本同组用例（至少 URL 可见性 + `host//path` 完整可见 + clean_text 词数 + 协议相对裁决）
- [x] `tests/skills/latex_thesis_zh/test_latex_thesis_zh_scripts.py` 新增 zh TypstParser URL 用例一条
- [x] 跑测确认新用例全红、存量全绿：`uv run --extra dev python -m pytest tests/shared tests/skills/typst_paper tests/skills/latex_thesis_zh -q`（13 failed / 62 passed，红用例与预期缺陷位点一一对应）

## Phase 2 — A-TY-1 实现（先 canonical 后镜像；批次内不 commit）

- [x] `latex-paper-en/scripts/parsers.py`：新增 `_strip_typst_line_comment`；替换 `split("//")`；clean_text 块注释先行 + 逐行剥离；PRESERVE_PATTERNS **删除** `r"//.*"` 条目（整条删除，不是改写）
- [x] 逐字节镜像到 `paper-audit/scripts/parsers.py`、`cover-letter/scripts/parsers.py`
- [x] `typst-paper/scripts/parsers.py` 同步（其 TypstParser 与 en 锁定成员须字节一致）
- [x] `latex-thesis-zh/scripts/parsers.py`：新增帮助函数（与 en 字节一致）；替换 `split("//")`；PRESERVE 条目同步删除（不加 clean_text）
- [x] `tests/contracts/test_parsers_alignment.py` ALIGNMENTS 新增两行（`_strip_typst_line_comment` 五副本、`TypstParser.clean_text` 四副本）；:83 PRESERVE 锁行零改动
- [x] 验证：`uv run --extra dev python -m pytest tests/skills/typst_paper tests/contracts -q`（237 passed）
- [x] 验证：`uv run --extra dev python -m pytest tests/shared tests/skills/latex_thesis_zh tests/skills/cover_letter tests/skills/paper_audit -q`（839 passed）
- [x] grep 复核零残留：`rg -n 'split\("//"\)|"//\.\*"' academic-writing-skills/*/scripts/parsers.py`（零命中；`typ_loader.py` 的 `LINE_COMMENT_RE` 未触碰，确认不在范围）
- [ ] **拟提交分组 1（记录，不执行 git commit）**：留待 Phase 3.4 前按实际累积 diff 重新分组（A-TY-1/A-TY-2 共同触碰 en/audit/cover_letter/typst 四份 parsers.py，套用 testing-and-tooling.md「批次拟提交分组」坑位处理，不照搬本节原分组）

## Phase 3 — A-TY-2 测试先行 + 实现（批次内不 commit）

- [x] 测试（预期红）：
  - [x] `tests/shared/test_parsers.py`：`= Abstract\n…\n== Keywords\n…` → 不含 Keywords；`= Abstract\n…\n= Introduction` 行为不变
  - [x] `tests/skills/typst_paper/test_typst_paper_scripts.py`：typst 副本同组用例
- [x] 实现：lookahead `(?=^=\s+|\Z)` → `(?=^=+\s+|\Z)` 四处（en → 镜像 audit / cover-letter；typst 自有副本，变量名 `heading_abs` 原样保留）
- [x] 验证：`uv run --extra dev python -m pytest tests/skills/typst_paper tests/contracts tests/shared -q`
- [ ] **拟提交分组 2（记录，不执行 git commit）**：同上，留待 Phase 3.4 前按实际 diff 重新分组

## Phase 4 — 收尾验证与评审门（workflow Phase 2.2 / 3.2）

- [x] `just fix`（ruff format + fix；167 files unchanged，无与本任务无关的重排）
- [x] **最终**：`just ci` 全绿（lint 通过 → pyright 0 errors/72 warnings → 1259 passed）
- [x] 复核 git diff：每一行改动可追溯到 A-TY-1/A-TY-2；SKILL.md version/last_updated 零改动；evals.json 零改动
- [ ] **评审门（Review Gate）**：人工确认后再进入提交——
  1. 五副本 parsers.py diff 并排比对，锁定成员字节一致（含 PRESERVE 列表五副本同步少一元素）；
  2. ALIGNMENTS 仅 +2 行，:83 锁行未动；
  3. 协议相对 URL 裁决用例与 `host//path` 完整可见用例均存在且有注释说明；
  4. 与 en 任务分支无函数级冲突（若 en 后合，通知其 rebase 后重跑 tests/contracts）。

## Phase 3.4 — 提交（workflow Phase 3.3/3.4；全部门禁通过 + spec 更新后才执行）

- [ ] （3.3）若实施中沉淀了可复用契约/教训，先按 trellis-update-spec 更新 `.trellis/spec/`
- [ ] （3.4）按拟提交分组顺序执行实际提交：分组 1 → 分组 2，各自 `git add <文件集>` + `git commit -m "<拟提交信息>"`；两 commit 保持相互独立可 revert

## 回滚

- 提交前（Phase 2/3 期间）：按拟提交分组记录的文件集定点回退（scoped restore，**禁用 reset**）——既有文件 `git checkout -- <分组修改文件>`（需留证先 `git stash push -- <files>`）；本批**新建文件（测试文件等）按分组登记清单单列显式 `rm`**（checkout 无法移除新文件）；不产生中间 commit。
- 提交后单项失败：`git revert <commit1|commit2>`（两 commit 相互独立）。
- 整体放弃：对两个分组文件集依次执行上述 scoped restore（修改文件 checkout 到 Phase 0 记录的基线 hash：`git checkout <基线hash> -- <修改文件>`；新建文件 `rm`）。**不得使用 `git reset`——工作树可能存在其他任务的无关改动。**
- 回滚后必跑：`uv run --extra dev python -m pytest tests/contracts -q`（确认对齐锁回到原状态）。

基线 commit hash：f0e21b3816f00341d03280cd0fae37bc517d179e（Phase 0 填写，仅作 scoped checkout 的还原基准；en 任务 07-15-audit-fix-latex-paper-en 已合并入此 commit 之前，含于基线内，无需 rebase）
