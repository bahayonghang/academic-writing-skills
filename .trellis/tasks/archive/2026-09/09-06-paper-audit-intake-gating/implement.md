# 实施计划

## 顺序

1. 读 `MODE_GUIDE.md:1-60`，确认改前字面与行号未漂移。
2. 改 `### Auto-Detection at Intake` 前言，插入门控三分支。
3. 改四条检测 bullet，各补已指定模式下的处理句；保留 `revision_coach_agent` dispatch 字面。
4. 改收尾句为陈述式/确认式两分支。
5. 改 `MODE_GUIDE.md:24-26` re-audit 段落为查找—唯一则陈述—否则询问三分支。
6. 补实质冲突判据段，含一个提问正例与一个不提问反例。
7. 同步 en/zh 两份镜像与 `docs/resource-manifest.json` 的 sha256。
8. 跑 AC3 / AC4 的行为验收，保存实际响应到 `research/`。

## 验证命令

```bash
uv run --extra dev python -m pytest tests/skills/paper_audit tests/contracts -q
uv run python docs/scripts/check_resource_sync.py
```

manifest sha256 用与 `docs/scripts/check_resource_sync.py` 相同的算法重算，
不手写散列。

## 审查门

- 步骤 3 完成后先跑 `pytest tests/skills/paper_audit/test_paper_audit_synthesis.py -q`，
  确认 `Auto-Detection at Intake` 与 `revision_coach_agent` 两条断言仍通过，再继续。
- 步骤 8 的行为验收失败时回到步骤 2 改措辞，不改测试。

## 回退点

步骤 2-6 是同一文件的连续编辑，回退单位是该文件的完整 diff。
步骤 7 的镜像与 manifest 必须与源同进同退，不允许只回退其中一侧。
