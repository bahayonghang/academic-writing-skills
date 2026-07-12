# 实现期校正便签（基于 2026-07-12 主会话实测，覆盖 fixture 报告的过时结论）

开工前用当前 HEAD（07-11 已全部提交归档，工作树干净，**无需 rebase**）实测复核，修正 `research/fixture-chapters3-6-audit.md` 的两处过时结论：

## C1：P5（S1 编号引言节导语误报）**已被 07-11 修复，不需再做**
- commit `6aef549` 已给 `_check_heading_leads` 加 `_has_numbered_intro_section` 豁免（analyze_logic.py L768-794）。
- 实测 `analyze_logic.py chapter3.tex`（默认模式）**零 S1 导语输出**。
- 影响：**design D6 的 R2a 作废**（无需再改 `_check_heading_leads`）。Step 1 少一项。`NUMBERED_INTRO_SEC_RE` 公共常量已存在（名为 `INTRO_SECTION_TITLES_ZH` + `_has_numbered_intro_section`），R5/R2 复用它即可，勿重复造。

## C2：P6（承上启下单文件失效）仍需 R4c `--first-chapter`，但 R5 才是主线
- 实测确认：ch3~6 默认模式均无"缺承上"输出（每章判 order==0 走第2章特判静默）。R4c 让单文件可声明章号；R5 让承上口径弹性化。二者仍做。

## C3：以下误报**现存复现，按 design 做**（实测命令与真实输出已核对）
- **P7 图名假阳**：`check_format.py chapter4.tex` 报 L88/111/152/161/187/230 六条 `Mixed Chinese/English punctuation`（全是 `\includegraphics{中文名.png}`）。ch6 同型更多。→ R2b。
- **P8 "特别"假阳**：ch4 L295 `oral expression`（"特别说明"）。→ R2c。
- **P9 方法论论证假阳**：`analyze_logic.py chapter6.tex` 默认模式 2 条。→ R2d。
- **P10 章式误判**：`analyze_logic.py chapter4.tex --process-chapter` 报 L82 P-FRAME Major"框架空泛"+Info 章号映射。→ R2e。
- **P1 P-PAPER 少报**：`--process-chapter` 下 ch4 仅报 L99 一处（实有 L99/295/301/482 四处）。→ R3a 全章全量。
- **P2/P3 草稿态/占位行**：check_format 默认全漏（词表窄）。→ R3b/R3c。

## 脚本输出格式备忘（写 fixture 断言用）
- `check_format.py`：文本报告，行 `[WARNING] file.tex:88: Mixed Chinese/English punctuation detected`。规则名 mixed_punctuation/oral_vague/F-NOTE/F-MD 是内部键，输出里是 message 文本。
- `analyze_logic.py`：`% 模块（第N行）[Severity: X] [Priority: P#]: [Script] CODE 描述`。
- 命令统一 `PYTHONIOENCODING=utf-8 python <script> <tex>`；Windows 下重定向 JSON 需此前缀（勿 export 全局）。
