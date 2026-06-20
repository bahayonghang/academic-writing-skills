# Design — 借鉴 4 项写作判断力资产

## 设计原则

- **文档优先，脚本最小**：①~④ 主体是判断力文档；唯一脚本改动是 ① 的 over-claim checker，
  复用现有 `AITraceChecker` 的扩展模式，不引入新框架。
- **三副本对齐但语境本地化**：en/typst 英文，zh 中文学位论文语境。结构对齐，措辞/示例各自地道。
- **不动解析器**：零 `parsers.py` 改动 → 不触发 `test_parsers_alignment`。

## 一、文件落点映射（三技能命名差异）

| 资产 | latex-paper-en (嵌套小写) | latex-thesis-zh (嵌套小写, 中文) | typst-paper (扁平大写) |
|---|---|---|---|
| ① 参考文档 | `references/evidence/over-claim-guard.md` | `references/writing/over-claim-guard.md` | `references/OVER_CLAIM_GUARD.md` |
| ① YAML | `references/deai/tone-thresholds.yaml` | `references/deai/tone-thresholds.yaml` | `references/AI_TONE_THRESHOLDS.yaml` |
| ① checker | `scripts/deai_check.py` | `scripts/deai_check.py` | `scripts/deai_check.py` |
| ② 结构级痕迹 | `references/deai/guide.md` | `references/deai/guide.md` | `references/DEAI_GUIDE.md` |
| ③ 修改顺序 | `references/modules/workflow.md` | `references/writing/writing-philosophy-zh.md` | `references/modules/WORKFLOW.md` |
| ③ 路由提示 | `latex-paper-en/SKILL.md` | `latex-thesis-zh/SKILL.md` | `typst-paper/SKILL.md` |
| ④ 维护声明 | `references/deai/tone-terms-en.md` | `references/deai/tone-terms-zh.md` | `references/AI_TONE_TERMS.md` |

> zh 无 `evidence/`、无 `modules/workflow.md`，故 ① 放 `writing/`、③ 放 `writing/writing-philosophy-zh.md`（已存在）。

## 二、① over-claim 脚本层设计

### 2.1 数据契约（tone-thresholds.yaml 新增段）

在现有 YAML 末尾追加（en/typst 英文词；zh 视情可仅保留英文词，因 zh 论文外文摘要/术语仍用英文，
但 zh 主要靠文档而非脚本，YAML 段保持与 en 一致即可，便于副本对齐）：

```yaml
# Over-claim trigger phrases -> conservative replacement.
# Emits [Script] LOW traces. Pattern is case-insensitive regex over visible prose.
overclaim:
  enabled: true
  categories:
    causal:
      "\\bcaused by\\b": "associated with / linked to"
      "\\bdrives\\b": "contributes to / is associated with"
      "\\bdetermines\\b": "influences / shapes"
      "\\bresponsible for\\b": "implicated in / associated with"
    novelty:
      "\\bfor the first time\\b": "to our knowledge, among the first to"
      "\\bunprecedented\\b": "substantial / notable"
    universality:
      "\\buniversally\\b": "across the cases studied"
      "\\bin all cases\\b": "in the cases studied"
    application:
      "\\bwill revolutionize\\b": "has potential implications for"
```

> 注意：`novel` / `robust` / `comprehensive` **已在** `term_thresholds` 计数管控，**不重复**进 overclaim，
> 避免双重触发。overclaim 只收 term_thresholds 未覆盖的**短语级**因果/首创/普适/应用陷阱。

### 2.2 checker 实现（deai_check.py）

复用现有模式（参照 `_check_throat_clearing` line 526 与 DEFAULT_THRESHOLDS line 50）：

1. `DEFAULT_THRESHOLDS` 增加 `overclaim` 默认块（YAML 缺失/不可解析时回退，与现有 checker 行为一致）。
2. `AITraceChecker.__init__` 预编译 overclaim 正则（仿 `self._throat_clearing_re`）。
3. 新增 `_check_overclaim(self, section_name) -> list[dict]`，trace dict 复用现有 schema：
   `{pattern, category:"overclaim", severity:"low", suggestion_type:"overclaim", suggestion, line, ...}`，
   provenance 走现有 `[Script]` 路径。
4. 在 `check_section`（line 312）追加 `results["traces"].extend(self._check_overclaim(section_name))`。
5. `enabled: false` 时整段跳过（给用户关闭开关）。

**不改** CLI 接口、不改输出格式、不改 scoring（overclaim 走 LOW，与现有 throat_clearing 同档）。

### 2.3 副本对齐

三份 `deai_check.py` 是有意副本（同 parsers 策略）。三份同步修改；改完核对 EN 为基准的逻辑一致。
若 `tests/` 有 deai 输出快照或 tone-thresholds 结构断言，需同步更新期望值。

## 三、②③④ 文档设计

- **② 结构级痕迹**：在 de-AI 指南 Category 列表后新增"Structural-Level Traces"小节，4 条 + 检测信号 +
  改写指引，全部标 `[LLM]`。zh 版中文化（如"过度声明式过渡""Discussion 无立场"）。
- **③ 修改三层顺序**：workflow/philosophy 文档新增"修改顺序：逻辑 → 句子 → 词汇（不可逆）"小节（~10 行），
  说明为何顺序反了白费功夫；SKILL.md 润色路由处加一句引导（如 "polish in order: logic → sentence → lexical"）。
- **④ 维护声明**：黑名单文件头部 frontmatter/注释加 `last_reviewed` + 维护节律 + 来源两条引用。

## 四、边界与兼容性

- 与 `claim-evidence-contract.md` 不冲突：分工写进 over-claim-guard 文档的"边界"小节互相 link。
- 与现有 `term_thresholds` 不重叠（见 2.1 注）。
- 关闭面：`overclaim.enabled: false` 可整体停用脚本检查，不影响其他 checker。

## 五、回滚形态

- 文档类（①doc/②/③/④）：纯新增/追加，`git checkout` 对应文件即回滚，无副作用。
- 脚本类（①script）：回滚 `deai_check.py` ×3 + YAML overclaim 段 ×3 + 新测试文件即可；
  因 `enabled` 开关与 YAML 回退，半完成状态也不会破坏现有 deai 流程。

## 六、风险

| 风险 | 缓解 |
|---|---|
| 三副本 deai_check.py 漂移 | 以 EN 为基准逐份 diff 核对；implement 中单列核对步骤 |
| 既有 deai 测试快照被新 trace 打破 | 先跑 `just test` 摸清受影响测试，再决定更新期望值 |
| zh 文档英文直译味 | zh 由"中文学位论文"视角重写示例，非翻译 en |
| SKILL.md 误 bump version | 只改 last_updated；提交前 grep version 三处与 pyproject 比对 |
