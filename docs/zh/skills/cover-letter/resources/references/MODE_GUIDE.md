# 模式指南

五种投稿信模式的每种模式工作流程详细信息。单一命令
表面为`scripts/cover_letter.py --mode <mode>`；它接受的唯一标志
是 `--mode`、`--manuscript`、`--letter`、`--journal`（别名 `--venue`）和
`--json`。 `align-check` 作为 `generate` 内部的默认功能运行，并且
`optimize`。

## 模式1：`generate`

**触发**：用户有 `main.tex` 稿件，想要从头开始写一封投稿信。

**输入**：

- `--manuscript <main.tex>`（必填；`\input`/`\include`骨架自动组装）
- `--journal <venue-name>`（以下之一：nature、science、cell、ieee-trans、acm、springer-lncs、neurips、icml、cvpr、generic）
- `--json` 用于结构化输出（事实 blob + 确定性草稿支架）

**工作流程步骤**：

1. `cover_letter.py --mode generate` 运行 `extract_manuscript_facts`（标题、摘要、贡献、作者、通讯作者、章节锚）并发出确定性的草稿支架。
2. 请阅读 `templates/<journal>.md` 了解层级策略和所需声明。
3. 阅读 `references/LETTER_STRUCTURE.md` 了解五段支架。
4. 请阅读 `references/JOURNAL_TIERS.md` 了解特定于层的成帧规则。
5. 克劳德综合了这封信的散文，在每个部分都填充了事实和该层的风格指南。
6. **默认对齐检查集成**：如果合成的字母保存到文件中，则对其运行 `--mode align-check`；任何 `claim_accuracy` 与 `claim_strength: unsupported` 的问题必须在提交信件之前得到解决。
7. 对最终字母和表面结果（声明、长度、陈词滥调、语气）运行 `--mode presubmission`。

**输出**：投稿信文本，加上 `% PRESUBMISSION` 和 `% ALIGNCHECK` 注释块，列出所有未解决的发现。

## 模式2：`optimize`

**触发器**：用户已有投稿信草稿并希望对其进行改进。

**输入**：

- `--letter <cover_letter.md|.tex>`（现有草案）
- `--manuscript <main.tex>`（推荐；启用对齐检查通过）
- `--journal <venue-name>`（告知层级策略）
- `--json` 用于结构化输出

**工作流程步骤**：

1. `cover_letter.py --mode optimize` 运行 `presubmission_check` 和（当给出 `--manuscript` 时）`align_check`。
2. 阅读 `templates/<journal>.md` 了解层级策略。
3. 克劳德建议将章节级重写为 LaTeX 注释差异建议（绝不是源代码编辑），每个都锚定到原始信件中的一行。
4. 任何引入新声明的重写都必须通过对齐检查（追踪论文稿件证据或标记为用户验证）。
5. 对保存到文件的建议重写重新运行 `--mode align-check`，以确认没有回归。

**输出**：对原始信件的 LaTeX 评论审查，包括严重性/优先级/建议重写。

## 模式3：`align-check`

**触发器**：用户明确想要验证投稿信相对于论文稿件没有过度夸大。

**输入**：

- `--letter <cover_letter.md|.tex>`
- `--manuscript <main.tex>`
- `--json` 用于机器可读输出

**工作流程步骤**：

1. 阅读这两个文件（论文稿件由 `\input`/`\include` 组成）。
2. 构建论文稿件锚定集 (`extract_manuscript_facts`)。
3. 从信件中提取声明候选者 (`build_letter_claim_map`)；当候选人数量超过详细上限时，声明地图会报告 `total_claim_sentences` 和 `truncated`。
4. 根据论文稿件 (`verify_letter_against_manuscript`) 验证每个声明的引用：完全匹配、段落本地数字+度量共现或 4 克。
5. 使用 `claim_strength` 对每个声明进行分类，并使用简化的 ISSUE_SCHEMA 发出结果。
6. 交叉检查信件和论文稿件之间AI 披露的一致性：如果一份文件披露了生成人工智能的使用（或不使用），而另一份文件保持沉默，或者两者在极性上相矛盾，则发出 `moderate` `disclosure_consistency` 结果。阅读这两个文档时，`%` 注释已被删除，因此注释掉的声明不算在内。

**输出**：声明准确性结果，每个结果都带有字母引用、论文稿件锚点（或 `none`）和推荐的 `allowed_wording`；当两份文件在AI 披露问题上存在分歧时，最多加上一项 `disclosure_consistency` 调查结果。

## 模式4：`journal-fit`

**触发器**：用户想知道信件的框架是否适合目标地点。

**输入**：

- `--letter <cover_letter.md|.tex>`
- `--venue <venue-name>`（`--journal` 的别名）
- `--json` 用于结构化输出

**工作流程步骤**：

1. 读这封信。
2. 请阅读 `templates/<venue>.md` 了解等级和场地期望。
3. 阅读 `references/JOURNAL_TIERS.md` 了解层级策略。
4. `journal_fit_check` 分为四个子轴：
   - `scope_fit`：这封信是否指明了场地的范围尺寸？
   - `novelty_framing`：新奇的音高是否针对该层进行了校准？
   - `evidence_density`：声明密度是否符合场地预期？
   - `format_compliance`：字数、必需声明、禁止短语。
5. 总体结论=最差子轴（任何地方都是低→低；如果有的话则为中；只有当所有四个都为高时才为高）。

**启发式限制（向用户披露）**：`journal-fit` 是 `[Script]` 启发式，而不是编辑判断。 `scope_fit` 匹配每个地点的一个小的固定关键字集，因此短语范围不同的目标明确的字母可以读取 LOW； `evidence_density` 仅计算第一人称主张句子（“我们报告/显示/...”），因此被动或第三人称框架会低估。将判决视为检查框架的提示，而不是大门。此模式下不读取稿件内容。

**输出**：每轴判决（高/中/低），以引号作为证据；总体判决；每轴建议。

## 模式5：`presubmission`

**触发器**：用户只需要声明、长度、陈词滥调和语气检查。

**输入**：

- `--letter <cover_letter.md|.tex>`
- `--journal <venue-name>`（启用模板驱动的声明和长度检查）
- `--json` 用于结构化输出

**工作流程步骤**：

1. 读取该字母（`errors="replace"`，因此非 UTF-8 字母不会崩溃）。
2. 加载活动模板的 frontmatter （无 PyYAML 依赖项）。
3. 扫描：破折号 (`G1`)、AI 音调频率 (`AI*`，2 = 小调 / 3+ = 大调)、多样化 AI 音调词汇 (`AI-DIV`)、平行段落开头 (`S1`)、统一句子长度 (`S2`)、开场陈词滥调 (`L2*`)、禁用短语(`J1*`)、通用短语 (`J4*`)、必需/可选声明 (`D-*`)、长度 (`L1`)、段落形状 (`G2`/`G3`)。
4. 没有检测器的声明会发出信息 `D-<kind>-unknown`（必需）或被跳过（可选），而不是错误的“不存在”。

**输出**：演示/声明/语气调查结果列表。

## 模式积分矩阵

| 模式 | 呼叫 `extract_manuscript_facts` | 呼叫 `align_check` | 呼叫 `presubmission_check` | 呼叫 `journal_fit_check` |
| --------------- | -------------------------------- | -------------------------- | --------------------------- | ------------------------- |
| `generate` | 始终 | 始终（合成后） | 始终（最终通过） | 可选 |
| `optimize` | 如果提供 `--manuscript` | 如果提供 `--manuscript` | 始终 | 可选 |
| `align-check` | 始终 | 始终 | 无 | 无 |
| `journal-fit` | 否 | 否 | 否 | 始终 |
| `presubmission` | 无 | 无 | 始终 | 无 |

## 路由规则

- 仅当未提供现有字母时才默认为 `generate`。
- 当同时提供信件和论文稿件且用户未指定模式时，默认为 `optimize`。
- `align-check` 和 `journal-fit` 是仅显式的 — 按名称调用它们。
- 如果用户要求“查看我的投稿信”而不指定模式，则更喜欢 `optimize`（它已经运行对齐检查 + 预提交）。
