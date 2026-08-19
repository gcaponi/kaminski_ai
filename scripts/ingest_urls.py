"""Ingest YouTube URLs into raw/transcripts/.

Reads a text file (one URL or 11-char video ID per line).
Writes one immutable markdown note per video. Skips IDs that already exist.

Usage:
    uv run python scripts/ingest_urls.py catalog/video-urls.txt
    uv run python scripts/ingest_urls.py catalog/video-urls.txt --limit 10
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "raw" / "transcripts"
DEFAULT_LANGS = ("pt", "pt-BR", "pt-PT")
YT_ID_RE = re.compile(r"(?:v=|/shorts/|youtu\.be/|/embed/|/live/)([A-Za-z0-9_-]{11})")
BARE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")


def parse_id(line: str) -> str | None:
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    if BARE_ID_RE.match(line):
        return line
    m = YT_ID_RE.search(line)
    return m.group(1) if m else None


def load_ids(path: Path) -> list[str]:
    ids: list[str] = []
    seen: set[str] = set()
    for raw in path.read_text(encoding="utf-8").splitlines():
        vid = parse_id(raw)
        if not vid or vid in seen:
            continue
        seen.add(vid)
        ids.append(vid)
    return ids


def fetch_transcript(video_id: str) -> tuple[str, list[dict], str]:
    from youtube_transcript_api import YouTubeTranscriptApi

    api = YouTubeTranscriptApi()
    fetched = None
    lang_used = "unknown"
    try:
        fetched = api.fetch(video_id, languages=list(DEFAULT_LANGS))
        lang_used = getattr(fetched, "language_code", None) or "pt"
    except Exception:
        transcript_list = api.list(video_id)
        fetched = transcript_list.find_transcript(
            [t.language_code for t in transcript_list]
        ).fetch()
        lang_used = getattr(fetched, "language_code", None) or "unknown"

    snippets = []
    for item in fetched:
        if isinstance(item, dict):
            snippets.append(item)
        else:
            snippets.append(
                {
                    "text": getattr(item, "text", ""),
                    "start": getattr(item, "start", 0.0),
                    "duration": getattr(item, "duration", 0.0),
                }
            )
    return lang_used, snippets, "ok"


def fmt_ts(seconds: float) -> str:
    s = int(seconds)
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    if h:
        return f"{h:02d}:{m:02d}:{sec:02d}"
    return f"{m:02d}:{sec:02d}"


def body_from_snippets(snippets: list[dict]) -> str:
    lines = []
    for snip in snippets:
        text = " ".join((snip.get("text") or "").split())
        if not text:
            continue
        lines.append(f"[{fmt_ts(float(snip.get('start') or 0))}] {text}")
    return "\n".join(lines).strip() + "\n"


def render_note(video_id: str, lang: str, snippets: list[dict]) -> str:
    body = body_from_snippets(snippets)
    digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
    today = date.today().isoformat()
    duration = 0.0
    if snippets:
        last = snippets[-1]
        duration = float(last.get("start") or 0) + float(last.get("duration") or 0)
    front = "\n".join(
        [
            "---",
            f"source_url: https://www.youtube.com/watch?v={video_id}",
            f"youtube_id: {video_id}",
            f"title: \"\"",
            "channel: \"\"",
            "published: ",
            f"ingested: {today}",
            f"language: {lang}",
            f"duration_s: {int(duration)}",
            "temas: [_inbox]",
            f"sha256: {digest}",
            "---",
            "",
        ]
    )
    note = (
        front
        + f"# {video_id}\n\n"
        + f"- Fonte: https://www.youtube.com/watch?v={video_id}\n"
        + "- Temas: [[_inbox]] · [[gabriel-kaminski]]\n\n"
        + "## Transcript\n\n"
        + body
    )
    return note


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("urls_file", type=Path)
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    if not args.urls_file.is_file():
        print(f"missing file: {args.urls_file}", file=sys.stderr)
        return 2

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ids = load_ids(args.urls_file)
    if args.limit:
        ids = ids[: args.limit]

    ok = skip = fail = 0
    for video_id in ids:
        dest = OUT_DIR / f"{video_id}.md"
        if dest.exists():
            print(f"SKIP {video_id}")
            skip += 1
            continue
        try:
            lang, snippets, _ = fetch_transcript(video_id)
            if not snippets:
                raise RuntimeError("empty transcript")
            dest.write_text(render_note(video_id, lang, snippets), encoding="utf-8")
            print(f"OK   {video_id}  lang={lang}  segs={len(snippets)}")
            ok += 1
        except Exception as exc:
            print(f"FAIL {video_id}  {type(exc).__name__}: {exc}")
            fail += 1

    print(f"\ndone ok={ok} skip={skip} fail={fail} total={len(ids)}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
