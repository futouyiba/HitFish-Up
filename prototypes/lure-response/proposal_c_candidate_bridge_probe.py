"""Proposal C → Candidate Resolver bridge probe.

Purpose:
- verify Complete Mode responses are composed inside Interaction first;
- expose one support-local CaptureRetention to Candidate Resolver;
- join Spatial Native Supply with CaptureRetention exactly once;
- keep ResolutionIncomplete distinct from resolved zero;
- reject treating native Interaction response as a later gameplay-policy modifier.

All numeric values are illustrative topology probes, not calibrated production values.
"""

from dataclasses import dataclass
from enum import Enum


class Status(str, Enum):
    INCOMPLETE = "ResolutionIncomplete"
    NONRESPONSIVE = "ResolvedNonResponsive"
    RESPONSIVE = "ResolvedResponsive"


@dataclass(frozen=True)
class ModeResponsePacket:
    mode_id: str
    status: Status
    c_mode: float | None


@dataclass(frozen=True)
class CaptureResponsePacket:
    status: Status
    capture_retention: float | None
    winning_mode: str | None


def aggregate_declared_alternative_siblings(modes: list[ModeResponsePacket]) -> CaptureResponsePacket:
    """Probe-only max for a group already declared alternative/overlapping siblings."""
    if any(m.status == Status.INCOMPLETE for m in modes):
        return CaptureResponsePacket(Status.INCOMPLETE, None, None)

    resolved = [(m.c_mode or 0.0, m.mode_id, m.status) for m in modes]
    best_c, best_id, best_status = max(resolved, key=lambda x: x[0])
    if best_c <= 0.0:
        return CaptureResponsePacket(Status.NONRESPONSIVE, 0.0, best_id)
    return CaptureResponsePacket(Status.RESPONSIVE, best_c, best_id)


def native_retention_join(spatial_native_supply: float, response: CaptureResponsePacket):
    """Candidate Resolver specialization of dQ = C * dM for one support."""
    if response.status == Status.INCOMPLETE:
        return None
    assert response.capture_retention is not None
    return spatial_native_supply * response.capture_retention


def run_probe():
    # A. Complete sibling modes are composed inside Interaction first.
    feeding_routes = [
        ModeResponsePacket("feeding_baitfish", Status.RESPONSIVE, 0.80),
        ModeResponsePacket("feeding_crayfish", Status.RESPONSIVE, 0.50),
    ]
    interaction = aggregate_declared_alternative_siblings(feeding_routes)
    assert interaction.capture_retention == 0.80
    assert interaction.winning_mode == "feeding_baitfish"

    # B. Candidate Resolver joins Spatial Native Supply and Interaction retention once.
    L = 0.75
    q = native_retention_join(L, interaction)
    assert abs(q - 0.60) < 1e-12

    # Applying the same native response again downstream creates squared attenuation.
    wrong_double_application = q * interaction.capture_retention
    assert abs(wrong_double_application - 0.48) < 1e-12
    assert wrong_double_application != q

    # C. A resolved terminal/non-responsive Interaction outcome can yield native zero.
    no_response = aggregate_declared_alternative_siblings([
        ModeResponsePacket("feeding", Status.NONRESPONSIVE, 0.0)
    ])
    assert no_response.status == Status.NONRESPONSIVE
    assert native_retention_join(L, no_response) == 0.0

    # D. Unknown/incomplete Interaction blocks Candidate closure; it is not zero.
    incomplete = aggregate_declared_alternative_siblings([
        ModeResponsePacket("feeding_baitfish", Status.RESPONSIVE, 0.80),
        ModeResponsePacket("feeding_crayfish", Status.INCOMPLETE, None),
    ])
    assert incomplete.status == Status.INCOMPLETE
    assert incomplete.capture_retention is None
    assert native_retention_join(L, incomplete) is None

    return {
        "interaction_output": "CaptureRetention C_i,j",
        "candidate_join": "q_i,j = L_i,j * C_i,j",
        "double_counting": "rejected",
        "unknown": "ResolutionIncomplete / NotRollable",
        "policy_boundary": "native C is resolved before Pre-Roll Gameplay Policy",
    }


if __name__ == "__main__":
    for key, value in run_probe().items():
        print(f"{key}: {value}")
