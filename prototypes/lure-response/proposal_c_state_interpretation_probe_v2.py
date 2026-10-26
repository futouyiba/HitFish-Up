"""Proposal C step-3 closure probe.

Shared presentation facts are maintained independently of prey support.
Prey-conditioned interpretation consumes those facts without rewriting them.
Thresholds are working design assumptions from proposal C section 5.
"""
from dataclasses import dataclass, field
from math import isclose

MOVE_ENTER, MOVE_HOLD = 0.04, 0.10
LOW_ENTER, LOW_HOLD = 0.02, 0.15
RECENT_PAUSE = 3.0
VERT_ENTER, VERT_LOW, VERT_HOLD = 0.02, 0.01, 0.15
IMBALANCE_ROLL, IMBALANCE_HOLD = 60.0, 0.20
EPS = 1e-9

@dataclass
class Segment:
    kind: str
    start: float
    confirmed: float
    end: float | None = None
    observed_lower_bound: bool = False
    def duration_at(self, t: float) -> float:
        return (self.end if self.end is not None else t) - self.start

@dataclass
class AxisState:
    confirmed: str | None = None
    segment: Segment | None = None
    candidate_kind: str | None = None
    candidate_start: float | None = None
    last_closed: Segment | None = None
    first_observation_t: float | None = None

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
    previous_speed: float | None = None
    previous_t: float | None = None
    burst_high_t: float | None = None
    burst_low_after_t: float | None = None
    burst_event: TemporalEvent | None = None
    imbalance_candidate_start: float | None = None
    imbalance_status: str = "Unknown"

    def reset_continuity(self, continuity_id: str):
        self.continuity_id = continuity_id
        self.last_t = None
        self.last_signature = None
        self.motion = AxisState()
        self.relative_motion = AxisState()
        self.vertical = AxisState()
        self.previous_speed = self.previous_t = None
        self.burst_high_t = self.burst_low_after_t = None
        self.burst_event = None
        self.imbalance_candidate_start = None
        self.imbalance_status = "Unknown"

    def rebind_source(self, version: str):
        if self.source_version != version:
            self.source_version = version
            self.burst_high_t = self.burst_low_after_t = None
            self.burst_event = None


def _update_axis(axis, t, value, hi_kind, lo_kind, hi_thr, lo_thr, hi_hold, lo_hold):
    if axis.first_observation_t is None:
        axis.first_observation_t = t
    if value >= hi_thr:
        cand, hold = hi_kind, hi_hold
    elif value <= lo_thr:
        cand, hold = lo_kind, lo_hold
    else:
        axis.candidate_kind = axis.candidate_start = None
        return
    if axis.confirmed == cand:
        axis.candidate_kind = axis.candidate_start = None
        return
    if axis.candidate_kind != cand:
        axis.candidate_kind, axis.candidate_start = cand, t
        return
    if t - axis.candidate_start + EPS >= hold:
        if axis.segment is not None:
            axis.segment.end = axis.candidate_start
            axis.last_closed = axis.segment
        lower_bound = axis.confirmed is None and isclose(axis.candidate_start, axis.first_observation_t, abs_tol=EPS)
        axis.confirmed = cand
        axis.segment = Segment(cand, axis.candidate_start, t, observed_lower_bound=lower_bound)
        axis.candidate_kind = axis.candidate_start = None


def _update_vertical(axis, t, vz):
    if axis.first_observation_t is None:
        axis.first_observation_t = t
    if vz >= VERT_ENTER:
        cand = "rising"
    elif vz <= -VERT_ENTER:
        cand = "falling"
    elif abs(vz) <= VERT_LOW:
        cand = "vertical_low"
    else:
        axis.candidate_kind = axis.candidate_start = None
        return
    if axis.confirmed == cand:
        axis.candidate_kind = axis.candidate_start = None
        return
    if axis.candidate_kind != cand:
        axis.candidate_kind, axis.candidate_start = cand, t
        return
    if t - axis.candidate_start + EPS >= VERT_HOLD:
        if axis.segment is not None:
            axis.segment.end = axis.candidate_start
            axis.last_closed = axis.segment
        lower_bound = axis.confirmed is None and isclose(axis.candidate_start, axis.first_observation_t, abs_tol=EPS)
        axis.confirmed = cand
        axis.segment = Segment(cand, axis.candidate_start, t, observed_lower_bound=lower_bound)
        axis.candidate_kind = axis.candidate_start = None


def _axis_packet(axis, t):
    if axis.segment is None:
        return {"state": axis.confirmed}
    return {
        "state": axis.confirmed,
        "start": axis.segment.start,
        "confirmed": axis.segment.confirmed,
        "duration": axis.segment.duration_at(t),
        "duration_semantics": "observed_lower_bound" if axis.segment.observed_lower_bound else "known_segment_start",
    }


def _recent_move_pause(mem, t):
    if mem.motion.confirmed != "low" or mem.motion.segment is None:
        return "NoMatch"
    prev = mem.motion.last_closed
    if prev is None or prev.kind != "moving":
        return "Unknown"
    return "Match" if t - prev.end <= RECENT_PAUSE + EPS else "NoMatch"


def snapshot(mem, sample):
    t = float(sample["t"])
    facts = {
        "world_speed": sample.get("world_speed"),
        "relative_speed": sample.get("relative_speed"),
        "motion": _axis_packet(mem.motion, t),
        "relative_motion": _axis_packet(mem.relative_motion, t),
        "vertical": _axis_packet(mem.vertical, t),
        "surface": bool(sample.get("surface", False)),
        "near_bottom": bool(sample.get("near_bottom", False)),
        "source_version": mem.source_version,
        "continuity_id": mem.continuity_id,
    }
    prey = {}
    for prey_type, support in sample.get("prey_support", {}).items():
        if support == 0:
            continue
        packet = {
            "support": support,
            "recent_move_then_pause": _recent_move_pause(mem, t),
            "burst_then_pause": "Match" if mem.burst_event else "NoMatch",
        }
        if prey_type == "frog":
            packet["imbalance_like_sinking"] = mem.imbalance_status
        prey[prey_type] = packet
    return {"t": t, "facts": facts, "prey": prey}


def process(mem, sample):
    t = float(sample["t"])
    continuity_id = sample.get("continuity_id", "cast-1")
    version = sample.get("source_version", "v1")
    if mem.continuity_id != continuity_id:
        mem.reset_continuity(continuity_id)
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
        mem.motion = AxisState(); mem.relative_motion = AxisState(); mem.vertical = AxisState()
        mem.previous_speed = mem.previous_t = None
        mem.burst_high_t = mem.burst_low_after_t = None; mem.burst_event = None
        mem.imbalance_candidate_start = None; mem.imbalance_status = "Unknown"
        mem.last_t, mem.last_signature = t, sig
        return snapshot(mem, sample)
    v = float(sample["world_speed"]); rv = sample.get("relative_speed"); vz = float(sample.get("vertical_speed", 0.0))
    _update_axis(mem.motion, t, v, "moving", "low", MOVE_ENTER, LOW_ENTER, MOVE_HOLD, LOW_HOLD)
    if rv is not None:
        _update_axis(mem.relative_motion, t, float(rv), "moving", "low", MOVE_ENTER, LOW_ENTER, MOVE_HOLD, LOW_HOLD)
    _update_vertical(mem.vertical, t, vz)
    if mem.previous_speed is not None and mem.previous_t is not None:
        if mem.previous_speed <= MOVE_ENTER and v >= 0.20 and t - mem.previous_t <= 0.15 + EPS:
            mem.burst_high_t, mem.burst_low_after_t = t, None
        if mem.burst_high_t is not None and v <= LOW_ENTER and 0 <= t - mem.burst_high_t <= 0.50 + EPS and mem.burst_low_after_t is None:
            mem.burst_low_after_t = t
        if mem.burst_low_after_t is not None and v <= LOW_ENTER and t - mem.burst_low_after_t >= LOW_HOLD - EPS:
            mem.burst_event = TemporalEvent("burst_then_pause", mem.burst_high_t, t, mem.source_version)
        elif mem.burst_low_after_t is not None and v > LOW_ENTER:
            mem.burst_low_after_t = None
    roll = sample.get("roll_deg")
    if vz <= -0.02:
        if roll is None:
            mem.imbalance_candidate_start = None; mem.imbalance_status = "Unknown"
        elif abs(float(roll)) > IMBALANCE_ROLL:
            if mem.imbalance_candidate_start is None: mem.imbalance_candidate_start = t
            if t - mem.imbalance_candidate_start + EPS >= IMBALANCE_HOLD: mem.imbalance_status = "Match"
        else:
            mem.imbalance_candidate_start = None; mem.imbalance_status = "NoMatch"
    else:
        mem.imbalance_candidate_start = None; mem.imbalance_status = "NoMatch"
    mem.previous_speed, mem.previous_t = v, t
    mem.last_t, mem.last_signature = t, sig
    return snapshot(mem, sample)


def feed(mem, samples):
    out = None
    for s in samples: out = process(mem, s)
    return out

def series(t0, t1, dt, speed, **kw):
    n = round((t1-t0)/dt); rv = kw.pop("relative_speed", speed)
    return [dict(t=round(t0+i*dt,10), world_speed=speed, relative_speed=rv, **kw) for i in range(n+1)]
def merge_unique(*parts):
    d={}
    for part in parts:
        for s in part: d[s["t"]]=s
    return [d[k] for k in sorted(d)]


def run_acceptance():
    passed=[]
    m=Memory(); out=feed(m,series(0,2,.05,.20,surface=True,prey_support={"frog":.9})); assert out["facts"]["motion"]["state"]=="moving" and out["facts"]["motion"]["duration_semantics"]=="observed_lower_bound" and out["prey"]["frog"]["recent_move_then_pause"]=="NoMatch"; passed.append("A")
    m=Memory(); out=feed(m,merge_unique(series(0,.60,.05,.20,surface=True,prey_support={"frog":.9}),series(.60,2,.05,0,surface=True,prey_support={"frog":.9}))); mp=out["facts"]["motion"]; assert mp["state"]=="low" and isclose(mp["start"],.60,abs_tol=EPS) and isclose(mp["confirmed"],.75,abs_tol=EPS) and isclose(mp["duration"],1.40,abs_tol=EPS) and mp["duration_semantics"]=="known_segment_start" and out["prey"]["frog"]["recent_move_then_pause"]=="Match"; passed.append("B")
    m=Memory(); out=feed(m,merge_unique(series(0,.60,.05,.20,surface=True,prey_support={"frog":.9}),series(.60,4,.05,0,surface=True,prey_support={"frog":.9}))); assert isclose(out["facts"]["motion"]["duration"],3.40,abs_tol=EPS) and out["prey"]["frog"]["recent_move_then_pause"]=="NoMatch"; passed.append("C")
    m=Memory(); out=feed(m,series(0,.20,.05,0,surface=True,prey_support={"frog":.9})); assert out["facts"]["motion"]["state"]=="low" and out["facts"]["motion"]["duration_semantics"]=="observed_lower_bound" and out["prey"]["frog"]["recent_move_then_pause"]=="Unknown"; passed.append("D")
    m=Memory(); ss=series(0,.20,.05,.10,prey_support={"frog":.9}); [ss.append(dict(t=i*.05,world_speed=v,relative_speed=v,prey_support={"frog":.9})) for i,v in enumerate((.025,.035,.028,.033,.030),start=5)]; out=feed(m,ss); assert out["facts"]["motion"]["state"]=="moving"; passed.append("E")
    for name,roll,expected in (("F",None,"Unknown"),("G",0,"NoMatch"),("H",75,"Match")):
        m=Memory(); ss=[dict(t=round(i*.05,2),world_speed=.05,relative_speed=.05,vertical_speed=-.05,surface=False,roll_deg=roll,prey_support={"frog":.9}) for i in range(6)]; out=feed(m,ss); assert out["facts"]["vertical"]["state"]=="falling" and out["prey"]["frog"]["imbalance_like_sinking"]==expected; passed.append(name)
    m=Memory(); out=feed(m,[dict(t=i*.05,world_speed=.10,relative_speed=0,prey_support={"frog":.9}) for i in range(5)]); assert out["facts"]["motion"]["state"]=="moving" and out["facts"]["relative_motion"]["state"]=="low"; passed.append("I")
    m=Memory(); ss=series(0,.20,.05,.10,prey_support={"frog":.9}); ss.append(dict(t=.25,world_speed=.10,relative_speed=.10,gap=True,prey_support={"frog":.9})); ss+=series(.50,.75,.05,0,prey_support={"frog":.9}); out=feed(m,ss); assert out["facts"]["motion"]["state"]=="low" and out["facts"]["motion"]["duration_semantics"]=="observed_lower_bound" and out["prey"]["frog"]["recent_move_then_pause"]=="Unknown"; passed.append("J")
    m=Memory(); ss=series(0,.20,.05,.20,prey_support={"frog":0})+series(.25,.60,.05,0,prey_support={"frog":0})+[dict(t=.65,world_speed=0,relative_speed=0,prey_support={"frog":.9})]; out=feed(m,ss); assert out["prey"]["frog"]["recent_move_then_pause"]=="Match"; passed.append("K")
    m=Memory(); feed(m,merge_unique(series(0,.20,.05,.20,prey_support={"frog":.9}),series(.20,.50,.05,0,prey_support={"frog":.9}))); out=feed(m,[dict(t=.55,world_speed=0,relative_speed=0,continuity_id="cast-2",prey_support={"frog":.9}),dict(t=.75,world_speed=0,relative_speed=0,continuity_id="cast-2",prey_support={"frog":.9})]); assert out["prey"]["frog"]["recent_move_then_pause"]=="Unknown" and out["facts"]["motion"]["duration_semantics"]=="observed_lower_bound"; passed.append("L")
    m=Memory(); out=feed(m,series(0,.20,.05,.10,near_bottom=True,prey_support={"small_baitfish":.9,"crayfish":.75})); assert set(out["prey"])=={"small_baitfish","crayfish"} and out["facts"]["near_bottom"]; passed.append("M")
    m=Memory(); ss=[dict(t=0,world_speed=0,relative_speed=0,prey_support={"frog":.9}),dict(t=.10,world_speed=.25,relative_speed=.25,prey_support={"frog":.9}),dict(t=.30,world_speed=0,relative_speed=0,prey_support={"frog":.9}),dict(t=.45,world_speed=0,relative_speed=0,prey_support={"frog":.9})]; out=feed(m,ss); assert out["prey"]["frog"]["burst_then_pause"]=="Match"; passed.append("N")
    ss=merge_unique(series(0,.60,.05,.20,prey_support={"frog":.9}),series(.60,2,.05,0,prey_support={"frog":.9})); m1=Memory(); o1=feed(m1,ss); m2=Memory(); feed(m2,ss[:10]); feed(m2,ss[9:25]); o2=feed(m2,ss[24:]); assert o1==o2; passed.append("O")
    m=Memory(); ss=[dict(t=0,world_speed=0,relative_speed=0,surface=True,near_bottom=True,source_version="skirt-v1",prey_support={"crayfish":.75}),dict(t=.10,world_speed=.25,relative_speed=.25,surface=True,near_bottom=True,source_version="skirt-v1",prey_support={"crayfish":.75}),dict(t=.30,world_speed=0,relative_speed=0,surface=True,near_bottom=True,source_version="skirt-v1",prey_support={"crayfish":.75}),dict(t=.45,world_speed=0,relative_speed=0,surface=True,near_bottom=True,source_version="skirt-v1",prey_support={"crayfish":.75}),dict(t=.50,world_speed=0,relative_speed=0,surface=True,near_bottom=True,source_version="skirt-v2",prey_support={"crayfish":.75})]; out=feed(m,ss); assert out["facts"]["surface"] and out["facts"]["near_bottom"] and out["prey"]["crayfish"]["burst_then_pause"]=="NoMatch" and out["facts"]["source_version"]=="skirt-v2"; passed.append("P")
    return passed

if __name__=="__main__":
    p=run_acceptance(); print("Step-3 acceptance passed:"," ".join(p))
