"""Nod dashboard: a live, read-only view of the team's memory.

Usage: .venv/bin/python dashboard/app.py   then open http://localhost:5050

Reads memory/store.jsonl (insights, lessons, features) and memory/ledger.json (credits)
on every request, so it updates while the agents work. It never writes to memory.
Set NOD_MEMORY_DIR to point it at another memory folder (e.g. sample data).
"""
import json
import os
from pathlib import Path

from flask import Flask, jsonify, send_from_directory

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
MEMORY_DIR = Path(os.environ.get("NOD_MEMORY_DIR", ROOT / "memory"))
FREE_CREDITS = int(os.environ.get("NOD_FREE_CREDITS", 20))

SLUGS = {
    "auto_reminders": "Payment reminders",
    "multi_currency": "Multi-currency invoices",
}

app = Flask(__name__)


def read_store():
    path = MEMORY_DIR / "store.jsonl"
    if not path.exists():
        return []
    entries = []
    for line in path.read_text().splitlines():
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue  # a half-written line while an agent is appending
    return entries


def read_ledger():
    path = MEMORY_DIR / "ledger.json"
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return {"credits": FREE_CREDITS, "events": []}


def rank(insights):
    """Group customers by feature slug: who wants it (+), who's against it (-)."""
    ranking = []
    for slug, label in SLUGS.items():
        wants, against = [], []
        for rec in insights:
            side = (rec.get("sentiment") or {}).get(slug)
            name = rec.get("customer", "?")
            if side == "+" and name not in wants:
                wants.append(name)
            elif side == "-" and name not in against:
                against.append(name)
        ranking.append({"slug": slug, "label": label, "wants": wants, "against": against,
                        "conflict": bool(wants and against)})
    # Same order as the PM: most + customers first, fewer - breaks ties.
    ranking.sort(key=lambda r: (-len(r["wants"]), len(r["against"])))
    return ranking


@app.get("/api/state")
def state():
    entries = read_store()
    live = [e for e in entries if not e.get("forgotten")]

    def records(kind, items):
        return [dict(e["record"], _id=e["id"]) for e in items if e.get("kind") == kind]

    insights = records("insight", live)
    ledger = read_ledger()
    return jsonify({
        "insights": insights,
        "lessons": records("lesson", live),
        "features": records("feature", live),
        "forgotten": [dict(e["record"], _id=e["id"], _kind=e.get("kind")) for e in entries if e.get("forgotten")],
        "ranking": rank(insights),
        "credits": {"balance": ledger.get("credits", FREE_CREDITS), "start": FREE_CREDITS,
                    "events": ledger.get("events", [])[-40:]},
    })


@app.get("/")
def index():
    return send_from_directory(HERE, "index.html")


if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 5050)), debug=False)
