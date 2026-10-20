"""Search team memory.

Usage: python tools/recall.py "late payments" --kind insight
"""
import argparse
import json
import re

from _common import KINDS, flag, out, store_read


def recall_cognee(query, kind, limit):
    # TODO(B): check against your installed Cognee version. Try CHUNKS vs GRAPH_COMPLETION.
    import asyncio
    import cognee
    from cognee import SearchType

    async def run():
        return await cognee.search(
            query_text=query,
            query_type=SearchType.GRAPH_COMPLETION,
            datasets=[kind] if kind else None,
        )

    results = asyncio.run(run())
    return [r if isinstance(r, (dict, str)) else str(r) for r in results][:limit]


def recall_local(query, kind, limit):
    words = [w for w in re.findall(r"\w+", query.lower()) if len(w) > 2]
    scored = []
    for e in store_read():
        if e["forgotten"] or (kind and e["kind"] != kind):
            continue
        text = json.dumps(e["record"]).lower()
        score = sum(text.count(w) for w in words) if words else 1
        if score:
            scored.append((score, e))
    scored.sort(key=lambda s: -s[0])
    return [dict(e["record"], _id=e["id"], _kind=e["kind"]) for _, e in scored[:limit]]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="?", default="")
    parser.add_argument("--kind", choices=KINDS)
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    if flag("NOD_USE_COGNEE"):
        out({"backend": "cognee", "results": recall_cognee(args.query, args.kind, args.limit)})
    out({"backend": "local", "results": recall_local(args.query, args.kind, args.limit)})


if __name__ == "__main__":
    main()
