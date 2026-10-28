# Presenting and Speaker Notes

This file explains the difference between the two PDFs, the slide build and the presenter build, the content of the note pages, and how to present on two screens with FerroStage or pympress. For the five note fields, see [Speaker Notes Format](speaker-notes.md). For the check of the presenter build, see D-NOTES-PDF in [Quality Gate](quality-gate.md).

## Two PDFs

| File                | Source                                  | Pages                                                    | Use                                  |
| ------------------- | --------------------------------------- | -------------------------------------------------------- | ------------------------------------ |
| `defense.pdf`       | `defense.tex`                           | 16:9 slides, one page per frame                          | Submission, printing, single-screen presenting, `preview` |
| `defense-notes.pdf` | `defense-notes.tex` (loads `defense.tex`) | The left half of each page is the slide and the right half is the speaker note of the frame; page ratio 32:9 | Two-screen presenter mode            |

- `build_deck.py --compile` compiles the slide build first and then the presenter build. `--no-notes-pdf` compiles only the slide build, and `build_manifest.json` records `notes_pdf` as `null`.
- The two PDFs have the same page count, and the page labels of both are `1, 2, 3, …`. Each page of the presenter build has a unique page label, so the presenter tool does not take two adjacent frames for the steps of one frame.
- After you change the speaker notes, run `build_deck.py --force --compile`; the two PDFs compile again together. Do not edit `defense.tex` or `defense-notes.tex` by hand.

## Note Page Content

The note of each frame comes from `notes` of that frame in the plan. `\DefenseNote` writes it in the frame, in this order:

1. **要点** (key point; one bold line).
2. **说什么** (what to say; body text).
3. **过渡** (transition; one gray line that starts with “→”), with the seconds of the page at the end of the line.

- “可能提问” (possible questions) does not go into the note pages. It is used only in `notes.md` and in the defense question preparation. The presenter screen has limited space, and the questions are preparation material before the defense.
- `**关键词**` (keyword) in the text is only bold on the note page, with no color. An empty field renders as empty, not as “无” (none).
- An unfilled placeholder “〔待填写〕” (to be filled) appears on the note page as is; the quality gate reports D-PLACEHOLDER in `notes.md`.
- The note font size is `\small`. A “说什么” of about 250 characters takes about half of the note half-page.

## FerroStage (Recommended, Windows)

[FerroStage](https://github.com/bahayonghang/ferrostage) is an offline two-screen PDF presenter that recognizes Beamer same-page notes.

- Platform: x64 Windows 10 1903 or later, or Windows 11. There is no macOS or Linux version.
- Installation: there is no GitHub Release installer yet. In the source repository, run `just release` to make `FerroStage-<version>-windows-x64-Setup.exe`, then double-click it to install (a Rust toolchain is required);
  developers can also run `just build` and then run `target\release\ferrostage.exe` directly. The README of that repository gives the exact requirements.
- Presenting steps:
  1. Open `defense-notes.pdf` (not `defense.pdf`) with FerroStage.
  2. When all pages have the same size and the width-to-height ratio is about 3.56, FerroStage proposes the `Right` layout automatically: the left half is the slide and the right half is the note. The interface marks this as a result inferred from the ratio.
  3. When it does not recognize the layout or recognizes it wrongly, select `Right` in the layout menu by hand.
  4. The presenter window shows the slide and the note; the audience window (projector) shows only the slide in the left half.
- FerroStage reads the notes only from the PDF. It does not read `notes.md`.
- FerroStage watches the PDF file for changes. When you compile the presenter build again before the talk, it reloads the file and keeps the current page.

## pympress (Cross-Platform)

macOS and Linux users use [pympress](https://github.com/Cimbali/pympress) (GPL-2.0+, also supports Windows). Open `defense-notes.pdf`; it also recognizes Beamer notes on the right;
when it does not recognize them automatically, select the right side in the note position menu.

## Without Two Screens

- Present `defense.pdf` on one screen, and hold a printed `notes.md`, or open `defense-notes.pdf` on another device.
- Do not project the presenter build on the audience screen: the audience would see the speech.
