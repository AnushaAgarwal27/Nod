# The scenario: “Maya’s Monday”

**Who:** Maya, solo founder of InvoiceFlow, an invoicing app for freelancers. She has no PM, no security person, and no time.

## Setup (0:00–0:20), spoken over the title

“Maya is a solo founder. Last week she interviewed four customers. Her notes are scattered across three apps, and she’s about to build whatever she remembers best. That’s how startups build the wrong thing. Meet Nod: an AI product team that listens to every customer, remembers them forever, and only ships secure code.”

## Act 1: Listening (0:20–0:50) · Band + Cognee

“Maya drops three interviews into her Nod room.”

**On screen:** the Trust Agent redacts Sarah’s phone and email (“customer data never leaves private”). The Listener pulls out pains and quotes and saves them to Cognee, then @mentions the PM.

## Act 2: Deciding (0:50–1:30) · Band board + human in the loop

“The PM doesn’t guess. It recalls every customer from memory: two of them, Sarah and Mike, want automatic payment reminders. The Skeptic checks every card against real quotes. Then Maya makes the one call only a founder should make.”

**On screen:** cards appear on the board, the Skeptic approves with quotes, and Maya picks “Payment reminders” in Band.

## Act 3: The mistake (1:30–1:55) · Snyk

“Maya’s in a hurry, so she tells the Builder to just hard-code the API key. It does. But Nod has a security team member. The Trust Agent runs Snyk, catches a high-severity hard-coded secret, blocks the card, and asks Maya to approve the fix. It also writes the lesson into team memory.”

**On screen:** the card goes to Blocked, the band ask pop-up appears, the Builder fixes it, the re-scan passes, and the card moves to Done.

## Act 4: The next morning (1:55–2:30) · Cognee across a restart. This is the payoff.

“Overnight, everything shuts down. Tuesday morning, a fourth customer, Tom, says the opposite: auto-reminders annoy his clients. A normal AI would start from zero. Nod remembers Sarah, Mike and Priya by name, spots the conflict, and changes the plan: reminders become optional, and euro invoices move up because Priya and Tom both asked. And when Maya rushes the Builder again (‘just hard-code it’), it refuses. It remembers yesterday’s Snyk lesson. Snyk passes first try.”

**On screen:** visibly restart all agents, upload Tom, the PM names three customers and flags the conflict, and the Builder posts “Applied lesson: …”.

## Act 5: The business (2:30–2:50) · Band cost view + Flexprice

“Every interview, scan and shipped feature is metered in Flexprice as credits. Band shows exactly what each agent costs. When credits run low, the team asks Maya before spending more.”

**On screen:** the per-agent cost view in Band, the Flexprice usage page, and the credits-running-low prompt.

## Close (2:50–3:00)

“Maya didn’t hire a PM, a researcher or a security engineer. She has a team that listens, remembers and ships safely. Nod: your customers talk, Nod listens, remembers, and ships.”

## Why this works for judges

- One human, with clear decisions: she picks the feature, approves the fix, and approves top-ups. That’s Band’s human in the loop.
- Two memory payoffs after a restart: customer conflict (PM) and security lesson (Builder). That’s Cognee’s 25%.
- A mistake gets caught and never repeated: Snyk as a teammate, which is exactly what they told you.
