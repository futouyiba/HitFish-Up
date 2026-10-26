"""Working probe for Proposal C escape-like state feature routing.

Purpose:
- keep positive prey-state trigger evidence separate from temporal/capture effects;
- avoid treating generic irregularity or pause as direct bonuses;
- demonstrate a minimal generic feature set: redirection events + burst events,
  with alternation / timing irregularity used only as interpretation confidence.

Not a production formula.
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, pstdev


def sat(x: float, half: float) -> float:
    if x <= 0:
        return 0.0
    return x / (x + half)


@dataclass(frozen=True)
class Pattern:
    name: str
    turn_events_deg: tuple[float, ...]
    burst_delta_v: tuple[float, ...]
    turn_signs: tuple[int, ...]
    event_times_s: tuple[float, ...]


def evaluate(pattern: Pattern) -> dict[str, float]:
    turns = [max(0.0, d - 10.0) for d in pattern.turn_events_deg]
    redirection = sat(mean(turns) / 60.0 if turns else 0.0, 0.35)
    burst = sat(mean(pattern.burst_delta_v) if pattern.burst_delta_v else 0.0, 0.35)

    if len(pattern.turn_signs) >= 2:
        alternations = sum(
            1
            for a, b in zip(pattern.turn_signs, pattern.turn_signs[1:])
            if a != b
        )
        alternation_ratio = alternations / (len(pattern.turn_signs) - 1)
    else:
        alternation_ratio = 0.0

    if len(pattern.event_times_s) >= 3:
        intervals = [
            b - a for a, b in zip(pattern.event_times_s, pattern.event_times_s[1:])
        ]
        timing_cv = pstdev(intervals) / max(mean(intervals), 1e-9)
        timing_irregularity = sat(timing_cv, 0.5)
    else:
        timing_irregularity = 0.0

    # Working interpretation-confidence projection only.
    confidence = 0.6 + 0.2 * alternation_ratio + 0.2 * timing_irregularity

    # Working generic evidence strength. Pause is intentionally absent.
    base_evidence = 0.65 * redirection + 0.35 * burst
    escape_like_support = base_evidence * confidence

    return {
        "redirection_event_strength": redirection,
        "burst_event_strength": burst,
        "alternation_ratio": alternation_ratio,
        "timing_irregularity": timing_irregularity,
        "interpretation_confidence": confidence,
        "escape_like_support": escape_like_support,
    }


PATTERNS = (
    Pattern("straight", (5, 3), (0.05,), (1, 1), (0.5, 1.5)),
    Pattern("regular_zigzag", (35, 35, 35, 35), (0.25, 0.20), (1, -1, 1, -1), (0.3, 0.7, 1.1, 1.5)),
    Pattern("erratic_escape", (25, 60, 40, 70), (0.50, 0.35, 0.55), (1, -1, 1, -1), (0.15, 0.42, 0.95, 1.48)),
    Pattern("circular", (20, 20, 20, 20, 20), (0.05,), (1, 1, 1, 1, 1), (0.2, 0.5, 0.8, 1.1, 1.4)),
    Pattern("burst_pause", (20, 45), (0.70,), (1, -1), (0.2, 0.45)),
)


if __name__ == "__main__":
    for pattern in PATTERNS:
        result = evaluate(pattern)
        print(pattern.name)
        for key, value in result.items():
            print(f"  {key}: {value:.3f}")
