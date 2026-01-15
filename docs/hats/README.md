# VERA Hats (Domain Governance Lenses)

Hats are **domain-specific governance lenses** that sit on top of the immutable VERA core.

A Hat may:
- declare domain proposal vocabulary (names only)
- add domain invariants (refusal-only)
- map refusal semantics into domain language (no new logic)
- produce post-hoc explanation artifacts (read-only)

A Hat may **never**:
- execute actions
- suggest actions
- automate behavior
- infer or reuse authority
- broker permissions
- optimize outcomes
- nudge users

Removal test (non-negotiable):
Removing a Hat must not change VERA core decision behavior.
