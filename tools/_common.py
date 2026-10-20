"""Shared helpers for Nod tools: .env loading, JSON output, local fallback store."""
import json
import os
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEMORY_DIR = ROOT / "memory"
STORE = MEMORY_DIR / "store.jsonl"
LEDGER = MEMORY_DIR / "ledger.json"

KINDS = ("insight", "lesson", "feature")


def load_env():
    path = ROOT / ".env"
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


load_env()


def flag(name):
    return os.environ.get(name, "0") == "1"


def out(obj, code=0):
    print(json.dumps(obj, indent=2))
    sys.exit(code)


def fail(msg, code=1):
    out({"ok": False, "error": msg}, code)


# --- Local fallback store (also the source of truth for forget) ---

def store_append(kind, record):
    MEMORY_DIR.mkdir(exist_ok=True)
    entry = {"id": uuid.uuid4().hex[:8], "kind": kind, "forgotten": False, "record": record}
    with STORE.open("a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry


def store_read():
    if not STORE.exists():
        return []
    return [json.loads(line) for line in STORE.read_text().splitlines() if line.strip()]


def store_write(entries):
    MEMORY_DIR.mkdir(exist_ok=True)
    STORE.write_text("".join(json.dumps(e) + "\n" for e in entries))
