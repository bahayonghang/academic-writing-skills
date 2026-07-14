# Example: Compilation and Template Detection

User request:
This Chinese master's thesis project keeps failing to compile. Also confirm whether it actually uses the `thuthesis` template.

Recommended module order:
1. `template`
2. `compile`

Commands:
```bash
uv run python $SKILL_DIR/scripts/detect_template.py main.tex
uv run python $SKILL_DIR/scripts/compile.py main.tex
```

Expected output:
- Template detection result.
- When compilation fails, the exact command, exit code, and next troubleshooting step.
