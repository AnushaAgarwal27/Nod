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
import uuid

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


# --- Flexprice (API ref: docs.flexprice.io/api-reference) ---
# Base URL: US accounts https://us.api.flexprice.io/v1, India https://api.cloud.flexprice.io/v1

def _fp(method, path, **kw):
    import requests

    resp = requests.request(
        method,
        os.environ.get("FLEXPRICE_API_URL", "https://us.api.flexprice.io/v1").rstrip("/") + path,
        headers={"x-api-key": os.environ["FLEXPRICE_API_KEY"], "Content-Type": "application/json"},
        timeout=10,
        **kw,
    )
    if resp.status_code >= 400:
        raise RuntimeError(f"{method} {path} -> {resp.status_code}: {resp.text[:300]}")
    return resp.json() if resp.text.strip() else {}


def flexprice_event(name):
    # POST /events -> 202 Accepted (processed async)
    _fp("POST", "/events", json={
        "event_name": name,
        "external_customer_id": os.environ["FLEXPRICE_CUSTOMER_ID"],
        "event_id": f"nod-{name}-{uuid.uuid4().hex[:12]}",
        "properties": {"credits": str(COSTS[name])},
        "source": "nod",
    })


def flexprice_wallet():
    """The customer's wallet. Set FLEXPRICE_WALLET_ID to skip the lookup."""
    wid = os.environ.get("FLEXPRICE_WALLET_ID")
    if wid:
        return _fp("GET", f"/wallets/{wid}/balance/real-time")
    ext = os.environ["FLEXPRICE_CUSTOMER_ID"]
    for key in ("lookup_key", "id"):
        try:
            wallets = _fp("GET", "/customers/wallets", params={key: ext, "include_real_time_balance": "true"})
        except RuntimeError:
            continue
        if isinstance(wallets, dict):
            wallets = wallets.get("items") or wallets.get("wallets") or [wallets]
        live = [w for w in wallets if w.get("wallet_status", "active") == "active"]
        if live:
            return live[0]
    raise RuntimeError(f"no active wallet for customer {ext}; create one in the dashboard or set FLEXPRICE_WALLET_ID")


def flexprice_balance():
    w = flexprice_wallet()
    for field in ("real_time_credit_balance", "credit_balance", "real_time_balance", "balance"):
        if w.get(field) not in (None, ""):
            return int(float(w[field]))
    return None


def flexprice_topup(amount):
    w = flexprice_wallet()
    wid = os.environ.get("FLEXPRICE_WALLET_ID") or w.get("id") or w.get("wallet_id")
    _fp("POST", f"/wallets/{wid}/top-up", json={
        "credits_to_add": str(amount),
        "transaction_reason": "PURCHASED_CREDIT_DIRECT",
        "description": "Founder top-up approved in Band",
        "idempotency_key": f"nod-topup-{uuid.uuid4().hex[:12]}",
    })


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
        credits, backend, err = None, "local", None
        if use_fp:
            try:
                credits, backend = flexprice_balance(), "flexprice"
            except Exception as e:
                err = str(e)
        if credits is None:
            credits, backend = data["credits"], "local"
        res = {"credits": credits, "backend": backend}
        if err:
            res["flexprice_error"] = err
        out(res, NO_CREDITS if credits <= 0 else 0)

    if args.cmd == "topup":
        if use_fp:
            try:
                flexprice_topup(args.amount)
            except Exception as e:
                fail(f"flexprice topup: {e}")
        data["credits"] += args.amount
        save(data)
        out({"ok": True, "credits": data["credits"], "backend": "flexprice" if use_fp else "local"})

    cost = COSTS[args.name]
    if use_fp:
        try:
            live = flexprice_balance()
            if live is not None:
                data["credits"] = live  # Flexprice is the source of truth when enabled
        except Exception:
            pass
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
