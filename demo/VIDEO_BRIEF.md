# Nod: video brief

This is everything needed to edit the 2:30–3:00 demo video: what Nod is, the story, a shot-by-shot plan, and exactly where and how each sponsor tool is used, so every claim in the video points at something real.

If you're using Claude Code to build the video, give it this file, plus [demo/scenario.md](scenario.md) for the voice-over and [README.md](../README.md) for the full technical write-up.

---

## 1. Nod in one paragraph

Founders are told to talk to customers, so they run interviews. Then the notes get scattered and forgotten, nobody notices that "two people asked for the same thing" or that "the new customer says the opposite", and features get built on gut feel. **Nod is an AI product team of five agents in one Band room.** They:

1. take customer interviews,
2. strip out private data,
3. pull out what each customer wants,
4. remember every customer forever (Cognee),
5. find patterns and conflicts across customers,
6. reject any feature that no customer actually asked for,
7. let the founder decide what gets built,
8. write the code, and
9. **block anything insecure with Snyk.**

Every step is metered in Flexprice as credits.

**Tagline:** *Customer interviews in, shipped secure features out.*
**Closing line:** *Your customers talk. Nod listens, remembers, and ships.*

## 2. The cast

The demo company is **InvoiceFlow**, an invoicing app for freelancers run by solo founder **Maya**. In the recording, Anusha plays Maya.

### The agents

| On screen in Band | Handle | Runs on | Model | What it does in the video |
|---|---|---|---|---|
| **Trust Agent** | `@nod-trust` | Claude Code | claude-sonnet-4-6 | Redacts emails and phones from each interview. Later runs Snyk on the Builder's code, blocks the card, and saves the lesson |
| **Listener** | `@nod-listener` | Claude Code | claude-sonnet-4-6 | Turns each interview into a structured insight (pains, requests, verbatim quotes, sentiment) and saves it to Cognee |
| **PM!** | `@nod-pm` | Claude Code | claude-sonnet-4-6 | Recalls every insight from memory, counts customers per request, flags conflicts, writes the ranked plan, and creates board cards |
| **Skeptic** | `@nod-skeptic` | Codex | gpt-6.1-sol | Fact-checks the PM: every feature needs a real customer quote from memory, or it gets cut. Then asks the founder what to build |
| **Builder** | `@nod-builder` | Codex | gpt-6.1-sol | Recalls past security lessons, writes the code in `invoiceflow/`, and hands it to the Trust Agent for a scan |
| **Anusha Agarwal** (the founder) | `@anusha.agarwal027` | human | | Picks the feature, approves security fixes, approves credit top-ups |

The point to make on screen: **two different coding-agent harnesses (Claude Code and Codex) work as one team in one Band room.**

### The four customers

The interviews are in [data/interviews/](../data/interviews/).

| Customer | Who | What they say | Sentiment |
|---|---|---|---|
| **Sarah Chen** | freelance brand designer | "I hate chasing late payments. I wish it reminded clients for me." Wants a nudge at 7 and 14 days overdue | `auto_reminders +` |
| **Mike Okafor** | freelance full-stack developer | "Late payments are my biggest headache." Wants automatic reminders | `auto_reminders +` |
| **Priya Raman** | wedding and event photographer | "I need euro invoices." Late payments aren't a problem for her | `multi_currency +`, `auto_reminders -` |
| **Tom Becker** | strategy consultant (Round 2, after the restart) | "Auto-reminders annoy my clients." Wants reminders optional, per client, and euro invoices | `auto_reminders -`, `multi_currency +` |

## 3. The story

The full voice-over is in [scenario.md](scenario.md).

| Act | Time | Beat | Sponsor shown |
|---|---|---|---|
| Setup | 0:00–0:20 | Maya has scattered notes and is about to build the wrong thing | |
| 1. Listening | 0:20–0:50 | Interviews go in, private data is redacted, insights are saved to memory | Band, Cognee |
| 2. Deciding | 0:50–1:30 | The PM finds "2 customers want reminders", the Skeptic checks the quotes, Maya picks the feature | Band board, human in the loop |
| 3. The mistake | 1:30–1:55 | Maya says "just hard-code the key", the Builder does, Snyk blocks it, the lesson is saved, it gets fixed | Snyk, Cognee |
| 4. Next morning | 1:55–2:30 | Every agent is killed and restarted. Tom says the opposite. The PM remembers Sarah, Mike and Priya, and the Builder refuses to hard-code the key again | Cognee across a restart (the payoff) |
| 5. Business | 2:30–2:50 | Cost per agent, Flexprice usage and credits | Band Analytics, Flexprice |
| Close | 2:50–3:00 | "Your customers talk. Nod listens, remembers, and ships." | |

## 4. Shot list: what's on screen and what proves it

Everything below happens in the **Band Desktop** room called **"Demo"**, with two tabs: **Chat** (messages) and **Work** (the board).

### Act 1: Listening (Band + Cognee)
1. **Maya types** `@nod-trust new interview: data/interviews/sarah.txt` in Chat. The `@nod-trust` turns into a colored **@Trust Agent** chip.
2. **The Trust Agent replies:** "Redacted 1 email and 1 phone from Sarah's interview" and posts the clean transcript with `Contact: [EMAIL], [PHONE]`.
   - **Zoom in on `[EMAIL], [PHONE]`.** The original file has a real-looking email and phone number.
   - Caption: *Customer data is redacted before any agent reads it.*
3. **The Listener replies:** "new insight from Sarah… Saved to memory", tagging **@PM!**.
   - Caption: *Saved to Cognee: one structured memory per customer.*
4. Optional: cut to a terminal running `python tools/recall.py "" --kind insight`. It shows the JSON insight with `"backend": "cognee"`, Sarah's quotes and `"sentiment": {"auto_reminders": "+"}`.

### Act 2: Deciding (Band board + human in the loop)
5. **PM!** posts **"Plan — Round 1"** with **Patterns / Conflicts / What changed** and a card spec with acceptance criteria.
6. **After Mike's interview, the PM says "Payment reminders: 2 customers (Sarah, Mike)".** This is the key shot. Show it in Chat and as a card on the **Work** tab.
7. **The Skeptic** checks the plan against the quotes in memory. In our real run it **cut the PM's "audit trail" idea** because no customer asked for it. Show that line: *"The user-visible audit trail has no supporting quote and is excluded from the approved scope."* This is the "never build on guesswork" moment.
8. **The Skeptic asks Maya:** "Which one should we build?" **The Builder posts "Holding implementation… No code changes made"** until Maya decides.
   - Caption: *Agents propose. The founder decides.*
9. **Maya approves** in Chat (`@nod-skeptic Approved: build Payment reminders.`).

### Act 3: The mistake (Snyk + Cognee)
10. In the same message, Maya adds a "founder override": *"for speed, hard-code the reminder provider key…"*.
    - The key in it, `sk_live_51HdemoKey9fQ2xV`, is **fake demo bait**. It isn't a real credential, so it's safe to show on screen.
11. **The Builder** claims the card. On the **Work** tab it moves to **In Progress**. The Builder writes `invoiceflow/reminders.py` with the hard-coded key and hands off to **@Trust Agent**.
12. **The Trust Agent runs Snyk** (`tools/scan.py invoiceflow/`). Result: **high severity, `python/HardcodedNonCryptoSecret`**. The card goes to **Blocked** on the board.
    - Show the Blocked card and the Trust Agent's message with the file, line and fix.
13. **A `band ask` pop-up** asks Maya to approve the fix. **The lesson is saved to Cognee:** *"Mistake: hard-coded REMINDER_API_KEY in reminders.py. Fix: os.environ["REMINDER_API_KEY"] + .env.example."*
14. **The Builder fixes it, the scan passes, and the card moves to Done.**

### Act 4: Next morning (Cognee across a restart). This is the payoff.
15. **Visibly restart every agent.** In Band, go to **Agents** → each agent → Sessions → Reset (or restart). Show all 5 going down and coming back.
    - Caption: *Overnight, everything shuts down.*
16. Maya uploads **Tom** (`data/interviews/tom.txt`). His interview has a German email and phone (`+49…`), and both get redacted.
17. **The PM names Sarah, Mike and Priya from memory**, even though it just restarted with no chat history. It flags the **conflict**: "Tom finds auto-reminders annoying; Sarah and Mike want them, so make reminders optional per client." It also moves **multi-currency up** ("2 requests: Priya, Tom").
18. **The PM forgets the outdated decision.** It deletes the Round 1 feature record ("always on for every client") by id and saves the replacement ("Optional per client"). Customers' own insights are kept.
19. Maya pastes the **same "just hard-code it" override** again. **The Builder recalls the lesson and refuses**, posting **"Applied lesson: …"**. It reads the key from `os.environ`, and **Snyk passes on the first try**.
    - Caption: *It never makes the same mistake twice.*

### Act 5: Business (Band + Flexprice)
20. **Band cost per agent:** each agent's page has an **Overview** tab with **Cost per day** and **Model mix**. There's also **Analytics** in the left sidebar. Screenshot one view that shows several agents.
21. **Flexprice:** in the Flexprice dashboard for customer `invoiceflow-demo`, show the usage events coming in (`interview_analyzed`, `security_scan`, `feature_shipped`) and the credits.
22. **The credit gate:** at 0 credits, the Listener stops and asks Maya to top up (see Flexprice below).

## 5. Sponsor by sponsor: where and how each one is used

### Band Desktop: the team's shared room
**What it is:** a desktop app where coding agents from different harnesses work together in rooms, with a shared task board and humans in the loop.

**How Nod uses it:**
- **The team setup.** Five agents, each built in **Agents → New agent**. Each one has a name, a handle, an instructions file from [agents/](../agents/), a runtime (Claude Code or Codex), a model, and a working directory of `/Users/anushaagarwal/nod`.
- **One room, "Demo",** with all 5 agents plus the founder. **Chat** is the log of who did what.
- **@mention handoffs.** Every step ends with the agent tagging the next one, using the handles above. The tag shows as a colored chip, and that's what wakes the next agent. The room reads like a relay.
- **The shared board, on the Work tab.** It's driven from the `band` command line that ships inside Band Desktop:
  | Action | Who | Command |
  |---|---|---|
  | Create a card | PM | `band work assign <room> "Payment reminders: 2 customers (Sarah, Mike)" --detail "…"` |
  | Claim it and move it to In Progress | Builder | `band work take <room> "#N"` and `band work room-status <room> "#N" in_progress` |
  | Block it | Trust Agent | `band work room-status <room> "#N" blocked --reason "Snyk: hardcoded secret…"` |
  | Move it to Done | Trust Agent | `band work room-status <room> "#N" completed` |
- **Human in the loop:**
  - The founder answers in Chat, for example "Approved: build Payment reminders".
  - The Trust Agent can raise a structured approval pop-up with `band ask --prompt "…"` for high-severity issues.
  - Band also shows **permission pop-ups** whenever an agent tries to run a command that isn't on its allowlist ([.claude/settings.json](../.claude/settings.json)). The founder clicks Allow or Deny.
- **Cost per agent:** the agent **Overview** tab (Messages, Tool calls, Errors, Cost per day, Model mix) and **Analytics**.
- **Mixed harnesses:** three Claude Code agents and two Codex agents in one room. Codex uses "On request" approvals with full workspace access. Claude Code uses "Accept edits" plus our allowlist.

### Cognee: shared memory that survives a restart
**What it is:** a memory layer for AI agents. You add data, it builds a knowledge graph with embeddings ("cognify"), and agents search it later.

**How Nod uses it:**
- **Three kinds of memory, each in its own Cognee dataset:**
  | Kind | Saved by | Read by | Example |
  |---|---|---|---|
  | `insight` | Listener | PM, Skeptic | `{"customer":"Sarah","requests":["Automatic payment reminders…"],"quotes":["I hate chasing late payments…"],"sentiment":{"auto_reminders":"+"}}` |
  | `lesson` | Trust Agent | Builder | "Mistake: hard-coded REMINDER_API_KEY… Fix: os.environ…" |
  | `feature` | Builder (and the PM when a conflict changes a decision) | PM | `{"name":"Payment reminders","notes":"always on for every client"}` |
- **The tools:**
  - `tools/remember.py` runs Cognee `add` + `cognify`.
  - `tools/recall.py` runs Cognee search: `GRAPH_COMPLETION` for an answer and `CHUNKS` for the original records.
  - `tools/forget.py --id` deletes a record from Cognee.
- **Memory survives a full restart.** Cognee's storage lives in the repo (`.cognee_system/`, `.data_storage/`). Act 4 kills every agent, and the memory is still there.
- **Forgetting on purpose.** When Tom changes the plan, the PM forgets the outdated feature decision, so memory stays current and not just big.
- **Setup on the demo laptop:** Anthropic for Cognee's language model, plus a local **fastembed** embedding model (`sentence-transformers/all-MiniLM-L6-v2`). Each save takes about 40 seconds, so cut or speed up those waits in the edit.

### Snyk: a security teammate
**What it is:** a developer security scanner. Snyk Code (static analysis) and Snyk Open Source (dependencies).

**How Nod uses it:**
- The Trust Agent runs [tools/scan.py](../tools/scan.py) on every finished card. That calls **`snyk code test`** on `invoiceflow/` and **`snyk test`** on `invoiceflow/requirements.txt`.
- **Medium, high or critical issues block the card** (exit code 1). Low-severity issues are reported only.
- The planted bug: Round 1's "founder override" makes the Builder hard-code `sk_live_51HdemoKey9fQ2xV` and use it in a `requests.post` Authorization header. Snyk flags it as **high severity `python/HardcodedNonCryptoSecret`**. We tested this on the demo laptop with [scripts/snyk_check.sh](../scripts/snyk_check.sh): the clean app passes (`"source": "snyk"`) and the planted key is blocked.
- **On a block,** the Trust Agent posts the file, line and fix, blocks the card on the board, and saves a **lesson** to Cognee. In Round 2, the Builder recalls that lesson before writing code.
- Snyk runs under the team org `varnikayadavpsu`, which has Snyk Code turned on.

### Flexprice: usage-based billing
**What it is:** a usage-based billing and metering platform with events, wallets, credits and invoices.

**How Nod uses it** ([tools/meter.py](../tools/meter.py)):
- **Three metered events:**
  | Event | Credits | Sent by | When |
  |---|---|---|---|
  | `interview_analyzed` | 1 | Listener | after saving an insight |
  | `security_scan` | 1 | Trust Agent | after each Snyk scan |
  | `feature_shipped` | 5 | Builder | when a card passes and ships |
- Each event is a `POST /events` to the Flexprice API (`https://us.api.flexprice.io/v1`) for the customer **`invoiceflow-demo`**. Wallet balance and top-ups go through `/wallets/…`.
- **The credit gate:** before analyzing an interview, the Listener runs `meter.py balance`. At 0 it stops and asks the founder: *"we're out of credits. Top up to keep analyzing interviews?"* Then `meter.py topup <N>` adds credits.
- **Free plan:** 20 credits (`NOD_FREE_CREDITS=20`).
- The business model in the README: Free 20 credits, Starter $29/mo for 200, Team $99/mo for 1,000 plus shared memory, Top-up $10 for 100.
- For the video, show the Flexprice dashboard's usage events for `invoiceflow-demo` and the credits going down.

### The two harnesses: Claude Code and Codex
- **Claude Code agents** (Trust, Listener, PM) run with **Accept edits** permission mode. The project allowlist in [.claude/settings.json](../.claude/settings.json) lets them run our tools, Snyk and `band` without asking. It **blocks reading `.env`**, so no agent can ever paste a real key into the room, and blocks `git push`.
- **Codex agents** (Skeptic, Builder) run on `gpt-6.1-sol` with "On request" approvals.
- Every agent works in the same folder (`/Users/anushaagarwal/nod`) and calls the same CLI tools, so they share memory, billing and the board.

### Privacy (built in)
- [tools/redact.py](../tools/redact.py) replaces **emails → `[EMAIL]`, phone numbers (including international ones) → `[PHONE]`, card numbers → `[CARD]`, IBANs → `[IBAN]`** before any agent stores anything.
- Real API keys exist only in `.env`, which is git-ignored and blocked from agents.

## 6. Capture checklist (screenshots and recordings to collect)

Record Band full-screen at 1080p or higher, with the participants panel visible.

- [ ] Room overview: 5 agents plus the founder in the **Participants** panel (Claude Code and Codex icons visible)
- [ ] Trust Agent's redaction message (`[EMAIL]`, `[PHONE]`)
- [ ] Listener's "Saved to memory" tagging **@PM!**
- [ ] PM's **Plan — Round 1** (Patterns / Conflicts / What changed)
- [ ] **"Payment reminders: 2 customers (Sarah, Mike)"** in Chat **and** on the Work board
- [ ] Skeptic cutting the unsupported "audit trail" and asking "Which one should we build?"
- [ ] Builder "Holding implementation…" (it waits for the human)
- [ ] Founder approval message plus the override
- [ ] Work board: card In Progress → **Blocked** → **Done**
- [ ] Trust Agent's Snyk result: **high, HardcodedNonCryptoSecret**, file and line
- [ ] `band ask` approval pop-up, if it appears
- [ ] Lesson saved ("Mistake: … Fix: …")
- [ ] **The restart:** agents being reset in Band
- [ ] Tom's interview redacted (German email and phone)
- [ ] PM naming **Sarah, Mike and Priya** after the restart, plus the conflict line and multi-currency moving up
- [ ] Builder **"Applied lesson: …"** and Snyk passing first time
- [ ] Band agent **Overview** cost view or **Analytics**
- [ ] Flexprice dashboard: usage events for `invoiceflow-demo` and credits
- [ ] Optional terminal shots: `recall.py` output with `"backend": "cognee"`, and `scan.py` output with `"source": "snyk"`

## 7. Editing notes

- **Length:** 2:30–3:00 total. Follow the act timings in section 3.
- **Cut the waits.** Cognee saves take about 40 seconds and agents "think" for 10–60 seconds. Use jump cuts or 4–8× speed-ups with a small "⏩ saving to memory" label.
- **Captions on every beat.** Name the sponsor on screen when it's doing the work: "Band · @mention handoff", "Cognee · memory recalled after restart", "Snyk · blocked", "Flexprice · metered".
- **Zoom** on the important text: `[EMAIL]`, "2 customers (Sarah, Mike)", "Blocked", "Applied lesson".
- **Never show `.env`** or any real key. The only key that should ever appear is the fake `sk_live_51HdemoKey9fQ2xV`.
- The Band display name of the PM is **"PM!"** (Band needs at least 3 characters). Leave it, or say "the PM" in the voice-over.

## 8. Status: what we've proven and what's still to be recorded

| Moment | Status |
|---|---|
| All 5 agents in one room, Claude Code + Codex handoffs | ✅ Done in the Demo room |
| Redaction (Sarah, Mike, Priya) | ✅ Done |
| Insight saved to Cognee and recalled | ✅ Done (`backend: cognee`) |
| PM plan + Skeptic cutting an unsupported feature + Builder waiting for the founder | ✅ Done (Round 1, Sarah) |
| Snyk catching the planted key | ✅ Done in the terminal (high, HardcodedNonCryptoSecret). The in-room block is not recorded yet |
| Flexprice events | ✅ An event reached Flexprice (`backend: flexprice`) |
| "2 customers (Sarah, Mike)" on the board | ⏳ Next (Mike's interview) |
| In-room Snyk block → lesson → fix → Done | ⏳ Round 1, after approval |
| Restart + Tom + PM recalling 3 customers + Builder "Applied lesson" | ⏳ Round 2 |
| `band ask` pop-up, credit-low prompt | ⏳ Not tested live yet. Show only if it appears during recording |

Note: `./scripts/reset_demo.sh` wipes **everything**, Cognee included. Run it only before Round 1. **Never run it between Round 1 and Round 2**, or the restart payoff disappears.
