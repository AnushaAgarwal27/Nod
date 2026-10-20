"""Remove private data from a transcript before anything is stored.

Usage: python tools/redact.py data/interviews/sarah.txt > clean.txt
"""
import argparse
import json
import re
import sys

PATTERNS = {
    "email": (re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"), "[EMAIL]"),
    "card": (re.compile(r"\b(?:\d[ -]?){13,16}\b"), "[CARD]"),
    "phone": (re.compile(r"(?:\+?\d{1,3}[ .-]?)?\(?\d{3}\)?[ .-]?\d{3}[ .-]?\d{4}\b"), "[PHONE]"),
    "iban": (re.compile(r"\b[A-Z]{2}\d{2}(?: ?[A-Z0-9]{4}){3,7}\b"), "[IBAN]"),
}


def redact(text):
    counts = {}
    for name, (pattern, token) in PATTERNS.items():
        text, n = pattern.subn(token, text)
        if n:
            counts[name] = n
    return text, counts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()
    with open(args.file) as f:
        text, counts = redact(f.read())
    sys.stdout.write(text)
    sys.stderr.write(json.dumps({"redacted": counts}) + "\n")


if __name__ == "__main__":
    main()
