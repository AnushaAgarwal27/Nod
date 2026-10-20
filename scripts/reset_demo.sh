#!/usr/bin/env bash
# Wipe the local memory, ledger and Cognee memory, and reset InvoiceFlow, for a clean demo take.
# Run this only BEFORE Round 1. The restart demo (Round 2) must keep Cognee memory.
set -euo pipefail
cd "$(dirname "$0")/.."
rm -rf .cognee_system .data_storage .cognee_ids.json memory/store.jsonl
rm -f memory/ledger.json
git checkout -- invoiceflow/ .env.example
git clean -fdq invoiceflow/
echo "Local memory, ledger, Cognee memory and invoiceflow/ reset."
