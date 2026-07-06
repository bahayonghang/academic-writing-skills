# 测试与工具链约定

> 来源：07-05-zh-abstract-tense-gating / 07-05-typst-deai-sync 两任务的实现与质检（2026-07-06）。

---

## Convention: zh/typst 副本脚本的测试必须 importlib 按路径加载

**What**：测试 `latex-thesis-zh/scripts/deai_check.py` 或 `typst-paper/scripts/deai_check.py`（以及任何非 EN/AUDIT 的按技能副本脚本）时，必须用 `importlib.util.spec_from_file_location` 按文件路径加载，并在 try/finally 中全量恢复 `sys.path` 与 `sys.modules`。

**Why**：`tests/conftest.py` 把 EN 与 AUDIT 的 scripts 目录放在 `sys.path` 前排，bare `import deai_check` **静默解析到 EN 副本**——测试全绿但根本没测到目标副本（XC-3b；zh/typst 的时态与结构壳逻辑曾因此长期零覆盖）。不对称恢复则会污染后续裸 import 的 EN/AUDIT 测试。

**Example**（canonical 模式，见 `tests/test_deai_tense_zh.py::_load_zh`，与 cover-letter 测试同源）：

```python
def _load_zh():
    saved_path = list(sys.path)                      # 全量快照
    saved = {m: sys.modules.pop(m, None) for m in ("parsers", "tex_loader")}
    try:
        spec = importlib.util.spec_from_file_location(
            "zh_deai_check", ZH_SCRIPTS / "deai_check.py"   # 命名空间名，勿用 "deai_check"
        )
        module = importlib.util.module_from_spec(spec)
        sys.path.insert(0, str(ZH_SCRIPTS))
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = saved_path                     # 全量恢复
        for name, mod in saved.items():              # 对称还原：缺失则 pop、存在则还原
            if mod is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = mod
```

**Wrong vs Correct**：

```python
# Wrong：解析到 EN 副本，zh 逻辑零覆盖还全绿
import deai_check
checker = deai_check.ChineseAITraceChecker(...)   # AttributeError 或更糟——静默测错对象

# Correct：按路径加载 + 守卫断言确认加载到目标副本
module = _load_zh()
assert hasattr(module, "ChineseAITraceChecker")   # 守卫：不是 EN 的 AITraceChecker
```

**Tests Required**：新测试文件应含一条"加载守卫"用例（断言副本特有类/常量存在），防止加载器改坏后静默退化成 EN 副本。

---

## Convention: zh 时态阈值是双层配置，改 pattern 必须两处同改

**What**：`latex-thesis-zh` 的时态信号 pattern 同时存在于 `scripts/deai_check.py` 的 `DEFAULT_THRESHOLDS`（:116 附近）与 `references/deai/tone-thresholds.yaml`（覆盖层）。改任何 pattern（如 `\bpresents\b`）必须两处同步。

**Why**：YAML 是 DEFAULT 之上的覆盖层，**PyYAML 缺失时走 DEFAULT**——只改 YAML 会在无 PyYAML 环境静默回退到旧行为；只改 DEFAULT 会被 YAML 覆盖掉。SH-1 修复时曾差点漏掉 DEFAULT 层。

**Validation**：改完 grep 全仓确认无旧 pattern 残留：`grep -rn "presents?" academic-writing-skills/*/scripts academic-writing-skills/*/references`（应零命中）。

---

## Gotcha: evals.json 禁用 Edit/Write，走 Bash python 写入

> **Warning**：PostToolUse 的 JSON 格式化 hook 会在 Edit/Write 后把 `academic-writing-skills/*/evals/evals.json` 的多行 `files: [...]` 数组压成单行，造成与改动无关的大面积重排。

**Fix**：改 evals.json 一律用 Bash 跑 python 写入（不触发 Edit/Write hook）。仓库 canonical 格式已 round-trip 验证：

```python
json.dumps(data, indent=2, ensure_ascii=False) + "\n"
```

若已被 hook 重排：`git checkout` 还原后用上式重写，diff 应只剩语义新增（参考 typst-deai-sync 收敛到 +35/-0 的做法）。

**同类陷阱**：SKILL.md 的表格被全局 hook 重新对齐会触发 `ROUTER_ROW_RE` contract 测试——改 SKILL.md 表格后必须跑 `tests/test_skill_contracts.py`。
