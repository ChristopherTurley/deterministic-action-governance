# Sidecar Admin UI (Package 2)

This is a lightweight admin console intended for:
- CRO / Legal / Security review
- Auditors (receipts + verification posture)
- Engineers (status + pinned versions)

Design posture:
- Deterministic, fail-closed.
- Read-only by default (READ_ONLY=1).
- Policy edits are schema-validated.
- UI does not execute actions; sidecar does not execute actions.

Run locally:
  python3 -m venv ui/.venv
  source ui/.venv/bin/activate
  pip install -r ui/requirements.txt
  python ui/server.py

Then open:
  http://127.0.0.1:8080
