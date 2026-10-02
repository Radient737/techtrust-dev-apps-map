# Techtrust — development applications map

Live: https://radient737.github.io/techtrust-dev-apps-map/ (GitHub Pages from `main`).

## Files
- `index.html` — MapLibre viewer.
- `applications.geojson` — mapped application parcels.
- `docs-index.json` — submission-pack PDF links per erf/key.
- `news.geojson` — local-news items (weekly radar). Points for located items; `geometry: null` items
  show only in the News panel. `properties.id` = `scripts/news_id.py <url>` (sha1 of canonical URL),
  used to dedupe week to week; validate with `python3 scripts/news_id.py --check`.
  Method: `/workspace/watches/news-scan-method.md`.
- `meta.json` — `last_updated` (SAST) + feature and news counts. The banner shows "Updated <date>" from this file
  (fallback if it can't load: the newest `added` date in the GeoJSON).

## Publishing an update (always use this)
After editing the data files:

```bash
cd /workspace/watches/maplibre-viewer
scripts/publish.sh "Weekly 2026-10-05: add Erf 123 George"
```

This stamps `meta.json` with the current SAST time (`scripts/stamp_updated.py`), commits everything,
and pushes to `origin/main`. Pages rebuilds in about 1–2 min; check
https://radient737.github.io/techtrust-dev-apps-map/meta.json.

Safety net: `hooks/pre-commit` re-stamps `meta.json` if `applications.geojson`, `docs-index.json` or
`news.geojson` is committed without it. Enable once per clone with `git config core.hooksPath hooks`
(already set on the box clone).

Other stamp options: `python3 scripts/stamp_updated.py --at 2026-09-28T15:55:04+02:00` or `--from-git`
(time of the last commit that touched the data files).
