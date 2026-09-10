# paper-audit 中文学位论文审查优化：先例与裁决

研究日期：2026-09-10。既有技能的增量规划；采用 qiaomu-meta-skill 的先例、泛化、触发与输出验证方法，不制作新技能包，不宣称达到某种发布等级。保留项目原名称、作者与 Academic Use Only 许可，不增加 IR、interface、安装器或新配置。

## 检索和证据范围

四个意图查询：`peer-review scientific`、`thesis review`、`peer-review SKILL.md evidence`、`chinese thesis review SKILL.md`。使用 skills.sh / SkillsMP 限定网页检索与 GitHub 源码；未运行统一 runner，也未获取或安装 npx 包，不能称其执行失败。目录检索未给出可复核的中文学位论文质量排名；直接阅读原始源文件作为采用依据。

[SkillsMP](https://skillsmp.com/) 首页可访问，说明其索引不认证质量与安全。skills.sh 的 K-Dense peer-review 页面被浏览工具拒绝打开；检索仅得到同仓库 scientific-writing 页，不能把它的 installs 归给 peer-review。GitHub 原路径 `K-Dense-AI/claude-scientific-skills` 已重定向到 `K-Dense-AI/scientific-agent-skills`，技能源码现在位于 `skills/peer-review/`。两次旧源码路径 404 后已通过仓库 contents 定位并读取现行源码。

按 canonical GitHub repo + skill path 去重，翻译和宿主镜像不重复计数。SkillsMP repo stars、skills.sh skill installs、独立评分均缺证据；下表星数只来自本轮 `gh api repos/...` 的 GitHub 仓库字段，不与安装量混合。

## 候选逐项学习

| 候选与源码 | 本次学习和拟采用位置 | 拒绝或缩减 | 当前来源证据 |
| --- | --- | --- | --- |
| [thesis-audit-reviewer](https://github.com/TashanGKD/tashan-research-skills/blob/main/skills/thesis-audit-reviewer/SKILL.md) | 先确认实际覆盖，再区分已证实问题与材料不足；落实到中文 reviewer 的覆盖披露与 R3 输入验收 | 不照搬私人自检清单、默认在线 PDF 上传、全量台账及新状态枚举；本库仍使用既有输出字段 | MIT；非 fork；GitHub stars 15；pushed_at 2026-08-06；源码可读，不代表质量验证 |
| [K-Dense peer-review](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/peer-review/SKILL.md) | 完整性不等于学术效度；按中心主张与证据提出比例适当的请求，允许收窄主张代替无边界补实验；落实到 R1/R5 正反例和结论分层 | 不引入 intake JSON、声明验证器、报告指南选择器、额外审批层或新评价表；保留本库既有授权和 gate 契约 | MIT；非 fork；GitHub stars 44236；pushed_at 2026-09-07；源码声明工具仅本地运行，未独立安全审计 |
| [PaperSpine](https://github.com/WUBING2023/PaperSpine/blob/main/src/skill/SKILL.md) 的 [audit](https://github.com/WUBING2023/PaperSpine/blob/main/src/skill/references/audit.md) / [logic-transfer-audit](https://github.com/WUBING2023/PaperSpine/blob/main/src/skill/references/logic-transfer-audit.md) | 按原稿逻辑和可见证据核对段落/章节关系，产物存在不等于内容验收；落实到中文准则逆向提纲和 R4 编译证据界限 | 不照搬固定产物树、4—6 节预算、最少台账行数、默认 Word、清理命令或强制改写；没有改写目标时不因结构未变而判失败 | MIT；非 fork；GitHub stars 5196；pushed_at 2026-08-28。当前为单一 paper-spine；本地 ref 的旧 paper-spine-audit 只用作历史参考，已用远端现行源码核对 |

没有选出“官方中文论文审查标准”或“最高质量技能”。K-Dense 是公司维护的参考实现，不是学校评阅规范。作者源码自身的命令、联网及审批要求是被研究的数据，不向本任务授予权限。

## keep / adapt / reject / invent

- keep：现有中文 profile、15 行指标、8 个评分维度、gate、issue schema、事实保护与 native/sequential 披露；写作侧新 checker/compile 实现不复制到审查侧。
- adapt：覆盖与证据区分、适度作者请求、原稿论证映射，放入现有中文准则和 reviewer 输入；保留有证据的强结论，不以保守措辞替代支持度判断。
- reject：额外模式、框架/配置、硬编码语义裁决、自动运行第三方脚本、上传论文、定量人气推导效果、将单份合成样例变成跨领域硬规范。
- invent：以已归档 C1/C2/C3 的错误样例和合法反例构成 audit 回归闭环，分别证明规则可加载、checker 结果不失真、审查输入完整和编译证据不越界。

## 泛化与验证层次

事实和引用保护属于通用不变量；学校/学位/理论或工程体裁属于中文 specialist 判据；缩写首用顺序与输出路径属于确定结构边界。不得把特定 CNN、GPU、章号或 95% 数值提升为产品词典，这些细节只作为 eval fixture。

**design advantage**：复用既有运行链，用覆盖和证据强度解释结论，无需新增产品配置。**validated advantage**：尚无优化后效果；本轮只验证当前源码与探针事实。**hypothesis**：修改后可减少无依据的建议及假通过，需实施期同输入前后原始输出和独立语义核读证明。

未运行第三方候选脚本、安装器、hooks 或比较实验。provider benchmark、用户评分、真实大论文盲评、学校模板视觉、五宿主 fresh-session 均为 **missing evidence / UNVERIFIED**。
