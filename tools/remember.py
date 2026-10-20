"""Save an insight, lesson or feature to team memory.

Usage: python tools/remember.py --kind insight --json '{"customer":"Sarah",...}'
"""
import argparse
import json

from _common import KINDS, fail, flag, out, store_append


def remember_cognee(kind, record, entry_id):
    # TODO(B): check against your installed Cognee version.
    import asyncio
    import cognee

    # Store the full record (with its id) so recall can rebuild structured records from Cognee.
    text = json.dumps(dict(record, _id=entry_id, _kind=kind))

    async def run():
        await cognee.add(text, dataset_name=kind)
        await cognee.cognify(datasets=[kind])

    asyncio.run(run())


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
