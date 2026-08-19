#!/usr/bin/env python3
"""Rewrite existing transcripts as prose (no [00:00:00] lines)."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prose import lines_to_prose

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "raw" / "transcripts"
FM = re.compile(r"^(---\n.*?\n---\n)", re.S)
SHA = re.compile(r"^sha256:\s*.*$", re.M)


def reflow(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8")
    m = FM.match(raw)
    if not m:
        print("SKIP no fm", path.name)
        return False
    head = m.group(1)
    rest = raw[m.end() :]
    if "## Transcript" not in rest:
        print("SKIP no section", path.name)
        return False
    before, after = rest.split("## Transcript", 1)
    cap_lines = []
    for line in after.splitlines():
        if line.startswith("[") and "]" in line[:12]:
            cap_lines.append(line)
        elif line.strip() and not line.startswith("#"):
            # already prose or leftover
            if not line.startswith("- "):
                cap_lines.append(line)
    prose = lines_to_prose(cap_lines)
    if not prose.strip():
        print("SKIP empty", path.name)
        return False
    digest = hashlib.sha256(prose.encode("utf-8")).hexdigest()
    head = SHA.sub(f"sha256: {digest}", head, count=1)
    new = head + before + "## Transcript\n\n" + prose
    if new == raw:
        return False
    path.write_text(new, encoding="utf-8")
    return True


def main() -> int:
    n = 0
    for p in sorted(DIR.glob("*.md")):
        if reflow(p):
            n += 1
            print("OK", p.name)
    print(f"rewrote {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
