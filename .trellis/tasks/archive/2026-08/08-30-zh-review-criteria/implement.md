# Implement — 中文审阅准则文档与 reviewer agent

前置：C1 `.trellis/tasks/08-30-zh-dispatch-wiring` 已完成并提交。读 `prd.md` 与 `design.md`。

## 命令约定（TPR-12）

PowerShell 与 POSIX shell 均可直接执行的形式。**不要用 `tail`、`head`、heredoc（`python - <<'PY'`）**。

```
uv run --extra dev python -m pytest tests/contracts/ -q
uv run --extra dev python -m pytest tests/skills/paper_audit/ -q
just ci
```

需要读长输出时写文件再看：`just ci > ci.log 2>&1`，用 Read 打开 `ci.log`。
需要临时脚本时写成 `.py` 文件用 `uv run --extra dev python <file>` 执行，或用 `python -c "..."` 单行形式。

## 阶段 0 — 前置确认

**0.1** 确认 C1 实际落地的检查器与模块映射（design §1 的 `[Script]` 档要对齐真实结果，不是 C1 的计划）：

```
python -c "import re,pathlib;s=pathlib.Path('academic-writing-skills/paper-audit/scripts/audit.py').read_text(encoding='utf-8');print([m for m in re.findall(r'\"(spec|blind|abstract|conclusion|literature|tables)\":\s*\"[^\"]+\"',s)])"
python -c "import sys;sys.path.insert(0,'academic-writing-skills/paper-audit/scripts');from scholar_eval import MODULE_DIMENSION_MAP as M;print(sorted(M))"
python -c "import sys;sys.path.insert(0,'academic-writing-skills/paper-audit/scripts');from audit import ZH_EXTRA_CHECKS as Z;print(Z)"
```

**0.2** 实测 `blind_review` 字段语义（design §4.4，R3.17）：

```
python -c "import re,pathlib;s=pathlib.Path('academic-writing-skills/paper-audit/scripts/audit.py').read_text(encoding='utf-8').splitlines();print('\n'.join(f'{i+1}: {l}' for i,l in enumerate(s) if 'blind_review' in l))"
```

读全部消费点，判定该字段控制什么。**结论写回 `design.md` §4.4，再动配置**（AC6-4）。

**0.3** 记录基线：

```
just ci > ci-baseline.log 2>&1
python -c "import json;m=json.load(open('docs/resource-manifest.json',encoding='utf-8'));print(len([r for r in m['resources'] if r['skill']=='paper-audit']))"
```
manifest 条目应为 58。

## 阶段 A — 准则文档与 agent（AC5-1 / AC5-2）

**A1** 写 `academic-writing-skills/paper-audit/references/ZH_THESIS_REVIEW_CRITERIA.md`：

1. Scope / 何时读（写明不适用于英文小论文）
2. **三集合辨析节**（design §1 首表）：8 个基础评分维度 / 1 个派生 `overall_base` / 15 行中文审阅指标。明确 `scoring_model.py` 的 `# 9 base dimensions` 注释不准（TPR-10）
3. **15 行**中文审阅指标表（design §1 主表），逐行标基础维度、权重、`[Script]` / `[LLM]` 档位、承载脚本与 module 名
4. 档位纪律节：5 个 `[LLM]` 行（1、3、5、6、14）不得新增正则代理判定；工作量与创新性不得用篇幅、图表数、公式数、参考文献数代理
5. 硕士 / 博士创新性与工作量标准差异（reviewer 判断依据）
6. 学位论文评阅人阅读路径（先结构完备性与工作量，后创新性），与 `REVIEWER_PSYCHOLOGY.md` 的期刊审稿人路径对照
7. 与既有参考的边界表（design §2）
8. 方法叙述边界指路（`latex-thesis-zh --method-narrative --section`，与 `SKILL.md:68` 一致）
9. 不产出评阅等级的取舍说明（design §3）
10. 中文伪代码不在表内的说明（C1 判定 `check_pseudocode.py` 非语言中性，本地化属范围外）

正文为中文（`sourceLocale: "zh"`）。引用 `quality_rubrics.md` 的权重，不复制其分档文字。

**A2** 写 `academic-writing-skills/paper-audit/agents/zh_thesis_reviewer_agent.md`。先读两个既有 cross-cutting lane agent 作结构参照：

```
Read academic-writing-skills/paper-audit/agents/claims_evidence_reviewer_agent.md
Read academic-writing-skills/paper-audit/agents/self_consistency_reviewer_agent.md
```

按 design §3 的表填 persona / lane 名 / 选择条件 / 输入 / 输出 / 退出条件 / `Output limit`，复述红线，写明不产出评阅等级。

## 阶段 B — lane 接线（AC5-3，TPR-07）

**仅登记文件不会让 agent 被调用。** 逐个入口改，每个配至少一条断言。

| # | 入口 | 改动 |
|---|---|---|
| B1 | `references/REVIEW_LANE_GUIDE.md` | 新增 `zh_thesis_review` cross-cutting lane 定义与选择条件 |
| B2 | `references/SUBAGENT_TEMPLATES.md` | 新增该 canonical lane 的 focus 块（`Focus` / `DO` / `DON'T` / `Output limit`），位置与既有块并列（`:58` 起的"Lane-specific focus blocks"节） |
| B3 | `references/MODE_GUIDE.md:174` Phase 3B | lane 清单加入并标注 `lang == "zh"` 门控 |
| B4 | `scripts/audit.py:924` `_selected_lanes_for_focus` | `full` / `editor` focus 的 lane 集合加入新 lane |
| B5 | `scripts/audit.py:949` `_register_json_lane_artifact` / `_write_lane_outputs` | 新 lane 产物登记 |
| B6 | `scripts/audit.py:792` `_fallback_cross_cutting_issues` | 新 lane 缺失时的 fallback 分支 |
| B7 | `scripts/audit.py:929` `_load_completed_lanes` | checkpoint 恢复识别新 lane 名；旧 workspace 无该文件时按未完成处理，不报错 |
| B8 | `scripts/consolidate_review_findings.py` | 接受新 lane 名并并入汇总 |

**B9** 登记面（**按类型分开**，TPR-07）：
- `SKILL.md ## References` 加 `ZH_THESIS_REVIEW_CRITERIA.md`
- `SKILL.md ## Reviewer Lanes` 加 agent 一行摘要
- `references/agent-roster.md` 加 agent 一行（**不加参考文件**）
- `SKILL.md` frontmatter：`last_updated` 改为落地日期，**`version` 不动**

**B10** 测试：
- 参考文件不在 `agent-roster.md`（AC5-3 的显式断言）
- B1–B8 每个入口至少一条断言：lane 名出现在该入口、`_selected_lanes_for_focus("full")` 含新 lane、非中文输入时不选中、fallback 分支可达、checkpoint 能识别、consolidation 接受

**校验**
```
uv run --extra dev python -m pytest tests/contracts/test_skill_contracts.py tests/contracts/test_skill_versions.py -q
uv run --extra dev python -m pytest tests/skills/paper_audit/ -q
```

**提交点 1**：`feat(paper-audit): ✨ 新增中文学位论文审阅通道与评阅准则`

## 阶段 C — 文档站同步（AC5-4）

**C1** 两个新文件登记进 `docs/resource-manifest.json`（字段形态照抄既有条目），design §6 表中的六个改动文件更新 `sourceSha256`。

**不用 `Edit` / `Write` 改这个 JSON**——格式化 hook 会压平数组。写临时 `.py` 文件：

```
# tmp_manifest_update.py，跑完删除
# 读 -> 改 -> 按既有 indent 写回；sha256 用 hashlib.sha256(path.read_bytes()).hexdigest()
```
执行：`uv run --extra dev python tmp_manifest_update.py`

**C2** 产出四个目标页面（两个新文件 × EN/ZH）。`sourceLocale: "zh"` 表示 zh 页面忠实转载、en 页面完整英译。**不留占位文本**。

**C3** 校验
```
just ci > ci-docs.log 2>&1
python -c "import json;m=json.load(open('docs/resource-manifest.json',encoding='utf-8'));print(len([r for r in m['resources'] if r['skill']=='paper-audit']))"
```
条目数应为 60。

**提交点 2**：`docs(paper-audit): 📝 同步中文审阅资源双语页面`

## 阶段 D — venue 配置与三集合关系（AC6-1 ~ AC6-4）

**D1** 按阶段 0.2 的实测结论处理 `blind_review` 字段（AC6-4）。

**D2** 扩充 `VENUE_CONFIG["thesis-zh"]`（**单数**，`scripts/audit.py:359`-`:367`）的 `extra_checks`，按 design §4.1 的裁定表：
- **收**：中文摘要 + 英文摘要、中文关键词 + 英文关键词（现有 3 条保留）
- **不收**：附录存在性、符号表存在性（模板标为可省 / 条件项，TPR-03）
- **不加** `required_sections`（无运行时消费者，TPR-04）
- **不设** `page_limit`，理由写入 `VENUE_RULES.md`

每条新正则对至少两种模板实测，素材：
```
Read academic-writing-skills/latex-thesis-zh/templates/yanshan.md
Read academic-writing-skills/latex-thesis-zh/templates/pkuthss.md
```

**D3** 为每个 `extra_checks` 项加稳定 ID `TZ-EC-<slug>`；扩充 `references/CHECKLIST.md` 的 Chinese Thesis 节，每项加 `TZ-CL-<slug>`；附录与符号表进 `CHECKLIST.md` 作**人工判断项（条件必备）**，不进 `extra_checks`。

**D4** 扩充 `references/VENUE_RULES.md`（`:12` 一行 → 独立小节），逐条给出 `TZ-EC-*` / `TZ-CL-*` 的依据说明，含不设 `page_limit` 的理由。

**D5** 新增 `tests/contracts/test_thesis_zh_venue_consistency.py`，断言 design §5 的三条**方向关系**：
1. 每个 `TZ-EC-*` 在 `CHECKLIST.md` 有 `TZ-CL-*` 对应项
2. 每个 `TZ-EC-*` 在 `VENUE_RULES.md` 有依据说明
3. 反向不要求（`CHECKLIST.md` 可含纯人工项）

**不断言集合相等**（TPR-04）。用语义 ID 锚定，不用行号或整数序号。结构参照：
```
Read tests/contracts/test_spec_checklists.py
Read tests/contracts/test_venue_templates_layout.py
```

**D6** 断言 `VENUE_CONFIG["thesis-zh"]` 不含附录 / 符号表存在性检查（AC6-2），测试注释引用模板证据（`yanshan.md:52`-`:53`、`pkuthss.md:25`/`:106`）；断言不含 `required_sections` 字段（AC6-3）。

**D7** 更新 `VENUE_RULES.md` / `CHECKLIST.md` 的 manifest `sourceSha256`（同 C1 方式）。

**提交点 3**：`feat(paper-audit): ✨ 扩充 thesis-zh venue 配置与覆盖关系校验`

## 阶段 E — 集成验收（父任务 AC7 / AC8）

**E1**
```
just fix
just ci > ci-final.log 2>&1
```
全绿，测试数不低于阶段 0.3 基线。

**E2** AC8 按 **C1 建立的 fixture manifest** 逐行验收（TPR-08），不用单一 fixture 承担全部断言。至少三条：

| 用例 | 命令 | 期望 |
|---|---|---|
| F1 正例 | `--mode gate --venue thesis-zh` | D2（作者信息）与 D3（规范失败项）进入阻断集 |
| F3 可选章节缺失 | `--mode gate --venue thesis-zh` | **不 FAIL**——附录与符号表缺失不得阻断（TPR-03） |
| F1 正例 | `--mode deep-review --venue thesis-zh` | `comments/zh_thesis_review.json` 产出且进入 consolidation |

命令形式（Windows 下重定向 JSON 须设编码，但不要 `export` 到全局）：
```
cd academic-writing-skills/paper-audit
uv run python -B scripts/audit.py <fixture.tex> --mode deep-review --venue thesis-zh > dr.log 2>&1
uv run python -B scripts/audit.py <fixture.tex> --mode gate --venue thesis-zh > gate.log 2>&1
```
断言对象是 `(module, severity, gate_blocker)` 三元组集合，不做整份报告文本快照。

**E3** 把 E2 的实测输出摘要写回本文件"验收记录"，父任务据此关闭 AC7 / AC8。

## 陷阱清单

| 陷阱 | 规避 |
|---|---|
| `tail` / heredoc | PowerShell 不支持；用上文"命令约定"的形式（TPR-12） |
| `docs/resource-manifest.json` | 格式化 hook 压平数组 → 写临时 `.py` 文件执行 |
| `SKILL.md` 路由表 | 格式化 hook 对齐表格会触发 `ROUTER_ROW_RE` contract 测试；只改正文 |
| `SKILL.md` `version` | 全仓同步规则；单 skill 任务不 bump，只改 `last_updated` |
| 只登记 agent 文件 | 不会被调度；必须走阶段 B 的 8 个入口（TPR-07） |
| 参考文件进 agent roster | `agent-roster.md` 只登记 `agents/` 下的真实 agent（TPR-07） |
| `VENUE_CONFIGS` | 真实符号是单数 `VENUE_CONFIG`（TPR-04） |
| 附录 / 符号表进 `extra_checks` | 会被标成必需项并阻断合法论文（TPR-03） |
| 维度数量口径 | 8 基础 + 1 派生 + 15 指标行，三者不混（TPR-10） |
| pyright | `basic` 模式下 `reportOptionalOperand` 等仍是 error 会卡 `just ci`；看 error 数不是 warning 数 |
| 越权改构建配置 | 不改 `justfile` / `pyproject.toml` / `uv.lock` |

## 验收记录

- [ ] 阶段 0.1 C1 落地检查器 = ____；`MODULE_DIMENSION_MAP` 键数 = ____
- [ ] 阶段 0.2 `blind_review` 语义结论 = ____（已回写 design §4.4）
- [ ] 基线：`just ci` 测试数 = ____，manifest paper-audit 条目 = 58
- [ ] AC5-1（指标表 15 行） / AC5-2 / AC5-3（8 个 lane 入口 + 登记面分离） / AC5-4（条目 = 60）
- [ ] AC6-1（三条方向关系） / AC6-2 / AC6-3 / AC6-4
- [ ] AC7-1 / AC7-2（`just ci` 测试数 = ____）
- [ ] AC8：F1 gate 阻断集 = ____；F3 gate 结论 = ____；F1 deep-review lane 产物 = ____
