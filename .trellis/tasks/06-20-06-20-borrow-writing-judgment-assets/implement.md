# Implement — 借鉴 4 项写作判断力资产

> 执行顺序：先文档（低风险、可独立验收）→ 后脚本（① script，含测试）→ 全量校验。
> 每个 checkpoint 给验证命令与回滚点。EN 为基准副本，zh/typst 镜像。

## 前置基线

- [ ] `just ci` 跑一次确认起点全绿（避免把既有红误算到本任务）
- [ ] `git switch -c feat/borrow-writing-judgment-assets`（在 dev 上开分支）
- [ ] 记录三处 SKILL.md 当前 `version`（用于结束前比对未被 bump）

验证：`uv run --extra dev python -m pytest -q` 起点通过。

---

## 阶段 A — ④ 维护声明（最小、先热身）

> 目标是 **AI 黑名单（tone-terms）**，非 protected `forbidden-terms.md`（后者是受保护术语，概念不同）。

1. EN：`latex-paper-en/references/deai/tone-terms-en.md` 加 `last_reviewed` + 维护节律 + 两条来源
   （Kobak et al., *Sci. Adv.* 2025；Geng & Trotta 2025）。
2. ZH：`latex-thesis-zh/references/deai/tone-terms-zh.md` 同（中文表述）。
3. Typst：`typst-paper/references/AI_TONE_TERMS.md` 同。

验证：`uv run --extra dev python -m pytest tests/ -q -k "forbidden or term"`（若无相关测试则跳过，靠下一阶段全量）。
回滚点：`git checkout -- <3 files>`。

---

## 阶段 B — ③ 修改三层顺序原则

1. EN：`references/modules/workflow.md` 加"修改顺序：逻辑→句子→词汇（不可逆）"小节；`SKILL.md` 润色路由加一句引导。
2. ZH：`references/writing/writing-philosophy-zh.md` 加同小节（中文）；`SKILL.md` 加引导。
3. Typst：`references/modules/WORKFLOW.md` 加小节；`SKILL.md` 加引导。
4. 三处 SKILL.md：更新 `last_updated`，**确认 `version` 未变**。

验证：`grep -n "^version" <3 SKILL.md>` 与 pyproject 一致；`grep -n last_updated` 已更新。
回滚点：`git checkout -- <6 files>`。

---

## 阶段 C — ② 结构级 AI 痕迹

1. EN：`references/deai/guide.md` 新增"Structural-Level Traces"小节（4 条 + 检测信号 + 改写指引，标 `[LLM]`）。
2. ZH：`references/deai/guide.md` 中文化新增。
3. Typst：`references/DEAI_GUIDE.md` 新增。

验证：人工通读 3 份小节结构对齐、zh 非直译。
回滚点：`git checkout -- <3 files>`。

---

## 阶段 D — ① over-claim 参考文档

1. EN：新建 `references/evidence/over-claim-guard.md`：动词梯子 + 7 替换表（因果/首创/普适/效应量/时序/应用/比较）
   + 陷阱句式表 + 与 `claim-evidence-contract.md` 边界小节（互相 link）。示例用 CS/通用语境。
2. ZH：新建 `references/writing/over-claim-guard.md`：中文学位论文语境重写示例。
3. Typst：新建 `references/OVER_CLAIM_GUARD.md`：英文。
4. 在各 SKILL.md 的 references 清单/路由表登记新文件（若该 SKILL.md 有显式文件索引）。

验证：检查 SKILL.md 引用的 references 路径无悬挂；若有 contract 测试校验 references 列表则同步。
回滚点：`git checkout -- <新建文件 + SKILL.md>`。

---

## 阶段 E — ① 脚本层（YAML + checker + 测试）

按 design §2 实施，EN 先行跑通再镜像：

1. **EN YAML**：`references/deai/tone-thresholds.yaml` 追加 `overclaim` 段（见 design 2.1）。
2. **EN checker**：`scripts/deai_check.py`
   - `DEFAULT_THRESHOLDS` 加 `overclaim` 默认块；
   - `__init__` 预编译 overclaim 正则；
   - 新增 `_check_overclaim(section_name)`；
   - `check_section` 追加调用；
   - 尊重 `enabled` 开关。
3. **EN 测试**：新建 `tests/test_deai_overclaim.py`
   - 导入 `from deai_check import AITraceChecker`（conftest 已把 SCRIPT_DIR_EN 上 sys.path）；
   - 喂含 "caused by" / "for the first time" 的文本 → 断言 emit overclaim trace，severity=low，provenance=[Script]；
   - 喂干净文本 → 断言无 overclaim trace；
   - YAML overclaim 缺失/`enabled:false` → 断言回退/跳过不报错。
4. **跑 EN 测试**：`uv run --extra dev python -m pytest tests/test_deai_overclaim.py -q` 通过。
5. **镜像 ZH**：`latex-thesis-zh/references/deai/tone-thresholds.yaml` + `scripts/deai_check.py` 同步改动。
6. **镜像 Typst**：`typst-paper/references/AI_TONE_THRESHOLDS.yaml` + `scripts/deai_check.py` 同步改动。
7. **副本核对**：以 EN 的 `_check_overclaim` 为基准 diff zh/typst 两份逻辑一致（仅路径/命名差异）。

验证：`uv run --extra dev python -m pytest academic-writing-skills/*/tests/ tests/ -q -k deai` 通过。
回滚点：`git checkout -- scripts/deai_check.py(×3) tone-thresholds yaml(×3) tests/test_deai_overclaim.py`。

---

## 阶段 F — 全量校验与收尾

1. `just fix`（ruff format + --fix）。
2. `just ci`（lint → typecheck → test）**全绿**。
   - 若既有 deai 快照测试被新 trace 打破 → 按 design §六 摸清后更新期望值（确认是预期新增而非回归）。
3. 验收清单逐条核对 prd.md。
4. 确认范围外技能未改：`git diff --name-only` 不含 `paper-audit/` `cover-letter/` `bib-search-citation/`。
5. 确认 3 处 SKILL.md `version` 未变、`last_updated` 已更新。

---

## 提交

- 按 skill 切分 commit（项目惯例 scoped conventional commits），或单 commit
  `feat(skills): borrow over-claim guard / structural de-ai traces / revision-order / blacklist cadence`。
- 提交信息含 `[AI]` 标记与 Why 行；不自动 push（等用户确认）。
- 不在本任务做：⑤时态、⑥reviewer、paper-audit over-claim 维度（建独立 follow-up 任务）。

## 校验命令速查

```bash
just ci                                                    # 全量
uv run --extra dev python -m pytest tests/test_deai_overclaim.py -q
uv run --extra dev python -m pytest -q -k deai             # de-AI 相关
git diff --name-only                                       # 范围核对
```
