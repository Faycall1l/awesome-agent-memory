#!/usr/bin/env python3
"""Check every link in data/entries.csv.

The list is only useful if its links work, so CI runs this weekly. The checker
is deliberately polite: one request at a time, a delay between requests, a
normal User-Agent, and a short timeout.

Not every non-200 response is a broken link:

  403, 405, 429  the site refuses bots or rate limits. Reported, not fatal.
  404, 410       the page is gone. Fatal.
  other 4xx/5xx  fatal after one retry.

    make links
    python scripts/check_links.py --delay 1.0
    python scripts/check_links.py --section "Frameworks, libraries & tools"
"""

from __future__ import annotations

import argparse
import csv
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

USER_AGENT = (
    "awesome-agent-memory-link-checker/1.0 "
    "(+https://github.com/Faycall1l/awesome-agent-memory)"
)
TOLERATED = {401, 403, 405, 429}


def check(url: str, timeout: float) -> tuple[int | None, str]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, ""
    except urllib.error.HTTPError as error:
        return error.code, error.reason or ""
    except Exception as error:  # noqa: BLE001 - report whatever the network says
        return None, f"{type(error).__name__}: {error}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=ROOT / "data" / "entries.csv")
    parser.add_argument("--delay", type=float, default=1.0, help="seconds between requests")
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--retries", type=int, default=1)
    parser.add_argument("--section", help="only check one section")
    args = parser.parse_args()

    with args.csv.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if args.section:
        rows = [row for row in rows if row["section"] == args.section]
        if not rows:
            parser.error(f"no entries in section {args.section!r}")

    urls: list[tuple[str, str]] = []
    for row in rows:
        urls.append((row["title"], row["link"]))
        if row["extra_url"]:
            urls.append((f"{row['title']} ({row['extra_label']})", row["extra_url"]))

    failures: list[tuple[str, str, str]] = []
    tolerated: list[tuple[str, str, int]] = []

    print(f"checking {len(urls)} links with {args.delay}s between requests\n")
    for index, (title, url) in enumerate(urls, start=1):
        status, detail = check(url, args.timeout)
        for _ in range(args.retries):
            if status is not None and status < 400:
                break
            if status in TOLERATED:
                break
            time.sleep(args.delay)
            status, detail = check(url, args.timeout)

        if status is not None and status < 400:
            mark = "ok"
        elif status in TOLERATED:
            mark = "blocked"
            tolerated.append((title, url, status))
        else:
            mark = "FAIL"
            failures.append((title, url, f"{status or 'error'} {detail}".strip()))
        print(f"[{index:>3}/{len(urls)}] {mark:<8} {url}")

        if index < len(urls):
            time.sleep(args.delay)

    print()
    if tolerated:
        print(f"{len(tolerated)} site(s) blocked automated checks (not counted as failures):")
        for title, url, status in tolerated:
            print(f"  {status}  {title} — {url}")
        print()
    if failures:
        print(f"{len(failures)} broken link(s):", flush=True)
        for title, url, detail in failures:
            print(f"  {detail}  {title} — {url}")
        return 1
    print(f"all {len(urls)} links responded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
