# Paper Writing Studio

Paper Writing Studio 是一个按投稿 venue 路由的学术写作润色 skill。它把 Nature 参考 skill 的证据保护与多节编排，和本仓库基于 Zotero 语料整理的 IEEE、Elsevier 写法分成独立 profiles，避免把一种刊物的句式误当成通用规则。

## 安装与使用

在本仓库中直接使用：

```powershell
python -m pytest academic-writing-skills/paper-writing-studio/tests/test_core.py -q
```

作为 agent skill 安装时使用仓库的标准安装流程。自然语言示例：

```powershell
npx skills add <owner/repository>
```

你可以直接这样说：

- “按 Nature 风格润色这个 abstract，保留数字和引用。”
- “按 IEEE Transactions 的 introduction 改写，检查 Related Work 和 contributions。”
- “按 Elsevier 过程控制论文的 experiments 改写，不要套用 Nature 的 Here we。”
- “没有目标期刊，先用中性学术英文润色，并列出缺失的 venue 证据。”

输入包含 `input_text`、`target`，以及可选的 `venue`、`journal`、`domain`。选择优先级为显式 venue、journal allowlist、明确 domain，最后才是 `unspecified` 中性基线。冲突会写入 summary，不静默猜测。

## Profiles 与证据

| profile | 适用范围 | 只读来源 | 特有边界 |
| --- | --- | --- | --- |
| `nature` | Nature 风格的单节或整稿润色 | `ref/nature-writing-studio/skill/` | anti-AI、em-dash、跨节上下文和证据分级留在本 profile |
| `ieee` | IEEE Transactions 等工程论文 | `materials/IEEE/` | self-reference、Related Work 路由和 `core`/candidate 门留在本 profile |
| `elsevier` | Elsevier 过程控制与工程论文 | `materials/Elsevier/` | domain-journal 路由、统计门和结论收束留在本 profile |

三套 profile 的 source path、provenance、section load order 和 TSV 不合并。`candidate` 行只记录为候选证据，不能提升为已应用规则。catalog installs、GitHub stars 和本地 fixture 都不是质量评分。

- `profiles/nature.json` 指向 `ref/nature-writing-studio/skill/`，保留反编造、em-dash、shared context 和跨节审计机制。
- `profiles/ieee.json` 指向 `materials/IEEE/`，只使用对应 section 的 reference 与 `core`/统计门控规则。
- `profiles/elsevier.json` 指向 `materials/Elsevier/`，只使用对应 section 的 reference 与 `core`/统计门控规则。

这些 source path 是本开发仓库中的只读证据边界；独立复制 skill 后若没有来源快照，profile 不能声称已经加载语料，应返回 degraded/missing evidence。不会把三套 TSV 合并，也不会把 catalog installs 或 GitHub stars 当作质量评分。

输出默认是 inline Markdown，包含 `text`、`text_compact` 和 summary。summary 记录 venue、profile version、section、规则/模式 ID、evidence rows、保护 token、冲突和 degraded 状态。无法确认来源时保留 `missing_evidence`，不回退到另一个 venue。skill 不负责 LaTeX/Typst 排版、编译、BibTeX、Zotero 写入、格式检查、未授权文件写出或补造数字、引用、实验结果。

## 验证

```powershell
python .agents/skills/qiaomu-meta-skill/scripts/validate_skill.py academic-writing-skills/paper-writing-studio
python .agents/skills/qiaomu-meta-skill/scripts/trigger_eval.py academic-writing-skills/paper-writing-studio --cases evals/trigger_cases.json --output reports/trigger-eval.json
python .agents/skills/qiaomu-meta-skill/scripts/export_skill_ir.py academic-writing-skills/paper-writing-studio --output reports/skill-ir.json
uv run --extra dev python -m pytest academic-writing-skills/paper-writing-studio/tests -q
python -X utf8 academic-writing-skills/paper-writing-studio/evals/output_contract_eval.py
uv run python docs/scripts/check_resource_sync.py --inventory-only
```

`evals/trigger_cases.json` 覆盖三种 venue、未指定 venue、单节/整稿、中译英和学术英文润色，以及排版、编译、Zotero、格式检查和未授权文件输出的负边界。`evals/output_contract_cases.json` 覆盖 alias、journal 冲突、candidate、保护 token、anti-AI、degraded 与 `text_compact`。该包没有公开的 `references/`、`templates/`、`examples/` 或 Markdown `agents/` 资源，因此资源同步检查使用 `--inventory-only` 验证仓库清单；报告是 `recorded_fixture` 和纯本地 core 证据；provider、真实论文、人审和干净安装仍标为 `missing evidence`。

## Troubleshooting

- 如果 venue 与 journal 冲突，显式 venue 获胜，summary 会保留冲突。
- 如果没有安全的 venue/journal/domain 映射，使用 `unspecified`，不要猜测。
- 如果 profile source path 不存在，保留 degraded 状态并报告缺失证据；不要回退到其他 venue 的 TSV。
- 本地 fixtures 和静态报告只能证明包结构、路由和 token 保护。真实 provider 输出、独立安装、真实论文风格相似度和人工编辑接受度目前是 `missing evidence`。

Copyright (c) 向阳乔木  
X: https://x.com/vista8  
GitHub: https://github.com/joeseesun/

Upstream inspiration: ref/nature-writing-studio plus local IEEE and Elsevier Zotero-derived materials.
