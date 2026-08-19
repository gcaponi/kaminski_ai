"""Junta linhas de legenda com timestamp em prosa legível em português."""

from __future__ import annotations

import re

TS_RE = re.compile(r"^\[\d{2}:\d{2}:\d{2}\]\s*")
NOISE_RE = re.compile(r"\[(?:m[uú]sica|music|applause|cheers)\]", re.I)
SPACE_RE = re.compile(r"\s+")
SENT_RE = re.compile(r"(?<=[.!?…])\s+")


def lines_to_prose(lines: list[str], sentences_per_para: int = 4) -> str:
    parts: list[str] = []
    for raw in lines:
        s = TS_RE.sub("", raw).strip()
        s = NOISE_RE.sub("", s)
        s = SPACE_RE.sub(" ", s).strip()
        if s and s not in {">", ">>"}:
            parts.append(s)
    if not parts:
        return ""
    blob = SPACE_RE.sub(" ", " ".join(parts)).strip()
    sents = [s.strip() for s in SENT_RE.split(blob) if s.strip()]
    if not sents:
        return blob
    paras: list[str] = []
    chunk: list[str] = []
    for sent in sents:
        chunk.append(sent)
        if len(chunk) >= sentences_per_para:
            paras.append(" ".join(chunk))
            chunk = []
    if chunk:
        paras.append(" ".join(chunk))
    return "\n\n".join(paras) + "\n"


def segs_to_prose(segs: list[tuple[str, str]]) -> str:
    return lines_to_prose([text for _ts, text in segs])
