#!/usr/bin/env python3
"""Classifica as notas da vault em temas/ com regras determinísticas.

Atualiza:
  - o frontmatter `temas:` e a linha de wikilink Temas em cada nota
  - a lista ## Vídeos de cada temas/*.md
  - temas/_inbox.md

Uso:
    python scripts/classify.py
    python scripts/classify.py --dry-run
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from themes import pick_themes  # noqa: E402

NOTES_DIRS = [ROOT / "raw" / "transcripts", ROOT / "raw" / "docs"]
TEMAS_DIR = ROOT / "temas"
FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)
TITLE_RE = re.compile(r'^title:\s*"(.*)"\s*$', re.M)
TEMAS_LINE_RE = re.compile(r"^temas:\s*\[.*?\]\s*$", re.M)
WIKI_TEMAS_RE = re.compile(r"^- Temas:.*$", re.M)


def parse_note(path: Path) -> tuple[str, str, str]:
    text = path.read_text(encoding="utf-8")
    m = FM_RE.match(text)
    fm = m.group(1) if m else ""
    body = text[m.end() :] if m else text
    tm = TITLE_RE.search(fm)
    title = tm.group(1) if tm else path.stem
    return title, fm, body


def apply_note(path: Path, themes: list[str], dry: bool) -> None:
    text = path.read_text(encoding="utf-8")
    slug_csv = ", ".join(themes)
    sm = re.search(r"^speaker:\s*(\S+)", text, re.M)
    person = sm.group(1) if sm else "gabriel-kaminski"
    links = " · ".join(f"[[{t}]]" for t in themes)
    links = f"{links} · [[{person}]]" if links else f"[[{person}]]"
    text2 = TEMAS_LINE_RE.sub(f"temas: [{slug_csv}]", text, count=1)
    if text2 == text and "temas:" not in text:
        text2 = text.replace("---\n", f"---\ntemas: [{slug_csv}]\n", 1)
    text2 = WIKI_TEMAS_RE.sub(f"- Temas: {links}", text2, count=1)
    if not dry and text2 != text:
        path.write_text(text2, encoding="utf-8")


def rebuild_theme_pages(by_theme: dict[str, list[tuple[str, str]]], dry: bool) -> None:
    today = date.today().isoformat()
    for page in sorted(TEMAS_DIR.glob("*.md")):
        slug = page.stem
        items = by_theme.get(slug, [])
        text = page.read_text(encoding="utf-8")
        text = re.sub(r"^updated:.*$", f"updated: {today}", text, count=1, flags=re.M)
        listing = "\n".join(f"- [[{vid}]] — {title}" for vid, title in items) or "Nenhum ainda."
        if "## Vídeos" in text:
            head, _ = text.split("## Vídeos", 1)
            text = head + "## Vídeos\n\n" + listing + "\n"
        else:
            text = text.rstrip() + "\n\n## Vídeos\n\n" + listing + "\n"
        if not dry:
            page.write_text(text, encoding="utf-8")


def collect_notes() -> list[Path]:
    out: list[Path] = []
    for d in NOTES_DIRS:
        if not d.is_dir():
            continue
        out.extend(p for p in sorted(d.glob("*.md")) if p.name != "README.md")
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    by_theme: dict[str, list[tuple[str, str]]] = defaultdict(list)
    counts: dict[str, int] = defaultdict(int)

    for path in collect_notes():
        title, _fm, body = parse_note(path)
        themes = pick_themes(title, body)
        apply_note(path, themes, args.dry_run)
        for t in themes:
            by_theme[t].append((path.stem, title))
            counts[t] += 1
        print(f"{path.stem:16} {themes}  {title[:60]}")

    rebuild_theme_pages(by_theme, args.dry_run)
    print("\ncounts:")
    for k, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"  {n:3d}  {k}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
