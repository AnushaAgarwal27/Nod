# Contracts

These are the interfaces between people. **Don't change a command or output shape without telling the team.**
Every tool prints JSON to stdout and runs from the repo root.

## Tools

| Command | Owner | Output | Exit code |
|---|---|---|---|
| `python tools/redact.py <file>` | B | redacted text on stdout, `{"redacted":{...counts}}` on stderr | 0 |
| `python tools/remember.py --kind insight\|lesson\|feature --json '<obj>'` | B | `{"ok":true,"kind":...,"id":...}` | 0 |
| `python tools/recall.py "<query>" [--kind K] [--limit N]` | B | `{"results":[<record>...]}` | 0 |
| `python tools/forget.py --customer <name> [--topic <word>]` | B | `{"ok":true,"forgotten":N}` | 0 |
| `python tools/scan.py <path>` | C | `{"pass":bool,"issues":[Issue...],"source":"snyk"\|"local"}` | 0 = pass, 1 = issues |
| `python tools/meter.py event <name>` | C | `{"ok":true,"event":...,"credits":N}` | 0, or 2 if no credits |
| `python tools/meter.py balance` | C | `{"credits":N}` | 0, or 2 if zero |
| `python tools/meter.py topup <N>` | C | `{"ok":true,"credits":N}` | 0 |

Events and their cost: `interview_analyzed` = 1, `security_scan` = 1, `feature_shipped` = 5.

## Record shapes

**insight** (written by the Listener)
```json
{"customer":"Sarah","role":"designer",
 "pains":["chasing late payments"],
 "requests":["auto payment reminders"],
 "quotes":["I hate chasing late payments. I wish it reminded clients for me."],
 "sentiment":{"auto_reminders":"+"},
 "date":"2026-10-20"}
```
`sentiment` maps a feature slug to `+` (wants it) or `-` (against it). The PM uses it to spot conflicts.

**lesson** (written by the Trust Agent)
```json
{"rule":"hardcoded-secret","file":"invoiceflow/reminders.py",
 "lesson":"Never hard-code API keys. Read them from os.environ and document them in .env.example.",
 "seen":1}
```

**feature** (written by the Builder)
```json
{"name":"Payment reminders","card":"NOD-1","customers":["Sarah","Mike"],
 "files":["invoiceflow/reminders.py"],"notes":"Optional per client (Tom)"}
```

**Issue** (output of scan.py)
```json
{"severity":"high","title":"Hardcoded secret","file":"invoiceflow/reminders.py","line":7,"fix":"Load from env"}
```

## Feature slugs (everyone uses these exact strings)

`auto_reminders`, `multi_currency`
