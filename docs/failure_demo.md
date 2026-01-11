Failure Demo
Automation Executed After Context Drift

Purpose

This document demonstrates a common failure mode in AI-assisted automation:
a previously authorized action executing under conditions that are no longer
valid.

This is an execution safety demonstration, not a feature demo.


Scenario

A user authorizes an automation:

“When my workday ends, send a summary message to my team and archive today’s
draft documents.”

At authorization time:
- The user is part of the team
- The documents belong to an active workspace
- The automation is appropriate and intended

The automation is approved.


Context Drift

Over time:
- Team membership changes
- Workspace structure evolves
- Document ownership shifts

The original context no longer exists.


Behavior Without Governance

At the scheduled time:
- The automation executes
- Messages are sent to outdated recipients
- Documents are archived incorrectly

The system reports that the automation was previously approved.

Responsibility is unclear.
Trust is degraded.


Behavior With Deterministic Governance

At trigger time:
- Authority validation occurs
- Context drift is detected
- Execution is refused

No messages are sent.
No documents are modified.

The refusal is explicit and inspectable.


Deterministic Trace

INTAKE
→ PROPOSED automation_042

COMMIT
→ authority: operator
→ context snapshot: 9f3a…
→ verification artifacts: present

TRIGGER
→ context drift detected

OUTCOME
→ REFUSED (CONTEXT_DRIFT)
→ LEDGER APPEND


Key Observation

The most dangerous failures are not incorrect actions.
They are correct actions executed under invalid assumptions.


Conclusion

Deterministic action governance prevents silent harm by enforcing explicit
authority and contextual validation at execution time.
