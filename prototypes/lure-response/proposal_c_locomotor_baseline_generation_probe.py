"""Working probe for Proposal C locomotor baseline generation.

This is not production calibration. It only checks authoring topology:
- archetype reference capacity
- monotonic sublinear size scaling
- sparse species/stage overrides
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Archetype:
    name: str
    reference_capacity: float


# Probe-only relative reference capacities. Not production values.
ARCHETYPES = {
    "streamlined_fast": Archetype("streamlined_fast", 1.20),
    "active_generalist": Archetype("active_generalist", 1.00),
    "burst_ambush": Archetype("burst_ambush", 1.05),
    "draggy_slow": Archetype("draggy_slow", 0.80),
    "benthic_low_mobility": Archetype("benthic_low_mobility", 0.65),
}


def size_scale(length_cm: float, reference_length_cm: float = 30.0, exponent: float = 0.5) -> float:
    """Probe-only monotonic sublinear curve.

    exponent=0.5 is deliberately a fixture, not a proposed production exponent.
    """
    assert length_cm > 0
    assert reference_length_cm > 0
    assert 0 < exponent < 1
    return (length_cm / reference_length_cm) ** exponent


def locomotor_baseline(
    archetype: str,
    length_cm: float,
    species_override: float = 1.0,
    stage_override: float = 1.0,
) -> float:
    a = ARCHETYPES[archetype]
    return (
        a.reference_capacity
        * size_scale(length_cm)
        * species_override
        * stage_override
    )


def run_assertions() -> None:
    # Same archetype: absolute capacity should rise with size.
    small = locomotor_baseline("active_generalist", 15)
    medium = locomotor_baseline("active_generalist", 30)
    large = locomotor_baseline("active_generalist", 60)
    assert small < medium < large

    # Growth is sublinear: doubling length does not double capacity.
    assert large / medium < 2.0

    # Archetype ordering survives at the same size.
    fast = locomotor_baseline("streamlined_fast", 30)
    normal = locomotor_baseline("active_generalist", 30)
    benthic = locomotor_baseline("benthic_low_mobility", 30)
    assert fast > normal > benthic

    # Sparse override changes only the exceptional species/stage.
    base = locomotor_baseline("active_generalist", 30)
    species_high = locomotor_baseline("active_generalist", 30, species_override=1.15)
    stage_low = locomotor_baseline("active_generalist", 30, stage_override=0.85)
    assert species_high > base > stage_low

    print("locomotor baseline generation topology assertions passed")


if __name__ == "__main__":
    run_assertions()
