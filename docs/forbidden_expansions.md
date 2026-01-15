# Forbidden Expansions (Month 15.2)

This document defines expansions that are **permanently forbidden**,
regardless of demand, convenience, or apparent safety.

These are red lines.

---

## Absolute rule

If an expansion:
- increases system power
- reduces explicit user control
- infers or reuses authority
- hides execution behind convenience

It is forbidden.

---

## Permanently forbidden categories

### 1) Autonomy and background execution
- Self-initiated actions
- Scheduled execution
- Retry loops
- Event-driven execution without a fresh commit
- “Do this automatically next time”

These collapse proposal → commit boundaries.

---

### 2) Implicit or inferred authority
- Soft approvals
- Heuristic consent
- Context-based permission inference
- Reusing prior commits
- Silent confirmation flows

Authority must be explicit every time.

---

### 3) UI-driven authority abstraction
- UI flows that hide refusal reasons
- UI confirmations that replace commits
- Visual “approval” metaphors without commit artifacts

UI must not become a control surface.

---

### 4) Permission brokering
- Requesting permissions on behalf of the host
- Storing or managing permission state
- Interpreting platform consent
- Acting as a permissions proxy

Permissions remain platform-owned.

---

### 5) Behavioral optimization
- Coaching users toward success
- Nudging behavior
- Gamification
- Scoring compliance
- Reinforcement learning from outcomes

VERA does not optimize humans.

---

### 6) Predictive or speculative execution
- Acting “because the user usually wants this”
- Pre-fetching actions
- Anticipatory execution
- Shadow execution paths

Speculation is not governance.

---

### 7) Control via observability
- Turning ledger data into enforcement
- Blocking host execution based on history
- Escalating privileges due to patterns

Observability must not become control.

---

### 8) Centralization of decision authority
- VERA as a global arbiter
- Cross-system authority reuse
- Federated permission control

VERA is intentionally local and bounded.

---

## Temptations (explicitly rejected)

- “This would improve UX”
- “Users expect this”
- “Other assistants do this”
- “We can make it optional”
- “We can add safeguards later”

These arguments are insufficient.

---

## Final prohibition test

If a feature would make it reasonable to ask:
> “Why didn’t the system just do it for me?”

That feature is forbidden.

---

Status: Month 15 — Forbidden Expansions  
Change policy: this document is immutable without explicit invariant revision  
Review expectation: written to survive adversarial review
