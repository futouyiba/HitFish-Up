"""Proposal C step-3 presentation-state interpretation probe.

This is an executable design probe, not a production classifier or biological
claim. Thresholds are authored assumptions from the step-3 handoff and remain
replaceable. The probe keeps common motion memory separate from prey-specific
state interpretation and never computes attraction, capture value, or response.
"""
from dataclasses import dataclass, field
from math import isfinite
from typing import Dict, Iterable, List, Optional, Tuple
import json


# Authored candidate thresholds; not calibrated gameplay values.
MOVE_SPEED = 0.04
MOVE_CONFIRM_SECONDS = 0.10
LOW_SPEED = 0.02
LOW_CONFIRM_SECONDS = 0.15
RECENT_MOVE_WINDOW = 3.0
GAP_TOLERANCE = 0.25
DOWNWARD_SPEED = 0.04
ROLL_ANGLE = 35.0
IMBALANCE_CONFIRM_SECONDS = 0.10


@dataclass(frozen=True)
class Sample:
    t: float
    speed: Optional[float]
    vertical_speed: Optional[float] = 0.0
    roll: Optional[float] = 0.0
    surface_distance: Optional[float] = 0.0
    bottom_distance: Optional[float] = 1.0
    assembly: str = "rig"
    throw: str = "throw-1"
    source_complete: bool = True


@dataclass
class MotionMemory:
    last_t: Optional[float] = None
    last_sample: Optional[Sample] = None
    segment_started_at: Optional[float] = None
    segment_observed_from: Optional[float] = None
    move_condition_since: Optional[float] = None
    low_condition_since: Optional[float] = None
    imbalance_condition_since: Optional[float] = None
    last_move_end: Optional[float] = None
    last_move_start: Optional[float] = None
    current_motion: str = "unknown"
    current_motion_since: Optional[float] = None
    current_imbalance: str = "unknown"
    current_imbalance_since: Optional[float] = None
    gap_before: bool = False
    reset_reason: Optional[str] = None


class InputError(ValueError):
    pass


def _number(value, name):
    if value is None:
        return
    if not isinstance(value, (int, float)) or not isfinite(value):
        raise InputError(f"{name} must be finite or None")


def _validate(sample: Sample):
    _number(sample.t, "t")
    for name in ("speed", "vertical_speed", "roll", "surface_distance", "bottom_distance"):
        _number(getattr(sample, name), name)
    if sample.t < 0:
        raise InputError("t must be non-negative")
    for name in ("speed", "surface_distance", "bottom_distance"):
        value = getattr(sample, name)
        if value is not None and value < 0:
            raise InputError(f"{name} must be non-negative")
    if sample.speed is not None and sample.vertical_speed is not None:
        # Vertical speed is signed: positive means downward.
        pass


def _condition_since(previous: Optional[float], condition: bool, t: float):
    if condition:
        return t if previous is None else previous
    return None


def _confirmed(since: Optional[float], t: float, required: float):
    return since is not None and t - since + 1e-12 >= required


def _motion_label(memory: MotionMemory, sample: Sample):
    if sample.speed is None:
        return "unknown"
    if _confirmed(memory.move_condition_since, sample.t, MOVE_CONFIRM_SECONDS):
        return "moving"
    if _confirmed(memory.low_condition_since, sample.t, LOW_CONFIRM_SECONDS):
        return "low_displacement"
    return memory.current_motion if memory.current_motion in {"moving", "low_displacement"} else "unknown"


def _source_key(sample: Sample):
    return sample.throw, sample.assembly


class Interpreter:
    """Incrementally interpret one continuous presentation stream."""

    def __init__(self, support_map: Dict[str, object]):
        # Preserve caller-owned support values exactly; state does not alter them.
        self.support_map = dict(support_map)
        self.memory = MotionMemory()
        self.rows: List[dict] = []

    def _reset_segment(self, sample: Sample, reason: str):
        self.memory = MotionMemory(
            last_t=sample.t,
            last_sample=sample,
            segment_started_at=sample.t,
            segment_observed_from=sample.t,
            gap_before=reason == "gap",
            reset_reason=reason,
        )

    def _apply(self, sample: Sample):
        m = self.memory
        previous = m.last_sample
        dt = None if previous is None else sample.t - previous.t
        source_changed = previous is not None and _source_key(previous) != _source_key(sample)
        duplicate = previous is not None and sample.t == previous.t
        if previous is not None and sample.t < previous.t:
            raise InputError("records must be ordered by timestamp")
        if duplicate:
            # Exact repeated observations do not advance clocks or event duration.
            if sample != previous:
                raise InputError("conflicting records at the same timestamp")
            return self._row(sample, duplicate=True)
        if source_changed:
            self._reset_segment(sample, "source_change")
            m = self.memory
            previous = None
            dt = None
        elif previous is not None and dt > GAP_TOLERANCE:
            self._reset_segment(sample, "gap")
            m = self.memory
            previous = None
            dt = None
        elif previous is None:
            self._reset_segment(sample, "initial")
            m = self.memory
            previous = None
            dt = None

        if sample.source_complete is False:
            m.gap_before = True
            m.move_condition_since = None
            m.low_condition_since = None
            m.imbalance_condition_since = None
        else:
            if sample.speed is None:
                m.move_condition_since = None
                m.low_condition_since = None
            else:
                moving = sample.speed >= MOVE_SPEED
                low = sample.speed <= LOW_SPEED
                m.move_condition_since = _condition_since(m.move_condition_since, moving, sample.t)
                m.low_condition_since = _condition_since(m.low_condition_since, low, sample.t)
            if sample.vertical_speed is None or sample.roll is None:
                m.imbalance_condition_since = None
            else:
                imbalance = sample.vertical_speed >= DOWNWARD_SPEED and abs(sample.roll) >= ROLL_ANGLE
                m.imbalance_condition_since = _condition_since(
                    m.imbalance_condition_since, imbalance, sample.t
                )

        motion = _motion_label(m, sample)
        if motion != m.current_motion:
            if m.current_motion == "moving" and motion == "low_displacement":
                m.last_move_end = sample.t
            if motion == "moving" and m.move_condition_since is not None:
                m.last_move_start = m.move_condition_since
            m.current_motion_since = sample.t
            m.current_motion = motion
        imbalance = (
            "imbalance_like_downward" if _confirmed(
                m.imbalance_condition_since, sample.t, IMBALANCE_CONFIRM_SECONDS
            ) else "normal_downward" if sample.vertical_speed is not None and sample.vertical_speed >= DOWNWARD_SPEED
            else "not_downward" if sample.vertical_speed is not None else "unknown"
        )
        if imbalance != m.current_imbalance:
            m.current_imbalance_since = sample.t
            m.current_imbalance = imbalance
        m.last_t = sample.t
        m.last_sample = sample
        return self._row(sample)

    def _row(self, sample: Sample, duplicate=False):
        m = self.memory
        duration = None if m.segment_observed_from is None else sample.t - m.segment_observed_from
        recent_pause = (
            m.current_motion == "low_displacement"
            and m.last_move_end is not None
            and sample.t - m.last_move_end <= RECENT_MOVE_WINDOW
            and not m.gap_before
        )
        imbalance = m.current_imbalance
        states = {}
        for prey, config in self.support_map.items():
            if config is None or config == "not_configured":
                states[prey] = {"status": "not_configured"}
                continue
            if prey == "fish":
                states[prey] = {
                    "status": "matched" if m.current_motion in {"moving", "low_displacement"} else
                              "unknown" if m.current_motion == "unknown" else "unmatched",
                    "motion": m.current_motion,
                    "recent_movement_then_pause": recent_pause,
                }
            elif prey == "crustacean":
                near_bottom = sample.bottom_distance is not None and sample.bottom_distance <= 0.5
                states[prey] = {
                    "status": "matched" if near_bottom and m.current_motion in {"moving", "low_displacement"}
                              else "unknown" if sample.bottom_distance is None or m.current_motion == "unknown"
                              else "unmatched",
                    "near_bottom": near_bottom if sample.bottom_distance is not None else None,
                    "motion": m.current_motion,
                }
            elif prey == "frog":
                if sample.surface_distance is None or sample.vertical_speed is None or sample.roll is None:
                    states[prey] = {"status": "unknown", "motion": m.current_motion}
                elif imbalance == "imbalance_like_downward":
                    states[prey] = {"status": "matched", "state": "imbalance_like_downward",
                                    "motion": m.current_motion}
                elif sample.vertical_speed >= DOWNWARD_SPEED:
                    states[prey] = {"status": "unmatched", "state": "normal_downward",
                                    "motion": m.current_motion}
                else:
                    states[prey] = {"status": "matched", "state": "surface_or_subsurface_motion",
                                    "motion": m.current_motion}
            else:
                states[prey] = {"status": "unknown", "motion": m.current_motion}
        facts = {
            "t": sample.t,
            "speed": sample.speed,
            "vertical_speed": sample.vertical_speed,
            "roll": sample.roll,
            "surface_distance": sample.surface_distance,
            "bottom_distance": sample.bottom_distance,
            "motion": m.current_motion,
            "motion_duration": duration,
            "motion_duration_is_lower_bound": m.segment_observed_from == sample.t,
            "recent_move_start": m.last_move_start,
            "recent_move_end": m.last_move_end,
            "gap_before": m.gap_before,
            "duplicate": duplicate,
            "reset_reason": m.reset_reason,
        }
        return {"facts": facts, "states": states, "support_map": dict(self.support_map)}

    def feed(self, sample: Sample):
        _validate(sample)
        row = self._apply(sample)
        self.rows.append(row)
        return row

    def finish(self):
        return {"support_map": dict(self.support_map), "rows": list(self.rows)}


def run(samples: Iterable[Sample], support_map=None):
    support_map = {"fish": 0.9, "crustacean": 0.5, "frog": 0.9} if support_map is None else support_map
    interpreter = Interpreter(support_map)
    for sample in samples:
        interpreter.feed(sample)
    return interpreter.finish()


def _series(start, end, step, **kwargs):
    count = round((end - start) / step)
    return [Sample(t=start + i * step, **kwargs) for i in range(count + 1)]


def _state(result, prey, index=-1):
    return result["rows"][index]["states"][prey]


def build_acceptance_cases():
    moving = _series(0, .20, .05, speed=.08)
    pause = _series(0, .20, .05, speed=.08) + _series(.25, .50, .05, speed=0.0)
    return {
        "continuous_movement": moving,
        "movement_then_pause": pause,
        "recent_pause_expired": pause + _series(3.55, 3.55, .05, speed=0.0),
        "insufficient_history": [Sample(.8, speed=0.0)],
        "threshold_jitter": [Sample(t, speed=v) for t, v in ((0,.05),(.05,.05),(.10,.05),(.15,.03),(.20,.03),(.25,.05))],
        "missing_roll": [Sample(0, speed=.02, vertical_speed=.08, roll=None), Sample(.15, speed=.02, vertical_speed=.08, roll=None)],
        "normal_downward": [Sample(0, speed=.02, vertical_speed=.08, roll=0), Sample(.15, speed=.02, vertical_speed=.08, roll=0)],
        "imbalance_downward": [Sample(0, speed=.02, vertical_speed=.08, roll=45), Sample(.15, speed=.02, vertical_speed=.08, roll=45)],
        "water_drift": [Sample(0, speed=None, vertical_speed=0, roll=0), Sample(.15, speed=None, vertical_speed=0, roll=0)],
        "record_gap": [Sample(0, speed=.08), Sample(.10, speed=.08), Sample(1.0, speed=0)],
        "type_reentry": [Sample(0, speed=.08), Sample(.15, speed=.08)],
        "multi_type": [Sample(0, speed=.08, bottom_distance=.2), Sample(.15, speed=.08, bottom_distance=.2)],
        "composite_order": [Sample(0, speed=.08), Sample(.15, speed=0), Sample(.30, speed=.08)],
        "batch_one": moving,
        "local_rebind": [Sample(0, speed=.08, assembly="a"), Sample(.15, speed=0, assembly="b")],
    }


def checks():
    cases = build_acceptance_cases()
    full = run(cases["movement_then_pause"])
    assert _state(full, "fish")["motion"] == "low_displacement"
    assert _state(full, "fish")["recent_movement_then_pause"] is True
    expired = run(cases["recent_pause_expired"])
    # A sampling gap starts a new segment; it cannot extend the old pause.
    assert _state(expired, "fish")["motion"] == "unknown"
    assert _state(expired, "fish")["recent_movement_then_pause"] is False
    assert _state(run(cases["insufficient_history"]), "fish")["status"] == "unknown"
    assert run(cases["insufficient_history"])["rows"][0]["facts"]["motion_duration_is_lower_bound"] is True
    # Hysteresis: an interval between thresholds retains a confirmed state.
    jitter = run(cases["threshold_jitter"])
    assert _state(jitter, "fish")["motion"] == "moving"
    assert _state(run(cases["missing_roll"]), "frog")["status"] == "unknown"
    assert _state(run(cases["normal_downward"]), "frog")["status"] == "unmatched"
    assert _state(run(cases["imbalance_downward"]), "frog")["state"] == "imbalance_like_downward"
    drift = run(cases["water_drift"])
    assert _state(drift, "fish")["status"] == "unknown"
    gap = run(cases["record_gap"])
    assert gap["rows"][-1]["facts"]["gap_before"] is True
    assert gap["rows"][-1]["facts"]["recent_move_end"] is None
    # Same facts can support more than one interpretation without duplication.
    multi = run(cases["multi_type"])
    assert _state(multi, "fish")["status"] == "matched"
    assert _state(multi, "crustacean")["status"] == "matched"
    assert multi["rows"][-1]["support_map"] == multi["support_map"]
    # A source rebind starts a new continuous segment and does not carry history.
    rebound = run(cases["local_rebind"])
    assert rebound["rows"][-1]["facts"]["reset_reason"] == "source_change"
    assert rebound["rows"][-1]["facts"]["recent_move_end"] is None
    # Duplicate records neither double-count duration nor mutate state.
    duplicate = run([Sample(0, speed=.08), Sample(.1, speed=.08), Sample(.1, speed=.08)])
    assert duplicate["rows"][-1]["facts"]["duplicate"] is True
    assert duplicate["rows"][-1]["facts"]["motion_duration"] == .1
    # Whole-stream and incremental batches are identical.
    one = run(cases["batch_one"])
    inc = Interpreter(one["support_map"])
    for sample in cases["batch_one"][:3]:
        inc.feed(sample)
    for sample in cases["batch_one"][3:]:
        inc.feed(sample)
    assert inc.finish() == one
    # Newly observed segments retain a lower-bound duration marker.
    assert run([Sample(.8, speed=0)])['rows'][0]['facts']['motion_duration_is_lower_bound'] is True
    # Conflicting same-time data is rejected, while out-of-order data is rejected.
    try:
        run([Sample(0, speed=.1), Sample(0, speed=0)])
    except InputError:
        pass
    else:
        raise AssertionError("conflicting same-time input was accepted")
    try:
        run([Sample(.1, speed=.1), Sample(0, speed=.1)])
    except InputError:
        pass
    else:
        raise AssertionError("out-of-order input was accepted")


if __name__ == "__main__":
    checks()
    print("All proposal-C step-3 acceptance checks passed.")
    print(json.dumps(run(build_acceptance_cases()["movement_then_pause"]), ensure_ascii=False, indent=2))
