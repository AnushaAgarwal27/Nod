"""Save an insight, lesson or feature to team memory.

Usage: python tools/remember.py --kind insight --json '{"customer":"Sarah",...}'
"""
import argparse
import json

from _common import KINDS, fail, flag, out, store_append


def remember_cognee(kind, record, entry_id):
    from _cognee import cognee, ids_save, run

    # Store the full record (with its id) so recall can rebuild structured records from Cognee.
    text = json.dumps(dict(record, _id=entry_id, _kind=kind))

    info = run(lambda: cognee.add(text, dataset_name=kind))
    # Keep Cognee's data id so forget.py can delete exactly this record.
    for item in info.data_ingestion_info or []:
        ids_save(kind, entry_id, item["data_id"], info.dataset_id)
    run(lambda: cognee.cognify(datasets=[kind]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--kind", required=True, choices=KINDS)
    parser.add_argument("--json", required=True, dest="data")
    args = parser.parse_args()

    try:
        record = json.loads(args.data)
    except json.JSONDecodeError as e:
        fail(f"invalid JSON: {e}")

    # The local store is always written: it's the fallback for recall and the index for forget.
    entry = store_append(args.kind, record)
    backend = "local"
    if flag("NOD_USE_COGNEE"):
        remember_cognee(args.kind, record, entry["id"])
        backend = "cognee"

    out({"ok": True, "kind": args.kind, "id": entry["id"], "backend": backend})


if __name__ == "__main__":
    main()
