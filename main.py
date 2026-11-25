#!/usr/bin/env python3
"""Monday Morning Punchlines — make.fun entry.

Writes exactly one joke about Monday mornings to /output/entry.txt.
The joke is a single line, 1-200 characters, no trailing newline, so the
gate's character count is exactly the joke's own length.

Validation (my own checks, run before anything is written):
  * the text mentions Monday, so it is really about Monday mornings
  * 1 <= len(text) <= 200 characters
  * it is one line, not only whitespace, and carries a punchline turn
    (Monday itself calling in sick, and HR assigning me to cover its shift)
  * after writing, the file is read back and must match the joke exactly,
    and the word count must sit in the 8-30 word band that keeps it tight
"""

import os
import sys

JOKE = "Monday called in sick this morning, and HR assigned me to cover its shift."

MIN_CHARS = 1
MAX_CHARS = 200


def validate(text: str) -> None:
    if not text or text != text.strip():
        raise SystemExit("joke must be non-empty with no leading/trailing space")
    if "\n" in text or "\r" in text:
        raise SystemExit("joke must be a single line")
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        raise SystemExit(f"joke is {len(text)} chars, must be {MIN_CHARS}-{MAX_CHARS}")
    if "monday" not in text.lower():
        raise SystemExit("joke must be about Monday mornings")
    words = text.split()
    if not (8 <= len(words) <= 30):
        raise SystemExit(f"joke is {len(words)} words, must be 8-30 for economy")
    if "hr" not in [w.lower().strip(".,") for w in words]:
        raise SystemExit("punchline turn missing: HR must assign the cover shift")
    if not any(word in text.lower() for word in ("sick", "shift", "called")):
        raise SystemExit("punchline turn missing")


def main() -> int:
    validate(JOKE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(JOKE)
    # Read-back check: the file on disk must be byte-identical to the joke.
    with open(out_path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != JOKE:
        raise SystemExit("read-back mismatch: entry.txt does not match the joke")
    print(f"wrote {out_path}: {len(JOKE)} chars, {len(JOKE.split())} words")
    print(JOKE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
