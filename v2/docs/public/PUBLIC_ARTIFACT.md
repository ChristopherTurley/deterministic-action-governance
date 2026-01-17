# PUBLIC ARTIFACT — What this repo is (and is not)
This repository is a governance-only reference artifact.
It is designed to be:
safe to clone
safe to audit
safe to demo
It is not designed to:
automate accounts
execute trades
broker permissions
run background agents
call external services as a core dependency
What evaluators should look for
Deterministic boundaries (tests)
Refusal clarity (reason tokens)
Replayable, diffable outputs (receipts/logs)
Offline verification on a second machine (Device B patterns)
Apple and platform alignment
This artifact is deliberately compatible with platform security expectations:
explicit user intent
explicit commit boundaries
no permission brokering
no hidden side effects
audit-legible surfaces
The goal is to make the missing control surface obvious:
a deterministic governance layer that sits between “model output” and “real-world action.”
