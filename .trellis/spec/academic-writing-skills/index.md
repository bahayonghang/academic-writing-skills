# Academic Writing Skills — 本仓库编码规范

> 本目录收录 academic-writing-skills 仓库自身的可执行约定（区别于 PaperSpine/ 等参考项目的 spec）。

## 文档索引

| 文档                                                                     | 内容                                                                                    | 何时读                                                                                  |
| ------------------------------------------------------------------------ | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| [testing-and-tooling.md](./testing-and-tooling.md)                       | 按技能副本脚本的测试加载约定、BibTeX 扫描器维护、阈值与 evals 工具约定                  | 给 zh/typst 副本写测试、改 BibTeX 扫描或 evals/阈值配置之前                             |
| [spec-checklist-convention.md](./spec-checklist-convention.md)           | 逐项检查清单五列格式、CHECKERS 双向锁、TEMPLATE_THRESHOLDS 阈值来源规则                 | 改 templates/*.md 清单、check_spec.py 检查器、SKILL.md 路由表之前                       |
| [docs-bilingual-resources.md](./docs-bilingual-resources.md)             | 技能公开资源到双语 VitePress 页面、manifest、侧栏和检查器的可执行契约                   | 增删 references/templates/examples/agents 或修改 docs 资源之前                          |
| [paper-audit-boundary-contracts.md](./paper-audit-boundary-contracts.md) | paper-audit severity、ScholarEval 模块映射与外置 BibTeX 数据流契约                      | 修改 consolidation、ScholarEval 或 literature comparison 链路之前                       |
| [method-narrative-contract.md](./method-narrative-contract.md)           | 三写作技能 M-* 判定、paper-audit 双调用、块解析、Info/P3 与报告层契约                 | 修改方法叙述检查、M-* 对齐面或 paper-audit methods 接线之前                              |
| [cover-letter-contracts.md](./cover-letter-contracts.md)                 | cover-letter claim 位置、journal-fit 去重与警告 payload 契约                            | 修改 cover-letter claim/journal-fit/统一 CLI 数据流之前                                 |
| [polish-rewrite-contract.md](./polish-rewrite-contract.md)               | 两层改写契约四字段、`--goal`/`--strength`/`--tier` 三轴、A/B/C 自动化分级、受保护 token | 改 EN/ZH/Typst 任一润色模块（expression/grammar/sentences/translation）或其契约字段之前 |
| [defensive-ai-rhetoric-contract.md](./defensive-ai-rhetoric-contract.md) | 防御性推测解释的组合判据、证据校准修复、跨 surface eval 与 audit lane 预算              | 改 de-AI/experiment 的机制解释规则或 claims-vs-evidence lane 之前                        |
| [results-analysis-checker-contract.md](./results-analysis-checker-contract.md) | 中文学位论文 RA-* 区间、证据窗口、误报避让与公开路由同步契约                       | 改 `--results-analysis`、RA-* 词表/判据、结果分析 fixture 或路由资源之前                 |

## 背景速览

- 各 skill 的 `scripts/parsers.py`、`scripts/deai_check.py` 是**按技能副本**（非共享 import）；共享面由对齐测试锁定（parsers：`tests/test_parsers_alignment.py`；deai：`tests/test_deai_alignment.py`，含 strict/logic 双层哈希锁与关系锁）。改共享逻辑先改 latex-paper-en，typst 逐字节镜像，zh 保留中文 docstring（logic 锁容忍、strict 锁不含 zh）。
- 还有第三套锁：`tests/contracts/test_writing_modules_alignment.py` 的 `TIER1_HASH_GROUPS` 要求 `analyze_abstract.py`/`analyze_grammar.py`/`analyze_sentences.py`/`improve_expression.py` 的 en/typst 副本**整文件字节一致**（sha256 整文件互比，不是成员级 diff）。改这四个脚本任一处都必须两副本同步落地——按成员级镜像会漏掉无关空白/顺序差异，该锁仍会红。
- `tests/conftest.py` 只把 EN 与 AUDIT 的 scripts 目录放进 `sys.path` 前排——**bare import 拿到的永远是 EN 副本**。
