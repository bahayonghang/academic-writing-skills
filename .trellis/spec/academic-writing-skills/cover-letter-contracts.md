# Cover-Letter Claim 与 Journal-Fit 契约

## 1. Scope / Trigger

修改 `cover-letter` 的 claim 抽取、align-check issue、journal-fit 评分或统一 CLI 时适用。
这些路径共享 claim 定义、数字单位、位置字段和 JSON payload；局部复制会重新引入误报或字段漂移。

## 2. Signatures

```text
cover_letter.py --mode journal-fit --letter <path> --journal <venue> [--dedup-length] [--json]
journal_fit_check.py <letter> --venue <venue> [--dedup-length] [--json]
run_journal_fit(letter_path, venue, skill_dir, *, dedup_length=False) -> JournalFitResult
build_claim_map(letter_text, manuscript_facts, max_items=12) -> dict
candidate_to_issue(candidate, facts, letter_text=None) -> AlignCheckIssue | None
```

## 3. Contracts

- `--dedup-length` 只跳过 journal-fit 字数子检查；banned phrases 仍执行，默认关闭。
- `JournalFitResult.warnings` 始终是 `list[str]`；模板缺 `tier` 时回退 `mid-journal` 并警告。
- number+unit 只由 `build_letter_claim_map.NUMBER_UNIT_PATTERN` 定义，verify/extract 必须导入。
- `.tex` letter 在 claim 抽取前调用 `strip_tex_comments`；`.md` 中 `%` 保留为正文。
- claim candidate 输出 `char_offset: int`，相对实际送入 `build_claim_map` 的文本；定位失败为 `-1`。
- align-check issue 透传 `char_offset`，并只按称呼、段界、落款映射
  `header|opening|body|closing`；没有 letter 文本时回退 `body`。
- manuscript title 由 vendored canonical `parsers.extract_title` 提取，不再维护 cover-letter fork。

## 4. Validation & Error Matrix

| Condition | Required behavior |
| --- | --- |
| `.tex` 注释行含 claim | 不产生 candidate/finding；转义 `\%` 活行保留 |
| `.md` claim 含 `%` | 按正文抽取，不执行 LaTeX 注释剥离 |
| 模板缺 `tier` | 使用 `mid-journal`，protocol/JSON/unified payload 均含 warning |
| `dedup_length=true` | 不报告 journal-fit 长度 finding，但 banned phrase 仍可命中 |
| claim 无法回定位 | `char_offset=-1`、`source_section=body` |
| finding 为 dict 或 dataclass | `_exit_code` 均可读 severity；major=2、其他非空 findings=1、空列表=0 |

## 5. Good / Base / Bad Cases

- Good：`47% reduction` 在称呼后首段，candidate/issue 共享非负 offset，section 为 `opening`。
- Base：单独运行 journal-fit 不传 flag，字数检查与旧行为一致，内置模板 warnings 为空。
- Bad：在 verify/extract 再复制数字单位正则，或用 claim 关键词猜 `contributions`/`fit`。

## 6. Tests Required

- `tests/skills/cover_letter/test_cover_letter_align_check.py`：注释、数字局部窗口、offset/section/JSON。
- `tests/skills/cover_letter/test_cover_letter_journal_fit.py`：claim 计数、scope 校准、dedup、缺 tier。
- `tests/skills/cover_letter/test_cover_letter_scripts.py`：单位边界、混类型 exit code、canonical title、通讯作者安全回退。
- `tests/contracts/test_parsers_alignment.py`：本任务不得使 vendored parser 副本漂移。
- 修改公开 references 后至少跑 inventory contract；双语正文同步由拥有该 release gate 的任务完成。

## 7. Wrong vs Correct

```python
# Wrong: private copies drift across claim/verify/extract.
number_pattern = r"\b\d+\s*(?:%|s|ms)"

# Correct: one owner, all consumers import it.
from build_letter_claim_map import NUMBER_UNIT_PATTERN
```

```python
# Wrong: semantic keywords pretend to be structural position.
source_section = "contributions" if "our work" in claim.lower() else "fit"

# Correct: carry the source offset and map only observable letter structure.
source_section = _source_section_for_offset(candidate["char_offset"], letter_text)
```
