"""Lock the security core while retaining each skill's encoding and display rules."""

import ast

import pytest

from tests.support.paths import SKILLS_ROOT

SKILLS = ("latex-thesis-zh", "latex-defense-zh", "latex-paper-en", "paper-audit", "cover-letter")
CORE = (
    "IncludeBoundaryError",
    "_checked_path",
    "_entry_and_root",
    "_resolve_include_target",
    "iter_files",
)


def members(skill):
    path = SKILLS_ROOT / skill / "scripts/tex_loader.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return {
        node.name: node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))
    }


@pytest.mark.parametrize("skill", SKILLS)
def test_boundary_core_and_keyword_interfaces_match(skill):
    canonical = members("latex-paper-en")
    actual = members(skill)
    for name in CORE:
        assert ast.dump(actual[name]) == ast.dump(canonical[name]), (skill, name)
    for name in ("iter_files", "assemble"):
        function = actual[name]
        assert isinstance(function, ast.FunctionDef)
        assert [arg.arg for arg in function.args.args] == ["entry"]
        assert [arg.arg for arg in function.args.kwonlyargs] == ["project_root"]
        default = function.args.kw_defaults[0]
        assert isinstance(default, ast.Constant)
        assert default.value is None
