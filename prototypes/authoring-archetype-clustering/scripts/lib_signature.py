# -*- coding: utf-8 -*-
"""
Effect Signature computation, strictly following the 0.3.4 / Bake DSL Core
Spec R0 evaluation semantics (range_fit LINEAR + SMOOTHSTEP), the
AffinityTierScale anchors, and the 5-period TimePeriod catalog.

Sources (Notion, read 2026-09-15):
- Bake DSL Core Spec R0: id 已移除
- 0.3.4.0 开发需求 (config table, tier scale): id 已移除
- 中鱼机制 0.3.4 main (5.2 / 5.4.8): id 已移除
"""
from __future__ import annotations

import numpy as np

# ---------------------------------------------------------------- contract

TEMP_GRID = np.arange(0, 40.5, 0.5)  # sampling grid in degC (81 points)

TIME_PERIODS = ["DAWN", "MORNING", "AFTERNOON", "DUSK", "NIGHT"]

FEEDING_LAYERS = ["SURFACE", "MIDDLE", "BOTTOM"]

# Shared AffinityTierScale (开发需求 3.2.1): tier -> (min, anchor, max)
TIER_SCALE = {
    "最优": (1.00, 1.00, 1.00),
    "次优": (0.50, 0.60, 0.75),
    "较差": (0.20, 0.25, 0.30),
    "不适": (0.00, 0.05, 0.10),
}


def tier_anchor(tier: str) -> float:
    return TIER_SCALE[tier][1]


def resolve_affinity(tier: str, fine_tune: float = 0.0) -> float:
    """tier + fine_tune in [-1,+1] -> float, piecewise linear within the
    tier band (per 开发需求 3.2.1)."""
    lo, anchor, hi = TIER_SCALE[tier]
    t = max(-1.0, min(1.0, fine_tune))
    return anchor + (t * ((hi - anchor) if t > 0 else (anchor - lo)))


# ------------------------------------------------------------- range_fit

def range_fit(x: float, a: float, b: float, c: float, d: float,
              shape: str = "LINEAR") -> float:
    """Bake DSL Core Spec R0 range_fit().

    a=temp_accept_min, b=temp_fav_min, c=temp_fav_max, d=temp_accept_max.
    fit=1 on [b,c], 0 outside [a,d], linear or smoothstep in transitions.
    """
    if x < a or x > d:
        return 0.0
    if b <= x <= c:
        return 1.0
    if x < b:
        if b == a:
            return 1.0 if x >= b else 0.0
        u = (x - a) / (b - a)
    else:
        if d == c:
            return 1.0
        u = (d - x) / (d - c)
    if shape == "SMOOTHSTEP":
        return u * u * (3.0 - 2.0 * u)
    return u


def temperature_signature(a: float, b: float, c: float, d: float,
                          shape: str = "LINEAR") -> np.ndarray:
    """81-dim TemperatureEffectSignature sampled on TEMP_GRID."""
    assert a <= b <= c <= d, f"invalid temp bounds {a},{b},{c},{d}"
    return np.array([range_fit(x, a, b, c, d, shape) for x in TEMP_GRID])


# ------------------------------------------------- derivation helpers

def derive_comfort_from_fav(fav: float, a: float, d: float,
                            half_width_frac: float = 0.15) -> tuple[float, float]:
    """DERIVED rule (this probe only, documented in input_schema.md):
    comfort band centred on the source 'favourite temperature' with
    half-width = 15% of the acceptable width. Clamped inside [a, d]."""
    half = half_width_frac * (d - a)
    b = max(a, fav - half)
    c = min(d, fav + half)
    if b > c:  # extremely narrow acceptable range
        mid = (a + d) / 2
        b = c = mid
    return b, c
