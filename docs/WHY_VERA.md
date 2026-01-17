# WHY VERA
The problem
Modern AI systems can propose actions, generate text, and appear capable.
But in high-stakes domains (money, identity, permissions, enterprise workflows), the real requirement is different:
We need systems that can refuse deterministically and prove it.
The failure mode is not “bad suggestions.”
The failure mode is:
silent execution
unclear accountability
un-auditable decisions
drift between what was proposed and what was committed
systems that cannot be independently verified
The missing primitive
VERA demonstrates a governance primitive:
Proposal → deterministic decision → auditable receipt → (optional) explicit operator commit
This primitive is missing from most assistant stacks.
What VERA guarantees
Determinism
The same inputs produce the same decision outputs
Runs are replayable and diffable
Fail-closed
Unknowns are refused by default
Refusal is a correct outcome
Auditability
Decisions are logged as receipt surfaces
Receipts include stable hashes
No silent execution
VERA does not perform side effects
Any side effect requires an explicit operator commit in a separate execution layer (out of scope for this repo)
Why this is the basis of a large category
High-stakes automation will not scale on “trust the model.”
It will scale on:
explicit boundaries
receipts and accountability
deterministic refusals
platform-aligned permission semantics
independent verification (Device B)
VERA is engineered as a reference artifact that auditors and platform engineers can accept.
This is how governance becomes a real product category rather than a marketing claim.
