# Nod

**Customer interviews in, shipped secure features out.**

Founders are told to talk to their users. They do 10–50 interviews, and then the insights end up in scattered notes and get forgotten. Patterns get missed ("7 people asked for this"), contradictions get missed ("the new customer says the opposite"), and features get built on gut feeling.

Nod is an AI product team of five agents that work in one Band Desktop room. They remember every customer forever (in Cognee), keep customer data private, and only ship code that passes Snyk. Each step is metered through Flexprice.

## The team

| Agent | Harness | Job | Memory (Cognee) | Other tools |
|---|---|---|---|---|
| Listener | Claude Code | Pulls pains, requests and quotes out of each interview | writes `insight` | Flexprice `interview_analyzed` |
| Trust Agent | Claude Code | Redacts private data, runs Snyk, blocks bad cards | writes `lesson` | Snyk, Flexprice `security_scan` |
| PM | Claude Code | Finds patterns and conflicts, writes the plan, creates cards | reads `insight` | Band board |
| Skeptic | Codex | Rejects any feature without a real customer quote | reads `insight` | |
| Builder | Codex | Claims cards, writes code, moves them to Done | reads `lesson`, writes `feature` | Flexprice `feature_shipped` |
| Founder | Human | Picks the feature, decides on high-severity security issues, approves top-ups | | Band |

## Flow

```
Founder uploads interview
 → Trust Agent: redact.py            → @Listener
 → Listener: meter balance → extract → remember insight → meter interview_analyzed → @PM
 → PM: recall insights → patterns + conflicts → cards on the board → @Skeptic
 → Skeptic: recall quotes → approve/reject → @Founder
 → FOUNDER picks a feature
 → Builder: recall lessons → code → @Trust Agent
 → Trust Agent: scan.py
      ✗ block card, @Builder with the fix, remember lesson
      ✓ card to Done, Builder: remember feature, meter feature_shipped
```

## Repo layout

```
tools/         CLI scripts the agents call (the interfaces are in CONTRACTS.md)
agents/        Instruction prompts for each agent
data/          Demo interviews (InvoiceFlow customers)
invoiceflow/   Small Flask app that the Builder edits
memory/        Local fallback store (git-ignored)
```

## Setup

> **Python 3.10–3.12 is required** (Cognee won't install on 3.9). On a Mac: `brew install python@3.12`.

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env              # fill in the keys (ask the team; never commit .env)
npm install -g snyk && snyk auth  # Snyk CLI
```

Quick test, which works before any keys are set because every tool has a local fallback:

```bash
python tools/redact.py data/interviews/sarah.txt
python tools/remember.py --kind insight --json '{"customer":"Sarah","requests":["auto payment reminders"],"quotes":["I hate chasing late payments."]}'
python tools/recall.py "payment reminders" --kind insight
python tools/meter.py balance
python tools/scan.py invoiceflow/
```

To use the real services, set `NOD_USE_COGNEE=1` / `NOD_USE_FLEXPRICE=1` in `.env`.

## Sponsors

- **Band Desktop:** one room, one board, @mention handoffs, a human in the loop, cost per agent
- **Cognee:** long-term memory shared between agents and kept across restarts (`add`, `cognify`, `search`, plus forget for outdated insights)
- **Snyk:** `snyk code test` + `snyk test` on every finished card, and the card stays blocked until it passes
- **Flexprice:** credits for each interview, scan and shipped feature; the agents stop at zero credits
