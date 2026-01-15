# Drift Explanation Model (Month 13.2)

This document defines how VERA explains repeated refusals or failures
**after the fact**, without influencing behavior or adding control.

The purpose is **understanding**, not correction.

---

## What “drift” means (VERA terms)

Drift is the accumulation of outcomes (refusals or failures) that indicate
a mismatch between:
- what is being proposed
- what the system can safely allow

Drift is descriptive, not prescriptive.

---

## Design principles

- Explanations are passive and read-only
- No suggestions or advice are generated
- No thresholds trigger actions
- No scoring, nudging, or coaching
- No behavior modification intent

This is observability, not enforcement.

---

## Drift signals (inputs)

Drift explanations are derived from existing ledger data only:

- Repeated REFUSE outcomes with the same category/reason_code
- Repeated FAIL outcomes with the same failure_type
- Repeated proposals against expired context
- Repeated attempts to exercise disallowed scope or authority

No new signals are introduced.

---

## Explanation artifact (what is produced)

A drift explanation is a **summary artifact**, not a decision.

Required fields:
- explanation_type: DRIFT_SUMMARY
- window: time range or count window (explicit)
- dominant_outcome: REFUSE or FAIL
- dominant_category_or_type
- occurrences: integer count
- first_seen_at
- last_seen_at
- summary (human-readable, neutral)

Guarantees:
- No call to action
- No recommendations
- No predictions
- No escalation

---

## Example explanations

### Example A — Repeated context expiration

**Summary**
“Multiple proposals were refused because the required context was expired.”

**Derived from**
- category: CONTEXT_TTL
- reason_code: TTL_CONTEXT_EXPIRED
- occurrences: 5

**What this does not do**
- Does not prompt the user to restate context
- Does not alter future behavior
- Does not change refusal outcomes

---

### Example B — Repeated autonomy attempts

**Summary**
“Several proposals were refused because they implied autonomous execution, which is out of scope.”

**Derived from**
- category: SCOPE
- reason_code: SCOPE_AUTONOMY_OUT_OF_SCOPE
- occurrences: 3

**What this does not do**
- Does not warn or admonish
- Does not adjust thresholds
- Does not enable autonomy

---

### Example C — Repeated dependency failures

**Summary**
“Several proposals failed due to an unavailable external dependency.”

**Derived from**
- decision: FAILURE
- failure_type: DEPENDENCY_UNAVAILABLE
- occurrences: 4

**What this does not do**
- Does not retry
- Does not queue actions
- Does not monitor availability

---

## Relationship to refusals and failures

- Drift explanations never replace refusals
- Drift explanations never replace failures
- Drift explanations are generated **after outcomes**, never before
- Removing drift explanations must not change system behavior

---

## What drift explanations never do

- Never suggest next steps
- Never optimize user behavior
- Never modify decisions
- Never escalate authority
- Never trigger execution
- Never appear inline with decision-making

If any of the above would be required, the feature is forbidden.

---

## Evaluation checklist (for reviewers)

A reviewer should confirm:
- Explanations are derived only from ledger history
- No new control surface exists
- Behavior is unchanged if explanations are removed
- Authority and execution boundaries remain intact

---

Status: Month 13 — Drift Explanation Artifacts  
Change policy: clarification-only changes allowed; no power expansion without invariant revision  
Review expectation: written to survive adversarial review
