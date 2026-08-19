#!/usr/bin/env python3
"""Fix ASR names/handles and set speaker entity on each transcript."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "raw" / "transcripts"

# Longer / more specific first.
REPLACEMENTS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"@dfrancelteror", re.I), "@drafrancieleconter"),
    (re.compile(r"@dorfrancielecontor", re.I), "@drafrancieleconter"),
    (re.compile(r"@dfrancielonter", re.I), "@drafrancieleconter"),
    (re.compile(r"@dfrancielter", re.I), "@drafrancieleconter"),
    (re.compile(r"@dfanciele", re.I), "@drafrancieleconter"),
    (re.compile(r"@dorfrancior", re.I), "@drafrancieleconter"),
    (re.compile(r"@caminscão", re.I), "@kaminskao"),
    (re.compile(r"@camiscão", re.I), "@kaminskao"),
    (re.compile(r"@camenscão", re.I), "@kaminskao"),
    (re.compile(r"@camiscam", re.I), "@kaminskao"),
    (re.compile(r"@camescam", re.I), "@kaminskao"),
    (re.compile(r"Dra\.\s+da\s+Franciara\s+Kaminsk", re.I), "Dra. Franciele Conter"),
    (re.compile(r"Dra\.\s+Francele\s+Kaminsk", re.I), "Dra. Franciele Conter"),
    (re.compile(r"Dra\.\s+Franciell\s+Conter", re.I), "Dra. Franciele Conter"),
    (re.compile(r"Dra\.\s+Franciale\s+Caminski", re.I), "Dra. Franciele Conter"),
    (re.compile(r"Franciele\s+Kaminsk[iy]?", re.I), "Franciele Conter"),
    (re.compile(r"Franciale\s+Caminski", re.I), "Franciele Conter"),
    (re.compile(r"Gabriel\s+Camisque", re.I), "Gabriel Kaminski"),
    (re.compile(r"Gabriel\s+Camiski", re.I), "Gabriel Kaminski"),
    (re.compile(r"Gabriel\s+Camins\b", re.I), "Gabriel Kaminski"),
    (re.compile(r"Gabriel\s+Caminsk[iy]?", re.I), "Gabriel Kaminski"),
    (re.compile(r"Gabriel\s+Kaminsk\b", re.I), "Gabriel Kaminski"),
    (re.compile(r"canal\s+Caminscão", re.I), "canal Kaminski Lab"),
    (re.compile(r"canal\s+Camincão", re.I), "canal Kaminski Lab"),
    (re.compile(r"canal\s+Camiscão", re.I), "canal Kaminski Lab"),
    (re.compile(r"perfis\s+Camincão", re.I), "perfis @kaminskao"),
    (re.compile(r"Instagram\s+Caminscão", re.I), "Instagram @kaminskao"),
    (re.compile(r"Instagram\s+@caminscão", re.I), "Instagram @kaminskao"),
    (re.compile(r"Caminski\s+Clab", re.I), "Kaminski Lab"),
    (re.compile(r"Caminskilab", re.I), "Kaminski Lab"),
    (re.compile(r"Caminskab", re.I), "Kaminski Lab"),
    (re.compile(r"Caminsk\s+Lab", re.I), "Kaminski Lab"),
    (re.compile(r"Caminsk Lab", re.I), "Kaminski Lab"),
    (re.compile(r"Kaminsk Lab", re.I), "Kaminski Lab"),
    (re.compile(r"\bCaminscão\b", re.I), "@kaminskao"),
    (re.compile(r"\bCamincão\b", re.I), "@kaminskao"),
    (re.compile(r"\bCamiscão\b", re.I), "@kaminskao"),
    (re.compile(r"cupom do meu marido Camisc", re.I), "cupom do meu marido @kaminskao"),
]

FRANCIELE = re.compile(
    r"(eu sou a?\s*dra\.?\s+franc)"
    r"|(eu sou franciele)"
    r"|(eu sou a dra\.)"
    r"|(meu marido gabriel)"
    r"|(cupom do meu marido)",
    re.I,
)
GABRIEL = re.compile(
    r"(eu sou o?\s*(dr\.?\s*)?gabriel)"
    r"|(meu nome é gabriel)",
    re.I,
)


# Continuations of Franciele's series without "eu sou" in the clip.
FRANCIELE_IDS = {
    "n_4TkZXtqjY",
    "06IiQ6uAaB8",
}


def detect_speaker(body: str, vid: str = "") -> str:
    if vid in FRANCIELE_IDS:
        return "franciele-conter"
    if FRANCIELE.search(body):
        return "franciele-conter"
    if GABRIEL.search(body):
        return "gabriel-kaminski"
    return "gabriel-kaminski"


def fix_text(text: str) -> str:
    for pat, repl in REPLACEMENTS:
        text = pat.sub(repl, text)
    return text


def set_speaker(text: str, speaker: str) -> str:
    if re.search(r"^speaker:", text, re.M):
        text = re.sub(r"^speaker:.*$", f"speaker: {speaker}", text, count=1, flags=re.M)
    else:
        text = text.replace("---\n", f"---\nspeaker: {speaker}\n", 1)
    # person wikilink on the Temas line
    def swap(m: re.Match[str]) -> str:
        line = m.group(0)
        line = line.replace("[[gabriel-kaminski]]", f"[[{speaker}]]")
        line = line.replace("[[franciele-conter]]", f"[[{speaker}]]")
        if f"[[{speaker}]]" not in line:
            line = line.rstrip() + f" · [[{speaker}]]"
        return line

    text = re.sub(r"^- Temas:.*$", swap, text, count=1, flags=re.M)
    return text


def main() -> None:
    counts = {"gabriel-kaminski": 0, "franciele-conter": 0}
    for path in sorted(DIR.glob("*.md")):
        raw = path.read_text(encoding="utf-8")
        body = raw.split("## Transcript", 1)[-1] if "## Transcript" in raw else raw
        speaker = detect_speaker(body, path.stem)
        new = set_speaker(fix_text(raw), speaker)
        if new != raw:
            path.write_text(new, encoding="utf-8")
        counts[speaker] += 1
        if speaker == "franciele-conter":
            print("FRANCIELE", path.stem)
    print(counts)


if __name__ == "__main__":
    main()
