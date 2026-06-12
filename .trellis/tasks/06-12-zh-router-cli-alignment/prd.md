# 对齐 SKILL.md 路由契约与脚本 CLI

> 父任务：`06-12-latex-thesis-zh-optimization`（见其 prd.md §2 发现 F9/F10/F13）
> 优先级：P1 · 依赖：建议在 `06-12-zh-parsers-multifile` 之后执行（CLI 行为以新地基为准）。

## Goal

消除 SKILL.md 承诺与脚本实际行为之间的错位：按文档原样执行路由命令，
就应得到路由表"Use when"列所描述的检查结果——不多收窄、不静默降级。

## Requirements

### R1 logic 模块命令与行为对齐（F9）

- 二选一（在 design 阶段定夺，倾向 a）：
  - (a) 改脚本：`--section` 模式下仍执行与该 section 相关的章节级检查
    （如 `--section related` 仍跑 A1/A3；`--section introduction` 仍跑漏斗检查），
    并把 `--cross-section` 的 C3 闭合检查并入默认全文档模式（保持向后兼容开关）；
  - (b) 改文档：路由表主命令去掉 `--section related`，在"路由规则"中明确
    哪些检查只在全文档模式下运行、`--cross-section` 何时该加。
- 无论选哪种：SKILL.md 中宣传的每一类检查（导语/主线/章引言/漏斗/三方对齐/C3 闭合/
  动机红线）都必须有一条文档化命令能够触达。

### R2 把 check_references.py 暴露进路由（F10）

- 新增 `references` 模块行（或并入 `format`/`tables` 的"Read next"与命令清单）：
  交叉引用完整性（undefined \ref、unreferenced label、缺 caption、编号断档）
  是中文学位论文盲审高频扣分点，质量最好的多文件脚本不应从 SKILL.md 不可达。
- 相应补 `references/modules/` 参考片段（可精简，复用脚本 docstring）。

### R3 `$SKILL_DIR` 约定显式化（F13）

- 在 SKILL.md "Workflow"或路由表上方加一句明确约定：`$SKILL_DIR` 指本 skill
  安装目录（会话上下文中的 base directory），执行时需替换为实际路径；
  或改用相对路径写法并说明工作目录假设。与套件内其他 skill 的写法保持一致
  （检查 latex-paper-en 等是否同样需要，如是则只在本 skill 范围内修，
  兄弟 skill 另行开任务）。

### R4 路由表与脚本旗标全量核对

- 对 13 个模块逐一核对"Primary command"与脚本 argparse：旗标存在性、默认值、
  退出码语义（SKILL.md Output Contract 要求报告退出码）。
- `deai` 行补充 `--analyze`（全文档模式）与 `--section` 的关系说明；
  `optimize_title.py --interactive` 从可用旗标中移除或标注"仅人工终端使用"。

## Constraints

- SKILL.md 正文保持 <500 行（当前 167 行，有富余）。
- 不改变模块数量级与触发语义（description/when_to_use 的触发优化不在本任务，
  避免与 trigger eval 基线漂移混在一起）。
- 不 bump version，只改 last_updated。

## Acceptance Criteria

- [ ] 逐条执行 SKILL.md 全部模块主命令（fixture 工程上）：每条命令的输出覆盖
      路由表"Use when"描述的检查类别，无静默缺项。
- [ ] SKILL.md 中宣传的每类 logic 检查均可通过文档化命令触达（含 C3 闭合）。
- [ ] `references`（交叉引用）能力从 SKILL.md 可达，并有对应 modules 参考片段。
- [ ] `$SKILL_DIR` 约定已说明；新读者按文档操作不会展开出空路径。
- [ ] `tests/test_skill_contracts.py` 的 ROUTER_ROW_RE 契约测试通过
      （注意 memory：全局格式化 hook 对齐表格可能破坏该测试，提交前自查）。
