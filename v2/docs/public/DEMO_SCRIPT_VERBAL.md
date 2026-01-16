# VERA v2 — Verbal Demo Script (Typed + Spoken)

This script is designed to be run live while you narrate. It proves:
- deterministic governance
- proposal vs commit separation
- drift detection
- stable refusal reasons
- no autonomy

## 0) One-command (recommended)
Run:
- `v2/demo/scripts/run_all_demos.sh`

What you say:
- “This command runs the full test suite first. If anything drifts, it fails.”
- “Then it runs each demo surface. These are locked behaviors.”

## 1) Trading Hat v1 (typed harness)
You say:
- “Trading Hat does not predict. It only enforces mechanical constraints.”

You point to outputs:
- Scenario A: ALLOW / ALLOW
- Scenario B: REFUSE due to daily loss limit
- Scenario C: REQUIRE_RECOMMIT when size drifts at commit time

Why it matters:
- “Assistants fail when they silently reinterpret. Drift gates prevent that.”

## 2) Trading spoken (opt-in voice)
You say:
- “This is the same decision system, rendered into stable language.”
- “Voice is a surface. Semantics are protected by tests.”

Expected:
- ALLOW / ALLOW spoken
- DRIFT -> REQUIRE_RECOMMIT spoken

## 3) Focus Hat v1 (typed + spoken)
You say:
- “Second hat proves domain independence. Same primitives, different rules.”

Expected:
- ALLOW scenario
- REFUSE when caps exceeded
- REQUIRE_RECOMMIT when commit changes proposal

## 4) Multi-hat router (explicit selection only)
You say:
- “There is no guessing which hat applies. The selection is explicit.”
- “Unknown hats refuse, deterministically.”

Expected:
- Known hats run
- Unknown hat -> REFUSE + known_hats list

## 5) Coat v1 (stable reason -> message)
You say:
- “The coat turns reason codes into consistent human messages.”
- “It’s snapshot tested so wording can’t drift silently.”

Expected:
- “Allowed.” / “Refused.” / “Re-commit required…” with stable phrasing

## 6) Bridge v1 (opt-in CLI)
You say:
- “Bridge is an opt-in runner. It does not touch v1.”
- “It proves hats + coat can be invoked as a governed session.”

Expected:
- Coated propose/commit outputs for Trading + Focus

## The punchline
You say:
- “This is Execution Intelligence without autonomy.”
- “The governance contract is what makes it safe, audit-ready, and reproducible.”

## 7) Domain hats surface proof (fail-closed, namespaced reasons)
You say:
- “These hats exist as governance lenses, but they do not execute.”
- “They’re intentionally stubbed — refusal is the correct outcome.”
- “The point is proving the surface is routable and audit-legible.”

Run:
- `v2/demo/scripts/demo_domain_hats_fail_closed_v1.sh`

Expected:
- Each domain hat routes by name
- Decisions are REFUSE or REQUIRE_RECOMMIT
- Reasons start with the correct INV_* namespace (e.g., INV_OPS_, INV_HEALTH_)

