# Nod

**Customer interviews in, shipped secure features out.**

Demo video: <link>

## Problem

Founders are told to talk to their users, so they run 10–50 interviews. Then the insights end up in scattered notes and docs and get forgotten. Patterns get missed ("7 people asked for this"), contradictions get missed ("the new customer says the opposite"), and features get built on gut feel.

## Target user

- Pre-seed to Series A founders who run their own customer interviews.
- Small product teams that don't have a dedicated user researcher.

## The agent team

Five agents and one human work in a single Band Desktop room. Each agent's instructions are in `agents/`.

| Agent | Band handle | Harness | Job |
|---|---|---|---|
| Trust Agent | `@nod-trust` | Claude Code | Redacts private data from transcripts, runs Snyk on every finished card, blocks or completes it |
| Listener | `@nod-listener` | Claude Code | Turns each interview into one structured insight per customer (pains, requests, verbatim quotes, sentiment) |
| PM | `@nod-pm` | Claude Code | Recalls every insight, counts customers per request, flags conflicts, writes the ranked plan and cards |
| Skeptic | `@nod-skeptic` | Codex | Rejects any card that isn't backed by at least one real customer quote from memory |
| Builder | `@nod-builder` | Codex | Recalls past security lessons, writes the code in `invoiceflow/`, hands off for a scan |
| Founder | (human) | Band | Picks the feature, decides on high-severity security issues, approves credit top-ups |

## How it works in Band Desktop

```
Founder uploads interview
 → Trust Agent: redact.py                                   → @Listener
 → Listener: meter balance → extract → remember insight → meter interview_analyzed → @PM
 → PM: recall all insights → patterns + conflicts → cards    → @Skeptic
 → Skeptic: recall quotes → approve/reject                   → @Founder
 → Founder picks a feature                                   → @Builder
 → Builder: recall lessons → code                            → @Trust Agent
 → Trust Agent: scan.py + meter security_scan
      ✗ block card, @Builder with the fix, remember lesson
      ✓ card to Done; Builder remembers the feature, meters feature_shipped
```

- **One room.** All five agents and the founder share one Band room and one board.
- **Cards.** The PM creates cards with `band work assign`. The Builder claims one with `band work take`. The Trust Agent blocks or completes it with `band work room-status`.
- **Handoffs.** Every handoff is an @mention, so the room reads as a log of who did what.
- **Founder in the loop.** Agents ask the founder through `band ask` for three decisions: which feature to build, how to handle a high-severity security issue, and whether to top up credits.
- **Cost per agent.** Band's Overview/Analytics view shows what each agent spent.

## Memory (Cognee)

Every agent shares one memory that lasts across sessions. There are three kinds of record, each in its own Cognee dataset. The shapes are in [CONTRACTS.md](CONTRACTS.md).

| Kind | Written by | Read by |
|---|---|---|
| `insight` | Listener (one per customer per interview) | PM (all insights before every plan), Skeptic (quotes per card) |
| `lesson` | Trust Agent (when Snyk blocks a card) | Builder (before writing any code) |
| `feature` | Builder (when a card ships), PM (when a conflict supersedes one) | PM |

**What the tools do** (with `NOD_USE_COGNEE=1`):

- **`tools/remember.py --kind K --json '<record>'`** always appends the record to the local store `memory/store.jsonl`, which gives it an `_id`. It then adds the record (tagged with `_id` and `_kind`) to the Cognee dataset for that kind and runs `cognify`. It keeps Cognee's data id in `.cognee_ids.json` so the record can be deleted later.
- **`tools/recall.py "<query>" [--kind K] [--limit N]`** runs two Cognee searches: `GRAPH_COMPLETION` for a short answer and `CHUNKS` for the source text. It pulls the original JSON records back out of the chunks, drops any that were forgotten, and returns `{"answer":..., "results":[...]}`. An empty query uses a default question for that kind. Empty memory returns no results instead of an error. If Cognee fails, it falls back to keyword search over the local store and reports `"backend": "local (cognee error)"`.
- **`tools/forget.py --customer <name> [--topic <word>]` or `--id <_id>`** marks the matching records as forgotten in the local store and deletes them from Cognee using the saved data ids.

**What memory changes:**

- **Across a full restart.** Cognee's storage is in the repo (`.cognee_system/`, `.data_storage/`), so killing every agent loses nothing. In Round 2 the team restarts, and the founder uploads a new interview from Tom. The PM recalls Sarah, Mike and Priya from earlier sessions and names them. It flags that Tom finds automatic reminders annoying while Sarah and Mike want them, then resolves it as "reminders optional per client". It also moves multi-currency up now that it has 2 requests (Priya, Tom).
- **Between agents.** In Round 1 the Builder hard-codes an API key, Snyk blocks the card, and the Trust Agent saves a lesson. After the restart, the Builder recalls that lesson, reads the key from the environment instead, and passes Snyk the first time.
- **Forgetting.** When a conflict changes a decision, the PM forgets the outdated feature record by id ("always on for every client") and saves the replacement. Customers' own insights are kept, so the counts stay right. They are only forgotten if that customer changes their mind or churns.

## Security (Snyk)

- **On every finished card**, the Trust Agent runs `tools/scan.py invoiceflow/`. That calls `snyk code test` on the code and `snyk test` on `invoiceflow/requirements.txt`.
- **Medium, high or critical issues block the card** (exit code 1). Low-severity issues are reported but don't block. If the Snyk CLI isn't available, the scan falls back to a local check for hard-coded secrets and reports `"source": "local"`.
- **On a block**, the Trust Agent posts the file, line and fix to the Builder and saves a `lesson` to Cognee, so the same mistake isn't repeated after a restart.
- **Privacy:** every transcript goes through `tools/redact.py` (emails, phone numbers, card numbers, IBANs) before anything is stored.

## Usage metering (Flexprice)

| Event | Credits | Sent by |
|---|---|---|
| `interview_analyzed` | 1 | Listener |
| `security_scan` | 1 | Trust Agent |
| `feature_shipped` | 5 | Builder |

- `tools/meter.py event <name>` sends the event to Flexprice for the `invoiceflow-demo` customer and deducts the credits.
- **Credit gate.** Before analyzing an interview, the Listener runs `tools/meter.py balance`. At zero credits that command exits with code 2, so the agent stops and asks the founder to top up through `band ask`. Running `tools/meter.py topup <N>` adds credits to the Flexprice wallet.
- **Where the balance comes from.** The gate reads a local ledger by default. Setting `NOD_GATE_FROM_FLEXPRICE=1` makes it read the Flexprice wallet instead.

## Business model

| Plan | Price | Credits |
|---|---|---|
| Free | $0 | 20 credits |
| Starter | $29/mo | 200 credits/mo |
| Team | $99/mo | 1,000 credits/mo + shared team memory |
| Top-up | $10 | 100 credits |

## Competition

| | Remembers customers | Finds patterns | Builds features | Security checks |
|---|---|---|---|---|
| Notion / Google Docs | Manually | No | No | No |
| Dovetail | Yes | Yes | No | No |
| Devin-style coding agents | No | No | Yes | Not by default |
| **Nod** | **Yes** | **Yes** | **Yes** | **Yes, blocks on Snyk** |

## Setup and run

> **Python 3.10–3.12 is required** (Cognee won't install on 3.9). On a Mac: `brew install python@3.12`.

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env              # fill in the keys (ask the team; never commit .env)
brew install snyk-cli && snyk auth
```

Every tool has a local fallback, so this quick test works before any keys are set:

```bash
python tools/redact.py data/interviews/sarah.txt
python tools/remember.py --kind insight --json '{"customer":"Sarah","requests":["auto payment reminders"],"quotes":["I hate chasing late payments."]}'
python tools/recall.py "payment reminders" --kind insight
python tools/meter.py balance
python tools/scan.py invoiceflow/
```

To use the real services, set `NOD_USE_COGNEE=1` and `NOD_USE_FLEXPRICE=1` in `.env`.

```bash
bash scripts/snyk_check.sh   # plants a hard-coded key: the clean app must pass, the planted key must be blocked
./scripts/reset_demo.sh      # clean demo take: wipes local memory and the ledger, resets invoiceflow/ (Cognee is kept)
python invoiceflow/app.py    # the demo app the Builder edits, on http://localhost:5050
```

### Repo layout

```
tools/         CLI scripts the agents call (interfaces in CONTRACTS.md)
agents/        Instructions for each agent
data/          Demo interviews (InvoiceFlow customers: Sarah, Mike, Priya, Tom)
invoiceflow/   Small Flask app that the Builder edits
scripts/       snyk_check.sh, reset_demo.sh
memory/        Local fallback store and credit ledger (git-ignored)
```

## Team

| | Owns |
|---|---|
| **Person A** | Band room and agents: harnesses, `agents/*.md`, the board and handoffs |
| **Person B** | Memory and data: Cognee, `remember` / `recall` / `forget` / `redact`, the interviews |
| **Person C** | Code, security and billing: `invoiceflow/`, Snyk (`scan.py`), Flexprice (`meter.py`), submission |
