#!/usr/bin/env python3
"""
Render the rebuttal revision plan and paste-ready responses from the ledger (latex-thesis-zh).

The script validates workspace/concerns.yaml, then writes workspace/revision_plan.md.
Without --plan-only it also resolves the modification locations against the revised
thesis aux files and writes responses/review-result.md, responses/response-all.md,
responses/response-R<n>.md, and workspace/anchors.json. The responses use
plain-text-equivalent Markdown: copying the raw file and copying the rendered view
give the same text, so the text pastes into a Word form unchanged. Only concerns
with status done are rendered; the others are written as 〔待填写〕.

Contract: references/rebuttal-workflow.md.

Usage:
    uv run python -B $SKILL_DIR/scripts/rebuttal_build.py --workspace DIR [--thesis DIR] \
        [--plan-only] [--force] [--json]

Exit codes: 0 success; 2 ledger or workspace error; 4 a responses file was edited by
hand after the last build and --force is not set.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import sys
from pathlib import Path

import yaml

try:
    import rebuttal_common as rc
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import rebuttal_common as rc

PENDING = "〔待填写〕"
NO_CHANGE = "无（论文未修改）"
ORDINALS = "一二三四五六七八九十"
ACTION_LABELS = {
    "revise": "修改已有内容",
    "add": "补充新内容",
    "clarify": "在回复中说明",
    "partial": "部分采纳",
    "future_work": "列为后续工作",
    "decline": "未采纳",
}
QUOTE_LIMIT = 160


class BuildError(Exception):
    """Workspace or ledger error (exit code 2)."""


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def _enum_error(cid: str, concern: dict, key: str, values: tuple[str, ...]) -> str | None:
    value = concern.get(key)
    if value is not None and value not in values:
        return f"{cid}: {key}={value!r} 不在 {'|'.join(values)} 中"
    return None


def validate(ledger: object, plan_only: bool) -> list[str]:
    """All schema errors of the ledger; an empty list means the ledger is usable."""
    if not isinstance(ledger, dict):
        return ["台账不是 YAML 映射"]
    errors = []
    if ledger.get("schema") != rc.LEDGER_SCHEMA:
        errors.append(f"schema 须为 {rc.LEDGER_SCHEMA}")
    reviewers = ledger.get("reviewers")
    if not isinstance(reviewers, list) or not all(
        isinstance(item, dict) and item.get("id") for item in reviewers
    ):
        errors.append("reviewers 须为含 id 的列表")
    concerns = ledger.get("concerns")
    if not isinstance(concerns, list) or not concerns:
        return [*errors, "concerns 须为非空列表"]
    seen: set[str] = set()
    for index, concern in enumerate(concerns, 1):
        if not isinstance(concern, dict):
            errors.append(f"concerns 第 {index} 项不是映射")
            continue
        cid = str(concern.get("id"))
        match = rc.CONCERN_ID_RE.match(cid)
        if not match:
            errors.append(f"concerns 第 {index} 项: id={cid!r} 不符合 R<n>-<条号>[子项字母]")
        elif cid in seen:
            errors.append(f"{cid}: id 重复")
        else:
            if concern.get("reviewer") != match.group(1):
                errors.append(f"{cid}: reviewer 须为 {match.group(1)}")
            if concern.get("item") != int(match.group(2)):
                errors.append(f"{cid}: item 须为 {match.group(2)}")
        seen.add(cid)
        if not isinstance(concern.get("quote"), str) or not concern["quote"]:
            errors.append(f"{cid}: quote 缺失")
        if concern.get("status") not in rc.STATUSES:
            errors.append(f"{cid}: status 须为 {'|'.join(rc.STATUSES)}")
        for key, values in (
            ("action", rc.ACTIONS),
            ("owner", rc.OWNERS),
            ("category", rc.CATEGORIES),
            ("severity", rc.SEVERITIES),
            ("priority", tuple(rc.PRIORITY.values())),
        ):
            error = _enum_error(cid, concern, key, values)
            if error:
                errors.append(error)
        if plan_only:
            for key in ("action", "owner"):
                if concern.get(key) is None:
                    errors.append(f"{cid}: --plan-only 需要 {key}")
            if not isinstance(concern.get("plan"), str) or not concern["plan"].strip():
                errors.append(f"{cid}: --plan-only 需要 plan")
        elif concern.get("status") in ("planned", "done") and concern.get("action") is None:
            errors.append(f"{cid}: status={concern.get('status')} 时须填写 action")
        for key in ("shared_with", "anchors", "locations"):
            if not isinstance(concern.get(key, []), list):
                errors.append(f"{cid}: {key} 须为列表")
        for location in concern.get("locations") or []:
            if not isinstance(location, dict) or not (
                location.get("label") or location.get("file")
            ):
                errors.append(f"{cid}: locations 每项须含 label 或 file")
        evidence = concern.get("evidence", {"kind": "none"})
        if not isinstance(evidence, dict) or evidence.get("kind") not in rc.EVIDENCE_KINDS:
            errors.append(f"{cid}: evidence.kind 须为 {'|'.join(rc.EVIDENCE_KINDS)}")
        elif not isinstance(evidence.get("files", []), list):
            errors.append(f"{cid}: evidence.files 须为列表")
    return errors


# ---------------------------------------------------------------------------
# Locations
# ---------------------------------------------------------------------------


class Resolver:
    """Current numbers and pages of labels in the revised thesis aux files."""

    def __init__(self, thesis: Path | None) -> None:
        self.labels = rc.load_aux_labels(thesis) if thesis else None
        self.keys = rc.reverse_cites(rc.load_bibcites(thesis)) if thesis else {}

    def current(self, label: str) -> tuple[str | None, str, str] | None:
        """(kind, number, page) of a label or bib key; None when it is not in the aux."""
        if self.labels is not None and label in self.labels:
            aux = self.labels[label]
            return aux.kind, aux.number, aux.page
        if label in self.keys:
            return "reference", self.keys[label], ""
        return None

    def location(self, location: dict, concern: dict) -> str:
        label = location.get("label")
        if label:
            base = next((a for a in concern.get("anchors") or [] if a.get("label") == label), None)
            current = self.current(label) if self.labels is not None else None
            if current is not None:
                kind, number, page = current
                text = rc.anchor_form(kind, number)
                if base is not None and str(base.get("base_number")) != number:
                    text = f"原{rc.anchor_form(kind, str(base.get('base_number')))}，现{text}"
                if kind != "chapter" and page:
                    text += f"（第{page}页）"
                return text
            if base is not None:
                return rc.anchor_form(base.get("kind"), str(base.get("base_number")))
            return str(label)
        if location.get("section"):
            return f"第{location['section']}节"
        return str(location.get("file"))

    def target_files(self, concern: dict) -> list[str]:
        files: list[str] = []
        for location in concern.get("locations") or []:
            label = location.get("label")
            if location.get("file"):
                files.append(str(location["file"]))
            elif label and self.labels is not None and label in self.labels:
                files.append(rc.aux_tex(self.labels[label].file))
            elif label:
                files.append(str(label))
        files += [str(path) for path in (concern.get("evidence") or {}).get("files") or []]
        return list(dict.fromkeys(files))

    def anchors(self, concerns: list[dict]) -> list[dict]:
        entries = []
        for concern in concerns:
            for anchor in concern.get("anchors") or []:
                label = anchor.get("label")
                current = self.current(label) if label and self.labels is not None else None
                if self.labels is None:
                    status = "no_thesis"
                else:
                    status = "resolved" if current is not None else "missing"
                entries.append(
                    {
                        "concern": concern["id"],
                        "text": anchor.get("text"),
                        "label": label,
                        "base_number": anchor.get("base_number"),
                        "base_page": anchor.get("base_page"),
                        "number": current[1] if current else None,
                        "page": (current[2] or None) if current else None,
                        "status": status,
                    }
                )
        return entries


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def reviewer_ids(ledger: dict) -> list[str]:
    ids = [str(item["id"]) for item in ledger.get("reviewers") or []]
    ids += [c["reviewer"] for c in ledger["concerns"] if c["reviewer"] not in ids]
    return sorted(dict.fromkeys(ids), key=lambda rid: int(rid[1:]))


def item_groups(concerns: list[dict], reviewer: str) -> list[list[dict]]:
    groups: dict[int, list[dict]] = {}
    for concern in concerns:
        if concern["reviewer"] == reviewer:
            groups.setdefault(concern["item"], []).append(concern)
    return [sorted(groups[item], key=lambda c: c["id"]) for item in sorted(groups)]


def item_quote(group: list[dict], review_items: dict[str, list[str]]) -> str:
    items = review_items.get(group[0]["reviewer"], [])
    number = group[0]["item"]
    text = items[number - 1] if 0 < number <= len(items) else "；".join(c["quote"] for c in group)
    if len(text) > QUOTE_LIMIT:
        short = next((c.get("quote_short") for c in group if c.get("quote_short")), None)
        return short or text
    return text


def sub_number(concern: dict, index: int) -> int:
    match = rc.CONCERN_ID_RE.match(concern["id"])
    letter = match.group(3) if match else ""
    return ord(letter) - ord("a") + 1 if letter else index


def response_text(concern: dict) -> str:
    if concern.get("status") != "done":
        return PENDING
    text = str(concern.get("response") or "").strip() or PENDING
    shared = [rc.concern_ref(str(item)) for item in concern.get("shared_with") or []]
    if shared:
        verb = "一并修改" if concern.get("action") in rc.MODIFYING_ACTIONS else "一并说明"
        text += f"（与{'、'.join(shared)}{verb}）"
    return text


def location_text(concern: dict, resolver: Resolver) -> str:
    if concern.get("status") != "done":
        return PENDING
    places = [resolver.location(item, concern) for item in concern.get("locations") or []]
    return "；".join(dict.fromkeys(places)) or NO_CHANGE


def reviewer_paragraphs(
    ledger: dict, reviewer: str, review_items: dict[str, list[str]], resolver: Resolver
) -> list[str]:
    paragraphs = []
    for group in item_groups(ledger["concerns"], reviewer):
        paragraphs.append(f"意见{group[0]['item']}：{item_quote(group, review_items)}")
        if len(group) == 1 and sub_number(group[0], 0) == 0:
            concern = group[0]
            paragraphs.append(f"回复：{response_text(concern)}")
            paragraphs.append(f"修改位置：{location_text(concern, resolver)}")
            continue
        for index, concern in enumerate(group, 1):
            number = sub_number(concern, index)
            paragraphs.append(f"（{number}）回复：{response_text(concern)}")
            paragraphs.append(f"（{number}）修改位置：{location_text(concern, resolver)}")
    return paragraphs


def summary_paragraph(ledger: dict, review_items: dict[str, list[str]]) -> str:
    concerns = ledger["concerns"]
    reviewers = reviewer_ids(ledger)
    items = sum(len(review_items.get(rid, [])) for rid in reviewers)
    items = items or len({(c["reviewer"], c["item"]) for c in concerns})
    counts = {action: sum(c.get("action") == action for c in concerns) for action in rc.ACTIONS}
    text = (
        f"总体说明：感谢各位评阅专家对本论文的审阅与指导。{len(reviewers)}位评阅专家共提出"
        f"{items}条意见，拆分为{len(concerns)}项逐项处理"
    )
    parts = [f"{ACTION_LABELS[action]}{count}项" for action, count in counts.items() if count]
    if parts:
        text += f"，其中{'、'.join(parts)}"
    return text + "。下文页码均指修改后论文。"


def join(paragraphs: list[str]) -> str:
    return "\n\n".join(paragraphs) + "\n"


def render_responses(
    ledger: dict, review_items: dict[str, list[str]], resolver: Resolver
) -> dict[str, str]:
    """responses/<name> -> text."""
    outputs: dict[str, str] = {}
    grades = {str(item["id"]): item.get("grade") for item in ledger.get("reviewers") or []}
    reviewers = reviewer_ids(ledger)
    outputs["review-result.md"] = (
        "；".join(f"总体评价 {rid[1:]}（{grades.get(rid) or ' '}）" for rid in reviewers) + "\n"
    )
    all_paragraphs = ["博士生修改说明", summary_paragraph(ledger, review_items)]
    for index, rid in enumerate(reviewers):
        body = reviewer_paragraphs(ledger, rid, review_items, resolver)
        ordinal = ORDINALS[index] if index < len(ORDINALS) else str(index + 1)
        all_paragraphs += [f"{ordinal}、评阅人{rid[1:]}意见的修改说明", *body]
        outputs[f"response-{rid}.md"] = join([f"评阅人{rid[1:]}意见的修改说明", *body])
    outputs["response-all.md"] = join(all_paragraphs)
    return outputs


def plan_rows(ledger: dict, resolver: Resolver) -> list[dict[str, str]]:
    """One row per group of concerns linked by shared_with."""
    concerns = {c["id"]: c for c in ledger["concerns"]}
    parent = {cid: cid for cid in concerns}

    def find(cid: str) -> str:
        while parent[cid] != cid:
            cid = parent[cid]
        return cid

    for cid, concern in concerns.items():
        for other in concern.get("shared_with") or []:
            if other in parent:
                parent[find(str(other))] = find(cid)
    groups: dict[str, list[dict]] = {}
    for cid in sorted(concerns):
        groups.setdefault(find(cid), []).append(concerns[cid])

    def values(group: list[dict], key: str) -> str:
        return "、".join(dict.fromkeys(str(c.get(key) or "") for c in group if c.get(key)))

    rows = []
    for group in groups.values():
        files = [path for c in group for path in resolver.target_files(c)]
        rows.append(
            {
                "意见": "、".join(c["id"] for c in group),
                "分类": values(group, "category"),
                "处理方式": values(group, "action"),
                "负责方": values(group, "owner") or "none",
                "计划": values(group, "plan"),
                "目标文件": "、".join(dict.fromkeys(files)),
                "状态": values(group, "status"),
            }
        )
    rows.sort(key=lambda row: (row["负责方"], row["目标文件"], row["意见"]))
    return rows


def render_plan(ledger: dict, resolver: Resolver) -> str:
    columns = ("意见", "分类", "处理方式", "负责方", "计划", "目标文件", "状态")
    lines = ["# 修改计划", ""]
    rows = plan_rows(ledger, resolver)
    for owner in dict.fromkeys(row["负责方"] for row in rows):
        lines += [f"## 负责方：{owner}", "", f"| {' | '.join(columns)} |"]
        lines.append(f"| {' | '.join('---' for _ in columns)} |")
        for row in rows:
            if row["负责方"] == owner:
                cells = [row[col].replace("|", "\\|").replace("\n", " ") for col in columns]
                lines.append(f"| {' | '.join(cells)} |")
        lines.append("")
    return "\n".join(lines).rstrip("\n") + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def load_inputs(workspace: Path) -> tuple[dict, object]:
    state_path = workspace / "rebuttal_state.json"
    ledger_path = workspace / "concerns.yaml"
    if not state_path.is_file() or not ledger_path.is_file():
        raise BuildError(
            f"{workspace} 缺少 rebuttal_state.json 或 concerns.yaml；先运行 rebuttal_intake.py"
        )
    try:
        state = rc.load_state(state_path)
    except (ValueError, json.JSONDecodeError) as exc:
        raise BuildError(f"状态文件无法读取：{exc}") from exc
    try:
        ledger = yaml.safe_load(ledger_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise BuildError(f"台账不是合法 YAML：{exc}") from exc
    return state, ledger


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "按意见台账写修改计划与可粘贴的修改说明（纯文本等价 Markdown）；"
            "修改位置的编号与页码取修改后论文的 aux。"
        )
    )
    parser.add_argument(
        "--workspace", required=True, help="rebuttal_intake.py 创建的 workspace/ 目录"
    )
    parser.add_argument("--thesis", help="修改后的论文仓库根目录；提供时用 aux 解析编号与页码")
    parser.add_argument("--plan-only", action="store_true", help="只写 workspace/revision_plan.md")
    parser.add_argument("--force", action="store_true", help="覆盖被手改的 responses 文件")
    parser.add_argument("--json", action="store_true", help="输出 JSON 摘要")
    args = parser.parse_args(argv)

    workspace = Path(args.workspace).resolve()
    root = workspace.parent
    responses = root / "responses"
    thesis = Path(args.thesis).resolve() if args.thesis else None
    try:
        if thesis is not None and not thesis.is_dir():
            raise BuildError(f"论文仓库不存在：{thesis}")
        state, ledger = load_inputs(workspace)
    except BuildError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 2
    errors = validate(ledger, args.plan_only)
    if errors:
        print("错误：台账校验失败", file=sys.stderr)
        for error in errors:
            print(f"  {error}", file=sys.stderr)
        return 2
    assert isinstance(ledger, dict)

    resolver = Resolver(thesis)
    written: list[str] = []
    write(workspace / "revision_plan.md", render_plan(ledger, resolver))
    written.append("workspace/revision_plan.md")
    anchors = resolver.anchors(ledger["concerns"])

    if not args.plan_only:
        outputs = render_responses(ledger, rc.load_review_items(workspace), resolver)
        rendered: dict[str, str] = dict(state.get("rendered") or {})
        edited = []
        for name in outputs:
            rel = f"responses/{name}"
            path = responses / name
            if (
                path.is_file()
                and rendered.get(rel) != hashlib.sha256(path.read_bytes()).hexdigest()
            ):
                edited.append(rel)
        if edited and not args.force:
            print(
                f"错误：{'、'.join(edited)} 在上次生成后被手改；把改动写回台账后重跑，或加 --force 覆盖",
                file=sys.stderr,
            )
            return 4
        for name, text in outputs.items():
            write(responses / name, text)
            rendered[f"responses/{name}"] = sha256_text(text)
            written.append(f"responses/{name}")
        anchors_text = json.dumps(anchors, ensure_ascii=False, indent=2) + "\n"
        write(workspace / "anchors.json", anchors_text)
        written.append("workspace/anchors.json")
        state["rendered"] = rendered
        state["updated"] = datetime.date.today().isoformat()
        rc.dump_state(workspace / "rebuttal_state.json", state)

    unresolved = [f"{a['concern']} {a['text']}" for a in anchors if a["status"] == "missing"]
    resolved = sum(a["status"] == "resolved" for a in anchors)
    if args.json:
        payload = {
            "written": written,
            "anchors_resolved": resolved,
            "anchors_unresolved": unresolved,
            "plan_only": args.plan_only,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for rel in written:
            print(f"已写入 {rel}")
        if thesis is None and not args.plan_only:
            print("未提供 --thesis：修改位置只写台账中的文字，不含现编号与页码")
        print(f"锚点：已解析 {resolved} 个，未解析 {len(unresolved)} 个")
        for item in unresolved:
            print(f"  未解析：{item}")
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8")
    sys.exit(main())
