#!/usr/bin/env bash
# Wipe the local memory and ledger and reset InvoiceFlow, for a clean demo take.
# Does NOT wipe Cognee. To do that: python -c "import asyncio,cognee; asyncio.run(cognee.prune.prune_data()); asyncio.run(cognee.prune.prune_system(metadata=True))"
set -euo pipefail
cd "$(dirname "$0")/.."
rm -f memory/store.jsonl memory/ledger.json
git checkout -- invoiceflow/
echo "Local memory, ledger and invoiceflow/ reset."
