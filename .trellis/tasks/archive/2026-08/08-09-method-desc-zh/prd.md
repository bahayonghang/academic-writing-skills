# latex-thesis-zh 方法描述规范参考与方法叙述检查器

## Goal

新建模块级方法描述参考 `method-description-guide-zh.md`，在 `analyze_logic.py` 增加
`--method-narrative`（显式 `--section` 选章）的 M-HEADING / M-SEQWORD / M-EQUATION 候选检查与
M-EDGETABLE 接口表骨架输出，配套测试与文档同步。判据唯一权威 = 父 design §2（不复述）。

## Requirements

### R1 新参考文件 `references/writing/method-description-guide-zh.md`

覆盖用户 spec 的可泛化内容（原文见父 research/user-spec-method-description.md，转写须核对
§9/§10 无损），与既有文件零重复（互链代替复述）：

1. 目标五问与三级规则（必须/应当/可以 → Major/Minor 推荐/Info）。
2. 单模块叙述契约六角色表 + 自然段骨架（spec §3）。
3. 相邻模块接口表 + 六类连接类型判据表 + M-NONDIRECT（spec §4）。
4. 公式闭环（spec §5；"式中"只是其中一环）。
5. 收益表述四类主张分级，映射 `over-claim-guard.md` 词表（spec §6，不建新词表）。
6. 标题使用边界：报幕反模式定义 + 三处合法行内小标题豁免（父 design §3）。
7. spec §9 三个正反例（结构保留，案例素材泛化脱敏，无本地论文名）。
8. spec §10 七步审阅改写流程。
9. 脚本检查映射表（M-* 四项：车道/触发/严重度/节号），格式对齐 `method-chapter-guide-zh.md` §十。
10. 与 `method-chapter-guide-zh.md`（章级）、`logic-coherence.md`（段落 AXES）、
    `thesis-writing-guide.md` 互链并写明分工；引用来源见父 research/external-sources.md
    （网络一手四条 + Gopen & Swan）。

### R2 检查器 `analyze_logic.py`

1. 新开关 `--method-narrative`（store_true）：启用 M-HEADING / M-SEQWORD / M-EQUATION +
   M-EDGETABLE。无开关时行为与现状逐字节一致。
2. **作用域 = 显式选章**（父 design §2.5）：必须配 `--section <中文章名/英文键>`（复用现有
   `--section` 语义，先例 `--process-chapter`）；缺 `--section` 时打印候选章清单
   （标题含 方法|原理|设计 ∪ 含实验节 − NON_METHOD 负筛，仅提示）后非零退出。
   单章文件照旧配 `--first-chapter`。不做任何章类型自动判定。
3. 三项检查判据严格按父 design §2.1-2.3 的 zh 侧常量实现；finding 结构沿用现有格式
   （Severity/Priority/`[Script]`，Meaning-Check 恒 NEEDS-LLM）。
4. M-EDGETABLE 骨架按父 design §2.4 输出（诊断输出尾部，非 finding）。
5. argparse help 文案含开关与选章要求（ROUTER_ROW_RE 子进程校验依赖）。

### R3 测试

按 `test_body_chapters.py` 规范写法（importlib 加载、字符串常量合成 fixture、断言形态）：

1. 病例 fixture：连续 ≥3 个 `\paragraph{X。}` 其中 ≥2 报幕句 + 编号公式无"式中" +
   小节首句纯顺序衔接 → 三码全触发。
2. 合规 fixture：约束驱动连续叙述（spec §9 推荐例结构）→ 零发现。
3. 门控断言：无 `--method-narrative` 不触发；有开关无 `--section` 非零退出且输出候选清单；
   `--section` 指向非选中章的内容不扫描。
4. 红线负例：`\paragraph{核心结论概括}`（实验节内容）不触发。
5. 现有全部测试不回归。

### R4 工作流与文档同步

1. SKILL.md：Reference Map 加行；logic 模块路由行命令展示
   `--method-narrative --section <章名>`；只改 `last_updated`。
2. `references/modules/logic.md` 增 M-* 说明段（对齐 L-*/P-* 现有写法）。
3. 双语契约四步链（方向按 spec：**中文源 → docs/zh 页与源一致（仅链接目标可重写）、
   docs/ 英文页做完整英文翻译**）：`check_resource_sync.py --write-manifest` → 建
   docs/zh 一致页 + docs/ 英文译文页 → 两个 index.md 加行 →
   `check_resource_sync.py --skill latex-thesis-zh` 自查。

## Acceptance Criteria

- [x] 新参考文件存在，spec §9/§10 转写与父 research 原文核对无损；Reference Map 与 docs 两个
      index.md 均有入链；正文无本地论文名与未脱敏案例。
- [x] R3 五组断言全绿（病例三码全触发 / 合规零发现 / 门控三态 / 红线负例 / 无回归）。
- [x] M-EDGETABLE 骨架输出包含小节清单与逐边空表。
- [x] `just ci` 全绿；`check_resource_sync.py --skill latex-thesis-zh` 通过（英文页为完整译文，
      非中文复制）。
- [x] SKILL.md version 未变更；无 `\cite`/`\ref`/数学环境处理逻辑改动。

## 排除项

- 不改 `analyze_experiment.py`、`check_format.py`、S1/_check_heading_leads；不做章类型自动判定。
- 不扩 over-claim-guard 词表（可选项，另议）。
- 不做 typst/EN 侧改动（C2 范围）；跨技能契约测试由 C2 交付。
