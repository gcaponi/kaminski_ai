#!/usr/bin/env python3
"""Automatic YouTube transcript ingest via yt-dlp + Chrome Profile 3 cookies.

YouTube blocks datacenter IPs. The VPS already has a logged-in Chrome
profile; we reuse those cookies, one PT-orig track per video, with pacing.

Usage:
    uv run python scripts/ingest_ytdlp.py video.txt
    uv run python scripts/ingest_ytdlp.py video.txt --limit 5
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
from datetime import date
from pathlib import Path

_venv_ytdlp = Path(sys.executable).parent / "yt-dlp"
YTDLP = str(_venv_ytdlp if _venv_ytdlp.exists() else "yt-dlp")
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "raw" / "transcripts"
COOKIE_BROWSER = "chrome:/root/.config/google-chrome/Profile 3"
COOKIE_FILE = Path("/tmp/kaminski-yt-cookies.txt")
WORKDIR = Path("/tmp/yt-caps")
ID_RE = re.compile(r"(?:v=|/shorts/|youtu\.be/|/embed/|/live/)([A-Za-z0-9_-]{11})")
BARE_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
CUE_TS = re.compile(
    r"(\d{2}:\d{2}:\d{2}\.\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2}\.\d{3})"
)
TAG_RE = re.compile(r"<[^>]+>")


def parse_ids(path: Path) -> list[str]:
    ids: list[str] = []
    seen: set[str] = set()
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        vid = None
        if BARE_RE.match(line):
            vid = line
        else:
            found = ID_RE.search(line)
            vid = found.group(1) if found else None
        if not vid or vid in seen:
            continue
        seen.add(vid)
        ids.append(vid)
    return ids


def vtt_to_segments(text: str) -> list[tuple[str, str]]:
    """Keep clean auto-caption lines (no word-level <c> tags), drop dupes."""
    segs: list[tuple[str, str]] = []
    last = ""
    current_ts = "00:00:00"
    for line in text.splitlines():
        m = CUE_TS.search(line)
        if m:
            current_ts = m.group(1)[:8]
            continue
        if not line.strip() or line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:"):
            continue
        if "<c>" in line or "</c>" in line:
            continue
        clean = TAG_RE.sub("", line).strip()
        if not clean or clean == last:
            continue
        last = clean
        segs.append((current_ts, clean))
    return segs


def fmt_body(segs: list[tuple[str, str]]) -> str:
    return "\n".join(f"[{ts}] {text}" for ts, text in segs) + ("\n" if segs else "")


def run(cmd: list[str], timeout: int = 90) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def refresh_cookies() -> None:
    WORKDIR.mkdir(parents=True, exist_ok=True)
    cmd = [
        YTDLP,
        "--cookies-from-browser",
        COOKIE_BROWSER,
        "--cookies",
        str(COOKIE_FILE),
        "--skip-download",
        "--ignore-no-formats-error",
        "--no-warnings",
        "--print",
        "id",
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    ]
    # dummy refresh can 429; that's ok if cookie file appears
    try:
        run(cmd, timeout=60)
    except Exception:
        pass
    if not COOKIE_FILE.exists() or COOKIE_FILE.stat().st_size < 50:
        raise RuntimeError("cookie file not written; is Profile 3 available?")


def fetch_one(video_id: str) -> dict:
    dest_base = WORKDIR / video_id
    for leftover in WORKDIR.glob(f"{video_id}*"):
        leftover.unlink()
    cmd = [
        YTDLP,
        "--cookies",
        str(COOKIE_FILE),
        "--write-auto-sub",
        "--sub-langs",
        "pt-orig",
        "--sub-format",
        "vtt",
        "--write-info-json",
        "--skip-download",
        "--ignore-no-formats-error",
        "--no-warnings",
        "-o",
        str(WORKDIR / "%(id)s"),
        f"https://www.youtube.com/watch?v={video_id}",
    ]
    proc = run(cmd, timeout=120)
    combined = ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()
    if "HTTP Error 429" in combined or "Too Many Requests" in combined:
        return {"ok": False, "error": "429", "detail": combined[-400:]}
    info_path = WORKDIR / f"{video_id}.info.json"
    meta = {"id": video_id, "title": "", "channel": "", "duration": 0, "upload_date": ""}
    if info_path.exists():
        info = json.loads(info_path.read_text(encoding="utf-8"))
        meta.update(
            {
                "id": info.get("id") or video_id,
                "title": info.get("title") or "",
                "channel": info.get("channel") or info.get("uploader") or "",
                "duration": info.get("duration") or 0,
                "upload_date": info.get("upload_date") or "",
            }
        )
    vtts = sorted(WORKDIR.glob(f"{video_id}*.vtt"))
    if not vtts:
        return {
            "ok": False,
            "error": "no_vtt",
            "detail": combined[-400:],
            "meta": meta,
        }
    segs = vtt_to_segments(vtts[0].read_text(encoding="utf-8", errors="replace"))
    if not segs:
        return {"ok": False, "error": "empty_vtt", "meta": meta}
    return {"ok": True, "meta": meta, "segments": segs, "lang": "pt-orig"}


def write_note(video_id: str, payload: dict) -> Path:
    segs = payload["segments"]
    meta = payload["meta"]
    body = fmt_body(segs)
    digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
    title = (meta.get("title") or video_id).replace('"', "'")
    channel = (meta.get("channel") or "").replace('"', "'")
    published = meta.get("upload_date") or ""
    if published and len(published) == 8:
        published = f"{published[:4]}-{published[4:6]}-{published[6:]}"
    duration = int(meta.get("duration") or 0)
    note = "\n".join(
        [
            "---",
            f"source_url: https://www.youtube.com/watch?v={video_id}",
            f"youtube_id: {video_id}",
            f'title: "{title}"',
            f'channel: "{channel}"',
            f"published: {published}",
            f"ingested: {date.today().isoformat()}",
            "language: pt-BR",
            f"duration_s: {duration}",
            "temas: [_inbox]",
            f"sha256: {digest}",
            "---",
            "",
            f"# {title}",
            "",
            f"- Fonte: https://www.youtube.com/watch?v={video_id}",
            "- Temas: [[_inbox]] · [[gabriel-kaminski]]",
            "",
            "## Transcript",
            "",
            body,
        ]
    )
    dest = OUT_DIR / f"{video_id}.md"
    dest.write_text(note, encoding="utf-8")
    return dest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("urls_file", type=Path)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--sleep", type=float, default=5.0)
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    WORKDIR.mkdir(parents=True, exist_ok=True)
    ids = parse_ids(args.urls_file)
    if args.limit:
        ids = ids[: args.limit]

    print(f"videos={len(ids)} cookie_source={COOKIE_BROWSER}", flush=True)
    if not COOKIE_FILE.exists():
        print("refreshing cookies from Chrome Profile 3…", flush=True)
        refresh_cookies()

    ok = skip = fail = ratelimited = 0
    for i, vid in enumerate(ids, 1):
        dest = OUT_DIR / f"{vid}.md"
        if dest.exists() and dest.stat().st_size > 200:
            print(f"[{i}/{len(ids)}] SKIP {vid}", flush=True)
            skip += 1
            continue
        attempt = 0
        while True:
            attempt += 1
            try:
                payload = fetch_one(vid)
            except subprocess.TimeoutExpired:
                payload = {"ok": False, "error": "timeout"}
            except Exception as exc:
                payload = {"ok": False, "error": type(exc).__name__, "detail": str(exc)}
            if payload.get("ok"):
                write_note(vid, payload)
                n = len(payload["segments"])
                title = (payload["meta"].get("title") or "")[:70]
                print(f"[{i}/{len(ids)}] OK   {vid}  segs={n}  {title}", flush=True)
                ok += 1
                time.sleep(args.sleep)
                break
            err = payload.get("error")
            if err == "429" and attempt < 4:
                wait = 30 * attempt
                print(f"[{i}/{len(ids)}] 429  {vid}  backoff {wait}s", flush=True)
                ratelimited += 1
                time.sleep(wait)
                refresh_cookies()
                continue
            print(
                f"[{i}/{len(ids)}] FAIL {vid}  {err}  {payload.get('detail','')[:180]}",
                flush=True,
            )
            fail += 1
            time.sleep(args.sleep)
            break

    print(f"\ndone ok={ok} skip={skip} fail={fail} 429s={ratelimited}", flush=True)
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
