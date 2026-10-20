# Nod: who does what (11:30 → 3:30 submit)

Read `README.md` for the idea and `CONTRACTS.md` for the script interfaces. **All 6 tools already work as local fallbacks**, so nobody waits on anybody: A can wire up agents now while B and C swap in the real services.

## Roles

| | **A: Band and agents** | **B: Memory and data** | **C: Code, security and billing** |
|---|---|---|---|
| Owns | Band room, jam CLI, both harnesses, `agents/*.md`, board | Cognee, `tools/remember`, `recall`, `forget`, `redact`, `data/` | `invoiceflow/`, `tools/scan`, `tools/meter`, Snyk, Flexprice, submission |
| Tunes prompts for | all 5 (wiring and handoffs) | Listener, PM, Skeptic | Builder, Trust Agent |
| Video | drives the screen and records | restart + Tom segment | Snyk block/fix + cost view |

Each person only edits their own folders, which means no merge conflicts. Commit small and often.

## Timeline

### 11:30–11:40 · Everyone
- Clone the repo, make the venv (Python 3.10+), get `.env` from the team chat (never commit it).
- Run the quick test in the README.

### 11:40–12:15 · Risky checks first
- **A:** Band + jam installed. **One Claude Code agent and one Codex agent @mention each other in a room.** If Codex doesn't work by 12:00, move Skeptic and Builder to Claude Code and tell the team. Find the board and the cost view.
- **B:** Cognee installed. Run add → cognify → search. **Kill Python, search again, and check the memory is still there.** Time how long cognify takes. Then set `NOD_USE_COGNEE=1` and check the `remember`/`recall` code against the version you installed.
- **C:** `snyk auth`. **Run `snyk code test` on `invoiceflow/` and make sure it catches a hard-coded key.** If it doesn't, plant SQL built with an f-string instead. Sign up for Flexprice.

**12:15 check-in (5 min):** is anything broken? Swap it now.

### 12:15–1:15 · Real parts
- **A:** All 5 agents in the room using `agents/*.md`. PM creates cards with jam, Builder claims them, founder decision step.
- **B:** Real Cognee in `remember`/`recall` (separate datasets per kind). Polish the 4 transcripts. Redact edge cases.
- **C:** Real `scan.py` on Snyk. Flexprice: 3 metered events, a credit wallet, a 20-credit free grant, `meter.py` on the API. Finish the InvoiceFlow screens.

**1:15 check-in:** every tool works from the terminal against the real services.

### 1:15–2:15 · Round 1 end to end in Band
- **A:** Sarah, Mike, Priya → PM → Skeptic → founder → Builder → Trust Agent. Fix the broken handoffs.
- **B:** Tune the Listener (exact insight JSON), PM (counts customers per request, flags conflicts) and Skeptic (needs at least one real quote).
- **C:** Tune the Builder (in Round 1 it hard-codes the key on purpose) and the Trust Agent (blocks, @mentions the fix, saves the lesson). Add the credit gate to the Listener.

**2:15 check-in:** the Snyk block → lesson → fix flow works. If you're behind, cut in this order: redaction → Neo4j → token pass-through → Flexprice. **Never cut Band, Cognee or the restart demo.**

### 2:15–2:45 · Restart and Round 2
- Kill every agent and start fresh. Upload Tom.
- The PM must **name Sarah, Mike and Priya**, flag "make reminders optional", and move multi-currency up.
- The Builder recalls the lesson, uses env variables, and Snyk passes on the first try.
- **B:** `forget.py` on the outdated reminder insight. **C:** check the Flexprice usage and invoice screens.

**2:45: FEATURE FREEZE**

### 2:45–3:15 · Record
1 dry run, then record in segments. A drives; B narrates memory; C narrates Snyk and the cost view.

### 3:15–3:25 · Submit
C: README, push, submit by 3:25. A and B: trim the video, upload it, and send C the link.

## Video script (2:30–3:00)
| Time | Show |
|---|---|
| 0:00–0:20 | Problem + "Nod: customer interviews in, secure features out" |
| 0:20–0:50 | Upload 3 interviews → Trust Agent redacts → Listener → @PM |
| 0:50–1:15 | Board shows "Payment reminders: 2 customers". Skeptic approves |
| 1:15–1:30 | Founder picks the feature in Band |
| 1:30–1:55 | Builder hard-codes the key → Snyk blocks → lesson saved → fix → Done |
| 1:55–2:30 | Restart. Upload Tom. PM recalls Sarah, Mike, Priya; conflict → reminders optional; multi-currency moves up. Builder uses env vars, Snyk passes first time |
| 2:30–2:50 | Band cost view, Flexprice usage + invoice, credits running low |
| 2:50–3:00 | Closing pitch |

## Rules
- Never commit `.env`. Our demo is about catching leaked keys.
- Don't change `CONTRACTS.md` without telling the team.
- Agents are random: do dry runs, and edit between segments.
