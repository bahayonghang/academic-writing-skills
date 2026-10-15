#!/usr/bin/env python3
"""
Check the rebuttal ledger and the rendered responses (latex-defense-zh).

The script reads workspace/concerns.yaml, workspace/rebuttal_state.json, the
normalized reviews, and the files in responses/. It reports R-* findings in the
D-* result line format: coverage of every numbered review item, open concerns,
verbatim quotes, git evidence of the declared modification locations, completion
words in replies that changed nothing, locations against the revised aux, stale
page numbers, renumbered anchors, Markdown syntax that would change the pasted
text, placeholders, numbers missing from the thesis, changed review files,
inconsistent shared concerns, the review-result line, hand edits, and tone. The
thesis repository is read only; git runs only diff --name-only, status --porcelain,
and rev-parse. Results are also written to workspace/check.json.

Contract: references/rebuttal-gate.md.

Usage:
    uv run python -B $SKILL_DIR/scripts/rebuttal_check.py --workspace DIR [--thesis DIR] [--json]

Exit codes: 0 no Critical or Major finding; 1 at least one Critical or Major finding;
2 input error.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    import check_deck
    import rebuttal_common as rc
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import check_deck
    import rebuttal_common as rc

SEVERITY_ORDER = {severity: index for index, severity in enumerate(rc.PRIORITY)}
COMPLETION_WORDS = (
    "已修改",
    "已补充",
    "已增加",
    "已删除",
    "已调整",
    "已完善",
    "已重绘",
    "已修正",
    "已更正",
    "已统一",
)
RESOURCE_WORDS = ("时间", "经费", "工作量")
DISPARAGING_WORDS = ("误解", "不了解", "没有看", "未仔细", "显然", "众所周知", "不懂")
OPENING_LENGTH = 12
OPENING_REPEAT = 3
PLACEHOLDER_RE = re.compile(r"〔待填写〕|(?<![A-Za-z])(?:TODO|TBD|XX)(?![A-Za-z])|\?\?|？？")
MD_LINE_START_RE = re.compile(r"^\s*(?:[#>*]|[-+](?:\s|$)|\d+[.)](?:\s|$))")
MD_INLINE_RULES = (
    ("**", re.compile(r"\*\*")),
    ("__", re.compile(r"__")),
    ("反引号", re.compile(r"`")),
    ("链接", re.compile(r"\[[^\]]*\]\([^)]*\)")),
    ("HTML 标签", re.compile(r"<[A-Za-z/!][^>]*>")),
    ("表格竖线", re.compile(r"\|")),
    ("$", re.compile(r"\$")),
    ("反斜杠", re.compile(r"\\")),
    ("脚注", re.compile(r"\[\^")),
)
MD_HARD_BREAK_RE = re.compile(r" {2,}$")
REPLY_NUMBER_RE = re.compile(r"\d+\.\d+%?|\d+%")
GRADE_LINE_RE = re.compile(r"总体评价\s*(\d+)\s*[（(]\s*([A-E]?)\s*[）)]")
MAIN_NAMES = ("main.tex", "thesis.tex", "document.tex")


class CheckError(Exception):
    """Input error (exit code 2)."""


@dataclass
class Context:
    root: Path
    workspace: Path
    ledger: dict
    ledger_lines: list[str]
    state: dict
    review_items: dict[str, list[str]]
    responses: dict[str, str]
    thesis: Path | None
    labels: dict[str, rc.AuxLabel] | None = None
    keys: dict[str, str] = field(default_factory=dict)
    changed: set[str] | None = None
    excluded: tuple[str, ...] = ()
    thesis_numbers: set[str] | None = None
    findings: list[rc.Finding] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)

    @property
    def concerns(self) -> list[dict]:
        return [c for c in self.ledger.get("concerns") or [] if isinstance(c, dict)]

    def add(
        self, code: str, severity: str, concern: str, message: str, file: str = "", line=None
    ) -> None:
        if not file:
            file, line = "workspace/concerns.yaml", self.ledger_line(concern)
        self.findings.append(rc.Finding(code, severity, concern, file, line, message))

    def ledger_line(self, concern: str) -> int | None:
        pattern = re.compile(rf"^\s*-?\s*id:\s*['\"]?{re.escape(concern)}['\"]?\s*$")
        for number, line in enumerate(self.ledger_lines, 1):
            if pattern.match(line):
                return number
        return None

    def skip(self, name: str) -> None:
        if name not in self.skipped:
            self.skipped.append(name)


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def normalize(text: str) -> str:
    return compact(text).replace("（", "(").replace("）", ")")


def needs_location(concern: dict) -> bool:
    action = concern.get("action")
    return action in rc.MODIFYING_ACTIONS or (
        action == "future_work" and bool(concern.get("locations"))
    )


def is_done(concern: dict) -> bool:
    return concern.get("status") == "done"


def target_files(ctx: Context, concern: dict) -> list[str]:
    """evidence.files, location files, and the tex file of each location label."""
    files = [str(path) for path in (concern.get("evidence") or {}).get("files") or []]
    for location in concern.get("locations") or []:
        if location.get("file"):
            files.append(str(location["file"]))
        label = location.get("label")
        if label and ctx.labels is not None and label in ctx.labels:
            files.append(rc.aux_tex(ctx.labels[label].file))
    return list(dict.fromkeys(path.replace("\\", "/") for path in files))


def is_excluded(ctx: Context, path: str) -> bool:
    return any(path == prefix or path.startswith(prefix + "/") for prefix in ctx.excluded)


# ---------------------------------------------------------------------------
# Checks, in the order of the R-* table
# ---------------------------------------------------------------------------


def check_cover(ctx: Context) -> None:
    present = {(c.get("reviewer"), c.get("item")) for c in ctx.concerns}
    for reviewer, items in ctx.review_items.items():
        for number in range(1, len(items) + 1):
            if (reviewer, number) not in present:
                ctx.add(
                    "R-COVER",
                    "Critical",
                    f"{reviewer}-{number}",
                    f"评阅意见 {reviewer} 第 {number} 条在台账中没有对应条目",
                    f"workspace/reviews/{reviewer}.md",
                )
    for concern in ctx.concerns:
        if is_done(concern) and not str(concern.get("response") or "").strip():
            ctx.add("R-COVER", "Critical", concern["id"], "status=done 但 response 为空")


def check_status(ctx: Context) -> None:
    for concern in ctx.concerns:
        if concern.get("status") in ("open", "planned", "needs_user_input"):
            ctx.add(
                "R-STATUS", "Major", concern["id"], f"条目未完成：status={concern.get('status')}"
            )


def check_quote(ctx: Context) -> None:
    for concern in ctx.concerns:
        items = ctx.review_items.get(str(concern.get("reviewer")), [])
        item = concern.get("item")
        if not isinstance(item, int) or not 0 < item <= len(items):
            ctx.add("R-QUOTE", "Major", concern["id"], "台账条号在评阅原文中不存在")
            continue
        source = compact(items[item - 1])
        if compact(str(concern.get("quote") or "")) not in source:
            ctx.add("R-QUOTE", "Major", concern["id"], "quote 不是评阅原文的逐字子串")
        short = concern.get("quote_short")
        if short and any(compact(part) not in source for part in str(short).split("……")):
            ctx.add("R-QUOTE", "Major", concern["id"], "quote_short 的某一段不是评阅原文的子串")


def check_commit(ctx: Context) -> None:
    for concern in ctx.concerns:
        if not is_done(concern) or not needs_location(concern):
            continue
        evidence = concern.get("evidence") or {}
        kind = evidence.get("kind", "none")
        cid = concern["id"]
        if kind == "none":
            ctx.add("R-COMMIT", "Critical", cid, f"action={concern.get('action')} 需要修改证据")
        elif kind == "user_confirmed":
            if not str(evidence.get("note") or "").strip():
                ctx.add("R-COMMIT", "Minor", cid, "user_confirmed 证据缺少 note 说明")
        elif ctx.changed is None:
            ctx.skip("R-COMMIT(git)")
            ctx.add("R-COMMIT", "Info", cid, "无法核对 git 证据，请用户确认")
        else:
            files = {path for path in target_files(ctx, concern) if not is_excluded(ctx, path)}
            if not files & ctx.changed:
                listed = "、".join(sorted(files)) or "无"
                ctx.add(
                    "R-COMMIT",
                    "Critical",
                    cid,
                    f"声明的修改文件自基线提交以来没有改动：{listed}",
                )


def check_claim(ctx: Context) -> None:
    for concern in ctx.concerns:
        if concern.get("action") not in ("clarify", "decline") and is_done(concern):
            continue
        response = str(concern.get("response") or "")
        words = [word for word in COMPLETION_WORDS if word in response]
        if words:
            ctx.add(
                "R-CLAIM",
                "Critical",
                concern["id"],
                f"action={concern.get('action')}、status={concern.get('status')} 的回复含完成用语："
                f"{'、'.join(words)}",
            )


def check_loc(ctx: Context) -> None:
    if ctx.labels is None:
        ctx.skip("R-LOC(aux)")
    for concern in ctx.concerns:
        if not is_done(concern):
            continue
        cid = concern["id"]
        locations = concern.get("locations") or []
        if needs_location(concern) and not locations:
            ctx.add("R-LOC", "Major", cid, f"action={concern.get('action')} 需要修改位置")
        if ctx.thesis is None or ctx.labels is None:
            continue
        for location in locations:
            label = location.get("label")
            if label and label not in ctx.labels and label not in ctx.keys:
                ctx.add("R-LOC", "Major", cid, f"标签 {label} 不在修改后的 aux 中")
            path = location.get("file")
            if path and not (ctx.thesis / str(path)).is_file():
                ctx.add("R-LOC", "Major", cid, f"位置文件不存在：{path}")


def main_tex(ctx: Context) -> str | None:
    if ctx.thesis is None:
        return None
    main = (ctx.state.get("thesis") or {}).get("main")
    if main and (ctx.thesis / main).is_file():
        return str(main)
    candidates = [
        path.name
        for path in sorted(ctx.thesis.glob("*.tex"))
        if "\\documentclass" in path.read_text(encoding="utf-8", errors="replace")
    ]
    if len(candidates) == 1:
        return candidates[0]
    return next((name for name in MAIN_NAMES if name in candidates), None)


def check_page_stale(ctx: Context) -> None:
    if ctx.thesis is None:
        ctx.skip("R-PAGE-STALE")
        return
    main = main_tex(ctx)
    document_aux = ctx.thesis / Path(main or "document.tex").with_suffix(".aux")
    seen: set[str] = set()
    for concern in ctx.concerns:
        for rel in target_files(ctx, concern):
            tex = ctx.thesis / rel
            if not rel.endswith(".tex") or rel in seen or not tex.is_file():
                continue
            seen.add(rel)
            aux = tex.with_suffix(".aux")
            aux = aux if aux.is_file() else document_aux
            if not aux.is_file():
                ctx.add(
                    "R-LOC", "Major", concern["id"], f"{rel} 没有对应的 aux，请先编译修改后论文"
                )
            elif tex.stat().st_mtime > aux.stat().st_mtime:
                ctx.add(
                    "R-PAGE-STALE",
                    "Major",
                    concern["id"],
                    f"{rel} 晚于 {aux.relative_to(ctx.thesis).as_posix()}，页码可能过期；请重新编译",
                )


def check_renum(ctx: Context) -> None:
    if ctx.labels is None:
        ctx.skip("R-RENUM")
        return
    for concern in ctx.concerns:
        response = normalize(str(concern.get("response") or ""))
        location_labels = {loc.get("label") for loc in concern.get("locations") or []}
        for anchor in concern.get("anchors") or []:
            label = anchor.get("label")
            base = str(anchor.get("base_number"))
            if not label or label in location_labels:
                continue
            if label in ctx.labels:
                kind, number = ctx.labels[label].kind, ctx.labels[label].number
            elif label in ctx.keys:
                kind, number = "reference", ctx.keys[label]
            else:
                continue
            if number == base:
                continue
            old, new = rc.anchor_form(kind, base), rc.anchor_form(kind, number)
            if normalize(old) in response and normalize(new) not in response:
                ctx.add(
                    "R-RENUM", "Minor", concern["id"], f"回复只写了原编号 {old}，修改后为 {new}"
                )


def check_md_syntax(ctx: Context) -> None:
    for rel, text in ctx.responses.items():
        for number, line in enumerate(text.splitlines(), 1):
            problems = []
            if MD_LINE_START_RE.match(line):
                problems.append("行首标记")
            problems += [name for name, pattern in MD_INLINE_RULES if pattern.search(line)]
            if MD_HARD_BREAK_RE.search(line):
                problems.append("行尾硬换行空格")
            if problems:
                ctx.add(
                    "R-MD-SYNTAX",
                    "Major",
                    "-",
                    f"Markdown 语法会改变粘贴结果：{'、'.join(problems)}",
                    rel,
                    number,
                )


def check_placeholder(ctx: Context) -> None:
    for rel, text in ctx.responses.items():
        for number, line in enumerate(text.splitlines(), 1):
            match = PLACEHOLDER_RE.search(line)
            if match:
                ctx.add("R-PLACEHOLDER", "Critical", "-", f"含占位符 {match.group(0)}", rel, number)
    for concern in ctx.concerns:
        match = PLACEHOLDER_RE.search(str(concern.get("response") or ""))
        if match:
            ctx.add(
                "R-PLACEHOLDER", "Critical", concern["id"], f"response 含占位符 {match.group(0)}"
            )


def reply_numbers(text: str) -> list[str]:
    text = check_deck.normalize_digits(text)
    for pattern in check_deck.NUMBER_EXCLUDED_RES:
        text = pattern.sub(" ", text)
    return list(dict.fromkeys(token.rstrip("%") for token in REPLY_NUMBER_RE.findall(text)))


def check_num_src(ctx: Context) -> None:
    if ctx.thesis_numbers is None:
        ctx.skip("R-NUM-SRC")
        return
    for concern in ctx.concerns:
        items = ctx.review_items.get(str(concern.get("reviewer")), [])
        review_numbers = set(check_deck.NUMBER_RE.findall("\n".join(items)))
        for number in reply_numbers(str(concern.get("response") or "")):
            if number in ctx.thesis_numbers:
                continue
            if number in review_numbers:
                message = f"数字 {number} 不在论文中，见于评阅原文（NEEDS-LLM 复核）"
                ctx.add("R-NUM-SRC", "Info", concern["id"], message)
            else:
                message = f"数字 {number} 不在论文可见文本中（NEEDS-LLM 复核）"
                ctx.add("R-NUM-SRC", "Major", concern["id"], message)


def check_review_changed(ctx: Context) -> None:
    reviews_dir = ctx.root / str(ctx.state.get("reviews_dir") or "")
    for review in ctx.state.get("reviews") or []:
        path = reviews_dir / str(review.get("file"))
        rel = f"{ctx.state.get('reviews_dir')}/{review.get('file')}"
        if not path.is_file():
            ctx.add("R-REVIEW-CHANGED", "Major", str(review.get("id")), "评阅书文件不存在", rel)
        elif hashlib.sha256(path.read_bytes()).hexdigest() != review.get("sha256"):
            message = "评阅书文件在 intake 之后有变化；请重跑 rebuttal_intake.py --force"
            ctx.add("R-REVIEW-CHANGED", "Major", str(review.get("id")), message, rel)


def check_shared(ctx: Context) -> None:
    by_id = {c["id"]: c for c in ctx.concerns}
    reported: set[frozenset[str]] = set()
    for concern in ctx.concerns:
        for other_id in concern.get("shared_with") or []:
            other = by_id.get(str(other_id))
            if other is None:
                ctx.add(
                    "R-SHARED", "Minor", concern["id"], f"shared_with 指向不存在的条目 {other_id}"
                )
                continue
            pair = frozenset((concern["id"], other["id"]))
            if pair in reported:
                continue
            reported.add(pair)
            modified = [c.get("action") in rc.MODIFYING_ACTIONS for c in (concern, other)]
            others = [
                c.get("action") in ("clarify", "decline", "future_work") for c in (concern, other)
            ]
            if (modified[0] and others[1]) or (modified[1] and others[0]):
                ctx.add(
                    "R-SHARED",
                    "Minor",
                    concern["id"],
                    f"与 {other['id']} 为同一问题，但一处修改论文、一处未修改"
                    f"（{concern.get('action')} / {other.get('action')}）",
                )


def check_result(ctx: Context) -> None:
    rel = "responses/review-result.md"
    text = ctx.responses.get(rel)
    parsed = dict(GRADE_LINE_RE.findall(text or ""))
    for reviewer in ctx.ledger.get("reviewers") or []:
        rid = str(reviewer.get("id"))
        grade = reviewer.get("grade")
        if grade is None:
            ctx.add("R-RESULT", "Major", rid, "台账中该评阅人的总体评价为空", rel)
        elif text is None:
            ctx.add(
                "R-RESULT", "Major", rid, "review-result.md 未生成；运行 rebuttal_build.py", rel
            )
        elif parsed.get(rid[1:], "") != grade:
            ctx.add("R-RESULT", "Major", rid, f"review-result.md 等级与台账 {grade} 不一致", rel)


def check_sync(ctx: Context) -> None:
    for rel, digest in (ctx.state.get("rendered") or {}).items():
        path = ctx.root / rel
        if not path.is_file():
            ctx.add("R-SYNC", "Minor", "-", "生成的文件已不存在", rel)
        elif hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            ctx.add("R-SYNC", "Minor", "-", "文件在生成后被手改；请把改动写回台账后重新生成", rel)


def check_tone(ctx: Context) -> None:
    openings: dict[str, list[str]] = {}
    for concern in ctx.concerns:
        response = str(concern.get("response") or "")
        if not response.strip():
            continue
        openings.setdefault(compact(response)[:OPENING_LENGTH], []).append(concern["id"])
        cid = concern["id"]
        if concern.get("action") in ("decline", "future_work"):
            words = [word for word in RESOURCE_WORDS if word in response]
            if words:
                message = (
                    f"不采纳或后续工作的理由含「{'、'.join(words)}」，请改为学术理由（NEEDS-LLM）"
                )
                ctx.add("R-TONE", "Info", cid, message)
        words = [word for word in DISPARAGING_WORDS if word in response]
        if words:
            message = f"回复含可能贬抑评阅人的用语：{'、'.join(words)}（NEEDS-LLM）"
            ctx.add("R-TONE", "Info", cid, message)
    for opening, ids in openings.items():
        if len(ids) >= OPENING_REPEAT:
            message = f"{len(ids)} 条回复以同一句开头「{opening}」（NEEDS-LLM）"
            ctx.add("R-TONE", "Info", ids[0], message)


CHECKS = (
    check_cover,
    check_status,
    check_quote,
    check_commit,
    check_claim,
    check_loc,
    check_page_stale,
    check_renum,
    check_md_syntax,
    check_placeholder,
    check_num_src,
    check_review_changed,
    check_shared,
    check_result,
    check_sync,
    check_tone,
)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def build_context(workspace: Path, thesis: Path | None) -> Context:
    root = workspace.parent
    state_path = workspace / "rebuttal_state.json"
    ledger_path = workspace / "concerns.yaml"
    if not state_path.is_file() or not ledger_path.is_file():
        raise CheckError(
            f"{workspace} 缺少 rebuttal_state.json 或 concerns.yaml；先运行 rebuttal_intake.py"
        )
    if thesis is not None and not thesis.is_dir():
        raise CheckError(f"论文仓库不存在：{thesis}")
    try:
        state = rc.load_state(state_path)
        ledger = rc.load_ledger(ledger_path)
    except (ValueError, json.JSONDecodeError) as exc:
        raise CheckError(str(exc)) from exc
    concerns = ledger.get("concerns")
    if not isinstance(concerns, list) or not all(
        isinstance(c, dict) and c.get("id") for c in concerns
    ):
        raise CheckError("台账 concerns 须为含 id 的列表；先用 rebuttal_build.py 校验")
    responses = {
        f"responses/{path.name}": path.read_text(encoding="utf-8")
        for path in sorted((root / "responses").glob("*.md"))
    }
    ctx = Context(
        root=root,
        workspace=workspace,
        ledger=ledger,
        ledger_lines=ledger_path.read_text(encoding="utf-8").splitlines(),
        state=state,
        review_items=rc.load_review_items(workspace),
        responses=responses,
        thesis=thesis,
    )
    if thesis is None:
        return ctx
    ctx.labels = rc.load_aux_labels(thesis)
    ctx.keys = rc.reverse_cites(rc.load_bibcites(thesis))
    excluded = []
    for path in (root, root / str(state.get("reviews_dir") or "")):
        rel = os.path.relpath(path, thesis)
        if not rel.startswith(".."):
            excluded.append(Path(rel).as_posix())
    ctx.excluded = tuple(excluded)
    base = (state.get("thesis") or {}).get("base_commit")
    ctx.changed = rc.git_changed_files(thesis, base) if base else None
    main = main_tex(ctx)
    if main:
        ctx.thesis_numbers = check_deck.load_thesis_numbers({"main_tex": main}, thesis)
    return ctx


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="检查意见台账与 responses：覆盖、原文引用、修改证据、位置与页码、粘贴格式与语气。"
    )
    parser.add_argument(
        "--workspace", required=True, help="rebuttal_intake.py 创建的 workspace/ 目录"
    )
    parser.add_argument("--thesis", help="修改后的论文仓库根目录；不提供时跳过依赖论文的检查")
    parser.add_argument("--json", action="store_true", help="输出 JSON 结果")
    args = parser.parse_args(argv)

    workspace = Path(args.workspace).resolve()
    try:
        ctx = build_context(workspace, Path(args.thesis).resolve() if args.thesis else None)
    except CheckError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 2
    if ctx.thesis is None:
        for name in ("R-COMMIT(git)", "R-LOC(aux)", "R-PAGE-STALE", "R-RENUM", "R-NUM-SRC"):
            ctx.skip(name)
    elif ctx.changed is None:
        ctx.skip("R-COMMIT(git)")
    for check in CHECKS:
        check(ctx)
    ctx.findings.sort(key=lambda f: (SEVERITY_ORDER[f.severity], f.code, f.concern))
    payload = rc.emit(ctx.findings, ctx.skipped, args.json)
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    (workspace / "check.json").write_text(text, encoding="utf-8", newline="\n")
    return 1 if any(f.severity in ("Critical", "Major") for f in ctx.findings) else 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8")
    sys.exit(main())
