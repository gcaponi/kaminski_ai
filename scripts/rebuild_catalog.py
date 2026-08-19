#!/usr/bin/env python3
"""Reconstrói catalog/kaminskilab-videos.md com títulos pt-BR dos transcripts."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "catalog" / "kaminskilab-videos.md"


def video_ids() -> list[str]:
    ids: list[str] = []
    for line in (ROOT / "video.txt").read_text(encoding="utf-8").splitlines():
        m = re.search(r"v=([A-Za-z0-9_-]{11})", line)
        if m:
            ids.append(m.group(1))
    return ids


def fmt_dur(seconds: int) -> str:
    return f"{seconds // 60}:{seconds % 60:02d}"


def main() -> int:
    ids = video_ids()
    rows = ["# Catálogo oficial @kaminskilab/videos", f"n={len(ids)}"]
    missing: list[str] = []
    for vid in ids:
        path = ROOT / "raw" / "transcripts" / f"{vid}.md"
        if not path.exists():
            missing.append(vid)
            continue
        text = path.read_text(encoding="utf-8")
        tm = re.search(r'^title:\s*"(.*)"', text, re.M)
        dm = re.search(r"^duration_s:\s*(\d+)", text, re.M)
        title = tm.group(1) if tm else vid
        dur = fmt_dur(int(dm.group(1)) if dm else 0)
        rows.append(f"- [{dur}] {title} — https://www.youtube.com/watch?v={vid}")
    OUT.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"ok {len(ids) - len(missing)}/{len(ids)}")
    if missing:
        print("faltando", missing)
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
