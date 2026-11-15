#!/usr/bin/env python3
"""Validate data/entries.csv against the schema this list promises.

Checks structure, not prose: required fields, known sections and kinds,
well-formed URLs, plausible years, unique titles, and the extra-link pair
(label and URL must travel together). Run it before opening a pull request;
CI runs it too.

    make validate
    python scripts/validate.py --csv data/entries.csv
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent

from build_readme import SECTIONS  # noqa: E402

FIELDS = [
    "section",
    "subsection",
    "title",
    "year",
    "link",
    "extra_label",
    "extra_url",
    "description",
    "kind",
]
KINDS = {"paper", "tool", "article", "list"}
SECTION_NAMES = [name for name, _ in SECTIONS]
MIN_YEAR, MAX_YEAR = 1990, 2100
MIN_DESCRIPTION, MAX_DESCRIPTION = 30, 260


def validate(path: Path) -> list[str]:
    errors: list[str] = []

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != FIELDS:
            errors.append(f"header must be exactly: {','.join(FIELDS)}")
            return errors
        rows = list(reader)

    if not rows:
        return ["entries.csv is empty"]

    seen_titles: dict[str, int] = {}
    seen_links: dict[str, int] = {}

    for line_no, row in enumerate(rows, start=2):
        where = f"line {line_no}"

        empty = [field for field in FIELDS if row[field] is None]
        if empty:
            errors.append(f"{where}: missing columns {', '.join(empty)}")
            continue

        title = row["title"].strip()
        if not title:
            errors.append(f"{where}: empty title")
        elif title in seen_titles:
            errors.append(f"{where}: duplicate title (also line {seen_titles[title]}): {title}")
        else:
            seen_titles[title] = line_no

        if row["section"] not in SECTION_NAMES:
            errors.append(f"{where}: unknown section {row['section']!r}")

        if row["kind"] not in KINDS:
            errors.append(f"{where}: unknown kind {row['kind']!r}")

        year = row["year"].strip()
        if not year.isdigit() or not MIN_YEAR <= int(year) <= MAX_YEAR:
            errors.append(f"{where}: year must be a four-digit year, got {row['year']!r}")

        link = row["link"].strip()
        parsed = urlparse(link)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            errors.append(f"{where}: link must be an absolute http(s) URL, got {link!r}")
        elif link in seen_links:
            errors.append(f"{where}: duplicate link (also line {seen_links[link]}): {link}")
        else:
            seen_links[link] = line_no

        label, extra = row["extra_label"].strip(), row["extra_url"].strip()
        if bool(label) != bool(extra):
            errors.append(f"{where}: extra_label and extra_url must be set together")
        elif extra:
            parsed_extra = urlparse(extra)
            if parsed_extra.scheme not in {"http", "https"} or not parsed_extra.netloc:
                errors.append(f"{where}: extra_url must be an absolute http(s) URL, got {extra!r}")

        description = row["description"].strip()
        if len(description) < MIN_DESCRIPTION:
            errors.append(f"{where}: description too short ({len(description)} chars)")
        elif len(description) > MAX_DESCRIPTION:
            errors.append(f"{where}: description too long ({len(description)} chars, max {MAX_DESCRIPTION})")
        if re.search(r"\s{2,}", description):
            errors.append(f"{where}: description contains repeated whitespace")

        if row["section"] == "Related lists & communities" and row["kind"] != "list":
            errors.append(f"{where}: entries in 'Related lists & communities' must have kind 'list'")
        if row["section"] == "Frameworks, libraries & tools" and row["kind"] != "tool":
            errors.append(f"{where}: entries in 'Frameworks, libraries & tools' must have kind 'tool'")
        if row["section"] == "Articles, blogs & talks" and row["kind"] != "article":
            errors.append(f"{where}: entries in 'Articles, blogs & talks' must have kind 'article'")

    for name in SECTION_NAMES:
        if not any(row["section"] == name for row in rows):
            errors.append(f"section is empty: {name}")

    kinds = Counter(row["kind"] for row in rows)
    print(f"{path.name}: {len(rows)} entries ({dict(kinds)}) across {len(SECTION_NAMES)} sections")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=ROOT / "data" / "entries.csv")
    args = parser.parse_args()

    errors = validate(args.csv)
    if errors:
        print(f"\n{len(errors)} problem(s) found:\n", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print("ok: entries.csv is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
