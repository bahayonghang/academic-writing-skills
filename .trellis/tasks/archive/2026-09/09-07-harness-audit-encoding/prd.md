# 修复 paper-audit Windows 子进程编码边界

优先级：P1。父需求：R2/R3/R4/R5/R7。状态：planning。

## 目标与背景

research/runtime-findings.md F1 已复现：同一 fixture 默认环境 exit0；仅 PYTHONIOENCODING=utf-8 时 UnicodeDecodeError/None.strip exit1；加 PYTHONUTF8=1 则恢复。audit.py:686-692 没有明确 subprocess encoding。

## 范围

- academic-writing-skills/paper-audit/scripts/audit.py（_run_check_script 与必要 import）
- tests/skills/paper_audit/test_paper_audit_integration.py

## 前置与授权

用户批准；可与 C1/C2 独立。

当前仅规划，禁止 task.py start/实现/正式规则回写。任务树归属不代替前置条件。不同工作者不得覆盖其他子任务或用户改动。

## 验收条件

以下需求编号继承父任务的同名要求，本子任务负责其中与自身范围有关的交付。

- R2：检查覆盖完整并记录真实通过/失败/未验证证据。
- R3：改造有已复现失败或工作流缺口证据，不混同历史与当前。
- R4：强模型负责判断与复核，便宜模型执行有明确边界。
- R5：文件范围、前置与检查可实施、可逐项验收。
- R7：批准后将证实经验按适用工具回写，保留规划/实施边界。

- [x] AC1（R3/R5）：Python checker 输出与父 pipe 读取采用同一 UTF-8 协议，不依赖调用 harness 的 locale。
- [x] AC2（R2/R3）：默认、stream-only UTF8、UTF8 mode 三种完整 checkout 的复现均不出现 UnicodeDecodeError、AttributeError 或丢失 checker 输出。
- [x] AC3（R2/R5）：真实 subprocess Unicode 回归验证中文和非 ASCII 标点字节保真，并保留超时、失败退出、stderr 的现有语义。
- [x] AC4（R4/R7）：不改全局配置、不用空字符串或 errors=ignore 吞掉协议错误、不扩张成全仓编码重构。

## 非目标

不新增依赖，不发布，不改全局工具配置，不扩大到整体框架重构。未运行的能力不得写成已验证。
