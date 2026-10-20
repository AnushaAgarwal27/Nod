"""Credits and usage metering (Flexprice).

Usage:
  python tools/meter.py balance              # exit 2 if zero
  python tools/meter.py event interview_analyzed
  python tools/meter.py topup 100
"""
import argparse
import json
import os
import time

from _common import LEDGER, MEMORY_DIR, fail, flag, out

COSTS = {"interview_analyzed": 1, "security_scan": 1, "feature_shipped": 5}
NO_CREDITS = 2


# --- Local ledger (fallback, and the credit gate until the Flexprice wallet is wired) ---

def ledger():
    if LEDGER.exists():
        return json.loads(LEDGER.read_text())
    return {"credits": int(os.environ.get("NOD_FREE_CREDITS", 20)), "events": []}


def save(data):
    MEMORY_DIR.mkdir(exist_ok=True)
    LEDGER.write_text(json.dumps(data, indent=2))


# --- Flexprice ---

def flexprice_event(name):
    # TODO(C): check the endpoint and body against the Flexprice docs.
    import requests

    resp = requests.post(
        f"{os.environ['FLEXPRICE_API_URL']}/events",
        headers={"x-api-key": os.environ["FLEXPRICE_API_KEY"]},
        json={
            "event_name": name,
            "external_customer_id": os.environ["FLEXPRICE_CUSTOMER_ID"],
            "properties": {"credits": COSTS[name]},
            "source": "nod",
        },
        timeout=10,
    )
    resp.raise_for_status()


def flexprice_balance():
    # TODO(C): read the real wallet balance from Flexprice and return it.
    return None


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("balance")
    ev = sub.add_parser("event")
    ev.add_argument("name", choices=list(COSTS))
    tu = sub.add_parser("topup")
    tu.add_argument("amount", type=int)
    args = parser.parse_args()

    data = ledger()
    use_fp = flag("NOD_USE_FLEXPRICE")

    if args.cmd == "balance":
        credits = flexprice_balance() if use_fp else None
        if credits is None:
            credits = data["credits"]
        out({"credits": credits}, NO_CREDITS if credits <= 0 else 0)

    if args.cmd == "topup":
        data["credits"] += args.amount
        save(data)
        out({"ok": True, "credits": data["credits"]})

    cost = COSTS[args.name]
    if data["credits"] < cost:
        out({"ok": False, "error": "out of credits, ask the founder to top up", "credits": data["credits"]}, NO_CREDITS)
    if use_fp:
        try:
            flexprice_event(args.name)
        except Exception as e:
            fail(f"flexprice: {e}")
    data["credits"] -= cost
    data["events"].append({"event": args.name, "cost": cost, "ts": int(time.time())})
    save(data)
    out({"ok": True, "event": args.name, "cost": cost, "credits": data["credits"], "backend": "flexprice" if use_fp else "local"})


if __name__ == "__main__":
    main()
