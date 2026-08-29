# 执行计划 (C1)

## 前置确认（写代码前必须完成）

- [x] P1 已确认真实锁面：ZH 中文规则独立；EN family 的 Latex 规则锁
      `latex-paper-en / paper-audit / cover-letter`，Typst 规则还锁 `typst-paper`；
      `SECTION_PATTERNS` 未锁。实施时按该集合同步，不使用“三副本”简化判断。
- [x] P2 已确认 EN/ZH/Typst 的 `deai_batch.py` 是独立 pattern 批处理器，不解析
      `deai_check.py` 的 `term_threshold` / `throat_clearing` 痕迹文本；本任务不动。
- [x] P3 已按章节分段重算 `首先/其次/然后/最后`：组织结构/背景聚合密度
      51.05/7.68=6.65，取 `organization=6.6`；本章小结/背景 19.29/7.68=2.51，
      取 `summary=2.5`。结果写入 `research/section-factors.md`。
      **不得凭印象取整数。**
- [x] P4 五篇命中密度为 `[2.64, 0.77, 1.21, 3.79, 2.17]`，inclusive P75=2.64，
      取 `budget_per_10k=2.6`、`min_budget=1`。作者确认保留 P75，并把验收改为语料集总体
      仍有超额痕迹，不要求每篇强制报警。结果写入同一份 research 文档。

## 步骤

### S1 阈值文件与语义开关

- [x] S1.1 `latex-thesis-zh/references/deai/tone-thresholds.yaml`：
      加 `threshold_unit` / `threshold_calibration` / `density_fallback`，
      `term_thresholds` 全表替换为 `research/calibration.md` 的建议值。
- [x] S1.2 同文件加 `section_factors` / `sequence_terms` / `throat_clearing.budget_*`。
- [x] S1.3 `references/deai/tone-terms-zh.md` 同步：表头「阈值」改为「密度上限/万字」，
      "阈值如何生效"一节改写为密度制说明，补回退口径与预算制说明，
      更新"上次复审"日期与来源。
- [x] S1.4 `latex-paper-en/references/deai/tone-thresholds.yaml` 同步结构
      （数值标定属 C3，此处只加字段并保持旧语义可读）。
- [ ] 验证：`uv run --extra dev python -c "import yaml,pathlib;yaml.safe_load(pathlib.Path('academic-writing-skills/latex-thesis-zh/references/deai/tone-thresholds.yaml').read_text(encoding='utf-8'))"`

### S2 密度判定机制（三副本）

- [x] S2.1 canonical = `latex-paper-en/scripts/deai_check.py`：增强 `_iter_visible_lines()`，
      状态化排除多行公式/图表/算法环境与注释，再调用 `extract_visible_text()`；
      新增 `_corpus_size()`、`_density_cap(word, density)`，改写 `_check_term_threshold`
      为同一规范化行流上的密度制 + 回退口径。不得调用 `parser.clean_text()`。
- [x] S2.2 `DEFAULT_THRESHOLDS` 加 `threshold_unit` / `density_fallback`；
      缺 `threshold_unit` 时按旧语义运行并 stderr 提示。
- [x] S2.3 逐字同步到 `latex-thesis-zh` 与 `typst-paper` 副本
      （zh 保留中文 docstring，走 `LOGIC_ALIGNMENTS`）。
- [x] S2.4 `tests/contracts/test_deai_alignment.py`：把新增方法登记进
      `ALIGNMENTS`（en/typst 字节锁）与 `LOGIC_ALIGNMENTS`（含 zh）。
      **不新增豁免项。**
- [x] S2.5 新增 runtime adapter 回归：`cite/ref/label` 参数、行内/多行数学、注释、
      figure/table/algorithm 内容不进入计数或分母；普通正文仍保留。ZH 测试按路径 importlib 加载。
- [ ] 验证：`uv run --extra dev python -m pytest tests/contracts/test_deai_alignment.py -q`

### S3 预算制清嗓子（三副本）

- [x] S3.1 canonical 改 `_check_throat_clearing(section_name)`：每次从全文收集并排序命中、
      只计算一次全文预算，再过滤到当前 section；不得在每节重新发预算。
      痕迹文本含「命中 M / 预算 N / 第 K 处」。
- [x] S3.2 逐字同步到 zh / typst（该方法在 `ALIGNMENTS` 中为字节锁，必须完全一致）。
- [ ] 验证：`uv run --extra dev python -m pytest tests/contracts/test_deai_alignment.py -q`

### S4 章节类型系数

- [x] S4.1 ZH `parsers.py` 独立追加中文 `organization` / `summary`；EN family 按 P1 的
      Latex/Typst 锁集合同步英文规则到 `latex-paper-en / typst-paper / paper-audit / cover-letter`。
- [x] S4.2 `_check_term_threshold` 内对 `sequence_terms` 按章节加权计算上限。
- [x] S4.3 若 P1 结论为"在锁定范围内"，更新 `test_parsers_alignment.py` 散列。
- [ ] 验证：`uv run --extra dev python -m pytest tests/contracts/ -q`

### S5 回归测试

- [x] S5.1 新建 `tests/skills/latex_thesis_zh/test_deai_density.py`：
      - 五篇论文正文片段 fixture（每篇取 §1.1 + §1.4 约 3000–5000 字，
        存 `tests/fixtures/`，注明来源，**不存整篇**）
      - AC1：痕迹数降至个位数，数值写死
      - AC2：密度超阈 2 倍样本仍触发
      - AC3：短文档回退口径 + 扩写 3 倍不翻转
      - AC4：五篇语料合计仍有超额痕迹；每篇痕迹数均非原始命中总数，
        低于 P75 的单篇允许 0 条
      - AC5：序列词章节系数生效
- [x] S5.2 EN 侧对应回归（数值标定属 C3，此处只测机制）。
- [ ] 验证：`uv run --extra dev python -m pytest tests/ academic-writing-skills/*/tests/ -q`

### S6 文档与收尾

- [x] S6.1 `references/modules/deai.md` 更新密度制与预算制描述。
- [x] S6.2 SKILL.md 三处只改 `last_updated`，不改 `version`。
- [x] S6.3 docs/ 双语页面同步；manifest 散列更新
      （`test_docs_bilingual_resources.py`、`test_writing_modules_alignment.py`）。
- [ ] 验证：`just ci`

## 复算命令

```bash
# 阈值、章节系数与清嗓子预算复算（口径见父任务 research/calibration.md）
python .trellis/tasks/08-29-writing-rhythm-arc/research/calibrate_density.py
```

## 评审门

- G1：P1–P4 完成后停下，把 `section_factors` 与 `budget_per_10k` 的标定结果
      交作者确认再进 S1。这两个数直接决定"允许多少"，不能自行拍板。
- G2：S3 完成后跑一次五篇全文，人工看痕迹列表是否"读起来合理"，
      再进 S4。信噪比是本任务的唯一目的，指标绿但读起来仍然刺眼即为失败。

## 回滚点

- S1 后：`threshold_unit` 删除即回旧行为。
- S2/S3 后：`git revert` 单 commit。
- S4 后：`section_factors` 置空表即退化为全文密度制。

## 禁止事项

- 不改 `justfile`、`pyproject.toml`、`uv.lock`。
- 不从 `ALIGNMENTS` / `LOGIC_ALIGNMENTS` 摘除已锁定成员。
- 不改 `burstiness`、`overclaim`、`tense`、`sentence_length` 配置。
- 不把整篇参考论文正文放进仓库。
