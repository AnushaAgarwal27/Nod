"""Forget outdated insights (a customer churned or changed their mind).

Usage: python tools/forget.py --customer Sarah --topic reminders
"""
import argparse
import json

from _common import flag, out, store_read, store_write


def forget_cognee(entries):
    # TODO(B): delete the matching data from Cognee (cognee.delete / dataset rebuild),
    # then re-cognify. Until then, recall_local already hides forgotten entries.
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--customer", required=True)
    parser.add_argument("--topic", help="only forget records mentioning this word")
    args = parser.parse_args()

    entries = store_read()
    hit = []
    for e in entries:
        rec = e["record"]
        if e["forgotten"] or str(rec.get("customer", "")).lower() != args.customer.lower():
            continue
        if args.topic and args.topic.lower() not in json.dumps(rec).lower():
            continue
        e["forgotten"] = True
        hit.append(e)
    store_write(entries)

    if flag("NOD_USE_COGNEE") and hit:
        forget_cognee(hit)

    out({"ok": True, "forgotten": len(hit), "ids": [e["id"] for e in hit]})


if __name__ == "__main__":
    main()
