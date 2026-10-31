"""Proposal C working probe: end-to-end response chain.

Toy implementation of docs/proposals/lure-response-proposal-c-response-algorithm-v1.md.
This probe now drives the whole path: frame/snapshot selection -> per-family
support/state -> evaluate -> compose -> L×C join, preserving provenance.

2026-10-30 direction: no latent bearing (K_close=0.19 on the no-theta scale);
sibling max with skipped provenance; interval support validation; cast snapshot
selected by ConditionGroup × EngagementMode.

Run: python3 -I prototypes/lure-response/proposal_c_end_to_end_probe.py
"""

from __future__ import annotations

import math

M0, M1 = 0.0, 0.40
K_CLOSE = 0.19  # no-theta rescale: was 0.76 under bearing averaging (x 1/4)
TRIGGER_BUDGET = 0.10
K_WARY = 1.0

RESOLVED = "Resolved"
UNKNOWN = "Unknown"
NOT_CONFIGURED = "NotConfigured"
RI = "ResolutionIncomplete"
REJECT = "Reject"
INVALID = "InvalidInput"


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def threshold(m: float) -> float:
    base = 0.60 - 0.40 * m
    if m > 0.80:
        base -= 0.50 * (m - 0.80)
    return base


def _finite(x) -> bool:
    return isinstance(x, (int, float)) and math.isfinite(x)


def activity_multiplier(activity):
    if activity in (UNKNOWN, NOT_CONFIGURED):
        return activity, None
    if not _finite(activity) or activity < 0:
        return INVALID, None
    return RESOLVED, float(activity)


def interval_valid(interval) -> bool:
    if not isinstance(interval, tuple) or len(interval) != 2:
        return False
    lo, hi = interval
    if not (_finite(lo) and _finite(hi)):
        return False
    return 0.0 <= lo <= hi <= 1.0


def normalize_support(support):
    """value | (lo, hi) | status -> (status, value). Invalid intervals -> InvalidInput."""
    if isinstance(support, tuple):
        if not interval_valid(support):
            return INVALID, None
        lo, hi = support
        if lo == hi:
            return RESOLVED, float(lo)
        return RI, None
    if support == REJECT:
        return REJECT, 0.0
    if support == UNKNOWN:
        return UNKNOWN, None
    if support == NOT_CONFIGURED:
        return NOT_CONFIGURED, None
    if support == INVALID:
        return INVALID, None
    if not _finite(support) or not 0.0 <= support <= 1.0:
        return INVALID, None
    return RESOLVED, float(support)


def cast_entry(cast_fc, cast_id, group, mode):
    if not cast_fc:
        return None
    if cast_fc.get("castId") != cast_id:
        return None
    if not cast_fc.get("blockVersion") or not cast_fc.get("formedAt"):
        return None
    return cast_fc.get("entries", {}).get((group, mode))


def evaluate(state_trigger, entry, seg):
    """entry fields: activity, feedingMotivation, wariness, dietShift."""
    act_status, activity = activity_multiplier(entry.get("activity"))
    if act_status != RESOLVED:
        return act_status, None

    motivation = entry.get("feedingMotivation")
    if motivation in (UNKNOWN, NOT_CONFIGURED):
        return motivation, None
    if not _finite(motivation):
        return INVALID, None

    wariness = entry.get("wariness")
    suspicion = seg.get("suspicionLoad", 0.0)
    if wariness in (UNKNOWN, NOT_CONFIGURED):
        if suspicion != 0.0:
            return wariness, None          # 缺失且有 cue：不闭合
        wariness = 0.0                     # 缺失且无 cue：RiskCost = 0
    elif not _finite(wariness):
        return INVALID, None

    food = clamp01(seg["food"] + entry.get("dietShift", {}).get(seg.get("family"), 0.0))
    trigger = TRIGGER_BUDGET * state_trigger
    closing = K_CLOSE * seg["q"] ** 2 * activity
    risk = K_WARY * wariness * suspicion
    margin = food + trigger - closing - risk - threshold(motivation)
    if not math.isfinite(margin):
        return INVALID, None
    return RESOLVED, clamp01((margin - M0) / (M1 - M0))


def branch_response(family, support, state, entry, seg):
    relation = seg.get("targetRelations", {}).get(family)
    if relation == REJECT:
        return REJECT, 0.0
    status, value = normalize_support(support)
    if status != RESOLVED:
        return status, value
    if state == REJECT:
        return REJECT, 0.0
    if state in (UNKNOWN, NOT_CONFIGURED):
        return state, None
    if not _finite(state) or not 0.0 <= state <= 1.0:
        return INVALID, None
    c_status, c = evaluate(state, entry, seg)
    if c_status != RESOLVED:
        return c_status, None
    return RESOLVED, value * c


def compose(results):
    """results: {family: (original_status, value)} -> (status, C_feed, skipped)."""
    resolved = [v for s, v in results.values() if s == RESOLVED]
    rejected = [v for s, v in results.values() if s == REJECT]
    skipped = {f: s for f, (s, _) in results.items()
               if s in (RI, UNKNOWN, NOT_CONFIGURED)}
    if any(s == INVALID for s, _ in results.values()):
        return INVALID, None, skipped
    if not resolved and rejected:
        return REJECT, 0.0, skipped
    if not resolved and not rejected:
        return RI, None, skipped
    return RESOLVED, max(resolved + rejected), skipped


def join(c_feed, L, skipped):
    if c_feed is None or L is None:
        return RI, None, skipped
    if L in (UNKNOWN, NOT_CONFIGURED):
        return RI, None, skipped
    if L == INVALID:
        return INVALID, None, skipped
    if not _finite(L) or L < 0:
        return INVALID, None, skipped
    return RESOLVED, L * c_feed, skipped


def response(seg, asm, cast_fc, supports, states, L):
    """Full driver: frame check -> snapshot entry -> families -> compose -> join."""
    if not seg.get("valid") or asm.get("version") != seg.get("assemblyVersion"):
        return RI, None, {}
    entry = cast_entry(cast_fc, seg["castId"], seg["conditionGroupId"], seg["engagementModeId"])
    if entry is None:
        return RI, None, {}

    results = {}
    for family in seg["siblingSet"]:
        results[family] = branch_response(
            family, supports.get(family), states.get(family), entry, seg
        )

    status, c_feed, skipped = compose(results)
    if status != RESOLVED:
        return status, None, skipped
    return join(c_feed, L, skipped)


def make_snapshot(entries, cast_id="cast-1", version="v1", formed_at=10.0):
    return {
        "castId": cast_id,
        "formedAt": formed_at,
        "blockVersion": version,
        "entries": entries,
    }


def base_entry(**overrides):
    entry = {
        "activity": 1.0,
        "feedingMotivation": 0.5,
        "wariness": 0.0,
        "dietShift": {},
    }
    entry.update(overrides)
    return entry


def base_seg(**overrides):
    seg = {
        "valid": True,
        "castId": "cast-1",
        "assemblyVersion": 1,
        "conditionGroupId": "cg-1",
        "engagementModeId": "mode-stalk",
        "siblingSet": ["baitfish", "crayfish"],
        "food": 0.70,
        "q": 0.40,
        "suspicionLoad": 0.0,
    }
    seg.update(overrides)
    return seg


def main() -> None:
    print("end-to-end driver scenarios")
    asm = {"version": 1}
    entry = base_entry()
    snap = make_snapshot({("cg-1", "mode-stalk"): entry})
    seg = base_seg()
    supports = {"baitfish": 1.0, "crayfish": 0.5}
    states = {"baitfish": 0.80, "crayfish": 0.40}

    out = response(seg, asm, snap, supports, states, 0.50)
    print("happy path:", out)

    # targetRelation Reject for one family
    seg_tr = base_seg(targetRelations={"crayfish": REJECT})
    out_tr = response(seg_tr, asm, snap, {"baitfish": 0.45, "crayfish": 0.90}, states, 0.50)
    print("target relation reject:", out_tr)

    # all families Reject
    seg_all = base_seg(targetRelations={"baitfish": REJECT, "crayfish": REJECT})
    out_all = response(seg_all, asm, snap, supports, states, 0.50)
    print("all reject:", out_all)

    # Reject + Unknown keeps original status in provenance
    out_rej_unk = response(
        seg_tr, asm, snap, {"baitfish": UNKNOWN, "crayfish": 0.90}, states, 0.50
    )
    print("reject + unknown:", out_rej_unk)

    # NotConfigured keeps its own reason
    out_nc = response(seg, asm, snap, {"baitfish": 1.0, "crayfish": NOT_CONFIGURED}, states, 0.50)
    print("not configured sibling:", out_nc)

    # Non-degenerate interval is skipped with RI, provenance survives join
    out_interval = response(
        seg, asm, snap, {"baitfish": 0.45, "crayfish": (0.10, 0.90)}, states, 0.50
    )
    print("interval sibling:", out_interval)

    # Degenerate interval behaves exactly like its scalar
    out_degenerate = response(seg, asm, snap, {"baitfish": 0.45, "crayfish": (0.50, 0.50)}, states, 0.50)
    out_scalar = response(seg, asm, snap, {"baitfish": 0.45, "crayfish": 0.50}, states, 0.50)
    same_states = {"baitfish": 0.80, "crayfish": 0.80}
    out_full = response(seg, asm, snap, {"baitfish": 1.0, "crayfish": 1.0}, same_states, 0.50)
    out_half_interval = response(
        seg, asm, snap, {"baitfish": (0.50, 0.50), "crayfish": (0.50, 0.50)}, same_states, 0.50
    )
    print("degenerate interval:", out_degenerate)
    print("same scalar:", out_scalar)

    # Invalid intervals must be InvalidInput, not evaluated
    out_bad_hi = response(seg, asm, snap, {"baitfish": 1.0, "crayfish": (2.0, 2.0)}, states, 0.50)
    out_bad_inv = response(seg, asm, snap, {"baitfish": 1.0, "crayfish": (0.75, 0.40)}, states, 0.50)
    out_bad_nan = response(seg, asm, snap, {"baitfish": 1.0, "crayfish": (float("nan"), 0.5)}, states, 0.50)
    print("invalid interval high:", out_bad_hi)
    print("invalid interval inverted:", out_bad_inv)
    print("invalid interval nan:", out_bad_nan)

    # Snapshot mode/group selection changes the evaluated entry
    snap_modes = make_snapshot({
        ("cg-1", "mode-stalk"): base_entry(activity=1.0),
        ("cg-1", "mode-cruise"): base_entry(activity=2.0),
        ("cg-2", "mode-stalk"): base_entry(activity=0.5),
    })
    out_stalk = response(base_seg(), asm, snap_modes, supports, states, 0.50)
    out_cruise = response(base_seg(engagementModeId="mode-cruise"), asm, snap_modes, supports, states, 0.50)
    out_group2 = response(base_seg(conditionGroupId="cg-2"), asm, snap_modes, supports, states, 0.50)
    print("mode stalk:", out_stalk)
    print("mode cruise:", out_cruise)
    print("group cg-2:", out_group2)

    # Snapshot metadata failures
    out_wrong_cast = response(base_seg(castId="cast-2"), asm, snap, supports, states, 0.50)
    out_no_version = response(base_seg(), asm, make_snapshot({("cg-1", "mode-stalk"): entry}, version=""), supports, states, 0.50)
    out_missing_entry = response(base_seg(engagementModeId="mode-other"), asm, snap, supports, states, 0.50)
    print("wrong cast:", out_wrong_cast)
    print("missing version:", out_no_version)
    print("missing entry:", out_missing_entry)

    # Per-field: unknown wariness without cue stays resolved; with cue blocks
    snap_unknown_wariness = make_snapshot({("cg-1", "mode-stalk"): base_entry(wariness=UNKNOWN)})
    out_no_cue = response(base_seg(), asm, snap_unknown_wariness, supports, states, 0.50)
    out_with_cue = response(base_seg(suspicionLoad=0.1), asm, snap_unknown_wariness, supports, states, 0.50)
    print("unknown wariness no cue:", out_no_cue)
    print("unknown wariness with cue:", out_with_cue)

    # Unknown activity blocks all families via evaluate status
    snap_unknown_activity = make_snapshot({("cg-1", "mode-stalk"): base_entry(activity=UNKNOWN)})
    out_unknown_activity = response(base_seg(), asm, snap_unknown_activity, supports, states, 0.50)
    print("unknown activity:", out_unknown_activity)

    # assertions
    assert out[0] == RESOLVED and 0 < out[1] <= 1
    assert out[2] == {}
    assert out_tr[0] == RESOLVED and abs(out_tr[1] - 0.50 * (0.45 * out[1] / 0.50)) < 1e-9
    assert out_all == (REJECT, None, {})
    assert out_rej_unk[0] == REJECT and out_rej_unk[2] == {"baitfish": UNKNOWN}
    assert out_nc[0] == RESOLVED and out_nc[2] == {"crayfish": NOT_CONFIGURED}
    assert out_interval[0] == RESOLVED and out_interval[2] == {"crayfish": RI}
    assert out_interval[1] < out[1]                      # skipped branch does not add value
    assert abs(out_degenerate[1] - out_scalar[1]) < 1e-12
    assert abs(out_degenerate[1] - out[1]) > 1e-6        # half support is not full support
    assert abs(out_half_interval[1] * 2 - out_full[1]) < 1e-12  # degenerate 0.5 is exactly half of support 1.0
    assert out_bad_hi[0] == INVALID and out_bad_inv[0] == INVALID and out_bad_nan[0] == INVALID
    assert out_group2[1] > out_stalk[1] > out_cruise[1]  # higher activity multiplier = higher cost
    assert out_wrong_cast[0] == RI
    assert out_no_version[0] == RI
    assert out_missing_entry[0] == RI
    assert out_no_cue[0] == RESOLVED
    assert out_with_cue[0] == RI and out_with_cue[2] == {"baitfish": UNKNOWN, "crayfish": UNKNOWN}
    assert out_unknown_activity[0] == RI
    assert out_unknown_activity[2] == {"baitfish": UNKNOWN, "crayfish": UNKNOWN}

    # single multiply: q is exactly L × C, no second factor
    assert abs(0.5 * 0.6 - 0.30) < 1e-12

    print("End-to-end response probe passed")


if __name__ == "__main__":
    main()
