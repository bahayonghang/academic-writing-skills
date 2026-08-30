# paper-audit 小节级审阅通道与窗口装配

父任务：`.trellis/tasks/08-30-subsection-context-polish`
共用契约：父任务 `design.md`
前置：`.trellis/tasks/08-30-subsection-cursor-zh` 先完成，本任务对齐其用词与三码。

## 目标

把 paper-audit 的最小审阅单元从「章节组」下沉到「小节」，让润色通道真正携带上一小节与
下一小节的上下文，**并把新 lane 接入 `audit.py` 的真实调度链**，而不是只写一段说明。

## 现状缺口

- `academic-writing-skills/paper-audit/scripts/prepare_review_workspace.py:112`
  `build_section_index` 用 `parser.split_sections()`，键是粗语义键，没有小节层。
- 同文件 `:19-27` 只导入 `read_text_robust`，`:223-253` 把**单个源文件的原始文本**交给
  `build_section_index`，不使用同目录已存在的
  `academic-writing-skills/paper-audit/scripts/tex_loader.py:167-171` 的 `assemble()`
  （携带 assembled-line → source 的 origin map）。多文件论文上标题数为 0。
- `split_sections()` 只保留可分类的语义 section；无关键词标题会被丢弃，这一差异记录在
  `academic-writing-skills/paper-audit/scripts/parsers.py:60-65` 的 `chapter_ranges` docstring。
- `academic-writing-skills/paper-audit/scripts/audit.py:224-264` 的 `FOCUS_TO_ALLOWED_LANES`
  与 `:275-291` 的 `ROLE_TO_REVIEW_LANES` 是 lane 是否被调度的真实开关；
  `:917-919,951-1002` 用它过滤 section 与 cross-cutting lane。
- `:2418-2425` 的 polish 路径直接进 `run_polish_precheck`，`:2330-2365` 只生成规则型 precheck
  state 并返回 `AuditResult`，没有任何小节窗口入口。
- `academic-writing-skills/paper-audit/references/POLISH_GUIDE.md` 末段的 subsection 切分只在
  > 1200 词时触发，切开后两侧互不可见邻接内容。

## 需求

### R-B1 装配式小节索引（TPR-01）

`prepare_review_workspace.py` 先用 `tex_loader.assemble()` 装配入口文档，在装配结果上用
`parser.extract_headings()` **全量枚举标题**（不经过 `split_sections()`），按父 `design.md` §1
构建单元，并经 origin map 得到 `source_file` 与文件内行号。

单元索引写入 `artifacts/data/subsection_index.json`（**独立文件**，不塞进
`section_index.json`；见「变更清单」与回滚约定）。`section_index.json` 增一个顶层伴随字段
`subsection_index_status`，取值 `"ok" | "no_depth3_headings" | "unsupported_format"`。

Typst 与 PDF 输入：显式降级为空单元列表 + `subsection_index_status: "unsupported_format"`，
不声称支持。

### R-B2 窗口装配

工作区新增 `artifacts/windows/<subsection_id>.json`，内容为父 `design.md` §2.4 的窗口对象，
只存部件与源坐标，**不复制正文**。Mentor 与 reviewer 用 `Read(offset, limit)` 取正文。

「合格段」用父 `design.md` §2.2 的 canonical eligibility，数值与 zh 侧相同，
英文正文用其中写明的等价投影，不由实现者自行决定。

### R-B3 新 lane 接入真实调度链（TPR-02，Route A）

文档层与代码层都要做：

**代码层**
- `audit.py:224-264` 的 `FOCUS_TO_ALLOWED_LANES["full"]` 与 `["logic"]` 加入
  `subsection_context_polish`。
- `audit.py:275-291` 的 `ROLE_TO_REVIEW_LANES["logic"]` 加入该 lane。
- `_write_lane_outputs`（`:951-1002`）**不为该 lane 生成脚本 fallback issue**
  （父 `design.md` §2.5：audit 侧 S-CTX 是 LLM 观察）；lane 通过 allowed 集合进入调度，
  其产物由 LLM subagent 写入 `artifacts/comments/subsection_context_polish.json`，
  checkpoint 用既有 `mark_lane_completed` 记录。
- polish 路径（`:2330-2365`）的 `precheck_data` 增 `subsection_windows` 键，
  列出窗口文件相对路径与每个单元的 editable / read_only 部件，供 Mentor 编排消费。

**文档层**
- `REVIEW_LANE_GUIDE.md` 增 `subsection_context_polish`（max 10 issues，职责边界）。
- `SUBAGENT_TEMPLATES.md` 增 focus block 与 DO/DON'T。

### R-B4 协议镜像文件（TPR-06）

新增 `academic-writing-skills/paper-audit/references/SUBSECTION_CONTEXT_PROTOCOL.md`，
是父 `design.md` §5 指定的**唯一 mirror 文件**，含 `<!-- S-CTX-CONTRACT:BEGIN -->` /
`<!-- S-CTX-CONTRACT:END -->` 契约块，内容与 zh canonical 文件规范化空白后完全相等。

`agents/section_reviewer_agent.md`、`REVIEW_LANE_GUIDE.md`、`SUBAGENT_TEMPLATES.md`、
`POLISH_GUIDE.md` **只写该文件的路径，不复制协议句**。

### R-B5 POLISH_GUIDE 切分改造

把「> 1200 词按 subsection 边界拆两个 Mentor」改为「按小节游标切分，每个 Mentor 调用携带该
小节的三元窗口」。保留 1200 词语义（超长小节仍需再切，切出的两半共享同一份 prev/next）。

### R-B6 ISSUE_SCHEMA 可选字段（TPR-03）

增两个 optional 字段：

- `subsection_id`：点分十进制串，如 `"2.1.1"`。
- `context_sides`：**列表**，取值域见父 `design.md` §2.5。原单值 `context_side` 不采用。

写明 S-CTX 类 issue 的 `source_kind` 恒为 `"llm"`、`severity` 为 `"minor"`（汇总项 `"moderate"`），
受 `academic-writing-skills/paper-audit/references/ISSUE_SCHEMA.md:5-14,30-38` 的枚举约束。
required 列表不变。

### R-B7 一致性锁

新增 `tests/contracts/test_subsection_context_contract.py`，按父 `design.md` §5 实现。

## 约束

1. 不改 `academic-writing-skills/paper-audit/scripts/parsers.py`；深度计算放在
   `prepare_review_workspace.py` 调用侧。
2. `section_index.json` 的既有字段与键名不变（只增一个顶层伴随字段）。
3. 不改 `SKILL.md` 的 `version`，只改 `last_updated`。
4. 新增/改动 references 必须同步 `docs/resource-manifest.json` 与双语页面。
5. `ISSUE_SCHEMA.md` 的 required 字段集合不变。
6. 不给 `audit.py` 加新 mode；新能力挂在既有 `polish` 与 `deep-review` 下。
7. 不新增脚本 fallback issue 生成器。

## 变更清单（TPR-09）

| 类别 | 路径 | 动作 | 步骤 |
| --- | --- | --- | --- |
| 脚本 | `academic-writing-skills/paper-audit/scripts/prepare_review_workspace.py` | 改：导入并调用 `assemble()`；新增 `build_subsection_units`；写 `subsection_index.json` 与窗口文件；`section_index.json` 增伴随字段 | S2、S3、S4 |
| 脚本 | `academic-writing-skills/paper-audit/scripts/paths.py` | 改：`WorkspaceLayout` 增 `subsection_index`、`windows_dir`、`window_file()` | S4 |
| 脚本 | `academic-writing-skills/paper-audit/scripts/audit.py` | 改：`FOCUS_TO_ALLOWED_LANES`、`ROLE_TO_REVIEW_LANES`、polish `precheck_data` | S5 |
| 资源 | `academic-writing-skills/paper-audit/references/SUBSECTION_CONTEXT_PROTOCOL.md` | 新增（mirror 契约文件） | S6 |
| 资源 | `academic-writing-skills/paper-audit/references/REVIEW_LANE_GUIDE.md` | 改：加 lane + 引用 mirror 路径 | S7 |
| 资源 | `academic-writing-skills/paper-audit/references/SUBAGENT_TEMPLATES.md` | 改：加 focus block + 引用 mirror 路径 | S7 |
| 资源 | `academic-writing-skills/paper-audit/agents/section_reviewer_agent.md` | 改：引用 mirror 路径（不复制协议句） | S7 |
| 资源 | `academic-writing-skills/paper-audit/references/POLISH_GUIDE.md` | 改：Context Window Management 段 | S8 |
| 资源 | `academic-writing-skills/paper-audit/references/ISSUE_SCHEMA.md` | 改：两个 optional 字段 + Guidance | S9 |
| 资源 | `academic-writing-skills/paper-audit/SKILL.md` | 改：路由说明 + `last_updated` | S10 |
| docs | `docs/resource-manifest.json` | 改：新增/改动 references 的 sha256 与页面映射 | S10 |
| docs | `docs/skills/paper-audit/resources/...` 与 `docs/zh/...` | 新增/改：mirror 与被改 references 的双语页面 | S10 |
| 测试 | `tests/contracts/test_subsection_context_contract.py` | 新增 | S11 |
| 测试 | `tests/skills/paper_audit/test_subsection_index.py` | 新增（索引、窗口、装配、降级） | S3、S4 |
| 测试 | `tests/skills/paper_audit/test_subsection_lane_wiring.py` | 新增（focus / role / polish state 矩阵） | S5 |

## 验收标准

- [ ] **AC-B-01**（R-B1）在多文件 fixture
      `academic-writing-skills/latex-thesis-zh/evals/fixtures/subsection-context/main.tex` 上，
      `subsection_index.json` 的编号序列等于写死的期望序列，且与 zh 侧输出相等。
- [ ] **AC-B-02**（R-B1）索引包含标题中**不含语义关键词**的小节，证明枚举未经过
      `split_sections()`。
- [ ] **AC-B-03**（R-B1）在既有
      `academic-writing-skills/latex-thesis-zh/evals/fixtures/thesis-project/main.tex`（无 `\subsection`）
      上，`subsection_index_status == "no_depth3_headings"`，单元列表为空，不回退到 depth-2。
- [ ] **AC-B-04**（R-B1）`.typ` 与 `.pdf` 输入下 `subsection_index_status == "unsupported_format"`，
      不抛异常。
- [ ] **AC-B-05**（R-B1、R-B2）窗口文件的 `source_file` 指向 `chapters/*.tex`，行号为文件内
      行号；用该坐标 `Read` 得到的文本确实是对应小节的开头。
- [ ] **AC-B-06**（R-B2）窗口 JSON 不含正文原句（对文档任意 20 字连续片段做子串检查）；
      部件数量按父 `design.md` §2.3 断言存在性与 `*_status`，不断言固定数量。
- [ ] **AC-B-07**（R-B3）运行态矩阵：`_selected_lanes_for_focus("full")` 与
      `_selected_lanes_for_focus("logic")` 含 `subsection_context_polish`；
      `"methodology"` 与 `"literature"` 不含；`ROLE_TO_REVIEW_LANES["logic"]` 含该 lane。
- [ ] **AC-B-08**（R-B3）`--mode polish` 写出的 state file 含 `subsection_windows` 键，
      其中每个单元有 editable 与 read_only 部件路径。
- [ ] **AC-B-09**（R-B3）`_write_lane_outputs` 不为该 lane 产出脚本 issue
      （`artifacts/comments/subsection_context_polish.json` 在无 LLM 参与时不存在）。
- [ ] **AC-B-10**（R-B4、R-B7）`SUBSECTION_CONTEXT_PROTOCOL.md` 的契约块与 zh canonical 文件
      规范化空白后完全相等；`REVIEW_LANE_GUIDE.md` / `SUBAGENT_TEMPLATES.md` /
      `section_reviewer_agent.md` / `POLISH_GUIDE.md` **不含**协议句正文，只含 mirror 路径。
- [ ] **AC-B-11**（R-B5）`POLISH_GUIDE.md` 的 Context Window Management 段已改为按小节游标
      切分并携带邻接上下文，1200 词语义保留。
- [ ] **AC-B-12**（R-B6）`ISSUE_SCHEMA.md` 增 `subsection_id` 与 `context_sides` 两个 optional
      字段，required 列表不变，且写明 S-CTX 的 `source_kind: "llm"` 与 severity 取值。
- [ ] **AC-B-13**（R-B7）`tests/contracts/test_subsection_context_contract.py` 通过，
      含 `S-CTX-DUP` 的负向断言。
- [ ] **AC-B-14**（全部）`docs/resource-manifest.json` 已同步改动文件的 `sourceSha256`，
      双语页面一致；`just ci` 全绿，pyright error 数不增加。
- [ ] **AC-B-15**（R-B3、承接父 AC-P-07）只读边界的行为核对已执行并记录，
      标注 **manual + UNVERIFIED**。
