# VERA Core Surface v1 (LOCKED)

Definition:
VERA Core is the invariant governance substrate. It MUST NOT change based on user or domain.
Hats are domain layers. Coats are explanation-only layers. Core enforces:
- deterministic routing boundaries (proposal vs commit)
- fail-closed behavior
- ledger/receipt shapes
- reason prefix contracts + allowlists
- offline verification (Device-B)

LOCKED CORE SURFACES (paths must exist):
- v2/contract.py
- v2/accountability.py
- v2/hats/hat_interface.py
- v2/hats/router_v1.py
- v2/hats/registry.py
- v2/hats/reason_allowlists_v1.py
- v2/coat/coat_v1.py
- v2/coat/templates_v1.py
- v2/device_b/MANIFEST.json
- v2/device_b/generate_manifest.py
- v2/device_b/verify_all.py
- v2/docs/public/COMMERCIAL_BUNDLE_V1.md
