# C1 交付冻结清单（C2/C3 一字不差复用）

C1 已实现完毕。以下为冻结产物，C2/C3 直接取用；若需变更，**回到 C1 改再同步**，不允许子任务各自变形。

## 1. 两轴命名与取值

| 轴         | 参数名       | 取值                                              | 默认      |
| ---------- | ------------ | ------------------------------------------------- | --------- |
| 编辑目标   | `--goal`     | `grammar` / `clarity` / `concision` / `coherence` | `grammar` |
| 编辑幅度   | `--strength` | `minimal` / `moderate` / `restructure`            | `minimal` |

`--tier` 不动，仍为 `deai_check.py` 的检测灵敏度。

## 2. 四个契约字段（三方逐字一致，注释符按文档语言取 `%` 或 `//`）

```
% Changed:       <脚本可验证的变更事实，或 none>
% Protected:     <本行内被识别并跳过的受保护 token，或 none>
% Meaning-Check: <PRESERVED | NEEDS-LLM>
% Risk-Flags:    <none | not-assessed | lexical-substitution | whitespace-normalized | overstatement | ambiguity | terminology-drift | invented-claim>
```

对齐用四空格填充到 `Meaning-Check: ` 的宽度（见三方 SKILL.md 与模块文档示例）。

## 3. 分层规则

- `[Script]`：`Meaning-Check` **恒** `NEEDS-LLM`；`Risk-Flags` 只能取 `none` / `not-assessed` /
  `lexical-substitution` / `whitespace-normalized`，无其他可确定标记时兜底 `not-assessed`。
- `[LLM]`：可取 `PRESERVED` 与全闭集，但 `PRESERVED` 是提案不是事实。
- 改写不得升高措辞强度；升高即置 `overstatement`（仅 `[LLM]` 层可置）。

## 4. 适用范围三分法

- 纳入：EN/Typst `expression`、`grammar`、`sentences`、`translation`；ZH `expression`（C3 新建）。
- 仅 `[LLM]` 层：EN `section-writing` / `caption` / `adapt`；Typst `adapt`；三方 `deai`。
- 排除：见三方路由文档的逐项清单，**不靠默认**。

## 5. ZH `references/modules/expression.md` 的 over-claim 指针文案（C3 取用）

在 ZH 新建的 `references/modules/expression.md` 中原样放入以下两段（放在输出示例之后）：

```markdown
## 改写契约

本模块产出可直接替换原文的文本，适用改写契约。`[Script]` 层输出恒为 `Meaning-Check: NEEDS-LLM`，且只允许置规则可确定的标记（`none`、`not-assessed`、`lexical-substitution`、`whitespace-normalized`）；只有 `[LLM]` 层可提出 `PRESERVED`，且仍是待作者核对的提案。字段定义与 `Risk-Flags` 闭集见 `references/modules/routing-rules.md`。

改写不得升高措辞强度。把留有余地的表述换成更强的断言（"可能" → "能够"、"有助于" → "显著提升"）是过度声称，不是表达改善：保持原强度，或置 `Risk-Flags: overstatement` 并明确说明。判据见 [over-claim-guard.md](../writing/over-claim-guard.md)——只做词汇层替换建议，强度分级不在本模块重复实现。
```

C3 的契约测试无需重写字段断言：`tests/contracts/test_polish_contract_alignment.py` 的
`POLISH_MODULE_DOCS` 已登记 ZH 路径，文件一旦创建即自动纳入断言。

## 6. C1 实际改动面

- 三方 `SKILL.md`：Required Inputs（两轴 + 追问边界）、Output Contract 新增 `### Rewrite Contract`
  段、`last_updated` → 2026-07-27（`version` 不动）。
- 三方路由文档：EN/ZH `references/modules/routing-rules.md`、Typst
  `references/skill-routing-notes.md` 新增「改写契约适用范围 / 分层规则 / 编辑轴与追问边界」。
- 六个润色模块文档（EN `expression|grammar|sentences`、Typst `EXPRESSION|GRAMMAR|SENTENCES`）：
  契约字段示例 + over-claim 指针。
- 新增 `tests/contracts/test_polish_contract_alignment.py`（10 条，只断言文档）。
- 文档站：9 个源文件对应的 18 个双语页面 + `docs/resource-manifest.json` 9 处散列。

## 7. 留给 C2 的既有缺陷（C1 有意未动）

- Typst `references/modules/EXPRESSION.md` / `GRAMMAR.md` 末行链接 `../references/STYLE_GUIDE.md`、
  `../references/COMMON_ERRORS.md` 是坏链（从 `modules/` 出发会解析到 `references/references/`）。
  文档站已用链接重写绕过（`../STYLE_GUIDE.md`），**源文件仍坏**。C2 修源时，
  `docs/scripts/check_resource_sync.py` 的链接重写会自动不再需要——修完跑全量 checker 确认。
- EN `references/modules/grammar.md` 的输出示例 `% Revised:  we propose a method ...` 保留小写
  `we`，因为脚本当前确实输出小写。C2 修保大小写时同步改示例与两个文档站页面。
