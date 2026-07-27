# Implementation Plan: C2 EN + Typst 表达链路修复

## Phase 0: Review Gate

- [ ] C1 `design.md` 已冻结；本任务复用其 `--goal` / `--strength` / 四字段 / `Risk-Flags` 闭集。
- [ ] `design.md` 的 A/B/C 三档分级经评审确认，尤其：`make` / `very` / `kind of` 降为 B 档
      （只报告不自动替换）这一**默认行为变化**被接受。
- [ ] 确认 typst 三脚本走**整文件镜像**而非人工逐段同步。
- [ ] 记录基线哈希：三脚本 en/typst 当前 IDENTICAL。

## Phase 1: 文档矛盾修复（先做，零行为风险）

- [ ] EN `references/modules/expression.md`：替换表改为与脚本一致；加一段说明
      `use → employ` / `show → demonstrate` 因 E15 被删除的原因并指向 de-AI 指南（防"修回去"）。
- [ ] Typst `references/modules/EXPRESSION.md`：
  - [ ] 删除 `use`、`show` 两行；其余与脚本对齐
  - [ ] 修示例：`get → obtain`（当前误写 `achieve`）
  - [ ] 修坏链：`../references/STYLE_GUIDE.md` → `../STYLE_GUIDE.md`
- [ ] 核对 EN `references/deai/{forbidden-terms,tone-terms-en}.md` 与 Typst
      `references/AI_TONE_TERMS.md`，确认剩余替换规则无同类冲突；有则一并列出处置。
- [ ] 加 C1 供的 over-claim 指针文案到六个模块文档。

## Phase 2: 保护 token 单点清单

- [ ] 新建 EN `references/writing/protected-tokens.md`：按 design §1.2 写 A/B/C 三档类别表。
- [ ] 新建 Typst `references/PROTECTED_TOKENS.md`，规则同源。
- [ ] EN/Typst SKILL.md 的 Safety Boundaries 加**指针**（不复制清单内容）。

## Phase 3: 脚本修复（EN canonical）

- [ ] `improve_expression.py`：
  - [ ] 保大小写替换（句首大写、全大写缩写形态保持）
  - [ ] `make` / `very` / `kind of` 降为 B 档：只报候选，不产 `Revised:`
  - [ ] 移除 `re.sub(r"\s+", " ", ...)` 的无差别空白压缩
  - [ ] A 档保护 token 检出并跳过，记入 `Protected`
  - [ ] 追加四字段；`Meaning-Check` 恒 `NEEDS-LLM`
  - [ ] 加 `--goal` / `--strength`，默认 `grammar` / `minimal`
- [ ] `analyze_grammar.py`：保大小写修复（修掉 `grammar.md:19-22` 示例暴露的 `W` 丢失）+ 四字段
      + 两 flag。
- [ ] `analyze_sentences.py`：四字段 + 两 flag；**保留** `Suggested:` 字段名不动。
- [ ] `translate_academic.py`：追加 `### Contract` 小节（design §2.2）。
- [ ] 更新四个模块文档的 Output format 示例，与实际输出逐字一致。

## Phase 4: Typst 镜像（与 Phase 3 同 commit）

- [ ] `cp` 整文件：`improve_expression.py`、`analyze_grammar.py`、`analyze_sentences.py`
      EN → Typst。**不要**手工逐段改。
- [ ] Typst `translate_academic.py` 独立实现 `### Contract`（不在字节锁内）。
- [ ] 立即跑 `test_writing_modules_alignment` 确认三组哈希一致。

## Phase 5: 测试

- [ ] 反例回归（每条至少一例）：
  - [ ] `Make sure the model converges.` → 不产生 `develop sure`
  - [ ] `We make use of a pretrained encoder.` → 不产生 `develop use of`
  - [ ] `Only very few samples are available.` → 不产生 `highly few`
  - [ ] `The results  are  aligned in   a table.` → 空白未被压缩
  - [ ] 句首大写 token 替换后首字母仍大写
- [ ] 正例回归：`We get 92.1% accuracy on CIFAR-100.` → `obtain`，且 `92.1%` 与 `CIFAR-100`
      出现在 `Protected` 字段
- [ ] 契约字段测试：四脚本输出均含四字段，`[Script]` 层 `Meaning-Check` 恒 `NEEDS-LLM`
- [ ] **禁止**写 `makes it possible` 用例（已证伪，写了就是无效测试）
- [ ] 存量用例：B 档降级导致的断言变化同 commit 更新

## Phase 6: Validation

```bash
uv run --extra dev python -m pytest tests/contracts/test_writing_modules_alignment.py -q
uv run --extra dev python -m pytest tests/ -k "expression or grammar or sentences or translat" -q
git diff --stat -- '*/scripts/deai_check.py' '*/scripts/analyze_abstract.py' '*/scripts/parsers.py'  # 期望空
just ci
```

- [ ] commit message 对 B 档降级做**双声明**（属"误报修复"例外 + 列出受影响存量用例）。

## Rollback Points

- Phase 1-2 纯文档，可独立回滚。
- Phase 3 与 Phase 4 **必须同 commit**；单独回滚任一侧都会让 TIER1 字节锁变红。
- Phase 5 的测试与 Phase 3/4 同 commit，保证任一回滚点 CI 自洽。

## 已知陷阱

- 按成员级同步 typst 会漏空白/顺序差异，锁仍红 —— 只用整文件复制。
- 改 `evals.json` 走 Bash python 写入。
- 不给 pytest 加 `PYTHONIOENCODING=utf-8`。
- 只改 `last_updated`，不 bump `version`。
