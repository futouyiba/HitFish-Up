"""Proposal C step-3 development probe.

ActualPresentation-like shared facts are maintained independently of prey support.
Prey-conditioned state interpretation consumes those facts but does not mutate them.

All thresholds are proposal assumptions from section 5; this is not calibrated biology.
"""

from dataclasses import dataclass, field
from math import isclose

MOVE_ENTER = 0.04
MOVE_HOLD = 0.10
LOW_ENTER = 0.02
LOW_HOLD = 0.15
RECENT_PAUSE = 3.0
VERT_ENTER = 0.02
VERT_LOW = 0.01
VERT_HOLD = 0.15
IMBALANCE_ROLL = 60.0
IMBALANCE_HOLD = 0.20
EPS = 1e-9


@dataclass
class Segment:
    kind: str
    start: float
    confirmed: float
    end: float | None = None
    observed_lower_bound: bool = False

    def duration_at(self, t):
        return (self.end if self.end is not None else t) - self.start


@dataclass
class AxisState:
    confirmed: str | None = None
    segment: Segment | None = None
    candidate_kind: str | None = None
    candidate_start: float | None = None
    last_closed: Segment | None = None


@dataclass
class TemporalEvent:
    kind: str
    start: float
    end: float
    source_version: str | None = None


@dataclass
class Memory:
    continuity_id: str | None = None
    source_version: str | None = None
    last_t: float | None = None
    last_signature: tuple | None = None
    motion: AxisState = field(default_factory=AxisState)
    relative_motion: AxisState = field(default_factory=AxisState)
    vertical: AxisState = field(default_factory=AxisState)
    recent_events: list = field(default_factory=list)
    gap_since_last_valid: bool = False
    previous_speed: float | None = None
    previous_t: float | None = None
    burst_high_t: float | None = None
    burst_low_after_t: float | None = None
    burst_event: TemporalEvent | None = None
    imbalance_candidate_start: float | None = None
    imbalance_status: str = "Unknown"

    def reset_continuity(self, continuity_id, t):
        self.continuity_id = continuity_id
        self.last_t = None
        self.last_signature = None
        self.motion = AxisState()
        self.relative_motion = AxisState()
        self.vertical = AxisState()
        self.recent_events = []
        self.gap_since_last_valid = False
        self.previous_speed = None
        self.previous_t = None
        self.burst_high_t = None
        self.burst_low_after_t = None
        self.burst_event = None
        self.imbalance_candidate_start = None
        self.imbalance_status = "Unknown"

    def rebind_source(self, version):
        if self.source_version != version:
            self.source_version = version
            self.recent_events = [e for e in self.recent_events if e.source_version is None]
            self.burst_event = None
            self.burst_high_t = None
            self.burst_low_after_t = None


def _update_binary(axis, t, value, high_kind, low_kind, high_thr, low_thr, high_hold, low_hold):
    if value >= high_thr:
        candidate = high_kind
        hold = high_hold
    elif value <= low_thr:
        candidate = low_kind
        hold = low_hold
    else:
        axis.candidate_kind = None
        axis.candidate_start = None
        return

    if axis.confirmed == candidate:
        axis.candidate_kind = None
        axis.candidate_start = None
        return

    if axis.candidate_kind != candidate:
        axis.candidate_kind = candidate
        axis.candidate_start = t
        return

    if t - axis.candidate_start + EPS >= hold:
        if axis.segment is not None:
            axis.segment.end = axis.candidate_start
            axis.last_closed = axis.segment
        axis.confirmed = candidate
        axis.segment = Segment(candidate, axis.candidate_start, t)
        axis.candidate_kind = None
        axis.candidate_start = None


def _update_vertical(axis, t, vz):
    if vz >= VERT_ENTER:
        candidate = "rising"
    elif vz <= -VERT_ENTER:
        candidate = "falling"
    elif abs(vz) <= VERT_LOW:
        candidate = "vertical_low"
    else:
        axis.candidate_kind = None
        axis.candidate_start = None
        return

    if axis.confirmed == candidate:
        axis.candidate_kind = None
        axis.candidate_start = None
        return

    if axis.candidate_kind != candidate:
        axis.candidate_kind = candidate
        axis.candidate_start = t
        return

    if t - axis.candidate_start + EPS >= VERT_HOLD:
        if axis.segment:
            axis.segment.end = axis.candidate_start
            axis.last_closed = axis.segment
        axis.confirmed = candidate
        axis.segment = Segment(candidate, axis.candidate_start, t)
        axis.candidate_kind = None
        axis.candidate_start = None


def process(mem, sample):
    t = float(sample["t"])
    continuity_id = sample.get("continuity_id", "cast-1")
    version = sample.get("source_version", "v1")
    if mem.continuity_id != continuity_id:
        mem.reset_continuity(continuity_id, t)
    mem.rebind_source(version)

    sig = tuple(sorted((k, repr(v)) for k, v in sample.items() if k != "prey_support"))
    if mem.last_t is not None:
        if t < mem.last_t - EPS:
            raise ValueError("out-of-order sample")
        if isclose(t, mem.last_t, abs_tol=EPS):
            if sig == mem.last_signature:
                return snapshot(mem, sample)
            raise ValueError("conflicting sample at same time")

    if sample.get("gap"):
        mem.gap_since_last_valid = True
        mem.motion = AxisState()
        mem.relative_motion = AxisState()
        mem.vertical = AxisState()
        mem.previous_speed = None
        mem.previous_t = None
        mem.burst_high_t = None
        mem.burst_low_after_t = None
        mem.imbalance_candidate_start = None
        mem.imbalance_status = "Unknown"
        mem.last_t, mem.last_signature = t, sig
        return snapshot(mem, sample)

    v = float(sample["world_speed"])
    rv = sample.get("relative_speed")
    vz = float(sample.get("vertical_speed", 0.0))

    _update_binary(mem.motion, t, v, "moving", "low", MOVE_ENTER, LOW_ENTER, MOVE_HOLD, LOW_HOLD)
    if rv is not None:
        _update_binary(mem.relative_motion, t, float(rv), "moving", "low", MOVE_ENTER, LOW_ENTER, MOVE_HOLD, LOW_HOLD)
    _update_vertical(mem.vertical, t, vz)

    # Ordered short acceleration followed by low motion.
    if mem.previous_speed is not None and mem.previous_t is not None:
        if mem.previous_speed <= MOVE_ENTER and v >= 0.20 and t - mem.previous_t <= 0.15 + EPS:
            mem.burst_high_t = t
            mem.burst_low_after_t = None
        if mem.burst_high_t is not None and v <= LOW_ENTER and 0 <= t - mem.burst_high_t <= 0.50 + EPS:
            if mem.burst_low_after_t is None:
                mem.burst_low_after_t = t
        if mem.burst_low_after_t is not None and v <= LOW_ENTER and t - mem.burst_low_after_t >= LOW_HOLD - EPS:
            mem.burst_event = TemporalEvent("burst_then_pause", mem.burst_high_t, t, mem.source_version)
        elif mem.burst_low_after_t is not None and v > LOW_ENTER:
            mem.burst_low_after_t = None

    # Optional frog imbalance-like sinking rule.
    roll = sample.get("roll_deg")
    if vz <= -0.02:
        if roll is None:
            mem.imbalance_candidate_start = None
            mem.imbalance_status = "Unknown"
        elif abs(float(roll)) > IMBALANCE_ROLL:
            if mem.imbalance_candidate_start is None:
                mem.imbalance_candidate_start = t
            if t - mem.imbalance_candidate_start + EPS >= IMBALANCE_HOLD:
                mem.imbalance_status = "Match"
        else:
            mem.imbalance_candidate_start = None
            mem.imbalance_status = "NoMatch"
    else:
        mem.imbalance_candidate_start = None
        mem.imbalance_status = "NoMatch"

    if mem.gap_since_last_valid:
        if mem.motion.segment and mem.motion.segment.start > (mem.last_t or -1):
            mem.gap_since_last_valid = False

    mem.previous_speed, mem.previous_t = v, t
    mem.last_t, mem.last_signature = t, sig
    return snapshot(mem, sample)


def _recent_move_pause(mem, t):
    if mem.motion.confirmed != "low" or mem.motion.segment is None:
        return "NoMatch"
    prev = mem.motion.last_closed
    if prev is None or prev.kind != "moving":
        return "Unknown"
    age = t - prev.end
    return "Match" if age <= RECENT_PAUSE + EPS else "NoMatch"


def snapshot(mem, sample):
    t = float(sample["t"])

    def axis_packet(axis):
        if not axis.segment:
            return {"state": axis.confirmed}
        return {
            "state": axis.confirmed,
            "start": axis.segment.start,
            "confirmed": axis.segment.confirmed,
            "duration": axis.segment.duration_at(t),
        }

    # Shared facts are prey-independent and stay outside prey interpretations.
    facts = {
        "world_speed": sample.get("world_speed"),
        "relative_speed": sample.get("relative_speed"),
        "motion": axis_packet(mem.motion),
        "relative_motion": axis_packet(mem.relative_motion),
        "vertical": axis_packet(mem.vertical),
        "surface": bool(sample.get("surface", False)),
        "near_bottom": bool(sample.get("near_bottom", False)),
        "source_version": mem.source_version,
        "continuity_id": mem.continuity_id,
    }

    # Prey support is consumed, never multiplied into shared facts or rewritten.
    support = sample.get("prey_support", {})
    prey = {}
    for prey_type, value in support.items():
        if value == 0:
            continue
        prey[prey_type] = {
            "support": value,
            "recent_move_then_pause": _recent_move_pause(mem, t),
            "burst_then_pause": "Match" if mem.burst_event else "NoMatch",
        }
        if prey_type == "frog":
            prey[prey_type]["imbalance_like_sinking"] = mem.imbalance_status

    return {"t": t, "facts": facts, "prey": prey}


def feed(mem, samples):
    out = None
    for sample in samples:
        out = process(mem, sample)
    return out


def series(t0, t1, dt, speed, **kw):
    n = round((t1 - t0) / dt)
    relative_speed = kw.pop("relative_speed", speed)
    return [
        dict(
            t=round(t0 + i * dt, 10),
            world_speed=speed,
            relative_speed=relative_speed,
            **kw,
        )
        for i in range(n + 1)
    ]


def merge_unique(*parts):
    out = {}
    for part in parts:
        for sample in part:
            out[sample["t"]] = sample
    return [out[k] for k in sorted(out)]


def run_acceptance():
    passed = []

    # A sustained movement.
    m = Memory()
    out = feed(m, series(0, 2, .05, .20, surface=True, prey_support={"frog": .9}))
    assert out["facts"]["motion"]["state"] == "moving"
    assert out["prey"]["frog"]["recent_move_then_pause"] == "NoMatch"
    passed.append("A")

    # B move then pause: confirmation is later than semantic segment start.
    m = Memory()
    samples = merge_unique(
        series(0, .60, .05, .20, surface=True, prey_support={"frog": .9}),
        series(.60, 2, .05, 0, surface=True, prey_support={"frog": .9}),
    )
    out = feed(m, samples)
    assert out["facts"]["motion"]["state"] == "low"
    assert isclose(out["facts"]["motion"]["start"], .60, abs_tol=EPS)
    assert isclose(out["facts"]["motion"]["confirmed"], .75, abs_tol=EPS)
    assert isclose(out["facts"]["motion"]["duration"], 1.40, abs_tol=EPS)
    assert out["prey"]["frog"]["recent_move_then_pause"] == "Match"
    passed.append("B")

    # C current pause survives after recent-relation expiry.
    m = Memory()
    samples = merge_unique(
        series(0, .60, .05, .20, surface=True, prey_support={"frog": .9}),
        series(.60, 4, .05, 0, surface=True, prey_support={"frog": .9}),
    )
    out = feed(m, samples)
    assert isclose(out["facts"]["motion"]["duration"], 3.40, abs_tol=EPS)
    assert out["prey"]["frog"]["recent_move_then_pause"] == "NoMatch"
    passed.append("C")

    # D recording starts during pause: movement history is unknown.
    m = Memory()
    out = feed(m, series(0, .20, .05, 0, surface=True, prey_support={"frog": .9}))
    assert out["facts"]["motion"]["state"] == "low"
    assert out["prey"]["frog"]["recent_move_then_pause"] == "Unknown"
    passed.append("D")

    # E hysteresis band does not manufacture transitions.
    m = Memory()
    samples = series(0, .20, .05, .10, prey_support={"frog": .9})
    for i, v in enumerate((.025, .035, .028, .033, .030), start=5):
        samples.append(dict(t=i * .05, world_speed=v, relative_speed=v, prey_support={"frog": .9}))
    out = feed(m, samples)
    assert out["facts"]["motion"]["state"] == "moving"
    passed.append("E")

    # F/G/H sinking with missing/normal/rolled pose.
    for name, roll, expected in (("F", None, "Unknown"), ("G", 0, "NoMatch"), ("H", 75, "Match")):
        m = Memory()
        samples = [
            dict(
                t=round(i * .05, 2),
                world_speed=.05,
                relative_speed=.05,
                vertical_speed=-.05,
                surface=False,
                roll_deg=roll,
                prey_support={"frog": .9},
            )
            for i in range(6)
        ]
        out = feed(m, samples)
        assert out["facts"]["vertical"]["state"] == "falling"
        assert out["prey"]["frog"]["imbalance_like_sinking"] == expected
        passed.append(name)

    # I world motion can coexist with water-relative low motion.
    m = Memory()
    out = feed(
        m,
        [dict(t=i * .05, world_speed=.10, relative_speed=0, prey_support={"frog": .9}) for i in range(5)],
    )
    assert out["facts"]["motion"]["state"] == "moving"
    assert out["facts"]["relative_motion"]["state"] == "low"
    passed.append("I")

    # J a declared gap cannot be counted as a pause or bridge a transition.
    m = Memory()
    samples = series(0, .20, .05, .10, prey_support={"frog": .9})
    samples.append(dict(t=.25, world_speed=.10, relative_speed=.10, gap=True, prey_support={"frog": .9}))
    samples += series(.50, .75, .05, 0, prey_support={"frog": .9})
    out = feed(m, samples)
    assert out["facts"]["motion"]["state"] == "low"
    assert out["prey"]["frog"]["recent_move_then_pause"] != "Match"
    passed.append("J")

    # K shared motion memory continues while one prey type has support zero.
    m = Memory()
    samples = series(0, .20, .05, .20, prey_support={"frog": 0})
    samples += series(.25, .60, .05, 0, prey_support={"frog": 0})
    samples += [dict(t=.65, world_speed=0, relative_speed=0, prey_support={"frog": .9})]
    out = feed(m, samples)
    assert out["prey"]["frog"]["recent_move_then_pause"] == "Match"
    passed.append("K")

    # L new cast starts a new continuity segment.
    m = Memory()
    samples = merge_unique(
        series(0, .20, .05, .20, prey_support={"frog": .9}),
        series(.20, .50, .05, 0, prey_support={"frog": .9}),
    )
    feed(m, samples)
    out = feed(
        m,
        [
            dict(t=.55, world_speed=0, relative_speed=0, continuity_id="cast-2", prey_support={"frog": .9}),
            dict(t=.75, world_speed=0, relative_speed=0, continuity_id="cast-2", prey_support={"frog": .9}),
        ],
    )
    assert out["prey"]["frog"]["recent_move_then_pause"] == "Unknown"
    passed.append("L")

    # M two prey interpretations reference one shared fact packet.
    m = Memory()
    out = feed(
        m,
        series(0, .20, .05, .10, near_bottom=True, prey_support={"small_baitfish": .9, "crayfish": .75}),
    )
    assert set(out["prey"]) == {"small_baitfish", "crayfish"}
    assert out["facts"]["near_bottom"]
    passed.append("M")

    # N ordered burst then pause; the rule is not an unordered window test.
    m = Memory()
    samples = [
        dict(t=0, world_speed=0, relative_speed=0, prey_support={"frog": .9}),
        dict(t=.10, world_speed=.25, relative_speed=.25, prey_support={"frog": .9}),
        dict(t=.30, world_speed=0, relative_speed=0, prey_support={"frog": .9}),
        dict(t=.45, world_speed=0, relative_speed=0, prey_support={"frog": .9}),
    ]
    out = feed(m, samples)
    assert out["prey"]["frog"]["burst_then_pause"] == "Match"
    passed.append("N")

    # O whole-stream and chunked delivery converge; duplicate overlap is idempotent.
    samples = merge_unique(
        series(0, .60, .05, .20, prey_support={"frog": .9}),
        series(.60, 2, .05, 0, prey_support={"frog": .9}),
    )
    m1 = Memory()
    o1 = feed(m1, samples)
    m2 = Memory()
    feed(m2, samples[:10])
    feed(m2, samples[9:25])
    o2 = feed(m2, samples[24:])
    for key in ("state", "start", "confirmed", "duration"):
        a = o1["facts"]["motion"].get(key)
        b = o2["facts"]["motion"].get(key)
        assert a == b or (isinstance(a, float) and isclose(a, b, abs_tol=EPS))
    assert o1["prey"]["frog"]["recent_move_then_pause"] == o2["prey"]["frog"]["recent_move_then_pause"]
    passed.append("O")

    # P surface and near-bottom can coexist; local source rebind clears source-bound events.
    m = Memory()
    samples = [
        dict(t=0, world_speed=0, relative_speed=0, surface=True, near_bottom=True, source_version="skirt-v1", prey_support={"crayfish": .75}),
        dict(t=.10, world_speed=.25, relative_speed=.25, surface=True, near_bottom=True, source_version="skirt-v1", prey_support={"crayfish": .75}),
        dict(t=.30, world_speed=0, relative_speed=0, surface=True, near_bottom=True, source_version="skirt-v1", prey_support={"crayfish": .75}),
        dict(t=.45, world_speed=0, relative_speed=0, surface=True, near_bottom=True, source_version="skirt-v1", prey_support={"crayfish": .75}),
        dict(t=.50, world_speed=0, relative_speed=0, surface=True, near_bottom=True, source_version="skirt-v2", prey_support={"crayfish": .75}),
    ]
    out = feed(m, samples)
    assert out["facts"]["surface"] and out["facts"]["near_bottom"]
    assert out["prey"]["crayfish"]["burst_then_pause"] == "NoMatch"
    assert out["facts"]["source_version"] == "skirt-v2"
    passed.append("P")

    return passed


if __name__ == "__main__":
    passed = run_acceptance()
    print("Step-3 acceptance passed:", " ".join(passed))
