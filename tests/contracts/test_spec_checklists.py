"""Contract lock: templates/*.md 逐项检查清单 ↔ check_spec.py 注册表 双向一致。

锁定内容（对应任务 07-08-spec-final-check design §5）：
1. 所有含「## 逐项检查清单」的模板快照均可被 parse_checklist 解析
   （ID 唯一、检查方式/适用枚举合法由解析器抛错保证），且 ID 前缀全文件统一；
2. 清单引用的 ``script:<checker>`` 必须存在于 check_spec.CHECKERS；
   反向：CHECKERS 的每个 checker 至少被一个清单引用（防死代码）；
3. 清单引用的 ``module:<name>`` 必须是 SKILL.md Module Router 中的模块；
4. yanshan.md 清单条目数下限（防误删）。
"""

from __future__ import annotations

import importlib.util
import re
import sys

from tests.support.paths import SCRIPT_DIR_ZH, SKILLS_ROOT

_SKILL_DIR = SKILLS_ROOT / "latex-thesis-zh"
_TEMPLATES_DIR = _SKILL_DIR / "templates"
CHECKLIST_HEADING = "## 逐项检查清单"
MIN_YANSHAN_ITEMS = 40


def _load_check_spec():
    saved_path = list(sys.path)
    saved = {m: sys.modules.pop(m, None) for m in ("parsers", "tex_loader")}
    try:
        spec = importlib.util.spec_from_file_location(
            "zh_check_spec_contract", SCRIPT_DIR_ZH / "check_spec.py"
        )
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        sys.path.insert(0, str(SCRIPT_DIR_ZH))
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = saved_path
        for name, mod in saved.items():
            if mod is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = mod


check_spec = _load_check_spec()


def _checklist_templates() -> dict[str, list]:
    """{模板名: items}，覆盖所有带清单段的模板快照。"""
    found = {}
    for md in sorted(_TEMPLATES_DIR.glob("*.md")):
        if CHECKLIST_HEADING in md.read_text(encoding="utf-8"):
            found[md.stem] = check_spec.parse_checklist(md)
    return found


def test_checklists_exist_and_parse():
    templates = _checklist_templates()
    assert "yanshan" in templates, "yanshan.md 必须携带逐项检查清单"
    for name, items in templates.items():
        assert items, f"{name}: 清单为空"


def test_checklist_id_prefix_uniform_per_file():
    for name, items in _checklist_templates().items():
        prefixes = {item.id.split("-")[0] for item in items}
        assert len(prefixes) == 1, f"{name}: 清单 ID 前缀不统一: {sorted(prefixes)}"


def test_script_checkers_bidirectionally_locked():
    used: set[str] = set()
    for name, items in _checklist_templates().items():
        for item in items:
            if item.method.startswith("script:"):
                key = item.method.split(":", 1)[1]
                assert key in check_spec.CHECKERS, f"{name}: {item.id} 引用不存在的检查器 {key}"
                used.add(key)
    dead = set(check_spec.CHECKERS) - used
    assert not dead, f"CHECKERS 存在未被任何清单引用的死代码检查器: {sorted(dead)}"


def test_module_refs_exist_in_router():
    skill_md = (_SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    router_modules = set(re.findall(r"^\|\s*`([a-z-]+)`\s*\|", skill_md, re.MULTILINE))
    assert router_modules, "SKILL.md 路由表解析失败"
    for name, items in _checklist_templates().items():
        for item in items:
            if item.method.startswith("module:"):
                mod = item.method.split(":", 1)[1]
                assert mod in router_modules, (
                    f"{name}: {item.id} 引用的模块 {mod} 不在 SKILL.md 路由表中"
                )


def test_yanshan_checklist_floor():
    items = _checklist_templates()["yanshan"]
    assert len(items) >= MIN_YANSHAN_ITEMS, (
        f"yanshan 清单仅 {len(items)} 条（下限 {MIN_YANSHAN_ITEMS}），疑似被误删"
    )
    # 覆盖面抽查：三大章都应有条目（依据 § 前缀）
    bases = " ".join(item.basis for item in items)
    for section in ("§1.", "§2.", "§3."):
        assert section in bases, f"yanshan 清单缺少 {section}x 章的条目"


def test_module_command_hints_match_router_scripts():
    """MODULE_COMMANDS 提示命令里的脚本必须真实存在（防文档漂移）。"""
    for mod, cmd in check_spec.MODULE_COMMANDS.items():
        m = re.search(r"\$SKILL_DIR/(scripts/\w+\.py)", cmd)
        assert m, f"MODULE_COMMANDS[{mod}] 未指向 $SKILL_DIR 脚本: {cmd}"
        assert (_SKILL_DIR / m.group(1)).exists(), f"MODULE_COMMANDS[{mod}] 脚本不存在: {cmd}"
