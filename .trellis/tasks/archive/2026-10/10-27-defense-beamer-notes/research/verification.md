# 验证记录（10-27-defense-beamer-notes）

- `just ci`（PYTHONUTF8=1）：2854 passed，16 skipped；资源同步：306 条通过。
- `DEFENSE_COMPILE=1` 编译用例：9 passed。fixture：`defense.pdf` 54 页（453.5×255.1），`defense-notes.pdf` 54 页（907.1×255.1，W/H 3.556），页标签 1…54。
- 已编译 fixture 上 `check_deck.py`（带 PyMuPDF）：Critical 0 / Major 0 / Minor 0，无 skipped；缺 PyMuPDF 时 D-NOTES-PDF 记入 skipped。
- 未加标签修正的 spike PDF：D-NOTES-PDF 报 27 条 Minor（相邻页标签重复），证明判据有效。
- trellis-check：无阻断缺陷；三处文档小问题已修。
- FerroStage 实机打开 `defense-notes.pdf`：**UNVERIFIED**（未取得只含 FerroStage 窗口的截图）。
