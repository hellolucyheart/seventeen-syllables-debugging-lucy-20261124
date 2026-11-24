# SPDX-License-Identifier: MIT
"""Seventeen Syllables of Debugging — make.fun bounty entry.

Writes one fresh haiku about debugging to /output/entry.txt.
Deterministic: the same bytes on every run. No network, no
randomness, no input files, no clock.

The haiku, 5-7-5, seventy-nine characters:

    The breakpoint holds still
    a log line scrolls past midnight
    and I wrote the bug

The picture at the centre is the halted program: a breakpoint
holding the run still while a log line scrolls past midnight.
The last line turns it — the hunted bug was the author's own.
"""

import os
import re

HAIKU = (
    "The breakpoint holds still\n"
    "a log line scrolls past midnight\n"
    "and I wrote the bug"
)

EXPECTED_SYLLABLES = (5, 7, 5)
MAX_CHARS = 200

VOWEL_RUN = re.compile(r"[aeiouy]+")


def count_syllables(word: str) -> int:
    """Rough spoken syllable count for one English word.

    Counts runs of vowels, then drops one for a silent trailing
    "e" (wrote, line, midnight keeps its own two). Every word
    counts at least one syllable.
    """
    clean = re.sub(r"[^a-z]", "", word.lower())
    if not clean:
        return 0
    groups = len(VOWEL_RUN.findall(clean))
    if clean.endswith("e") and groups > 1:
        groups -= 1
    return max(groups, 1)


def validate_haiku(haiku: str) -> str:
    """Return the haiku unchanged, or raise ValueError if it breaks the rules.

    The gate checks /output/entry.txt is UTF-8 text of 1 to 200
    characters, not only whitespace; the judge weighs the 5-7-5
    shape, so the three lines are counted here too.
    """
    chars = len(haiku)
    if not (1 <= chars <= MAX_CHARS):
        raise ValueError(f"haiku is {chars} characters, must be 1-{MAX_CHARS}")
    if not haiku.strip():
        raise ValueError("haiku must not be only whitespace")
    if haiku != haiku.strip():
        raise ValueError("haiku must not start or end with whitespace")
    lines = haiku.split("\n")
    if len(lines) != 3:
        raise ValueError(f"haiku must be exactly 3 lines, got {len(lines)}")
    for line, expected in zip(lines, EXPECTED_SYLLABLES):
        words = line.split()
        got = sum(count_syllables(w) for w in words)
        if got != expected:
            raise ValueError(
                f"line {line!r} counts {got} syllables, expected {expected}"
            )
    bad = [c for c in haiku if ord(c) < 0x20 and c not in "\t\n"]
    if bad:
        raise ValueError(f"haiku holds control characters: {bad!r}")
    return haiku


def main() -> int:
    haiku = validate_haiku(HAIKU)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(haiku)
    print(f"wrote {len(haiku)} characters to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
