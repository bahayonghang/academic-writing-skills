# Academic Writing Skills - Just Commands

# Use PowerShell on Windows so recipes do not require a POSIX `sh`.
set windows-shell := ["powershell.exe", "-NoLogo", "-NoProfile", "-Command"]

# 默认显示所有可用命令
default:
    @just --choose

# 显示帮助信息
help:
    @echo "════════════════════════════════════════════════════════════════"
    @echo "  Academic Writing Skills - 任务管理工具"
    @echo "════════════════════════════════════════════════════════════════"
    @echo ""
    @echo "🔧 开发环境："
    @echo "  just install           - 安装开发依赖"
    @echo ""
    @echo "🔍 代码质量检查："
    @echo "  just lint              - 运行格式和代码检查"
    @echo "  just typecheck         - 运行类型检查"
    @echo "  just test              - 运行测试"
    @echo "  just check-versions    - 校验所有 skills 与 pyproject 版本一致"
    @echo "  just ci                - 运行完整 CI 流程"
    @echo ""
    @echo "🔧 代码修复："
    @echo "  just fix               - 自动修复格式和代码问题"
    @echo "  just format            - 仅格式化代码"
    @echo ""
    @echo "📚 文档："
    @echo "  just docs              - 本地预览文档"
    @echo "  just doc-build         - 构建文档"
    @echo ""
    @echo "📦 打包："
    @echo "  just zip               - 打包每个 skill 为 zip 到 archive/"
    @echo "  just clean-zip         - 清理 archive/ 下的 zip 文件"
    @echo ""
    @echo "🧹 清理："
    @echo "  just clean             - 清理缓存文件"
    @echo ""
    @echo "════════════════════════════════════════════════════════════════"

# 安装开发依赖
install:
    @echo "📦 Installing development dependencies..."
    uv sync --extra dev
    @echo "✅ Installation complete!"

# 运行所有 CI 检查
ci:
    @echo "════════════════════════════════════════════════════════════════"
    @echo "  🚀 开始执行 CI 流程"
    @echo "════════════════════════════════════════════════════════════════"
    @echo ""
    @echo "🔢 步骤 1/4: 校验 skills 版本与 pyproject 一致..."
    @just check-versions
    @echo ""
    @echo "🔍 步骤 2/4: Ruff 代码检查..."
    @just lint
    @echo ""
    @echo "🔍 步骤 3/4: Pyright 类型检查..."
    @just typecheck
    @echo ""
    @echo "🧪 步骤 4/4: 运行测试..."
    @just test
    @echo ""
    @echo "════════════════════════════════════════════════════════════════"
    @echo "  ✅ CI 流程执行完成！"
    @echo "════════════════════════════════════════════════════════════════"

# 校验所有 SKILL.md 版本与 pyproject.toml 一致
check-versions:
    @echo "  → 校验 skills 版本与 pyproject.toml 对齐..."
    @uv run --extra dev python -m pytest tests/contracts/test_skill_versions.py -q
    @echo "  ✓ 版本一致性检查通过"

# 代码格式化和 lint 检查
lint:
    @echo "  → 检查代码格式..."
    @uv run --extra dev ruff format --check .
    @echo "  → 检查代码规范..."
    @uv run --extra dev ruff check .
    @echo "  ✓ Lint 检查通过"

# 自动修复 lint 问题
fix:
    @echo "🔧 自动修复代码问题..."
    @echo "  → 格式化代码..."
    @uv run --extra dev ruff format .
    @echo "  → 修复可修复的问题..."
    @uv run --extra dev ruff check --fix .
    @echo "✅ 修复完成！"

# 仅格式化代码
format:
    @echo "🎨 格式化代码..."
    @uv run --extra dev ruff format .
    @echo "✅ 格式化完成！"

# 类型检查
typecheck:
    @echo "  → 运行 Pyright 类型检查..."
    @uv run --extra dev pyright
    @echo "  ✓ 类型检查通过"

# 运行测试
test:
    @echo "  → 运行单元测试..."
    @uv run --extra dev python -c "import pathlib, subprocess, sys; paths = ['tests', *(str(p) for p in pathlib.Path('academic-writing-skills').glob('*/tests') if p.is_dir())]; raise SystemExit(subprocess.call([sys.executable, '-m', 'pytest', *paths]))"
    @echo "  ✓ 测试通过"

# 清理缓存文件
clean:
    @echo "🧹 清理缓存文件..."
    @uv run --extra dev python -c "import pathlib, shutil; roots = pathlib.Path('.'); [shutil.rmtree(p, ignore_errors=True) for name in ('__pycache__', '.pytest_cache', '.ruff_cache') for p in roots.rglob(name) if p.is_dir()]; [p.unlink(missing_ok=True) for p in roots.rglob('*.pyc')]"
    @echo "✅ 清理完成！"

# 打包每个 skill 子目录为 zip 到 archive/
zip:
    @echo "📦 打包 skills 到 archive/..."
    @uv run --extra dev python -c "import pathlib, shutil; src = pathlib.Path('academic-writing-skills'); dst = pathlib.Path('archive'); dst.mkdir(exist_ok=True); [shutil.make_archive(str(dst / p.name), 'zip', root_dir=src, base_dir=p.name) for p in sorted(src.iterdir()) if p.is_dir() and (p / 'SKILL.md').exists()]; [print(f'  → {f.name}') for f in sorted(dst.glob('*.zip'))]"
    @echo "✅ 打包完成！"

# 清理 archive/ 下的 zip 文件
clean-zip:
    @echo "🧹 清理 archive/ 下的 zip 文件..."
    @uv run --extra dev python -c "import pathlib; dst = pathlib.Path('archive'); zips = list(dst.glob('*.zip')) if dst.exists() else []; [p.unlink(missing_ok=True) for p in zips]; print(f'  → 已删除 {len(zips)} 个 zip 文件')"
    @echo "✅ 清理完成！"

# 本地预览文档
docs:
    @echo "📚 启动文档开发服务器..."
    @cd docs; npm run docs:dev

# 构建文档
doc-build:
    @echo "🏗️ 构建文档..."
    @cd docs; npm run docs:build

