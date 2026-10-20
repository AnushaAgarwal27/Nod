"""Cognee setup for Nod tools: repo-local storage, .env loaded first, retry on DB locks.

Usage:
    from _cognee import cognee, run
    run(cognee.add("text", dataset_name="insight"))
"""
import asyncio
import json
import os
import random
import time

from _common import ROOT  # importing _common loads .env into os.environ

SYSTEM_ROOT = ROOT / ".cognee_system"
DATA_ROOT = ROOT / ".data_storage"
IDS_FILE = ROOT / ".cognee_ids.json"

# Cognee reads these at import time, so set them before importing it.
# COGNEE_ENV_FILE pins its own .env lookup to the repo, whatever the working directory.
os.environ.setdefault("COGNEE_ENV_FILE", str(ROOT / ".env"))
os.environ["SYSTEM_ROOT_DIRECTORY"] = str(SYSTEM_ROOT)
os.environ["DATA_ROOT_DIRECTORY"] = str(DATA_ROOT)
# Tools are one-shot CLI calls: skip the per-search session analysis (an extra LLM call).
os.environ.setdefault("AUTO_FEEDBACK", "false")

import cognee  # noqa: E402
import litellm  # noqa: E402

# litellm prints help banners to stdout on errors, which would break the JSON output contract.
litellm.suppress_debug_info = True

# Also set them through the config API: it moves the relational, graph and vector DB paths too.
cognee.config.system_root_directory(str(SYSTEM_ROOT))
cognee.config.data_root_directory(str(DATA_ROOT))

LOCK_RETRIES = 6


def is_lock_error(exc):
    msg = str(exc).lower()
    return "lock" in msg or "busy" in msg


def run(coro_factory, retries=LOCK_RETRIES):
    """Run an async cognee call, retrying with backoff while another process holds a DB lock.

    Pass a zero-arg function that returns a coroutine (a coroutine can't be awaited twice).
    """
    for attempt in range(retries + 1):
        try:
            return asyncio.run(coro_factory())
        except Exception as e:
            if attempt == retries or not is_lock_error(e):
                raise
            time.sleep(min(0.5 * 2 ** attempt, 10) + random.uniform(0, 0.5))


# --- Cognee data IDs, keyed by dataset + label (the local store entry id), so forget can find them ---

def ids_read():
    return json.loads(IDS_FILE.read_text()) if IDS_FILE.exists() else {}


def ids_save(dataset, label, data_id, dataset_id):
    ids = ids_read()
    ids.setdefault(dataset, {})[label] = {"data_id": str(data_id), "dataset_id": str(dataset_id)}
    IDS_FILE.write_text(json.dumps(ids, indent=2))


def ids_pop(dataset, label):
    ids = ids_read()
    entry = ids.get(dataset, {}).pop(label, None)
    if entry:
        IDS_FILE.write_text(json.dumps(ids, indent=2))
    return entry


def result_text(result):
    """Unwrap cognee search results (dicts or SearchResult objects) into plain items."""
    value = result.get("search_result") if isinstance(result, dict) else getattr(result, "search_result", result)
    return value if isinstance(value, list) else [value]
