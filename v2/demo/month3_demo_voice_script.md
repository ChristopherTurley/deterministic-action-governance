# VERA v2 — Month 3 Demo Voice Script (Live)

Goal: prove determinism + trust with a tight, repeatable sequence.

## Setup
- Terminal A: run `python run_vera_v2.py`
- Terminal B (optional): run `./v2/demo/demo_run_month3.sh` before/after to show verification

## Demo Sequence (say these, in order)

1) Wake
- Say: “hey vera”
- Expect: VERA wakes (no extra chatter)

2) Web lookup
- Say: “search the web for pizza near me”
- Expect: VERA reads 3 results and says: “Say: open 1, open 2, or open 3.”

3) Open link follow-up (no wake required)
- Say: “open 1”
- Expect: VERA opens link 1 and says “Opening …”

4) Spotify
- Say: “play spotify”
- Expect: “Playing: spotify.”

5) Start day
- Say: “start my day”
- Expect: intake mode enabled (no surprises)

6) Time
- Say: “what time is it”
- Expect: time read

7) Priority
- Say: “what is my priority”
- Expect: “You haven’t set…” (or current priority)

8) Sleep
- Say: “go to sleep”
- Expect: asleep + ignores non-wake input

## Trust claims you can state out loud (true today)
- Web search returns results OR says “No results found” (truthful)
- “Open 1/2/3” works as a follow-up without re-wake (within follow-up window)
- If last search had zero results: OPEN is truthful (“nothing to open”)
- Demo verification produces receipts + a persisted PDS snapshot
