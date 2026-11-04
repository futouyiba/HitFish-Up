"""Proposal C working probe: end-to-end response chain.

Toy implementation of docs/proposals/lure-response-proposal-c-response-algorithm-v1.md.
Driver: frame/snapshot selection -> per-family support/state -> evaluate -> compose.
Response returns C_feed only; L x C is a separate Opportunity-internal toy join
(2026-11-04: the roundtable interface is SpatialDistributionWeight x AdaptationCoeff).

2026-10-30 direction: no latent bearing (K_close=0.19 on the no-theta scale);
sibling max with skipped provenance; interval support validation; cast snapshot
selected by ConditionGroup x EngagementMode. Activity domain is [0,2] and maps to
ActivityCostMultiplier = clamp(1/A, 0.5, 2), A=0 -> 2.

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
    """Activity [0,2] -> ActivityCostMultiplier clamp(1/A, 0.5, 2); A=0 -> 2."""
    if activity in (UNKNOWN, NOT_CONFIGURED):
        return activity, None
    if not _finite(activity) or not 0.0 <= activity <= 2.0:
        return INVALID, None
    if activity == 0.0:
        return RESOLVED, 2.0
    return RESOLVED, max(0.5, min(2.0, 1.0 / activity))


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


def evaluate(family, state_trigger, entry, seg):
    """entry fields: activity, feedingMotivation, wariness, dietShift[family]."""
    act_status, activity_mult = activity_multiplier(entry.get("activity"))
    if act_status != RESOLVED:
        return act_status, None

    motivation = entry.get("feedingMotivation")
    if motivation in (UNKNOWN, NOT_CONFIGURED):
        return motivation, None
    if not _finite(motivation) or not 0.0 <= motivation <= 1.0:
        return INVALID, None

    wariness = entry.get("wariness")
    suspicion = seg.get("suspicionLoad", 0.0)
    if not _finite(suspicion):
        return INVALID, None
    if wariness in (UNKNOWN, NOT_CONFIGURED):
        if suspicion != 0.0:
            return wariness, None          # 缺失且有 cue：不闭合
        wariness = 0.0                     # 缺失且无 cue：RiskCost = 0
    elif not _finite(wariness) or not 0.0 <= wariness <= 1.0:
        return INVALID, None

    if not _finite(seg.get("food")):
        return INVALID, None
    diet = entry.get("dietShift", {}).get(family)
    if diet is None:
        return UNKNOWN, None               # 缺失 family 偏移：该 family 不闭合
    if diet in (UNKNOWN, NOT_CONFIGURED):
        return diet, None
    if not _finite(diet) or not -0.2 <= diet <= 0.2:
        return INVALID, None
    food = clamp01(seg["food"] + diet)

    if not _finite(seg.get("q")):
        return INVALID, None
    trigger = TRIGGER_BUDGET * state_trigger
    closing = K_CLOSE * seg["q"] ** 2 * activity_mult
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
    c_status, c = evaluate(family, state, entry, seg)
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


def opportunity_join(c_feed, L, skipped):
    """Opportunity-internal toy join. Not the roundtable interface."""
    if c_feed is None or L is None:
        return RI, None, skipped
    if L in (UNKNOWN, NOT_CONFIGURED):
        return RI, None, skipped
    if L == INVALID:
        return INVALID, None, skipped
    if not _finite(L) or L < 0:
        return INVALID, None, skipped
    return RESOLVED, L * c_feed, skipped


def response(seg, asm, cast_fc, supports, states):
    """Response driver: returns (status, C_feed, skipped). No L join."""
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

    return compose(results)


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
        "dietShift": {"baitfish": 0.0, "crayfish": 0.0},
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

    out = response(seg, asm, snap, supports, states)
    print("happy path:", out)

    seg_tr = base_seg(targetRelations={"crayfish": REJECT})
    out_tr = response(seg_tr, asm, snap, {"baitfish": 0.45, "crayfish": 0.90}, states)
    print("target relation reject:", out_tr)

    seg_all = base_seg(targetRelations={"baitfish": REJECT, "crayfish": REJECT})
    out_all = response(seg_all, asm, snap, supports, states)
    print("all reject:", out_all)

    out_rej_unk = response(seg_tr, asm, snap, {"baitfish": UNKNOWN, "crayfish": 0.90}, states)
    print("reject + unknown:", out_rej_unk)

    out_nc = response(seg, asm, snap, {"baitfish": 1.0, "crayfish": NOT_CONFIGURED}, states)
    print("not configured sibling:", out_nc)

    out_interval = response(seg, asm, snap, {"baitfish": 0.45, "crayfish": (0.10, 0.90)}, states)
    print("interval sibling:", out_interval)

    out_degenerate = response(seg, asm, snap, {"baitfish": 0.45, "crayfish": (0.50, 0.50)}, states)
    out_scalar = response(seg, asm, snap, {"baitfish": 0.45, "crayfish": 0.50}, states)
    same_states = {"baitfish": 0.80, "crayfish": 0.80}
    out_full = response(seg, asm, snap, {"baitfish": 1.0, "crayfish": 1.0}, same_states)
    out_half_interval = response(
        seg, asm, snap, {"baitfish": (0.50, 0.50), "crayfish": (0.50, 0.50)}, same_states
    )
    print("degenerate interval:", out_degenerate)
    print("same scalar:", out_scalar)

    out_bad_hi = response(seg, asm, snap, {"baitfish": 1.0, "crayfish": (2.0, 2.0)}, states)
    out_bad_inv = response(seg, asm, snap, {"baitfish": 1.0, "crayfish": (0.75, 0.40)}, states)
    out_bad_nan = response(seg, asm, snap, {"baitfish": 1.0, "crayfish": (float("nan"), 0.5)}, states)
    print("invalid interval high:", out_bad_hi)
    print("invalid interval inverted:", out_bad_inv)
    print("invalid interval nan:", out_bad_nan)

    snap_modes = make_snapshot({
        ("cg-1", "mode-stalk"): base_entry(activity=1.0),
        ("cg-1", "mode-cruise"): base_entry(activity=2.0),
        ("cg-2", "mode-stalk"): base_entry(activity=0.5),
    })
    out_stalk = response(base_seg(), asm, snap_modes, supports, states)
    out_cruise = response(base_seg(engagementModeId="mode-cruise"), asm, snap_modes, supports, states)
    out_group2 = response(base_seg(conditionGroupId="cg-2"), asm, snap_modes, supports, states)
    print("mode stalk:", out_stalk)
    print("mode cruise:", out_cruise)
    print("group cg-2:", out_group2)

    out_wrong_cast = response(base_seg(castId="cast-2"), asm, snap, supports, states)
    out_no_version = response(base_seg(), asm, make_snapshot({("cg-1", "mode-stalk"): entry}, version=""), supports, states)
    out_missing_entry = response(base_seg(engagementModeId="mode-other"), asm, snap, supports, states)
    print("wrong cast:", out_wrong_cast)
    print("missing version:", out_no_version)
    print("missing entry:", out_missing_entry)

    snap_unknown_wariness = make_snapshot({("cg-1", "mode-stalk"): base_entry(wariness=UNKNOWN)})
    out_no_cue = response(base_seg(), asm, snap_unknown_wariness, supports, states)
    out_with_cue = response(base_seg(suspicionLoad=0.1), asm, snap_unknown_wariness, supports, states)
    print("unknown wariness no cue:", out_no_cue)
    print("unknown wariness with cue:", out_with_cue)

    snap_diet = make_snapshot({
        ("cg-1", "mode-stalk"): base_entry(dietShift={"baitfish": 0.10, "crayfish": -0.10})
    })
    out_diet = response(seg, asm, snap_diet, {"baitfish": 1.0, "crayfish": 0.30}, states)
    print("diet shift +0.10 baitfish:", out_diet)
    snap_diet_unknown = make_snapshot({
        ("cg-1", "mode-stalk"): base_entry(dietShift={"baitfish": UNKNOWN, "crayfish": 0.0})
    })
    out_diet_unknown = response(seg, asm, snap_diet_unknown, {"baitfish": 1.0, "crayfish": 0.30}, states)
    print("diet shift unknown baitfish:", out_diet_unknown)

    snap_unknown_activity = make_snapshot({("cg-1", "mode-stalk"): base_entry(activity=UNKNOWN)})
    out_unknown_activity = response(base_seg(), asm, snap_unknown_activity, supports, states)
    print("unknown activity:", out_unknown_activity)

    snap_activity_out = make_snapshot({("cg-1", "mode-stalk"): base_entry(activity=2.5)})
    out_activity_out = response(base_seg(), asm, snap_activity_out, supports, states)
    print("activity out of range:", out_activity_out)

    out_nan_food = response(base_seg(food=float("nan")), asm, snap, supports, states)
    out_nan_q = response(base_seg(q=float("nan")), asm, snap, supports, states)
    print("nan food:", out_nan_food)
    print("nan q:", out_nan_q)

    joined = opportunity_join(out[1], 0.50, out[2])
    joined_low = opportunity_join(out[1], 0.25, out[2])
    join_missing = opportunity_join(out[1], None, out[2])
    join_invalid = opportunity_join(out[1], INVALID, out[2])
    print("C_feed:", out)
    print("opportunity join L=0.50:", joined)
    print("opportunity join L=0.25:", joined_low)
    print("join missing L:", join_missing)
    print("join invalid L:", join_invalid)

    snap_no_formed_at = make_snapshot({("cg-1", "mode-stalk"): entry}, formed_at=None)
    out_no_formed_at = response(base_seg(), asm, snap_no_formed_at, supports, states)
    print("missing formedAt:", out_no_formed_at)

    # assertions
    assert out[0] == RESOLVED and abs(out[1] - 0.874) < 1e-9   # Response returns C_feed
    assert out[2] == {}
    assert out_tr[0] == RESOLVED and abs(out_tr[1] - 0.45 * out[1]) < 1e-9
    assert out_all == (REJECT, 0.0, {})
    assert out_rej_unk[0] == REJECT and out_rej_unk[1] == 0.0 and out_rej_unk[2] == {"baitfish": UNKNOWN}
    assert out_nc[0] == RESOLVED and out_nc[2] == {"crayfish": NOT_CONFIGURED}
    assert out_interval[0] == RESOLVED and out_interval[2] == {"crayfish": RI}
    assert abs(out_interval[1] - 0.45 * out[1]) < 1e-9
    assert abs(out_degenerate[1] - out_scalar[1]) < 1e-12
    assert abs(out_degenerate[1] - out[1]) > 1e-6
    assert abs(out_half_interval[1] * 2 - out_full[1]) < 1e-12
    assert out_bad_hi[0] == INVALID and out_bad_inv[0] == INVALID and out_bad_nan[0] == INVALID
    assert out_cruise[1] > out_stalk[1] > out_group2[1]   # higher Activity = lower cost multiplier
    assert out_wrong_cast[0] == RI
    assert out_no_version[0] == RI
    assert out_missing_entry[0] == RI
    assert out_no_cue[0] == RESOLVED
    assert out_with_cue[0] == RI and out_with_cue[2] == {"baitfish": UNKNOWN, "crayfish": UNKNOWN}
    assert out_unknown_activity[0] == RI
    assert out_unknown_activity[2] == {"baitfish": UNKNOWN, "crayfish": UNKNOWN}
    assert out_activity_out[0] == INVALID

    assert out_diet[0] == RESOLVED and abs(out_diet[1] - 1.0) < 1e-9
    assert out_diet_unknown[0] == RESOLVED
    assert out_diet_unknown[2] == {"baitfish": UNKNOWN}
    assert out_diet_unknown[1] < out_diet[1]

    assert out_nan_food[0] == INVALID
    assert out_nan_q[0] == INVALID

    # Opportunity-internal toy join only; roundtable is SDW x AdaptationCoeff.
    assert opportunity_join(0.6, 0.5, {}) == (RESOLVED, 0.30, {})
    assert opportunity_join(0.6, None, {}) == (RI, None, {})
    assert opportunity_join(0.6, INVALID, {}) == (INVALID, None, {})
    assert abs(joined[1] - 0.5 * out[1]) < 1e-9
    assert abs(joined_low[1] * 2 - joined[1]) < 1e-12
    assert join_missing[0] == RI and join_invalid[0] == INVALID

    assert out_no_formed_at[0] == RI

    # Activity mapping: domain and monotone decreasing multiplier.
    assert activity_multiplier(0.5) == (RESOLVED, 2.0)
    assert activity_multiplier(1.0) == (RESOLVED, 1.0)
    assert activity_multiplier(2.0) == (RESOLVED, 0.5)
    assert activity_multiplier(0.0) == (RESOLVED, 2.0)
    assert activity_multiplier(2.5)[0] == INVALID

    print("End-to-end response probe passed")


if __name__ == "__main__":
    main()
