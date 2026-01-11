from __future__ import annotations

from typing import Any, Dict, List
import json
import hashlib
CONTRACT_VERSION = "v2_contract_v1"
SUGGESTIONS_VERSION = "suggestions_v1"
REVIEW_CONTROLS_VERSION = "review_controls_v1"
REVIEW_LEDGER_VERSION = "review_ledger_v1"
REVIEW_CONFLICTS_VERSION = "review_conflicts_v1"
COMMIT_LEDGER_VERSION = "commit_ledger_v1"
COMMIT_CONTROLS_VERSION = "commit_controls_v1"
COMMIT_REQUESTS_VERSION = "commit_requests_v1"
COMMIT_CONFLICTS_VERSION = "commit_conflicts_v1"
PROPOSED_ACTIONS_VERSION = "proposed_actions_v1"
CONTEXT_VERSION = "context_v1"

COMMIT_ACK_VERSION = "commit_ack_v1"

# Metadata-only action types (must NEVER produce receipts).
META_ONLY_ACTION_TYPES = {
    "SUGGESTION_ACCEPT",
    "SUGGESTION_REJECT",
    "SUGGESTION_DEFER",
    "SUGGESTION_REVISE",
    "PROPOSED_ACTION_COMMIT",
}

def _jsonable(obj: Any) -> Any:
    if obj is None:
        return None
    if isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, dict):
        return {k: _jsonable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_jsonable(v) for v in obj]
    to_dict = getattr(obj, "to_dict", None)
    if callable(to_dict):
        return _jsonable(to_dict())
    d = getattr(obj, "__dict__", None)
    if isinstance(d, dict):
        return _jsonable(d)
    try:
        return json.loads(json.dumps(obj, default=str))
    except Exception:
        return {"_repr": repr(obj)}


def _m9w2_suggestions_from_context(ctx):
    # M9W2: deterministic, non-binding suggestions derived ONLY from context.
    # No actions. No execution. Advisory metadata only.
    if not isinstance(ctx, dict) or not ctx:
        return []
    try:
        raw = json.dumps(ctx, sort_keys=True, default=str).encode("utf-8")
    except Exception:
        raw = repr(ctx).encode("utf-8")
    sid = hashlib.sha1(raw).hexdigest()[:12]
    return [{
        "id": f"ctx_{sid}",
        "kind": "CONTEXT_NOTE",
        "label": f"Context: {(ctx.get('active_app') or 'App')} — {(ctx.get('screen_hint') or 'No hint')}",
        "reason": "Derived from context_v1 (active_app/screen_hint). Non-binding.",
        "payload": {"context": ctx},
    }]


def _m9w4_proposed_actions_from_contract(c):
    # M9W4: proposal-only mapping
    # - Never adds execution actions to `actions`
    # - Only emits proposed actions when an explicit SUGGESTION_ACCEPT is present
    if not isinstance(c, dict):
        return []

    acts = c.get("actions")
    if not isinstance(acts, list):
        acts = []

    sid = None
    for a in acts:
        if not isinstance(a, dict):
            continue
        if str(a.get("kind") or "").upper() == "SUGGESTION_ACCEPT":
            pld = a.get("payload") if isinstance(a.get("payload"), dict) else {}
            sid = pld.get("suggestion_id")
            break

    if not isinstance(sid, str) or not sid.strip():
        return []

    ctx = c.get("context")
    if not isinstance(ctx, dict):
        ctx = {}

    app = str(ctx.get("active_app") or "").strip()
    hint = str(ctx.get("screen_hint") or "").strip()
    q = f"{hint} {app}".strip() or "context"

    pa = {
        "kind": "WEB_LOOKUP_QUERY",
        "payload": {"query": q},
        "label": f"Proposed: search the web for “{q}”",
        "reason": "Mapped from accepted suggestion + context_v1. Proposal-only (non-binding).",
    }

    # Stable id derived from sid+kind+payload (deterministic)
    try:
        pa["id"] = _m7w2_hash_id({"sid": sid, "kind": pa["kind"], "payload": pa["payload"]})
    except Exception:
        pa["id"] = _m7w2_hash_id({"sid": sid})

    return [pa]

def _m10w2_review_controls_from_contract(c: dict) -> dict:
    # Month 10 Week 2: Review UX & trust signals (contract-only).
    # Absolutely no execution. No autonomy. No commit gate implemented yet.
    sug = c.get("suggestions") or []
    sid = ""
    if isinstance(sug, list) and sug:
        s0 = sug[0] or {}
        if isinstance(s0, dict):
            sid = str(s0.get("id") or "").strip()

    verbs = [
        {"verb": "accept", "requires": "<suggestion_id>", "effect": "Emits SUGGESTION_ACCEPT only (no execution). May create proposal-only proposed_actions."},
        {"verb": "reject", "requires": "<suggestion_id>", "effect": "Emits SUGGESTION_REJECT only (no execution, no proposals)."},
        {"verb": "defer",  "requires": "<suggestion_id>", "effect": "Emits SUGGESTION_DEFER only (no execution, no proposals)."},
        {"verb": "revise", "requires": "<suggestion_id> <note>", "effect": "Emits SUGGESTION_REVISE with note only (no execution, no proposals)."},
    ]

    guardrails = [
        "Suggestions are non-binding metadata only.",
        "Proposed actions are proposal-only and never executed.",
        "No autonomy. No inference-based execution.",
        "Execution requires an explicit future COMMIT step (not implemented).",
    ]

    examples = []
    if sid:
        examples = [
            f"accept {sid}",
            f"reject {sid}",
            f"defer {sid}",
            f"revise {sid} clarify intent",
        ]
    else:
        examples = [
            "accept <suggestion_id>",
            "reject <suggestion_id>",
            "defer <suggestion_id>",
            "revise <suggestion_id> <note>",
        ]

    return {
        "title": "Review & control",
        "verbs": verbs,
        "guardrails": guardrails,
        "examples": examples,
        "commit_gate": {"implemented": False, "required_for_execution": True},
    }


def _m10w3_review_ledger_from_contract(c: dict) -> list:
    # Month 10 Week 3: operator-visible review ledger (metadata-only).
    # Derived strictly from explicit review actions. No execution. No autonomy.
    acts = c.get("actions") or []
    out = []

    for a in acts:
        if not isinstance(a, dict):
            continue
        kind = str(a.get("kind") or a.get("type") or "").upper().strip()
        if kind not in {"SUGGESTION_ACCEPT", "SUGGESTION_REJECT", "SUGGESTION_DEFER", "SUGGESTION_REVISE"}:
            continue

        payload = a.get("payload") if isinstance(a.get("payload"), dict) else {}
        sid = str(payload.get("suggestion_id") or "").strip()
        if not sid:
            continue

        entry = {"kind": kind, "suggestion_id": sid}

        # Only revise carries a note (metadata only)
        if kind == "SUGGESTION_REVISE":
            note = str(payload.get("note") or "").strip()
            if note:
                entry["note"] = note

        out.append(entry)

    return out


def _m10w4_review_conflicts_from_contract(c: dict) -> list:
    # Month 10 Week 4: conflict + redundancy guards (contract-only diagnostics).
    # Derived strictly from review_ledger (metadata-only). No execution. Deterministic.
    led = c.get("review_ledger") or []
    if not isinstance(led, list) or not led:
        return []

    conflicts = []

    # 1) Duplicate entries (same kind/sid/note)
    seen = set()
    dup_sids = set()
    for e in led:
        if not isinstance(e, dict):
            continue
        kind = str(e.get("kind") or "").strip()
        sid = str(e.get("suggestion_id") or "").strip()
        note = str(e.get("note") or "").strip() if "note" in e else ""
        key = (kind, sid, note)
        if key in seen and sid:
            dup_sids.add(sid)
        seen.add(key)

    for sid in sorted(dup_sids):
        conflicts.append({
            "type": "DUPLICATE_ENTRY",
            "suggestion_id": sid,
            "detail": "Same review entry repeated (kind/suggestion_id/note).",
        })

    # 2) Conflicting verbs on same suggestion id (more than one unique kind)
    by_sid = {}
    for e in led:
        if not isinstance(e, dict):
            continue
        sid = str(e.get("suggestion_id") or "").strip()
        kind = str(e.get("kind") or "").strip()
        if not sid or not kind:
            continue
        by_sid.setdefault(sid, set()).add(kind)

    for sid in sorted(by_sid.keys()):
        kinds = sorted(list(by_sid[sid]))
        if len(kinds) > 1:
            conflicts.append({
                "type": "CONFLICTING_VERBS",
                "suggestion_id": sid,
                "verbs": kinds,
                "detail": "Multiple different review verbs applied to the same suggestion_id.",
            })

    return conflicts



def _m11w2_commit_ack_from_contract(c: dict) -> list:
    # Month 11 Week 2: contract-only acknowledgement surface for commit gate.
    # Derived strictly from normalized actions. Deterministic. No side effects.
    acts = c.get("actions") or []
    if not isinstance(acts, list) or not acts:
        return []

    out = []
    for a in acts:
        if not isinstance(a, dict):
            continue
        if a.get("type") != "PROPOSED_ACTION_COMMIT":
            continue
        p = a.get("payload") or {}
        pid = p.get("proposal_id") if isinstance(p, dict) else None
        if not isinstance(pid, str) or not pid.strip():
            continue
        out.append({
            "proposal_id": pid,
            "ack": True,
            "source_action_type": "PROPOSED_ACTION_COMMIT",
        })
    return out


def _m11w3_commit_ledger_from_contract(c: dict) -> list:
    # Month 11 Week 3: commit ledger (contract-only state).
    # Deterministic and derived strictly from metadata surfaces.
    # No execution. No receipts. No side effects.

    # Prefer commit_requests if already computed, otherwise fall back to actions.
    reqs = c.get("commit_requests")
    if not isinstance(reqs, list):
        reqs = []

    actions = c.get("actions")
    if not isinstance(actions, list):
        actions = []

    ack = c.get("commit_ack") or {}
    if not isinstance(ack, dict):
        ack = {}

    out = []

    # 1) Commit requests (deterministic order)
    # Prefer commit_requests, else derive from actions (PROPOSED_ACTION_COMMIT).
    if reqs:
        for r in reqs:
            if not isinstance(r, dict):
                continue
            pid = r.get("proposal_id")
            if not isinstance(pid, str) or not pid.strip():
                continue
            out.append({"kind": "COMMIT_REQUEST", "proposal_id": pid})
    else:
        for a in actions:
            if not isinstance(a, dict):
                continue
            if a.get("type") != "PROPOSED_ACTION_COMMIT":
                continue
            pld = a.get("payload") if isinstance(a.get("payload"), dict) else {}
            pid = pld.get("proposal_id")
            if not isinstance(pid, str) or not pid.strip():
                continue
            out.append({"kind": "COMMIT_REQUEST", "proposal_id": pid})

    # 2) Commit ack (if present)
    pid_ack = ack.get("proposal_id")
    if isinstance(pid_ack, str) and pid_ack.strip():
        out.append({
            "kind": "COMMIT_ACK",
            "proposal_id": pid_ack,
            "status": str(ack.get("status") or "ACK"),
        })

    return out
def _m11w1_commit_controls_from_contract(c: dict) -> dict:
    # Month 11 Week 1: explicit commit gate DESIGN surface (no execution).
    # Contract-only trust signals; deterministic.
    return {
        "allowed_verbs": ["commit"],
        "format": "commit <proposal_id>",
        "guarantees": [
            "Commit emits metadata action only (PROPOSED_ACTION_COMMIT).",
            "Commit never executes anything.",
            "Commit does not change proposals; execution requires future explicit executor stage.",
        ],
    }


def _m11w1_commit_requests_from_contract(c: dict) -> list:
    # Derived strictly from explicit PROPOSED_ACTION_COMMIT actions.
    acts = c.get("actions") or []
    out = []
    for a in acts:
        if not isinstance(a, dict):
            continue
        kind = str(a.get("kind") or a.get("type") or "").upper().strip()
        if kind != "PROPOSED_ACTION_COMMIT":
            continue
        payload = a.get("payload") if isinstance(a.get("payload"), dict) else {}
        pid = str(payload.get("proposal_id") or "").strip()
        if not pid:
            continue
        out.append({"proposal_id": pid})
    return out


def _m11w1_commit_conflicts_from_contract(c: dict) -> list:
    # Contract-only diagnostics (no execution).
    # Flag commit requests that reference unknown proposal ids (based on proposed_actions surface).
    reqs = c.get("commit_requests") or []
    pas = c.get("proposed_actions") or []

    known = set()
    if isinstance(pas, list):
        for pa in pas:
            if isinstance(pa, dict):
                pid = str(pa.get("id") or "").strip()
                if pid:
                    known.add(pid)

    conflicts = []
    if isinstance(reqs, list):
        for r in reqs:
            if not isinstance(r, dict):
                continue
            pid = str(r.get("proposal_id") or "").strip()
            if pid and pid not in known:
                conflicts.append({
                    "type": "UNKNOWN_PROPOSAL_ID",
                    "proposal_id": pid,
                    "detail": "Commit requested for proposal_id not present in proposed_actions (proposal-only surface).",
                })

    # Deterministic ordering
    conflicts.sort(key=lambda x: (str(x.get("type") or ""), str(x.get("proposal_id") or "")))
    return conflicts

def _normalize_context_v1(ctx: Any) -> Dict[str, Any]:
    if not isinstance(ctx, dict):
        return {}
    allowed = ("active_app", "local_date", "local_time", "screen_hint")
    out: Dict[str, Any] = {}
    for k in allowed:
        v = ctx.get(k, None)
        if v is None:
            continue
        out[k] = str(v)
    return out

def _extract_context_any(engine_out: Any) -> Dict[str, Any]:
    ctx = _get_attr(engine_out, ["context"], None)
    if isinstance(ctx, dict):
        return _normalize_context_v1(ctx)
    dbg = _get_attr(engine_out, ["debug"], None)
    if isinstance(dbg, dict):
        return _normalize_context_v1(dbg.get("context"))
    return {}
def _get_attr(obj: Any, keys: List[str], default=None):
    for k in keys:
        v = getattr(obj, k, None)
        if v is not None:
            return v
    return default

def to_contract_output(engine_out: Any, *, awake_fallback: bool) -> Dict[str, Any]:
    route_kind = _get_attr(engine_out, ["route_kind", "kind", "route", "route_name"], "") if engine_out is not None else ""
    route_kind = (route_kind or "").strip()

    awake = _get_attr(engine_out, ["awake"], None)
    if not isinstance(awake, bool):
        awake = bool(awake_fallback)

    receipts = _get_attr(engine_out, ["receipts", "receipt_list", "actions", "action_list", "planned_actions"], None)

    # M9W3_SURFACE_ACTIONS: keep actions separate from receipts (contract surface)
    actions = _get_attr(engine_out, ["actions", "action_list", "planned_actions"], None)
    if not isinstance(actions, list):
        actions = []

    if not isinstance(receipts, list):
        one = _get_attr(engine_out, ["receipt", "action"], None)
        receipts = [one] if one is not None else []

    return {
        "version": CONTRACT_VERSION,
        "awake": awake,
        "route_kind": route_kind,
        "receipts": [_jsonable(r) for r in receipts],
        "actions": [_jsonable(a) for a in actions],
        "context_version": CONTEXT_VERSION,
        "context": _extract_context_any(engine_out),
    }

def apply_contract(engine_out: Any, *, awake_fallback: bool) -> Any:
    c = to_contract_output(engine_out, awake_fallback=awake_fallback)

    rk = (c.get("route_kind") or "").strip().upper()
    if rk == "WAKE":
        c["awake"] = True
    elif rk == "SLEEP":
        c["awake"] = False

    if isinstance(engine_out, dict):
        engine_out.update(c)
        engine_out["contract"] = c
        return engine_out

    for k, v in c.items():
        try:
            setattr(engine_out, k, v)
        except Exception:
            pass

    try:
        setattr(engine_out, "contract", c)
    except Exception:
        pass

    return engine_out

# === MONTH6W3_CANONICAL_CONTRACT ===

def _m6w3_normalize_receipt(r):
    if r is None:
        return {"type": "UNKNOWN", "payload": {}}
    if isinstance(r, dict):
        t = r.get("type") or r.get("kind") or r.get("route_kind") or "UNKNOWN"
        t = str(t).strip() or "UNKNOWN"
        payload = r.get("payload")
        if not isinstance(payload, dict):
            payload = r.get("data") if isinstance(r.get("data"), dict) else {}
        return {"type": t, "payload": payload}
    t = getattr(r, "type", None) or getattr(r, "kind", None) or getattr(r, "route_kind", None) or "UNKNOWN"
    t = str(t).strip() or "UNKNOWN"
    payload = getattr(r, "payload", None)
    if not isinstance(payload, dict):
        payload = {}
    return {"type": t, "payload": payload}

def _m6w3_canonicalize_contract_output(c):
    if not isinstance(c, dict):
        c = {"route_kind": str(c), "receipts": [], "actions": []}

    rk = c.get("route_kind")
    if not isinstance(rk, str) or not rk.strip():
        c["route_kind"] = "UNKNOWN"

    receipts = c.get("receipts")
    actions = c.get("actions")

    if not isinstance(receipts, list):
        receipts = []
    if not isinstance(actions, list):
        actions = []

    # Receipts are side-effect evidence only. Strip metadata-only action types.
    if isinstance(receipts, list):
        receipts = [r for r in receipts if not (isinstance(r, dict) and str(r.get('type') or '') in META_ONLY_ACTION_TYPES)]

    c["receipts"] = [_m6w3_normalize_receipt(r) for r in receipts]
    c["actions"] = [a if isinstance(a, dict) else {"_repr": repr(a)} for a in actions]
    return c

# Wrap to_contract_output so every internal return path becomes canonical.
_to_contract_output_impl_m6w3 = to_contract_output

def to_contract_output(*args, **kwargs):
    c = _to_contract_output_impl_m6w3(*args, **kwargs)

    # M9W2: suggestions surface (non-binding). Derived ONLY from context (already attached in Week 1).
    if isinstance(c, dict):
        ctx = c.get("context")
        if not isinstance(ctx, dict):
            ctx = {}
        c["suggestions_version"] = SUGGESTIONS_VERSION
        c["suggestions"] = _m9w2_suggestions_from_context(ctx)

    # M9W4: proposal-only suggested executions (never executed).
    if isinstance(c, dict):
        c["proposed_actions_version"] = PROPOSED_ACTIONS_VERSION
        c["proposed_actions"] = _m9w4_proposed_actions_from_contract(c)
        # M10W2: review UX & trust signals (contract-only)
        c["review_controls_version"] = REVIEW_CONTROLS_VERSION
        c["review_controls"] = _m10w2_review_controls_from_contract(c)
        # M10W3: review ledger (metadata-only)
        c["review_ledger_version"] = REVIEW_LEDGER_VERSION
        c["review_ledger"] = _m10w3_review_ledger_from_contract(c)
        # M10W4: review conflict diagnostics (contract-only)
        c["review_conflicts_version"] = REVIEW_CONFLICTS_VERSION
        c["review_conflicts"] = _m10w4_review_conflicts_from_contract(c)

        # M11W2: commit acknowledgement (contract-only)
        c["commit_ack_version"] = COMMIT_ACK_VERSION
        c["commit_ack"] = _m11w2_commit_ack_from_contract(c)

        # M11W3: commit ledger (contract-only)
        c["commit_ledger_version"] = COMMIT_LEDGER_VERSION
        c["commit_ledger"] = _m11w3_commit_ledger_from_contract(c)
        # M11W1: commit gate DESIGN surfaces (no execution)
        c["commit_controls_version"] = COMMIT_CONTROLS_VERSION
        c["commit_controls"] = _m11w1_commit_controls_from_contract(c)
        c["commit_requests_version"] = COMMIT_REQUESTS_VERSION
        c["commit_requests"] = _m11w1_commit_requests_from_contract(c)
        c["commit_conflicts_version"] = COMMIT_CONFLICTS_VERSION
        c["commit_conflicts"] = _m11w1_commit_conflicts_from_contract(c)

    # M9W4: proposal-only mapping (FINAL PASS; after actions normalization).
    if isinstance(c, dict):
        c.setdefault("proposed_actions_version", "proposed_actions_v1")
        if not isinstance(c.get("proposed_actions"), list):
            c["proposed_actions"] = []

        acts = c.get("actions")
        if not isinstance(acts, list):
            acts = []

        sid = None
        for a in acts:
            if not isinstance(a, dict):
                continue
            k = a.get("kind") or a.get("type") or a.get("action_kind") or a.get("name") or ""
            k = str(k).strip().upper()
            if k == "SUGGESTION_ACCEPT":
                pld = a.get("payload")
                if not isinstance(pld, dict):
                    pld = a.get("data") if isinstance(a.get("data"), dict) else {}
                sid = pld.get("suggestion_id")
                if isinstance(sid, str) and sid.strip():
                    sid = sid.strip()
                    break

        # Only populate proposals after explicit accept.
        if sid:
            ctx = c.get("context")
            if not isinstance(ctx, dict):
                ctx = {}
            app = str(ctx.get("active_app") or "").strip()
            hint = str(ctx.get("screen_hint") or "").strip()
            q = f"{hint} {app}".strip() or "context"

            c["proposed_actions"] = [{
                "id": _m7w2_hash_id({"sid": sid, "kind": "WEB_LOOKUP_QUERY", "payload": {"query": q}}),
                "kind": "WEB_LOOKUP_QUERY",
                "label": f"Proposed: search the web for “{q}”",
                "reason": "Mapped from explicit SUGGESTION_ACCEPT + context_v1. Proposal-only (non-binding).",
                "payload": {"query": q},
            }]
    return _m6w3_canonicalize_contract_output(c)

# === MONTH7W2_ACTION_NORMALIZATION ===

def _m7w2_hash_id(obj) -> str:
    try:
        raw = json.dumps(obj, sort_keys=True, default=str).encode("utf-8")
    except Exception:
        raw = repr(obj).encode("utf-8")
    return hashlib.sha1(raw).hexdigest()[:12]

def _m7w2_normalize_action(a):
    if a is None:
        return {"id": _m7w2_hash_id("NONE"), "kind": "UNKNOWN", "payload": {}}
    if not isinstance(a, dict):
        return {"id": _m7w2_hash_id({"_repr": repr(a)}), "kind": "UNKNOWN", "payload": {}, "_repr": repr(a)}

    kind = a.get("kind") or a.get("action_kind") or a.get("type") or a.get("name") or "UNKNOWN"
    kind = str(kind).strip().upper() or "UNKNOWN"

    payload = a.get("payload")
    if not isinstance(payload, dict):
        payload = a.get("data") if isinstance(a.get("data"), dict) else {}

    aid = a.get("id") or a.get("action_id") or a.get("receipt_id") or a.get("event_id")
    aid = str(aid).strip() if isinstance(aid, str) else ""
    if not aid:
        # Stable ID derived from kind+payload only (deterministic)
        aid = _m7w2_hash_id({"kind": kind, "payload": payload})

    out = {"id": aid, "kind": kind, "payload": payload}
    # Keep any extra keys for debugging, but don't rely on them.
    if "_repr" in a:
        out["_repr"] = a["_repr"]
    return out

# Upgrade the existing canonicalizer to normalize actions too.
_m6w3_canonicalize_contract_output_prev = _m6w3_canonicalize_contract_output

def _m6w3_canonicalize_contract_output(c):
    c = _m6w3_canonicalize_contract_output_prev(c)
    actions = c.get("actions")
    if not isinstance(actions, list):
        actions = []
    c["actions"] = [_m7w2_normalize_action(a) for a in actions]
    return c

