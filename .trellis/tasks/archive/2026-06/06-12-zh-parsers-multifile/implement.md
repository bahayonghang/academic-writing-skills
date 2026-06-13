# Implement: parsers 多文件解析与章节切分修复

执行顺序（每步后跑相关测试）：

1. [x] 阅读全部消费方脚本与对齐测试，确认锁定边界
2. [x] 新建 `scripts/tex_loader.py`（read_text_robust / iter_files / assemble / AssembledDocument）
3. [x] 重写 `parsers.py` 的 split_sections（两 Parser）+ chapter_ranges + resolve_section_keys
4. [x] 接入 analyze_logic.py（行号注入 + --section resolve + 告警头）
5. [x] 接入 deai_check.py / deai_batch.py
6. [x] 接入 analyze_experiment / analyze_literature / analyze_abstract / optimize_title
7. [x] 接入 check_tables / check_format
8. [x] check_consistency: include 图默认 + --all-files；check_references / map_structure 切换 tex_loader
9. [x] 新增回归测试（tests/test_latex_thesis_zh_multifile.py，23 例）
10. [x] 测试全绿（647 passed）；pyright 0 errors；ruff 通过（注：.trellis 脚本与 test_skill_contracts.py
       存在先于本任务的未格式化问题，另行 chore 处理）

实施备注：
- ZH analyze_abstract.py / check_tables.py 因引入 tex_loader 退出 TIER1_HASH_GROUPS
  字节对齐组（tests/test_writing_modules_alignment.py 已记录原因，2026-06）。
- test_parsers_alignment.py 锁定成员零改动，全部通过。

验证命令：
- `uv run --extra dev python -m pytest tests/test_latex_thesis_zh_scripts.py tests/test_parsers_alignment.py tests/test_latex_thesis_zh_multifile.py -q`
- `just ci`

回滚点：单 commit，revert 即回滚。
