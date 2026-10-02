#!/usr/bin/env python3
"""Stable ids + dedupe check for news.geojson.

  python3 scripts/news_id.py <url> [<url> ...]   # print the id for each article URL
  python3 scripts/news_id.py --check             # validate news.geojson (ids match URLs, no duplicates)

id = first 12 hex chars of sha1(canonical URL). Canonical URL: https, lower-case host
without "www.", path without trailing slash, query string and fragment dropped.
An item's "also_urls" (same story from another outlet) count as seen too.
"""
import hashlib
import json
import sys
from pathlib import Path
from urllib.parse import urlsplit

NEWS = Path(__file__).resolve().parent.parent / "news.geojson"


def canonical(url: str) -> str:
    p = urlsplit(url.strip())
    host = p.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    return f"https://{host}{p.path.rstrip('/')}"


def news_id(url: str) -> str:
    return hashlib.sha1(canonical(url).encode("utf-8")).hexdigest()[:12]


def check() -> int:
    feats = json.loads(NEWS.read_text(encoding="utf-8"))["features"]
    seen, bad = {}, 0
    for f in feats:
        p = f["properties"]
        if p["id"] != news_id(p["url"]):
            print(f"id mismatch: {p['id']} != {news_id(p['url'])} for {p['url']}")
            bad += 1
        for u in [p["url"], *p.get("also_urls", [])]:
            k = news_id(u)
            if k in seen and seen[k] != p["id"]:
                print(f"duplicate story URL {u} in {p['id']} and {seen[k]}")
                bad += 1
            seen[k] = p["id"]
    print(f"{len(feats)} items, {sum(1 for f in feats if f['geometry'])} located, {bad} problems")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1:] == ["--check"]:
        sys.exit(check())
    for u in sys.argv[1:]:
        print(news_id(u), u)
