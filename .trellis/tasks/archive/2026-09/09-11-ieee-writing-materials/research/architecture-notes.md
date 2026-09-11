# 参考架构笔记

## nature-writing-studio（`ref/nature-writing-studio/skill/`）

可执行知识包，不是散文目录。

```
skill/
  SKILL.md
  knowledge/*.tsv
  prompts/system_writer.txt, style_guide.txt, sections/*.txt
  scripts/run_e2e_sanity.py
  docs/ROADMAP_v3.md
  fixtures/
```

蒸馏机制：

- 逐篇 observation，再聚合成 TSV
- 行带 `paper_count`、`top_papers`、`exemplar_quote`
- 五类信号：节首 3-gram、节内转折、动词证据强度、跨节衔接、results 段首
- `PROVENANCE.md` 记录论文数与生成日期
- 禁止把 Nature 先验行直接当作 IEEE 规则（`Here we`、methods last、Extended Data Fig.）

TSV 表头（落地时按 IEEE 章节改 section 枚举）：

| 文件 | 关键列 |
| --- | --- |
| writing_rules.tsv | rule_id, category, description, paper_count, severity, exemplar_quote, primary_section |
| phrase_bank.tsv | phrase_id, slot, phrase, paper_count, usage_note |
| opener_distribution.tsv | section, opener_3gram, total_occurrences, paper_count |
| gap_transitions.tsv | section, pivot_word, template, occurrences, paper_count, exemplar_quotes |
| hedge_verbs.tsv | verb, tier, total_occurrences, paper_count, exemplar_quotes |
| cross_section_linkers.tsv | from_section, to_section, pattern, occurrences, paper_count |
| results_discussion_openers.tsv | section, opener_template, total_occurrences, paper_count |
| paper_story_patterns.tsv | pattern_id, name, section_sequence, paper_count |
| anti_ai_patterns.tsv | pattern_id, banned_phrase, why, smell_severity |
| domain_register.tsv | domain, paper_count |

IEEE 章节枚举（相对 Nature）需要改：Abstract / Introduction / Related Work / Method / Experiments / Conclusion。Methods 在正文中段，不在文末。

## 本仓库 catalog skill（`academic-writing-skills/<skill>/`）

```
SKILL.md          路由与最小工作流
references/       判断规则
scripts/          确定性检查
examples/         请求到命令
evals/            trigger / output
templates/        会场快照
agents/           可选
```

`latex-paper-en/templates/ieee.md` 只覆盖栏式、摘要字数、引用、图表、伪代码。`references/writing/` 是通用英文学术写法，不是 IEEE 语料蒸馏。

qiaomu-meta-skill：判断进 `references/`，可执行知识进独立文件，根 `SKILL.md` 只做路由。一次性总结不要做成 catalog skill。

## 已锁定：选项 A 知识包（2026-09-11）

用户确认 `materials/IEEE/` 做成知识包：逐篇 `observations/`、可计数 `knowledge/*.tsv`、由 core 行综合的 `references/`、根 `SKILL.md` 只做路由。

不做 `prompts/` 改写器，不安装进 `academic-writing-skills/`，不复制 Nature 先验 TSV 行。`just skills-install` 只扫描 catalog 根目录，`materials/IEEE/SKILL.md` 不会被安装。

```
materials/IEEE/
  README.md
  SKILL.md
  corpus/inventory.json
  corpus/FILTER.md
  observations/_schema.md
  observations/<item-key>.md
  knowledge/*.tsv
  knowledge/PROVENANCE.md
  references/style-guide.md
  references/writing/*.md
  scripts/validate_knowledge.py
  scripts/next_pending.py
```
