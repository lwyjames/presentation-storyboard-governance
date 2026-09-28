#!/usr/bin/env python3
"""Validate a Storyboard_Manifest.md and optionally emit its derived page map."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


FRONT_RE = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.DOTALL)
SLIDE_RE = re.compile(
    r"(?ms)^## (?P<heading_id>[A-Z][A-Z0-9-]+)｜(?P<heading_title>[^\n]+)\n\n"
    r"```yaml\n(?P<meta>.*?)\n```\n(?P<body>.*?)(?=^## [A-Z][A-Z0-9-]+｜|\Z)"
)
ID_RE = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+$")


def scalar(value: str):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1].replace('\\"', '"').replace('\\\\', '\\')
    if value in {"true", "false"}:
        return value == "true"
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def parse_flat_yaml(text: str) -> dict[str, object]:
    values: dict[str, object] = {}
    for number, line in enumerate(text.splitlines(), start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"invalid YAML-like line {number}: {line}")
        key, value = line.split(":", 1)
        values[key.strip()] = scalar(value)
    return values


def validate(path: Path, require_approved: bool = False):
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []

    front_match = FRONT_RE.search(text)
    if not front_match:
        return ["missing document YAML front matter"], warnings, []
    try:
        front = parse_flat_yaml(front_match.group("body"))
    except ValueError as exc:
        return [f"front matter: {exc}"], warnings, []

    required_front = {
        "schema_version",
        "document_type",
        "project_id",
        "title",
        "storyboard_version",
        "status",
        "source_of_truth",
        "source_reference",
        "effective_date",
        "slide_count",
        "page_numbers_are_derived",
        "ppt_notes_marker",
    }
    for key in sorted(required_front - front.keys()):
        errors.append(f"front matter missing `{key}`")
    if front.get("document_type") != "storyboard_manifest":
        errors.append("document_type must be `storyboard_manifest`")
    if front.get("status") not in {"draft", "approved"}:
        errors.append("document status must be draft or approved")
    if require_approved and front.get("status") != "approved":
        errors.append("deck handoff requires an approved document")
    if require_approved and front.get("effective_date") in {None, "", "未批准"}:
        errors.append("deck handoff requires an approval effective_date")
    if front.get("source_of_truth") is not True:
        errors.append("source_of_truth must be true")
    if front.get("page_numbers_are_derived") is not True:
        errors.append("page_numbers_are_derived must be true")
    if "STORYBOARD_ID" not in str(front.get("ppt_notes_marker", "")):
        errors.append("ppt_notes_marker must contain STORYBOARD_ID")

    slides = []
    for match in SLIDE_RE.finditer(text):
        try:
            meta = parse_flat_yaml(match.group("meta"))
        except ValueError as exc:
            errors.append(f"{match.group('heading_id')}: {exc}")
            continue
        meta["_heading_id"] = match.group("heading_id")
        meta["_heading_title"] = match.group("heading_title").strip()
        meta["_body"] = match.group("body").strip()
        slides.append(meta)

    if front.get("slide_count") != len(slides):
        errors.append(
            f"slide_count is {front.get('slide_count')!r}, but {len(slides)} slide entries were found"
        )

    required_slide = {
        "slide_id",
        "section_id",
        "order",
        "source_page_reference",
        "type",
        "title",
        "status",
        "revision",
        "locked",
    }
    ids: set[str] = set()
    orders: set[int] = set()
    valid_types = {"cover", "section_divider", "content", "content_locked"}
    valid_statuses = {"approved", "draft", "deprecated"}

    for slide in slides:
        label = str(slide.get("slide_id", slide.get("_heading_id", "unknown")))
        for key in sorted(required_slide - slide.keys()):
            errors.append(f"{label}: missing `{key}`")

        slide_id = slide.get("slide_id")
        if not isinstance(slide_id, str) or not ID_RE.fullmatch(slide_id):
            errors.append(f"{label}: invalid semantic slide_id")
        elif slide_id in ids:
            errors.append(f"{label}: duplicate slide_id")
        else:
            ids.add(slide_id)

        if slide_id != slide.get("_heading_id"):
            errors.append(f"{label}: heading ID and YAML slide_id differ")
        if slide.get("title") != slide.get("_heading_title"):
            errors.append(f"{label}: heading title and YAML title differ")

        order = slide.get("order")
        if not isinstance(order, int) or order <= 0:
            errors.append(f"{label}: order must be a positive integer")
        elif order in orders:
            errors.append(f"{label}: duplicate order {order}")
        else:
            orders.add(order)

        if slide.get("type") not in valid_types:
            errors.append(f"{label}: unsupported type {slide.get('type')!r}")
        if slide.get("status") not in valid_statuses:
            errors.append(f"{label}: unsupported status {slide.get('status')!r}")
        if not isinstance(slide.get("revision"), int) or slide.get("revision", 0) < 1:
            errors.append(f"{label}: revision must be a positive integer")
        if not isinstance(slide.get("locked"), bool):
            errors.append(f"{label}: locked must be true or false")

        body = str(slide.get("_body", ""))
        kind = slide.get("type")
        if kind == "cover" and not all(token in body for token in ("**主标题**", "**视觉设计**")):
            errors.append(f"{label}: cover must retain 主标题 and 视觉设计")
        if kind == "section_divider" and not all(
            token in body for token in ("**章节标题**", "**章节引导语**", "**视觉设计**")
        ):
            errors.append(f"{label}: section divider must retain 章节标题、章节引导语、视觉设计")
        if kind == "content" and not all(token in body for token in ("**核心表达**", "**视觉设计**")):
            errors.append(f"{label}: content slide must retain 核心表达 and 视觉设计")
        if kind == "content_locked" and slide.get("locked") is not True:
            errors.append(f"{label}: content_locked must set locked: true")

    active = [s for s in slides if s.get("status") != "deprecated"]
    if require_approved:
        for slide in active:
            if slide.get("status") != "approved":
                errors.append(f"{slide.get('slide_id', 'unknown')}: deck handoff requires approved slide status")
    active.sort(key=lambda item: item.get("order", 0))
    page_map = [
        {
            "page": page,
            "order": slide.get("order"),
            "slide_id": slide.get("slide_id"),
            "section_id": slide.get("section_id"),
            "title": slide.get("title"),
        }
        for page, slide in enumerate(active, start=1)
    ]
    return errors, warnings, page_map


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--page-map", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--require-approved", action="store_true", help="require approval before deck production")
    args = parser.parse_args()

    errors, warnings, page_map = validate(args.manifest, require_approved=args.require_approved)
    result = {
        "valid": not errors,
        "slides": len(page_map),
        "errors": errors,
        "warnings": warnings,
    }
    if args.page_map:
        args.page_map.parent.mkdir(parents=True, exist_ok=True)
        args.page_map.write_text(
            json.dumps({"slides": page_map}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"{'PASS' if not errors else 'FAIL'}: {len(page_map)} active slides")
        for message in errors:
            print(f"ERROR: {message}")
        for message in warnings:
            print(f"WARNING: {message}")
        if args.page_map:
            print(f"Page map: {args.page_map}")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
