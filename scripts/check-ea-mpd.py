#!/usr/bin/env python3
"""Compare the EA-MPD workbook's Last-Modified date with the recorded one.

factors/ea-mpd-last-modified.txt holds the Last-Modified header of the ECB
workbook that the factor vintages in factors/data were estimated from.

    python3 scripts/check-ea-mpd.py            # report whether they differ
    python3 scripts/check-ea-mpd.py --record   # store the current value

Inside GitHub Actions the result is also written to $GITHUB_OUTPUT as
`changed` (true or false), `last_modified`, and `recorded`. The script exits
with an error if the ECB does not answer or sends no usable date, so that a
moved or renamed workbook fails the workflow instead of passing silently.
"""

import argparse
import os
import sys
import urllib.request
from email.utils import parsedate_to_datetime
from pathlib import Path

URL = "https://www.ecb.europa.eu/pub/pdf/annex/Dataset_EA-MPD.xlsx"
RECORD = Path(__file__).resolve().parent.parent / "factors" / "ea-mpd-last-modified.txt"


def parse(value, source):
    try:
        return parsedate_to_datetime(value)
    except (TypeError, ValueError):
        sys.exit(f"error: {source} has an unreadable date: {value!r}")


def current_last_modified():
    request = urllib.request.Request(
        URL, method="HEAD", headers={"User-Agent": "ea-mpd-release-check/1.0"}
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        value = response.headers.get("Last-Modified")
    if not value:
        sys.exit(f"error: {URL} sent no Last-Modified header")
    value = value.strip()
    parse(value, URL)
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--record", action="store_true", help=f"write the current value to {RECORD.name}"
    )
    args = parser.parse_args()

    current = current_last_modified()

    if args.record:
        RECORD.write_text(current + "\n")
        print(f"recorded: {current}")
        return

    if not RECORD.exists():
        sys.exit(f"error: {RECORD} is missing; run with --record once")
    recorded = RECORD.read_text().strip()
    changed = parse(current, URL) != parse(recorded, RECORD.name)

    print(f"ECB workbook Last-Modified: {current}")
    print(f"recorded in {RECORD.name}:  {recorded}")
    print("new release" if changed else "no new release")

    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a") as fh:
            fh.write(f"changed={'true' if changed else 'false'}\n")
            fh.write(f"last_modified={current}\n")
            fh.write(f"recorded={recorded}\n")


if __name__ == "__main__":
    main()
