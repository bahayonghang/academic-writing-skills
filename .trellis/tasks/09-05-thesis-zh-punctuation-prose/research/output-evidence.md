# 标点与句间逻辑实际输出审阅

日期：2026-09-06。实际输入和完整回答见 [output-responses.md](output-responses.md)。
采样 Agent 为 gpt-5.6-sol/max，仅投影 eval 43–45 输入；主 Agent 逐条阅读后裁决。
本次输出包含既有 Changed / Protected / Meaning-Check / Risk-Flags 四字段，没有执行脚本，
其中 PRESERVED 是待作者核对的 LLM 提案，不是形式化语义证明。

| ID | 逐项实际观察 | 裁决 |
| --- | --- | --- |
| 43 | 删除三处标签壳和分号清单，改成结果、组件移除对照、适用范围三个完整句；ref tab:ablation、0.28/0.21/0.27 与离线范围均保留；使用相关性而非绝对因果措辞 | PASS |
| 44 | A/B、120/118、MAE、0.18/0.21 全部保留；不补配对、重复实验或因果设计；依输入许可删除无证据“更稳定”结论并说明不可推出 | PASS |
| 45 | 合理引出、复杂条件并列、关键词格式、h=[h_A;h_B]、mode: safe; retry: 2、URL、cite std 和定义冒号原样保留；只局部改写最后一句标签壳，保留离线完成和无现场验证两个事实 | PASS |

主 Agent 对照的是实际响应正文与全部受保护 token，而非只看 expected_output 或标点计数。
没有发现将必要冒号/分号全部删除、用逗号简单替换整段、补造句间因果或以符号判断 AI 作者。
ID 45 的诊断说明和四字段仍可以使用结构化标点；用户要求针对的是论文连续正文，不是禁止
审阅报告或受保护源码使用这些符号。

## 实现与检查交接

唯一规则源为 academic-style-zh.md §5.4，expression、deai、routing 与 SKILL 均可按需到达；
README/README_CN、两语技能入口、四份修改资源的镜像及 manifest 已同步。
规则明确出现实验/消融/来源文本本身不证明因果，论断强度继续由 over-claim-guard 负责。

实施 Agent 依 implement.md 运行：目标 pytest 106 passed；双语资源契约 10 passed；
manifest inventory 271 entries 与单技能完整同步通过；just doc-build 通过（VitePress 1.6.4）；
diff --check 通过。本子任务新增 output 43–45 和第 48 条 trigger；未改变任何脚本/阈值/规则码。

结论只覆盖本地 Agent 的三个合成场景；跨模型效果、人工盲评、真实论文整体语气仍为 UNVERIFIED。

## 构建后导航返修与实证

主 Agent 查看构建 HTML 后发现，新 §5.4 的中文标题 slug 不能同时命中 EN/ZH 的自动 id；
原先资源形状检查与 doc-build 成功没有发现此 fragment 错误。原 implement Agent 只修本次
新增导航，在 source/EN/ZH 的节标题前加入同一 `punctuation-prose` 显式锚点，三侧目录与
expression/deai 指针共 9 处链接同步，未扩展修复旧目录。
最后由题注 implement Agent 统一更新 manifest 和构建。主 Agent 读取实际生成的两语 HTML：
每语均有 1 个目标 id、1 个目录 href、1 个 expression 指针、1 个 deai 指针，全部指向
`#punctuation-prose`，实际到达性通过。验证路径为
`docs/.vitepress/dist/{skills,zh/skills}/latex-thesis-zh/resources/references/` 下对应三页。
