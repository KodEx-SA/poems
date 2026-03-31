#!/usr/bin/env python3
"""
poem_typer.py — Type your poems in the terminal, character by character.
Usage:
    python3 poem_typer.py --file my_poem.txt     # load from a .txt file
    python3 poem_typer.py --speed 40             # chars per second (default: 25)
    python3 poem_typer.py --color green          # color: green | cyan | white | amber | pink | none
    python3 poem_typer.py --no-pause             # skip the pause between stanzas
"""

import sys
import time
import argparse
import os

# ── ANSI color codes ──────────────────────────────────────────────────────────
COLORS = {
    "green":  "\033[38;2;0;255;100m",
    "cyan":   "\033[38;2;0;220;255m",
    "white":  "\033[38;2;230;230;230m",
    "amber":  "\033[38;2;255;180;0m",
    "none":   "",
}
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
ITALIC = "\033[3m"

# ── Helpers ───────────────────────────────────────────────────────────────────
def clear_screen():
    os.system("clear")

def parse_poem(raw: str):
    """
    Returns (title, author, lines[]).
    Recognises optional 'title:' and 'author:' headers at the top.
    """
    lines = raw.strip().splitlines()
    title = ""
    author = ""
    body_start = 0

    for i, line in enumerate(lines):
        low = line.strip().lower()
        if low.startswith("title:"):
            title = line.split(":", 1)[1].strip()
            body_start = i + 1
        elif low.startswith("author:"):
            author = line.split(":", 1)[1].strip()
            body_start = i + 1
        else:
            break

    body_lines = lines[body_start:]
    # remove leading blank line after headers
    while body_lines and body_lines[0].strip() == "":
        body_lines.pop(0)

    return title, author, body_lines

def type_string(text: str, cps: float, color: str):
    """Type `text` character by character at `cps` chars/sec."""
    delay = 1.0 / cps
    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(RESET)
    sys.stdout.flush()

def print_header(title: str, author: str, color: str):
    width = 60
    print()
    if title:
        display = f"  {BOLD}{color}{title.upper()}{RESET}"
        print(display)
        print(f"  {DIM}{color}{'─' * min(len(title) + 2, width)}{RESET}")
    if author:
        print(f"  {ITALIC}{DIM}{color}by {author}{RESET}")
    print()

def run_poem(lines: list, cps: float, color: str, stanza_pause: float):
    for i, line in enumerate(lines):
        stripped = line.strip()

        if stripped == "":
            # blank line = stanza break — pause before continuing
            print()
            if stanza_pause > 0:
                time.sleep(stanza_pause)
        else:
            sys.stdout.write("  ")  # indent
            type_string(stripped, cps, color)
            print()  # newline after each line

    print()

def print_fin(color: str):
    print(f"\n  {DIM}{color}— fin —{RESET}\n")

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Type your poem in the terminal, character by character."
    )
    parser.add_argument(
        "--file", "-f",
        help="Path to a .txt file containing your poem",
        default=None
    )
    parser.add_argument(
        "--speed", "-s",
        type=float,
        default=25,
        help="Characters per second (default: 25). Higher = faster."
    )
    parser.add_argument(
        "--color", "-c",
        choices=list(COLORS.keys()),
        default="green",
        help="Text color (default: green)"
    )
    parser.add_argument(
        "--no-pause",
        action="store_true",
        help="Disable the pause between stanzas"
    )
    args = parser.parse_args()

    # Load poem
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                raw = f.read()
        except FileNotFoundError:
            print(f"Error: file '{args.file}' not found.")
            sys.exit(1)
    else:
        raw = DEMO_POEM

    title, author, lines = parse_poem(raw)
    color = COLORS[args.color]
    stanza_pause = 0 if args.no_pause else 0.8

    clear_screen()
    print_header(title, author, color)
    time.sleep(0.6)

    try:
        run_poem(lines, cps=args.speed, color=color, stanza_pause=stanza_pause)
        print_fin(color)
    except KeyboardInterrupt:
        print(f"\n\n  {DIM}(interrupted){RESET}\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
