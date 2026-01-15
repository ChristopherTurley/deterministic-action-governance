# Trading Hat v1 — Live Demo Checklist & Verbal Script

**Version:** v1.0  
**Status:** LOCKED  
**Bound To:** VERA_v2_TRADING_HAT_WEEK3_OPEN_SESSION_FREEZE_20260114  
**Scope:** Demo / Operator / Investor / Compliance  
**Non-Goals:** Strategy, prediction, automation

---

## 15-Question Live Checklist (Pass / Fail)

### Environment & Safety
1. Demo is paper or micro only  
2. VERA v1 behavior unchanged  
3. Trading Hat invoked explicitly  
4. No market data ingestion  
5. No autonomous execution

### Context Integrity
6. Context declared explicitly  
7. Context treated as read-only  
8. Instrument matches proposal  
9. Context TTL not exceeded

### Proposal Discipline
10. Proposal includes all required fields  
11. Proposal evaluated before commit  
12. Refusals are explicit and final

### Commit Governance
13. Commit is explicit (`COMMIT`)  
14. Any drift triggers REQUIRE_RECOMMIT  
15. All decisions logged to ledger

A valid demo must pass **15/15**.

---

## Verbal Demo Script (Exact Wording)

### Opening
> “This is VERA’s Trading Hat.  
> It does not predict markets.  
> It does not suggest trades.  
> It only enforces whether I am allowed to trade.  
> Nothing executes without my explicit commit.”

---

### Scenario 1 — Allowed Trade
Context → Proposal → Commit  
Result: **ALLOW / ALLOW**

Purpose: proves deterministic governance.

---

### Scenario 2 — Risk Refusal
Daily loss equals max daily loss.  
Result: **REFUSE**

Purpose: proves hard stops.

---

### Scenario 3 — Commit Drift
Proposal size changes at commit.  
Result: **REQUIRE_RECOMMIT**

Purpose: prevents silent rule breaking.

---

### Closing
> “VERA doesn’t help me win trades.  
> It prevents me from breaking my own rules.”

---

## Notes
- This document is authoritative for Trading Hat v1 demos.
- Any change to rules or commit semantics requires a new version.
