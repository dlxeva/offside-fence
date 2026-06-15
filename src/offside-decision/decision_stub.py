"""
Offside decision stub — tactical state engine.

This is a reference function signature for the offside decision layer of
OffsideFence. It is NOT an implementation. It exists so that a reader can
confirm the function signature matches the architecture in
`docs/architecture.md` and the protocol in `spec/ofp-protocol.md`.

A real implementation would:
  - consume per-frame homography-transformed player positions,
  - identify the last defender (excluding the goalkeeper, excluding the
    player under evaluation),
  - identify the ball-played frame timestamp,
  - return a Decision with offside boolean, confidence float, and the
    recommended actuator intensity for the current operating mode.

This stub raises NotImplementedError by design. See `src/README.md` for
the boundary this stub holds.
"""

from dataclasses import dataclass
from enum import Enum


class Mode(Enum):
    """Operating mode of the haptic tactical correction collar."""
    TRAINING = 0x01
    MATCH = 0x02
    DARWIN = 0x03
    INZAGHI_LEGACY = 0x04  # silence by design


class DecisionOutcome(Enum):
    """Outcome of a single decision evaluation."""
    ON = 0x01       # onside
    OFF = 0x02      # offside
    NONE = 0x00     # no decision (e.g., no ball-played frame detected)


@dataclass(frozen=True)
class PitchPosition:
    """Top-down pitch coordinates, in meters from the center spot."""
    x: float  # attacking direction is positive
    y: float


@dataclass(frozen=True)
class Decision:
    """The output of a single decision evaluation."""
    outcome: DecisionOutcome
    confidence: float          # 0.0 – 1.0
    intensity: int             # 0 – 255, recommended actuator intensity
    repeat_count: int = 0      # for Darwin mode, repeat-offense count in match


def decide(
    forward_pos: PitchPosition,
    last_defender_pos: PitchPosition,
    ball_played_at_ns: int,
    mode: Mode,
    repeat_count: int = 0,
) -> Decision:
    """
    Decide whether `forward_pos` is offside at the moment the ball was played.

    Parameters
    ----------
    forward_pos : PitchPosition
        Top-down position of the forward under evaluation, in meters.
    last_defender_pos : PitchPosition
        Top-down position of the last defender (excluding goalkeeper,
        excluding the forward), in meters. In a real implementation, the
        choice of which defender is "last" would itself be a tracked
        state, not a single function argument.
    ball_played_at_ns : int
        Wall-clock timestamp of the ball-played frame, in nanoseconds.
    mode : Mode
        Current operating mode of the collar.
    repeat_count : int
        Repeat-offense count in the current match, used by Darwin mode.

    Returns
    -------
    Decision
        The offside decision, with confidence and recommended intensity.

    Notes
    -----
    A real implementation would:
      - apply the per-mode threshold and confidence requirement,
      - apply the Inzaghi Legacy override (return Decision(NONE, 1.0, 0)),
      - apply the Darwin intensity curve,
      - include the player under evaluation in the per-mode threshold
        calculation (forward vs. last defender, not just the forward's
        position in absolute terms),
      - emit the decision packet on the OFP/0.1 wire format.

    This stub does not implement any of the above. It raises
    NotImplementedError. The signature is the documentation.
    """
    raise NotImplementedError(
        "decision_stub is a reference signature, not an implementation. "
        "See src/README.md for the boundary this stub holds."
    )
