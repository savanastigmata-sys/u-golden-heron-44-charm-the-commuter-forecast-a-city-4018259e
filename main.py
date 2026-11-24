"""Charm the Commuter: Forecast a City That Isn't.

Writes one line of weather forecast (at most 140 characters) for a city
that does not exist to $MAKEFUN_OUTPUT_DIR/entry.txt.

The entry is a single fixed text: deterministic, no network, no secrets,
no model calls. validate() enforces the competition gate (UTF-8 text of
1 to 140 characters, not only white space, a single line).
"""

import os
import sys

MAX_CHARS = 140

ENTRY_TEXT = (
    "In Mizzleford, light rain at 12\u00b0, buses four minutes late \u2014 "
    "but the puddles are doing their best impression of the sunrise, "
    "free of charge."
)


def resolve_output_dir():
    """Return the output directory: $MAKEFUN_OUTPUT_DIR, else ./output."""
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out:
        return out
    return os.path.join(os.getcwd(), "output")


def validate(text):
    """Enforce the competition gate; raise ValueError on any violation."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(
            "entry must be 1 to 140 characters, got %d" % len(text)
        )
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if text != text.strip():
        raise ValueError("entry must not start or end with white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def main():
    text = validate(ENTRY_TEXT)
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    # Read the file back and confirm it holds exactly the validated text,
    # so a write failure or encoding surprise can never ship silently.
    with open(path, "r", encoding="utf-8", newline="") as fh:
        written = fh.read()
    if written != text:
        raise ValueError("entry.txt round-trip mismatch")
    validate(written)
    return 0


if __name__ == "__main__":
    sys.exit(main())
