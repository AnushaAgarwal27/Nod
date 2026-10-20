#!/usr/bin/env bash
# Person C, 11:45 check: does Snyk Code catch our planted bugs?
# Plants (1) a hard-coded key used in an HTTP call and (2) SQL built with an f-string,
# scans with the real Snyk CLI, then restores invoiceflow/.
set -uo pipefail
cd "$(dirname "$0")/.."
command -v snyk >/dev/null || { echo "snyk not installed: npm install -g snyk && snyk auth"; exit 1; }

cat > invoiceflow/_planted.py <<'EOF'
import sqlite3
import requests

REMINDER_API_KEY = "sk_live_51HdemoKey9fQ2xV"


def send_reminder(email):
    return requests.post(
        "https://api.remindly.example/v1/send",
        headers={"Authorization": f"Bearer {REMINDER_API_KEY}"},
        json={"to": email},
    )


def find_invoice(client):
    db = sqlite3.connect("invoices.db")
    return db.execute(f"SELECT * FROM invoices WHERE client = '{client}'").fetchall()
EOF

echo "== Clean app (should PASS) =="
mv invoiceflow/_planted.py /tmp/_planted.py
python tools/scan.py invoiceflow/ | head -30
mv /tmp/_planted.py invoiceflow/_planted.py

echo; echo "== With planted bugs (should FAIL, source=snyk) =="
python tools/scan.py invoiceflow/
echo "exit=$?  (1 = blocked, which is what we want)"

rm -f invoiceflow/_planted.py
echo
echo "Look for: \"source\": \"snyk\". Which planted bug did Snyk flag?"
echo " - Hard-coded key flagged -> keep the Round 1 line in agents/builder.md as is."
echo " - Only SQL injection flagged -> change the Round 1 line to plant the f-string SQL instead."
echo " - source is \"local\" -> read snyk_error; usually 'snyk auth' or Snyk Code disabled in org settings."
