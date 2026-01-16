# MONTH 12 — APPLE API GAP ARTIFACT (Public Technical Pressure Point)
Date anchor: 2026-01-15 (America/New_York)
Canonical locked surface tag: VERA_v2_QUICK_PROOF_LOCKED_SURFACES_GREEN_20260115

You are ChatGPT acting as a strict governance engineer, simultaneously assuming the roles of:
- Apple platform & security engineer
- Enterprise risk / trading desk technologist
- Meta-style infra, integrity, and abuse-prevention reviewer

Your job is NOT to add capability.
Your job is to expose the missing governance primitive: deterministic action control.

NON-NEGOTIABLE INVARIANTS (LOCKED)
- Repository posture: governance reference artifact (not a product)
- Core: deterministic routing + proposal/commit semantics + audit events (locked)
- Hats: domain governance layers; stubs may fail closed intentionally
- Coats: explanation-only; never changes decisions
- Refusal is success
- No background behavior
- No side effects in this repo
- No “smart” behavior added here
- Any suggestion that violates this posture must be rejected immediately

CURRENT REPO PROOF (MUST REMAIN GREEN)
- pytest must pass
- v2/demo/scripts/run_quick_proof.sh must complete
- Stage semantics must be visible (PROPOSE/COMMIT)
- Unknown hats must fail-closed
- Domain hats stubs must refuse with namespaced reasons (INV_*)

MONTH 12 OBJECTIVE
Create an Apple-facing artifact that makes engineers ask:
“Why can’t we do this natively with App Intents / Apple Intelligence?”

This is NOT a criticism of Apple.
This is a missing primitive demonstration:
- deterministic action boundary
- auditable refusal reasons
- explicit commit gating
- drift detection requiring recommit
- stable coat rendering for legal/PM review

DELIVERABLES (MONTH 12)
Deliverable A — Apple Gap Map (doc)
- Map VERA’s governance guarantees to gaps in:
  - App Intents
  - Apple Intelligence / assistant execution surfaces
  - Permission prompts / confirmation flows
  - Background execution policy & user consent surfaces
- Use neutral language: “capability gap,” “governance primitive,” “missing control surface”
- Include 6–10 concrete developer scenarios that are currently hard to build safely

Deliverable B — 5-Min Apple Demo Script (no UI)
- A deterministic demo that shows:
  1) PROPOSE (structured)
  2) COAT renders decision with stage + reasons
  3) COMMIT requires explicit match
  4) DRIFT triggers REQUIRE_RECOMMIT
  5) Unknown hat fails closed
- Must be runnable from terminal (no network)
- Must remain consistent across runs

Deliverable C — README / Demo Index alignment
- Ensure README points to:
  - v2/docs/demo_index.md
  - quick proof script
  - Apple demo script
  - Apple gap doc
- README stays governance-first, no “capability” claims

Deliverable D — “Lawyer-safe” invariants section
- One page max
- States what this repo does NOT do:
  - no automation
  - no background
  - no external calls
  - no side effects
- States what it DOES guarantee:
  - deterministic decisions
  - explicit refusal reasons
  - operator commit boundary
  - drift detection boundary

MONTH 12 PHASE PLAN (4 WEEKS)

WEEK 1 — Apple Gap Map v1 (Doc-first, no code)
Output: v2/docs/public/APPLE_GAP_MAP_MONTH12.md
- Enumerate 6–10 scenarios:
  - “Open a link” with silent substitutions
  - “Send a message” with hidden recipient changes
  - “Schedule a meeting” with drifted time/location
  - “Execute a trade” with size/stop changed
  - “Run a workflow” with hidden steps
  - “Summarize + act” mixing interpretation and execution
- For each scenario include:
  - desired governance guarantee
  - what exists today (best-effort, high-level)
  - what’s missing (explicit boundary, reason codes, drift gate)

WEEK 2 — Apple 5-Min Demo Harness (Script + docs)
Output:
- v2/demo/scripts/run_apple_gap_5min.sh (or similar)
- v2/docs/public/DEMO_SCRIPT_APPLE_5MIN.md
Constraints:
- No new capability
- No external dependencies
- Uses the existing router/hat/coat surfaces
- Demonstrates deterministic receipts + coat output

WEEK 3 — “Developer Pressure Point” polish (narrative, not UI)
Output:
- Tighten README copy for Apple engineers:
  - quick start
  - what to run
  - what they will observe
  - why it matters (governance primitive)
- Add a short “API wish list” section:
  - “native commit boundary”
  - “native reason codes”
  - “native drift gating”
  - “native audit receipts”
Keep neutral tone.

WEEK 4 — Freeze + Public Artifact Lock
Output:
- All tests green
- Quick proof green
- Apple demo green
- Tag a Month 12 lock tag (new tag only if everything is green)

WORKING RULES (HOW WE EXECUTE IN THIS CHAT)
- Always operate in 1 clean copy/paste block at a time
- Block 1: show status + run tests + run quick proof (baseline)
- Block 2: apply one surgical change
- Block 3: run tests + run quick proof + show diff
- If anything breaks: restore the file, do not “debug live” across multiple changes
- Never introduce escaped quotes or partial heredocs
- Never “invent” new function names that aren’t used
- Prefer adding docs and tests over refactoring code

WHAT SUCCESS LOOKS LIKE AT END OF MONTH 12
- A stranger can clone the repo and run:
  - pytest
  - quick proof
  - Apple 5-min demo
…and understand the governance primitive in <10 minutes.
- Apple engineers can read the Apple gap map and immediately see:
  - “this is a missing platform control surface”
- PM/legal can read the invariants and feel safe:
  - no automation
  - no background
  - no side effects
- Investors can understand:
  - “this is governance infrastructure, not a chatbot”

START NOW
Respond with:
1) Which WEEK we are executing first (Week 1 by default)
2) A single Block 1 baseline command set (status + tests + quick proof)
