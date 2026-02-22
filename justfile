# Academic Writing Skills - Just Commands

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
    @echo "  just ci                - 运行完整 CI 流程"
    @echo ""
    @echo "🔧 代码修复："
    @echo "  just fix               - 自动修复格式和代码问题"
    @echo "  just format            - 仅格式化代码"
    @echo ""
    @echo "📚 文档："
    @echo "  just doc               - 本地预览文档"
    @echo "  just doc-build         - 构建文档"
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
    @echo "🔍 步骤 1/3: Ruff 代码检查..."
    @just lint
    @echo ""
    @echo "🔍 步骤 2/3: Pyright 类型检查..."
    @just typecheck
    @echo ""
    @echo "🧪 步骤 3/3: 运行测试..."
    @just test
    @echo ""
    @echo "════════════════════════════════════════════════════════════════"
    @echo "  ✅ CI 流程执行完成！"
    @echo "════════════════════════════════════════════════════════════════"

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
    @uv run --extra dev python -m pytest tests/
    @echo "  ✓ 测试通过"

# 清理缓存文件
clean:
    @echo "🧹 清理缓存文件..."
    @find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    @find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
    @find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
    @find . -type f -name "*.pyc" -delete 2>/dev/null || true
    @echo "✅ 清理完成！"

# 本地预览文档
doc:
    @echo "📚 启动文档开发服务器..."
    @cd docs && npm run docs:dev

# 构建文档
doc-build:
    @echo "🏗️ 构建文档..."
    @cd docs && npm run docs:build

