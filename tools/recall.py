"""Search team memory.

Usage: python tools/recall.py "late payments" --kind insight
"""
import argparse
import json
import re

from _common import KINDS, flag, out, store_read


DEFAULT_QUESTION = {
    "insight": "Which customers want or oppose automatic payment reminders and multi-currency invoices, and what did they say?",
    "lesson": "What security lessons must the Builder follow?",
    "feature": "Which features have been shipped and for which customers?",
}


def _records_from(results, kind):
    """Pull our JSON records back out of whatever shape Cognee returns."""
    records = []
    for r in results or []:
        blobs = []
        if isinstance(r, dict):
            blobs = [r.get("text"), r.get("search_result"), json.dumps(r)]
        else:
            blobs = [getattr(r, "text", None), getattr(r, "search_result", None), str(r)]
        for blob in blobs:
            for m in re.finditer(r"\{.*?\"_kind\":\s*\"\w+\"\}", str(blob or ""), re.S):
                try:
                    rec = json.loads(m.group(0))
                except json.JSONDecodeError:
                    continue
                if (not kind or rec.get("_kind") == kind) and rec not in records:
                    records.append(rec)
    return records


def recall_cognee(query, kind, limit):
    # TODO(B): check against your installed Cognee version (SearchType names, datasets kwarg).
    import asyncio
    import cognee
    from cognee import SearchType

    question = query or DEFAULT_QUESTION.get(kind, "What does the team know?")
    datasets = [kind] if kind else None

    async def run():
        answer = await cognee.search(query_text=question, query_type=SearchType.GRAPH_COMPLETION, datasets=datasets)
        chunks = await cognee.search(query_text=question, query_type=SearchType.CHUNKS, datasets=datasets, top_k=max(limit, 20))
        return answer, chunks

    answer, chunks = asyncio.run(run())
    forgotten = {e["id"] for e in store_read() if e["forgotten"]}
    records = [r for r in _records_from(chunks, kind) if r.get("_id") not in forgotten][:limit]
    summary = answer[0] if isinstance(answer, list) and answer else answer
    return {"answer": summary if isinstance(summary, (str, dict)) else str(summary), "results": records}


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
        try:
            out(dict(backend="cognee", **recall_cognee(args.query, args.kind, args.limit)))
        except Exception as e:  # never let the demo die; but make the fallback visible
            res = recall_local(args.query, args.kind, args.limit)
            out({"backend": "local (cognee error)", "cognee_error": str(e), "results": res})
    out({"backend": "local", "results": recall_local(args.query, args.kind, args.limit)})


if __name__ == "__main__":
    main()
