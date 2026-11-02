# Example: Typst Touying Pre-Defense Deck with FerroStage Notes

This example uses the synthetic thesis `evals/fixtures/mini-thesis/` (traffic flow prediction, 7 chapters) and builds the deck with the Touying backend. The thesis title, names, and numbers are all synthetic. The steps to extract the inventory and fill the plan are as in [40-minute pre-defense deck](predefense-40min.md); this example covers only what differs in the Touying backend.

## User Request

> My thesis repository is in `mini-thesis/`. The pre-defense is 40 minutes. I want a deck in Typst Touying with the simply-ysu-touying theme, and I want to see the notes in FerroStage while presenting. Put the output in `defense-work/`.

## 1. Dependency Check

First confirm that this machine has Typst 0.15.1 or later and has cached the three Typst packages (for installation, see [Typst Touying Backend](../references/touying-backend.md)):

| Dependency | Spec                                |
| ---------- | ----------------------------------- |
| Theme      | `@preview/simply-ysu-touying:0.2.0` |
| Touying    | `@preview/touying:0.8.0`            |
| mitex      | `@preview/mitex:0.2.6`              |

The thesis figures must be PDF, PNG, JPG, or SVG; EPS figures cannot be used with the Touying backend.

## 2. Plan Skeleton

After the inventory is extracted (checkpoint 1 as in the Beamer workflow), generate the Touying plan:

```bash
uv run python -B $SKILL_DIR/scripts/plan_deck.py --inventory defense-work/inventory.json --out defense-work/slide_plan.yaml --minutes 40 --stage predefense --theme yanshan --backend touying
```

Output summary:

```text
已写入 defense-work/slide_plan.yaml：帧数 54，内容页数 45，占位符 279
  提示（c2-toc）：Touying 页脚导航：章题超过 6 字，nav_label 暂写「第2章」；建议改成不超过 6 字的短名
  提示（c3-toc）：Touying 页脚导航：章题超过 6 字，nav_label 暂写「第3章」；建议改成不超过 6 字的短名
  ……
```

The plan gains `deck.backend: touying` at the top level and `nav_label` for each chapter. Change long chapter titles to short names, for example:

```yaml
meta:
  chapters:
    - number: 3
      title: 基于时空图卷积的流量补全方法研究
      role: research
      nav_label: 流量补全
deck:
  backend: touying
```

The short name is used only in the footer navigation bar; it does not change the chapter titles on the contents pages or chapter openers, and it does not change the thesis. Fill the other fields as `references/content-rules.md` specifies, in the same way as a Beamer plan. Handle the hints in the plan that start with “Touying” (EPS figures, complex tables, macros that cannot be translated) before building: change the figure, table, or layout, or use the Beamer backend.

## 3. Outline and Build

The `--outline` reading and checkpoint 2 are as in the Beamer workflow. After confirmation, build and compile:

```bash
uv run python -B $SKILL_DIR/scripts/build_deck.py --plan defense-work/slide_plan.yaml --inventory defense-work/inventory.json --out defense-work/deck --compile
```

The output directory `defense-work/deck/` contains `defense.typ`, `notes.md`, `build_manifest.json`, `img/` (copies of the thesis images that the plan uses), `defense.pdf`, `defense-notes.pdf`, and `defense.log`.

When a Typst package is missing, the build script has already written `defense.typ` but does not call typst, and exits with 6:

```text
错误：以下 Typst 包未安装在本机：
  - @preview/mitex:0.2.6：在有网络的环境运行一次 typst compile 让 typst 缓存它，或按 references/touying-backend.md 以 @local 方式安装；本脚本不下载包
```

Ask the user to install it as the reference describes, then rebuild with `build_deck.py --force --compile`.

## 4. Quality Gate

```bash
uv run python -B $SKILL_DIR/scripts/check_deck.py --deck defense-work/deck/defense.typ --inventory defense-work/inventory.json --plan defense-work/slide_plan.yaml
```

Output excerpt (line numbers and counts change with the plan):

```text
% D-OVERFLOW-V (frame=c3-method-1, defense.typ:<行>) [Severity: Major] [Priority: P1]: [Script] 帧内容溢出，自动续出 1 页（第 <页> 页起）；精简内容或拆页
% 汇总：Critical 0，Major 1，Minor 0，Info 0；skipped：D-OVERFLOW-H
```

- The Touying theme continues a frame on extra pages when its content overflows. D-OVERFLOW-V finds the overflowing frame from the page count of each frame; the fix order is as in Beamer: cut text, split into two pages, change the layout, reduce the figure width.
- D-OVERFLOW-H always goes into `skipped`: typst does not report horizontal overflow, and visual review of the preview replaces it.
- After changing the plan, rebuild with `build_deck.py --force --compile`, at most 3 rounds. Do not edit `defense.typ` directly.

## 5. Preview, Presenting, and Checkpoint 3

```bash
uv run python -B $SKILL_DIR/scripts/render_preview.py --pdf defense-work/deck/defense.pdf --out defense-work/deck/preview
```

Example delivery note:

> The deck has 54 pages, and both PDFs compiled; quality gate Critical 0, Major 0, Minor 0. The presenter build `defense-notes.pdf` has 108 pages: each slide page is followed by a `notes:N` notes page.
> For two-screen presenting, open `defense-work/deck/defense-notes.pdf` in FerroStage: it pairs slides and notes by page label automatically, so no split layout needs to be chosen; the projector shows only the slides.
> On macOS or Linux, open the same file in pympress. Submit and print `defense.pdf`.
