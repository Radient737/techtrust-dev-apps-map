#!/usr/bin/env python3
"""Stamp meta.json with the map's "last updated" time (SAST, Africa/Johannesburg).

The map banner (index.html) reads meta.json and shows "Updated <d Mon yyyy>".

Usage:
  python3 scripts/stamp_updated.py                 # stamp now (SAST)
  python3 scripts/stamp_updated.py --at 2026-09-28T15:55:04+02:00   # stamp a given time
  python3 scripts/stamp_updated.py --from-git      # use the last commit that touched the data files
"""
import argparse
import json
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
META = ROOT / "meta.json"
GEOJSON = ROOT / "applications.geojson"
DOCS = ROOT / "docs-index.json"
NEWS = ROOT / "news.geojson"
SAST = timezone(timedelta(hours=2), "SAST")  # South Africa has no DST


def from_git() -> datetime:
    out = subprocess.check_output(
        ["git", "-C", str(ROOT), "log", "-1", "--format=%aI", "--",
         GEOJSON.name, DOCS.name, NEWS.name],
        text=True,
    ).strip()
    if not out:
        raise SystemExit("no commit found touching the data files")
    return datetime.fromisoformat(out)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--at", help="ISO-8601 timestamp to stamp instead of now")
    g.add_argument("--from-git", action="store_true", help="use last data commit time")
    args = ap.parse_args()

    if args.at:
        ts = datetime.fromisoformat(args.at)
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=SAST)
    elif args.from_git:
        ts = from_git()
    else:
        ts = datetime.now(SAST)
    ts = ts.astimezone(SAST).replace(microsecond=0)

    count = None
    try:
        count = len(json.loads(GEOJSON.read_text(encoding="utf-8"))["features"])
    except Exception:
        pass

    news_count = None
    try:
        news_count = len(json.loads(NEWS.read_text(encoding="utf-8"))["features"])
    except Exception:
        pass

    meta = {
        "last_updated": ts.isoformat(),
        "last_updated_date": ts.date().isoformat(),
        "last_updated_display": f"{ts.day} {ts.strftime('%b %Y')}, {ts.strftime('%H:%M')} SAST",
        "timezone": "Africa/Johannesburg",
        "feature_count": count,
        "news_count": news_count,
    }
    META.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"meta.json stamped: {meta['last_updated']} ({count} features)")


if __name__ == "__main__":
    main()
